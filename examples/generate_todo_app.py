#!/usr/bin/env python3
"""
示例脚本：生成一个简单的待办事项应用

此脚本展示了如何使用FastAPI Generator创建一个简单的待办事项应用。
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from fastapi_generator.core.project_creator import create_project
from fastapi_generator.generators.model_generator import generate_model
from fastapi_generator.generators.api_generator import generate_api
from fastapi_generator.generators.service_generator import generate_service

def main():
    """
    主函数：生成待办事项应用
    """
    # 创建输出目录
    output_dir = Path.cwd() / "todo_app"
    if output_dir.exists():
        print(f"错误: 目录已存在: {output_dir}")
        return
    
    # 创建项目
    print("1. 创建项目...")
    project_dir = create_project("todo_app", output_dir=output_dir.parent, template="standard")
    print(f"   项目创建成功: {project_dir}")
    
    # 创建服务目录
    services_dir = project_dir / "app" / "services"
    os.makedirs(services_dir, exist_ok=True)
    
    # 生成Todo模型
    print("2. 生成Todo模型...")
    model_file = generate_model("Todo", output_dir=project_dir / "app")
    print(f"   模型生成成功: {model_file}")
    
    # 生成Todo服务
    print("3. 生成Todo服务...")
    service_file = generate_service("Todo", output_dir=services_dir)
    print(f"   服务生成成功: {service_file}")
    
    # 生成Todo API
    print("4. 生成Todo API...")
    api_file = generate_api("Todo", output_dir=project_dir / "app" / "api" / "api_v1" / "endpoints")
    print(f"   API生成成功: {api_file}")
    
    print("\n✅ 待办事项应用生成完成!")
    print(f"   项目路径: {project_dir}")
    print("\n运行应用:")
    print(f"   cd {project_dir}")
    print("   pip install -r requirements.txt")
    print("   python main.py")
    print("\n访问API文档: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main() 