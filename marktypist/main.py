from pathlib import Path
from .md_parser import MarkdownParser
from .typ_parser import TypstParser
from .md_renderer import MarkdownRenderer
from .typ_renderer import TypstRenderer

def convert_md_to_typ(markdown_text: str) -> str:
    parser = MarkdownParser()
    renderer = TypstRenderer()
    document_model = parser.parse(markdown_text)
    typst_output = renderer.render(document_model)
    return typst_output

# 新增：Typst -> MD 的转换函数
def convert_typ_to_md(typst_text: str) -> str:
    parser = TypstParser()
    renderer = MarkdownRenderer()
    document_model = parser.parse(typst_text)
    md_output = renderer.render(document_model)
    return md_output

def convert_file(input_path: Path, output_path: Path = None):
    source_text = input_path.read_text(encoding="utf-8-sig")
    
    # 扩展逻辑以处理 Typst 输入
    if input_path.suffix.lower() == ".md":
        converted_text = convert_md_to_typ(source_text)
    elif input_path.suffix.lower() == ".typ":
        converted_text = convert_typ_to_md(source_text)
    else:
        raise ValueError(f"Unsupported input file format: {input_path.suffix}")
            
    if output_path:
        output_path.write_text(converted_text, encoding="utf-8")
    else:
        return converted_text