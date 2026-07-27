from .utils import exists


class Dependencies:

    REQUIRED = [

        "prime-select",

        "brightnessctl",

        "rfkill",

        "powertop",

        "tlp",

        "nvidia-smi"

    ]

    @classmethod

    def check(cls):

        result = {}

        for dependency in cls.REQUIRED:

            result[dependency] = exists(dependency)

        return result