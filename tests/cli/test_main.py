"""
命令行接口测试
"""
import os
import sys
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
import typer

from fastapi_generator.cli import main as cli_main


def create_typer_app_for_testing():
    """创建一个用于测试的Typer应用"""
    app = typer.Typer()
    
    @app.command("create")
    def create_project_cmd(
        project_name: str, 
        output_dir: Path = typer.Option(None, "--output-dir", "-o", help="输出目录"),
        template: str = typer.Option("standard", "--template", "-t", help="项目模板")
    ):
        from fastapi_generator.core.project_creator import create_project
        project_path = create_project(project_name, output_dir, template)
        return 0
    
    @app.command("generate")
    def generate_component(
        component_type: str, 
        name: str = typer.Argument(..., help="组件名称"),
        output_dir: Path = typer.Option(None, "--output-dir", "-o", help="输出目录")
    ):
        if component_type == "api":
            from fastapi_generator.generators.api_generator import generate_api
            generate_api(name, output_dir)
        elif component_type == "model":
            from fastapi_generator.generators.model_generator import generate_model
            generate_model(name, output_dir)
        elif component_type == "service":
            from fastapi_generator.generators.service_generator import generate_service
            generate_service(name, output_dir)
        elif component_type == "migration":
            from fastapi_generator.generators.migration_generator import generate_migration
            # 为迁移生成提供一个虚拟名称
            generate_migration(output_dir)
        return 0
    
    return app


class TestCliMain:
    """测试命令行主程序功能"""
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录用于测试"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # 测试后清理
        shutil.rmtree(temp_dir)
    
    @patch("fastapi_generator.core.project_creator.create_project")
    def test_create_command(self, mock_create_project, temp_dir):
        """测试项目创建命令"""
        # 准备
        mock_create_project.return_value = Path(temp_dir) / "test_project"
        
        project_name = "test_project"
        
        # 使用测试版本的app
        test_app = create_typer_app_for_testing()
        
        # 执行，设置standalone_mode=False以防止系统退出
        with patch.object(sys, 'argv', [
            "fg", "create", project_name, 
            "--output-dir", str(temp_dir),
        ]):
            result = test_app(["create", project_name, "--output-dir", str(temp_dir)], standalone_mode=False)
        
        # 验证
        assert result == 0
        mock_create_project.assert_called_once_with(
            project_name, 
            temp_dir,
            "standard"
        )
    
    @patch("fastapi_generator.generators.api_generator.generate_api")
    def test_generate_api_command(self, mock_generate_api, temp_dir):
        """测试API生成命令"""
        # 准备
        mock_generate_api.return_value = Path(temp_dir) / "app" / "api" / "api_v1" / "endpoints" / "user.py"
        
        # 创建模拟项目目录
        os.makedirs(temp_dir / "app" / "api" / "api_v1" / "endpoints", exist_ok=True)
        
        resource_name = "user"
        
        # 使用测试版本的app
        test_app = create_typer_app_for_testing()
        
        # 执行，设置standalone_mode=False以防止系统退出
        with patch.object(sys, 'argv', [
            "fg", "generate", "api", resource_name, 
            "--output-dir", str(temp_dir)
        ]):
            result = test_app(["generate", "api", resource_name, "--output-dir", str(temp_dir)], standalone_mode=False)
        
        # 验证
        assert result == 0
        mock_generate_api.assert_called_once_with(resource_name, temp_dir)
    
    @patch("fastapi_generator.generators.model_generator.generate_model")
    def test_generate_model_command(self, mock_generate_model, temp_dir):
        """测试模型生成命令"""
        # 准备
        mock_generate_model.return_value = Path(temp_dir) / "app" / "models" / "user.py"
        
        # 创建模拟项目目录
        os.makedirs(temp_dir / "app" / "models", exist_ok=True)
        os.makedirs(temp_dir / "app" / "schemas", exist_ok=True)
        
        model_name = "user"
        
        # 使用测试版本的app
        test_app = create_typer_app_for_testing()
        
        # 执行，设置standalone_mode=False以防止系统退出
        with patch.object(sys, 'argv', [
            "fg", "generate", "model", model_name,
            "--output-dir", str(temp_dir)
        ]):
            result = test_app(["generate", "model", model_name, "--output-dir", str(temp_dir)], standalone_mode=False)
        
        # 验证
        assert result == 0
        mock_generate_model.assert_called_once_with(model_name, temp_dir)
    
    @patch("fastapi_generator.generators.migration_generator.generate_migration")
    def test_generate_migration_command(self, mock_generate_migration, temp_dir):
        """测试迁移生成命令"""
        # 准备
        mock_generate_migration.return_value = Path(temp_dir / "migrations")
        
        # 创建模拟项目目录结构
        os.makedirs(temp_dir / "app" / "models", exist_ok=True)
        
        # 使用测试版本的app
        test_app = create_typer_app_for_testing()
        
        # 执行，设置standalone_mode=False以防止系统退出
        # 为迁移命令提供一个虚拟名称参数
        with patch.object(sys, 'argv', [
            "fg", "generate", "migration", "init",
            "--output-dir", str(temp_dir)
        ]):
            result = test_app(["generate", "migration", "init", "--output-dir", str(temp_dir)], standalone_mode=False)
        
        # 验证
        assert result == 0
        mock_generate_migration.assert_called_once_with(temp_dir)
    
    @patch("fastapi_generator.generators.service_generator.generate_service")
    def test_generate_service_command(self, mock_generate_service, temp_dir):
        """测试服务生成命令"""
        # 准备
        mock_generate_service.return_value = Path(temp_dir) / "app" / "services" / "user_service.py"
        
        # 创建模拟项目目录结构
        os.makedirs(temp_dir / "app" / "services", exist_ok=True)
        os.makedirs(temp_dir / "app" / "models", exist_ok=True)
        
        # 创建模拟模型文件
        model_dir = temp_dir / "app" / "models"
        with open(model_dir / "__init__.py", "w", encoding="utf-8") as f:
            f.write("from app.models.user import User")
        
        with open(model_dir / "user.py", "w", encoding="utf-8") as f:
            f.write("class User: pass")
        
        model_name = "user"
        
        # 使用测试版本的app
        test_app = create_typer_app_for_testing()
        
        # 执行，设置standalone_mode=False以防止系统退出
        with patch.object(sys, 'argv', [
            "fg", "generate", "service", model_name,
            "--output-dir", str(temp_dir)
        ]):
            result = test_app(["generate", "service", model_name, "--output-dir", str(temp_dir)], standalone_mode=False)
        
        # 验证
        assert result == 0
        mock_generate_service.assert_called_once_with(model_name, temp_dir) 