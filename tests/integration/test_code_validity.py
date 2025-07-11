"""
生成代码有效性测试
验证生成的代码能否正确运行
"""
import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
import pytest

from typer.testing import CliRunner


class TestCodeValidity:
    """生成代码有效性测试类"""
    
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
    
    def test_generated_code_syntax(self, runner, temp_dir):
        """测试生成的代码语法正确性"""
        project_name = "syntax_test_project"
        
        # 创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name, 
            "--output", str(temp_dir)
        ]
        subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        
        project_dir = temp_dir / project_name
        
        # 生成模型
        model_name = "user"
        model_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "model", model_name, 
            "--output", str(project_dir)
        ]
        subprocess.run(model_cmd, capture_output=True, text=True, check=True)
        
        # 生成API
        api_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "api", model_name, 
            "--output", str(project_dir)
        ]
        subprocess.run(api_cmd, capture_output=True, text=True, check=True)
        
        # 生成迁移
        migration_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "migration", "init", 
            "--output", str(project_dir)
        ]
        subprocess.run(migration_cmd, capture_output=True, text=True, check=True)
        
        # 检查Python语法
        python_files = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        for py_file in python_files:
            # 使用Python编译器检查语法
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", py_file],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"语法错误 in {py_file}: {result.stderr}"
    
    def test_main_app_imports(self, runner, temp_dir):
        """测试主应用导入正确性"""
        project_name = "import_test_project"
        
        # 创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name, 
            "--output", str(temp_dir)
        ]
        subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        
        project_dir = temp_dir / project_name
        
        # 测试main.py的导入
        main_py = project_dir / "main.py"
        
        # 创建一个临时Python文件来测试导入
        test_import_py = project_dir / "test_import.py"
        with open(test_import_py, "w", encoding="utf-8") as f:
            f.write(f"""
import sys
sys.path.append('{project_dir}')
try:
    import main
    print("Main import successful")
except Exception as e:
    print(f"Import error: {{e}}")
    exit(1)
""")
        
        # 执行导入测试
        result = subprocess.run(
            [sys.executable, str(test_import_py)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"导入错误: {result.stderr}"
        assert "Main import successful" in result.stdout
    
    def test_model_schema_compatibility(self, runner, temp_dir):
        """测试模型和Schema的兼容性"""
        project_name = "model_schema_test"
        
        # 创建项目
        create_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "create", project_name, 
            "--output", str(temp_dir)
        ]
        subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        
        project_dir = temp_dir / project_name
        
        # 生成模型
        model_name = "product"
        model_cmd = [
            sys.executable, "-m", "fastapi_generator.cli.main", 
            "generate", "model", model_name, 
            "--output", str(project_dir)
        ]
        subprocess.run(model_cmd, capture_output=True, text=True, check=True)
        
        # 创建一个临时Python文件来测试模型和Schema的兼容性
        test_model_py = project_dir / "test_model.py"
        with open(test_model_py, "w", encoding="utf-8") as f:
            f.write(f"""
import sys
sys.path.append('{project_dir}')
try:
    from app.models.{model_name} import {model_name.capitalize()}
    from app.schemas.{model_name} import {model_name.capitalize()}Create, {model_name.capitalize()}Response
    
    # 创建模型实例
    model_instance = {model_name.capitalize()}(
        name="Test {model_name.capitalize()}",
        description="Test description",
        price=10.0
    )
    
    # 测试Schema创建
    create_data = {model_name.capitalize()}Create(
        name="Test {model_name.capitalize()}",
        description="Test description",
        price=10.0
    )
    
    # 测试模型转Schema
    response_data = {model_name.capitalize()}Response.model_validate(model_instance)
    
    print("Model and Schema compatibility test passed")
except Exception as e:
    print(f"Compatibility error: {{e}}")
    exit(1)
""")
        
        # 执行兼容性测试
        result = subprocess.run(
            [sys.executable, str(test_model_py)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"兼容性错误: {result.stderr}"
        assert "Model and Schema compatibility test passed" in result.stdout 