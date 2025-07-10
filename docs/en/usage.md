# Usage Guide

This document provides detailed instructions for using FastAPI Generator.

## Command Line Tool

FastAPI Generator provides a command-line tool called `fg` for creating projects and generating code.

### View Help

```bash
fg --help
```

### Check Version

```bash
fg --version
```

## Creating a Project

### Basic Usage

```bash
fg create my-project
```

This will create a standard FastAPI project named `my-project` in the current directory.

### Specify Template

```bash
fg create my-project --template basic
```

Available templates include:
- `basic`: Basic template with minimal functionality
- `standard`: Standard template with common features and structure (default)
- `enterprise`: Enterprise-grade template with more comprehensive features and structure

### Specify Output Directory

```bash
fg create my-project --output /path/to/directory
```

## Generating APIs

### Basic Usage

```bash
fg generate api user
```

This will generate user-related API endpoints, including CRUD operations.

### Specify Output Directory

```bash
fg generate api user --output /path/to/directory
```

## Generating Data Models

### Basic Usage

```bash
fg generate model user
```

This will generate user-related data models and schemas.

### Specify Output Directory

```bash
fg generate model user --output /path/to/directory
```

## Generating Services

### Basic Usage

```bash
fg generate service user
```

This will generate user-related service layer code.

### Specify Output Directory

```bash
fg generate service user --output /path/to/directory
```

## Examples

### Create a Complete User Management System

```bash
# Create project
fg create user-management

# Change to project directory
cd user-management

# Generate user model
fg generate model user

# Generate user API
fg generate api user

# Generate user service
fg generate service user
```

### Create a Blog System

```bash
# Create project
fg create blog-system

# Change to project directory
cd blog-system

# Generate article model
fg generate model article

# Generate comment model
fg generate model comment

# Generate article API
fg generate api article

# Generate comment API
fg generate api comment

# Generate article service
fg generate service article

# Generate comment service
fg generate service comment
```

## Advanced Usage

### Using the Python API

In addition to the command-line tool, you can also use FastAPI Generator's API directly in Python code:

```python
from fastapi_generator.core.project_creator import create_project
from fastapi_generator.generators.model_generator import generate_model
from fastapi_generator.generators.api_generator import generate_api
from fastapi_generator.generators.service_generator import generate_service

# Create project
project_dir = create_project("my-project", template="standard")

# Generate model
generate_model("user", output_dir=project_dir / "app")

# Generate API
generate_api("user", output_dir=project_dir / "app" / "api" / "api_v1" / "endpoints")

# Generate service
generate_service("user", output_dir=project_dir / "app" / "services")
```

For more examples, see the `examples` directory. 