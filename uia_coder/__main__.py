"""
CLI entry point for running `python -m uia_coder`
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.cli import main

if __name__ == "__main__":
    main()
