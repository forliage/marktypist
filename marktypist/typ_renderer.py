from .model import *

class TypstRenderer:
    """
    遍历 UDM 树并将其渲染为 Typst 格式的字符串。
    """
    def render(self, document: Document) -> str:
        # 修正后的渲染入口点：不再对单个元素做特殊处理。
        # 总是访问 Document 节点，让 visit_document 负责正确的连接。
        # .strip() 可以在最后移除可能由顶层块连接产生的前后空白。
        return self._visit(document).strip()

    def _visit(self, node):
        """根据节点的类型，动态调用对应的 visit_xxx 方法"""
        method_name = f"visit_{node.__class__.__name__.lower()}"
        visitor = getattr(self, method_name, self.visit_default)
        return visitor(node)

    def visit_default(self, node):
        raise NotImplementedError(f"No visitor for node type: {node.__class__.__name__}")

    # --- 内联元素访问者 ---
    def _render_inline_content(self, content: List[InlineElement]) -> str:
        return "".join(self._visit(item) for item in content)

    def visit_text(self, node: Text) -> str:
        return node.content

    def visit_bold(self, node: Bold) -> str:
        return f"*{self._render_inline_content(node.content)}*"

    def visit_italic(self, node: Italic) -> str:
        return f"_{self._render_inline_content(node.content)}_"

    def visit_code(self, node: Code) -> str:
        return f"`{node.content}`"

    def visit_link(self, node: Link) -> str:
        return f'#link("{node.url}")[{self._render_inline_content(node.content)}]'
    
    def visit_image(self, node: Image) -> str:
        alt_text = node.alt.replace('"', '\\"')
        return f'#image("{node.src}", alt: "{alt_text}")'

    # --- 块级元素访问者 ---
    def _render_block_content(self, content: List[BlockElement], join_str="\n\n") -> str:
        return join_str.join(self._visit(item) for item in content)

    def visit_document(self, node: Document) -> str:
        # Document 节点负责用两个换行符连接所有顶层块
        return self._render_block_content(node.content, join_str="\n\n")

    def visit_heading(self, node: Heading) -> str:
        # 块级元素自身不带末尾换行
        return f"{'=' * node.level} {self._render_inline_content(node.content)}"

    def visit_paragraph(self, node: Paragraph) -> str:
        # 如果一个段落只包含一个图片，那么它应该只渲染图片，而不是图片被包裹在段落中
        if len(node.content) == 1 and isinstance(node.content[0], Image):
            return self._visit(node.content[0])
        return self._render_inline_content(node.content)

    def visit_unorderedlist(self, node: UnorderedList) -> str:
        items_str = [f"- {self._visit(item)}" for item in node.items]
        return "\n".join(items_str)

    def visit_orderedlist(self, node: OrderedList) -> str:
        items_str = [f"+ {self._visit(item)}" for item in node.items]
        return "\n".join(items_str)

    def visit_listitem(self, node: ListItem) -> str:
        if node.content and isinstance(node.content[0], Paragraph):
             return self._render_inline_content(node.content[0].content)
        return self._render_block_content(node.content, join_str="\n  ")

    def visit_codeblock(self, node: CodeBlock) -> str:
        return f"```{node.language}\n{node.content}\n```"
    
    def visit_blockquote(self, node: BlockQuote) -> str:
        inner_content = self._render_block_content(node.content)
        return f"#quote[{inner_content}]"

    # --- 表格渲染器 ---
    def visit_table(self, node: Table) -> str:
        if not node.header.cells:
            return ""

        num_columns = len(node.header.cells)
        columns_def = f"  columns: ({', '.join(['auto'] * num_columns)}),\n"

        header_cells = [f"[*{(self._visit(cell))}*]" for cell in node.header.cells]
        header_line = "  " + ", ".join(header_cells) + ",\n"
        
        body_lines = []
        for row in node.rows:
            row_cells = []
            for cell in row.cells:
                cell_content_str = self._visit(cell)
                is_pure_text = len(cell.content) == 1 and isinstance(cell.content[0], Text)
                
                if is_pure_text:
                    escaped_content = cell_content_str.replace('\\', '\\\\').replace('"', '\\"')
                    row_cells.append(f'"{escaped_content}"')
                else:
                    row_cells.append(cell_content_str)
            
            while len(row_cells) < num_columns:
                row_cells.append('""')
            
            body_lines.append("  " + ", ".join(row_cells) + ",")
        
        body_str = "\n".join(body_lines) + "\n" if body_lines else ""

        return f"#table(\n{columns_def}{header_line}{body_str})"

    def visit_tablecell(self, node: TableCell) -> str:
        return self._render_inline_content(node.content)