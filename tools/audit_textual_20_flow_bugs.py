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

REPO_PATH = os.path.abspath(os.path.join(project_root, "test_repos", "textual"))

def get_20_textual_commits():
    cmd = ["git", "-C", REPO_PATH, "log", "--no-merges", "-n", "2500", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    matches = []
    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        lower_msg = msg.lower()
        if lower_msg.startswith("docs") or "test fix" in lower_msg or "snapshot" in lower_msg or "typo" in lower_msg or "changelog" in lower_msg or "bump" in lower_msg:
            continue
        if re.search(r"\b(fix|fixes|fixed|bug|prevent|handle|issue|glitch|crash|error)\b", msg, re.IGNORECASE):
            f_res = subprocess.run(["git", "-C", REPO_PATH, "diff-tree", "--no-commit-id", "--name-only", "-r", h], capture_output=True, text=True, encoding="utf-8", errors="replace")
            py_files = [f for f in f_res.stdout.splitlines() if f.endswith(".py") and f.startswith("src/textual/") and "test" not in f]
            if 1 <= len(py_files) <= 3:
                matches.append((h, msg, py_files))
                if len(matches) == 20:
                    break
    return matches

def main():
    commits = get_20_textual_commits()
    print("================================================================================")
    print("🌲 檢索出 20 個 Textual 真實「流程/事件/狀態/非同步/渲染」修復 Commits:")
    print("================================================================================")
    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案數: {len(files)}")

    print("\n================================================================================")
    print("🚀 開始逐一進行 CODE-Map Python 適配器語意差分審查與捕獲檢驗:")
    print("================================================================================\n")

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
                    "added_nodes": added_nodes, "removed_nodes": removed_nodes,
                    "added_edges": added_edges, "removed_edges": removed_edges,
                    "modified_funcs": modified_funcs,
                    "transitions": transitions,
                    "verdict": diff_res.verdict,
                })
            except Exception as e:
                print(f"  • [{f}] ❌ 剖析失敗: {e}")
                commit_res["files"].append({"file": f, "error": str(e)})

        report_records.append(commit_res)

    print("\n================================================================================")
    print("📊 CODE-Map Python 基準評估統計結果 (去水分雙軌指標):")
    print("================================================================================")
    total_files = sum(len(c["files"]) for c in report_records)
    structural_captured = 0
    body_level_captured = 0
    zero_delta = 0
    errors = 0

    for c in report_records:
        for f in c["files"]:
            if "error" in f:
                errors += 1
            else:
                is_structural = (
                    f["added_edges"] > 0
                    or f["removed_edges"] > 0
                    or f["added_nodes"] > 0
                    or f["removed_nodes"] > 0
                    or f["transitions"] > 0
                    or (f["anchors_a"] != f["anchors_b"])
                )
                if is_structural:
                    structural_captured += 1
                elif f["modified_funcs"] > 0:
                    body_level_captured += 1
                else:
                    zero_delta += 1

    total_captured = structural_captured + body_level_captured
    print(f"總審查 Commit 數: {len(report_records)}")
    print(f"審查檔案總數: {total_files}")
    print(f"  🔹 結構性因果圖變動 (Structural Graph Delta): {structural_captured} / {total_files} ({structural_captured/total_files*100:.1f}%)")
    print(f"  🔸 函式體純文字變動 (Body-Level Semantic Delta): {body_level_captured} / {total_files} ({body_level_captured/total_files*100:.1f}%)")
    print(f"  🏆 總體可執行邏輯變更捕獲率: {total_captured} / {total_files} ({total_captured/total_files*100:.1f}%)")
    print(f"無語意圖譜變動 (純註釋/空白或未涵蓋): {zero_delta} / {total_files} ({zero_delta/total_files*100:.1f}%)")
    print(f"解析錯誤: {errors} / {total_files}")

if __name__ == "__main__":
    main()
