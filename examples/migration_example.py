#!/usr/bin/env python3
"""
数据库迁移功能示例

本示例展示如何使用FastAPI Generator的数据库迁移功能。
"""
from pathlib import Path
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_generator.generators.migration_generator import generate_migration, update_config_for_migrations

def main():
    """
    运行迁移功能示例
    """
    # 创建示例项目目录
    project_dir = Path("./example_project")
    if not project_dir.exists():
        project_dir.mkdir(parents=True)
    
    # 创建必要的目录结构
    app_dir = project_dir / "app"
    db_dir = app_dir / "db"
    core_dir = app_dir / "core"
    
    for dir_path in [app_dir, db_dir, core_dir]:
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
    
    # 生成迁移配置
    print("生成数据库迁移配置...")
    migrations_dir = generate_migration(project_dir)
    print(f"迁移配置已生成: {migrations_dir}")
    
    # 更新配置文件
    print("更新配置文件...")
    config_path = update_config_for_migrations(project_dir)
    print(f"配置文件已更新: {config_path}")
    
    print("\n迁移配置生成完成！")
    print("\n接下来，你可以使用以下命令创建和应用迁移:")
    print("  cd example_project")
    print("  alembic revision --autogenerate -m \"创建初始表\"")
    print("  alembic upgrade head")

if __name__ == "__main__":
    main() 