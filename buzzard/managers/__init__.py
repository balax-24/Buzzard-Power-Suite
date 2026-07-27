"""Buzzard Hardware Subsystem Managers Package.

Exposes hardware managers for GPU, CPU, Battery, Brightness, Bluetooth, TLP, PowerTOP, Display, PowerEstimator, PCIe, PowerProfiles, KernelPower, MacMode, and Vendor.
"""

from buzzard.managers.battery import BatteryManager
from buzzard.managers.bluetooth import BluetoothManager
from buzzard.managers.brightness import BrightnessManager
from buzzard.managers.cpu import CPUManager
from buzzard.managers.display import DisplayManager
from buzzard.managers.gpu import GPUManager
from buzzard.managers.kernel_power import KernelPowerManager
from buzzard.managers.pcie import PCIeManager
from buzzard.managers.power_estimator import PowerEstimator
from buzzard.managers.powerprofiles import PowerProfilesManager
from buzzard.managers.powertop import PowerTOPManager
from buzzard.managers.profile import ProfileManager
from buzzard.managers.tlp import TLPManager
from buzzard.managers.ultrasaver import MacModeManager
from buzzard.managers.vendor import VendorManager

__all__ = [
    "BatteryManager",
    "BluetoothManager",
    "BrightnessManager",
    "CPUManager",
    "DisplayManager",
    "GPUManager",
    "KernelPowerManager",
    "MacModeManager",
    "PCIeManager",
    "PowerEstimator",
    "PowerProfilesManager",
    "PowerTOPManager",
    "ProfileManager",
    "TLPManager",
    "VendorManager",
]
