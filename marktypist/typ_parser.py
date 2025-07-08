# marktypist/typ_parser.py

import re
from typing import List, Union, Optional

from .model import (
    Document, BlockElement, InlineElement, Text, Bold, Italic,
    Heading, Paragraph, UnorderedList, OrderedList, ListItem
)

class TypstParser:
    def parse(self, typst_text: str) -> Document:
        blocks: List[BlockElement] = []
        
        # 将输入文本按行分割，并处理 Typst 的块级和内联级模式
        lines = typst_text.splitlines()
        
        current_paragraph: Optional[Paragraph] = None
        current_list: Optional[Union[UnorderedList, OrderedList]] = None
        
        for line in lines:
            stripped_line = line.strip()

            # 处理空行
            if not stripped_line:
                if current_paragraph is not None:
                    # 结束当前段落，如果存在
                    current_paragraph = None
                if current_list is not None:
                    # 结束当前列表，如果存在 (简单处理，不支持列表项内有多行或复杂嵌套)
                    current_list = None
                continue # 空行不生成块

            # 检查标题
            match_heading = re.match(r'(=+)\s*(.*)', stripped_line)
            if match_heading:
                level = len(match_heading.group(1))
                content_text = match_heading.group(2)
                inline_elements = self._parse_inline(content_text)
                blocks.append(Heading(level=level, content=inline_elements))
                current_paragraph = None
                current_list = None
                continue
            
            # 检查无序列表 (Typst 使用 - )
            match_unordered_list = re.match(r'-\s*(.*)', stripped_line)
            if match_unordered_list:
                item_content_text = match_unordered_list.group(1)
                inline_elements = self._parse_inline(item_content_text)
                
                # 如果当前没有列表，则创建一个新的无序列表
                if current_list is None or not isinstance(current_list, UnorderedList):
                    current_list = UnorderedList(items=[])
                    blocks.append(current_list)
                
                # 添加列表项，其内容是一个 Paragraph
                current_list.items.append(ListItem(content=[Paragraph(content=inline_elements)]))
                current_paragraph = None # 列表项不应是段落的延续
                continue
            
            # 处理段落
            inline_elements = self._parse_inline(stripped_line)
            if current_paragraph is None:
                current_paragraph = Paragraph(content=inline_elements)
                blocks.append(current_paragraph)
            else:
                # 续接现有段落
                current_paragraph.content.extend(inline_elements)
            
            current_list = None # 段落不是列表的延续

        return Document(content=blocks)

    def _parse_inline(self, text: str) -> List[InlineElement]:
        """
        使用正则表达式解析内联样式：粗体和斜体，以及粗斜体。
        """
        result: List[InlineElement] = []
        
        # Typst: *bold*, _italic_, *_bold_italic_*
        # Markdown: **bold**, *italic*, ***bold_italic***

        # 使用一个更精确的正则表达式，按照优先级从左到右匹配
        # 1. Typst 粗斜体模式: *_..._*
        # 2. Typst 粗体模式: *...* (确保不是粗斜体的一部分)
        # 3. Typst 斜体模式: _..._ (确保不是粗斜体的一部分)
        # 4. 普通文本
        
        # 捕获组: (粗斜体捕获1)(粗体捕获2)(斜体捕获3)
        # 注意：这里的正则需要非常精确，确保边界条件。
        # 对于嵌套，简单的 regex 很难完全实现，这里仅能处理直接模式。
        # 复杂模式如 "这是 *_粗体*斜体_*" 将无法被此简陋解析器处理。
        
        # 正则表达式分解：
        # ( \*_ ( .*? ) _\* ) : 匹配 *_TEXT_*。Group 1 是完整匹配，Group 2 是内部 TEXT
        # | ( \* ( .*? ) \* ) : 匹配 *TEXT*。Group 3 是完整匹配，Group 4 是内部 TEXT
        # | ( _ ( .*? ) _ )   : 匹配 _TEXT_。Group 5 是完整匹配，Group 6 是内部 TEXT
        # | ( [^_*]+ )        : 匹配任何非 *, _, 空格的字符 (普通文本)
        # | ( . )             : 匹配单个字符，作为回退（用于处理特殊字符）
        
        # Typst 的粗斜体是 `*_content_*`
        # Typst 的粗体是 `*content*`
        # Typst 的斜体是 `_content_`
        
        # 确保 `*` 和 `_` 只有在其作为分隔符时才被匹配，并且要处理嵌套和歧义
        # 例如，`*a _b_ c*` 应该解析为 Bold(Text("a "), Italic(Text("b")), Text(" c"))
        # 这对于纯 regex 是一个巨大的挑战。
        # 鉴于我们测试用例是简单的，我们可以使用一个更直接的模式：
        
        # 简化的内联正则表达式，匹配单个标签
        # 确保它不吞噬内部的换行符
        parts = re.split(r'(\*_.+?_\*|\*.+?\*|_.+?_)', text)
        
        for part in parts:
            if not part:
                continue
            
            # 粗斜体: Typst *_..._*
            match_bold_italic = re.match(r'\*_(.+?)_\*', part)
            if match_bold_italic:
                inner = self._parse_inline(match_bold_italic.group(1)) # 递归解析内部
                result.append(Italic(content=[Bold(content=inner)]))
                continue
            
            # 粗体: Typst *...*
            match_bold = re.match(r'\*(.+?)\*', part)
            if match_bold:
                inner = self._parse_inline(match_bold.group(1)) # 递归解析内部
                result.append(Bold(content=inner))
                continue
            
            # 斜体: Typst _..._
            match_italic = re.match(r'_(.+?)_', part)
            if match_italic:
                inner = self._parse_inline(match_italic.group(1)) # 递归解析内部
                result.append(Italic(content=inner))
                continue
            
            # 普通文本
            result.append(Text(content=part))

        # 确保对于纯文本输入也能正确处理
        if not result and text: # 如果没有匹配到任何样式，整个就是文本
            result.append(Text(content=text))

        return result