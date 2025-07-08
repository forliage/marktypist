# marktypist/model.py

from dataclasses import dataclass, field
from typing import List, Union

# --- 内联元素 (Inline Elements) ---

@dataclass
class Text:
    content: str

@dataclass
class Bold:
    content: List['InlineElement']

@dataclass
class Italic:
    content: List['InlineElement']

@dataclass
class Code:
    content: str

@dataclass
class Link:
    url: str
    content: List['InlineElement']

@dataclass
class Image:
    src: str
    alt: str

# 更新 InlineElement 类型别名
InlineElement = Union[Text, Bold, Italic, Code, Link, Image]

# --- 表格专用结构 (重新添加) ---
@dataclass
class TableCell:
    content: List[InlineElement]

@dataclass
class TableRow:
    cells: List[TableCell]

@dataclass
class Table:
    header: TableRow
    align: List[str] # 暂时不用，但保留字段
    rows: List[TableRow]

# --- 块级元素 (Block Elements) ---

@dataclass
class Paragraph:
    content: List[InlineElement]

@dataclass
class Heading:
    level: int
    content: List[InlineElement]

@dataclass
class ListItem:
    content: List['BlockElement'] # 列表项内容可以是块级元素

@dataclass
class UnorderedList:
    items: List[ListItem]

@dataclass
class OrderedList:
    start: int
    items: List[ListItem]

@dataclass
class CodeBlock:
    language: str
    content: str

@dataclass
class BlockQuote:
    content: List['BlockElement']

# 更新 BlockElement 类型别名，重新包含 Table
BlockElement = Union[Paragraph, Heading, UnorderedList, OrderedList, CodeBlock, BlockQuote, Table]

# --- 文档根节点 ---
@dataclass
class Document:
    content: List[BlockElement]