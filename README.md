# FastAPI Generator

[![EN](https://img.shields.io/badge/Language-English-blue)](README.md)
[![中文](https://img.shields.io/badge/语言-中文-red)](README_CN.md)

A FastAPI project code generation tool that makes FastAPI development simpler, faster, and more standardized.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-Personal-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

## 📖 Project Introduction

FastAPI Generator is a code generation tool designed specifically for the FastAPI framework, aiming to simplify the creation and development process of FastAPI projects. By providing standardized project structures, templates, and code generation features, it helps developers quickly build high-quality FastAPI applications.

## 🚀 Quick Start

### Installation

```bash
# Install from source code
git clone https://github.com/your-username/fastapi-generator.git
cd fastapi-generator
pip install -e .

# Or install directly
pip install fastapi-generator
```

### Usage

```bash
# Create a new project
fg create my-project

# Use a specific template
fg create my-project --template standard

# Generate a module
fg generate module user-management

# Generate API endpoints
fg generate api user --methods crud

# Run the project
fg run

# View help
fg --help
```

## 📋 Features

### Project Creation
- ✅ Standard FastAPI project structure
- 🔄 Microservice project templates
- 🔄 API gateway templates
- 🔄 Monolithic application templates
- 🔄 Frontend-backend separation templates

### Code Generation
- 🔄 Module generator
- 🔄 API endpoint generator
- 🔄 Data model generator
- 🔄 Service layer generator
- 🔄 Test code generator

### Development Tools
- ✅ Project validation
- ✅ Dependency management
- ✅ Code formatting
- ✅ Project cleanup
- 🔄 Automated testing

## 🎯 User Stories

### Quick Project Creation
**As a** Python developer  
**I want** to quickly create a new FastAPI project  
**So that** I can immediately start developing business logic

```bash
fg create my-api --template standard
# Complete project creation in 5 minutes, saving 95% time
```

### Generate Business Modules
**As a** business developer  
**I want** to quickly generate common business modules  
**So that** I can focus on implementing business logic

```bash
fg generate module user-management
# Complete module development in 1 hour, saving 87% time
```

### Generate API Endpoints
**As an** API developer  
**I want** to quickly generate RESTful API endpoints  
**So that** I can quickly build API services

```bash
fg generate api user --methods crud
# Complete API development in 30 minutes, saving 87% time
```

## 📁 Project Structure

```
fastapi_generator/
├── src/fastapi_generator/     # Source code
│   ├── cli/                   # Command line interface
│   ├── core/                  # Core engine
│   ├── generators/            # Code generators
│   ├── templates/             # Template system
│   ├── file_system/           # File system
│   └── utils/                 # Utility functions
├── tests/                     # Test files
├── examples/                  # Usage examples
├── docs/                      # Documentation
└── scripts/                   # Script files
```

## 🛠️ Development Guide

### Environment Setup

```bash
# Clone the project
git clone https://github.com/your-username/fastapi-generator.git
cd fastapi-generator

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
ruff check src tests
```

### Adding New Features

1. Create a new generator under `src/fastapi_generator/generators/`
2. Inherit from the `BaseGenerator` class
3. Implement the `generate()` and `validate_context()` methods
4. Add corresponding CLI commands
5. Write test cases

## 📊 Performance Metrics

- **Project Creation Time**: < 30 seconds
- **Module Generation Time**: < 1 minute
- **API Generation Time**: < 30 seconds
- **Memory Usage**: < 100MB
- **Startup Time**: < 3 seconds

## 🎯 Development Plan

### Phase One (Completed)
- ✅ Project initialization functionality
- ✅ Standard project templates
- ✅ Basic CLI commands
- ✅ File system management

### Phase Two (In Progress)
- 🔄 Module generator
- 🔄 API endpoint generator
- 🔄 Data model generator
- 🔄 Template system

### Phase Three (Planned)
- ⏸️ Plugin system
- ⏸️ Advanced templates
- ⏸️ Batch operations
- ⏸️ Cloud-native deployment

## 🤝 Project Status

This is a personal project maintained by yggai. External code contributions are not accepted. If you have suggestions or find issues, please submit them through GitHub Issues.

## 📄 License

This project is licensed under a personal license - see the [LICENSE](LICENSE) file for details.

**Important**: Commercial use requires explicit authorization from the author. Please contact via email: pygosuperman@outlook.com for commercial licensing.

## 📞 Support and Contact

- 📧 Email: generator@example.com
- 🐛 Issue Reporting: [GitHub Issues](https://github.com/your-username/fastapi-generator/issues)
- 📖 Documentation: [Project Documentation](docs/)

---

**Making FastAPI development simpler, faster, and more standardized!** 🚀 