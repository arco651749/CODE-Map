import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from code_map.adapters import AdapterRegistry, get_adapter_for_file
from code_map.core.differ import CodeMapDiffer
from code_map.core.spec_verifier import SpecVerifier, verify_objection
from code_map.core.workspace_graph import WorkspaceGraphBuilder


def main():
    parser = argparse.ArgumentParser(
        description="🌲 CODE-Map: Causal Operation & Dependency Evaluation Map (行為因果與接線依賴評估地圖引擎)"
    )
    parser.add_argument("--file", help="目標分析之單一源碼檔案路徑 (自動依副檔名匹配語言)")
    parser.add_argument("--files", nargs="+", help="聯合解析多個源碼檔案並自動消解跨檔案 import/export 依賴")
    parser.add_argument("--dir", help="遍歷指定目錄下所有源碼檔案並聯合建構工作區圖譜")
    parser.add_argument("--export-json", help="導出 NetworkX Node-Link JSON 檔案路徑")
    parser.add_argument("--slice", help="針對特定 UI 錨點 (Anchor ID) 進行前向圖切片")
    parser.add_argument("--bundle", help="以特定 UI 控制項 (Anchor ID 或 Label) 為起點，提取其波及的全部函式真實原始碼包")
    parser.add_argument("--locate", help="SWE-bench 雙向病灶定位：依符號關鍵字搜尋節點，同時打包『上游呼叫者 (Callers) + 目標函式 + 下游被呼叫者 (Callees)』源碼")
    parser.add_argument("--check", action="store_true", help="執行形式化不變量守衛檢驗，有違規時返回非 0 狀態碼")
    parser.add_argument("--html", help="導出互動式 HTML 雙欄視覺化儀表板檔案路徑")
    parser.add_argument("--list-languages", action="store_true", help="列出目前所有已支援的程式語言與副檔名")
    
    # 規格驗收與異議查證
    parser.add_argument("--verify-spec", help="指定上位架構圖譜契約檔案 (JSON/YAML/源碼)，對實作進行偏序驗收")
    parser.add_argument("--verify-objection", help="指定 Subagent 提交之 Spec Objection (YAML/JSON)，進行 AST 防偽查證")

    # 差分專用參數
    parser.add_argument("--diff-files", nargs=2, metavar=("BEFORE_FILE", "AFTER_FILE"), help="比對兩個檔案間的 UIA 語意圖譜差分 (規格 vs 實作)")
    parser.add_argument("--git-diff", nargs="?", const="HEAD~1", help="比對指定檔案在 Git 歷史中的 UIA 語意差分 (預設 HEAD~1)")
    parser.add_argument("--repo", default=".", help="Git 倉庫目錄路徑 (配合 --git-diff 使用)")

    args = parser.parse_args()

    if args.list_languages:
        print("🌲 CODE-Map 目前支援之程式語言：")
        for item in AdapterRegistry.list_supported_languages():
            print(f"  • {item['language']:12} (副檔名: {item['extensions']})")
        return

    # 0. 規格異議 AST 查證 (Spec Objection Verification)
    if args.verify_objection:
        print(f"🔍 正在對 Subagent 異議報告執行 AST 實地防偽查證: [{args.verify_objection}]...")
        with open(args.verify_objection, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            import yaml
            obj_data = yaml.safe_load(raw)
        except ImportError:
            obj_data = json.loads(raw)

        if "objection" in obj_data:
            obj_data = obj_data["objection"]

        res = verify_objection(obj_data, workspace_root=args.repo)
        print("\n" + res["report"])
        if not res["is_valid"]:
            sys.exit(1)
        return

    # 1. 雙檔案圖譜差分 (Subagent 實作 vs 期望規格，或 Buggy vs Fixed)
    if args.diff_files:
        f_before, f_after = args.diff_files
        print(f"🔍 正在比對語意差分: [{f_before}] ➔ [{f_after}]...")
        
        adapter_b = get_adapter_for_file(f_before)
        adapter_a = get_adapter_for_file(f_after)

        with open(f_before, "r", encoding="utf-8") as f:
            code_b = f.read()
        with open(f_after, "r", encoding="utf-8") as f:
            code_a = f.read()

        g_b = adapter_b.parse_and_build(code_b, file_path=f_before)
        g_a = adapter_a.parse_and_build(code_a, file_path=f_after)

        diff_res = CodeMapDiffer.diff_graphs(g_b, g_a)
        print("\n" + diff_res.to_diff_markdown())

        if args.check and not diff_res.passed:
            sys.exit(1)
        return

    # 2. Git 歷史語意差分
    if args.git_diff and args.file:
        print(f"🔍 正在從 Git 抽取歷史比對: [{args.file}] (範圍: {args.git_diff})...")
        diff_res = CodeMapDiffer.diff_git_file(
            repo_path=args.repo,
            file_path=args.file,
            diff_range=args.git_diff
        )
        print("\n" + diff_res.to_diff_markdown())
        if args.check and not diff_res.passed:
            sys.exit(1)
        return

    # 3. 獲取分析圖譜 (單一檔案、多檔案聯合、或目錄遍歷)
    graph = None
    target_desc = ""

    if args.files:
        print(f"🌐 正在聯合解析 {len(args.files)} 個檔案並消解跨模組 import/export...")
        graph = WorkspaceGraphBuilder.build_from_files(args.files, root_dir=args.repo)
        target_desc = f"{len(args.files)} 個聯合模組"
    elif args.dir:
        print(f"🌐 正在遍歷目錄 [{args.dir}] 並消解跨模組 import/export...")
        graph = WorkspaceGraphBuilder.build_from_dir(args.dir)
        target_desc = f"目錄 {args.dir}"
    elif args.file:
        try:
            adapter = get_adapter_for_file(args.file)
        except ValueError as e:
            print(f"❌ 錯誤: {e}")
            sys.exit(1)

        print(f"🔍 檢測到目標語言: {adapter.language_name}，正在解析...")
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
        graph = adapter.parse_and_build(code, file_path=args.file)
        target_desc = args.file

    if graph:
        # 若指定了 --verify-spec，執行規格驗收
        if args.verify_spec:
            print(f"⚖️ 正在對 [{target_desc}] 執行上位架構規格契約驗收: [{args.verify_spec}]...")
            v_res = SpecVerifier.verify(spec=args.verify_spec, actual=graph, workspace_root=args.repo)
            print("\n" + v_res.to_markdown())
            if not v_res.passed:
                sys.exit(1)
            return

        if args.locate:
            print(graph.locate_symbol_bundle(args.locate))
            return

        if args.bundle:
            target_id = args.bundle
            if target_id not in graph.g:
                candidates = [n for n, d in graph.g.nodes(data=True) if d.get("label") == target_id or target_id in n]
                if candidates:
                    target_id = candidates[0]
            print(graph.to_causal_code_bundle(target_id))
            return

        if args.slice:
            graph = graph.forward_slice(args.slice)
            print(f"✂️ 已針對錨點 '{args.slice}' 執行前向切片。")

        print("\n" + graph.to_uia_markdown())

        inv = graph.check_invariants()
        print(f"\n驗收裁決: {inv['verdict']}")
        for err in inv["scope_errors"]:
            print(f"  ❌ {err['detail']}")
        for h in inv["hazards"]:
            print(f"  ⚠️ {h['detail']}")

        if args.export_json:
            with open(args.export_json, "w", encoding="utf-8") as f:
                f.write(graph.to_json(indent=2))
            print(f"\n📦 Node-Link JSON 已導出至: {args.export_json}")

        if args.html and args.file:
            from code_map.reporters.html_reporter import HTMLDashboardReporter
            reporter = HTMLDashboardReporter()
            out_path = reporter.generate(graph, args.html, file_path=args.file)
            print(f"\n🌲 [HTML 雙欄因果儀表板已輸出至]: {out_path}")

        if args.check and not inv["passed"]:
            sys.exit(1)
    else:
        print("CODE-Map 行為語意圖譜引擎已就緒！請使用 --file <檔案>、--files <A> <B>、--verify-spec <契約> 或 --diff-files <A> <B>。")


if __name__ == "__main__":
    main()
