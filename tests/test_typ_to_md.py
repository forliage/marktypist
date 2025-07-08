import pytest
from pathlib import Path

# 导入一个新的转换函数，它还不存在，但这是我们的目标
from marktypist.main import convert_typ_to_md

# 定义测试数据目录
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# --- 定义一组基本的 Typst -> MD 测试用例 ---
TYP_TO_MD_BASIC_CASES = [
    ("h1", "= 标题1", "# 标题1"),
    ("h2", "== 标题2", "## 标题2"),
    ("paragraph", "这是一个段落。", "这是一个段落。"),
    ("bold", "这是 *粗体* 文字。", "这是 **粗体** 文字。"),
    ("italic", "这是 _斜体_ 文字。", "这是 *斜体* 文字。"),
    # 注意 Typst 的粗斜体是 *_..._*
    ("bold_italic", "这是 *_粗斜体_* 文字。", "这是 ***粗斜体*** 文字。"),
]

@pytest.mark.parametrize(
    "test_id, typst_input, expected_md_output",
    TYP_TO_MD_BASIC_CASES,
    ids=[case[0] for case in TYP_TO_MD_BASIC_CASES]
)
def test_basic_typ_to_md_conversion(test_id, typst_input, expected_md_output):
    """测试最基本的 Typst 到 Markdown 的转换功能。"""
    actual_output = convert_typ_to_md(typst_input).strip()
    assert actual_output == expected_md_output

def test_full_file_typ_to_md_conversion():
    """测试从文件读取并进行 Typst -> MD 转换的端到端场景。"""
    typ_content = (FIXTURES_DIR / "basic.typ").read_text(encoding="utf-8")
    expected_md_content = (FIXTURES_DIR / "basic.md").read_text(encoding="utf-8")

    actual_output = convert_typ_to_md(typ_content)
    
    # 为了比较，我们可以统一换行符并去除首尾空白
    normalized_actual = actual_output.replace('\r\n', '\n').strip()
    normalized_expected = expected_md_content.replace('\r\n', '\n').strip()
    
    assert normalized_actual == normalized_expected