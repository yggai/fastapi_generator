# Installation Guide

This document provides detailed steps for installing FastAPI Generator.

## System Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv or conda recommended)

## Installation Methods

### 1. Install from PyPI (Recommended)

```bash
pip install fastapi-generator
```

### 2. Install from Source

#### Clone the Repository

```bash
git clone https://github.com/yggai/fastapi_generator.git
cd fastapi_generator
```

#### Create and Activate a Virtual Environment

```bash
# Using venv (Python 3.8+)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

#### Install Dependencies

```bash
pip install -e .
```

This will install FastAPI Generator in development mode, allowing any changes to the source code to take effect immediately.

#### Verify Installation

```bash
fg --version
```

If the installation was successful, you will see the version information of FastAPI Generator.

## Development Environment Setup

If you want to contribute to FastAPI Generator or do development work, install the development dependencies:

```bash
pip install -e ".[dev]"
```

This will install all development tools such as testing frameworks, code formatting tools, etc.

## Common Issues

### Installation Failures

If you encounter problems during installation, try the following steps:

1. Make sure your pip is up to date:
   ```bash
   pip install --upgrade pip
   ```

2. If dependency installation fails, try installing dependencies separately:
   ```bash
   pip install fastapi sqlmodel typer jinja2 pydantic rich
   ```

3. Check if your Python version meets the requirements:
   ```bash
   python --version
   ```

### Permission Issues

If you encounter permission issues, try using the `--user` flag:

```bash
pip install --user fastapi-generator
```

Or use sudo on Linux/Mac (not recommended):

```bash
sudo pip install fastapi-generator
```

## Updating

To update to the latest version, run:

```bash
pip install --upgrade fastapi-generator
```

## Uninstalling

If you need to uninstall FastAPI Generator, run:

```bash
pip uninstall fastapi-generator
``` 