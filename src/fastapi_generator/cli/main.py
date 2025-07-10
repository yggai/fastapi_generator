"""
FastAPI Generator CLI 主入口
"""
import typer
from typing import Optional
from rich.console import Console
import sys
from pathlib import Path
from fastapi_generator import __version__

# 初始化CLI应用
app = typer.Typer(
    name="fg",
    help="FastAPI项目代码生成工具",
    add_completion=False,
)

# 初始化rich控制台对象
console = Console()

@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        False, "--version", "-V", help="显示版本信息并退出"
    )
):
    """
    FastAPI Generator - 快速生成FastAPI项目代码
    """
    if version:
        console.print(f"FastAPI Generator v{__version__}")
        raise typer.Exit()

@app.command("create")
def create_project(
    project_name: str = typer.Argument(..., help="项目名称"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="输出目录，默认为当前目录"
    ),
    template: str = typer.Option(
        "standard", "--template", "-t", help="项目模板: basic, standard, enterprise"
    ),
):
    """
    创建一个新的FastAPI项目
    """
    from fastapi_generator.core.project_creator import create_project as do_create
    
    console.print(f"[bold green]创建项目: {project_name}[/bold green]")
    console.print(f"模板: {template}")
    
    try:
        project_path = do_create(
            project_name=project_name, 
            output_dir=output_dir, 
            template=template
        )
        console.print(f"[bold green]✓ 项目创建成功![/bold green] 路径: {project_path}")
    except Exception as e:
        console.print(f"[bold red]错误: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

@app.command("generate")
def generate_component(
    component_type: str = typer.Argument(..., help="组件类型: api, model, service, migration"),
    name: str = typer.Argument(..., help="组件名称"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="输出目录，默认为当前目录下对应的模块目录"
    ),
):
    """
    生成项目组件(API、模型、服务、数据库迁移等)
    """
    console.print(f"[bold green]生成{component_type}: {name}[/bold green]")
    
    try:
        if component_type == "api":
            from fastapi_generator.generators.api_generator import generate_api
            generate_api(name=name, output_dir=output_dir)
        elif component_type == "model":
            from fastapi_generator.generators.model_generator import generate_model
            generate_model(name=name, output_dir=output_dir)
        elif component_type == "service":
            from fastapi_generator.generators.service_generator import generate_service
            generate_service(name=name, output_dir=output_dir)
        elif component_type == "migration":
            from fastapi_generator.generators.migration_generator import generate_migration
            generate_migration(output_dir=output_dir)
            console.print(f"[bold green]✓ 数据库迁移配置生成成功![/bold green]")
            return
        else:
            console.print(f"[bold red]错误: 未知的组件类型 '{component_type}'[/bold red]")
            console.print("可用的组件类型: api, model, service, migration")
            raise typer.Exit(code=1)
            
        console.print(f"[bold green]✓ {component_type}生成成功![/bold green]")
    except Exception as e:
        console.print(f"[bold red]错误: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

@app.command("init-migration")
def init_migration(
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="输出目录，默认为当前项目根目录"
    ),
):
    """
    初始化数据库迁移配置
    """
    from fastapi_generator.generators.migration_generator import generate_migration
    
    console.print("[bold green]初始化数据库迁移配置[/bold green]")
    
    try:
        migrations_dir = generate_migration(output_dir=output_dir)
        console.print(f"[bold green]✓ 数据库迁移配置初始化成功![/bold green] 路径: {migrations_dir}")
    except Exception as e:
        console.print(f"[bold red]错误: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 