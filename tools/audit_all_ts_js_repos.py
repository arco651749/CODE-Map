import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from code_map.core.differ import CodeMapDiffer

REPOS_CONFIG: Dict[str, Dict[str, Any]] = {
    "todomvc": {
        "dir": "todomvc",
        "exts": (".js", ".ts"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "bower_components", "dist/"],
        "lang": "JavaScript (Vanilla/MVC Showcases)",
    },
    "Sortable": {
        "dir": "Sortable",
        "exts": (".js", ".mjs"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "st/"],
        "lang": "JavaScript (Drag & Drop Reorder Engine)",
    },
    "alpine": {
        "dir": "alpine",
        "exts": (".js",),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "JavaScript (Lightweight Reactive UI)",
    },
    "preact": {
        "dir": "preact",
        "exts": (".js", ".mjs", ".ts"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "demo"],
        "lang": "JavaScript/TypeScript (Fast 3kB React Alternative)",
    },
    "xstate": {
        "dir": "xstate",
        "exts": (".ts", ".tsx", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "TypeScript (Actor Model & State Machines)",
    },
    "ink": {
        "dir": "ink",
        "exts": (".ts", ".tsx", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "TypeScript (React for Interactive CLIs)",
    },
    "vue": {
        "dir": "vue",
        "exts": (".ts", ".tsx", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples", "dts-test", "vitest"],
        "lang": "TypeScript (Progressive Frontend Framework)",
    },
    "nest": {
        "dir": "nest",
        "exts": (".ts", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "TypeScript (Enterprise Node.js Server Framework)",
    },
    "zustand": {
        "dir": "zustand",
        "exts": (".ts", ".tsx", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "TypeScript (Bearbones State Management)",
    },
    "trpc": {
        "dir": "trpc",
        "exts": (".ts", ".tsx", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "TypeScript (End-to-End Typesafe APIs)",
    },
    "vite": {
        "dir": "vite",
        "exts": (".ts", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples", "playground"],
        "lang": "TypeScript (Next Generation Frontend Tooling)",
    },
    "next.js": {
        "dir": "next.js",
        "exts": (".ts", ".tsx", ".js"),
        "exclude": ["test", "tests", "__tests__", "spec", "e2e", "doc", "docs", "bench", ".d.ts", ".min.js", "node_modules", "dist/", "examples"],
        "lang": "TypeScript/JavaScript (The React Framework)",
    },
}

FIX_PATTERN = re.compile(
    r"(\bfix\b|\bfixes\b|\bfixed\b|\bbug\b|\bprevent\b|\bhandle\b|\bissue\b|\bcrash\b|\berror\b|\bpatch\b|\bresolve\b|🐛|\bavoid\b|\bworkaround\b|\bleak\b|\bcorrect\b|\bclose\b)",
    re.IGNORECASE,
)
IGNORE_PREFIXES = ("release", "bump", "docs", "doc:", "documentation", "🔖")


def get_commits_for_repo(repo_name: str, config: Dict[str, Any], limit: int = 20) -> List[Tuple[str, str, List[str]]]:
    repo_path = os.path.abspath(os.path.join(project_root, "test_repos", config["dir"]))
    cmd = ["git", "-C", repo_path, "log", "--no-merges", "-n", "3000", "--format=COMMIT:%H%x09%s", "--name-only"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    commits: List[Tuple[str, str, List[str]]] = []
    current_commit = None
    current_files: List[str] = []
    for line in res.stdout.splitlines():
        line = line.strip()
        if line.startswith("COMMIT:"):
            if current_commit:
                commits.append((current_commit[0], current_commit[1], current_files))
            h, msg = line[7:].split("\t", 1)
            current_commit = (h, msg)
            current_files = []
        elif line:
            current_files.append(line)
    if current_commit:
        commits.append((current_commit[0], current_commit[1], current_files))

    matches = []
    for h, msg, files in commits:
        lower_msg = msg.lower().strip()
        if any(lower_msg.startswith(pfx) for pfx in IGNORE_PREFIXES):
            continue
        if any(kw in lower_msg for kw in ["typo", "changelog", "release version", "bump version", "readme", "license"]):
            continue
        if not FIX_PATTERN.search(msg):
            continue

        valid_files = []
        for f in files:
            if not f.endswith(config["exts"]):
                continue
            f_lower = f.lower()
            if any(ex in f_lower for ex in config["exclude"]):
                continue
            valid_files.append(f)

        if 1 <= len(valid_files) <= 3:
            matches.append((h, msg, valid_files))
            if len(matches) == limit:
                break
    return matches


def run_benchmark(output_json: str = None, repo_filter: str = None) -> Dict[str, Any]:
    all_results = {}

    target_repos = (
        {repo_filter: REPOS_CONFIG[repo_filter]}
        if repo_filter and repo_filter in REPOS_CONFIG
        else REPOS_CONFIG
    )

    for repo_name, cfg in target_repos.items():
        repo_path = os.path.abspath(os.path.join(project_root, "test_repos", cfg["dir"]))
        commits = get_commits_for_repo(repo_name, cfg, limit=20)
        print("=" * 80)
        print(f"📦 專案: {repo_name} [{cfg['lang']}] (篩選出 {len(commits)} 個真實修復 Commits)")
        print("=" * 80)

        repo_records = []
        for idx, (h, msg, files) in enumerate(commits, 1):
            commit_record = {"commit": h, "msg": msg, "files": []}
            print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案數: {len(files)}")
            for f in files:
                full_path = os.path.join(repo_path, f)
                try:
                    diff_res = CodeMapDiffer.diff_git_file(
                        repo_path=repo_path,
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

                    is_structural = (
                        added_edges > 0
                        or removed_edges > 0
                        or added_nodes > 0
                        or removed_nodes > 0
                        or transitions > 0
                        or (anchors_a != anchors_b)
                    )
                    is_body = (not is_structural) and (modified_funcs > 0)
                    is_zero = (not is_structural) and (not is_body)

                    category = (
                        "STRUCTURAL_GRAPH_DELTA"
                        if is_structural
                        else ("BODY_LEVEL_SEMANTIC_DELTA" if is_body else "ZERO_DELTA")
                    )

                    commit_record["files"].append({
                        "file": f,
                        "category": category,
                        "nodes_b": nodes_b,
                        "edges_b": edges_b,
                        "anchors_b": anchors_b,
                        "nodes_a": nodes_a,
                        "edges_a": edges_a,
                        "anchors_a": anchors_a,
                        "added_nodes": added_nodes,
                        "removed_nodes": removed_nodes,
                        "added_edges": added_edges,
                        "removed_edges": removed_edges,
                        "modified_funcs": modified_funcs,
                        "transitions": transitions,
                        "verdict": diff_res.verdict,
                    })
                except Exception as e:
                    print(f"    ❌ [{f}] 剖析失敗: {e}")
                    commit_record["files"].append({
                        "file": f,
                        "category": "CRASH_OR_ERROR",
                        "error": str(e),
                    })
            repo_records.append(commit_record)
        all_results[repo_name] = repo_records

    # 產出統計彙整
    print("\n" + "=" * 105)
    print("📊 12 大開源 TS/JS 專案 240-Commit 基準審查統計匯總")
    print("=" * 105)
    header = f"{'專案名稱':<12} | {'Commit':<6} | {'檔案數':<6} | {'結構拓撲 (STRUCT)':<20} | {'函式體 (BODY)':<18} | {'零變動 (ZERO)':<16} | {'錯誤':<6} | {'捕獲率':<8}"
    print(header)
    print("-" * len(header))

    grand_total_files = 0
    grand_structural = 0
    grand_body = 0
    grand_zero = 0
    grand_errors = 0

    summary_data = {}

    for repo_name, records in all_results.items():
        total_files = sum(len(c["files"]) for c in records)
        structural = sum(1 for c in records for f in c["files"] if f.get("category") == "STRUCTURAL_GRAPH_DELTA")
        body = sum(1 for c in records for f in c["files"] if f.get("category") == "BODY_LEVEL_SEMANTIC_DELTA")
        zero = sum(1 for c in records for f in c["files"] if f.get("category") == "ZERO_DELTA")
        errors = sum(1 for c in records for f in c["files"] if f.get("category") == "CRASH_OR_ERROR")

        grand_total_files += total_files
        grand_structural += structural
        grand_body += body
        grand_zero += zero
        grand_errors += errors

        rate = ((structural + body) / total_files * 100) if total_files > 0 else 0.0
        struct_pct = f"{structural} ({structural/total_files*100:5.1f}%)" if total_files else "0"
        body_pct = f"{body} ({body/total_files*100:5.1f}%)" if total_files else "0"
        zero_pct = f"{zero} ({zero/total_files*100:5.1f}%)" if total_files else "0"
        print(
            f"{repo_name:<12} | {len(records):<6} | {total_files:<6} | {struct_pct:<20} | {body_pct:<18} | {zero_pct:<16} | {errors:<6} | {rate:5.1f}%"
        )
        summary_data[repo_name] = {
            "commits": len(records),
            "files": total_files,
            "structural": structural,
            "body": body,
            "zero": zero,
            "errors": errors,
            "capture_rate": round(rate, 2),
        }

    print("-" * len(header))
    grand_rate = ((grand_structural + grand_body) / grand_total_files * 100) if grand_total_files > 0 else 0.0
    tot_struct = f"{grand_structural} ({grand_structural/grand_total_files*100:5.1f}%)" if grand_total_files else "0"
    tot_body = f"{grand_body} ({grand_body/grand_total_files*100:5.1f}%)" if grand_total_files else "0"
    tot_zero = f"{grand_zero} ({grand_zero/grand_total_files*100:5.1f}%)" if grand_total_files else "0"
    print(
        f"{'總計 (ALL)':<12} | {len(target_repos)*20:<6} | {grand_total_files:<6} | {tot_struct:<20} | {tot_body:<18} | {tot_zero:<16} | {grand_errors:<6} | {grand_rate:5.1f}%"
    )
    summary_data["TOTAL"] = {
        "commits": len(target_repos) * 20,
        "files": grand_total_files,
        "structural": grand_structural,
        "body": grand_body,
        "zero": grand_zero,
        "errors": grand_errors,
        "capture_rate": round(grand_rate, 2),
    }

    output_payload = {
        "summary": summary_data,
        "details": all_results,
    }

    if output_json:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 完整數據已保存至: {output_json}")

    return output_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit 12 TS/JS Repos (20 Commits each)")
    parser.add_argument("--output", type=str, default="audit_all_ts_js_repos_baseline.json", help="Output JSON path")
    parser.add_argument("--repo", type=str, default=None, help="Filter by single repository name")
    args = parser.parse_args()

    run_benchmark(output_json=args.output, repo_filter=args.repo)
