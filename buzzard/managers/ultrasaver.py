"""MacMode & Ultra Power Saver Subsystem Manager.

Applies maximum power reduction parameters across CPU, GPU, Display, PCIe, and Kernel
to target Apple Silicon MacBook-equivalent battery discharge rates (~3.5W - 5.0W).
"""

from typing import List
from buzzard.core.result import Result
from buzzard.managers.bluetooth import BluetoothManager
from buzzard.managers.brightness import BrightnessManager
from buzzard.managers.cpu import CPUManager
from buzzard.managers.display import DisplayManager
from buzzard.managers.gpu import GPUManager
from buzzard.managers.kernel_power import KernelPowerManager
from buzzard.managers.pcie import PCIeManager
from buzzard.managers.powertop import PowerTOPManager
from buzzard.managers.tlp import TLPManager


class MacModeManager:
    """MacBook-Level Battery Optimization Manager."""

    @classmethod
    def activate_macmode(cls) -> List[Result]:
        """Activates all deep battery saving mechanisms targeting ~4W power draw.

        Returns:
            List of Result objects.
        """
        results: List[Result] = []

        # 1. Force Integrated Intel/AMD GPU
        results.append(GPUManager.use_intel())

        # 2. CPU Governor -> powersave
        results.append(CPUManager.powersave())

        # 3. CPU EPP -> power
        results.append(CPUManager.set_epp("power"))

        # 4. CPU Turbo Boost -> Disable
        results.append(CPUManager.set_turbo_boost(False))

        # 5. Display Refresh Rate -> 60Hz
        results.append(DisplayManager.set_refresh_rate(60))

        # 6. Brightness -> 25%
        results.append(BrightnessManager.set(25))

        # 7. Bluetooth -> Off
        results.append(BluetoothManager.disable())

        # 8. PCIe & USB Autosuspend
        results.append(PCIeManager.enable_powersave())

        # 9. Deep Kernel & Audio Power Savings
        k_results = KernelPowerManager.apply_ultra_power_save()
        results.extend(k_results)

        # 10. TLP & PowerTOP Autotune
        results.append(TLPManager.start())
        results.append(PowerTOPManager.autotune())

        return results
