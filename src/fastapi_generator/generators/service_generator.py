"""
服务生成器模块
"""
from pathlib import Path
from typing import List, Optional
import os
from jinja2 import Environment, FileSystemLoader
import re

from fastapi_generator.utils.path_utils import ensure_dir_exists, find_project_root
from fastapi_generator.utils.string_utils import to_snake_case, to_pascal_case, pluralize

# 服务模板
SERVICE_TEMPLATE = """from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models.{model_name} import {model_class}
from app.schemas.{model_name} import {model_class}Create, {model_class}Update


class {model_class}Service:
    \"""
    {model_display_name}服务类
    处理与{model_display_name}相关的业务逻辑
    \"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[{model_class}]:
        \"""
        获取所有{model_display_name}列表
        
        Args:
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            {model_display_name}列表
        \"""
        return self.session.exec(select({model_class}).offset(skip).limit(limit)).all()
    
    def get_by_id(self, {model_name}_id: int) -> Optional[{model_class}]:
        \"""
        根据ID获取{model_display_name}
        
        Args:
            {model_name}_id: {model_display_name}的ID
            
        Returns:
            {model_display_name}对象，如果不存在则返回None
        \"""
        return self.session.get({model_class}, {model_name}_id)
    
    def create(self, {model_name}_data: {model_class}Create) -> {model_class}:
        \"""
        创建新的{model_display_name}
        
        Args:
            {model_name}_data: {model_display_name}创建数据
            
        Returns:
            创建的{model_display_name}对象
        \"""
        {model_name} = {model_class}(**{model_name}_data.model_dump())
        self.session.add({model_name})
        self.session.commit()
        self.session.refresh({model_name})
        return {model_name}
    
    def update(self, {model_name}_id: int, {model_name}_data: {model_class}Update) -> {model_class}:
        \"""
        更新{model_display_name}
        
        Args:
            {model_name}_id: 要更新的{model_display_name}的ID
            {model_name}_data: {model_display_name}更新数据
            
        Returns:
            更新后的{model_display_name}对象
            
        Raises:
            HTTPException: 如果{model_display_name}不存在
        \"""
        {model_name} = self.get_by_id({model_name}_id)
        if not {model_name}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model_display_name} ID {{{model_name}_id}} 不存在"
            )
        
        # 更新模型数据
        {model_name}_data_dict = {model_name}_data.model_dump(exclude_unset=True)
        for key, value in {model_name}_data_dict.items():
            setattr({model_name}, key, value)
        
        self.session.add({model_name})
        self.session.commit()
        self.session.refresh({model_name})
        return {model_name}
    
    def delete(self, {model_name}_id: int) -> None:
        \"""
        删除{model_display_name}
        
        Args:
            {model_name}_id: 要删除的{model_display_name}的ID
            
        Raises:
            HTTPException: 如果{model_display_name}不存在
        \"""
        {model_name} = self.get_by_id({model_name}_id)
        if not {model_name}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model_display_name} ID {{{model_name}_id}} 不存在"
            )
        
        self.session.delete({model_name})
        self.session.commit()
"""

def generate_service(name: str, output_dir: Optional[Path] = None) -> Path:
    """
    生成服务文件
    
    Args:
        name: 服务名称
        output_dir: 输出目录，默认为当前项目的services目录
        
    Returns:
        生成的服务文件路径
    """
    # 处理名称
    model_name = to_snake_case(name)
    model_class = to_pascal_case(name)
    model_display_name = name  # 原始名称作为显示名称
    
    # 确定输出目录
    if output_dir is None:
        # 尝试找到项目根目录
        project_root = find_project_root()
        if project_root:
            # 假设标准项目结构
            services_dir = project_root / "app" / "services"
        else:
            # 如果找不到项目根目录，使用当前目录
            services_dir = Path.cwd() / "app" / "services"
    else:
        services_dir = output_dir
    
    # 确保输出目录存在
    ensure_dir_exists(services_dir)
    
    # 生成服务文件
    service_file = services_dir / f"{model_name}_service.py"
    
    # 渲染模板
    service_content = SERVICE_TEMPLATE.format(
        model_name=model_name,
        model_class=model_class,
        model_display_name=model_display_name
    )
    
    # 写入文件
    with open(service_file, "w", encoding="utf-8") as f:
        f.write(service_content)
    
    # 更新__init__.py文件
    _update_init_file(services_dir, model_name, model_class)
    
    return service_file

def _update_init_file(directory: Path, model_name: str, model_class: str) -> None:
    """
    更新__init__.py文件，添加服务导入
    
    Args:
        directory: 目录路径
        model_name: 模型名称（蛇形命名法）
        model_class: 模型类名（帕斯卡命名法）
    """
    init_file = directory / "__init__.py"
    
    # 如果__init__.py不存在，创建一个
    if not init_file.exists():
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""服务模块"""\n')
    
    # 读取现有内容
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否已经导入了该服务
    service_class = f"{model_class}Service"
    import_pattern = rf"from .{model_name}_service import {service_class}"
    if not re.search(import_pattern, content):
        # 添加导入语句
        if content.strip() and not content.endswith("\n"):
            content += "\n"
        content += f"from .{model_name}_service import {service_class}\n"
        
        # 写回文件
        with open(init_file, "w", encoding="utf-8") as f:
            f.write(content) 