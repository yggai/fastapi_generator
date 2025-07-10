"""
测试数据库迁移生成器
"""
import os
import shutil
import tempfile
from pathlib import Path
import pytest

from fastapi_generator.generators.migration_generator import generate_migration, update_config_for_migrations


class TestMigrationGenerator:
    """测试数据库迁移生成器"""
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # 清理
        shutil.rmtree(temp_dir)
    
    def test_generate_migration(self, temp_dir):
        """测试生成迁移配置"""
        # 创建模拟的项目结构
        app_dir = temp_dir / "app"
        db_dir = app_dir / "db"
        os.makedirs(db_dir, exist_ok=True)
        
        # 生成迁移配置
        migrations_dir = generate_migration(temp_dir)
        
        # 验证生成的文件和目录
        assert migrations_dir.exists()
        assert (migrations_dir / "versions").exists()
        assert (migrations_dir / "env.py").exists()
        assert (migrations_dir / "README.md").exists()
        assert (migrations_dir / "__init__.py").exists()
        assert (migrations_dir / "versions" / "__init__.py").exists()
        
        # 验证生成的数据库相关文件
        assert (temp_dir / "alembic.ini").exists()
        assert (db_dir / "base.py").exists()
        
    def test_update_config_for_migrations(self, temp_dir):
        """测试更新配置文件"""
        # 创建模拟的配置文件
        core_dir = temp_dir / "app" / "core"
        os.makedirs(core_dir, exist_ok=True)
        
        # 创建一个简单的配置文件
        config_content = """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Test Project"
    DATABASE_URL: str = "sqlite:///./test.db"
    
settings = Settings()
"""
        config_path = core_dir / "config.py"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        
        # 更新配置
        updated_config_path = update_config_for_migrations(temp_dir)
        
        # 验证配置已更新
        assert updated_config_path.exists()
        
        # 读取更新后的配置
        with open(updated_config_path, "r", encoding="utf-8") as f:
            updated_content = f.read()
        
        # 验证新配置项已添加
        assert "DB_ECHO" in updated_content
        assert "DB_CONNECT_ARGS" in updated_content 