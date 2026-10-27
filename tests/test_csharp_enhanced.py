import os
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from code_map.adapters.csharp_adapter import CSharpCodeMapBuilder
from code_map.adapters.xaml_adapter import XAMLCodeMapBuilder
from code_map.core.workspace_graph import WorkspaceGraphBuilder

print("============================================================")
print("▶ 測試 1: C# 單檔屬性、AddHandler、鏈式調用與 Task.Wait 死鎖攔截")
print("============================================================")

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

assert any("TitleText" in nid for nid in graph.g.nodes), "TitleText 屬性未被捕獲"
assert any("CalculatedCount" in nid for nid in graph.g.nodes), "CalculatedCount 屬性未被捕獲"
assert any("AddHandler" in nid for nid in graph.g.nodes), "Avalonia AddHandler 事件未被捕獲"
assert any(d.get("edge_type") == "TRIGGERS" and "OnSaveClicked" in v for u, v, d in graph.g.edges(data=True)), "AddHandler 未正確 TRIGGERS OnSaveClicked"
assert any("hazard:AsyncSyncDeadlock" in nid for nid in graph.g.nodes), "Task.Wait() 阻塞危害未被攔截"
print("✅ 測試 1 通過！")

print("\n============================================================")
print("▶ 測試 2 (方向一 + 二 + 三): Avalonia .axaml + .cs 跨檔雙向縫合、MVVM [RelayCommand] 與跨執行緒 UI 崩潰守衛")
print("============================================================")

axaml_content = '''<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.Views.MainWindow"
        x:DataType="vm:MainViewModel">
    <StackPanel>
        <!-- 1. 正常路由事件按鈕 -->
        <Button x:Name="btnRefresh" Content="重新整理" Click="OnRefreshClicked" />

        <!-- 2. MVVM RelayCommand 綁定按鈕 (自動對接 SaveAsync -> SaveCommand) -->
        <Button x:Name="btnSave" Content="儲存設定" Command="{Binding SaveCommand}" />

        <!-- 3. 隱藏父容器內的按鈕 (測試 BLOCKED_VISIBILITY 級聯攔截) -->
        <Border IsVisible="False">
            <Button x:Name="btnHiddenAction" Content="隱藏按鈕" Click="OnRefreshClicked" />
        </Border>

        <!-- 4. 拼錯名字的懸空事件按鈕 (測試 BLOCKED_SCOPE 斷路攔截) -->
        <Button x:Name="btnBroken" Content="壞掉的按鈕" Click="OnNonExistentHandler" />
    </StackPanel>
</Window>
'''

cs_viewmodel_and_codebehind = '''
using System;
using System.Threading.Tasks;
using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainWindow : Window {
    [ObservableProperty]
    private string _statusMessage = "Ready";

    public void OnRefreshClicked(object sender, EventArgs e) {
        // 方向三危害：在背景 Task.Run 未經 Dispatcher.UIThread 直接修改 UI 控制項 .Text
        Task.Run(() => {
            lblTitle.Text = "Updated from background thread!";
        });
    }

    [RelayCommand]
    private async Task SaveAsync() {
        await PersistConfigAsync();
    }
}
'''

with tempfile.TemporaryDirectory() as tmpdir:
    axaml_path = os.path.join(tmpdir, "MainWindow.axaml")
    cs_path = os.path.join(tmpdir, "MainWindow.axaml.cs")
    with open(axaml_path, "w", encoding="utf-8") as f:
        f.write(axaml_content)
    with open(cs_path, "w", encoding="utf-8") as f:
        f.write(cs_viewmodel_and_codebehind)

    merged_g = WorkspaceGraphBuilder.build_from_files([axaml_path, cs_path], root_dir=tmpdir)
    inv = merged_g.check_invariants()

    print(merged_g.to_codemap_markdown())
    print("\n--- 形式化守衛報告 ---")
    print("Verdict:", inv["verdict"])
    for err in inv["scope_errors"]:
        print("  [Scope Error]:", err["detail"])
    for haz in inv["hazards"]:
        print("  [Hazard]:", haz["detail"])

    # 斷言 A (方向一): XAML Click="OnRefreshClicked" 成功跨檔連通至 MainWindow.OnRefreshClicked
    assert any(
        "btnRefresh" in u and "MainWindow.OnRefreshClicked" in v and d.get("status") == "VALID"
        for u, v, d in merged_g.g.edges(data=True)
    ), "XAML Click='OnRefreshClicked' 未成功跨檔縫合至 C# OnRefreshClicked"

    # 斷言 B (方向二): XAML Command="{Binding SaveCommand}" 成功對接至 C# [RelayCommand] SaveAsync()
    assert any(
        "btnSave" in u and "MainWindow.SaveAsync" in v and d.get("status") == "VALID"
        for u, v, d in merged_g.g.edges(data=True)
    ), "XAML Command='{Binding SaveCommand}' 未成功對接至 [RelayCommand] SaveAsync()"

    # 斷言 C (方向二): [ObservableProperty] _statusMessage 自動推導 StatusMessage
    assert any(
        d.get("props", {}).get("generated_property") == "StatusMessage"
        for _, d in merged_g.g.nodes(data=True)
    ), "[ObservableProperty] _statusMessage 未成功推導出 StatusMessage"

    # 斷言 D (方向一): 隱藏容器 IsVisible="False" 觸發 VISIBILITY_VIOLATION
    assert any(
        h.get("type") == "VISIBILITY_VIOLATION" and 'IsVisible="False"' in h.get("detail", "")
        for h in inv["hazards"]
    ), "Avalonia IsVisible='False' 視覺樹遮蔽未被攔截"

    # 斷言 E (方向一): 懸空事件 Click="OnNonExistentHandler" 觸發 SCOPE_VIOLATION
    assert any(
        "OnNonExistentHandler" in e.get("detail", "")
        for e in inv["scope_errors"]
    ), "XAML 懸空 Handler (OnNonExistentHandler) 未被攔截"

    # 斷言 F (方向三): Task.Run 未經 Dispatcher.UIThread 直接改 UI 觸發 CrossThreadUIAccess 攔截
    assert any(
        "CrossThreadUIAccess" in n
        for n in merged_g.g.nodes
    ), "Task.Run 未經 Dispatcher.UIThread 直接操作 UI 控制項未被攔截"

print("\n🎉 方向一 (.axaml 視覺樹跨檔縫合)、方向二 (MVVM RelayCommand/ObservableProperty)、方向三 (CrossThreadUI 守衛) 100% 測試通過！")
