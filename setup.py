#!/usr/bin/env python3
"""
FastAPI Generator 安装配置
"""

from setuptools import setup, find_packages
import os
import re

# 读取版本信息
with open("src/fastapi_generator/__init__.py", "r", encoding="utf-8") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("无法找到版本信息")

# 读取README.md作为长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fastapi-generator",
    version=version,
    description="FastAPI项目代码生成工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="源滚滚AI编程",
    author_email="pygosuperman@outlook.com",
    url="https://github.com/yggai/fastapi_generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.100.0",
        "sqlmodel>=0.0.8",
        "typer>=0.9.0",
        "jinja2>=3.1.2",
        "pydantic>=2.0.0",
        "click>=8.1.3",
        "rich>=13.5.0",
    ],
    entry_points={
        "console_scripts": [
            "fg=fastapi_generator.cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="fastapi, generator, code generator, api, rest, sqlmodel",
) 