# Claude Code 项目约定和配置

## 📋 项目概述

本项目是一个医疗文档OCR识别演示项目，使用PaddleOCR进行中文医疗文档的文字识别，并提供结构化的CSV输出。

**当前版本**: v1.1.1 (修复API兼容性)  
**更新时间**: 2025-08-17

## 🛠️ 开发约定

### 版本管理
- 使用语义化版本号 (Semantic Versioning)
- 格式: `主版本.次版本.修订版本`
- 每次修复或改进都需要更新版本号
- 在notebook第一个cell中更新版本信息

### Git提交规范
- 使用中文commit message
- 格式: `动作 + 具体内容`
- 每次commit都包含Claude Code签名
- 修复/改进后立即提交并推送到远程仓库

### 代码质量要求
- 运行lint和typecheck命令确保代码质量
- 修复所有IDE PROBLEMS警告
- 使用类型注解提高代码可读性
- 添加必要的noqa标记避免误报

## 🧪 测试和构建

### 必须运行的命令
在代码修改后，请按顺序运行以下命令：

```bash
# 类型检查
python -m mypy demos/ --ignore-missing-imports

# 代码风格检查
python -m flake8 demos/ --max-line-length=100

# 如果有其他lint工具，请在此添加
```

### 依赖管理
- 核心依赖: paddlepaddle, paddleocr, pandas, pillow, opencv-python
- 开发依赖: mypy, flake8, jupyter
- 保持依赖最新且兼容

## 📁 项目结构

```
claude-colab-projects/
├── demos/                    # 演示项目目录
│   └── medical-ocr-demo.ipynb  # 医疗OCR演示notebook
├── .vscode/                  # VSCode配置
│   └── settings.json         # IDE设置
├── pyproject.toml           # Python项目配置
├── requirements-dev.txt     # 开发依赖
└── CLAUDE.md               # 本文件
```

## 🔧 IDE配置

### VSCode设置
- 启用Pylance类型检查
- 配置Python解释器
- 使用项目级别的设置覆盖全局设置

### 类型检查配置
- 忽略第三方库的类型检查错误
- 对项目代码进行严格的类型检查
- 使用mypy进行静态类型分析

## 📝 开发工作流

1. **环境检查**: 确保所有依赖正确安装
2. **代码修改**: 按照项目约定进行开发
3. **质量检查**: 运行lint和typecheck
4. **解决问题**: 修复所有IDE PROBLEMS
5. **版本更新**: 更新版本号和文档
6. **提交推送**: 使用规范的commit message

## 🚨 注意事项

- 每次重大修改后需要重启IDE以刷新类型检查
- 确保Jupyter notebook的兼容性
- 保持中文注释和文档的准确性
- 测试在Google Colab环境中的运行效果

## 📞 技术支持

- GitHub仓库: https://github.com/zhurong2020/claude-colab-projects
- 使用Claude Code进行开发和维护
- 遵循防御性安全开发原则

---
*本文档随项目发展持续更新*