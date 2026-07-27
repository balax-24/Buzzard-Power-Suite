"""Buzzard Workload & Process Introspector.

Analyzes running process tables to classify active user workloads into application categories
(gaming, AI/LLM, creator, pentest, meeting, or battery saver) for automated profile shifting.
"""

import re
from typing import Dict, List, Optional
from buzzard.core.shell import Shell


class WorkloadIntrospector:
    """Introspects system process tables to detect active workload types."""

    WORKLOAD_SIGNATURES: Dict[str, List[str]] = {
        "gaming": ["steam", "lutris", "heroic", "cs2", "dota2", "cyberpunk", "wine", "proton", "mangohud"],
        "llm": ["ollama", "vllm", "llama.cpp", "text-generation-webui", "comfyui", "torch", "nvcc"],
        "creator": ["blender", "resolve", "gimp", "inkscape", "obs", "kdenlive", "audacity"],
        "pentest": ["wireshark", "burpsuite", "nmap", "msfconsole", "ghidra", "radare2"],
        "meeting": ["zoom", "teams", "slack", "discord", "webex"],
    }

    @classmethod
    def get_running_processes(cls) -> str:
        """Queries running process list via ps.

        Returns:
            Lowercase process command line string list.
        """
        res = Shell.run("ps -eo comm,args --no-headers")
        if res.success:
            return res.stdout.lower()
        return ""

    @classmethod
    def detect_workload(cls) -> str:
        """Detects current primary workload category.

        Returns:
            Workload profile name string (gaming, llm, creator, pentest, meeting, or 'default').
        """
        procs = cls.get_running_processes()
        if not procs:
            return "default"

        for category, signatures in cls.WORKLOAD_SIGNATURES.items():
            for sig in signatures:
                if re.search(r"\b" + re.escape(sig) + r"\b", procs):
                    return category

        return "default"
