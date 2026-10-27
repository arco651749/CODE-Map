"""
CLI entry point for running `python -m code_map`
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from code_map.cli import main

if __name__ == "__main__":
    main()
