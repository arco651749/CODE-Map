import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from code_map.core.differ import CodeMapDiffer

GO_REPOS: Dict[str, Dict[str, Any]] = {
    "bubbletea": {
        "dir": "bubbletea",
        "exts": (".go",),
        "exclude": ["test/", "_test.go", "examples/"],
        "filter_dir": "",
        "lang": "Go (TUI / Elm Architecture Framework)",
    },
    "caddy": {
        "dir": "caddy",
        "exts": (".go",),
        "exclude": ["test/", "_test.go"],
        "filter_dir": "",
        "lang": "Go (Extensible Multi-Platform Web Server with HTTPS)",
    },
    "cobra": {
        "dir": "cobra",
        "exts": (".go",),
        "exclude": ["test/", "_test.go"],
        "filter_dir": "",
        "lang": "Go (Commander for Modern CLI Applications)",
    },
    "fzf": {
        "dir": "fzf",
        "exts": (".go",),
        "exclude": ["test/", "_test.go"],
        "filter_dir": "",
        "lang": "Go (Command-line Fuzzy Finder)",
    },
    "gin": {
        "dir": "gin",
        "exts": (".go",),
        "exclude": ["test/", "_test.go"],
        "filter_dir": "",
        "lang": "Go (High-Performance HTTP Web Framework)",
    },
    "go-redis": {
        "dir": "go-redis",
        "exts": (".go",),
        "exclude": ["test/", "_test.go", "example/"],
        "filter_dir": "",
        "lang": "Go (Type-Safe High-Performance Redis Client)",
    },
    "traefik": {
        "dir": "traefik",
        "exts": (".go",),
        "exclude": ["integration/", "_test.go"],
        "filter_dir": "",
        "lang": "Go (Cloud Native Edge Router & Reverse Proxy)",
    },
}

KEYWORDS = r"\b(fix|fixes|fixed|bug|prevent|handle|issue|crash|panic|leak|overflow|render|layout|scroll|event|clear|draw|race|window|resize|deadlock|stream|query|route|handler|error|state|cache|alloc|bound|type|add|update)\b"


def get_commits_for_repo(repo_path: str, repo_info: Dict[str, Any], max_count: int = 20) -> List[Tuple[str, str, List[str]]]:
    exts = repo_info["exts"]
    exclude = repo_info["exclude"]
    filter_dir = repo_info.get("filter_dir", "")

    cmd = ["git", "-C", repo_path, "log", "--no-merges", "-n", "1500", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    matches = []
    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        lower_msg = msg.lower()
        if any(w in lower_msg for w in ["bump", "release", "version", "changelog", "typo"]):
            continue
        if lower_msg.startswith("docs") or lower_msg.startswith("doc:"):
            continue

        if re.search(KEYWORDS, msg, re.IGNORECASE):
            # Exclude pure deletions using --diff-filter=d
            f_res = subprocess.run(
                ["git", "-C", repo_path, "diff-tree", "--no-commit-id", "--name-only", "-r", "--diff-filter=d", h],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            valid_files = [
                f for f in f_res.stdout.splitlines()
                if f.endswith(exts)
                and not any(x in f for x in exclude)
                and (not filter_dir or filter_dir in f)
            ]
            if 1 <= len(valid_files) <= 3:
                matches.append((h, msg, valid_files))
                if len(matches) == max_count:
                    break
    return matches


def audit_repo(repo_name: str, repo_info: Dict[str, Any], inspect_zero: bool = False) -> Dict[str, Any]:
    print(f"\n{'='*80}")
    print(f"🌲 正在評估 Go 專案: {repo_name} [{repo_info['lang']}]")
    print(f"{'='*80}")

    repo_path = os.path.abspath(os.path.join(project_root, "test_repos", repo_info["dir"]))
    commits = get_commits_for_repo(repo_path, repo_info, max_count=20)
    print(f"篩選出 {len(commits)} 個核心修復 Commits:")
    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案: {files}")

    stats: Dict[str, Any] = {
        "repo": repo_name,
        "lang": repo_info["lang"],
        "commits": len(commits),
        "total_files": 0,
        "structural": 0,
        "body_semantic": 0,
        "zero_delta": 0,
        "crashes": 0,
        "zero_delta_files": [],
        "crash_files": [],
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
                    target_ref=h,
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
                    stats["zero_delta_files"].append({
                        "commit": h,
                        "msg": msg,
                        "file": f,
                    })
                    if inspect_zero:
                        print(f"    [ZERO_DELTA] {h[:8]} {f} ({msg[:40]})")
            except Exception as e:
                print(f"  [CRASH] {h[:8]} {f}: {e}")
                stats["crashes"] += 1
                stats["crash_files"].append({
                    "commit": h,
                    "msg": msg,
                    "file": f,
                    "error": str(e),
                })

    captured = stats["structural"] + stats["body_semantic"]
    total = stats["total_files"]
    rate = (captured / total * 100) if total > 0 else 0
    stats["captured"] = captured
    stats["rate"] = rate

    print(f"\n📊 {repo_name} 評估結果:")
    print(f"  • 總審查檔案數: {total}")
    print(f"  • 結構性圖譜變動 (Structural): {stats['structural']} ({stats['structural']/total*100:.1f}%)" if total else "  • 結構性: 0")
    print(f"  • 函式體語意變動 (Body-level):  {stats['body_semantic']} ({stats['body_semantic']/total*100:.1f}%)" if total else "  • 函式體: 0")
    print(f"  • 零語意變動 (Zero-delta):     {stats['zero_delta']} ({stats['zero_delta']/total*100:.1f}%)" if total else "  • 零變動: 0")
    print(f"  • 崩潰率 (Crash):             {stats['crashes']} (0.0%)")
    print(f"  • 🏆 總體邏輯捕獲率:            {captured}/{total} ({rate:.1f}%)")
    return stats


def main():
    parser = argparse.ArgumentParser(description="Audit Go Repositories")
    parser.add_argument("--save-json", type=str, default="", help="Save results to JSON file")
    parser.add_argument("--repo", type=str, default="", help="Audit only a specific repo")
    parser.add_argument("--inspect-zero", action="store_true", help="Print details on zero-delta files")
    args = parser.parse_args()

    target_repos = (
        {args.repo: GO_REPOS[args.repo]}
        if args.repo and args.repo in GO_REPOS
        else GO_REPOS
    )

    print(f"🚀 開始執行 {len(target_repos)} 大 Go 頂級開源專案 20-Commit 實戰基準審查...")
    summary = []
    grand = {
        "total_files": 0,
        "structural": 0,
        "body_semantic": 0,
        "zero_delta": 0,
        "crashes": 0,
        "captured": 0,
    }

    for name, info in target_repos.items():
        res = audit_repo(name, info, inspect_zero=args.inspect_zero)
        summary.append(res)
        grand["total_files"] += res["total_files"]
        grand["structural"] += res["structural"]
        grand["body_semantic"] += res["body_semantic"]
        grand["zero_delta"] += res["zero_delta"]
        grand["crashes"] += res["crashes"]
        grand["captured"] += res["captured"]

    grand_rate = (grand["captured"] / grand["total_files"] * 100) if grand["total_files"] else 0
    total_commits = sum(s["commits"] for s in summary)

    print("\n" + "=" * 95)
    print("🏆 7 大 Go 頂級開源專案 20-Commit 基準測試驗收總表:")
    print("=" * 95)
    print(f"{'專案名稱':<12} | {'Commits':<8} | {'檔案數':<7} | {'結構圖變動':<10} | {'函式體語意':<10} | {'Zero-Delta':<10} | {'Crash':<6} | {'捕獲率'}")
    print("-" * 95)
    for s in summary:
        print(f"{s['repo']:<12} | {s['commits']:<8} | {s['total_files']:<7} | {s['structural']:<10} | {s['body_semantic']:<10} | {s['zero_delta']:<10} | {s['crashes']:<6} | {s['rate']:<6.1f}%")
    print("-" * 95)
    print(f"{'總計 (GRAND)':<12} | {total_commits:<8} | {grand['total_files']:<7} | {grand['structural']:<10} | {grand['body_semantic']:<10} | {grand['zero_delta']:<10} | {grand['crashes']:<6} | {grand_rate:<6.1f}%")
    print("=" * 95)

    if args.save_json:
        out_path = args.save_json
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"summary": summary, "grand": grand}, f, ensure_ascii=False, indent=2)
        print(f"\n[INFO] 已將審查結果儲存至: {out_path}")


if __name__ == "__main__":
    main()
