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

REPOS = {
    "ratatui": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "ratatui")),
        "exts": (".rs",),
        "filter_dir": "src/",
        "lang": "Rust (Terminal UI Framework)",
    },
    "bubbletea": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "bubbletea")),
        "exts": (".go",),
        "filter_dir": "",
        "lang": "Go (TUI / Elm Architecture)",
    },
}

def get_commits_for_repo(repo_info, max_count=20):
    repo_path = repo_info["path"]
    exts = repo_info["exts"]
    filter_dir = repo_info["filter_dir"]

    cmd = ["git", "-C", repo_path, "log", "--no-merges", "-n", "800", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    matches = []
    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        lower_msg = msg.lower()
        if lower_msg.startswith("docs") or "changelog" in lower_msg or "bump" in lower_msg or "release" in lower_msg or "version" in lower_msg or "typo" in lower_msg:
            continue

        if re.search(r"\b(fix|fixes|fixed|bug|prevent|handle|issue|crash|panic|leak|overflow|render|layout|scroll|event|clear|draw|race|window|resize|deadlock)\b", msg, re.IGNORECASE):
            f_res = subprocess.run(["git", "-C", repo_path, "diff-tree", "--no-commit-id", "--name-only", "-r", h], capture_output=True, text=True, encoding="utf-8", errors="replace")
            valid_files = [
                f for f in f_res.stdout.splitlines()
                if f.endswith(exts) and not f.endswith("_test.go")
                and "tests" not in f and "benches" not in f and "examples" not in f and filter_dir in f
            ]
            if 1 <= len(valid_files) <= 3:
                matches.append((h, msg, valid_files))
                if len(matches) == max_count:
                    break
    return matches

def audit_repo(repo_name, repo_info):
    print(f"\n{'='*80}")
    print(f"🌲 正在評估專案: {repo_name} [{repo_info['lang']}]")
    print(f"{'='*80}")

    commits = get_commits_for_repo(repo_info, max_count=20)
    print(f"篩選出 {len(commits)} 個核心修復 Commits:")
    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案: {files}")

    report_records = []
    repo_path = repo_info["path"]

    for idx, (h, msg, files) in enumerate(commits, 1):
        commit_res = {"commit": h, "msg": msg, "files": []}
        for f in files:
            full_path = os.path.join(repo_path, f)
            try:
                diff_res = UIAGraphDiffer.diff_git_file(
                    repo_path=repo_path,
                    file_path=full_path,
                    diff_range=f"{h}~1",
                    target_ref=h,
                )
                nodes_b = len(diff_res.g_before.g.nodes)
                nodes_a = len(diff_res.g_after.g.nodes)
                added_nodes = len(diff_res.nodes_added)
                removed_nodes = len(diff_res.nodes_removed)
                added_edges = len(diff_res.edges_added)
                removed_edges = len(diff_res.edges_removed)
                modified_funcs = len(diff_res.functions_modified)
                transitions = len(diff_res.status_transitions)
                anchors_b = len(diff_res.g_before.get_ui_anchors())
                anchors_a = len(diff_res.g_after.get_ui_anchors())

                is_captured = (added_edges > 0 or removed_edges > 0 or added_nodes > 0 or removed_nodes > 0 or modified_funcs > 0 or transitions > 0 or (anchors_a != anchors_b))

                commit_res["files"].append({
                    "file": f,
                    "captured": is_captured,
                    "nodes_b": nodes_b, "nodes_a": nodes_a,
                    "added_nodes": added_nodes, "removed_nodes": removed_nodes,
                    "added_edges": added_edges, "removed_edges": removed_edges,
                    "modified_funcs": modified_funcs,
                    "verdict": diff_res.verdict,
                })
            except Exception as e:
                commit_res["files"].append({"file": f, "error": str(e), "captured": False})

        report_records.append(commit_res)

    total_files = sum(len(c["files"]) for c in report_records)
    flow_captured = sum(1 for c in report_records for f in c["files"] if f.get("captured"))
    zero_delta = sum(1 for c in report_records for f in c["files"] if not f.get("captured") and "error" not in f)
    errors = sum(1 for c in report_records for f in c["files"] if "error" in f)

    rate = (flow_captured / total_files * 100) if total_files else 0
    print(f"\n--- {repo_name} 評估結果 ---")
    print(f"審查檔案總數: {total_files}")
    print(f"成功捕獲流程/語意變動: {flow_captured} / {total_files} ({rate:.1f}%)")
    print(f"無變動 (零差異/型別等): {zero_delta} / {total_files}")
    print(f"解析錯誤: {errors} / {total_files}")

    return {
        "repo": repo_name,
        "lang": repo_info["lang"],
        "commits": len(report_records),
        "total_files": total_files,
        "captured": flow_captured,
        "zero_delta": zero_delta,
        "errors": errors,
        "rate": rate,
        "records": report_records,
    }

def main():
    summary = []
    for r_name, r_info in REPOS.items():
        res = audit_repo(r_name, r_info)
        summary.append(res)

    print("\n" + "="*80)
    print("🏆 Rust & Go 系統級/併發 TUI 驗收總表:")
    print("="*80)
    print(f"{'專案名稱':<12} | {'語言/生態':<28} | {'Commits':<8} | {'檔案數':<8} | {'捕獲數':<8} | {'命中率':<8} | {'錯誤數'}")
    print("-" * 80)
    for s in summary:
        print(f"{s['repo']:<12} | {s['lang']:<28} | {s['commits']:<8} | {s['total_files']:<8} | {s['captured']:<8} | {s['rate']:<6.1f}% | {s['errors']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
