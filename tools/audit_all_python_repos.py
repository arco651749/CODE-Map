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

REPOS_CONFIG = {
    "textual": {
        "dir": "textual",
        "prefix": "src/textual/",
    },
    "fastapi": {
        "dir": "fastapi",
        "prefix": "fastapi/",
    },
    "httpx": {
        "dir": "httpx",
        "prefix": "httpx/",
    },
    "pydantic": {
        "dir": "pydantic",
        "prefix": "pydantic/",
    },
    "vllm": {
        "dir": "vllm",
        "prefix": "vllm/",
    },
}


def get_commits_for_repo(repo_name: str, config: Dict[str, str], limit: int = 20) -> List[Tuple[str, str, List[str]]]:
    repo_path = os.path.abspath(os.path.join(project_root, "test_repos", config["dir"]))
    cmd = ["git", "-C", repo_path, "log", "--no-merges", "-n", "2000", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    matches = []
    ignore_prefixes = ("release", "bump", "docs", "doc:", "documentation", "🔖")
    fix_pattern = re.compile(
        r"(\bfix\b|\bfixes\b|\bfixed\b|\bbug\b|\bprevent\b|\bhandle\b|\bissue\b|\bcrash\b|\berror\b|\bpatch\b|\bresolve\b|🐛|\btreat\b|\bavoid\b|\bworkaround\b)",
        re.IGNORECASE,
    )

    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        lower_msg = msg.lower().strip()
        if any(lower_msg.startswith(p) for p in ignore_prefixes):
            continue
        if any(kw in lower_msg for kw in ["typo", "changelog", "release version", "bump version", "readme"]):
            continue
        if fix_pattern.search(msg):
            f_res = subprocess.run(
                ["git", "-C", repo_path, "diff-tree", "--no-commit-id", "--name-only", "-r", h],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            raw_files = [f.strip() for f in f_res.stdout.splitlines() if f.strip()]

            py_files = []
            for f in raw_files:
                f_lower = f.lower()
                if not f.endswith(".py"):
                    continue
                if any(p in f_lower for p in ["test", "tests/", "doc/", "docs/", "example", "examples/", "benchmark", "benchmarks/", "scripts/"]):
                    continue
                if not f.startswith(config["prefix"]):
                    continue
                py_files.append(f)

            if 1 <= len(py_files) <= 3:
                matches.append((h, msg, py_files))
                if len(matches) == limit:
                    break
    return matches


def run_benchmark(output_json: str = None) -> Dict[str, Any]:
    all_results = {}

    for repo_name, cfg in REPOS_CONFIG.items():
        repo_path = os.path.abspath(os.path.join(project_root, "test_repos", cfg["dir"]))
        commits = get_commits_for_repo(repo_name, cfg, limit=20)
        print("=" * 80)
        print(f"📦 專案: {repo_name} (篩選出 {len(commits)} 個真實修復 Commits)")
        print("=" * 80)

        repo_records = []
        for idx, (h, msg, files) in enumerate(commits, 1):
            print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案數: {len(files)}")
            commit_record = {"commit": h, "msg": msg, "files": []}
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
    print("\n" + "=" * 80)
    print("📊 5 大開源 Python 專案 100-Commit 基準審查統計匯總")
    print("=" * 80)
    header = f"{'專案名稱':<12} | {'Commit':<6} | {'檔案數':<6} | {'結構拓撲 (STRUCT)':<18} | {'函式體 (BODY)':<16} | {'零變動 (ZERO)':<14} | {'錯誤 (ERR)':<10} | {'總體捕獲率':<10}"
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
        print(
            f"{repo_name:<12} | {len(records):<6} | {total_files:<6} | {structural:<3} ({structural/total_files*100:5.1f}%)        | {body:<3} ({body/total_files*100:5.1f}%)      | {zero:<3} ({zero/total_files*100:5.1f}%)    | {errors:<10} | {rate:5.1f}%"
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
    print(
        f"{'總計 (ALL)':<12} | {100:<6} | {grand_total_files:<6} | {grand_structural:<3} ({grand_structural/grand_total_files*100:5.1f}%)        | {grand_body:<3} ({grand_body/grand_total_files*100:5.1f}%)      | {grand_zero:<3} ({grand_zero/grand_total_files*100:5.1f}%)    | {grand_errors:<10} | {grand_rate:5.1f}%"
    )
    summary_data["TOTAL"] = {
        "commits": 100,
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
    parser = argparse.ArgumentParser(description="Audit 5 Python Repos (20 Commits each)")
    parser.add_argument("--output", type=str, default="audit_python_repos_baseline.json", help="Output JSON path")
    args = parser.parse_args()

    run_benchmark(output_json=args.output)
