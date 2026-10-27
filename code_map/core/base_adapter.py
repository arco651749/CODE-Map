from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set
from code_map.core.graph import CodeMapGraph


def _has_early_exit(node: Any) -> bool:
    """檢查 AST 子樹中是否包含 return, throw, raise, panic, exit 等早退語句"""
    if not node:
        return False
    exit_types = {
        "return_statement", "throw_statement", "raise_statement",
        "break_statement", "continue_statement"
    }
    stack = [node]
    while stack:
        curr = stack.pop()
        if curr.type in exit_types:
            return True
        if curr.type == "call_expression":
            fn = curr.child_by_field_name("function")
            if fn:
                txt = fn.text.decode("utf-8", errors="replace").lower()
                if any(k in txt for k in ("panic", "exit", "abort", "fatal")):
                    return True
        if hasattr(curr, "children"):
            stack.extend(curr.children)
    return False


class BaseCodeMapBuilder(ABC):
    """
    所有語言語意圖譜建構器的抽象基礎介面 (Strategy Pattern)
    """

    @property
    @abstractmethod
    def supported_extensions(self) -> Set[str]:
        """支援的副檔名集合，例如 {'.js', '.mjs'} 或 {'.py'}"""
        pass

    @property
    @abstractmethod
    def language_name(self) -> str:
        """語言名稱，例如 'JavaScript', 'Python'"""
        pass

    @abstractmethod
    def parse_and_build(self, source_code: str, file_path: str = "main") -> CodeMapGraph:
        """
        將原始碼字串解析為標準 CodeMapGraph
        """
        pass

    def compute_executable_fingerprint(self, node: Any) -> str:
        """
        提取 AST 中所有可執行語意之 Token 指紋（去除 comments、docstrings 與純型別標註）。
        回傳正規化的 token 字串 SHA-256 雜湊值。
        """
        if not node:
            return ""
        import hashlib

        tokens = []
        skip_types = {
            "comment", "line_comment", "block_comment",
            "type_annotation", "type_arguments", "type_parameters",
            "type_parameter", "return_type", "generic_type", "type_alias",
            "omission"
        }

        # 檢查 Python docstring: 如果子樹為 block，且第一個 expression_statement 其子節點為 string
        docstring_nodes = set()
        body_node = node.child_by_field_name("body") if hasattr(node, "child_by_field_name") else None
        target_body = body_node if body_node else node
        if hasattr(target_body, "children") and len(target_body.children) > 0:
            first_stmt = target_body.children[0]
            if first_stmt.type == "expression_statement":
                for c in first_stmt.children:
                    if c.type in ("string", "concatenated_string"):
                        docstring_nodes.add(first_stmt.id)
                        break

        stack = [node]
        while stack:
            curr = stack.pop()
            if curr.id in docstring_nodes:
                continue
            if curr.type in skip_types or "comment" in curr.type:
                continue
            # 檢查父節點是否把當前節點當作 type 標註（例如 Python typed_parameter 的 type 子節點）
            if curr.parent and hasattr(curr.parent, "child_by_field_name"):
                if curr.parent.child_by_field_name("type") == curr:
                    continue

            if not curr.children:
                # 葉節點
                txt = curr.text.decode("utf-8", errors="replace").strip()
                if txt:
                    tokens.append(txt)
            else:
                # 將 children 逆序加入 stack，保證 DFS preorder 走訪
                stack.extend(reversed(curr.children))

        combined = " ".join(tokens)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def _inspect_control_context(self, call_node: Any, enclosing_func_node: Any = None) -> Dict[str, Any]:
        """
        從 call_node 向上走訪 parent 直到 enclosing_func_node，
        檢查該呼叫點是否位於條件分支 (if / switch / match / 三元運算) 或異常處理 (try / catch) 內部，
        或是該函式在此呼叫點之前是否已有 early-return 守衛 (if (...) return)。
        """
        res = {
            "is_conditional": False,
            "guard_type": "NONE",       # "NONE", "IF_BRANCH", "EARLY_RETURN_GUARD", "SHORT_CIRCUIT", "SWITCH_MATCH", "TERNARY", "LOOP"
            "is_error_handled": False,
            "guard_expr": "",
        }
        if not call_node:
            return res

        func_boundary_types = {
            "function_declaration", "function_expression", "arrow_function",
            "method_definition", "function_definition", "func_literal",
            "function_item", "local_function_statement"
        }

        # 1. 檢查直接包裹之祖先節點 (Direct Ancestors)
        curr = call_node.parent
        while curr and curr != enclosing_func_node:
            if curr.type in func_boundary_types and enclosing_func_node is None:
                break

            c_type = curr.type
            if c_type in ("if_statement", "if_expression"):
                res["is_conditional"] = True
                res["guard_type"] = "IF_BRANCH"
                cond = curr.child_by_field_name("condition")
                if cond:
                    res["guard_expr"] = cond.text.decode("utf-8", errors="replace").strip()
            elif c_type in ("switch_statement", "switch_expression", "match_expression", "match_statement"):
                res["is_conditional"] = True
                res["guard_type"] = "SWITCH_MATCH"
            elif c_type in ("conditional_expression", "ternary_expression"):
                res["is_conditional"] = True
                res["guard_type"] = "TERNARY"
            elif c_type in ("binary_expression", "logical_expression"):
                op = curr.child_by_field_name("operator")
                op_text = op.text.decode("utf-8", errors="replace") if op else curr.text.decode("utf-8", errors="replace")
                if any(k in op_text for k in ("&&", "||", "and", "or")):
                    res["is_conditional"] = True
                    res["guard_type"] = "SHORT_CIRCUIT"
            elif c_type in ("for_statement", "while_statement", "for_in_statement", "for_range_loop"):
                res["is_conditional"] = True
                if res["guard_type"] == "NONE":
                    res["guard_type"] = "LOOP"

            if c_type in ("try_statement", "try_expression"):
                res["is_error_handled"] = True

            curr = curr.parent

        # 2. 檢查同一個 block / body 內的 Preceding Sibling Early-Return 守衛
        # 向上找到 call_node 在 block / body 內的直接子語句
        block_types = {"statement_block", "block", "body", "compound_statement", "block_body"}
        stmt = call_node
        while stmt and stmt.parent and stmt.parent.type not in block_types:
            if stmt.parent.type in func_boundary_types:
                break
            stmt = stmt.parent

        if stmt and stmt.parent and stmt.parent.type in block_types:
            parent_block = stmt.parent
            for sibling in parent_block.children:
                if sibling == stmt:
                    break
                if sibling.type in ("if_statement", "if_expression"):
                    if _has_early_exit(sibling):
                        res["is_conditional"] = True
                        res["guard_type"] = "EARLY_RETURN_GUARD"
                        cond = sibling.child_by_field_name("condition")
                        if cond:
                            res["guard_expr"] = cond.text.decode("utf-8", errors="replace").strip()
                        break

        # 3. 檢查鏈式 .catch() 或 Rust ?
        p = call_node.parent
        if p and p.type == "member_expression":
            prop = p.child_by_field_name("property")
            if prop and prop.text.decode("utf-8", errors="replace") in ("catch", "handle_error"):
                res["is_error_handled"] = True
        elif call_node.type == "try_expression":  # Rust ?
            res["is_error_handled"] = True

        return res
