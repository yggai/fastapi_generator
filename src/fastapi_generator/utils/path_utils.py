"""
路径工具函数
"""
import os
from pathlib import Path
from typing import Optional

def get_package_root() -> Path:
    """
    获取包的根目录
    """
    # 当前文件所在的目录
    current_dir = Path(__file__).parent
    
    # 包的根目录 (fastapi_generator)
    return current_dir.parent

def get_templates_dir() -> Path:
    """
    获取模板目录路径
    """
    return get_package_root() / "templates"

def ensure_dir_exists(dir_path: Path) -> Path:
    """
    确保目录存在，如果不存在则创建它
    
    Args:
        dir_path: 要确保存在的目录路径
        
    Returns:
        目录路径
    """
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def find_project_root(start_dir: Optional[Path] = None) -> Optional[Path]:
    """
    从给定目录开始向上查找项目根目录
    项目根目录定义为包含 pyproject.toml、setup.py 或 main.py 的最近目录
    
    Args:
        start_dir: 起始目录，默认为当前工作目录
        
    Returns:
        项目根目录路径，如果没有找到则返回None
    """
    if start_dir is None:
        start_dir = Path.cwd()
    
    current_dir = start_dir.absolute()
    
    # 向上查找，直到找到项目标记文件或达到文件系统根目录
    while True:
        # 检查是否存在项目标记文件
        for marker in ["pyproject.toml", "setup.py", "main.py"]:
            if (current_dir / marker).exists():
                return current_dir
        
        # 检查是否存在app目录，这是FastAPI项目的典型结构
        if (current_dir / "app").exists() and (current_dir / "app").is_dir():
            return current_dir
        
        # 移动到父目录
        parent_dir = current_dir.parent
        
        # 如果已经到达根目录，停止查找
        if parent_dir == current_dir:
            return None
        
        current_dir = parent_dir 