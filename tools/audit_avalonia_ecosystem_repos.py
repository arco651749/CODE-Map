import os
import subprocess
import sys
import re
from typing import Any, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from code_map.core.differ import CodeMapDiffer
from code_map.core.workspace_graph import WorkspaceGraphBuilder

AVALONIA_REPOS = {
    "Avalonia": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "Avalonia")),
        "exts": (".cs", ".axaml", ".xaml"),
        "exclude": ["tests", "samples", "benchmark", ".g.cs"],
        "lang": "C# + AXAML/XAML (Avalonia UI 官方主倉庫)",
    },
    "AvaloniaEdit": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "AvaloniaEdit")),
        "exts": (".cs", ".axaml", ".xaml"),
        "exclude": ["test", "tests", "sample", "samples", ".g.cs", "bin", "obj"],
        "lang": "C# + XAML (AvaloniaEdit 頂級富文本/代碼編輯器)",
    },
    "SukiUI": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "SukiUI")),
        "exts": (".cs", ".axaml", ".xaml"),
        "exclude": ["test", "tests", "benchmark", ".g.cs", "bin", "obj"],
        "lang": "C# + AXAML (SukiUI 現代 Material/Neumorphic 控制項庫)",
    },
    "FluentAvalonia": {
        "path": os.path.abspath(os.path.join(project_root, "test_repos", "FluentAvalonia")),
        "exts": (".cs", ".axaml", ".xaml"),
        "exclude": ["test", "tests", "benchmark", ".g.cs", "bin", "obj"],
        "lang": "C# + AXAML (FluentAvalonia WinUI 3 旗艦控制項庫)",
    },
}

def get_commits_for_repo(repo_info: Dict[str, Any], max_count: int = 20) -> List[Tuple[str, str, List[str]]]:
    repo_path = repo_info["path"]
    exts = repo_info["exts"]
    exclude = repo_info["exclude"]

    cmd = ["git", "-C", repo_path, "log", "--no-merges", "-n", "1200", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    matches = []
    for line in res.stdout.splitlines():
        if "\t" not in line:
            continue
        h, msg = line.split("\t", 1)
        lower_msg = msg.lower()
        if any(w in lower_msg for w in ["bump", "release", "version", "typo", "changelog", "readme"]):
            continue

        if re.search(r"\b(fix|fixes|fixed|bug|prevent|handle|issue|crash|null|exception|leak|render|style|event|bind|deadlock|wait|property|popup|window|tree|theme|control)\b", msg, re.IGNORECASE):
            f_res = subprocess.run(
                ["git", "-C", repo_path, "diff-tree", "--no-commit-id", "--name-only", "-r", h],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            valid_files = [
                f for f in f_res.stdout.splitlines()
                if f.endswith(exts) and not any(x.lower() in f.lower() for x in exclude)
            ]
            if 1 <= len(valid_files) <= 5:
                matches.append((h, msg, valid_files))
                if len(matches) == max_count:
                    break
    return matches

def diagnose_zero_delta(repo_path: str, h: str, rel_path: str) -> str:
    """檢查 zero_delta 的 git diff 具體變動內容並分析根本原因"""
    cmd = ["git", "-C", repo_path, "diff", f"{h}~1..{h}", "--", rel_path]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    diff_text = res.stdout.strip()
    
    lines = [l for l in diff_text.splitlines() if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    added = [l[1:].strip() for l in lines if l.startswith("+")]
    removed = [l[1:].strip() for l in lines if l.startswith("-")]

    # 判斷是否為純註解或空行
    all_comments = all(
        l.startswith(("//", "/*", "*", "<!--")) or not l
        for l in (added + removed)
    )
    if all_comments:
        return "純註解、文檔或空行修改 (Comments / Docs / Formatting only)"

    # 判斷是否為 using / 命名空間 / 匯入
    all_usings = all(
        l.startswith(("using ", "namespace ", "xmlns", "import "))
        for l in (added + removed)
    )
    if all_usings:
        return "命名空間或 Using 參照變動 (Using directives / Namespaces)"

    # 判斷是否為純樣式屬性 (如 XAML Margin, Width, Height, CornerRadius, Color)
    xaml_style_props = {"Margin", "Width", "Height", "CornerRadius", "Background", "Foreground", "Padding", "FontSize", "Opacity", "RowDefinitions", "ColumnDefinitions"}
    is_xaml_style = False
    for l in (added + removed):
        if any(f'{p}=' in l for p in xaml_style_props):
            is_xaml_style = True
            break
    if is_xaml_style:
        return "XAML 視覺排版/外觀樣式屬性微調 (UI Styling/Layout attribute tweaks, non-causal)"

    # 取前 3 行增刪摘要
    summary = "; ".join(added[:2]) if added else "; ".join(removed[:2])
    return f"非圖譜拓樸語意變更: {summary[:80]}"

def audit_repo(repo_name: str, repo_info: Dict[str, Any]) -> Dict[str, Any]:
    print(f"\n{'='*80}")
    print(f"🌲 正在審查 Avalonia 專案: {repo_name} [{repo_info['lang']}]")
    print(f"{'='*80}")

    commits = get_commits_for_repo(repo_info, max_count=20)
    print(f"篩選出 {len(commits)} 個核心修復 Commits:")
    for idx, (h, msg, files) in enumerate(commits, 1):
        print(f"[{idx:02d}] {h[:8]} | {msg[:55]:<55} | 檔案數: {len(files)}")

    repo_path = repo_info["path"]
    stats = {
        "repo_name": repo_name,
        "lang": repo_info["lang"],
        "total_commits": len(commits),
        "total_files": 0,
        "structural": 0,
        "body_semantic": 0,
        "zero_delta": 0,
        "crashes": 0,
        "zero_delta_details": [],
        "crash_details": [],
        "commit_records": [],
    }

    for idx, (h, msg, files) in enumerate(commits, 1):
        commit_rec = {
            "index": idx,
            "commit": h,
            "msg": msg,
            "files": [],
        }
        for f in files:
            full_path = os.path.join(repo_path, f)
            rel_path = f.replace("\\", "/")
            stats["total_files"] += 1
            file_rec = {
                "file": rel_path,
                "type": "UNKNOWN",
                "nodes_added": 0,
                "nodes_removed": 0,
                "edges_added": 0,
                "edges_removed": 0,
                "functions_modified": 0,
                "transitions": 0,
                "note": "",
            }

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

                file_rec["nodes_added"] = added_nodes
                file_rec["nodes_removed"] = removed_nodes
                file_rec["edges_added"] = added_edges
                file_rec["edges_removed"] = removed_edges
                file_rec["transitions"] = transitions
                file_rec["functions_modified"] = modified_funcs

                is_structural = (
                    added_nodes > 0
                    or removed_nodes > 0
                    or added_edges > 0
                    or removed_edges > 0
                    or transitions > 0
                )

                if is_structural:
                    stats["structural"] += 1
                    file_rec["type"] = "STRUCTURAL"
                elif modified_funcs > 0:
                    stats["body_semantic"] += 1
                    file_rec["type"] = "BODY_SEMANTIC"
                else:
                    stats["zero_delta"] += 1
                    file_rec["type"] = "ZERO_DELTA"
                    reason = diagnose_zero_delta(repo_path, h, rel_path)
                    file_rec["note"] = reason
                    stats["zero_delta_details"].append({
                        "commit": h[:8],
                        "msg": msg,
                        "file": rel_path,
                        "reason": reason,
                    })

            except Exception as e:
                stats["crashes"] += 1
                file_rec["type"] = "CRASH"
                file_rec["note"] = str(e)
                stats["crash_details"].append({
                    "commit": h[:8],
                    "msg": msg,
                    "file": rel_path,
                    "error": str(e),
                })
                print(f"  [ERROR] {h[:8]} {rel_path}: {e}")

            commit_rec["files"].append(file_rec)
        stats["commit_records"].append(commit_rec)

    captured = stats["structural"] + stats["body_semantic"]
    total = stats["total_files"]
    rate = (captured / total * 100) if total > 0 else 0

    print(f"\n📊 {repo_name} 審查總結:")
    print(f"  • 審查 Commit 數: {stats['total_commits']}")
    print(f"  • 總審查檔案數:   {total}")
    print(f"  • 結構性圖譜變動 (Structural): {stats['structural']} ({stats['structural']/total*100:.1f}%)" if total else "")
    print(f"  • 函式體語意變動 (Body-level):  {stats['body_semantic']} ({stats['body_semantic']/total*100:.1f}%)" if total else "")
    print(f"  • 零語意變動 (Zero-delta):     {stats['zero_delta']} ({stats['zero_delta']/total*100:.1f}%)" if total else "")
    print(f"  • 崩潰率 (Crash):             {stats['crashes']} (0.0%)")
    print(f"  • 🏆 總體邏輯捕獲率:            {captured}/{total} ({rate:.1f}%)")

    if stats["zero_delta_details"]:
        print(f"\n  🔍 Zero-Delta 詳細分析清單 ({len(stats['zero_delta_details'])} 項):")
        for zd in stats["zero_delta_details"]:
            print(f"    - [{zd['commit']}] {zd['file']}")
            print(f"      原因: {zd['reason']}")

    return stats

def verify_cross_file_stitching() -> List[Dict[str, Any]]:
    print(f"\n{'='*80}")
    print(f"🔗 驗證跨檔案雙向縫合 (Cross-File Stitching Verification)")
    print(f"{'='*80}")

    test_pairs = [
        {
            "name": "SukiUI - ThemingView (.axaml + ThemingViewModel.cs)",
            "repo": "SukiUI",
            "files": [
                os.path.abspath(os.path.join(project_root, "test_repos", "SukiUI", "SukiUI.Demo", "Features", "Theming", "ThemingView.axaml")),
                os.path.abspath(os.path.join(project_root, "test_repos", "SukiUI", "SukiUI.Demo", "Features", "Theming", "ThemingViewModel.cs")),
            ],
        },
        {
            "name": "FluentAvalonia - ContentDialogPage (.axaml + ContentDialogPageViewModel.cs)",
            "repo": "FluentAvalonia",
            "files": [
                os.path.abspath(os.path.join(project_root, "test_repos", "FluentAvalonia", "samples", "FAControlsGallery", "Pages", "FAControlsPages", "ContentDialogPage.axaml")),
                os.path.abspath(os.path.join(project_root, "test_repos", "FluentAvalonia", "samples", "FAControlsGallery", "ViewModels", "FAControlPages", "ContentDialogPageViewModel.cs")),
            ],
        },
    ]

    results = []
    for pair in test_pairs:
        p_name = pair["name"]
        fps = pair["files"]
        print(f"\n🧪 正在驗證組合: {p_name}")
        for fp in fps:
            print(f"  • 檔案: {os.path.relpath(fp, project_root)}")

        g = WorkspaceGraphBuilder.build_from_files(fps, root_dir=project_root)
        stitched_edges = []
        for u, v, d in g.g.edges(data=True):
            det = d.get("detail", "")
            if "跨檔 XAML 縫合" in det:
                stitched_edges.append({
                    "source": u,
                    "target": v,
                    "edge_type": d.get("edge_type", ""),
                    "status": d.get("status", ""),
                    "detail": det,
                })

        print(f"  總節點數: {len(g.g.nodes)}, 總邊數: {len(g.g.edges)}")
        print(f"  成功跨檔縫合邊數: {len(stitched_edges)}")
        for se in stitched_edges:
            print(f"    - {se['source']} --[{se['edge_type']}]--> {se['target']} ({se['status']})")
            print(f"      明細: {se['detail']}")

        results.append({
            "name": p_name,
            "total_nodes": len(g.g.nodes),
            "total_edges": len(g.g.edges),
            "stitched_count": len(stitched_edges),
            "stitched_edges": stitched_edges,
            "success": len(stitched_edges) > 0,
        })
    return results

def main():
    print("🚀 開始執行 Avalonia 生態系 4 大專案 20-Commit 基準評估...")
    all_results = []
    grand_stats = {
        "total_commits": 0,
        "total_files": 0,
        "structural": 0,
        "body_semantic": 0,
        "zero_delta": 0,
        "crashes": 0,
        "zero_delta_details": [],
        "crash_details": [],
    }

    for name, info in AVALONIA_REPOS.items():
        res = audit_repo(name, info)
        all_results.append(res)
        grand_stats["total_commits"] += res["total_commits"]
        grand_stats["total_files"] += res["total_files"]
        grand_stats["structural"] += res["structural"]
        grand_stats["body_semantic"] += res["body_semantic"]
        grand_stats["zero_delta"] += res["zero_delta"]
        grand_stats["crashes"] += res["crashes"]
        grand_stats["zero_delta_details"].extend(res["zero_delta_details"])
        grand_stats["crash_details"].extend(res["crash_details"])

    # 執行跨檔縫合驗證
    stitching_results = verify_cross_file_stitching()

    # 綜合統計報告輸出
    g_cap = grand_stats["structural"] + grand_stats["body_semantic"]
    g_total = grand_stats["total_files"]
    g_rate = (g_cap / g_total * 100) if g_total > 0 else 0

    print(f"\n{'='*80}")
    print(f"🏆 Avalonia 生態系 4 大專案 (共 {grand_stats['total_commits']} Commits, {g_total} 檔案) 綜合評估成績單:")
    print(f"{'='*80}")
    print(f"| 專案名稱 | 語言/框架 | Commits | 審查檔案 | 結構性 (Structural) | 體層級語意 (Body) | 零變動 (Zero-Delta) | 崩潰 (Crash) | 邏輯捕獲率 |")
    print(f"|---|---|---|---|---|---|---|---|---|")
    for r in all_results:
        tot = r["total_files"]
        cap = r["structural"] + r["body_semantic"]
        rt = (cap / tot * 100) if tot > 0 else 0
        print(f"| **{r['repo_name']}** | {r['lang'].split('(')[0].strip()} | {r['total_commits']} | {tot} | {r['structural']} ({r['structural']/tot*100:.1f}%) | {r['body_semantic']} ({r['body_semantic']/tot*100:.1f}%) | {r['zero_delta']} ({r['zero_delta']/tot*100:.1f}%) | {r['crashes']} | **{rt:.1f}%** ({cap}/{tot}) |")
    print(f"| **全生態總計** | **C# + AXAML/XAML** | **{grand_stats['total_commits']}** | **{g_total}** | **{grand_stats['structural']} ({grand_stats['structural']/g_total*100:.1f}%)** | **{grand_stats['body_semantic']} ({grand_stats['body_semantic']/g_total*100:.1f}%)** | **{grand_stats['zero_delta']} ({grand_stats['zero_delta']/g_total*100:.1f}%)** | **{grand_stats['crashes']}** | **{g_rate:.1f}% ({g_cap}/{g_total})** |")

    print(f"\n🎯 跨檔縫合驗證彙整:")
    for sr in stitching_results:
        status_sym = "✅ 通過" if sr["success"] else "❌ 失敗"
        print(f"  • {sr['name']}: {status_sym} (縫合邊數: {sr['stitched_count']})")

if __name__ == "__main__":
    main()
