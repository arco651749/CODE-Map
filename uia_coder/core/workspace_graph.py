import os
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import networkx as nx
from uia_coder.adapters import get_adapter_for_file
from uia_coder.core.graph import UIACodeGraph


class WorkspaceGraphBuilder:
    """
    跨檔案語意圖譜建構器 (Workspace Graph Builder)
    解析多檔案間的 import / export 關聯，重連 (Rewire) 跨檔案呼叫邊，
    打通 Subagent A (API) 與 Subagent B (UI 元件) 的跨檔因果切片。
    """

    @classmethod
    def _resolve_module_path(cls, current_file: str, module_specifier: str, known_files: List[str]) -> Optional[str]:
        """
        將相對引用模組路徑 (如 '../api/user_api') 消解為工作區內的真實檔案路徑
        """
        curr_dir = os.path.dirname(current_file)
        raw_target = os.path.normpath(os.path.join(curr_dir, module_specifier)).replace("\\", "/")

        # 候選副檔名嘗試
        candidates = [
            raw_target,
            f"{raw_target}.ts",
            f"{raw_target}.tsx",
            f"{raw_target}.js",
            f"{raw_target}.jsx",
            f"{raw_target}.mjs",
            f"{raw_target}.py",
            os.path.join(raw_target, "index.ts").replace("\\", "/"),
            os.path.join(raw_target, "index.tsx").replace("\\", "/"),
            os.path.join(raw_target, "index.js").replace("\\", "/"),
        ]

        known_set = set(known_files)
        for cand in candidates:
            if cand in known_set:
                return cand

        # 若 known_files 內包含相對結尾
        for cand in candidates:
            for kf in known_files:
                if kf.endswith(cand) or cand.endswith(kf):
                    return kf

        return None

    @classmethod
    def build_from_files(
        cls,
        file_paths: List[str],
        root_dir: str = ".",
    ) -> UIACodeGraph:
        """
        聯合解析多個源碼檔案並拼接為一張統一的 Workspace UIACodeGraph
        """
        merged_graph = UIACodeGraph(name="Workspace Multi-File Unified Graph")
        file_graphs: Dict[str, UIACodeGraph] = {}
        normalized_paths: List[str] = []

        # Pass 1: 單檔解析與圖結構匯入
        for fp in file_paths:
            abs_fp = os.path.abspath(fp)
            if not os.path.exists(abs_fp):
                continue
            rel_fp = os.path.relpath(abs_fp, root_dir).replace("\\", "/")
            normalized_paths.append(rel_fp)

            adapter = get_adapter_for_file(abs_fp)
            with open(abs_fp, "r", encoding="utf-8") as f:
                code = f.read()

            single_g = adapter.parse_and_build(code, file_path=rel_fp)
            file_graphs[rel_fp] = single_g

            # 合併節點與邊至總圖
            for n, d in single_g.g.nodes(data=True):
                merged_graph.g.add_node(n, **d)
            for u, v, d in single_g.g.edges(data=True):
                merged_graph.g.add_edge(u, v, **d)

        # Pass 2: 跨檔案符號消解 (Cross-File Symbol Linking & Rewiring)
        for rel_fp, single_g in file_graphs.items():
            imports = single_g.g.graph.get("imports", [])

            for imp in imports:
                local_name = imp.get("local_name")
                imported_name = imp.get("imported_name")
                mod_spec = imp.get("module_specifier")

                target_file = cls._resolve_module_path(rel_fp, mod_spec, normalized_paths)
                if not target_file or target_file not in file_graphs:
                    continue

                target_g = file_graphs[target_file]
                target_exports = target_g.g.graph.get("exports", {})

                # 尋找目標檔案中是否匯出該函式
                is_exported = imported_name in target_exports

                # 在目標圖中尋找實體 FUNCTION_DEF 節點
                real_func_node_id = None
                for tn, td in target_g.g.nodes(data=True):
                    if td.get("category") == "FUNCTION_DEF" and td.get("label") == imported_name:
                        real_func_node_id = tn
                        break

                if not real_func_node_id and is_exported:
                    real_func_node_id = target_exports[imported_name]

                # 尋找呼叫端原本連向 external 佔位點的邊
                unresolved_nid = f"func:{local_name}@external"
                edges_to_rewire = []
                if unresolved_nid in merged_graph.g:
                    for u, v, ed in merged_graph.g.in_edges(unresolved_nid, data=True):
                        edges_to_rewire.append((u, dict(ed)))

                # 執行重連 (Rewire)
                if real_func_node_id:
                    for u, ed in edges_to_rewire:
                        merged_graph.g.remove_edge(u, unresolved_nid)

                        if is_exported:
                            merged_graph.add_edge_rich(
                                source=u,
                                target=real_func_node_id,
                                edge_type="RESOLVES_TO",
                                flow_type=ed.get("flow_type", "SYNC"),
                                status="VALID",
                                sequence_order=ed.get("sequence_order", 1),
                                is_conditional=ed.get("is_conditional", False),
                                guard_type=ed.get("guard_type", "NONE"),
                                guard_expr=ed.get("guard_expr", ""),
                                is_error_handled=ed.get("is_error_handled", False),
                                detail=f"跨模組符號消解: 成功接線至 {target_file}:{imported_name}()",
                            )
                        else:
                            # 致命死穴：目標函式忘了加 export 關鍵字！
                            merged_graph.add_edge_rich(
                                source=u,
                                target=real_func_node_id,
                                edge_type="RESOLVES_TO",
                                flow_type=ed.get("flow_type", "SYNC"),
                                status="BLOCKED_SCOPE",
                                sequence_order=ed.get("sequence_order", 1),
                                is_conditional=ed.get("is_conditional", False),
                                guard_type=ed.get("guard_type", "NONE"),
                                guard_expr=ed.get("guard_expr", ""),
                                is_error_handled=ed.get("is_error_handled", False),
                                detail=f"💥 跨模組作用域阻隔: 目標函式 '{imported_name}' 未匯出 (Not Exported in {target_file})！",
                            )

                    # 若 external 佔位節點已無任何入邊，予以清理
                    if unresolved_nid in merged_graph.g and merged_graph.g.in_degree(unresolved_nid) == 0:
                        merged_graph.g.remove_node(unresolved_nid)

        return merged_graph

    @classmethod
    def build_from_dir(cls, dir_path: str, extensions: Optional[Set[str]] = None) -> UIACodeGraph:
        """遍歷目錄下所有支援的原始碼檔案並聯合建圖"""
        from uia_coder.adapters import AdapterRegistry
        valid_exts = extensions or set(AdapterRegistry.get_registry().keys())

        collected_files = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in valid_exts:
                    collected_files.append(os.path.join(root, file))

        return cls.build_from_files(collected_files, root_dir=dir_path)
