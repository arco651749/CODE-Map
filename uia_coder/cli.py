import argparse
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.adapters import AdapterRegistry, get_adapter_for_file
from uia_coder.core.differ import UIAGraphDiffer


def main():
    parser = argparse.ArgumentParser(
        description="🌲 CODE-Map: Causal Operation & Dependency Evaluation Map (行為因果與接線依賴評估地圖引擎)"
    )
    parser.add_argument("--file", help="目標分析之源碼檔案路徑 (自動依副檔名匹配語言)")
    parser.add_argument("--export-json", help="導出 NetworkX Node-Link JSON 檔案路徑")
    parser.add_argument("--slice", help="針對特定 UI 錨點 (Anchor ID) 進行前向圖切片")
    parser.add_argument("--check", action="store_true", help="執行形式化不變量守衛檢驗，有違規時返回非 0 狀態碼")
    parser.add_argument("--list-languages", action="store_true", help="列出目前所有已支援的程式語言與副檔名")
    
    # 差分專用參數
    parser.add_argument("--diff-files", nargs=2, metavar=("BEFORE_FILE", "AFTER_FILE"), help="比對兩個檔案間的 UIA 語意圖譜差分 (規格 vs 實作)")
    parser.add_argument("--git-diff", nargs="?", const="HEAD~1", help="比對指定檔案在 Git 歷史中的 UIA 語意差分 (預設 HEAD~1)")
    parser.add_argument("--repo", default=".", help="Git 倉庫目錄路徑 (配合 --git-diff 使用)")

    args = parser.parse_args()

    if args.list_languages:
        print("🌲 UIA-Coder 目前支援之程式語言：")
        for item in AdapterRegistry.list_supported_languages():
            print(f"  • {item['language']:12} (副檔名: {item['extensions']})")
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

        diff_res = UIAGraphDiffer.diff_graphs(g_b, g_a)
        print("\n" + diff_res.to_diff_markdown())

        if args.check and not diff_res.passed:
            sys.exit(1)
        return

    # 2. Git 歷史語意差分
    if args.git_diff and args.file:
        print(f"🔍 正在從 Git 抽取歷史比對: [{args.file}] (範圍: {args.git_diff})...")
        diff_res = UIAGraphDiffer.diff_git_file(
            repo_path=args.repo,
            file_path=args.file,
            diff_range=args.git_diff
        )
        print("\n" + diff_res.to_diff_markdown())
        if args.check and not diff_res.passed:
            sys.exit(1)
        return

    # 3. 單一檔案分析
    if args.file:
        try:
            adapter = get_adapter_for_file(args.file)
        except ValueError as e:
            print(f"❌ 錯誤: {e}")
            sys.exit(1)

        print(f"🔍 檢測到目標語言: {adapter.language_name}，正在解析...")
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()

        graph = adapter.parse_and_build(code, file_path=args.file)

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

        if args.check and not inv["passed"]:
            sys.exit(1)
    else:
        print("UIA-Coder 行為語意圖譜引擎已就緒！請使用 --file <檔案>、--diff-files <A> <B> 或 --list-languages。")


if __name__ == "__main__":
    main()
