import os
import sys
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Set

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class _DOMTreeParser(HTMLParser):
    """
    HTML DOM 拓樸結構走訪器 (基於 Python 標準庫 html.parser)
    負責構建 DOM 樹、追蹤父子包含關係、標籤閉合平衡，並即時識別可見性阻隔危害。
    """

    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    STRUCTURAL_TAGS = {
        "div", "section", "article", "main", "header", "footer", "nav",
        "aside", "form", "ul", "ol", "table", "dialog", "details"
    }

    INTERACTIVE_TAGS = {
        "button", "input", "select", "textarea", "a", "form", "details"
    }

    OVERLAY_KEYWORDS = {
        "modal", "dialog", "confirm-modal", "alert-modal", "prompt-modal",
        "confirm-dialog", "modal-overlay", "popup-overlay"
    }

    def __init__(self, file_path: str, graph: UIACodeGraph):
        super().__init__()
        self.file_path = file_path
        self.graph = graph
        self.stack: List[Dict[str, Any]] = []
        self.all_elements: List[Dict[str, Any]] = []
        self.id_table: Dict[str, str] = {}
        self.hazards: List[Dict[str, Any]] = []
        self.scripts: List[Dict[str, Any]] = []
        self.stylesheets: List[Dict[str, Any]] = []
        self._reported_visibility_targets: Set[str] = set()

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        tag_lower = tag.lower()
        attr_dict = dict(attrs)
        elem_id = attr_dict.get("id", "").strip() or None
        class_str = attr_dict.get("class", "").strip()
        classes = class_str.split() if class_str else []
        line, col = self.getpos()

        # 樣式與可見性判定
        style = attr_dict.get("style", "").replace(" ", "").lower()
        is_hidden = ("hidden" in attr_dict) or ("display:none" in style)

        parent = self.stack[-1] if self.stack else None
        ancestors = list(self.stack)

        # 判斷是否已有祖先為浮層對話框 (若已處於對話框內部，不再當作獨立對話框根節點)
        has_overlay_ancestor = any(a.get("is_overlay_dialog") for a in ancestors)

        # 獨立浮層 / 模態對話框判定 (Modal / Dialog / Confirm Overlay)
        is_overlay_dialog = (not has_overlay_ancestor) and (
            tag_lower == "dialog" or
            any(kw in (elem_id or "").lower() for kw in self.OVERLAY_KEYWORDS) or
            any(any(kw in c.lower() for kw in self.OVERLAY_KEYWORDS) for c in classes)
        )

        # 互動元件判定 (Button / Input / Anchor / Form)
        is_interactive = (
            tag_lower in self.INTERACTIVE_TAGS or
            "onclick" in attr_dict or
            attr_dict.get("role") in ("button", "link", "checkbox", "switch") or
            (elem_id and any(elem_id.lower().startswith(p) for p in ("btn-", "btn", "input-", "search-", "select-")))
        )

        # 生成節點識別碼
        if elem_id:
            node_id = f"DOM:{tag_lower}#{elem_id}"
            label = f"<{tag_lower} id='{elem_id}'>"
        else:
            node_id = f"DOM:{tag_lower}@{self.file_path}:L{line}C{col}"
            cls_repr = f".{classes[0]}" if classes else ""
            label = f"<{tag_lower}{cls_repr}>"

        elem_record = {
            "node_id": node_id,
            "tag": tag_lower,
            "id": elem_id,
            "classes": classes,
            "line": line,
            "col": col,
            "is_hidden": is_hidden,
            "is_overlay_dialog": is_overlay_dialog,
            "is_interactive": is_interactive,
            "attrs": attr_dict,
            "parent": parent,
            "ancestors": ancestors,
        }

        self.all_elements.append(elem_record)
        if elem_id:
            self.id_table[elem_id] = node_id

        # 註冊資源引用
        if tag_lower == "script" and "src" in attr_dict:
            self.scripts.append({"src": attr_dict["src"], "line": line, "col": col})
        elif tag_lower == "link" and attr_dict.get("rel") == "stylesheet" and "href" in attr_dict:
            self.stylesheets.append({"href": attr_dict["href"], "line": line, "col": col})

        # 新增至 UIACodeGraph
        scope = {
            "file": self.file_path,
            "line": line,
            "col": col,
            "qualified_path": "/".join([a["tag"] + (f"#{a['id']}" if a["id"] else "") for a in ancestors] + [tag_lower + (f"#{elem_id}" if elem_id else "")])
        }

        self.graph.add_node_rich(
            node_id=node_id,
            label=label,
            category="DOM_ELEMENT",
            scope=scope,
            props={
                "tag": tag_lower,
                "id": elem_id,
                "classes": classes,
                "is_hidden": is_hidden,
                "is_overlay_dialog": is_overlay_dialog,
                "is_interactive": is_interactive,
                "line": line,
                "col": col,
            }
        )

        # 若具備互動屬性或對話框，同步登記為 UI_CONTROL 錨點
        if elem_id and (is_interactive or is_overlay_dialog):
            anchor_id = f"#{elem_id}"
            if anchor_id not in self.graph.g:
                control_type = "Button" if "btn" in elem_id.lower() or tag_lower == "button" else ("Modal" if is_overlay_dialog else "Control")
                self.graph.add_node_rich(
                    node_id=anchor_id,
                    label=f"#{elem_id} ({control_type})",
                    category="UI_CONTROL",
                    scope=scope,
                    props={"control_type": control_type, "dom_node_id": node_id}
                )
                self.graph.add_edge_rich(
                    source=anchor_id,
                    target=node_id,
                    edge_type="GROUNDS_TO",
                    flow_type="DOM_GROUNDING",
                    status="VALID",
                    detail="UI 控制項對齊至實體 DOM 元素"
                )

        # 建立父子包含邊與物理可見性阻隔守衛
        if parent:
            edge_status = "VALID"
            detail = ""

            # 🚨 物理可見性阻隔守衛 (Visibility Cascade Invariant):
            # 僅當「獨立浮層對話框 (Modal/Confirm Dialog)」被塞進任何帶有 hidden/display:none 的父容器時觸發
            if is_overlay_dialog and node_id not in self._reported_visibility_targets:
                hidden_ancestor = next((a for a in ancestors if a["is_hidden"]), None)
                if hidden_ancestor:
                    self._reported_visibility_targets.add(node_id)
                    edge_status = "BLOCKED_VISIBILITY"
                    h_name = f"<{hidden_ancestor['tag']} id='{hidden_ancestor['id']}'>" if hidden_ancestor['id'] else f"<{hidden_ancestor['tag']}>"
                    detail = f"💥 物理可見性阻隔: 獨立對話框 '{label}' 被錯誤嵌套於帶有 hidden 或 display:none 的容器 {h_name} 內部！導致該對話框在使用者端物理上無法正常看見！"

            self.graph.add_edge_rich(
                source=parent["node_id"],
                target=node_id,
                edge_type="CONTAINS",
                flow_type="DOM_TREE",
                status=edge_status,
                detail=detail
            )

        if tag_lower not in self.VOID_ELEMENTS:
            self.stack.append(elem_record)

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower in self.VOID_ELEMENTS:
            return

        line, col = self.getpos()

        # 頂部直接匹配
        if self.stack and self.stack[-1]["tag"] == tag_lower:
            self.stack.pop()
            return

        # 向上搜尋堆疊，查找是否有未閉合的中間標籤
        match_idx = -1
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag_lower:
                match_idx = i
                break

        if match_idx != -1:
            # 找到匹配，說明中間夾帶了未閉合標籤
            unclosed_items = self.stack[match_idx + 1:]
            for u in unclosed_items:
                if u["tag"] in self.STRUCTURAL_TAGS:
                    u_label = f"<{u['tag']} id='{u['id']}'>" if u['id'] else f"<{u['tag']}>"
                    msg = f"💥 HTML 結構缺陷: 標籤 {u_label} 於 L{u['line']} 開啟但未正常閉合，已被 L{line} 的 </{tag_lower}> 非預期吞噬！"
                    self.hazards.append({
                        "type": "UNCLOSED_TAG",
                        "node": u["node_id"],
                        "detail": msg,
                        "count": 1,
                    })
            self.stack = self.stack[:match_idx]
        else:
            # 孤兒閉合標籤
            msg = f"💥 HTML 結構缺陷: 出現無對應開啟標籤的孤兒閉合標籤 </{tag_lower}> 於 L{line}！"
            self.hazards.append({
                "type": "ORPHAN_END_TAG",
                "detail": msg,
                "count": 1,
            })

    def finalize(self):
        # 檢查檔案結尾未閉合的結構性標籤 (如未閉合的 div / modal / drawer)
        for u in self.stack:
            if u["tag"] in self.STRUCTURAL_TAGS:
                u_label = f"<{u['tag']} id='{u['id']}'>" if u['id'] else f"<{u['tag']}>"
                msg = f"💥 HTML 結構缺陷: 標籤 {u_label} 於 L{u['line']} 開啟，但直至檔案結尾仍未閉合！"
                self.hazards.append({
                    "type": "UNCLOSED_TAG",
                    "node": u["node_id"],
                    "detail": msg,
                    "count": 1,
                })


class HTMLUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 DOM 拓樸樹的 HTML 語意控制圖建構器
    提供實體 DOM 元素建模、容器嵌套包含關係、標籤閉合平衡與物理可見性阻隔守衛。
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".html", ".htm"}

    @property
    def language_name(self) -> str:
        return "HTML"

    def parse_and_build(self, source_code: str, file_path: str = "index.html") -> UIACodeGraph:
        graph = UIACodeGraph(name=f"DOM Graph of {file_path}")
        parser = _DOMTreeParser(file_path=file_path, graph=graph)
        try:
            parser.feed(source_code)
            parser.finalize()
        except Exception as e:
            parser.hazards.append({
                "type": "HTML_PARSE_ERROR",
                "detail": f"HTML 解析異常中斷: {str(e)}",
                "count": 1
            })

        # 將中繼資料存入圖譜屬性
        graph.g.graph["id_table"] = parser.id_table
        graph.g.graph["scripts"] = parser.scripts
        graph.g.graph["stylesheets"] = parser.stylesheets
        graph.g.graph["hazards"] = parser.hazards

        return graph
