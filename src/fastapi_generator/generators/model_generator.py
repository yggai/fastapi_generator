"""
模型生成器模块
"""
from pathlib import Path
from typing import List, Optional, Dict, Any
import os
from jinja2 import Environment, FileSystemLoader
import re

from fastapi_generator.utils.path_utils import ensure_dir_exists, find_project_root
from fastapi_generator.utils.string_utils import to_snake_case, to_pascal_case

# 模型模板
MODEL_TEMPLATE = """from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class {model_class}Base(SQLModel):
    \"""基础{model_display_name}模型\"""
    name: str = Field(index=True, description="{model_display_name}名称")
    description: Optional[str] = Field(default=None, description="描述")


class {model_class}(SQLModel, table=True):
    \"""数据库{model_display_name}模型\"""
    __tablename__ = "{model_name_plural}"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="{model_display_name}名称")
    description: Optional[str] = Field(default=None, description="描述")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
"""

# 模式模板
SCHEMA_TEMPLATE = """from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.models.{model_name} import {model_class}Base


class {model_class}Create({model_class}Base):
    \"""创建{model_display_name}请求模型\"""
    pass


class {model_class}Update(BaseModel):
    \"""更新{model_display_name}请求模型\"""
    name: Optional[str] = None
    description: Optional[str] = None


class {model_class}Read({model_class}Base):
    \"""返回{model_display_name}响应模型\"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
"""

def generate_model(name: str, output_dir: Optional[Path] = None, fields: Optional[Dict[str, Any]] = None) -> Path:
    """
    生成数据模型文件和对应的模式文件
    
    Args:
        name: 模型名称
        output_dir: 输出目录，默认为当前项目的app目录
        fields: 模型字段定义，默认为None（使用基本字段）
        
    Returns:
        生成的模型文件路径
    """
    # 处理名称
    model_name = to_snake_case(name)
    model_class = to_pascal_case(name)
    model_display_name = name  # 原始名称作为显示名称
    
    # 确定模型输出目录
    if output_dir is None:
        # 尝试找到项目根目录
        project_root = find_project_root()
        if project_root:
            # 假设标准项目结构
            app_dir = project_root / "app"
            models_dir = app_dir / "models"
            schemas_dir = app_dir / "schemas"
        else:
            # 如果找不到项目根目录，使用当前目录下的app目录
            app_dir = Path.cwd() / "app"
            models_dir = app_dir / "models"
            schemas_dir = app_dir / "schemas"
    else:
        # 如果提供了输出目录，检查是否有app目录
        if (output_dir / "app").exists() and (output_dir / "app").is_dir():
            # 如果存在app目录，使用app下的models和schemas目录
            app_dir = output_dir / "app"
            models_dir = app_dir / "models"
            schemas_dir = app_dir / "schemas"
        else:
            # 否则，假设output_dir已经是app目录或直接使用output_dir
            app_dir = output_dir
            models_dir = app_dir / "models"
            schemas_dir = app_dir / "schemas"
    
    # 确保输出目录存在
    ensure_dir_exists(models_dir)
    ensure_dir_exists(schemas_dir)
    
    # 生成模型文件
    model_file = models_dir / f"{model_name}.py"
    schema_file = schemas_dir / f"{model_name}.py"
    
    # 获取模型名称的复数形式
    model_name_plural = model_name + "s"  # 简化处理，实际应使用更复杂的复数规则
    
    # 渲染模型模板
    model_content = MODEL_TEMPLATE.format(
        model_name=model_name,
        model_class=model_class,
        model_display_name=model_display_name,
        model_name_plural=model_name_plural
    )
    
    # 渲染模式模板
    schema_content = SCHEMA_TEMPLATE.format(
        model_name=model_name,
        model_class=model_class,
        model_display_name=model_display_name
    )
    
    # 写入模型文件
    with open(model_file, "w", encoding="utf-8") as f:
        f.write(model_content)
    
    # 写入模式文件
    with open(schema_file, "w", encoding="utf-8") as f:
        f.write(schema_content)
    
    # 更新模型和模式的__init__.py文件
    _update_init_file(models_dir, model_name, model_class)
    _update_init_file(schemas_dir, model_name, model_class)
    
    return model_file

def _update_init_file(dir_path: Path, model_name: str, model_class: str) -> None:
    """
    更新__init__.py文件，添加模型导入
    """
    # 确保__init__.py文件存在
    init_file = dir_path / "__init__.py"
    if not init_file.exists():
        with open(init_file, "w", encoding="utf-8") as f:
            f.write(f"""\"\"\"数据模型模块\"\"\"\n""")
    
    # 读取现有内容
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 添加导入语句（如果不存在）
    import_line = f"from .{model_name} import {model_class}\n"
    if import_line not in content:
        # 如果文件为空或只有文档字符串，添加新行
        if not content.strip() or content.strip().endswith('"""'):
            content += "\n" + import_line
        else:
            content += import_line
        
        # 写回文件
        with open(init_file, "w", encoding="utf-8") as f:
            f.write(content) 