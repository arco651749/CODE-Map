"""
向後相容轉發入口：UIA-Coder 行為感知與接線驗收圖譜引擎
所有核心實作已模組化遷移至 `uia_coder` 套件中。
"""
from uia_coder.core.graph import UIACodeGraph
from uia_coder.adapters.javascript_adapter import JavaScriptUIAGraphBuilder as JSUIAGraphBuilder
from uia_coder.adapters.python_adapter import PythonUIAGraphBuilder
from uia_coder.adapters import get_adapter_for_file, AdapterRegistry

__all__ = [
    "UIACodeGraph",
    "JSUIAGraphBuilder",
    "PythonUIAGraphBuilder",
    "get_adapter_for_file",
    "AdapterRegistry",
]

if __name__ == "__main__":
    from uia_coder.cli import main
    main()
