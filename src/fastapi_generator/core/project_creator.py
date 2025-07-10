"""
项目创建器核心功能
"""
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import re
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi_generator.utils.path_utils import ensure_dir_exists, get_templates_dir
from fastapi_generator.utils.string_utils import to_snake_case, to_pascal_case, to_kebab_case

# 定义可用的项目模板
AVAILABLE_TEMPLATES = ["basic", "standard", "enterprise"]

def validate_project_name(project_name: str) -> str:
    """
    验证并转换项目名称为有效的Python包名
    """
    # 转换为蛇形命名法
    valid_name = to_snake_case(project_name)
    
    # 确保首字符是字母或下划线
    if not valid_name[0].isalpha() and valid_name[0] != '_':
        valid_name = f"app_{valid_name}"
    
    # 替换任何非法字符
    valid_name = re.sub(r'[^a-zA-Z0-9_]', '_', valid_name)
    
    return valid_name

def create_project(
    project_name: str, 
    output_dir: Optional[Path] = None, 
    template: str = "standard"
) -> Path:
    """
    创建一个新的FastAPI项目
    
    Args:
        project_name: 项目名称
        output_dir: 输出目录，默认为当前目录
        template: 项目模板类型
        
    Returns:
        项目路径
    """
    # 验证模板类型
    if template not in AVAILABLE_TEMPLATES:
        raise ValueError(f"无效的模板类型: {template}。可用的模板: {', '.join(AVAILABLE_TEMPLATES)}")
    
    # 验证并转换项目名称
    valid_project_name = validate_project_name(project_name)
    display_name = project_name  # 用于显示的原始名称
    
    # 确定输出目录
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
    
    # 创建项目目录
    project_dir = output_dir / valid_project_name
    if project_dir.exists():
        raise FileExistsError(f"目录已存在: {project_dir}")
    
    # 获取模板目录
    templates_dir = get_templates_dir() / "project" / template
    if not templates_dir.exists():
        raise ValueError(f"模板不存在: {template}")
    
    # 准备渲染上下文
    context = {
        "project_name": valid_project_name,
        "display_name": display_name,
        "pascal_case_name": to_pascal_case(valid_project_name),
        "kebab_case_name": to_kebab_case(valid_project_name),
    }
    
    try:
        # 创建项目结构
        _create_project_structure(templates_dir, project_dir, context)
        
        # 创建迁移配置（仅对standard和enterprise模板）
        if template in ["standard", "enterprise"]:
            _setup_migration(project_dir, context)
        
        return project_dir
    except Exception as e:
        # 如果出现错误，清理创建的目录
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)
        print(f"创建项目失败: {str(e)}")
        raise

def _setup_migration(project_dir: Path, context: Dict[str, Any]) -> None:
    """
    设置数据库迁移配置
    
    Args:
        project_dir: 项目目录
        context: 模板渲染上下文
    """
    try:
        # 导入迁移生成器
        from fastapi_generator.generators.migration_generator import generate_migration
        
        # 生成迁移配置
        generate_migration(output_dir=project_dir)
    except ImportError:
        print("警告: 无法导入迁移生成器，跳过迁移配置")
    except Exception as e:
        print(f"警告: 创建迁移配置失败: {str(e)}")

def _create_project_structure(
    template_dir: Path, 
    project_dir: Path, 
    context: Dict[str, Any]
) -> None:
    """
    从模板创建项目结构
    
    Args:
        template_dir: 模板目录
        project_dir: 项目目录
        context: 模板渲染上下文
    """
    # 确保项目目录存在
    ensure_dir_exists(project_dir)
    
    # 检查模板目录中是否有{{project_name}}目录
    project_name_dir = template_dir / "{{project_name}}"
    if project_name_dir.exists() and project_name_dir.is_dir():
        # 如果存在，直接从{{project_name}}目录复制内容到项目目录
        _copy_and_render_directory(project_name_dir, project_dir, context)
    else:
        # 否则，从模板根目录复制内容
        _copy_and_render_directory(template_dir, project_dir, context)

def _copy_and_render_directory(
    source_dir: Path,
    target_dir: Path,
    context: Dict[str, Any]
) -> None:
    """
    复制并渲染目录中的所有文件
    
    Args:
        source_dir: 源目录
        target_dir: 目标目录
        context: 模板渲染上下文
    """
    # 确保目标目录存在
    ensure_dir_exists(target_dir)
    
    # 设置Jinja2环境
    env = Environment(
        autoescape=select_autoescape(['html', 'xml']),
        keep_trailing_newline=True,
    )
    
    # 遍历源目录中的所有文件和子目录
    for item in source_dir.iterdir():
        # 处理目录名称中的变量
        name = item.name
        if name.startswith("{{") and name.endswith("}}"):
            # 提取变量名并从上下文获取值
            var_name = name[2:-2].strip()
            if var_name in context:
                name = str(context[var_name])
        
        # 构建目标路径
        target_path = target_dir / name
        
        # 处理目录
        if item.is_dir():
            _copy_and_render_directory(item, target_path, context)
            continue
        
        # 处理文件
        if item.is_file():
            # 如果是模板文件（.j2扩展名），渲染它
            if item.name.endswith(".j2"):
                try:
                    # 读取模板内容
                    with open(item, "r", encoding="utf-8") as f:
                        template_content = f.read()
                    
                    # 渲染模板
                    template = env.from_string(template_content)
                    content = template.render(**context)
                    
                    # 移除.j2扩展名
                    if target_path.name.endswith(".j2"):
                        target_path = target_path.with_name(target_path.name[:-3])
                    
                    # 写入渲染后的内容
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    print(f"错误: 渲染模板 {item} 失败: {str(e)}")
                    raise
            else:
                # 直接复制非模板文件
                try:
                    shutil.copy2(item, target_path)
                except Exception as e:
                    print(f"错误: 复制文件 {item} 到 {target_path} 失败: {str(e)}")
                    raise 