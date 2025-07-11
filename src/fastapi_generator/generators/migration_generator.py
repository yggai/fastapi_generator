"""
数据库迁移生成器模块
"""
from pathlib import Path
from typing import Optional
import os
import shutil
import subprocess
from jinja2 import Environment, FileSystemLoader

from fastapi_generator.utils.path_utils import ensure_dir_exists, find_project_root
from fastapi_generator.utils.string_utils import to_snake_case

# Alembic配置模板
ALEMBIC_INI_TEMPLATE = """# alembic.ini
[alembic]
script_location = migrations
prepend_sys_path = .
sqlalchemy.url = %(DATABASE_URL)s

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

# Alembic env.py模板
ALEMBIC_ENV_TEMPLATE = """# migrations/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 导入所有模型以便Alembic可以自动检测
from app.models import *
from app.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 从环境变量获取数据库URL
config.set_main_option("sqlalchemy.url", os.environ.get("DATABASE_URL", "sqlite:///./app.db"))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    # 在离线模式下运行迁移
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # 在在线模式下运行迁移
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

# Alembic README模板
ALEMBIC_README_TEMPLATE = """# 数据库迁移说明

本项目使用Alembic进行数据库迁移管理。

## 常用命令

### 创建迁移

```bash
# 自动生成迁移脚本
alembic revision --autogenerate -m "描述迁移的内容"

# 手动创建空白迁移脚本
alembic revision -m "描述迁移的内容"
```

### 应用迁移

```bash
# 升级到最新版本
alembic upgrade head

# 升级指定版本
alembic upgrade <revision>

# 升级指定步数
alembic upgrade +2

# 降级到上一个版本
alembic downgrade -1

# 降级到基础版本
alembic downgrade base
```

### 查看迁移信息

```bash
# 查看当前版本
alembic current

# 查看历史版本
alembic history

# 查看特定版本详情
alembic show <revision>
```
"""

# 修改后的数据库会话模板
DB_BASE_TEMPLATE = """\"\"\"
数据库基础配置
\"\"\"
from sqlalchemy.ext.declarative import declarative_base

# 创建SQLAlchemy基础模型
Base = declarative_base()
"""

DB_SESSION_TEMPLATE = """\"\"\"
数据库会话管理
\"\"\"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.core.config import settings
from app.db.base import Base

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # 在生产环境中设置为False
    connect_args=settings.DB_CONNECT_ARGS
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    \"\"\"初始化数据库，创建所有表\"\"\"
    # 在开发环境中可以使用这个函数创建表
    # 在生产环境中应该使用Alembic进行数据库迁移
    Base.metadata.create_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    \"\"\"获取数据库会话\"\"\"
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
"""

def generate_migration(output_dir: Optional[Path] = None) -> Path:
    """
    生成数据库迁移配置
    
    Args:
        output_dir: 输出目录，默认为当前项目根目录
        
    Returns:
        迁移配置目录路径
    """
    # 确定输出目录
    if output_dir is None:
        # 尝试找到项目根目录
        project_root = find_project_root()
        if project_root:
            output_dir = project_root
        else:
            # 如果找不到项目根目录，使用当前目录
            output_dir = Path.cwd()
    
    # 创建迁移目录结构
    migrations_dir = output_dir / "migrations"
    versions_dir = migrations_dir / "versions"
    
    # 确保目录存在
    ensure_dir_exists(migrations_dir)
    ensure_dir_exists(versions_dir)
    
    # 创建alembic.ini文件
    alembic_ini_path = output_dir / "alembic.ini"
    with open(alembic_ini_path, "w", encoding="utf-8") as f:
        f.write(ALEMBIC_INI_TEMPLATE)
    
    # 创建env.py文件
    env_py_path = migrations_dir / "env.py"
    with open(env_py_path, "w", encoding="utf-8") as f:
        f.write(ALEMBIC_ENV_TEMPLATE)
    
    # 创建README.md文件
    readme_path = migrations_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(ALEMBIC_README_TEMPLATE)
    
    # 创建空的versions目录下的__init__.py文件
    init_py_path = versions_dir / "__init__.py"
    with open(init_py_path, "w", encoding="utf-8") as f:
        f.write("# 迁移版本目录\n")
    
    # 创建migrations目录下的__init__.py文件
    init_py_path = migrations_dir / "__init__.py"
    with open(init_py_path, "w", encoding="utf-8") as f:
        f.write("# 迁移配置目录\n")
    
    # 创建或更新数据库基础文件
    db_dir = output_dir / "app" / "db"
    ensure_dir_exists(db_dir)
    
    # 创建base.py文件
    base_py_path = db_dir / "base.py"
    with open(base_py_path, "w", encoding="utf-8") as f:
        f.write(DB_BASE_TEMPLATE)
    
    # 更新session.py文件
    session_py_path = db_dir / "session.py"
    with open(session_py_path, "w", encoding="utf-8") as f:
        f.write(DB_SESSION_TEMPLATE)
    
    # 更新requirements.txt，添加alembic依赖
    requirements_path = output_dir / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, "r", encoding="utf-8") as f:
            requirements = f.read()
        
        # 检查是否已经包含alembic
        if "alembic" not in requirements:
            with open(requirements_path, "a", encoding="utf-8") as f:
                f.write("\n# 数据库迁移\nalembic>=1.12.0\n")
    
    # 尝试初始化alembic（如果已安装）
    try:
        subprocess.run(["alembic", "init", "migrations"], 
                      cwd=output_dir, 
                      check=False,
                      capture_output=True)
    except FileNotFoundError:
        # 如果alembic未安装，跳过此步骤
        pass
    
    return migrations_dir

def update_config_for_migrations(output_dir: Optional[Path] = None) -> Path:
    """
    更新配置文件以支持数据库迁移
    
    Args:
        output_dir: 输出目录，默认为当前项目根目录
        
    Returns:
        配置文件路径
    """
    # 确定输出目录
    if output_dir is None:
        # 尝试找到项目根目录
        project_root = find_project_root()
        if project_root:
            output_dir = project_root
        else:
            # 如果找不到项目根目录，使用当前目录
            output_dir = Path.cwd()
    
    # 更新配置文件
    config_dir = output_dir / "app" / "core"
    config_path = config_dir / "config.py"
    
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config_content = f.read()
        
        # 检查是否已经包含数据库连接参数
        if "DB_CONNECT_ARGS" not in config_content:
            # 寻找合适的位置插入新配置
            if "DATABASE_URL" in config_content:
                # 在DATABASE_URL后添加新配置
                lines = config_content.split("\n")
                new_lines = []
                for line in lines:
                    new_lines.append(line)
                    if "DATABASE_URL" in line and "DB_CONNECT_ARGS" not in config_content:
                        new_lines.append("    DB_ECHO: bool = False  # 是否显示SQL语句")
                        new_lines.append("    DB_CONNECT_ARGS: dict = {\"check_same_thread\": False}  # 仅用于SQLite")
                
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines))
    
    return config_path

if __name__ == "__main__":
    # 测试生成迁移配置
    migrations_dir = generate_migration()
    print(f"迁移配置已生成: {migrations_dir}")
    
    # 更新配置
    config_path = update_config_for_migrations()
    print(f"配置已更新: {config_path}") 