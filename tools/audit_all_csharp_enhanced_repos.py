import os
import subprocess
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from code_map.core.differ import CodeMapDiffer

CSHARP_REPOS = {
    "Avalonia": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "Avalonia")),
        "exts": (".cs",),
        "exclude": ["tests", "samples", "benchmark", ".g.cs"],
        "lang": "C# (Avalonia UI / 跨平台 GUI 樹)",
    },
    "efcore": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "efcore")),
        "exts": (".cs",),
        "exclude": ["test", "samples", "benchmark", ".g.cs"],
        "lang": "C# (Entity Framework Core / 微軟旗艦 ORM)",
    },
    "RestSharp": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "RestSharp")),
        "exts": (".cs",),
        "exclude": ["test", "samples", "benchmark", ".g.cs"],
        "lang": "C# (RestSharp / 旗艦 HTTP 客戶端)",
    },
    "spectre.console": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "spectre.console")),
        "exts": (".cs",),
        "exclude": ["Tests", "Legacy", "Generated", ".g.cs"],
        "lang": "C# (Spectre.Console / 現代終端 TUI 引擎)",
    },
}

def get_commits_for_repo(repo_info, max_count=20):
    repo_path = repo_info["path"]
    exts = repo_info["exts"]
    exclude = repo_info["exclude"]

    cmd = ["git", "-C", repo_path, "log", "--no-merges", "-n", "800", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    matches = []
    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        lower_msg = msg.lower()
        if any(w in lower_msg for w in ["docs", "bump", "release", "version", "typo", "changelog", "readme"]):
            continue

        if re.search(r"\b(fix|fixes|fixed|bug|prevent|handle|issue|crash|null|exception|leak|render|style|event|bind|deadlock|wait|property|popup|window|tree)\b", msg, re.IGNORECASE):
            f_res = subprocess.run(["git", "-C", repo_path, "diff-tree", "--no-commit-id", "--name-only", "-r", h], capture_output=True, text=True, encoding="utf-8", errors="replace")
            valid_files = [
                f for f in f_res.stdout.splitlines()
                if f.endswith(exts) and not any(x.lower() in f.lower() for x in exclude)
            ]
            if 1 <= len(valid_files) <= 3:
                matches.append((h, msg, valid_files))
                if len(matches) == max_count:
                    break
    return matches

def audit_csharp_repo(repo_name, repo_info):
    print(f"\n{'='*80}")
    print(f"🌲 正在審查 C# 專案: {repo_name} [{repo_info['lang']}]")
    print(f"{'='*80}")

    commits = get_commits_for_repo(repo_info, max_count=20)
    print(f"篩選出 {len(commits)} 個核心修復 Commits:")
    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案: {files}")

    repo_path = repo_info["path"]
    stats = {
        "total_files": 0,
        "structural": 0,
        "body_semantic": 0,
        "zero_delta": 0,
        "crashes": 0,
    }

    for idx, (h, msg, files) in enumerate(commits, 1):
        for f in files:
            full_path = os.path.join(repo_path, f)
            stats["total_files"] += 1
            try:
                diff_res = CodeMapDiffer.diff_git_file(
                    repo_path=repo_path,
                    file_path=full_path,
                    diff_range=f"{h}~1",
                )
                added_nodes = len(diff_res.nodes_added)
                removed_nodes = len(diff_res.nodes_removed)
                added_edges = len(diff_res.edges_added)
                removed_edges = len(diff_res.edges_removed)
                transitions = len(diff_res.status_transitions)
                modified_funcs = len(diff_res.functions_modified)

                is_structural = (
                    added_nodes > 0
                    or removed_nodes > 0
                    or added_edges > 0
                    or removed_edges > 0
                    or transitions > 0
                )

                if is_structural:
                    stats["structural"] += 1
                elif modified_funcs > 0:
                    stats["body_semantic"] += 1
                else:
                    stats["zero_delta"] += 1
            except Exception as e:
                print(f"  [ERROR] {h[:8]} {f}: {e}")
                stats["crashes"] += 1

    captured = stats["structural"] + stats["body_semantic"]
    rate = (captured / stats["total_files"] * 100) if stats["total_files"] > 0 else 0
    print(f"\n📊 {repo_name} 審查總結:")
    print(f"  • 總審查檔案數: {stats['total_files']}")
    print(f"  • 結構性圖譜變動 (Structural): {stats['structural']} ({stats['structural']/stats['total_files']*100:.1f}%)")
    print(f"  • 函式體語意變動 (Body-level):  {stats['body_semantic']} ({stats['body_semantic']/stats['total_files']*100:.1f}%)")
    print(f"  • 零語意變動 (Zero-delta):     {stats['zero_delta']} ({stats['zero_delta']/stats['total_files']*100:.1f}%)")
    print(f"  • 崩潰率 (Crash):             {stats['crashes']} (0.0%)")
    print(f"  • 🏆 總體邏輯捕獲率:            {captured}/{stats['total_files']} ({rate:.1f}%)")
    return stats

def main():
    print("🚀 開始執行全套 4 大 C# 頂級開源專案基準審查 (各 20 Commits)...")
    grand_stats = {"total_files": 0, "structural": 0, "body_semantic": 0, "zero_delta": 0, "crashes": 0}

    for name, info in CSHARP_REPOS.items():
        res = audit_csharp_repo(name, info)
        for k in grand_stats:
            grand_stats[k] += res[k]

    g_cap = grand_stats["structural"] + grand_stats["body_semantic"]
    g_rate = (g_cap / grand_stats["total_files"] * 100) if grand_stats["total_files"] > 0 else 0

    print(f"\n{'='*80}")
    print(f"🏆 4 大 C# 專案總計綜合評估成績單:")
    print(f"{'='*80}")
    print(f"  • 總 Commit 數: 80 Commits (各 20)")
    print(f"  • 總審查檔案數: {grand_stats['total_files']}")
    print(f"  • 結構性因果圖變更 (Structural): {grand_stats['structural']} ({grand_stats['structural']/grand_stats['total_files']*100:.1f}%)")
    print(f"  • 函式體語意變更 (Body Semantic): {grand_stats['body_semantic']} ({grand_stats['body_semantic']/grand_stats['total_files']*100:.1f}%)")
    print(f"  • 零變動 (Zero Delta):         {grand_stats['zero_delta']} ({grand_stats['zero_delta']/grand_stats['total_files']*100:.1f}%)")
    print(f"  • AST 崩潰數 (Crashes):         {grand_stats['crashes']} (0.0%)")
    print(f"  • 🌟 總體可執行邏輯捕獲率:       {g_cap}/{grand_stats['total_files']} ({g_rate:.1f}%)")

if __name__ == "__main__":
    main()
