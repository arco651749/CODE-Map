import argparse
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.adapters import AdapterRegistry, get_adapter_for_file
from uia_coder.core.differ import UIAGraphDiffer


class CodeMapMiner:
    """
    CODE-Map 實戰探勘與基準評估引擎
    掃描目標 Git 倉庫中的 Bug 修復與性能優化 Commit，並自動評估 CODE-Map 的辨識與驗收命中率。
    """

    DEFAULT_KEYWORDS = [
        "fix", "bug", "error", "scope", "leak", "cleanup",
        "perf", "optimize", "parallel", "debounce", "throttle"
    ]

    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        if not os.path.isdir(os.path.join(self.repo_path, ".git")):
            raise ValueError(f"指定路徑不是有效的 Git 倉庫: {self.repo_path}")

    def find_target_commits(
        self,
        max_commits: int = 20,
        keywords: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """從 Git log 檢索包含關鍵字的 Commits"""
        kw_list = keywords or self.DEFAULT_KEYWORDS
        pattern = "|".join(re.escape(k) for k in kw_list)

        cmd = [
            "git", "-C", self.repo_path, "log",
            f"-n", str(max_commits * 3),
            "--pretty=format:%H%x09%s"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            return []

        matched = []
        for line in res.stdout.splitlines():
            if "\t" in line:
                h, msg = line.split("\t", 1)
                if re.search(pattern, msg, re.IGNORECASE):
                    matched.append({"hash": h, "message": msg})
                    if len(matched) >= max_commits:
                        break

        return matched

    def get_changed_code_files(self, commit_hash: str) -> List[str]:
        """取得該次 Commit 中有變動的 Python, JS, TS 檔案清單"""
        cmd = [
            "git", "-C", self.repo_path, "diff-tree",
            "--no-commit-id", "--name-only", "-r", commit_hash
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            return []

        supported_exts = set(AdapterRegistry._registry.keys())
        files = []
        for f in res.stdout.splitlines():
            lower = f.lower()
            if lower.endswith(".min.js") or "worker" in lower or "vendor" in lower:
                continue
            _, ext = os.path.splitext(f)
            if ext.lower() in supported_exts:
                files.append(f)
        return files

    def audit_commit(self, commit_hash: str, message: str) -> Dict[str, Any]:
        """對單一 Commit 進行 CODE-Map 語意差分審查"""
        changed_files = self.get_changed_code_files(commit_hash)
        file_audits = []

        for rel_file in changed_files:
            full_path = os.path.join(self.repo_path, rel_file)
            try:
                diff_res = UIAGraphDiffer.diff_git_file(
                    repo_path=self.repo_path,
                    file_path=full_path,
                    diff_range=f"{commit_hash}~1",
                    target_ref=commit_hash,
                )
                file_audits.append({
                    "file": rel_file,
                    "passed": diff_res.passed,
                    "status_transitions": diff_res.status_transitions,
                    "nodes_added_count": len(diff_res.nodes_added),
                    "edges_added_count": len(diff_res.edges_added),
                    "diff_markdown": diff_res.to_diff_markdown(),
                })
            except Exception as e:
                file_audits.append({
                    "file": rel_file,
                    "error": str(e)
                })

        return {
            "hash": commit_hash[:8],
            "message": message,
            "changed_files_count": len(changed_files),
            "file_audits": file_audits,
        }

    def run_benchmark(self, max_commits: int = 10) -> Dict[str, Any]:
        """執行完整倉庫自動探勘與天梯打分"""
        print(f"🔍 正在探勘倉庫: {self.repo_path} (搜尋帶有 fix/perf/leak 之提交)...")
        commits = self.find_target_commits(max_commits=max_commits)
        print(f"📊 找到 {len(commits)} 個符合條件的關鍵提交，開始執行 CODE-Map 語意差分驗收...")

        results = []
        for i, c in enumerate(commits, 1):
            print(f"  [{i}/{len(commits)}] 審查 {c['hash'][:8]}: {c['message'][:50]}...")
            audit = self.audit_commit(c["hash"], c["message"])
            results.append(audit)

        return {
            "repo": self.repo_path,
            "total_audited": len(results),
            "audits": results
        }

    @staticmethod
    def render_markdown_report(benchmark_data: Dict[str, Any]) -> str:
        lines = []
        lines.append(f"# 🏆 CODE-Map 實戰探勘與基準天梯報告")
        lines.append(f"> **目標倉庫**: `{benchmark_data['repo']}`  ")
        lines.append(f"> **審查提交數**: {benchmark_data['total_audited']} Commits\n")
        lines.append("| Commit | 開發者說明 (Ground Truth) | 涉及檔案 | CODE-Map 語意洞察與狀態躍遷 | 驗收結果 |")
        lines.append("|:------:|:--------------------------|:--------:|:----------------------------|:--------:|")

        for item in benchmark_data["audits"]:
            chash = item["hash"]
            msg = item["message"].replace("|", "\\|")
            file_count = item["changed_files_count"]

            # 統計所有檔案的躍遷
            transitions = []
            all_passed = True
            for fa in item["file_audits"]:
                if fa.get("status_transitions"):
                    for tr in fa["status_transitions"]:
                        transitions.append(f"{tr['icon']} {tr['target']} ({tr['from']}➔{tr['to']})")
                if not fa.get("passed", True):
                    all_passed = False

            trans_str = "<br/>".join(transitions) if transitions else "_結構性重構 / 檔案內部微調_"
            verdict_badge = "🟢 PASS" if all_passed else "🔴 BLOCKED"
            lines.append(f"| `{chash}` | {msg} | {file_count} 檔 | {trans_str} | {verdict_badge} |")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CODE-Map: GitHub 實戰探勘與基準評估工具")
    parser.add_argument("--repo", default=".", help="目標 Git 倉庫目錄路徑")
    parser.add_argument("--max", type=int, default=10, help="最多審查的目標 Commit 數量")
    parser.add_argument("--output", help="輸出 Markdown 報告檔案路徑")

    args = parser.parse_args()

    try:
        miner = CodeMapMiner(repo_path=args.repo)
        bench = miner.run_benchmark(max_commits=args.max)
        report = CodeMapMiner.render_markdown_report(bench)
        print("\n" + report)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📊 實戰報告已匯出至: {args.output}")

    except Exception as e:
        print(f"❌ 探勘失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
