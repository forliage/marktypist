import pytest
from pathlib import Path

from marktypist.main import convert_md_to_typ

# 定义测试数据目录
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# --- 使用 parametrize 的第一个强大测试 ---

MD_TO_TYP_BASIC_CASES = [
    # --- 已有测试 ---
    ("h1", "# 标题1", "= 标题1"),
    ("h2", "## 标题2", "== 标题2"),
    ("paragraph", "这是一个简单的段落。", "这是一个简单的段落。"),
    ("bold", "这是 **粗体** 文字。", "这是 *粗体* 文字。"),
    ("italic", "这是 *斜体* 文字。", "这是 _斜体_ 文字。"),
    ("unordered_list", "- item 1\n- item 2", "- item 1\n- item 2"),
    ("inline_code", "使用 `print()` 函数。", "使用 `print()` 函数。"),
    (
        "code_block",
        "```python\ndef hello():\n    print(\"Hello\")\n```",
        "```python\ndef hello():\n    print(\"Hello\")\n```"
    ),
    ("blockquote", "> 这是一个引用。", "#quote[这是一个引用。]"),
    (
        "nested_blockquote",
        "> 第一层引用。\n> > 第二层引用。",
        "#quote[第一层引用。\n\n#quote[第二层引用。]]"
    ),
    # --- 修正后的测试用例 ---
    ("ordered_list", "1. 第一项\n2. 第二项", "+ 第一项\n+ 第二项"),
    # 修正: 只测试链接本身
    ("link", "[Typst官网](https://typst.app)", '#link("https://typst.app")[Typst官网]'),
    # 修正: 只测试图片本身
    ("image", "![Typst logo](logo.png)", '#image("logo.png", alt: "Typst logo")'),

    # --- 新增测试用例 ---
    (
        "table",
        # Markdown GFM Table
        "| 命令 | 描述 |\n"
        "| :--- | :--- |\n"
        "| `git status` | 列出所有新的或修改的文件 |\n"
        "| `git diff` | 显示文件差异 |",
        # Expected Typst Table
        '#table(\n'
        '  columns: (auto, auto),\n'
        '  [*命令*], [*描述*],\n'
        '  `git status`, "列出所有新的或修改的文件",\n'
        '  `git diff`, "显示文件差异",\n'
        ')'
    ),
]

@pytest.mark.parametrize(
    "test_id, markdown_input, expected_typst_output",
    MD_TO_TYP_BASIC_CASES,
    ids=[case[0] for case in MD_TO_TYP_BASIC_CASES]
)
def test_basic_md_to_typ_conversion(test_id, markdown_input, expected_typst_output):
    actual_output = convert_md_to_typ(markdown_input).strip()
    assert actual_output == expected_typst_output

# ... (test_full_file_md_to_typ_conversion 保持不变)
def test_full_file_md_to_typ_conversion():
    md_content = (FIXTURES_DIR / "basic.md").read_text(encoding="utf-8")
    expected_typst_content = (FIXTURES_DIR / "basic.typ").read_text(encoding="utf-8")
    actual_output = convert_md_to_typ(md_content)
    assert actual_output.strip() == expected_typst_content.strip()