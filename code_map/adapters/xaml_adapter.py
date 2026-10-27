import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Set, Tuple

from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.core.graph import CodeMapGraph


class XAMLCodeMapBuilder(BaseCodeMapBuilder):
    """
    Avalonia (.axaml) 與 WPF / WinUI / MAUI (.xaml) 視覺樹與事件接線建構器
    - 解析 XAML 控制項階層樹 (CONTAINS) 與 x:Name / Name 錨點
    - 偵測可見性阻斷守衛: Avalonia IsVisible="False" 與 WPF Visibility="Collapsed|Hidden" (BLOCKED_VISIBILITY)
    - 捕捉路由事件綁定 (Click, PointerPressed, Tapped, SelectionChanged, TextChanged 等)
    - 捕捉 MVVM 命令綁定 (Command="{Binding SaveCommand}" / "{CompiledBinding ...}")
    - 支援與 Code-behind (.axaml.cs / .xaml.cs) 及 ViewModel 跨檔自動縫合
    """

    XAML_EVENTS = {
        "Click", "PointerPressed", "PointerReleased", "PointerMoved", "PointerEntered", "PointerExited",
        "Tapped", "DoubleTapped", "RightTapped", "KeyDown", "KeyUp", "TextInput",
        "GotFocus", "LostFocus", "SelectionChanged", "TextChanged", "ValueChanged",
        "Checked", "Unchecked", "Indeterminate", "Loaded", "Unloaded",
        "AttachedToVisualTree", "DetachedFromVisualTree", "Opened", "Closed", "Closing",
        "DataContextChanged", "Initialized", "TemplateApplied",
    }

    LAYOUT_CONTAINERS = {
        "Window", "UserControl", "Page", "Application", "ResourceDictionary",
        "Grid", "StackPanel", "DockPanel", "WrapPanel", "Canvas", "RelativePanel",
        "Border", "ScrollViewer", "Viewbox", "SplitView", "TabControl", "TabItem",
        "Expander", "GroupBox", "Card", "ItemsControl", "ContentControl",
    }

    INTERACTIVE_CONTROLS = {
        "Button", "RepeatButton", "ToggleButton", "RadioButton", "CheckBox", "HyperlinkButton",
        "TextBox", "MaskedTextBox", "NumericUpDown", "AutoCompleteBox", "ComboBox",
        "ListBox", "ListView", "TreeView", "DataGrid", "Slider", "ToggleSwitch",
        "MenuItem", "NativeMenuItem", "Calendar", "DatePicker", "TimePicker", "TabStrip",
    }

    @property
    def supported_extensions(self) -> Set[str]:
        return {".axaml", ".xaml"}

    @property
    def language_name(self) -> str:
        return "XAML / Avalonia AXAML"

    def parse_and_build(self, source_code: str, file_path: str = "MainWindow.axaml") -> CodeMapGraph:
        graph = CodeMapGraph(name=f"XAML Graph of {file_path}")
        graph.g.graph["imports"] = []
        graph.g.graph["exports"] = {}
        graph.g.graph["xaml_bindings"] = []

        # 提取 x:Class 與 x:DataType
        x_class_match = re.search(r'x:Class\s*=\s*"([^"]+)"', source_code)
        x_datatype_match = re.search(r'x:DataType\s*=\s*"([^"]+)"', source_code)
        x_class = x_class_match.group(1) if x_class_match else ""
        x_datatype = x_datatype_match.group(1).split(":")[-1] if x_datatype_match else ""
        graph.g.graph["x_class"] = x_class
        graph.g.graph["x_datatype"] = x_datatype

        # 使用正則預掃描所有起始/自閉合標籤與行號，兼顧容錯性與精確行號
        tag_pattern = re.compile(
            r"<(/?)([A-Za-z_][\w.]*)(?:\s+([^>]*?))?(/?)>",
            re.DOTALL,
        )
        attr_pattern = re.compile(r'([A-Za-z_][\w:.-]*)\s*=\s*"([^"]*)"')
        binding_pattern = re.compile(r"\{(?:Compiled)?Binding\s+(?:Path\s*=\s*)?([A-Za-z_][\w.]*)")

        line_starts = [0]
        for idx, ch in enumerate(source_code):
            if ch == "\n":
                line_starts.append(idx + 1)

        import bisect
        def get_line(offset: int) -> int:
            return bisect.bisect_right(line_starts, offset)

        stack: List[Dict[str, Any]] = []
        ctrl_counter = 0

        for m in tag_pattern.finditer(source_code):
            is_closing = bool(m.group(1))
            raw_tag = m.group(2)
            attr_str = m.group(3) or ""
            is_self_closing = bool(m.group(4))
            line_no = get_line(m.start())

            # 略過屬性元素語法，例如 <Window.DataContext> 或 <Button.Styles>
            if "." in raw_tag:
                continue

            local_tag = raw_tag.split(":")[-1]

            if is_closing:
                # 彈出對應開啟標籤
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i]["tag"] == local_tag:
                        stack.pop(i)
                        break
                continue

            attrs: Dict[str, str] = {}
            for am in attr_pattern.finditer(attr_str):
                attrs[am.group(1)] = am.group(2)

            # 判斷當前元素是否隱藏 (IsVisible="False" 或 Visibility="Collapsed"/"Hidden")
            is_self_hidden = False
            hidden_reason = ""
            is_vis_attr = attrs.get("IsVisible", "").strip().lower()
            wpf_vis_attr = attrs.get("Visibility", "").strip().lower()
            if is_vis_attr == "false":
                is_self_hidden = True
                hidden_reason = 'IsVisible="False"'
            elif wpf_vis_attr in ("collapsed", "hidden"):
                is_self_hidden = True
                hidden_reason = f'Visibility="{attrs.get("Visibility")}"'

            parent_hidden = any(item["is_hidden"] for item in stack)
            parent_hidden_reason = next((item["hidden_reason"] for item in reversed(stack) if item["is_hidden"]), "")
            effective_hidden = is_self_hidden or parent_hidden
            effective_reason = hidden_reason if is_self_hidden else f"父容器隱藏 ({parent_hidden_reason})"

            # 決定控制項名稱與 ID
            x_name = attrs.get("x:Name") or attrs.get("Name")
            ctrl_counter += 1
            display_name = f"#{x_name}" if x_name else f"<{local_tag}>#{ctrl_counter}"
            ctrl_id = f"ctrl:{display_name}@{file_path}:L{line_no}"

            # 檢查是否有綁定事件或 Command
            bound_events: List[Tuple[str, str, str]] = []  # (event_or_prop, target_name, kind)
            for k, v in attrs.items():
                clean_k = k.split(".")[-1].split(":")[-1]
                if clean_k in self.XAML_EVENTS and not v.strip().startswith("{"):
                    bound_events.append((clean_k, v.strip(), "ROUTED_EVENT"))
                elif clean_k == "Command":
                    bm = binding_pattern.search(v)
                    if bm:
                        cmd_path = bm.group(1).split(".")[-1]
                        bound_events.append(("Command", cmd_path, "MVVM_COMMAND"))

            should_create_node = (
                bool(x_name)
                or bool(bound_events)
                or local_tag in self.INTERACTIVE_CONTROLS
                or local_tag in ("Window", "UserControl", "Page")
            )

            current_node_id = None
            if should_create_node:
                current_node_id = ctrl_id
                graph.add_node_rich(
                    node_id=ctrl_id,
                    label=display_name,
                    category="UI_CONTROL",
                    scope={"scope_id": x_class or "scope:xaml", "file": file_path, "line": line_no},
                    props={
                        "ui_type": f"Avalonia/XAML {local_tag}",
                        "tag": local_tag,
                        "x_name": x_name or "",
                        "is_hidden": effective_hidden,
                        "hidden_reason": effective_reason,
                        "source_code": m.group(0),
                        "line_start": line_no,
                        "line_end": line_no,
                    },
                )

                # 建立與最近一個祖先控制項節點的 CONTAINS 邊
                parent_ctrl_id = next((item["node_id"] for item in reversed(stack) if item.get("node_id")), None)
                if parent_ctrl_id:
                    graph.add_edge_rich(
                        parent_ctrl_id,
                        ctrl_id,
                        edge_type="CONTAINS",
                        status="BLOCKED_VISIBILITY" if effective_hidden else "VALID",
                        detail=effective_reason if effective_hidden else "XAML 視覺樹包含關係",
                    )

                # 建立事件與 MVVM Command 綁定
                for evt_name, target_handler, kind in bound_events:
                    evt_id = f"event:{display_name}.{evt_name}@{file_path}:L{line_no}"
                    evt_label = f"{evt_name} [MVVM: {target_handler}]" if kind == "MVVM_COMMAND" else f"{evt_name}()"
                    edge_status = "BLOCKED_VISIBILITY" if effective_hidden else "VALID"

                    graph.add_node_rich(
                        node_id=evt_id,
                        label=evt_label,
                        category="EVENT_BINDING",
                        scope={"scope_id": x_class or "scope:xaml", "file": file_path, "line": line_no},
                        props={"event": evt_name, "kind": kind, "target": target_handler},
                    )
                    graph.add_edge_rich(
                        ctrl_id,
                        evt_id,
                        edge_type="WIRES_TO",
                        status=edge_status,
                        detail=f"💥 視覺樹遮蔽阻斷: {effective_reason}" if effective_hidden else f"XAML {kind} 綁定",
                    )

                    # 建立外部目標節點佔位符 (待 WorkspaceGraph 跨檔縫合至 .axaml.cs 或 ViewModel.cs)
                    ext_target_id = f"func:{target_handler}@external"
                    if ext_target_id not in graph.g:
                        graph.add_node_rich(
                            node_id=ext_target_id,
                            label=target_handler,
                            category="FUNCTION_DEF",
                            scope={"scope_id": "external", "file": file_path, "line": line_no},
                            props={"signature": f"{target_handler}()", "is_xaml_target": True, "kind": kind},
                        )

                    graph.add_edge_rich(
                        evt_id,
                        ext_target_id,
                        edge_type="TRIGGERS",
                        status=edge_status,
                        detail=f"💥 視覺樹遮蔽阻斷: {effective_reason}" if effective_hidden else f"XAML 觸發 {target_handler}",
                    )

                    graph.g.graph["xaml_bindings"].append({
                        "event_node_id": evt_id,
                        "placeholder_id": ext_target_id,
                        "target_name": target_handler,
                        "kind": kind,
                        "line": line_no,
                        "is_hidden": effective_hidden,
                        "hidden_reason": effective_reason,
                    })

            if not is_self_closing:
                stack.append({
                    "tag": local_tag,
                    "node_id": current_node_id,
                    "is_hidden": effective_hidden,
                    "hidden_reason": effective_reason,
                })

        return graph
