from .model import *

class TypstRenderer:
    """
    遍历 UDM 树并将其渲染为 Typst 格式的字符串。
    """
    def render(self, document: Document) -> str:
        if len(document.content) == 1:
            return self._visit(document.content[0])
        return self._visit(document).strip()

    def _visit(self, node):
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
        # 正确：用 * 包裹
        return f"*{self._render_inline_content(node.content)}*"

    def visit_italic(self, node: Italic) -> str:
        # 关键修正：必须用 _ 包裹
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
        return self._render_block_content(node.content, join_str="\n\n")

    def visit_heading(self, node: Heading) -> str:
        return f"{'=' * node.level} {self._render_inline_content(node.content)}"

    def visit_paragraph(self, node: Paragraph) -> str:
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