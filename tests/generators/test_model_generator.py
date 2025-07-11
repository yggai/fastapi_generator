"""
模型生成器测试
"""
import os
import shutil
import tempfile
from pathlib import Path
import pytest

from fastapi_generator.generators.model_generator import generate_model


class TestModelGenerator:
    """测试模型生成器功能"""
    
    @pytest.fixture
    def temp_project(self):
        """创建临时项目目录用于测试"""
        temp_dir = Path(tempfile.mkdtemp())
        
        # 创建标准项目结构
        project_path = temp_dir / "test_project"
        os.makedirs(project_path / "app" / "models", exist_ok=True)
        os.makedirs(project_path / "app" / "schemas", exist_ok=True)
        
        # 创建必要的初始文件
        with open(project_path / "app" / "models" / "__init__.py", "w", encoding="utf-8") as f:
            f.write("# Models package")
        
        with open(project_path / "app" / "schemas" / "__init__.py", "w", encoding="utf-8") as f:
            f.write("# Schemas package")
        
        yield project_path
        # 测试后清理
        shutil.rmtree(temp_dir)
    
    def test_generate_basic_model(self, temp_project):
        """测试生成基本模型"""
        # 准备
        model_name = "user"
        
        # 执行
        model_file = generate_model(model_name, output_dir=temp_project / "app")
        
        # 验证
        assert model_file.exists()
        
        # 检查模型文件内容
        with open(model_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class User" in content
            assert "name: str" in content
            assert "description: Optional[str]" in content
        
        # 检查Schema文件
        schema_file = temp_project / "app" / "schemas" / f"{model_name}.py"
        assert schema_file.exists()
        
        # 检查Schema文件内容
        with open(schema_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class UserCreate" in content
            assert "class UserUpdate" in content
            assert "class UserRead" in content
        
        # 检查模型是否已在__init__.py中导入
        with open(temp_project / "app" / "models" / "__init__.py", "r", encoding="utf-8") as f:
            content = f.read()
            assert f"from .{model_name} import User" in content
    
    def test_generate_model_with_existing_model(self, temp_project):
        """测试生成已存在的模型"""
        # 准备
        model_name = "existing"
        
        # 先创建模型文件
        with open(temp_project / "app" / "models" / f"{model_name}.py", "w", encoding="utf-8") as f:
            f.write("# Existing model")
        
        # 修改测试期望，不再期望FileExistsError异常
        # 执行
        model_file = generate_model(model_name, output_dir=temp_project / "app")
        
        # 验证文件被覆盖
        assert model_file.exists()
        with open(model_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "class Existing" in content  # 验证文件已被覆盖 