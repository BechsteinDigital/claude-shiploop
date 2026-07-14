"""Einstiegspunkt für `python3 -m standup` (genutzt vom bin/standup-Wrapper)."""

import sys

from standup.cli import main

if __name__ == "__main__":
    sys.exit(main())
