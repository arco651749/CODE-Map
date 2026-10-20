import os
import sys
import tempfile
import networkx as nx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.adapters import get_adapter_for_file
from uia_coder.core.differ import UIAGraphDiffer
from uia_coder.core.spec_verifier import SpecVerifier, SpecContract, verify_objection
from uia_coder.core.workspace_graph import WorkspaceGraphBuilder


def test_a_same_name_no_collision():
    print("\n" + "=" * 60)
    print("▶ Test A: 同一檔案內多個元件同名函式防碰撞驗證 (Qualified Path)")
    print("=" * 60)

    # 模擬同一個檔案內有 UserModal 與 ItemCard 兩個元件，內部皆有 handleClick
    code_before = """
    function UserModal() {
        const handleClick = () => {
            console.log("UserModal clicked v1");
        };
    }

    function ItemCard() {
        const handleClick = () => {
            console.log("ItemCard clicked constant");
        };
    }
    """

    # 修改 UserModal 的 handleClick，保持 ItemCard 的 handleClick 不變
    code_after = """
    function UserModal() {
        const handleClick = () => {
            console.log("UserModal clicked v2 - modified!");
        };
    }

    function ItemCard() {
        const handleClick = () => {
            console.log("ItemCard clicked constant");
        };
    }
    """

    adapter = get_adapter_for_file("app.tsx")
    g_before = adapter.parse_and_build(code_before, file_path="app.tsx")
    g_after = adapter.parse_and_build(code_after, file_path="app.tsx")

    # 驗證圖中兩個 handleClick 節點皆獨立存在
    funcs_b = [d.get("label") for n, d in g_before.g.nodes(data=True) if d.get("category") == "FUNCTION_DEF"]
    assert funcs_b.count("handleClick") == 2, f"圖中必須同時保留兩個 handleClick 節點，實際: {funcs_b}"

    # 執行圖差分
    diff_res = UIAGraphDiffer.diff_graphs(g_before, g_after)

    # 斷言：functions_modified 必須「精準只捕獲被修改的 UserModal 及其內部 handleClick」，ItemCard 不受影響
    modified_cids = [f["canonical_id"] for f in diff_res.functions_modified]
    print(f"  • 偵測到之函式實作變更: {modified_cids}")
    assert any("UserModal::handleClick" in cid for cid in modified_cids), "必須精準識別出 UserModal 內部的 handleClick 變更"
    assert not any("ItemCard" in cid for cid in modified_cids), "ItemCard 及其內部的 handleClick 絕不可被誤認為變更或覆蓋"
    assert all("UserModal" in cid for cid in modified_cids), "所有變更必須精準限制在 UserModal 範圍內"
    print("✅ Test A 通過：同名函式依 Qualified Path 隔離，未發生字典靜默覆寫！")


def test_b_conditional_guards_and_early_return():
    print("\n" + "=" * 60)
    print("▶ Test B: AST 條件守衛 (if 分支) 與 Early-Return 守衛精確識別")
    print("=" * 60)

    # 案例 1: 帶有 if (!confirmed) return; Early-Return 守衛
    code_guarded = """
    async function handleDeleteFlow() {
        const confirmed = await confirmModal("確定刪除？");
        if (!confirmed) return;
        await deleteRpc();
    }
    """

    # 案例 2: 忘記寫 if 守衛，直接往下刪 (致命危害)
    code_unguarded = """
    async function handleDeleteFlow() {
        const confirmed = await confirmModal("確定刪除？");
        await deleteRpc();
    }
    """

    adapter = get_adapter_for_file("flow.js")
    g_guarded = adapter.parse_and_build(code_guarded, file_path="flow.js")
    g_unguarded = adapter.parse_and_build(code_unguarded, file_path="flow.js")

    # 檢查 g_guarded 中到 deleteRpc 的呼叫邊
    edge_guarded = None
    for u, v, d in g_guarded.g.edges(data=True):
        if "deleteRpc" in v:
            edge_guarded = d
            break

    assert edge_guarded is not None, "必須找到 deleteRpc 的呼叫邊"
    assert edge_guarded.get("is_conditional") is True, "有 early-return 守衛時 is_conditional 必須為 True！"
    assert edge_guarded.get("guard_type") == "EARLY_RETURN_GUARD", f"guard_type 應為 EARLY_RETURN_GUARD，實際: {edge_guarded.get('guard_type')}"
    print(f"  • Guarded 邊屬性: is_conditional={edge_guarded.get('is_conditional')}, guard_type={edge_guarded.get('guard_type')}, expr={edge_guarded.get('guard_expr')}")

    # 檢查 g_unguarded 中到 deleteRpc 的呼叫邊
    edge_unguarded = None
    for u, v, d in g_unguarded.g.edges(data=True):
        if "deleteRpc" in v:
            edge_unguarded = d
            break

    assert edge_unguarded is not None, "必須找到 deleteRpc 的呼叫邊"
    assert edge_unguarded.get("is_conditional") is False, "未加條件守衛時 is_conditional 必須為 False！"
    print("✅ Test B 通過：AST 引擎成功區分受 Early-Return 保護的呼叫與裸露危險呼叫！")


def test_c_spec_verifier_helper_tolerance():
    print("\n" + "=" * 60)
    print("▶ Test C: SpecVerifier 容許 Helper 輔助函式抽取與偏序約束驗收")
    print("=" * 60)

    # 定義上位架構師契約: #btnDelete ➔ confirmModal ➔ deleteRpc (要求 await 與 conditional guard)
    spec_dict = {
        "required_anchors": ["#btnDelete"],
        "required_causal_chains": [
            {
                "anchor": "#btnDelete",
                "chain": ["confirmModal", "deleteRpc"],
                "constraints": {
                    "deleteRpc": {
                        "require_await": True,
                        "require_conditional_guard": True,
                    }
                }
            }
        ]
    }

    # 實作代碼 1 (合法優良實作: 抽取了 onBtnClick 與 doDelete 兩個 Helper 函式)
    code_good_implementation = """
    const btnDelete = document.createElement('button');
    btnDelete.id = 'btnDelete';
    btnDelete.addEventListener('click', onBtnClick);

    async function onBtnClick() {
        const ok = await confirmModal();
        if (!ok) return;
        await doDelete();
    }

    async function doDelete() {
        await deleteRpc();
    }

    async function confirmModal() {}
    async function deleteRpc() {}
    """

    # 實作代碼 2 (違規實作 A: 漏了 await deleteRpc)
    code_bad_missing_await = """
    const btnDelete = document.createElement('button');
    btnDelete.id = 'btnDelete';
    btnDelete.addEventListener('click', onBtnClick);

    async function onBtnClick() {
        const ok = await confirmModal();
        if (!ok) return;
        deleteRpc(); // 💥 Bug: 忘了 await
    }

    async function confirmModal() {}
    async function deleteRpc() {}
    """

    # 實作代碼 3 (違規實作 B: 漏了條件守衛)
    code_bad_missing_guard = """
    const btnDelete = document.createElement('button');
    btnDelete.id = 'btnDelete';
    btnDelete.addEventListener('click', onBtnClick);

    async function onBtnClick() {
        await confirmModal();
        // 💥 Bug: 忘了 if (!ok) return;
        await deleteRpc();
    }

    async function confirmModal() {}
    async function deleteRpc() {}
    """

    adapter = get_adapter_for_file("app.js")
    g_good = adapter.parse_and_build(code_good_implementation, file_path="app.js")
    g_bad_await = adapter.parse_and_build(code_bad_missing_await, file_path="app.js")
    g_bad_guard = adapter.parse_and_build(code_bad_missing_guard, file_path="app.js")

    # 驗證 1: 優良實作必須 PASS (即使抽取了中間 Helper)
    res_good = SpecVerifier.verify(spec=spec_dict, actual=g_good)
    print(f"  • Good 實作裁決: {res_good.verdict}")
    assert res_good.passed is True, f"優質 Helper 抽取實作必須通過驗收！違規: {res_good.violations}"

    # 驗證 2: 漏 await 必須 FAIL
    res_bad_await = SpecVerifier.verify(spec=spec_dict, actual=g_bad_await)
    print(f"  • Bad (Missing Await) 裁決: {res_bad_await.verdict}")
    assert res_bad_await.passed is False, "漏 await 必須被裁判攔截！"
    assert any(v["type"] == "MISSING_AWAIT" for v in res_bad_await.violations)

    # 驗證 3: 漏條件守衛必須 FAIL
    res_bad_guard = SpecVerifier.verify(spec=spec_dict, actual=g_bad_guard)
    print(f"  • Bad (Missing Guard) 裁決: {res_bad_guard.verdict}")
    assert res_bad_guard.passed is False, "漏條件守衛必須被裁判攔截！"
    assert any(v["type"] == "MISSING_CONDITIONAL_GUARD" for v in res_bad_guard.violations)

    print("✅ Test C 通過：SpecVerifier 成功容許 Helper 函式，同時零死角攔截時序與守衛違規！")


def test_d_cross_file_linking_and_unexported_blocking():
    print("\n" + "=" * 60)
    print("▶ Test D: 跨檔案 Import/Export 接線消解與未 Export 作用域阻隔驗證")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        api_file = os.path.join(tmpdir, "user_api.ts")
        ui_file = os.path.join(tmpdir, "UserPanel.tsx")

        # 案例 1: 正常匯出與匯入 (Valid Export)
        with open(api_file, "w", encoding="utf-8") as f:
            f.write("""
            export async function deleteUserRpc(id: string) {
                console.log("執行使用者遠端刪除:", id);
            }
            """)

        with open(ui_file, "w", encoding="utf-8") as f:
            f.write("""
            import { deleteUserRpc } from './user_api';

            const btnDelete = document.createElement('button');
            btnDelete.id = 'btnDelete';
            btnDelete.addEventListener('click', handleDelete);

            async function handleDelete() {
                await deleteUserRpc("u123");
            }
            """)

        workspace_graph_valid = WorkspaceGraphBuilder.build_from_files([api_file, ui_file], root_dir=tmpdir)

        # 驗證跨檔切片：從 #btnDelete 必須能跨檔案可達 deleteUserRpc
        anchors = workspace_graph_valid.get_ui_anchors()
        assert len(anchors) > 0, "必須找到 UI 控制項"
        anchor = anchors[0]
        descendants = nx.descendants(workspace_graph_valid.g, anchor)
        descendant_labels = [workspace_graph_valid.g.nodes[n].get("label") for n in descendants]
        print(f"  • 跨檔切片波及函式: {descendant_labels}")
        assert "deleteUserRpc" in descendant_labels, "跨檔切片必須成功連通至 user_api.ts 中的 deleteUserRpc！"

        inv_valid = workspace_graph_valid.check_invariants()
        assert inv_valid["passed"] is True, "正常匯出的跨檔專案必須綠燈放行！"

        # 案例 2: 忘記加 export 關鍵字 (Not Exported Bug)
        with open(api_file, "w", encoding="utf-8") as f:
            f.write("""
            // 💥 致命 Bug: 忘了加 export
            async function deleteUserRpc(id: string) {
                console.log("執行使用者遠端刪除:", id);
            }
            """)

        workspace_graph_blocked = WorkspaceGraphBuilder.build_from_files([api_file, ui_file], root_dir=tmpdir)
        inv_blocked = workspace_graph_blocked.check_invariants()
        print(f"  • 未 Export 專案驗收裁決: {inv_blocked['verdict']}")
        assert inv_blocked["passed"] is False, "目標函式未匯出時必須亮紅牌攔截！"
        assert len(inv_blocked["scope_errors"]) > 0, "必須產生跨模組作用域阻隔 (BLOCKED_SCOPE)！"
        print(f"  • 成功抓出跨模組死穴: {inv_blocked['scope_errors'][0]['detail']}")

    print("✅ Test D 通過：WorkspaceGraphBuilder 成功實現跨檔符號接線，並嚴格阻隔未 Export 函式！")


def test_e_spec_objection_ast_verification():
    print("\n" + "=" * 60)
    print("▶ Test E: Subagent 規格異議 (Spec Objection) AST 自動防偽查核")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        api_file = os.path.join(tmpdir, "items_api.ts")
        with open(api_file, "w", encoding="utf-8") as f:
            f.write("""
            export async function deleteMany(ids: string[]) {
                console.log("批次刪除:", ids);
            }
            """)

        # 異議 1: 屬實 (宣稱不存在 deleteItem，只提供 deleteMany)
        genuine_objection = {
            "target": "edge: confirmModal -> deleteItem",
            "reason": "後端只支援批次刪除",
            "evidence": "items_api.ts:L2 只提供 deleteMany",
        }
        res_genuine = verify_objection(genuine_objection, workspace_root=tmpdir)
        print(f"  • 屬實異議查證: {res_genuine['status']} -> {res_genuine['report']}")
        assert res_genuine["is_valid"] is True

        # 異議 2: 不實偷懶謊報 (宣稱不存在 deleteMany，想藉此推託實作)
        falsified_objection = {
            "target": "edge: confirmModal -> deleteMany",
            "reason": "後端沒有 deleteMany",
            "evidence": "items_api.ts:L2 不存在 deleteMany",
        }
        res_falsified = verify_objection(falsified_objection, workspace_root=tmpdir)
        print(f"  • 不實異議查證: {res_falsified['status']} -> {res_falsified['report']}")
        assert res_falsified["is_valid"] is False

    print("✅ Test E 通過：Spec Objection AST 實地防偽查核成功識破虛假證據！")


def run_all_next_phase_tests():
    test_a_same_name_no_collision()
    test_b_conditional_guards_and_early_return()
    test_c_spec_verifier_helper_tolerance()
    test_d_cross_file_linking_and_unexported_blocking()
    test_e_spec_objection_ast_verification()

    print("\n" + "=" * 60)
    print("🎉 ALL NEXT-PHASE ADVANCED TESTS (TESTS A, B, C, D, E) PASSED 100%!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_next_phase_tests()
