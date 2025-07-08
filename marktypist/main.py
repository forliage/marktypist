from .md_parser import MarkdownParser
from .typ_renderer import TypstRenderer

def convert_md_to_typ(markdown_text: str) -> str:
    """
    将 Markdown 文本转换为 Typst 文本的核心函数。
    它协调解析器和渲染器的工作。
    """
    # 1. 实例化解析器和渲染器
    parser = MarkdownParser()
    renderer = TypstRenderer()
    
    # 2. 解析 Markdown 文本，得到我们的 UDM 对象
    document_model = parser.parse(markdown_text)
    
    # 3. 使用渲染器将 UDM 对象转换为 Typst 字符串
    typst_output = renderer.render(document_model)
    
    return typst_output