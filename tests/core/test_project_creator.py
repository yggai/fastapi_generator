"""
项目创建器测试
"""
import os
import shutil
import tempfile
from pathlib import Path
import pytest

from fastapi_generator.core.project_creator import create_project, validate_project_name


class TestProjectCreator:
    """测试项目创建功能"""
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录用于测试"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # 测试后清理
        shutil.rmtree(temp_dir)
    
    def test_validate_project_name(self):
        """测试项目名称验证"""
        assert validate_project_name("test-project") == "test_project"
        assert validate_project_name("TestProject") == "test_project"
        assert validate_project_name("test_project") == "test_project"
        assert validate_project_name("123test") == "app_123test"
        assert validate_project_name("test@project") == "test_project"
    
    def test_create_basic_project(self, temp_dir):
        """测试创建基础项目"""
        # 准备
        project_name = "test_project"
        
        # 执行
        project_path = create_project(project_name, output_dir=temp_dir, template="basic")
        
        # 验证
        assert project_path.exists()
        assert (project_path / "main.py").exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / "README.md").exists()
    
    def test_create_standard_project(self, temp_dir):
        """测试创建标准项目"""
        # 准备
        project_name = "test_standard"
        
        # 执行
        project_path = create_project(project_name, output_dir=temp_dir, template="standard")
        
        # 验证
        assert project_path.exists()
        # 验证标准项目特有的目录结构
        assert (project_path / "app").exists()
        assert (project_path / "app" / "api").exists()
        assert (project_path / "app" / "models").exists()
        assert (project_path / "app" / "schemas").exists()
        assert (project_path / "migrations").exists()
    
    def test_create_project_with_invalid_template(self, temp_dir):
        """测试使用无效模板创建项目"""
        # 准备
        project_name = "invalid_template"
        
        # 执行与验证
        with pytest.raises(ValueError):
            create_project(project_name, output_dir=temp_dir, template="non_existent")
    
    def test_create_project_with_existing_directory(self, temp_dir):
        """测试在已存在目录中创建项目"""
        # 准备
        project_name = "existing_dir"
        project_path = temp_dir / project_name
        os.makedirs(project_path)  # 先创建目录
        
        # 执行与验证
        with pytest.raises(FileExistsError):
            create_project(project_name, output_dir=temp_dir) 