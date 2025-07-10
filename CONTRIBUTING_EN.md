# Contribution Guidelines

Thank you for your interest in the FastAPI Generator project! We welcome and encourage contributions from community members. This document provides guidelines for participating in project development and helps you submit high-quality code.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Commit Conventions](#commit-conventions)
- [Branch Management](#branch-management)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Version Guidelines](#version-guidelines)

## Code of Conduct

Please respect all project contributors and users. We expect all participants to create a friendly and inclusive environment.

## How to Contribute

There are many ways to contribute, including but not limited to:

- Reporting bugs
- Submitting feature requests
- Writing or improving documentation
- Submitting code fixes or new features
- Participating in community discussions

### Reporting Bugs or Submitting Requests

1. Use GitHub Issues
2. Use the provided Issue templates
3. Describe the problem or request in detail
4. Provide steps to reproduce or use cases

## Development Process

1. Fork the project repository
2. Clone your forked repository locally
   ```bash
   git clone https://github.com/YOUR-USERNAME/fastapi-generator.git
   cd fastapi-generator
   ```
3. Add the upstream repository
   ```bash
   git remote add upstream https://github.com/original-owner/fastapi-generator.git
   ```
4. Create a new branch
   ```bash
   git checkout -b feature/your-feature
   ```
5. Develop your changes
6. Commit your code
7. Create a Pull Request

## Commit Conventions

We follow a structured commit message format, which helps with automatic changelog generation and understanding the purpose of commits.

### Commit Message Format

```
<type>(<scope>): <short description>

<detailed description>

<reference to related issues>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes only
- **style**: Changes that do not affect code meaning (whitespace, formatting, missing semicolons, etc.)
- **refactor**: Code changes that neither fix bugs nor add features
- **perf**: Code changes that improve performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies (example: pip, docker, npm)
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Scope

Specifies the area of the project affected (optional):

- **core**: Core engine
- **cli**: Command-line interface
- **generator**: Code generators
- **template**: Template system
- **fs**: File system
- **util**: Utility functions

### Example

```
feat(generator): Add module generation feature

Implements functionality to automatically generate module code from templates
Supports custom templates and parameter configuration

Closes #123
```

## Branch Management

### Branch Naming Conventions

- **main/master**: Main branch, kept in stable, releasable state
- **dev**: Development branch, contains the latest development code
- **feature/xxx**: Feature branches, used for developing new features
- **fix/xxx**: Fix branches, used for bug fixes
- **release/x.x.x**: Release branches, used to prepare version releases
- **hotfix/xxx**: Hotfix branches, used for urgent production environment fixes

### Workflow

1. Create feature branches from the `dev` branch
2. Develop on the feature branch
3. Submit a PR to the `dev` branch when complete
4. After review and testing, merge into `dev`
5. Periodically merge the `dev` branch into the `main` branch and release versions

## Pull Request Process

### PR Title Format

PR titles should follow the same format as commit messages:
```
<type>(<scope>): <short description>
```

### PR Description Content

- **Feature introduction or problem description**: Explain what problem this PR solves or what feature it adds
- **Solution description**: Briefly describe the implementation approach
- **Related test content**: Describe what tests were added to verify functionality
- **Screenshots or examples**: If applicable, provide screenshots of UI changes or examples of feature usage
- **Related issues**: Link related issues using keywords (e.g., "Closes #123")

### PR Checklist

- [ ] Code style conforms to project standards
- [ ] Necessary tests have been added
- [ ] All tests pass
- [ ] Related documentation has been updated
- [ ] Code has no obvious bugs or security issues

### PR Review Process

1. At least one project maintainer must review
2. All automated tests must pass
3. Resolve all issues raised during review
4. Project maintainers are responsible for merging the PR

## Code Standards

### Python Code Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards
- Use [Black](https://github.com/psf/black) for code formatting
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Use type annotations
- Write clear docstrings
- Maximum line length of 88 characters

### Automated Checks

The project has pre-commit hooks configured that automatically run the following checks before commit:

- Black formatting
- Ruff linting
- MyPy type checking
- Test execution

## Testing Guidelines

- Write unit tests for all new features
- Maintain test coverage above 80%
- Test code should be placed in the `tests/` directory
- Use pytest to run tests

```bash
pytest
```

## Documentation Guidelines

- All public APIs must have docstrings
- Follow [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Update README and other documentation to reflect code changes
- Provide usage examples for complex features

## Version Guidelines

We follow [Semantic Versioning (SemVer)](https://semver.org/):

- **Major version**: When making incompatible API changes
- **Minor version**: When adding backward-compatible functionality
- **Patch version**: When making backward-compatible bug fixes

For example: 1.2.3 represents major version 1, minor version 2, and patch version 3

---

Thank you again for contributing to the FastAPI Generator project! If you have any questions, please feel free to ask in GitHub Issues or contact the project maintainers. 