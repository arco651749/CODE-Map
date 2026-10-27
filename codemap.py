"""
🌲 CODE-Map: Causal Operation & Dependency Evaluation Map
行為因果與接線依賴評估地圖引擎 (Official CLI Entrypoint)
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from code_map.cli import main

if __name__ == "__main__":
    main()
