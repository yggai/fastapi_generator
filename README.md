# FastAPI Generator

一个用于快速生成FastAPI项目和组件的命令行工具。

## 功能特点

- 创建标准FastAPI项目结构
- 生成API端点（CRUD操作）
- 生成数据模型（使用SQLModel）
- 生成服务层代码
- 数据库迁移（使用Alembic）
- 模块化和可扩展的设计

## 安装

```bash
# 从源码安装
git clone https://github.com/yggai/fastapi_generator.git
cd fastapi_generator
pip install -e .
```

## 使用方法

### 创建新项目

```bash
# 创建一个名为"my-project"的新项目
fg create my-project

# 使用特定模板创建项目
fg create my-project --template enterprise
```

### 生成API

```bash
# 生成用户API
fg generate api user
```

### 生成数据模型

```bash
# 生成用户模型
fg generate model user
```

### 生成服务

```bash
# 生成用户服务
fg generate service user
```

### 数据库迁移

```bash
# 初始化数据库迁移
fg init-migration

# 生成迁移配置
fg generate migration initial
```

## 项目结构

```
fastapi_generator/
├── src/
│   └── fastapi_generator/
│       ├── cli/                # 命令行接口
│       ├── core/               # 核心功能
│       ├── generators/         # 代码生成器
│       ├── templates/          # 项目模板
│       └── utils/              # 工具函数
├── tests/                      # 测试
├── setup.py                    # 安装配置
└── pyproject.toml              # 项目配置
```

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

## 许可证

MIT 