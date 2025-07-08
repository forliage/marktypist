import click
from pathlib import Path
from .main import convert_file

@click.group()
def cli():
    """Marktypist: A powerful converter between Markdown and Typst."""
    pass

@cli.command()
@click.argument(
    'input_file', 
    type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.option(
    '-o', '--output', 
    'output_file', # 在函数中参数名为 output_file
    type=click.Path(dir_okay=False, resolve_path=True), 
    help="Output file path. If omitted, prints to standard output."
)
@click.option(
    '-t', '--to', 
    type=click.Choice(['md', 'typst'], case_sensitive=False), 
    help="Target format. If omitted, it's inferred from the output file extension."
)
def convert(input_file, output_file, to):
    """Converts a file from Markdown to Typst or vice versa."""
    
    input_path = Path(input_file)
    output_path = Path(output_file) if output_file else None

    # TODO: 实现更复杂的格式推断逻辑
    # if not to:
    #     if output_path:
    #         to = output_path.suffix[1:].lower()
    #     else:
    #         # ...

    click.echo(f"Converting {input_path.name}...")

    try:
        # 如果有输出路径，直接调用 convert_file 进行文件到文件的转换
        if output_path:
            convert_file(input_path, output_path)
            click.secho(f"Conversion successful! Output written to {output_path.name}", fg="green")
        else:
            # 如果没有输出路径，调用 convert_file 获取字符串并打印
            result_string = convert_file(input_path, None)
            click.echo(result_string)

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg="red", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()