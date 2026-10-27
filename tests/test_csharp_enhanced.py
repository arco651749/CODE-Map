import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from code_map.adapters.csharp_adapter import CSharpCodeMapBuilder

csharp_code = '''
using System;
using Avalonia.Controls;

public class MyAvaloniaWindow : Window {
    public string TitleText { get; set; }
    public int CalculatedCount => 42;

    private Button _saveButton;

    public void InitControls() {
        _saveButton = new Button();
        _saveButton.AddHandler(Button.ClickEvent, OnSaveClicked);
    }

    public void OnSaveClicked(object sender, EventArgs e) {
        var result = service?.ApiClient?.FetchData();
        DoBlockingWork();
    }

    public void DoBlockingWork() {
        // 危害：在 UI 執行緒直接阻塞等待非同步 Task
        var task = GetDataAsync();
        task.Wait();
    }
}
'''

builder = CSharpCodeMapBuilder()
graph = builder.parse_and_build(csharp_code, file_path="MyAvaloniaWindow.cs")

print("=== 節點列表 ===")
for nid, data in graph.g.nodes(data=True):
    print(f"[{data.get('category')}] {nid} | label={data.get('label')}")

print("\n=== 邊與接線列表 ===")
for u, v, data in graph.g.edges(data=True):
    print(f"{u} --[{data.get('edge_type')}]--> {v} (status={data.get('status')})")

# 斷言 1: 屬性宣告是否被捕獲
assert any("TitleText" in nid for nid in graph.g.nodes), "TitleText 屬性未被捕獲"
assert any("CalculatedCount" in nid for nid in graph.g.nodes), "CalculatedCount 屬性未被捕獲"

# 斷言 2: Avalonia AddHandler 是否接通
assert any("AddHandler" in nid for nid in graph.g.nodes), "Avalonia AddHandler 事件未被捕獲"
assert any(d.get("edge_type") == "TRIGGERS" and "OnSaveClicked" in v for u, v, d in graph.g.edges(data=True)), "AddHandler 未正確 TRIGGERS OnSaveClicked"

# 斷言 3: Task.Wait() 阻塞危害是否被攔截
assert any("hazard:AsyncSyncDeadlock" in nid for nid in graph.g.nodes), "Task.Wait() 阻塞危害未被攔截"
assert any(d.get("status") == "BLOCKED_INVARIANT" for u, v, d in graph.g.edges(data=True)), "未觸發 BLOCKED_INVARIANT 守衛狀態"

print("\n🎉 C# Avalonia 增強適配器所有斷言 100% 通過！")
