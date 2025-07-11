# PyPI发布指南

本文档介绍如何使用GitHub Actions自动发布fastapi-generator到PyPI。

## 准备工作

### 1. 创建PyPI账号

如果你还没有PyPI账号，请前往[PyPI官网](https://pypi.org/account/register/)注册。

### 2. 生成PyPI API Token

1. 登录你的PyPI账号
2. 访问[账号设置](https://pypi.org/manage/account/)
3. 在"API令牌"部分，点击"添加API令牌"
4. 输入令牌名称（例如：github-actions-fastapi-generator）
5. 选择范围（建议选择特定项目：fastapi-generator）
6. 点击"创建"按钮
7. 保存显示的令牌（这是唯一一次可以看到完整令牌的机会）

### 3. 添加PyPI API Token到GitHub仓库

1. 进入GitHub仓库
2. 点击"Settings" > "Secrets and variables" > "Actions"
3. 点击"New repository secret"
4. 名称填写：`PYPI_API_TOKEN`
5. 值填写：刚才生成的PyPI API Token
6. 点击"Add secret"保存

## 发布流程

我们已经配置了GitHub Actions工作流，当你创建新版本发布时，会自动将包发布到PyPI。

### 发布新版本的步骤

1. **更新版本号**

   编辑`src/fastapi_generator/__init__.py`文件，更新`__version__`变量：

   ```python
   __version__ = "x.y.z"  # 将x.y.z替换为新版本号
   ```

2. **更新CHANGELOG**

   如果有CHANGELOG文件，记录此版本的更新内容。

3. **提交并推送更改**

   ```bash
   git add .
   git commit -m "Bump version to x.y.z"
   git push origin main
   ```

4. **创建发布标签**

   在GitHub仓库页面：
   - 点击"Releases" > "Draft a new release"
   - 输入标签版本，例如：`v0.1.0`
   - 标题填写发布版本，例如：`FastAPI Generator v0.1.0`
   - 描述中添加版本更新内容
   - 点击"Publish release"

5. **监控发布过程**

   - 创建发布后，GitHub Actions将自动运行发布工作流
   - 可以在仓库的"Actions"标签页查看发布进度
   - 工作流成功完成后，包将发布到PyPI

### 手动发布（备选方案）

如果需要手动发布，可以使用以下命令：

```bash
# 安装发布工具
pip install build twine

# 构建包
python -m build

# 检查构建结果
twine check dist/*

# 发布到PyPI
twine upload dist/*
```

## 常见问题

1. **发布失败**
   - 检查GitHub Actions日志查找错误信息
   - 验证PyPI API Token是否有效
   - 确认包版本号是否已更新（PyPI不允许覆盖已发布的版本）

2. **版本冲突**
   - PyPI不允许重复上传相同版本号的包
   - 每次发布必须更新`__version__`变量

3. **包构建问题**
   - 检查`pyproject.toml`和`setup.py`配置是否正确
   - 确保`MANIFEST.in`包含所有必要文件

## 测试发布

在发布到正式PyPI之前，可以先发布到TestPyPI进行测试：

1. 注册[TestPyPI账号](https://test.pypi.org/account/register/)
2. 生成TestPyPI API Token
3. 修改GitHub Actions配置，将发布目标改为TestPyPI
4. 创建测试版本发布

成功在TestPyPI发布并安装测试后，再发布到正式PyPI。 