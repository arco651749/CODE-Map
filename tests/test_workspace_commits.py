import os
import subprocess
import sys
import time

# 將專案根目錄加入模組搜尋路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_PATH = r"D:\Users\arco0\.gemini\config\plugins\workspace-file-tree"

from uia_coder.adapters import AdapterRegistry
from uia_coder.core.differ import UIAGraphDiffer

def get_all_commits():
    cmd = ["git", "-C", REPO_PATH, "log", "--reverse", "--pretty=format:%H%x09%s"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    commits = []
    for line in res.stdout.splitlines():
        if "\t" in line:
            h, msg = line.split("\t", 1)
            commits.append((h, msg))
    return commits

def is_vendor_or_minified(file_path):
    lower = file_path.lower()
    return lower.endswith(".min.js") or "pdf.worker" in lower or "vendor" in lower

def get_changed_code_files(commit_hash):
    cmd = ["git", "-C", REPO_PATH, "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    supported = set(AdapterRegistry._registry.keys())
    files = []
    for f in res.stdout.splitlines():
        if is_vendor_or_minified(f):
            continue
        _, ext = os.path.splitext(f)
        if ext.lower() in supported:
            files.append(f)
    return files

def main():
    commits = get_all_commits()
    print(f"總共發現 {len(commits)} 個 Commit，開始逐版本評估 CODE-Map 分析成效：\n", flush=True)
    
    total_audited = 0
    passed_count = 0
    blocked_count = 0

    for idx, (h, msg) in enumerate(commits, 1):
        short_h = h[:7]
        files = get_changed_code_files(h)
        if not files:
            print(f"[{idx:02d}/{len(commits)}] {short_h} | {msg} -> (無支援源碼變動，跳過)", flush=True)
            continue
            
        print(f"\n==================================================", flush=True)
        print(f"[{idx:02d}/{len(commits)}] Commit: {short_h} - {msg}", flush=True)
        print(f"  變動代碼檔案: {files}", flush=True)
        
        t0 = time.time()

        # 如果是第一個 commit，沒有 HEAD~1，做初次建置
        if idx == 1:
            print(f"  [首個提交] 測試單檔 CODE-Map 解析...", flush=True)
            for f in files:
                try:
                    cmd_show = ["git", "-C", REPO_PATH, "show", f"{h}:{f}"]
                    src = subprocess.run(cmd_show, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
                    adapter = AdapterRegistry.get_adapter(f)
                    graph = adapter.parse_and_build(src, file_path=f)
                    anchors = graph.get_ui_anchors()
                    print(f"    - {f}: 節點數={graph.g.number_of_nodes()}, 邊數={graph.g.number_of_edges()}, 根控制項={len(anchors)}", flush=True)
                except Exception as e:
                    print(f"    - {f} 解析失敗: {e}", flush=True)
            continue

        for f in files:
            total_audited += 1
            full_path = os.path.join(REPO_PATH, f)
            try:
                diff_res = UIAGraphDiffer.diff_git_file(
                    repo_path=REPO_PATH,
                    file_path=full_path,
                    diff_range=f"{h}~1",
                    target_ref=h,
                )
                status_icon = '🟢 通過' if diff_res.passed else '🔴 阻擋 (BLOCKED)'
                if diff_res.passed:
                    passed_count += 1
                else:
                    blocked_count += 1

                print(f"  檔案: {f}", flush=True)
                print(f"    - 驗收判定: {status_icon}", flush=True)
                print(f"    - 節點增減: +{len(diff_res.nodes_added)} / -{len(diff_res.nodes_removed)}", flush=True)
                print(f"    - 邊增減:   +{len(diff_res.edges_added)} / -{len(diff_res.edges_removed)}", flush=True)
                if diff_res.status_transitions:
                    trans_list = [t['target'] + ': ' + t['from'] + ' -> ' + t['to'] for t in diff_res.status_transitions]
                    print(f"    - 狀態躍遷: {trans_list}", flush=True)
                if diff_res.invariant_violations:
                    viol_list = [v['message'] for v in diff_res.invariant_violations]
                    print(f"    - 違規項:   {viol_list}", flush=True)
            except Exception as e:
                print(f"  檔案 {f} 差分失敗: {e}", flush=True)

        t1 = time.time()
        print(f"  審查耗時: {t1 - t0:.2f} 秒", flush=True)

    print(f"\n==================================================", flush=True)
    print(f"評估總結: 共審查 {total_audited} 次檔案變更 | 🟢 通過: {passed_count} | 🔴 阻擋: {blocked_count}", flush=True)

if __name__ == "__main__":
    main()
