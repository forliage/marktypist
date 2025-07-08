# marktypist/md_renderer.py

from .model import *
from typing import List

class MarkdownRenderer:
    """
    遍历 UDM 树并将其渲染为 Markdown 格式的字符串。
    """
    def render(self, document: Document) -> str:
        return self._visit(document).strip()

    def _visit(self, node):
        # 核心修正：移除了多余的 .__name__
        method_name = f"visit_{node.__class__.__name__.lower()}"
        visitor = getattr(self, method_name, self.visit_default)
        return visitor(node)

    def visit_default(self, node):
        # 如果遇到未知的节点类型，抛出 NotImplementedError
        raise NotImplementedError(f"No visitor for node type: {node.__class__.__name__} ({node})")

    def _render_inline_content(self, content: List[InlineElement]) -> str:
        return "".join(self._visit(item) for item in content)

    def visit_text(self, node: Text) -> str: return node.content
    
    def visit_bold(self, node: Bold) -> str:
        # Typst 的粗斜体 *_..._* 解析为 Italic(Bold(...))
        # 所以，Bold 节点不会是粗斜体的顶层，这里只处理纯 Bold
        return f"**{self._render_inline_content(node.content)}**"

    def visit_italic(self, node: Italic) -> str:
        # 关键修复：处理 Typst 解析器生成的 Italic(Bold(...)) 粗斜体
        if len(node.content) == 1 and isinstance(node.content[0], Bold):
            bold_node = node.content[0]
            # 渲染成 Markdown 的粗斜体 ***...***
            return f"***{self._render_inline_content(bold_node.content)}***"
        # 否则，是纯斜体
        return f"*{self._render_inline_content(node.content)}*"

    def visit_document(self, node: Document) -> str:
        # 块与块之间用两个换行符分隔
        return "\n\n".join(self._visit(item) for item in node.content)

    def visit_heading(self, node: Heading) -> str:
        return f"{'#' * node.level} {self._render_inline_content(node.content)}"

    def visit_paragraph(self, node: Paragraph) -> str:
        return self._render_inline_content(node.content)

    # --- 新增列表渲染器 ---
    def visit_unorderedlist(self, node: UnorderedList) -> str:
        # 列表项之间用换行符分隔
        items_str = "\n".join(self._visit(item) for item in node.items)
        return items_str

    def visit_listitem(self, node: ListItem) -> str:
        # Markdown 列表项以 '- ' 开头
        # 列表项内容可以是段落，或者其他块
        item_content_lines = []
        for block_elem in node.content:
            # 渲染列表项内部的块级元素
            block_output = self._visit(block_elem)
            item_content_lines.append(block_output)
        
        # 首行加 '- '，后续行缩进
        first_line = f"- {item_content_lines[0]}" if item_content_lines else "- "
        
        remaining_lines = []
        if len(item_content_lines) > 1:
            for line in item_content_lines[1:]:
                # 对于多行内容，每行前面加4个空格（CommonMark 列表项缩进）
                remaining_lines.append(f"    {line}")
        
        return first_line + ("\n" + "\n".join(remaining_lines) if remaining_lines else "")