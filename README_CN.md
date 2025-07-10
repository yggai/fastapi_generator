# FastAPI Generator

[![EN](https://img.shields.io/badge/Language-English-blue)](README.md)
[![中文](https://img.shields.io/badge/语言-中文-red)](README_CN.md)

FastAPI项目代码生成工具，让FastAPI开发更简单、更快速、更规范。

![版本](https://img.shields.io/badge/版本-0.1.0-blue)
![许可证](https://img.shields.io/badge/许可证-个人-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

## 📖 项目简介

FastAPI Generator是一款专为FastAPI框架设计的代码生成工具，旨在简化FastAPI项目的创建和开发流程。通过提供标准化的项目结构、模板和代码生成功能，帮助开发者快速搭建高质量的FastAPI应用。

## 🚀 快速开始

### 安装

```bash
# 从源码安装
git clone https://github.com/yggai/fastapi-generator.git
cd fastapi-generator
pip install -e .

# 或者直接安装
pip install fastapi-generator
```

### 使用

```bash
# 创建新项目
fg create my-project

# 使用指定模板
fg create my-project --template standard

# 生成模块
fg generate module user-management

# 生成API接口
fg generate api user --methods crud

# 运行项目
fg run

# 查看帮助
fg --help
```

## 📋 功能特性

### 项目创建
- ✅ 标准FastAPI项目结构
- 🔄 微服务项目模板
- 🔄 API网关模板
- 🔄 单体应用模板
- 🔄 前后端分离模板

### 代码生成
- 🔄 模块生成器
- 🔄 API接口生成器
- 🔄 数据模型生成器
- 🔄 服务层生成器
- 🔄 测试代码生成器

### 开发工具
- ✅ 项目验证
- ✅ 依赖管理
- ✅ 代码格式化
- ✅ 项目清理
- 🔄 自动化测试

## 🎯 用户故事

### 快速创建新项目
**作为** Python开发者  
**我希望** 能够快速创建一个新的FastAPI项目  
**以便** 立即开始业务逻辑开发

```bash
fg create my-api --template standard
# 5分钟内完成项目创建，节省95%时间
```

### 生成业务模块
**作为** 业务开发者  
**我希望** 能够快速生成常用的业务模块  
**以便** 专注于业务逻辑实现

```bash
fg generate module user-management
# 1小时内完成模块开发，节省87%时间
```

### 生成API接口
**作为** API开发者  
**我希望** 能够快速生成RESTful API接口  
**以便** 快速构建API服务

```bash
fg generate api user --methods crud
# 30分钟内完成API开发，节省87%时间
```

## 📁 项目结构

```
fastapi_generator/
├── src/fastapi_generator/     # 源代码
│   ├── cli/                   # 命令行接口
│   ├── core/                  # 核心引擎
│   ├── generators/            # 代码生成器
│   ├── templates/             # 模板系统
│   ├── file_system/           # 文件系统
│   └── utils/                 # 工具函数
├── tests/                     # 测试文件
├── examples/                  # 使用示例
├── docs/                      # 文档
└── scripts/                   # 脚本文件
```

## 🛠️ 开发指南

### 环境设置

```bash
# 克隆项目
git clone https://github.com/yggai/fastapi-generator.git
cd fastapi-generator

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src tests
ruff check src tests
```

### 添加新功能

1. 在`src/fastapi_generator/generators/`下创建新的生成器
2. 继承`BaseGenerator`类
3. 实现`generate()`和`validate_context()`方法
4. 添加相应的CLI命令
5. 编写测试用例

## 📊 性能指标

- **项目创建时间**: < 30秒
- **模块生成时间**: < 1分钟
- **API生成时间**: < 30秒
- **内存使用**: < 100MB
- **启动时间**: < 3秒

## 🎯 开发计划

### 第一阶段（已完成）
- ✅ 项目初始化功能
- ✅ 标准项目模板
- ✅ 基础CLI命令
- ✅ 文件系统管理

### 第二阶段（进行中）
- 🔄 模块生成器
- 🔄 API接口生成器
- 🔄 数据模型生成器
- 🔄 模板系统

### 第三阶段（计划中）
- ⏸️ 插件系统
- ⏸️ 高级模板
- ⏸️ 批量操作
- ⏸️ 云原生部署

## 🤝 项目状态

这是由yggai维护的个人项目，不接受外部代码贡献。如果您有建议或发现问题，请通过GitHub Issues提交。

## 📄 许可证

本项目采用个人许可证 - 查看[LICENSE](LICENSE)文件了解详情

**重要**: 商业用途需要获得作者的明确授权。请通过邮箱联系获取商业许可：pygosuperman@outlook.com

## 📞 支持与联系

- 📧 邮箱: generator@example.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/yggai/fastapi-generator/issues)
- 📖 文档: [项目文档](docs/)

## 💼 商业合作

如需商业使用授权、咨询或定制开发，请联系作者：

- 📱 电话: 18010070052
- 💬 微信: 扫描下面的二维码
- 🧑‍🏫 服务内容:
  - 一对一私教课培训
  - 企业项目定制开发
  - 技术咨询与解决方案

微信公众号:

![微信二维码](https://raw.githubusercontent.com/yggai/fastapi_generator/main/assets/vx.jpg)

---

**让FastAPI开发更简单、更快速、更规范！** 🚀 