"""
服务生成器测试
"""
import os
import shutil
import tempfile
from pathlib import Path
import pytest

from fastapi_generator.generators.service_generator import generate_service


class TestServiceGenerator:
    """测试服务生成器功能"""
    
    @pytest.fixture
    def temp_project(self):
        """创建临时项目目录用于测试"""
        temp_dir = Path(tempfile.mkdtemp())
        
        # 创建标准项目结构
        project_path = temp_dir / "test_project"
        os.makedirs(project_path / "app" / "services", exist_ok=True)
        os.makedirs(project_path / "app" / "models", exist_ok=True)
        os.makedirs(project_path / "app" / "schemas", exist_ok=True)
        
        # 创建必要的初始文件
        with open(project_path / "app" / "services" / "__init__.py", "w", encoding="utf-8") as f:
            f.write("# Services package")
        
        # 创建模型文件
        with open(project_path / "app" / "models" / "user.py", "w", encoding="utf-8") as f:
            f.write("""from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    is_active: bool = True
""")
        
        # 创建Schema文件
        with open(project_path / "app" / "schemas" / "user.py", "w", encoding="utf-8") as f:
            f.write("""from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    is_active: Optional[bool] = True

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
""")
        
        # 更新模型__init__.py
        with open(project_path / "app" / "models" / "__init__.py", "w", encoding="utf-8") as f:
            f.write("from app.models.user import User")
        
        # 更新Schema__init__.py
        with open(project_path / "app" / "schemas" / "__init__.py", "w", encoding="utf-8") as f:
            f.write("from app.schemas.user import UserCreate, UserRead, UserUpdate")
        
        yield project_path
        # 测试后清理
        shutil.rmtree(temp_dir)
    
    def test_generate_basic_service(self, temp_project):
        """测试生成基本服务"""
        # 准备
        model_name = "user"
        
        # 执行
        service_file = generate_service(model_name, output_dir=temp_project / "app" / "services")
        
        # 验证
        assert service_file.exists()
        
        # 检查服务文件内容
        with open(service_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class UserService" in content
            assert "def get_all" in content
            assert "def get_by_id" in content
            assert "def create" in content
            assert "def update" in content
            assert "def delete" in content
            assert "from app.models.user import User" in content
            assert "from app.schemas.user import UserCreate, UserUpdate" in content
        
        # 检查服务是否已在__init__.py中导入
        with open(temp_project / "app" / "services" / "__init__.py", "r", encoding="utf-8") as f:
            content = f.read()
            assert f"from .{model_name}_service import UserService" in content
    
    def test_generate_service_with_existing_service(self, temp_project):
        """测试生成已存在的服务"""
        # 准备
        model_name = "existing"
        
        # 先创建服务文件
        with open(temp_project / "app" / "services" / f"{model_name}_service.py", "w", encoding="utf-8") as f:
            f.write("# Existing service")
        
        # 修改测试期望，不再期望FileExistsError异常
        # 执行
        service_file = generate_service(model_name, output_dir=temp_project / "app" / "services")
        
        # 验证文件被覆盖
        assert service_file.exists()
        with open(service_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class ExistingService" in content  # 验证文件已被覆盖 