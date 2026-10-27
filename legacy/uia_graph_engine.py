"""
向後相容轉發入口：CODE-Map 行為感知與接線驗收圖譜引擎
所有核心實作已模組化遷移至 `code_map` 套件中。
"""
from code_map.core.graph import CodeMapGraph
from code_map.adapters.javascript_adapter import JavaScriptCodeMapBuilder as JSUIAGraphBuilder
from code_map.adapters.python_adapter import PythonCodeMapBuilder
from code_map.adapters import get_adapter_for_file, AdapterRegistry

__all__ = [
    "CodeMapGraph",
    "JSUIAGraphBuilder",
    "PythonCodeMapBuilder",
    "get_adapter_for_file",
    "AdapterRegistry",
]

if __name__ == "__main__":
    from code_map.cli import main
    main()
