from pathlib import Path
from .md_parser import MarkdownParser
from .typ_renderer import TypstRenderer

def convert_md_to_typ(markdown_text: str) -> str:
    """
    将 Markdown 文本字符串转换为 Typst 文本字符串的核心函数。
    """
    parser = MarkdownParser()
    renderer = TypstRenderer()
    document_model = parser.parse(markdown_text)
    typst_output = renderer.render(document_model)
    return typst_output

def convert_file(input_path: Path, output_path: Path = None):
    """
    读取输入文件，进行格式转换，并写入输出文件或返回字符串。
    """
    # 使用 'utf-8-sig' 来处理可能由 Windows 生成的带 BOM 的文件
    source_text = input_path.read_text(encoding="utf-8-sig")
    
    if input_path.suffix.lower() == ".md":
        converted_text = convert_md_to_typ(source_text)
    else:
        raise ValueError(f"Unsupported input file format: {input_path.suffix}")
            
    if output_path:
        output_path.write_text(converted_text, encoding="utf-8")
    else:
        return converted_text