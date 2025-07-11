# PyPI Publishing Guide

This document explains how to use GitHub Actions to automatically publish fastapi-generator to PyPI.

## Prerequisites

### 1. Create a PyPI Account

If you don't already have a PyPI account, register at the [PyPI website](https://pypi.org/account/register/).

### 2. Generate PyPI API Token

1. Log in to your PyPI account
2. Visit [Account Settings](https://pypi.org/manage/account/)
3. In the "API Tokens" section, click "Add API token"
4. Enter a token name (e.g., github-actions-fastapi-generator)
5. Choose the scope (it's recommended to select a specific project: fastapi-generator)
6. Click the "Create" button
7. Save the displayed token (this is the only time you'll see the complete token)

### 3. Add PyPI API Token to GitHub Repository

1. Go to your GitHub repository
2. Click "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Enter name: `PYPI_API_TOKEN`
5. Enter value: The PyPI API Token you just generated
6. Click "Add secret" to save

## Publishing Process

We have configured a GitHub Actions workflow that automatically publishes the package to PyPI when you create a new release.

### Steps to Publish a New Version

1. **Update Version Number**

   Edit the `src/fastapi_generator/__init__.py` file and update the `__version__` variable:

   ```python
   __version__ = "x.y.z"  # Replace x.y.z with the new version number
   ```

2. **Update CHANGELOG**

   If you have a CHANGELOG file, record the changes for this version.

3. **Commit and Push Changes**

   ```bash
   git add .
   git commit -m "Bump version to x.y.z"
   git push origin main
   ```

4. **Create a Release Tag**

   On your GitHub repository page:
   - Click "Releases" > "Draft a new release"
   - Enter a tag version, e.g., `v0.1.0`
   - Fill in the release title, e.g., `FastAPI Generator v0.1.0`
   - Add release notes in the description
   - Click "Publish release"

5. **Monitor the Publishing Process**

   - After creating the release, GitHub Actions will automatically run the publishing workflow
   - You can check the progress in the "Actions" tab of your repository
   - Once the workflow completes successfully, the package will be published to PyPI

### Manual Publishing (Alternative Method)

If you need to publish manually, you can use the following commands:

```bash
# Install publishing tools
pip install build twine

# Build the package
python -m build

# Check the build
twine check dist/*

# Publish to PyPI
twine upload dist/*
```

## Common Issues

1. **Publishing Failure**
   - Check GitHub Actions logs for error messages
   - Verify that the PyPI API Token is valid
   - Confirm that the package version has been updated (PyPI doesn't allow overwriting published versions)

2. **Version Conflict**
   - PyPI does not allow uploading a package with the same version number more than once
   - You must update the `__version__` variable for each release

3. **Package Build Issues**
   - Check that `pyproject.toml` and `setup.py` are configured correctly
   - Ensure `MANIFEST.in` includes all necessary files

## Test Publishing

Before publishing to the official PyPI, you can first publish to TestPyPI:

1. Register for a [TestPyPI account](https://test.pypi.org/account/register/)
2. Generate a TestPyPI API Token
3. Modify the GitHub Actions configuration to target TestPyPI
4. Create a test version release

After successfully publishing and testing installation from TestPyPI, proceed with publishing to the official PyPI. 