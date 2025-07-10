# FastAPI Generator

[![EN](https://img.shields.io/badge/Language-English-blue)](README.md)
[![中文](https://img.shields.io/badge/语言-中文-red)](README_CN.md)

A command-line tool for quickly generating FastAPI projects and components.

## Features

- Create standard FastAPI project structures
- Generate API endpoints (CRUD operations)
- Generate data models (using SQLModel)
- Generate service layer code
- Database migrations (using Alembic)
- Modular and extensible design

## Installation

```bash
# Install from source
git clone https://github.com/yggai/fastapi_generator.git
cd fastapi_generator
pip install -e .
```

## Usage

### Create a New Project

```bash
# Create a new project named "my-project"
fg create my-project

# Create a project with a specific template
fg create my-project --template enterprise
```

### Generate API

```bash
# Generate user API
fg generate api user
```

### Generate Data Model

```bash
# Generate user model
fg generate model user
```

### Generate Service

```bash
# Generate user service
fg generate service user
```

### Database Migrations

```bash
# Initialize database migration
fg init-migration

# Generate migration configuration
fg generate migration initial
```

## Project Structure

```
fastapi_generator/
├── src/
│   └── fastapi_generator/
│       ├── cli/                # Command-line interface
│       ├── core/               # Core functionality
│       ├── generators/         # Code generators
│       ├── templates/          # Project templates
│       └── utils/              # Utility functions
├── tests/                      # Tests
├── setup.py                    # Installation configuration
└── pyproject.toml              # Project configuration
```

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

## Support the Project

If you find this project helpful, please consider supporting its development:

<img src="wxzf.jpg" alt="WeChat Payment QR Code" width="300"/>

*WeChat payment QR code: 源滚滚AI编程*

Your support helps maintain this project and develop new features!

## License

This project is under a personal license. For personal use (learning, research, and private projects), you are free to use this software. However, any commercial use requires explicit authorization from the author.

For commercial licensing, please contact: pygosuperman@outlook.com

See [LICENSE](LICENSE) for details. 