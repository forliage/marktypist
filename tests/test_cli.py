import pytest
from click.testing import CliRunner
from pathlib import Path

from marktypist.cli import cli

# 使用 pytest 的 tmp_path fixture 来创建一个临时目录进行测试
def test_md_to_typ_conversion_cli(tmp_path: Path):
    """测试 'marktypist convert file.md -o file.typ' 命令"""
    runner = CliRunner()
    
    # 1. 准备输入文件
    input_md_file = tmp_path / "test.md"
    input_md_file.write_text("# Hello\n\nThis is a test.")
    
    # 2. 准备输出文件路径
    output_typ_file = tmp_path / "test.typ"
    
    # 3. 运行命令行
    result = runner.invoke(cli, [
        "convert",
        str(input_md_file),
        "--output",
        str(output_typ_file)
    ])
    
    # 4. 验证结果
    assert result.exit_code == 0, f"CLI exited with error: {result.output}"
    assert "Converting" in result.output
    assert "successful" in result.output
    
    # 5. 验证输出文件内容
    assert output_typ_file.exists()
    expected_content = "= Hello\n\nThis is a test."
    assert output_typ_file.read_text().strip() == expected_content

def test_conversion_to_stdout(tmp_path: Path):
    """测试转换并输出到标准输出 (stdout)"""
    runner = CliRunner()
    
    input_md_file = tmp_path / "test.md"
    input_md_file.write_text("**Bold** text.")
    
    # 不使用 -o 选项，结果应该打印到 stdout
    result = runner.invoke(cli, ["convert", str(input_md_file)])
    
    assert result.exit_code == 0
    
    # 结果应该在 result.output 中
    expected_content = "*Bold* text."
    # 我们要去掉命令本身的回显信息，只检查核心输出
    assert expected_content in result.output

def test_input_file_not_found(tmp_path: Path):
    """测试输入文件不存在的情况"""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["convert", "non_existent_file.md"])
    
    # Click 会自动处理文件不存在的错误
    assert result.exit_code != 0
    assert "Error: Invalid value for 'INPUT_FILE'" in result.output
    assert "does not exist" in result.output