"""
文件输出验证测试
验证生成的文件内容是否符合预期
"""
import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
import pytest

from typer.testing import CliRunner


class TestFileValidation:
    """文件输出验证测试类"""
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录用于测试"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # 测试后清理
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def runner(self):
        """创建CLI测试运行器"""
        return CliRunner()
    
    @pytest.fixture
    def project_dir(self, runner, temp_dir):
        """创建测试项目"""
        project_name = "validation_project"
        
        # 创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name, 
            "--output", str(temp_dir)
        ]
        subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        
        project_dir = temp_dir / project_name
        return project_dir
    
    def test_main_py_content(self, project_dir):
        """验证main.py文件内容"""
        main_py = project_dir / "main.py"
        assert main_py.exists()
        
        with open(main_py, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 验证主要导入
        assert "from fastapi import FastAPI" in content
        assert "from app.api.api_v1.api import api_router" in content
        
        # 验证应用创建
        assert "app = FastAPI(" in content
        assert "title=" in content
        assert "description=" in content
        assert "version=" in content
        
        # 验证路由注册
        assert "app.include_router(api_router" in content
    
    def test_api_router_content(self, project_dir):
        """验证API路由文件内容"""
        api_py = project_dir / "app" / "api" / "api_v1" / "api.py"
        assert api_py.exists()
        
        with open(api_py, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证路由器创建
        assert "from fastapi import APIRouter" in content
        assert "api_router = APIRouter()" in content
    
    def test_config_py_content(self, project_dir):
        """验证配置文件内容"""
        config_py = project_dir / "app" / "core" / "config.py"
        assert config_py.exists()
        
        with open(config_py, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证配置类
        assert "from pydantic_settings import BaseSettings" in content
        assert "class Settings(BaseSettings):" in content
        assert "PROJECT_NAME: str" in content
        assert "API_V1_STR: str" in content
        assert "settings = Settings()" in content
    
    def test_generated_model_content(self, runner, project_dir):
        """验证生成的模型文件内容"""
        # 生成模型
        model_name = "item"
        model_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "model", model_name, 
            "--output", str(project_dir)
        ]
        subprocess.run(model_cmd, capture_output=True, text=True, check=True)
        
        # 检查模型文件
        model_py = project_dir / "app" / "models" / f"{model_name}.py"
        assert model_py.exists()
        
        with open(model_py, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证模型类定义
        assert "from sqlmodel import Field, SQLModel" in content
        assert "class ItemBase(SQLModel):" in content
        assert "class Item(SQLModel, table=True):" in content
        assert "__tablename__ = \"items\"" in content
        
        # 检查Schema文件
        schema_py = project_dir / "app" / "schemas" / f"{model_name}.py"
        assert schema_py.exists()
        
        with open(schema_py, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证Schema类定义
        model_cap = model_name.capitalize()
        assert f"class {model_cap}Create" in content
        assert f"class {model_cap}Update" in content
        assert f"class {model_cap}Read" in content
    
    def test_generated_api_content(self, runner, project_dir):
        """验证生成的API文件内容"""
        # 生成API
        resource_name = "product"
        api_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "api", resource_name, 
            "--output", str(project_dir)
        ]
        subprocess.run(api_cmd, capture_output=True, text=True, check=True)
        
        # 检查API文件
        api_py = project_dir / "app" / "api" / "api_v1" / "endpoints" / f"{resource_name}.py"
        assert api_py.exists()
        
        with open(api_py, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证API路由定义
        assert "from fastapi import APIRouter, Depends, HTTPException, status" in content
        assert "router = APIRouter()" in content
        
        # 验证CRUD端点
        assert "@router.get(\"/\"" in content
        assert "@router.get(\"/{product_id}\"" in content
        assert "@router.post(\"/\"" in content
        assert "@router.put(\"/{product_id}\"" in content
        assert "@router.delete(\"/{product_id}\"" in content
        
        # 验证模型导入
        assert "from app.models.product import Product" in content
        assert "from app.schemas.product import ProductCreate, ProductRead, ProductUpdate" in content
    
    def test_migration_files(self, runner, project_dir):
        """验证迁移文件内容"""
        # 生成迁移
        migration_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "migration", "init", 
            "--output", str(project_dir)
        ]
        subprocess.run(migration_cmd, capture_output=True, text=True, check=True)
        
        # 检查迁移文件
        assert (project_dir / "alembic.ini").exists()
        assert (project_dir / "migrations").exists()
        assert (project_dir / "migrations" / "env.py").exists()
        assert (project_dir / "migrations" / "README.md").exists()
        assert (project_dir / "migrations" / "versions").exists()
        
        # 检查alembic.ini内容
        with open(project_dir / "alembic.ini", "r", encoding="utf-8") as f:
            content = f.read()
            assert "script_location = migrations" in content
            
        # 检查env.py内容
        with open(project_dir / "migrations" / "env.py", "r", encoding="utf-8") as f:
            content = f.read()
            assert "from alembic import context" in content
            assert "from app.models import *" in content
            assert "from app.db.base import Base" in content 