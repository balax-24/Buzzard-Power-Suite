class Color:

    RESET = "\033[0m"

    RED = "\033[91m"

    GREEN = "\033[92m"

    YELLOW = "\033[93m"

    BLUE = "\033[94m"

    CYAN = "\033[96m"

    BOLD = "\033[1m"


class Console:

    @staticmethod
    def info(msg):

        print(f"{Color.BLUE}ℹ {msg}{Color.RESET}")

    @staticmethod
    def success(msg):

        print(f"{Color.GREEN}✔ {msg}{Color.RESET}")

    @staticmethod
    def warning(msg):

        print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")

    @staticmethod
    def error(msg):

        print(f"{Color.RED}✘ {msg}{Color.RESET}")

    @staticmethod
    def title(msg):

        print()

        print(Color.BOLD + msg + Color.RESET)