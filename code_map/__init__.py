"""
CODE-Map: 行為感知與接線驗收的程式碼語意分析引擎
"""
from code_map.adapters import AdapterRegistry, get_adapter_for_file
from code_map.core.differ import CodeMapDiffer, CodeMapDiffResult
from code_map.core.graph import CodeMapGraph
from code_map.core.spec_verifier import SpecVerifier, verify_objection
from code_map.core.workspace_graph import WorkspaceGraphBuilder

__version__ = "2.0.0"
__all__ = [
    "CodeMapGraph",
    "AdapterRegistry",
    "get_adapter_for_file",
    "WorkspaceGraphBuilder",
    "CodeMapDiffer",
    "CodeMapDiffResult",
    "SpecVerifier",
    "verify_objection",
]
