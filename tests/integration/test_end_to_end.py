"""
端到端测试模块
"""
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Tuple
import pytest

from typer.testing import CliRunner


@pytest.fixture
def runner():
    """创建测试运行器"""
    return CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """创建临时目录用于测试"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # 测试后清理
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestEndToEnd:
    """端到端测试类"""

    def test_full_project_workflow(self, runner, temp_dir):
        """测试完整项目工作流程"""
        project_name = "full_test_project"
        output_dir = temp_dir

        # 步骤1: 创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name, 
            "--output", str(output_dir)
        ]
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"创建项目失败: {result.stderr}"
        
        # 验证项目结构
        project_dir = output_dir / project_name
        assert project_dir.exists()
        assert (project_dir / "app").exists()
        assert (project_dir / "app" / "api").exists()
        assert (project_dir / "app" / "core").exists()
        assert (project_dir / "app" / "models").exists()
        assert (project_dir / "app" / "schemas").exists()
        assert (project_dir / "main.py").exists()

        # 步骤2: 生成数据模型
        model_name = "item"
        model_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main",
            "generate", "model", model_name,
            "--output", str(project_dir)
        ]
        result = subprocess.run(model_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"生成模型失败: {result.stderr}"
        
        # 验证模型生成
        model_file = project_dir / "app" / "models" / f"{model_name}.py"
        schema_file = project_dir / "app" / "schemas" / f"{model_name}.py"
        assert model_file.exists()
        assert schema_file.exists()
        
        # 步骤3: 生成API
        api_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main",
            "generate", "api", model_name,
            "--output", str(project_dir)
        ]
        result = subprocess.run(api_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"生成API失败: {result.stderr}"
        
        # 验证API生成
        api_file = project_dir / "app" / "api" / "api_v1" / "endpoints" / f"{model_name}.py"
        assert api_file.exists()

    def test_create_project_and_generate_api(self, runner, temp_dir):
        """测试创建项目并生成API的完整流程"""
        project_name = "test_project"
        
        # 使用subprocess直接调用命令行工具而不是通过Typer
        # 第1步：创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name,
            "--output", str(temp_dir)
        ]
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"创建项目失败: {result.stderr}"
        
        # 验证项目创建成功
        project_dir = temp_dir / project_name
        assert project_dir.exists()
        assert (project_dir / "main.py").exists()
        assert (project_dir / "app").exists()
        
        # 第2步：生成API
        resource_name = "user"
        api_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "api", resource_name,
            "--output", str(project_dir)
        ]
        result = subprocess.run(api_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"生成API失败: {result.stderr}"
        
        # 验证API生成成功
        api_file = project_dir / "app" / "api" / "api_v1" / "endpoints" / f"{resource_name}.py"
        assert api_file.exists()
        
        # 验证API文件内容
        with open(api_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "router = APIRouter()" in content
            assert "@router.get(\"/\"" in content
            assert "@router.post(\"/\"" in content
            assert "@router.put(\"/{" in content
            assert "@router.delete(\"/{" in content
            assert "response_model=List[UserRead]" in content
    
    def test_create_project_and_generate_model(self, runner, temp_dir):
        """测试创建项目并生成模型的完整流程"""
        project_name = "test_model_project"
        
        # 第1步：创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name,
            "--output", str(temp_dir)
        ]
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"创建项目失败: {result.stderr}"
        
        # 验证项目创建成功
        project_dir = temp_dir / project_name
        assert project_dir.exists()
        
        # 第2步：生成模型
        model_name = "product"
        model_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "model", model_name,
            "--output", str(project_dir)
        ]
        result = subprocess.run(model_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"生成模型失败: {result.stderr}"
        
        # 验证模型生成成功
        model_file = project_dir / "app" / "models" / f"{model_name}.py"
        schema_file = project_dir / "app" / "schemas" / f"{model_name}.py"
        
        assert model_file.exists()
        assert schema_file.exists()
        
        # 验证模型文件内容
        with open(model_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class Product(SQLModel, table=True):" in content
        
        # 验证Schema文件内容
        with open(schema_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class ProductCreate" in content
            assert "class ProductUpdate" in content
            assert "class ProductRead" in content 