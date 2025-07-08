from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from typing import List, Sequence

# 导入所有需要的模型
from .model import (
    Document, BlockElement, InlineElement, Text, Bold, Italic, Code, Link, Image,
    Heading, Paragraph, UnorderedList, OrderedList, ListItem, CodeBlock, BlockQuote,
    Table, TableRow, TableCell
)

class UdmRenderer(RendererProtocol):
    """
    一个自定义的 markdown-it 渲染器，它不输出字符串，
    而是构建我们的通用文档模型 (UDM) 对象。
    """
    def __init__(self):
        self.stack: List = [Document(content=[])]
        self.in_header = False  # 状态变量，用于区分表格的 a a和 a

    def render(self, tokens: Sequence[Token]) -> Document:
        for token in tokens:
            method = getattr(self, token.type, self.render_default)
            method(token)
        return self.stack[0]

    def render_default(self, token: Token):
        pass
        
    def _push(self, node):
        """将一个新节点压入栈，并附加到其父节点上"""
        parent = self.stack[-1]
        
        # 根据父节点类型决定如何附加子节点
        if isinstance(parent, TableRow):
            parent.cells.append(node)
        elif isinstance(parent, Table):
            if self.in_header:
                parent.header = node
            else:
                parent.rows.append(node)
        elif hasattr(parent, 'content'):
            parent.content.append(node)
        elif hasattr(parent, 'items'):
            parent.items.append(node)
            
        self.stack.append(node)

    def _pop(self):
        """将节点从栈中弹出"""
        return self.stack.pop()

    # --- 块级元素处理器 ---
    def heading_open(self, token: Token): self._push(Heading(level=int(token.tag[1]), content=[]))
    def heading_close(self, token: Token): self._pop()

    def paragraph_open(self, token: Token): self._push(Paragraph(content=[]))
    def paragraph_close(self, token: Token): self._pop()

    def bullet_list_open(self, token: Token): self._push(UnorderedList(items=[]))
    def bullet_list_close(self, token: Token): self._pop()
    
    def ordered_list_open(self, token: Token):
        start = int(token.meta.get('start', 1))
        self._push(OrderedList(start=start, items=[]))
    def ordered_list_close(self, token: Token): self._pop()

    def list_item_open(self, token: Token): self._push(ListItem(content=[]))
    def list_item_close(self, token: Token): self._pop()
    
    def blockquote_open(self, token: Token): self._push(BlockQuote(content=[]))
    def blockquote_close(self, token: Token): self._pop()

    def fence(self, token: Token):
        lang = token.info.split()[0] if token.info else ""
        code_block = CodeBlock(language=lang, content=token.content.strip())
        self.stack[-1].content.append(code_block)
        
    # --- 表格处理器 ---
    def table_open(self, token: Token):
        self._push(Table(header=TableRow(cells=[]), rows=[], align=[]))
    def table_close(self, token: Token): self._pop()

    def thead_open(self, token: Token): self.in_header = True
    def thead_close(self, token: Token): self.in_header = False
        
    def tbody_open(self, token: Token): pass
    def tbody_close(self, token: Token): pass

    def tr_open(self, token: Token): self._push(TableRow(cells=[]))
    def tr_close(self, token: Token): self._pop()

    def th_open(self, token: Token): self._push(TableCell(content=[]))
    def th_close(self, token: Token): self._pop()

    def td_open(self, token: Token): self._push(TableCell(content=[]))
    def td_close(self, token: Token): self._pop()
        
    # --- 内联元素处理器 ---
    def inline(self, token: Token):
        for child in token.children:
            method = getattr(self, child.type, self.render_default)
            method(child)

    def text(self, token: Token): self.stack[-1].content.append(Text(content=token.content))

    def strong_open(self, token: Token): self._push(Bold(content=[]))
    def strong_close(self, token: Token): self._pop()
        
    def em_open(self, token: Token): self._push(Italic(content=[]))
    def em_close(self, token: Token): self._pop()

    def code_inline(self, token: Token): self.stack[-1].content.append(Code(content=token.content))

    def link_open(self, token: Token):
        url = token.attrs['href']
        self._push(Link(url=url, content=[]))
    def link_close(self, token: Token): self._pop()
        
    def image(self, token: Token):
        src = token.attrs['src']
        alt = token.content
        img_node = Image(src=src, alt=alt)
        parent = self.stack[-1]
        if hasattr(parent, 'content'):
            parent.content.append(img_node)


class MarkdownParser:
    def __init__(self):
        # 使用 "gfm-like" 预设，它包含了表格等功能
        self.md = MarkdownIt("gfm-like")

    def parse(self, markdown_text: str) -> Document:
        tokens = self.md.parse(markdown_text)
        renderer = UdmRenderer()
        doc = renderer.render(tokens)
        
        # 修复一个可能的解析问题：有时根节点会错误地嵌套一层
        if len(doc.content) == 1 and isinstance(doc.content[0], Document):
            return doc.content[0]
        return doc