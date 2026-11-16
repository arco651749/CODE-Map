import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from code_map.adapters import get_adapter_for_file
from code_map.cli import _extract_diff_target_nodes
from code_map.core.differ import CodeMapDiffer
from code_map.core.lint_providers import (
    CliExplainer,
    GeminiDecisionProvider,
    HttpTemplateDecisionProvider,
    LintProviderError,
    OpenAiDecisionProvider,
)
from code_map.core.semantic_linter import DEFAULT_RULES_PATH, SemanticLinter


class TestSemanticLinter(unittest.TestCase):
    def _load_default_cfg(self) -> dict:
        with open(DEFAULT_RULES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_domain_routing_and_cli_exclusion(self):
        py_code = (
            "import click\n"
            "@click.command()\n"
            "def main():\n"
            "    with open('out.txt', 'w', encoding='utf-8') as f:\n"
            "        f.write('ok')\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
        adapter = get_adapter_for_file("cli_app.py")
        graph = adapter.parse_and_build(py_code, file_path="cli_app.py")

        linter = SemanticLinter(self._load_default_cfg(), api_key_override="test-key")
        main_nodes = [n for n, d in graph.g.nodes(data=True) if d.get("label") == "main"]
        self.assertTrue(main_nodes)
        domains = linter.detect_node_domains(graph, main_nodes[0])
        self.assertIn("GLOBAL", domains)
        self.assertIn("DISK_IO", domains)
        self.assertNotIn("UI", domains)

    def test_gui_domain_routing_for_csharp_button(self):
        cs_code = (
            "using Avalonia.Controls;\n"
            "public class MainWindow {\n"
            "    public MainWindow() {\n"
            "        SaveButton.Click += OnSaveClick;\n"
            "    }\n"
            "    private void OnSaveClick(object sender, System.EventArgs e) {\n"
            "        System.Threading.Thread.Sleep(500);\n"
            "    }\n"
            "}\n"
        )
        adapter = get_adapter_for_file("MainWindow.axaml.cs")
        graph = adapter.parse_and_build(cs_code, file_path="MainWindow.axaml.cs")
        linter = SemanticLinter(self._load_default_cfg(), api_key_override="test-key")
        handler_nodes = [
            n for n, d in graph.g.nodes(data=True)
            if "OnSaveClick" in str(d.get("label", "")) and d.get("props", {}).get("source_code")
        ]
        self.assertTrue(handler_nodes)
        domains = linter.detect_node_domains(graph, handler_nodes[0])
        self.assertIn("UI", domains)

    def test_from_file_provider_override_strips_stale_endpoint(self):
        linter = SemanticLinter.from_file(
            gatekeeper_override="Disabled",
            explainer_override="AgyCli",
            explainer_model_override="gemini-3.8-flash-low",
        )
        self.assertIsNone(linter.gatekeeper)
        self.assertIsInstance(linter.explainer, CliExplainer)
        self.assertEqual(linter.explainer.command, "agy")
        self.assertEqual(linter.explainer.model, "gemini-3.8-flash-low")

    def test_gemini_decision_and_explainer_two_stage_flow(self):
        py_code = (
            "def bad_fn(x):\n"
            "    try:\n"
            "        return 1 / x\n"
            "    except Exception as e:\n"
            "        _ = e\n"
            "        return 0\n"
        )
        adapter = get_adapter_for_file("bad.py")
        graph = adapter.parse_and_build(py_code, file_path="bad.py")
        linter = SemanticLinter(self._load_default_cfg(), api_key_override="dummy-key")

        decision_resp = {
            "answers": {
                "GLOBAL-SWALLOW-01": {"type": "noul", "noul": 0.94, "confidence": 0.94},
                "GLOBAL-STUB-01": {
                    "type": "choice",
                    "selected_option": "real_impl",
                    "confidence": 0.99,
                    "probabilities": {"real_impl": 0.99},
                },
            }
        }
        explainer_resp = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps(
                                    {
                                        "findings": [
                                            {
                                                "rule_id": "GLOBAL-SWALLOW-01",
                                                "evidence_lines": "L4-L6",
                                                "reasoning": "吞掉例外並用 _ = e 規避檢查",
                                                "suggested_fix": "記錄日誌或重新拋出例外",
                                            }
                                        ]
                                    },
                                    ensure_ascii=False,
                                )
                            }
                        ]
                    }
                }
            ]
        }

        with patch(
            "code_map.core.lint_providers._http_post_json",
            side_effect=[decision_resp, explainer_resp],
        ) as mock_post:
            report = linter.lint_graph(graph)

        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(report.total_blocks, 1)
        self.assertTrue(report.has_blocks)
        md = report.to_markdown()
        self.assertIn("0.9400", md)
        self.assertIn("L4-L6", md)
        self.assertIn("吞掉例外", md)

    def test_fail_open_when_explainer_crashes_preserves_decision_verdicts(self):
        py_code = (
            "def bad_fn(x):\n"
            "    try:\n"
            "        return 1 / x\n"
            "    except Exception as e:\n"
            "        _ = e\n"
            "        return 0\n"
        )
        adapter = get_adapter_for_file("bad.py")
        graph = adapter.parse_and_build(py_code, file_path="bad.py")
        linter = SemanticLinter(self._load_default_cfg(), api_key_override="dummy-key")

        decision_resp = {
            "answers": {
                "GLOBAL-SWALLOW-01": {"type": "noul", "noul": 0.91, "confidence": 0.91},
                "GLOBAL-STUB-01": {
                    "type": "choice",
                    "selected_option": "real_impl",
                    "confidence": 0.99,
                    "probabilities": {"real_impl": 0.99},
                },
            }
        }

        with patch(
            "code_map.core.lint_providers._http_post_json",
            side_effect=[decision_resp, LintProviderError("HTTP 503 Service Unavailable")],
        ):
            report = linter.lint_graph(graph)

        self.assertEqual(report.total_blocks, 1)
        md = report.to_markdown()
        self.assertIn("AI-LINT-SERVICE-WARN", md)
        self.assertIn("0.9100", md)

    def test_fail_open_when_gatekeeper_missing_api_key(self):
        py_code = (
            "def ok_fn(x):\n"
            "    if x == 0:\n"
            "        raise ValueError('x cannot be zero')\n"
            "    return 1 / x\n"
        )
        adapter = get_adapter_for_file("ok.py")
        graph = adapter.parse_and_build(py_code, file_path="ok.py")

        with patch.dict(os.environ, {}, clear=True):
            linter = SemanticLinter(self._load_default_cfg(), api_key_override=None)
            report = linter.lint_graph(graph)

        self.assertEqual(report.total_blocks, 0)
        self.assertFalse(report.has_blocks)
        self.assertIn("AI-LINT-SERVICE-WARN", report.to_markdown())

    def test_http_template_and_openai_decision_adapters(self):
        rules = [
            {
                "Id": "R1",
                "Title": "Rule 1",
                "Domain": "GLOBAL",
                "Severity": "BLOCK",
                "Decision": {"Type": "noul", "Instructions": "Check R1"},
                "Thresholds": {"Warn": 0.6, "Block": 0.85},
            }
        ]
        tpl_provider = HttpTemplateDecisionProvider(
            {
                "Endpoint": "https://jev.example/decide",
                "Model": "jev-1",
                "Headers": {"Authorization": "Bearer $JEV_KEY"},
                "ResponseMapping": {"answers_path": "data.results", "score_field": "prob"},
            },
            api_key_override="jev-secret",
        )
        with patch(
            "code_map.core.lint_providers._http_post_json",
            return_value={"data": {"results": {"R1": {"prob": 0.89, "confidence": 0.89}}}},
        ):
            verdicts, _ = tpl_provider.evaluate("code", rules)
        self.assertEqual(verdicts["R1"].status, "BLOCK")

        oai_provider = OpenAiDecisionProvider({"Model": "gpt-4o-mini"}, api_key_override="oai-key")
        with patch(
            "code_map.core.lint_providers._http_post_json",
            return_value={
                "choices": [
                    {
                        "message": {
                            "content": json.dumps({"answers": {"R1": {"score": 0.72, "confidence": 0.80}}})
                        }
                    }
                ]
            },
        ):
            verdicts_oai, _ = oai_provider.evaluate("code", rules)
        self.assertEqual(verdicts_oai["R1"].status, "WARN")

    def test_agy_cli_envelope_unwrap(self):
        explainer = CliExplainer("AgyCli", {"Model": "gemini-3.8-flash-low"})
        fake_proc = MagicMock(
            returncode=0,
            stdout=json.dumps(
                {
                    "response": json.dumps(
                        {
                            "findings": [
                                {
                                    "rule_id": "R1",
                                    "evidence_lines": "L1-L2",
                                    "reasoning": "測試理由",
                                    "suggested_fix": "測試修正",
                                }
                            ]
                        },
                        ensure_ascii=False,
                    )
                },
                ensure_ascii=False,
            ),
            stderr="",
        )
        verdict_mock = MagicMock(rule_id="R1", title="Rule 1", status="BLOCK", score=0.9, selected_choice=None)
        with patch("shutil.which", return_value="C:\\bin\\agy.exe"), patch(
            "subprocess.run", return_value=fake_proc
        ):
            findings, _ = explainer.explain("L0001: pass", [verdict_mock], {"R1": {}})
        self.assertIn("R1", findings)
        self.assertEqual(findings["R1"].evidence_lines, "L1-L2")

    def test_extract_diff_target_nodes_filters_only_changed_functions(self):
        before = (
            "def untouched(a):\n"
            "    return a + 1\n\n"
            "def changed(x):\n"
            "    return x * 2\n"
        )
        after = (
            "def untouched(a):\n"
            "    return a + 1\n\n"
            "def changed(x):\n"
            "    return x * 3\n\n"
            "def added(y):\n"
            "    return y - 1\n"
        )
        diff_res = CodeMapDiffer.diff_source(before, after, ext=".py", file_path="mod.py")
        targets = _extract_diff_target_nodes(diff_res)
        labels = {diff_res.g_after.g.nodes[nid].get("label") for nid in targets}
        self.assertIn("changed", labels)
        self.assertIn("added", labels)
        self.assertNotIn("untouched", labels)


if __name__ == "__main__":
    unittest.main(verbosity=2)
