"""
API生成器模块
"""
from pathlib import Path
from typing import List, Optional
import os
from jinja2 import Environment, FileSystemLoader
import re

from fastapi_generator.utils.path_utils import ensure_dir_exists, find_project_root
from fastapi_generator.utils.string_utils import to_snake_case, to_pascal_case, pluralize

# API端点模板
API_ENDPOINT_TEMPLATE = """from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from app.db.session import get_session
from app.models.{model_name} import {model_class}
from app.schemas.{model_name} import {model_class}Create, {model_class}Read, {model_class}Update

router = APIRouter()


@router.get("/", response_model=List[{model_class}Read])
def get_all_{model_name_plural}(
    skip: int = 0, 
    limit: int = 100,
    session: Session = Depends(get_session)
):
    \"""
    获取所有{model_display_name}列表
    \"""
    {model_name_plural} = session.exec(select({model_class}).offset(skip).limit(limit)).all()
    return {model_name_plural}


@router.get("/{{{model_name}_id}}", response_model={model_class}Read)
def get_{model_name}(
    {model_name}_id: int,
    session: Session = Depends(get_session)
):
    \"""
    根据ID获取{model_display_name}
    \"""
    {model_name} = session.get({model_class}, {model_name}_id)
    if not {model_name}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_display_name} ID {{{model_name}_id}} 不存在"
        )
    return {model_name}


@router.post("/", response_model={model_class}Read, status_code=status.HTTP_201_CREATED)
def create_{model_name}(
    {model_name}_data: {model_class}Create,
    session: Session = Depends(get_session)
):
    \"""
    创建新的{model_display_name}
    \"""
    {model_name} = {model_class}(**{model_name}_data.model_dump())
    session.add({model_name})
    session.commit()
    session.refresh({model_name})
    return {model_name}


@router.put("/{{{model_name}_id}}", response_model={model_class}Read)
def update_{model_name}(
    {model_name}_id: int,
    {model_name}_data: {model_class}Update,
    session: Session = Depends(get_session)
):
    \"""
    更新{model_display_name}
    \"""
    {model_name} = session.get({model_class}, {model_name}_id)
    if not {model_name}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_display_name} ID {{{model_name}_id}} 不存在"
        )
    
    # 更新模型数据
    {model_name}_data_dict = {model_name}_data.model_dump(exclude_unset=True)
    for key, value in {model_name}_data_dict.items():
        setattr({model_name}, key, value)
    
    session.add({model_name})
    session.commit()
    session.refresh({model_name})
    return {model_name}


@router.delete("/{{{model_name}_id}}", status_code=status.HTTP_204_NO_CONTENT)
def delete_{model_name}(
    {model_name}_id: int,
    session: Session = Depends(get_session)
):
    \"""
    删除{model_display_name}
    \"""
    {model_name} = session.get({model_class}, {model_name}_id)
    if not {model_name}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_display_name} ID {{{model_name}_id}} 不存在"
        )
    
    session.delete({model_name})
    session.commit()
    return None
"""

def generate_api(name: str, output_dir: Optional[Path] = None) -> Path:
    """
    生成API端点文件
    
    Args:
        name: API资源名称
        output_dir: 输出目录，默认为当前项目的api/endpoints目录
        
    Returns:
        生成的API文件路径
    """
    # 处理名称
    model_name = to_snake_case(name)
    model_class = to_pascal_case(name)
    model_name_plural = pluralize(model_name)
    model_display_name = name  # 原始名称作为显示名称
    
    # 确定输出目录
    if output_dir is None:
        # 尝试找到项目根目录
        project_root = find_project_root()
        if project_root:
            # 假设标准项目结构
            output_dir = project_root / "app" / "api" / "api_v1" / "endpoints"
        else:
            # 如果找不到项目根目录，使用当前目录
            output_dir = Path.cwd() / "app" / "api" / "api_v1" / "endpoints"
    
    # 确保输出目录存在
    ensure_dir_exists(output_dir)
    
    # 生成API端点文件
    endpoint_file = output_dir / f"{model_name}.py"
    
    # 渲染模板
    endpoint_content = API_ENDPOINT_TEMPLATE.format(
        model_name=model_name,
        model_class=model_class,
        model_name_plural=model_name_plural,
        model_display_name=model_display_name
    )
    
    # 写入文件
    with open(endpoint_file, "w", encoding="utf-8") as f:
        f.write(endpoint_content)
    
    # 更新API路由聚合文件
    _update_api_router(model_name, model_name_plural, output_dir.parent)
    
    return endpoint_file

def _update_api_router(model_name: str, model_name_plural: str, api_dir: Path) -> None:
    """
    更新API路由聚合文件
    
    Args:
        model_name: 模型名称（蛇形命名法）
        model_name_plural: 模型复数名称（蛇形命名法）
        api_dir: API目录路径
    """
    api_file = api_dir / "api.py"
    
    if not api_file.exists():
        # 如果API路由聚合文件不存在，创建一个基础文件
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('"""API路由聚合"""\n')
            f.write("from fastapi import APIRouter\n\n")
            f.write("api_router = APIRouter()\n")
    
    # 读取现有内容
    with open(api_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否已经导入了该模块
    import_pattern = rf"from app.api.api_v1.endpoints import {model_name}"
    if not re.search(import_pattern, content):
        # 添加导入语句
        import_section_end = content.find("api_router = APIRouter()")
        if import_section_end == -1:
            # 如果找不到api_router定义，添加到文件末尾
            content += f"\nfrom app.api.api_v1.endpoints import {model_name}\n"
        else:
            # 在api_router定义前添加导入
            content = content[:import_section_end] + f"from app.api.api_v1.endpoints import {model_name}\n\n" + content[import_section_end:]
    
    # 检查是否已经注册了该路由
    router_pattern = rf"api_router.include_router\({model_name}.router, prefix=\"/{model_name_plural}\""
    if not re.search(router_pattern, content):
        # 添加路由注册
        if "api_router.include_router" in content:
            # 在最后一个include_router后添加
            last_include = content.rfind("api_router.include_router")
            if last_include != -1:
                # 找到该行的结束位置
                line_end = content.find("\n", last_include)
                if line_end != -1:
                    content = content[:line_end+1] + f"api_router.include_router({model_name}.router, prefix=\"/{model_name_plural}\", tags=[\"{model_name_plural}\"])\n" + content[line_end+1:]
        else:
            # 如果没有任何include_router，添加到文件末尾
            content += f"\napi_router.include_router({model_name}.router, prefix=\"/{model_name_plural}\", tags=[\"{model_name_plural}\"])\n"
    
    # 写回文件
    with open(api_file, "w", encoding="utf-8") as f:
        f.write(content) 