from buzzard import __version__
from buzzard.colors import Color

def banner(title):
    print()
    print(f"{Color.BOLD}🦅 Buzzard Power Suite{Color.RESET}")
    print(f"Version : {__version__}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(title)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
