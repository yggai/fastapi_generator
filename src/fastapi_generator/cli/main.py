"""
FastAPI Generator 命令行工具
"""
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from fastapi_generator.core.project_creator import create_project as create_project_func
from fastapi_generator.generators.api_generator import generate_api as generate_api_func
from fastapi_generator.generators.model_generator import generate_model as generate_model_func
from fastapi_generator.generators.service_generator import generate_service as generate_service_func
from fastapi_generator.generators.migration_generator import generate_migration as generate_migration_func

app = typer.Typer(help="FastAPI Generator - 快速生成FastAPI项目和组件")
console = Console()

@app.command("create")
def create_project(
    project_name: str,
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="输出目录，默认为当前目录"),
    template: str = typer.Option("standard", "--template", "-t", help="项目模板: basic, standard, enterprise")
):
    """创建一个新的FastAPI项目"""
    # 显示创建信息
    console.print(f"创建项目: {project_name}")
    console.print(f"模板: {template}")
    
    # 设置默认输出目录为当前目录
    output_dir = output or Path.cwd()
    
    try:
        # 调用项目创建函数
        project_path = create_project_func(
            project_name=project_name,
            output_dir=output_dir,
            template=template
        )
        console.print(f"[bold green]项目创建成功![/bold green] 路径: \n{project_path}")
    except Exception as e:
        console.print(f"[bold red]错误: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

@app.command("generate")
def generate_component(
    component_type: str = typer.Argument(..., help="组件类型: api, model, service, migration"),
    name: str = typer.Argument(..., help="组件名称"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="输出目录，默认为当前目录")
):
    """生成FastAPI项目组件"""
    # 设置默认输出目录为当前目录
    output_dir = output or Path.cwd()
    
    try:
        if component_type == "api":
            console.print(f"生成API: {name}")
            api_file = generate_api_func(name, output_dir)
            console.print(f"[bold green]API生成成功![/bold green] 文件: \n{api_file}")
            
        elif component_type == "model":
            console.print(f"生成模型: {name}")
            model_file = generate_model_func(name, output_dir)
            console.print(f"[bold green]模型生成成功![/bold green] 文件: \n{model_file}")
            
        elif component_type == "service":
            console.print(f"生成服务: {name}")
            service_file = generate_service_func(name, output_dir)
            console.print(f"[bold green]服务生成成功![/bold green] 文件: \n{service_file}")
            
        elif component_type == "migration":
            console.print(f"生成数据库迁移")
            migrations_dir = generate_migration_func(output_dir)
            console.print(f"[bold green]数据库迁移生成成功![/bold green] 目录: \n{migrations_dir}")
            
        else:
            console.print(f"[bold red]错误: 不支持的组件类型 '{component_type}'[/bold red]")
            console.print("支持的组件类型: api, model, service, migration")
            raise typer.Exit(code=1)
            
    except Exception as e:
        console.print(f"[bold red]错误: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

def main():
    """主函数入口"""
    app()

if __name__ == "__main__":
    main() 