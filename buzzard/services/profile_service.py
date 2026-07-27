"""Buzzard Profile Orchestration Service.

Coordinates hardware managers to apply declarative profiles, manage profile state,
handle rollbacks on failure, record history, publish EventBus events, and auto-detect profiles.
"""

from datetime import datetime
import time
from typing import Any, Dict, List, Tuple
from buzzard.core.config import ConfigManager
from buzzard.core.constants import CURRENT_PROFILE_FILE, PREVIOUS_PROFILE_FILE
from buzzard.core.event_bus import EventBus, ProfileAppliedEvent, ProfileFailedEvent
from buzzard.core.logger import Logger
from buzzard.core.result import Result
from buzzard.core.state_machine import ProfileState, ProfileStateMachine
from buzzard.managers import (
    BatteryManager,
    BluetoothManager,
    BrightnessManager,
    CPUManager,
    DisplayManager,
    GPUManager,
    KernelPowerManager,
    PCIeManager,
    PowerProfilesManager,
    PowerTOPManager,
    ProfileManager,
    TLPManager,
    VendorManager,
)
from buzzard.services.history_service import HistoryService
from buzzard.services.logger_service import LoggerService

logger = Logger()


class ProfileService:
    """Service for coordinating profile application, state persistence, and rollback."""

    @classmethod
    def current(cls) -> str:
        """Gets current recorded profile name or detects active hardware profile.

        Returns:
            Profile name string.
        """
        try:
            if CURRENT_PROFILE_FILE.exists():
                name = CURRENT_PROFILE_FILE.read_text(encoding="utf-8").strip()
                if name:
                    return name
        except Exception:
            pass
        return cls.detect_active_profile()

    @classmethod
    def previous(cls) -> str:
        """Gets previously recorded profile name.

        Returns:
            Profile name string or 'None'.
        """
        try:
            if PREVIOUS_PROFILE_FILE.exists():
                name = PREVIOUS_PROFILE_FILE.read_text(encoding="utf-8").strip()
                if name:
                    return name
        except Exception:
            pass
        return "None"

    @classmethod
    def save_state(cls, new_profile: str) -> None:
        """Persists profile application state to ~/.config/buzzard/.

        Args:
            new_profile: Name of newly applied profile.
        """
        try:
            CURRENT_PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
            curr = cls.current()
            if curr and curr != new_profile:
                PREVIOUS_PROFILE_FILE.write_text(curr, encoding="utf-8")
            CURRENT_PROFILE_FILE.write_text(new_profile, encoding="utf-8")
        except Exception as exc:
            logger.error(f"Failed to save profile state: {exc}")

    @classmethod
    def get_hardware_snapshot(cls) -> Dict[str, Any]:
        """Captures a full snapshot of current hardware state.

        Returns:
            Dictionary containing state of all managed subsystems.
        """
        return {
            "gpu": GPUManager.current(),
            "cpu": CPUManager.current(),
            "brightness": BrightnessManager.get(),
            "bluetooth": BluetoothManager.is_enabled(),
            "tlp": TLPManager.status() == "Active",
            "battery_percent": BatteryManager.percent(),
            "battery_status": BatteryManager.status(),
            "ac_connected": BatteryManager.is_ac_connected(),
        }

    @classmethod
    def rollback_state(cls, snapshot: Dict[str, Any]) -> List[Result]:
        """Rolls back hardware settings to captured snapshot.

        Args:
            snapshot: Hardware state dictionary from get_hardware_snapshot().

        Returns:
            List of Result objects from rollback operations.
        """
        rollback_results = []
        logger.warning("Initiating hardware rollback to previous snapshot state...")

        # CPU Governor
        if "cpu" in snapshot and snapshot["cpu"] != "unknown":
            rollback_results.append(CPUManager.set_governor(snapshot["cpu"]))

        # Brightness
        if "brightness" in snapshot:
            rollback_results.append(BrightnessManager.set(int(snapshot["brightness"])))

        # Bluetooth
        if "bluetooth" in snapshot:
            if snapshot["bluetooth"]:
                rollback_results.append(BluetoothManager.enable())
            else:
                rollback_results.append(BluetoothManager.disable())

        # TLP
        if "tlp" in snapshot:
            if snapshot["tlp"]:
                rollback_results.append(TLPManager.start())
            else:
                rollback_results.append(TLPManager.stop())

        return rollback_results

    @classmethod
    def apply_profile(cls, profile_name: str) -> Tuple[bool, List[Result]]:
        """Applies a declarative profile using state machine transitions.

        Args:
            profile_name: Name of target profile (low, hybrid, gaming, creator, macmode, etc.).

        Returns:
            Tuple of (overall_success boolean, list of Result objects).
        """
        sm = ProfileStateMachine(profile_name)
        sm.transition_to(ProfileState.APPLYING)
        start_time = time.time()
        snapshot = cls.get_hardware_snapshot()

        try:
            cfg = ProfileManager.load_profile(profile_name)
        except Exception as exc:
            sm.transition_to(ProfileState.FAILED)
            err_res = Result(
                success=False,
                message=f"Failed loading profile '{profile_name}': {exc}",
            )
            logger.error(err_res.message)
            EventBus.publish(ProfileFailedEvent(profile_name=profile_name, error_message=str(exc)))
            return False, [err_res]

        results: List[Result] = []
        has_failure = False
        reboot_required = False

        # 1. GPU Subsystem
        gpu_target = cfg.get("gpu", "hybrid")
        if gpu_target == "intel":
            gpu_res = GPUManager.use_intel()
        elif gpu_target == "nvidia":
            gpu_res = GPUManager.use_nvidia()
        else:
            gpu_res = GPUManager.use_hybrid()
        results.append(gpu_res)
        if not gpu_res.success:
            has_failure = True
        if gpu_res.reboot_required:
            reboot_required = True

        # 2. CPU Subsystem (Governor, EPP, Turbo Boost)
        cpu_target = cfg.get("cpu", "powersave")
        cpu_res = CPUManager.set_governor(cpu_target)
        results.append(cpu_res)
        if not cpu_res.success:
            has_failure = True

        if "epp" in cfg:
            epp_res = CPUManager.set_epp(cfg["epp"])
            results.append(epp_res)

        if "turbo_boost" in cfg:
            tb_res = CPUManager.set_turbo_boost(bool(cfg["turbo_boost"]))
            results.append(tb_res)

        # 3. System Power Profiles Daemon (powerprofilesctl / powerctl)
        if PowerProfilesManager.exists():
            pp_res = PowerProfilesManager.set_profile(profile_name)
            results.append(pp_res)

        # 4. Brightness & Refresh Rate
        bright_res = BrightnessManager.set(cfg.get("brightness", 50))
        results.append(bright_res)

        if "refresh_rate" in cfg:
            rr_res = DisplayManager.set_refresh_rate(int(cfg["refresh_rate"]))
            results.append(rr_res)

        # 5. Bluetooth Subsystem
        if cfg.get("bluetooth", True):
            bt_res = BluetoothManager.enable()
        else:
            bt_res = BluetoothManager.disable()
        results.append(bt_res)

        # 6. TLP Subsystem
        if cfg.get("tlp", True):
            tlp_res = TLPManager.start()
        else:
            tlp_res = TLPManager.stop()
        results.append(tlp_res)

        # 7. PowerTOP
        if cfg.get("powertop", False):
            pt_res = PowerTOPManager.autotune()
            results.append(pt_res)

        # 8. PCIe & Deep Kernel Power Savings
        PCIeManager.enable_powersave()
        if cfg.get("audio_powersave", False) or profile_name in ["low", "macmode", "travel"]:
            k_results = KernelPowerManager.apply_ultra_power_save()
            results.extend(k_results)

        # 9. Vendor Subsystem
        v_options = cfg.get("vendor_options", {})
        if v_options:
            v_results = VendorManager.apply_vendor_settings(v_options)
            results.extend(v_results)

        sm.transition_to(ProfileState.VERIFYING)
        duration = round(time.time() - start_time, 3)

        if has_failure:
            sm.transition_to(ProfileState.ROLLBACK)
            logger.warning(f"Profile '{profile_name}' application failed. Performing rollback.")
            cls.rollback_state(snapshot)
            results.append(
                Result(
                    success=False,
                    message="Automatic rollback performed due to operation failures.",
                    rollback_available=True,
                )
            )
            overall_success = False
            sm.transition_to(ProfileState.FAILED)
            EventBus.publish(
                ProfileFailedEvent(
                    profile_name=profile_name,
                    error_message="Subsystem operation failed during profile application",
                    duration_sec=duration,
                )
            )
        else:
            cls.save_state(profile_name)
            overall_success = True
            sm.transition_to(ProfileState.COMPLETED)
            EventBus.publish(
                ProfileAppliedEvent(
                    profile_name=profile_name,
                    duration_sec=duration,
                    battery_percent=snapshot["battery_percent"],
                    cpu_governor=cfg["cpu"],
                    gpu_mode=cfg["gpu"],
                    reboot_required=reboot_required,
                )
            )

        status_str = "SUCCESS" if overall_success else "FAILED"
        log_msg = f"Profile '{profile_name}' applied in {duration}s [{status_str}] (Battery: {snapshot['battery_percent']}%, CPU: {cfg['cpu']}, GPU: {cfg['gpu']})"
        LoggerService.write(log_msg)

        HistoryService.record(
            profile=profile_name,
            duration=duration,
            status=status_str,
            battery=snapshot["battery_percent"],
            cpu_governor=cfg["cpu"],
            gpu=cfg["gpu"],
        )

        return overall_success, results

    @classmethod
    def apply_auto(cls) -> Tuple[bool, List[Result]]:
        """Auto-selects profile based on battery & AC power state.

        Returns:
            Tuple of (success boolean, list of Result objects).
        """
        ac = BatteryManager.is_ac_connected()
        pct = BatteryManager.percent()

        if ac:
            target = "full" if pct > 80 else "hybrid"
        else:
            target = "low" if pct <= 30 else "hybrid"

        logger.info(f"Auto-selected profile '{target}' (AC: {ac}, Battery: {pct}%)")
        return cls.apply_profile(target)

    @classmethod
    def detect_active_profile(cls) -> str:
        """Inspects running system hardware and matches against declarative profiles.

        Returns:
            Matched profile name or 'Custom'.
        """
        curr_gpu = GPUManager.current()
        curr_cpu = CPUManager.current()

        for prof in ConfigManager.list_available_profiles():
            try:
                cfg = ConfigManager.load_profile(prof)
                if cfg.get("gpu") == curr_gpu and cfg.get("cpu") == curr_cpu:
                    return prof
            except Exception:
                continue

        return "Custom"
