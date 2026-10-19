import os
import sys

# 將專案根目錄加入模組搜尋路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.adapters import get_adapter_for_file, AdapterRegistry
from uia_coder.core.graph import UIACodeGraph
from uia_coder.core.differ import UIAGraphDiffer


def test_registry_supported_languages():
    print("\n" + "=" * 60)
    print("▶ 測試 0: 語言註冊中心與自動分發驗證")
    print("=" * 60)

    languages = AdapterRegistry.list_supported_languages()
    for lang in languages:
        print(f"  • {lang['language']:12} -> {lang['extensions']}")

    assert len(languages) >= 3
    js_adapter = get_adapter_for_file("app.js")
    assert js_adapter.language_name == "JavaScript"
    py_adapter = get_adapter_for_file("gui.py")
    assert py_adapter.language_name == "Python"
    rust_adapter = get_adapter_for_file("server.rs")
    assert rust_adapter.language_name == "Rust"
    print("✅ 測試 0 通過：語言註冊中心與自動路由 (JS/TS/Python/Rust) 100% 正常！")


def get_src_path(filename: str) -> str:
    return os.path.join(project_root, "src", filename)


def test_js_buggy_commit():
    print("\n" + "=" * 60)
    print("▶ 測試 1 (JavaScript): Buggy Commit (閉包作用域囚禁 + confirm 阻塞)")
    print("=" * 60)

    with open(get_src_path("workspaceFileTree_buggy.js"), "r", encoding="utf-8") as f:
        code = f.read()

    adapter = get_adapter_for_file("workspaceFileTree.js")
    graph = adapter.parse_and_build(code, file_path="workspaceFileTree_buggy.js")

    inv = graph.check_invariants()
    assert not inv["passed"], "Buggy commit 必須亮紅牌被阻擋！"
    assert len(inv["scope_errors"]) > 0, "必須抓出閉包 ReferenceError！"
    print("✅ 測試 1 通過：成功攔截 JavaScript 閉包死穴！")


def test_js_fixed_commit():
    print("\n" + "=" * 60)
    print("▶ 測試 2 (JavaScript): Fix Commit (作用域提升修復 + 守衛驗收通過)")
    print("=" * 60)

    with open(get_src_path("workspaceFileTree.js"), "r", encoding="utf-8") as f:
        code = f.read()

    adapter = get_adapter_for_file("workspaceFileTree.js")
    graph = adapter.parse_and_build(code, file_path="workspaceFileTree.js")

    inv = graph.check_invariants()
    assert inv["passed"], "Fix commit 必須亮綠燈放行！"
    print("✅ 測試 2 通過：JavaScript 修復版完全通過驗收！")


def test_python_buggy_code():
    print("\n" + "=" * 60)
    print("▶ 測試 3 (Python): PyQt/Tkinter Buggy 案例 (閉包囚禁 + time.sleep 凍結 UI)")
    print("=" * 60)

    buggy_py_code = """
    import time
    def setup_ui():
        def on_delete_clicked():
            time.sleep(5)
    self.btn_delete = QPushButton("刪除項目")
    self.btn_delete.clicked.connect(on_delete_clicked)
    """

    adapter = get_adapter_for_file("file_manager.py")
    graph = adapter.parse_and_build(buggy_py_code, file_path="file_manager.py")

    inv = graph.check_invariants()
    assert not inv["passed"]
    assert len(inv["scope_errors"]) > 0
    assert len(inv["hazards"]) > 0
    print("✅ 測試 3 通過：成功攔截 Python 閉包死穴與 time.sleep UI 凍結危害！")


def test_python_fixed_code():
    print("\n" + "=" * 60)
    print("▶ 測試 4 (Python): PyQt/Tkinter Fix 案例 (正確方法可達性 + 非同步背景執行)")
    print("=" * 60)

    fixed_py_code = """
    def on_delete_clicked():
        execute_async_rpc()

    def execute_async_rpc():
        pass

    self.btn_delete = QPushButton("刪除項目")
    self.btn_delete.clicked.connect(on_delete_clicked)
    """

    adapter = get_adapter_for_file("file_manager.py")
    graph = adapter.parse_and_build(fixed_py_code, file_path="file_manager.py")

    inv = graph.check_invariants()
    assert inv["passed"]
    print("✅ 測試 4 通過：Python 修復版本全綠燈通過驗收！")


def test_graph_diffing():
    print("\n" + "=" * 60)
    print("▶ 測試 5: UIA-Graph 語意圖譜差分驗收 (Buggy ➔ Fixed 演進比對)")
    print("=" * 60)

    adapter = get_adapter_for_file("workspaceFileTree.js")
    with open(get_src_path("workspaceFileTree_buggy.js"), "r", encoding="utf-8") as f:
        g_b = adapter.parse_and_build(f.read(), "before.js")
    with open(get_src_path("workspaceFileTree.js"), "r", encoding="utf-8") as f:
        g_a = adapter.parse_and_build(f.read(), "after.js")

    diff_res = UIAGraphDiffer.diff_graphs(g_b, g_a)
    print(diff_res.to_diff_markdown())

    # 斷言
    assert diff_res.passed, "修復後的圖譜必須通過驗收！"
    assert len(diff_res.status_transitions) > 0, "必須檢測到 BLOCKED_SCOPE ➔ VALID 的狀態修復躍遷！"
    assert any(t["from"] == "BLOCKED_SCOPE" and t["to"] == "VALID" for t in diff_res.status_transitions)
    print("\n✅ 測試 5 通過：UIA 圖譜差分引擎成功檢測因果躍遷與修復驗收！")


def test_rust_support():
    print("\n" + "=" * 60)
    print("▶ 測試 6 (Rust): WebServer 結構體關聯方法、CLI 進入點與 todo!() 危害阻擋")
    print("=" * 60)

    rust_file = get_src_path("sample_rust_app.rs")
    with open(rust_file, "r", encoding="utf-8") as f:
        code = f.read()

    adapter = get_adapter_for_file("sample_rust_app.rs")
    assert adapter.language_name == "Rust"

    graph = adapter.parse_and_build(code, file_path="sample_rust_app.rs")

    # 驗證 CLI 入口
    nodes_by_label = {d.get("label"): n for n, d in graph.g.nodes(data=True)}
    assert "#CLI: main" in nodes_by_label, "必須自動識別 fn main() 並建構 #CLI: main 根節點！"
    assert "WebServer::start" in nodes_by_label, "必須識別 impl WebServer 結構體關聯方法！"
    assert "WebServer::bind_socket" in nodes_by_label, "必須識別 self.bind_socket() 私有呼叫！"

    # 驗證危害攔截
    inv = graph.check_invariants()
    assert not inv["passed"], "存在 todo!() 巨集的 Rust 程式必須亮紅牌攔截！"
    assert len(inv["hazards"]) > 0, "必須檢測到 todo!() 造成的 RUST_TODO 執行期危害！"
    print(f"  • 成功攔截未決危害: {[h.get('detail') for h in inv['hazards']]}")
    print("✅ 測試 6 通過：Rust Tree-sitter 控制樹與 todo!() 執行期危害完全攔截！")


if __name__ == "__main__":
    test_registry_supported_languages()
    test_js_buggy_commit()
    test_js_fixed_commit()
    test_python_buggy_code()
    test_python_fixed_code()
    test_graph_diffing()
    test_rust_support()
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS (INCLUDING RUST & UIA-DIFF) PASSED WITH 100% SUCCESS!")
    print("=" * 60)

