import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple, Union

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import networkx as nx
from code_map.core.graph import CodeMapGraph


class SpecContract:
    """
    CODE-Map 形式化規格契約物件
    定義上位架構師 Agent 對 Subagents 交付成果的不可違抗約束。
    """

    def __init__(
        self,
        required_anchors: Optional[List[str]] = None,
        required_causal_chains: Optional[List[Dict[str, Any]]] = None,
        invariants: Optional[Dict[str, Any]] = None,
        spec_graph: Optional[CodeMapGraph] = None,
    ):
        self.required_anchors = required_anchors or []
        self.required_causal_chains = required_causal_chains or []
        self.invariants = invariants or {
            "no_scope_trap": True,
            "no_blocking_api": True,
        }
        self.spec_graph = spec_graph

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpecContract":
        return cls(
            required_anchors=data.get("required_anchors", []),
            required_causal_chains=data.get("required_causal_chains", []),
            invariants=data.get("invariants", {"no_scope_trap": True, "no_blocking_api": True}),
        )

    @classmethod
    def from_file(cls, file_path: str) -> "SpecContract":
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 支援 YAML 或 JSON
        if file_path.endswith((".yaml", ".yml")):
            try:
                import yaml
                data = yaml.safe_load(content)
            except ImportError:
                # 簡單 yaml 兼容解析器
                data = json.loads(content)
        else:
            data = json.loads(content)

        return cls.from_dict(data)

    @classmethod
    def from_spec_graph(cls, spec_graph: CodeMapGraph) -> "SpecContract":
        """從一張精簡的 CodeMapGraph (上位 Spec 圖譜) 自動抽取契約"""
        anchors = spec_graph.get_ui_anchors()
        chains = []

        for anchor in anchors:
            descendants = nx.descendants(spec_graph.g, anchor)
            # 依拓樸順序提取呼叫鏈
            sub_nodes = [anchor] + list(descendants)
            sub_g = spec_graph.g.subgraph(sub_nodes)
            
            # 收集關鍵路徑上的函式節點
            chain_funcs = []
            constraints = {}
            for n in nx.topological_sort(sub_g):
                nd = spec_graph.g.nodes[n]
                label = nd.get("label", n)
                if nd.get("category") == "FUNCTION_DEF":
                    chain_funcs.append(label)
                    # 檢查入邊屬性
                    in_edges = list(spec_graph.g.in_edges(n, data=True))
                    if in_edges:
                        _, _, ed = in_edges[0]
                        c = {}
                        if ed.get("flow_type") == "AWAIT":
                            c["require_await"] = True
                        if ed.get("is_conditional"):
                            c["require_conditional_guard"] = True
                        if c:
                            constraints[label] = c

            if chain_funcs:
                chains.append({
                    "anchor": spec_graph.g.nodes[anchor].get("label", anchor),
                    "chain": chain_funcs,
                    "constraints": constraints,
                })

        return cls(
            required_anchors=[spec_graph.g.nodes[a].get("label", a) for a in anchors],
            required_causal_chains=chains,
            invariants={"no_scope_trap": True, "no_blocking_api": True},
            spec_graph=spec_graph,
        )


class SpecVerificationResult:
    """規格驗收裁決報告"""

    def __init__(
        self,
        passed: bool,
        verdict: str,
        violations: List[Dict[str, Any]],
        passed_rules: List[str],
        actual_graph: CodeMapGraph,
        spec: SpecContract,
    ):
        self.passed = passed
        self.verdict = verdict
        self.violations = violations
        self.passed_rules = passed_rules
        self.actual_graph = actual_graph
        self.spec = spec

    def to_markdown(self) -> str:
        lines = []
        lines.append(f"## ⚖️ CODE-Map 形式化規格驗收報告 ({self.verdict})")
        lines.append("---")

        if self.passed:
            lines.append("🎉 **所有規格契約條件皆已嚴格達成！**\n")
            lines.append("### ✅ 已通過之契約規則:")
            for r in self.passed_rules:
                lines.append(f"  • {r}")
        else:
            lines.append("🔴 **驗收未通過：實作代碼違反了上位架構契約！**\n")
            lines.append("### 💥 違規清單 (Proof-Carrying Violations):")
            for v in self.violations:
                lines.append(f"  - ❌ **[{v.get('type')}]**: {v.get('detail')}")
                if "target" in v:
                    lines.append(f"    • 目標節點/邊: `{v.get('target')}`")
                if "suggested_fix" in v:
                    lines.append(f"    • 建議修復方式: {v.get('suggested_fix')}")

        lines.append("\n### 🌲 實際展開控制樹 (Actual UIA Control Tree):")
        lines.append("```")
        lines.append(self.actual_graph.to_uia_markdown())
        lines.append("```")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "verdict": self.verdict,
            "violations": self.violations,
            "passed_rules": self.passed_rules,
        }


class SpecVerifier:
    """
    基於有向路徑可達性與拓樸偏序的規格驗收裁判引擎
    容許 Subagent 自由抽取私有 Helper 輔助函式，但嚴格守護因果順序與時序約束。
    """

    @classmethod
    def _find_actual_node(cls, actual_graph: CodeMapGraph, name: str) -> Optional[str]:
        """在 Actual Graph 中尋找語意吻合的節點"""
        clean_name = name.lstrip("#")

        # 1. 若以 # 開頭（UI 控制項錨點），優先在 UI_CONTROL 中尋找
        if name.startswith("#"):
            for n, d in actual_graph.g.nodes(data=True):
                if d.get("category") == "UI_CONTROL":
                    lbl = d.get("label", "")
                    if lbl == name or lbl.lstrip("#") == clean_name:
                        return n

        # 2. 優先尋找 FUNCTION_DEF、UI_CONTROL 或 EVENT_BINDING
        for n, d in actual_graph.g.nodes(data=True):
            cat = d.get("category")
            if cat in ("FUNCTION_DEF", "UI_CONTROL", "EVENT_BINDING"):
                lbl = d.get("label", "")
                clean_lbl = lbl.lstrip("#")
                if lbl == name or clean_lbl == clean_name:
                    return n
                if "::" in lbl and lbl.split("::")[-1] == clean_name:
                    return n

        # 3. 兜底通用搜尋
        for n, d in actual_graph.g.nodes(data=True):
            lbl = d.get("label", "")
            clean_lbl = lbl.lstrip("#")
            if lbl == name or clean_lbl == clean_name:
                return n
            if "::" in lbl and lbl.split("::")[-1] == clean_name:
                return n
            if clean_name in n:
                return n
        return None

    @classmethod
    def _find_common_ancestor_order(
        cls, actual_graph: CodeMapGraph, u: str, v: str
    ) -> Tuple[bool, Optional[str]]:
        """
        尋找 u 與 v 在 Actual Graph 中的最近共同祖先 (LCA)，
        並檢驗 u 的呼叫時序是否嚴格小於或等於 v 的呼叫時序。
        """
        ancestors_u = nx.ancestors(actual_graph.g, u)
        ancestors_v = nx.ancestors(actual_graph.g, v)
        common = ancestors_u & ancestors_v
        if not common:
            return False, "無共同祖先函式/處理常式"

        # 取離 u, v 最近的共同祖先
        for anc in common:
            # 找尋從 anc 到達 u 與 v 的路徑
            paths_to_u = list(nx.all_simple_paths(actual_graph.g, anc, u))
            paths_to_v = list(nx.all_simple_paths(actual_graph.g, anc, v))
            if not paths_to_u or not paths_to_v:
                continue

            # 取從 anc 出發的第一條邊序號
            p_u = paths_to_u[0]
            p_v = paths_to_v[0]
            edge_u_data = actual_graph.g.get_edge_data(p_u[0], p_u[1]) or {}
            edge_v_data = actual_graph.g.get_edge_data(p_v[0], p_v[1]) or {}
            order_u = edge_u_data.get("sequence_order", 1)
            order_v = edge_v_data.get("sequence_order", 1)

            if order_u <= order_v:
                return True, None
            else:
                return False, f"共同祖先 `{anc}` 內部執行偏序倒置 (order({u})={order_u} > order({v})={order_v})"

        return True, None

    @classmethod
    def verify(
        cls,
        spec: Union[SpecContract, Dict[str, Any], CodeMapGraph, str],
        actual: Union[CodeMapGraph, str],
        workspace_root: str = ".",
    ) -> SpecVerificationResult:
        """
        執行形式化驗收
        """
        # 1. 規格標準化
        if isinstance(spec, str):
            if spec.endswith((".json", ".yaml", ".yml")):
                contract = SpecContract.from_file(spec)
            else:
                from code_map.adapters import get_adapter_for_file
                ad = get_adapter_for_file(spec)
                with open(spec, "r", encoding="utf-8") as f:
                    contract = SpecContract.from_spec_graph(ad.parse_and_build(f.read(), spec))
        elif isinstance(spec, CodeMapGraph):
            contract = SpecContract.from_spec_graph(spec)
        elif isinstance(spec, dict):
            contract = SpecContract.from_dict(spec)
        else:
            contract = spec

        # 2. 實作圖譜標準化
        if isinstance(actual, str):
            from code_map.adapters import get_adapter_for_file
            ad = get_adapter_for_file(actual)
            with open(actual, "r", encoding="utf-8") as f:
                actual_graph = ad.parse_and_build(f.read(), actual)
        else:
            actual_graph = actual

        violations = []
        passed_rules = []

        # Step 1: 全域安全不變量驗收 (Invariant Check)
        inv = actual_graph.check_invariants()
        if not inv["passed"]:
            for err in inv.get("scope_errors", []):
                violations.append({
                    "type": "SCOPE_VIOLATION",
                    "target": f"{err.get('caller')} -> {err.get('target')}",
                    "detail": err.get("detail", "存在閉包作用域阻隔"),
                    "suggested_fix": "將目標函式提升至模組可達作用域 (Hoisting) 或透過 export 匯出",
                })
            for haz in inv.get("hazards", []):
                violations.append({
                    "type": "INVARIANT_VIOLATION",
                    "target": haz.get("node", haz.get("source", "?")),
                    "detail": haz.get("detail", "觸發阻塞或危險操作"),
                    "suggested_fix": "移除同步阻塞呼叫 (window.confirm, time.sleep 等) 或改為非同步實作",
                })
        else:
            passed_rules.append("形式化安全不變量守衛全數通過 (無閉包阻隔、無同步阻塞)")

        # Step 2: 錨點存在性檢查 (Required Anchors)
        for anchor in contract.required_anchors:
            actual_anchor = cls._find_actual_node(actual_graph, anchor)
            if not actual_anchor:
                violations.append({
                    "type": "MISSING_ANCHOR",
                    "target": anchor,
                    "detail": f"實作代碼中找不到規格要求的控制項錨點: `{anchor}`",
                    "suggested_fix": f"在 UI 模板或代碼中建立或綁定 `{anchor}` 控制項",
                })
            else:
                passed_rules.append(f"控制項錨點 `{anchor}` 存在且已正確認證")

        # Step 3: 有向路徑可達性與拓樸偏序驗收 (Causal Chains & Constraints)
        for chain_spec in contract.required_causal_chains:
            anchor_name = chain_spec.get("anchor") or (contract.required_anchors[0] if contract.required_anchors else None)
            chain = chain_spec.get("chain", [])
            constraints = chain_spec.get("constraints", {})

            if not chain:
                continue

            # 檢查起點 (Anchor)
            curr_actual_u = cls._find_actual_node(actual_graph, anchor_name) if anchor_name else None
            
            # 遍歷鏈中的相鄰兩階段 (u -> v)
            for idx in range(len(chain)):
                step_name = chain[idx]
                step_actual_node = cls._find_actual_node(actual_graph, step_name)

                if not step_actual_node:
                    violations.append({
                        "type": "MISSING_CHAIN_NODE",
                        "target": step_name,
                        "detail": f"因果調用鏈中缺少關鍵業務函式: `{step_name}`",
                        "suggested_fix": f"實作並接線 `{step_name}` 函式",
                    })
                    continue

                # 驗證從上一個節點到達此節點的路徑可達性或共同祖先偏序
                if idx == 0 and curr_actual_u:
                    # 從控制項錨點到第一階段處理常式
                    if not nx.has_path(actual_graph.g, curr_actual_u, step_actual_node):
                        violations.append({
                            "type": "BROKEN_CAUSAL_PATH",
                            "target": f"{anchor_name} ➔ {step_name}",
                            "detail": f"控制項 `{anchor_name}` 無法透過有向事件鏈到達 `{step_name}` (中間電線斷裂)",
                            "suggested_fix": f"確認事件監聽常式是否正確呼叫了 `{step_name}`",
                        })
                    else:
                        passed_rules.append(f"因果路徑通電: `{anchor_name}` ➔ ... ➔ `{step_name}`")
                elif idx > 0:
                    prev_name = chain[idx - 1]
                    prev_node = cls._find_actual_node(actual_graph, prev_name)
                    if prev_node:
                        # 檢查 1: 直接或間接路徑 (prev -> step)
                        has_direct_or_indirect_path = nx.has_path(actual_graph.g, prev_node, step_actual_node)
                        if not has_direct_or_indirect_path:
                            # 檢查 2: 共同父處理常式下的兄弟調用偏序 (LCA)
                            ok_order, reason = cls._find_common_ancestor_order(actual_graph, prev_node, step_actual_node)
                            if not ok_order:
                                violations.append({
                                    "type": "BROKEN_PARTIAL_ORDER",
                                    "target": f"{prev_name} ➔ {step_name}",
                                    "detail": f"階段順序違規: 規格要求先執行 `{prev_name}` 再執行 `{step_name}`，但實際接線未維持偏序 ({reason})",
                                    "suggested_fix": f"調整調用順序，確保 `{prev_name}` 優先於 `{step_name}` 執行",
                                })
                            else:
                                passed_rules.append(f"拓樸偏序吻合: `{prev_name}` 先於 `{step_name}` 執行")
                        else:
                            passed_rules.append(f"因果路徑可達: `{prev_name}` ➔ ... ➔ `{step_name}`")

                # Step 4 & 5: 檢查約束 (require_await / require_conditional_guard)
                c_rules = constraints.get(step_name, {})
                if c_rules.get("require_await"):
                    # 檢查到達 step_actual_node 的呼叫是否為 await
                    in_edges = actual_graph.g.in_edges(step_actual_node, data=True)
                    has_await = any(ed.get("flow_type") == "AWAIT" for _, _, ed in in_edges)
                    if not has_await:
                        violations.append({
                            "type": "MISSING_AWAIT",
                            "target": step_name,
                            "detail": f"規格要求呼叫 `{step_name}` 必須使用 `await` 非同步等待，但實際為同步或遺漏 await",
                            "suggested_fix": f"在呼叫 `{step_name}` 前加上 `await`",
                        })
                    else:
                        passed_rules.append(f"非同步約束達成: `await {step_name}()`")

                if c_rules.get("require_conditional_guard"):
                    # 檢查直接入邊或從起點/祖先到達 step_actual_node 的路徑上是否有條件分支或 Early-Return 守衛
                    has_guard = False
                    in_edges = actual_graph.g.in_edges(step_actual_node, data=True)
                    if any(ed.get("is_conditional") for _, _, ed in in_edges):
                        has_guard = True
                    
                    if not has_guard and curr_actual_u and nx.has_path(actual_graph.g, curr_actual_u, step_actual_node):
                        for path in nx.all_simple_paths(actual_graph.g, curr_actual_u, step_actual_node):
                            for i in range(len(path) - 1):
                                ed = actual_graph.g.get_edge_data(path[i], path[i+1]) or {}
                                if ed.get("is_conditional"):
                                    has_guard = True
                                    break
                            if has_guard:
                                break

                    if not has_guard:
                        violations.append({
                            "type": "MISSING_CONDITIONAL_GUARD",
                            "target": step_name,
                            "detail": f"規格要求呼叫 `{step_name}` 必須受到條件分支或 Early-Return 守衛保護 (如 if (!confirmed) return;)",
                            "suggested_fix": f"在呼叫 `{step_name}` 前加入條件守衛判斷",
                        })
                    else:
                        passed_rules.append(f"條件守衛約束達成: `{step_name}` 受到條件分支/Early-Return 保護")

        passed = len(violations) == 0
        verdict = "🟢 SPEC_PASSED" if passed else "🔴 SPEC_VIOLATION"

        return SpecVerificationResult(
            passed=passed,
            verdict=verdict,
            violations=violations,
            passed_rules=passed_rules,
            actual_graph=actual_graph,
            spec=contract,
        )


def verify_objection(objection_dict: Dict[str, Any], workspace_root: str = ".") -> Dict[str, Any]:
    """
    Subagent 規格異議 (Spec Objection) AST 自動防偽查核器
    解析證據檔案，透過 Tree-sitter AST 實地檢視該檔案實際存在的函式清單，
    防止模型因偷懶編造假理由欺騙上位 Architect Agent。
    """
    evidence_str = objection_dict.get("evidence", "")
    target = objection_dict.get("target", "")

    # 解析證據字串中可能包含的檔案路徑 (例如 "api/items.ts:L42 只提供 deleteMany(ids)")
    match = re.search(r"([\w\-./\\]+\.[a-zA-Z0-9]+)", evidence_str)
    if not match:
        return {
            "status": "UNPARSEABLE_EVIDENCE",
            "is_valid": False,
            "report": f"⚠️ 無法從證據字串中解析出有效檔案路徑: '{evidence_str}'",
        }

    rel_file = match.group(1).replace("\\", "/")
    full_path = os.path.join(workspace_root, rel_file)

    if not os.path.exists(full_path):
        return {
            "status": "EVIDENCE_FILE_NOT_FOUND",
            "is_valid": False,
            "report": f"❌ 異議證據檔案不存在: '{rel_file}'，判定 Subagent 證據無效或路徑虛構！",
        }

    from code_map.adapters import get_adapter_for_file
    adapter = get_adapter_for_file(full_path)
    with open(full_path, "r", encoding="utf-8") as f:
        src = f.read()

    graph = adapter.parse_and_build(src, file_path=rel_file)
    actual_funcs = [
        d.get("label", n)
        for n, d in graph.g.nodes(data=True)
        if d.get("category") == "FUNCTION_DEF"
    ]

    # 查核質疑的函式名稱是否存在
    # 從 target 或 reason 中提取函式名
    queried_func = None
    target_match = re.search(r"->\s*([a-zA-Z0-9_]+)", target)
    if target_match:
        queried_func = target_match.group(1)

    genuine = True
    if queried_func and queried_func in actual_funcs:
        genuine = False
        report = f"🚨 異議駁回 (證據不實): Subagent 宣稱 `{rel_file}` 不存在或無法調用 `{queried_func}`，但 AST 實地查核確認該檔案第 L{graph.g.nodes.get(f'func:{queried_func}@{rel_file}', {}).get('scope', {}).get('line', '?')} 行確實存在 `{queried_func}`！"
    else:
        report = f"✅ 異議證據屬實: `{rel_file}` 確實未提供 `{queried_func or '指定目標'}` 函式。該檔案現存函式清單: {actual_funcs}。"

    return {
        "status": "VERIFIED_GENUINE" if genuine else "EVIDENCE_FALSIFIED",
        "is_valid": genuine,
        "evidence_file": rel_file,
        "discovered_functions": actual_funcs,
        "report": report,
    }
