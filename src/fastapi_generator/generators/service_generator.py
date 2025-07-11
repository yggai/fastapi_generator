"""
服务生成器模块
"""
from pathlib import Path
from typing import List, Optional
from fastapi_generator.utils.path_utils import ensure_dir_exists, find_project_root
from fastapi_generator.utils.string_utils import to_snake_case, to_pascal_case

# 服务模板
SERVICE_TEMPLATE = """from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from typing import List, Optional

from app.db.session import get_session
from app.models.{model_name} import {model_class}
from app.schemas.{model_name} import {model_class}Create, {model_class}Read, {model_class}Update


class {model_class}Service:
    \"\"\"
    {model_display_name}服务类
    \"\"\"
    
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[{model_class}]:
        \"\"\"
        获取所有{model_display_name}列表
        \"\"\"
        return self.session.exec(select({model_class}).offset(skip).limit(limit)).all()
    
    def get_by_id(self, {model_name}_id: int) -> Optional[{model_class}]:
        \"\"\"
        根据ID获取{model_display_name}
        \"\"\"
        return self.session.get({model_class}, {model_name}_id)
    
    def create(self, {model_name}_data: {model_class}Create) -> {model_class}:
        \"\"\"
        创建新的{model_display_name}
        \"\"\"
        {model_name} = {model_class}(**{model_name}_data.dict())
        self.session.add({model_name})
        self.session.commit()
        self.session.refresh({model_name})
        return {model_name}
    
    def update(self, {model_name}_id: int, {model_name}_data: {model_class}Update) -> {model_class}:
        \"\"\"
        更新{model_display_name}
        \"\"\"
        {model_name} = self.get_by_id({model_name}_id)
        if not {model_name}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model_display_name} ID {{{model_name}_id}} 不存在"
            )
        
        # 更新模型字段
        {model_name}_data_dict = {model_name}_data.dict(exclude_unset=True)
        for key, value in {model_name}_data_dict.items():
            setattr({model_name}, key, value)
        
        self.session.add({model_name})
        self.session.commit()
        self.session.refresh({model_name})
        return {model_name}
    
    def delete(self, {model_name}_id: int) -> None:
        \"\"\"
        删除{model_display_name}
        \"\"\"
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
            app_dir = project_root / "app"
            services_dir = app_dir / "services"
        else:
            # 如果找不到项目根目录，使用当前目录下的app目录
            app_dir = Path.cwd() / "app"
            services_dir = app_dir / "services"
    else:
        # 如果提供了输出目录，检查是否有app目录
        if (output_dir / "app").exists() and (output_dir / "app").is_dir():
            # 如果存在app目录，使用app下的services目录
            app_dir = output_dir / "app"
            services_dir = app_dir / "services"
        else:
            # 否则，假设output_dir已经是app目录或直接使用output_dir
            app_dir = output_dir
            services_dir = app_dir / "services"
    
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

def _update_init_file(dir_path: Path, model_name: str, model_class: str) -> None:
    """
    更新__init__.py文件，添加服务类导入
    """
    # 确保__init__.py文件存在
    init_file = dir_path / "__init__.py"
    if not init_file.exists():
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("\"\"\"服务模块\"\"\"\n")
    
    # 读取现有内容
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 添加导入语句（如果不存在）
    import_line = f"from .{model_name}_service import {model_class}Service\n"
    if import_line not in content:
        # 如果文件为空或只有文档字符串，添加新行
        if not content.strip() or content.strip().endswith('"""'):
            content += "\n" + import_line
        else:
            content += import_line
        
        # 写回文件
        with open(init_file, "w", encoding="utf-8") as f:
            f.write(content) 