"""Buzzard Power Optimization Service.

Executes safe, reversible system optimizations (TLP refresh, CPU governor tuning,
and explicit PowerTOP autotune) only when requested via 'buzzard optimize'.
"""

from typing import List
from buzzard.core.result import Result
from buzzard.managers import CPUManager, PowerTOPManager, TLPManager


class OptimizeService:
    """Service for orchestrating explicit system power optimizations."""

    @classmethod
    def optimize(cls, enable_powertop: bool = True) -> List[Result]:
        """Runs optimization sequence across TLP, CPU, and optional PowerTOP.

        Args:
            enable_powertop: Whether to execute PowerTOP autotune (default True).

        Returns:
            List of Result objects.
        """
        results: List[Result] = []

        # 1. Ensure CPU is set to powersave governor for battery efficiency
        cpu_res = CPUManager.powersave()
        results.append(cpu_res)

        # 2. Refresh TLP optimizations
        if TLPManager.is_installed():
            tlp_res = TLPManager.start()
            results.append(tlp_res)
        else:
            results.append(
                Result(
                    success=False,
                    message="TLP is not installed. Install tlp for maximum battery efficiency.",
                )
            )

        # 3. Explicit PowerTOP autotune (ONLY when invoked by optimize service)
        if enable_powertop:
            if PowerTOPManager.is_installed():
                pt_res = PowerTOPManager.autotune()
                results.append(pt_res)
            else:
                results.append(
                    Result(
                        success=False,
                        message="PowerTOP is not installed. Install powertop for autotune optimizations.",
                    )
                )

        return results
