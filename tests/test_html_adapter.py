import os
import sys
import unittest

# 將專案根目錄加入模組搜尋路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.adapters import AdapterRegistry
from uia_coder.adapters.html_adapter import HTMLUIAGraphBuilder


class TestHTMLAdapter(unittest.TestCase):

    def setUp(self):
        self.builder = HTMLUIAGraphBuilder()

    def test_registry_supports_html(self):
        """測試語言註冊中心是否正確包含 HTML 且副檔名支援 .html, .htm"""
        adapter = AdapterRegistry.get_adapter("test.html")
        self.assertIsInstance(adapter, HTMLUIAGraphBuilder)
        adapter_htm = AdapterRegistry.get_adapter("view.htm")
        self.assertIsInstance(adapter_htm, HTMLUIAGraphBuilder)

    def test_clean_html_passes_invariants(self):
        """測試乾淨結構完整的 HTML 頁面正常通過形式化驗收 (READY_TO_SHIP)"""
        html_code = """<!DOCTYPE html>
<html>
<head><title>Clean Page</title></head>
<body>
  <div class="container">
    <button id="btn-save" class="btn btn-primary">Save</button>
    <input id="user-name" type="text" />
  </div>
</body>
</html>"""
        graph = self.builder.parse_and_build(html_code, file_path="clean.html")
        verdict = graph.check_invariants()
        self.assertTrue(verdict["passed"])
        self.assertEqual(verdict["verdict"], "🟢 READY_TO_SHIP")
        self.assertEqual(len(verdict["hazards"]), 0)

        # 驗證 UI 錨點接地
        anchors = graph.get_ui_anchors()
        anchor_labels = [graph.g.nodes[a]["label"] for a in anchors]
        self.assertTrue(any("btn-save" in l for l in anchor_labels))
        self.assertTrue(any("user-name" in l for l in anchor_labels))

    def test_unclosed_tag_blocked(self):
        """測試未閉合結構性標籤能被精確攔截為 BLOCKED_BY_INVARIANTS"""
        html_code = """<div class="app-layout">
  <div class="sidebar">
    <button id="btn-menu">Menu</button>
  <!-- 缺少 sidebar 的 </div> 閉合標籤 -->
</div>"""
        graph = self.builder.parse_and_build(html_code, file_path="unclosed.html")
        verdict = graph.check_invariants()
        self.assertFalse(verdict["passed"])
        self.assertEqual(verdict["verdict"], "🔴 BLOCKED_BY_INVARIANTS")
        hazard_types = [h["type"] for h in verdict["hazards"]]
        self.assertIn("UNCLOSED_TAG", hazard_types)

    def test_modal_trapped_in_hidden_container_blocked(self):
        """測試獨立對話框若被誤嵌於 hidden/display:none 容器內部，能被物理可見性守衛攔截"""
        html_code = """<div class="app-layout">
  <div id="drawer" hidden>
    <div id="confirm-modal" class="modal-overlay">
      <button id="btn-confirm">OK</button>
    </div>
  </div>
</div>"""
        graph = self.builder.parse_and_build(html_code, file_path="modal_trapped.html")
        verdict = graph.check_invariants()
        self.assertFalse(verdict["passed"])
        self.assertEqual(verdict["verdict"], "🔴 BLOCKED_BY_INVARIANTS")
        hazard_types = [h["type"] for h in verdict["hazards"]]
        self.assertIn("VISIBILITY_VIOLATION", hazard_types)
        # 違規訊息中應包含 drawer 與 confirm-modal 的 ID
        vis_hazards = [h for h in verdict["hazards"] if h["type"] == "VISIBILITY_VIOLATION"]
        self.assertTrue(any("confirm-modal" in h["detail"] and "drawer" in h["detail"] for h in vis_hazards))


if __name__ == "__main__":
    unittest.main()
