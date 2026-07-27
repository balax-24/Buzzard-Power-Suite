"""
Buzzard CLI Entry Point
"""

import sys

from buzzard.dispatcher import dispatch


def main() -> int:
    """
    Main CLI entry.
    """
    try:
        dispatch(sys.argv[1:])
        return 0

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 130

    except Exception as exc:
        print(f"Buzzard Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
