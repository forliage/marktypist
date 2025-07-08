from dataclasses import dataclass, field
from typing import List, Union

# --- 内联元素 (Inline Elements) ---

@dataclass
class Text: content: str
@dataclass
class Bold: content: List['InlineElement']
@dataclass
class Italic: content: List['InlineElement']
@dataclass
class Code: content: str

@dataclass
class Link: # 新增：链接
    url: str
    content: List['InlineElement']

@dataclass
class TableCell:
    # 单元格内容可以是丰富的内联元素
    content: List['InlineElement']
    # is_header 标志在解析时可能有用，但Typst渲染时有自己的语法
    is_header: bool = False

@dataclass
class TableRow:
    cells: List[TableCell]

@dataclass
class Table:
    header: TableRow
    # 表格对齐信息，暂时可以不用，但先定义出来
    align: List[str]
    rows: List[TableRow]

# 图片在 Markdown 中是内联元素，但在 Typst 中更像块级元素。
# 我们将其定义为可以在任何地方出现的通用元素，但在模型中先归为块级。
@dataclass
class Image: # 新增：图片
    src: str
    alt: str

# 更新 InlineElement 类型别名
InlineElement = Union[Text, Bold, Italic, Code, Link]

# --- 块级元素 (Block Elements) ---

@dataclass
class Paragraph: content: List[InlineElement]
@dataclass
class Heading:
    level: int
    content: List[InlineElement]

@dataclass
class ListItem: content: List['BlockElement']
@dataclass
class UnorderedList: items: List[ListItem]

@dataclass
class OrderedList: # 新增：有序列表
    start: int
    items: List[ListItem]

@dataclass
class CodeBlock:
    language: str
    content: str

@dataclass
class BlockQuote: content: List['BlockElement']

InlineElement = Union[Text, Bold, Italic, Code, Link, Image]
BlockElement = Union[Paragraph, Heading, UnorderedList, OrderedList, CodeBlock, BlockQuote, Table] # Table 是块级元素

# --- 文档根节点 ---
@dataclass
class Document: content: List[BlockElement]