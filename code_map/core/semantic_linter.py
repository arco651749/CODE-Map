"""
CODE-Map Hybrid Semantic Linter:
AST/Graph Domain Routing -> Decision API Gatekeeper -> Generative LLM Explainer.
Strictly Fail-Open: external AI/network errors emit warnings and never break CODE-Map.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import json
import os
import re
from typing import Any, Dict, List, Optional, Set

from code_map.core.graph import CodeMapGraph
from code_map.core.lint_providers import (
    BaseDecisionProvider,
    BaseExplainerProvider,
    DecisionVerdict,
    ExplainerFinding,
    LintProviderError,
    create_decision_provider,
    create_explainer_provider,
)

DEFAULT_RULES_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "rules", "codemap_lint_rules.json")
)

EXT_LANGUAGE_MAP = {
    ".py": "python",
    ".cs": "csharp",
    ".axaml": "xaml",
    ".xaml": "xaml",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".html": "html",
    ".vue": "vue",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
}


@dataclass
class NodeLintResult:
    """Lint outcome for a single graph node."""
    node_id: str
    label: str
    file_path: str
    line_start: int
    line_end: int
    domains: List[str]
    verdicts: List[DecisionVerdict] = field(default_factory=list)
    findings: Dict[str, ExplainerFinding] = field(default_factory=dict)
    gatekeeper_ms: float = 0.0
    explainer_ms: float = 0.0
    node_warnings: List[str] = field(default_factory=list)


@dataclass
class SemanticLintReport:
    """Aggregated semantic lint report across inspected nodes."""
    gatekeeper_name: str
    explainer_name: str
    nodes_inspected: int
    nodes_skipped_by_prefilter: int
    node_results: List[NodeLintResult] = field(default_factory=list)
    service_warnings: List[str] = field(default_factory=list)

    @property
    def total_blocks(self) -> int:
        return sum(1 for nr in self.node_results for v in nr.verdicts if v.status == "BLOCK")

    @property
    def total_warns(self) -> int:
        return sum(1 for nr in self.node_results for v in nr.verdicts if v.status == "WARN")

    @property
    def has_blocks(self) -> bool:
        return self.total_blocks > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gatekeeper": self.gatekeeper_name,
            "explainer": self.explainer_name,
            "nodes_inspected": self.nodes_inspected,
            "nodes_skipped_by_prefilter": self.nodes_skipped_by_prefilter,
            "total_blocks": self.total_blocks,
            "total_warns": self.total_warns,
            "service_warnings": self.service_warnings,
            "results": [
                {
                    "node_id": nr.node_id,
                    "label": nr.label,
                    "file": nr.file_path,
                    "line_start": nr.line_start,
                    "line_end": nr.line_end,
                    "domains": nr.domains,
                    "gatekeeper_ms": round(nr.gatekeeper_ms, 1),
                    "explainer_ms": round(nr.explainer_ms, 1),
                    "node_warnings": nr.node_warnings,
                    "verdicts": [
                        {
                            "rule_id": v.rule_id,
                            "title": v.title,
                            "domain": v.domain,
                            "severity": v.severity,
                            "question_type": v.question_type,
                            "score": round(v.score, 4),
                            "confidence": round(v.confidence, 4),
                            "selected_choice": v.selected_choice,
                            "status": v.status,
                            "raw": v.raw,
                            "explanation": (
                                {
                                    "evidence_lines": nr.findings[v.rule_id].evidence_lines,
                                    "reasoning": nr.findings[v.rule_id].reasoning,
                                    "suggested_fix": nr.findings[v.rule_id].suggested_fix,
                                }
                                if v.rule_id in nr.findings
                                else None
                            ),
                        }
                        for v in nr.verdicts
                    ],
                }
                for nr in self.node_results
            ],
        }

    def to_markdown(self, show_all_decisions: bool = False) -> str:
        lines: List[str] = [
            "🤖 === CODE-Map AI Semantic Lint Report ===",
            f"• Gatekeeper: `{self.gatekeeper_name}` | Explainer: `{self.explainer_name}`",
            (
                f"• 掃描節點: {self.nodes_inspected} (AST 前置過濾略過: {self.nodes_skipped_by_prefilter}) | "
                f"🔴 BLOCK: {self.total_blocks} | ⚠️ WARN: {self.total_warns}"
            ),
        ]

        if self.service_warnings:
            lines.append("")
            lines.append("⚠️ [AI-LINT-SERVICE-WARN] 外部服務降級訊息 (不阻斷 CODE-Map 主流程):")
            for w in self.service_warnings:
                lines.append(f"  - {w}")

        any_rendered = False
        for nr in self.node_results:
            visible = [
                v for v in nr.verdicts if show_all_decisions or v.status in ("WARN", "BLOCK")
            ]
            if not visible and not nr.node_warnings:
                continue
            any_rendered = True
            lines.append("")
            loc = f"{nr.file_path}:L{nr.line_start}-L{nr.line_end}" if nr.file_path else f"L{nr.line_start}-L{nr.line_end}"
            lines.append(
                f"📌 節點 `{nr.label}` ({loc}) | Domains: `{', '.join(nr.domains)}` "
                f"[Decision: {nr.gatekeeper_ms:.0f}ms"
                + (f", Explainer: {nr.explainer_ms:.0f}ms" if nr.explainer_ms > 0 else "")
                + "]"
            )
            for nw in nr.node_warnings:
                lines.append(f"  ⚠️ [AI-LINT-SERVICE-WARN] {nw}")
            for v in visible:
                badge = "🔴 BLOCK" if v.status == "BLOCK" else ("⚠️ WARN" if v.status == "WARN" else "🟢 PASS")
                choice_info = f", choice={v.selected_choice}" if v.selected_choice else ""
                lines.append(f"  [{v.rule_id}] ({v.domain}) {v.title} -> {badge}")
                lines.append(
                    f"    ├─ Decision API: type={v.question_type}, score={v.score:.4f}, "
                    f"confidence={v.confidence:.4f}{choice_info}"
                )
                if v.rule_id in nr.findings:
                    fnd = nr.findings[v.rule_id]
                    lines.append("    └─ Explainer LLM:")
                    lines.append(f"       • 問題行號: {fnd.evidence_lines}")
                    lines.append(f"       • 判定原因: {fnd.reasoning}")
                    if fnd.suggested_fix:
                        lines.append(f"       • 修正建議: {fnd.suggested_fix}")

        if not any_rendered:
            lines.append("\n🟢 所有已檢驗節點皆通過語意規則門檻（無 WARN / BLOCK）。")

        return "\n".join(lines)


class SemanticLinter:
    """Orchestrates domain routing, AST pre-filtering, Decision API gating, and LLM explaining."""

    def __init__(self, config: Dict[str, Any], api_key_override: Optional[str] = None):
        self.config = config
        self.api_key_override = api_key_override
        self.rules: List[Dict[str, Any]] = config.get("Rules", [])
        self.domain_detectors: Dict[str, List[str]] = config.get("DomainDetectors", {})
        self.trigger_on: str = config.get("Explainer", {}).get("TriggerOn", "WarnOrBlock")

        self.gatekeeper: Optional[BaseDecisionProvider] = None
        self.explainer: Optional[BaseExplainerProvider] = None
        self.init_warnings: List[str] = []

        try:
            self.gatekeeper = create_decision_provider(
                config.get("Gatekeeper", {}), api_key_override=api_key_override
            )
        except Exception as exc:
            self.init_warnings.append(f"Gatekeeper 初始化失敗 ({exc})，已安全略過。")

        try:
            self.explainer = create_explainer_provider(
                config.get("Explainer", {}), api_key_override=api_key_override
            )
        except Exception as exc:
            self.init_warnings.append(f"Explainer 初始化失敗 ({exc})，僅保留 Gatekeeper 結果。")

    @classmethod
    def from_file(
        cls,
        rules_path: Optional[str] = None,
        gatekeeper_override: Optional[str] = None,
        explainer_override: Optional[str] = None,
        explainer_model_override: Optional[str] = None,
        api_key_override: Optional[str] = None,
    ) -> "SemanticLinter":
        path = rules_path or DEFAULT_RULES_PATH
        if not os.path.exists(path):
            raise FileNotFoundError(f"找不到 Lint 規則設定檔: {path}")
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        if gatekeeper_override:
            gk_cfg = cfg.setdefault("Gatekeeper", {})
            if gatekeeper_override != gk_cfg.get("Provider"):
                gk_cfg.pop("Endpoint", None)
                gk_cfg.pop("Model", None)
            gk_cfg["Provider"] = gatekeeper_override
            gk_cfg["Enabled"] = gatekeeper_override != "Disabled"
        if explainer_override:
            exp_cfg = cfg.setdefault("Explainer", {})
            if explainer_override != exp_cfg.get("Provider"):
                exp_cfg.pop("EndpointOrCommand", None)
                if not explainer_model_override:
                    exp_cfg.pop("Model", None)
            exp_cfg["Provider"] = explainer_override
            exp_cfg["Enabled"] = explainer_override != "Disabled"
        if explainer_model_override:
            cfg.setdefault("Explainer", {})["Model"] = explainer_model_override

        return cls(cfg, api_key_override=api_key_override)

    @staticmethod
    def _infer_language(file_path: str) -> str:
        _, ext = os.path.splitext(file_path.lower())
        return EXT_LANGUAGE_MAP.get(ext, ext.lstrip(".") or "unknown")

    def detect_node_domains(self, graph: CodeMapGraph, node_id: str) -> List[str]:
        """Infer applicable semantic domains for a graph node using topology and source tokens."""
        domains: Set[str] = {"GLOBAL"}
        ndata = graph.g.nodes.get(node_id, {})
        src = ndata.get("props", {}).get("source_code", "")

        # Topology check for UI domain (exclude CLI Entry anchors from GUI UI-thread rules)
        ui_cats = {"UI_CONTROL", "DOM_ELEMENT", "EVENT_BINDING"}
        def _is_gui_node(nid: str) -> bool:
            nid_low = nid.lower()
            if nid_low.startswith(("ctrl:#cli:", "event:cli.")):
                return False
            nd = graph.g.nodes.get(nid, {})
            if nd.get("category") not in ui_cats:
                return False
            ui_type = str(nd.get("props", {}).get("ui_type", "")).lower()
            label = str(nd.get("label", "")).lower()
            return "cli" not in ui_type.split() and not label.startswith("#cli:")

        if _is_gui_node(node_id):
            domains.add("UI")
        else:
            neighbors = list(graph.g.predecessors(node_id)) + list(graph.g.successors(node_id))
            for nb in neighbors:
                if _is_gui_node(nb):
                    domains.add("UI")
                    break

        # Combine source code + downstream callee labels for accurate domain routing
        callee_labels = " ".join(
            str(graph.g.nodes.get(succ, {}).get("label", ""))
            for succ in graph.g.successors(node_id)
        )
        haystack = f"{src}\n{callee_labels}".lower()

        for dom, tokens in self.domain_detectors.items():
            if any(tok.lower() in haystack for tok in tokens):
                domains.add(dom)

        return sorted(domains)

    @staticmethod
    def _passes_prefilter(rule: Dict[str, Any], source_code: str) -> bool:
        prefilter = rule.get("AstPreFilter", {})
        if not prefilter:
            return True
        min_lines = int(prefilter.get("MinLines", 0))
        if min_lines and len(source_code.splitlines()) < min_lines:
            return False
        contains_any = prefilter.get("ContainsAny", [])
        if contains_any and not any(tok in source_code for tok in contains_any):
            return False
        regex_pat = prefilter.get("RegexMatch")
        if regex_pat and not re.search(regex_pat, source_code, re.MULTILINE):
            return False
        return True

    def filter_rules_for_node(
        self, language: str, node_category: str, domains: List[str], source_code: str
    ) -> List[Dict[str, Any]]:
        matched: List[Dict[str, Any]] = []
        domain_set = set(domains)
        for rule in self.rules:
            if not rule.get("Enabled", True):
                continue
            rule_domain = rule.get("Domain", "GLOBAL")
            if rule_domain not in domain_set:
                continue
            scope = rule.get("Scope", {})
            langs = scope.get("Languages", ["*"])
            if "*" not in langs and language not in langs:
                continue
            cats = scope.get("NodeCategories", ["*"])
            if "*" not in cats and node_category not in cats:
                continue
            if not self._passes_prefilter(rule, source_code):
                continue
            matched.append(rule)
        return matched

    def build_node_context(self, graph: CodeMapGraph, node_id: str) -> str:
        """Build minimal causal + line-numbered source context for Gatekeeper/Explainer."""
        ndata = graph.g.nodes.get(node_id, {})
        props = ndata.get("props", {})
        scope = ndata.get("scope", {})
        file_path = scope.get("file", "")
        lang = self._infer_language(file_path)
        line_start = int(props.get("line_start", scope.get("line", 1)) or 1)
        src = props.get("source_code", "").rstrip()

        callers = [
            graph.g.nodes[u].get("props", {}).get("signature") or graph.g.nodes[u].get("label", u)
            for u in list(graph.g.predecessors(node_id))[:5]
        ]
        callees = [
            graph.g.nodes[v].get("props", {}).get("signature") or graph.g.nodes[v].get("label", v)
            for v in list(graph.g.successors(node_id))[:8]
        ]

        numbered_lines = [
            f"L{line_start + idx:04d}: {line}"
            for idx, line in enumerate(src.splitlines())
        ]

        header = [
            f"File: {file_path} (Language: {lang})",
            f"Symbol: {props.get('signature', ndata.get('label', node_id))}",
            f"Upstream Callers: {', '.join(callers) if callers else 'None (Entry/Top-level)'}",
            f"Downstream Callees: {', '.join(callees) if callees else 'None'}",
            "Target Source Code:",
            f"```{lang}",
            "\n".join(numbered_lines),
            "```",
        ]
        return "\n".join(header)

    def _inspect_single_node(
        self, graph: CodeMapGraph, node_id: str
    ) -> Optional[NodeLintResult]:
        ndata = graph.g.nodes.get(node_id, {})
        props = ndata.get("props", {})
        scope = ndata.get("scope", {})
        src = props.get("source_code", "")
        file_path = scope.get("file", "")
        lang = self._infer_language(file_path)
        line_start = int(props.get("line_start", scope.get("line", 1)) or 1)
        line_end = int(props.get("line_end", line_start + len(src.splitlines()) - 1) or line_start)

        domains = self.detect_node_domains(graph, node_id)
        matched_rules = self.filter_rules_for_node(
            lang, ndata.get("category", "FUNCTION_DEF"), domains, src
        )
        if not matched_rules:
            return None

        nr = NodeLintResult(
            node_id=node_id,
            label=str(ndata.get("label", node_id)),
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            domains=domains,
        )
        context = self.build_node_context(graph, node_id)
        rules_by_id = {r["Id"]: r for r in matched_rules}

        # Stage 1: Gatekeeper (Decision API)
        triggered: List[DecisionVerdict] = []
        if self.gatekeeper is not None:
            try:
                verdict_map, gk_ms = self.gatekeeper.evaluate(context, matched_rules)
                nr.gatekeeper_ms = gk_ms
                nr.verdicts = list(verdict_map.values())
                for v in nr.verdicts:
                    if v.status == "BLOCK" or (self.trigger_on == "WarnOrBlock" and v.status == "WARN"):
                        triggered.append(v)
            except LintProviderError as exc:
                nr.node_warnings.append(f"Gatekeeper ({self.gatekeeper.provider_name}) 失敗: {exc}")
                return nr
            except Exception as exc:
                nr.node_warnings.append(f"Gatekeeper 未預期錯誤: {exc}")
                return nr
        else:
            # Gatekeeper disabled: pass all matched rules directly to Explainer as WARN candidates
            for r in matched_rules:
                v = DecisionVerdict(
                    rule_id=r["Id"],
                    title=r.get("Title", r["Id"]),
                    domain=r.get("Domain", "GLOBAL"),
                    severity=r.get("Severity", "WARN"),
                    question_type="direct",
                    score=1.0,
                    confidence=1.0,
                    status="WARN",
                )
                nr.verdicts.append(v)
                triggered.append(v)

        # Stage 2: Explainer (Generative LLM) - only when triggered
        if triggered and self.explainer is not None:
            try:
                findings, exp_ms = self.explainer.explain(context, triggered, rules_by_id)
                nr.explainer_ms = exp_ms
                nr.findings = findings
            except LintProviderError as exc:
                nr.node_warnings.append(
                    f"Explainer ({self.explainer.provider_name}) 失敗 (已保留 Decision 結果): {exc}"
                )
            except Exception as exc:
                nr.node_warnings.append(f"Explainer 未預期錯誤 (已保留 Decision 結果): {exc}")

        return nr

    def lint_graph(
        self,
        graph: CodeMapGraph,
        target_node_ids: Optional[List[str]] = None,
        max_nodes: int = 20,
        max_workers: int = 4,
    ) -> SemanticLintReport:
        """Inspect executable nodes in `graph` using Fail-Open Decision + LLM pipeline."""
        gk_name = self.gatekeeper.provider_name if self.gatekeeper else "Disabled"
        exp_name = self.explainer.provider_name if self.explainer else "Disabled"

        if target_node_ids is not None:
            candidates = [
                nid for nid in target_node_ids
                if nid in graph.g and graph.g.nodes[nid].get("props", {}).get("source_code")
            ]
        else:
            candidates = [
                nid for nid, d in graph.g.nodes(data=True)
                if d.get("category") in ("FUNCTION_DEF", "MODULE_STATE")
                and d.get("props", {}).get("source_code")
            ]
            # Prioritize production functions over test functions and larger non-trivial nodes
            candidates.sort(
                key=lambda nid: (
                    1 if any(t in str(graph.g.nodes[nid].get("label", "")).lower() for t in ("test_", "_test")) else 0,
                    -len(graph.g.nodes[nid].get("props", {}).get("source_code", "").splitlines()),
                )
            )
            candidates = candidates[:max_nodes]

        report = SemanticLintReport(
            gatekeeper_name=gk_name,
            explainer_name=exp_name,
            nodes_inspected=0,
            nodes_skipped_by_prefilter=0,
            service_warnings=list(self.init_warnings),
        )

        if not candidates or (self.gatekeeper is None and self.explainer is None):
            return report

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_map = {
                pool.submit(self._inspect_single_node, graph, nid): nid
                for nid in candidates
            }
            for fut in as_completed(future_map):
                try:
                    res = fut.result()
                    if res is None:
                        report.nodes_skipped_by_prefilter += 1
                    else:
                        report.nodes_inspected += 1
                        report.node_results.append(res)
                except Exception as exc:
                    report.service_warnings.append(f"節點審查工作執行緒異常 ({future_map[fut]}): {exc}")

        # Stable deterministic ordering by file & start line
        report.node_results.sort(key=lambda r: (r.file_path, r.line_start, r.label))
        return report
