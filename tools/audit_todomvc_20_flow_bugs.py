import os
import subprocess
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from uia_coder.core.differ import UIAGraphDiffer

REPO_PATH = os.path.abspath(os.path.join(project_root, "test_repos", "todomvc"))

def get_20_flow_commits():
    # 執行 git log
    cmd = ["git", "-C", REPO_PATH, "log", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    
    flow_keywords = [
        "event", "listener", "click", "keypress", "keyup", "keydown",
        "escape", "enter", "blur", "focus", "bind", "delegate",
        "callback", "async", "cancel", "stale", "double", "race", "count",
        "routing", "render", "sync", "refresh"
    ]
    pattern = re.compile(r"\b(" + "|".join(flow_keywords) + r")\b", re.IGNORECASE)
    fix_pattern = re.compile(r"\b(fix|bug|close|correct|resolve|patch|prevent)\b", re.IGNORECASE)

    commits = []
    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        if fix_pattern.search(msg) and pattern.search(msg):
            # 獲取修改的 js 檔案
            files_cmd = ["git", "-C", REPO_PATH, "diff-tree", "--no-commit-id", "--name-only", "-r", h]
            f_res = subprocess.run(files_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            js_files = [
                f for f in f_res.stdout.splitlines() 
                if f.endswith(".js") and not f.endswith(".min.js") 
                and "bower_components" not in f and "node_modules" not in f
                and "test" not in f.lower() and "karma" not in f.lower()
            ]
            if 1 <= len(js_files) <= 5: # 聚焦在核心邏輯變更的 Commit (排除大量升級的 mega commit)
                commits.append((h, msg, js_files))
                if len(commits) == 20:
                    break
    return commits

def main():
    commits = get_20_flow_commits()
    print(f"================================================================================")
    print(f"🌲 檢索出 20 個 TodoMVC 真實「流程/事件/回呼/生命週期」錯誤修復 Commits:")
    print(f"================================================================================")
    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"[{idx:02d}] {h[:8]} | {msg[:60]:<60} | 檔案數: {len(files)}")

    print(f"\n================================================================================")
    print(f"🚀 開始逐一進行 CODE-Map 語意差分審查與流程捕獲檢驗:")
    print(f"================================================================================\n")

    report_records = []

    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"--- Commit #{idx:02d}: {h[:8]} - {msg} ---")
        commit_res = {"commit": h, "msg": msg, "files": []}
        for f in files:
            full_path = os.path.join(REPO_PATH, f)
            try:
                diff_res = UIAGraphDiffer.diff_git_file(
                    repo_path=REPO_PATH,
                    file_path=full_path,
                    diff_range=f"{h}~1",
                    target_ref=h,
                )
                nodes_b = len(diff_res.g_before.g.nodes)
                edges_b = len(diff_res.g_before.g.edges)
                nodes_a = len(diff_res.g_after.g.nodes)
                edges_a = len(diff_res.g_after.g.edges)
                anchors_b = len(diff_res.g_before.get_ui_anchors())
                anchors_a = len(diff_res.g_after.get_ui_anchors())

                added_nodes = len(diff_res.nodes_added)
                removed_nodes = len(diff_res.nodes_removed)
                added_edges = len(diff_res.edges_added)
                removed_edges = len(diff_res.edges_removed)
                modified_funcs = len(diff_res.functions_modified)
                transitions = len(diff_res.status_transitions)
                
                print(f"  • [{f}]")
                print(f"    Graph: Before(N:{nodes_b}, E:{edges_b}, A:{anchors_b}) -> After(N:{nodes_a}, E:{edges_a}, A:{anchors_a})")
                print(f"    Diff:  +Nodes:{added_nodes}, -Nodes:{removed_nodes}, +Edges:{added_edges}, -Edges:{removed_edges}, ΔFuncs:{modified_funcs}, ΔTrans:{transitions}")
                print(f"    Verdict: {diff_res.verdict} (Passed: {diff_res.passed})")
                
                commit_res["files"].append({
                    "file": f,
                    "nodes_b": nodes_b, "edges_b": edges_b, "anchors_b": anchors_b,
                    "nodes_a": nodes_a, "edges_a": edges_a, "anchors_a": anchors_a,
                    "added_edges": added_edges, "removed_edges": removed_edges,
                    "modified_funcs": modified_funcs,
                    "transitions": transitions,
                    "verdict": diff_res.verdict,
                    "markdown": diff_res.to_diff_markdown(),
                })
            except Exception as e:
                print(f"  • [{f}] ❌ 剖析失敗: {e}")
                commit_res["files"].append({"file": f, "error": str(e)})

        report_records.append(commit_res)

    # 輸出摘要統計
    print("\n================================================================================")
    print("📊 CODE-Map 基準評估統計結果:")
    print("================================================================================")
    total_files = sum(len(c["files"]) for c in report_records)
    flow_captured = 0
    zero_delta = 0
    errors = 0

    for c in report_records:
        for f in c["files"]:
            if "error" in f:
                errors += 1
            elif f["added_edges"] > 0 or f["removed_edges"] > 0 or f["modified_funcs"] > 0 or f["transitions"] > 0 or (f["anchors_a"] != f["anchors_b"]):
                flow_captured += 1
            else:
                zero_delta += 1

    print(f"總審查 Commit 數: {len(report_records)}")
    print(f"審查檔案總數: {total_files}")
    print(f"成功捕獲流程/接線/函式語意變動: {flow_captured} / {total_files} ({flow_captured/total_files*100:.1f}%)")
    print(f"無語意圖譜變動 (盲區): {zero_delta} / {total_files} ({zero_delta/total_files*100:.1f}%)")
    print(f"解析錯誤: {errors} / {total_files}")

if __name__ == "__main__":
    main()
