# 医疗文档OCR识别项目

> 🏥 使用PaddleOCR进行中文医疗文档文字识别，支持本地开发和Colab运行

**当前版本**: v1.3.36 (修复PaddleOCR变量未定义和PIL导入警告) | **更新时间**: 2025-08-26

## 🎯 项目概述

这是一个医疗文档OCR识别演示项目，特色功能：
- **高精度识别**: 基于PaddleOCR的中英文混合识别
- **本地开发**: 完整的Python虚拟环境和一键启动
- **云端运行**: Google Colab免费GPU资源支持
- **Web界面**: Gradio交互式界面
- **数据导出**: 结构化CSV格式输出

## 📁 项目结构

```
claude-colab-projects/
├── demos/                      # 演示应用目录
│   ├── medical-ocr/           # 医疗OCR识别应用 (独立可运行)
│   │   ├── medical-ocr-demo.ipynb  # 主演示notebook
│   │   ├── gradio_demo.py          # Web界面版本
│   │   ├── test_chinese_encoding_fix.py  # 中文编码测试
│   │   └── assets/                 # 应用资源文件
│   ├── shared/                # 共享资源和工具
│   └── dev-tools/             # 开发辅助工具
├── standalone/                # 大型独立项目目录
├── shared/                    # 项目级共享资源
├── tests/                     # 测试目录
├── tools/                     # 项目管理工具
├── venv/                      # Python虚拟环境
├── .vscode/                   # VSCode配置
├── start_local.sh             # 本地环境一键启动
├── requirements-dev.txt       # 开发依赖
└── CLAUDE.md                  # 项目约定和配置
```

## 🚀 快速开始

### 本地运行（推荐）
```bash
# 一键启动（自动处理虚拟环境）
./start_local.sh

# 选择启动方式：
# 1) Jupyter Notebook (默认)
# 2) Gradio Web界面演示  
# 3) 仅激活虚拟环境
```

### Google Colab运行
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zhurong2020/claude-colab-projects/blob/main/demos/medical-ocr/medical-ocr-demo.ipynb)

### 手动安装
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements-dev.txt

# 运行测试
python test_local_ocr.py
```

## ✨ 功能特性

### 🔍 OCR识别能力
- **多语言支持**: 中英文混合识别
- **高精度引擎**: 基于PaddleOCR v3.1+
- **GPU加速**: 支持CUDA加速处理
- **角度矫正**: 自动检测和矫正文档角度

### 📊 数据处理
- **结构化输出**: 生成CSV格式报告
- **置信度评估**: 每行文字的识别置信度
- **批量处理**: 支持多图像文件处理
- **错误处理**: 完善的异常处理机制

### 🌐 用户界面
- **Jupyter Notebook**: 交互式开发环境
- **Gradio Web界面**: 用户友好的Web界面
- **命令行工具**: 脚本化批量处理
- **实时预览**: 识别结果即时显示

## 🛠️ 技术栈

- **OCR引擎**: PaddleOCR 3.1+
- **深度学习**: PaddlePaddle
- **图像处理**: OpenCV, PIL
- **数据处理**: Pandas
- **Web界面**: Gradio
- **开发环境**: Jupyter Notebook
- **代码质量**: MyPy, Flake8

## 📖 使用场景

- **医疗档案**: 病历、处方、检查报告数字化
- **文档管理**: 纸质文档电子化归档
- **数据录入**: 批量文字识别和录入
- **质量控制**: OCR结果置信度评估

## 🔧 开发说明

### 环境要求
- Python 3.8+
- 2GB+ RAM (推荐4GB+)
- GPU支持 (可选，提升处理速度)

### 代码质量
- 遵循PEP 8代码风格
- 类型注解完整
- 单元测试覆盖
- 文档字符串完备

### 版本管理
- 使用语义化版本号
- 详细的提交信息
- 分支管理策略
- 自动化CI/CD

## 📞 技术支持

- **GitHub仓库**: [zhurong2020/claude-colab-projects](https://github.com/zhurong2020/claude-colab-projects)
- **问题反馈**: 通过GitHub Issues提交
- **开发文档**: 查看 [CLAUDE.md](./CLAUDE.md) 了解开发约定
- **本地运行**: 参考 [README_LOCAL.md](./README_LOCAL.md)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

*使用 Claude Code 开发，支持本地和Colab运行 🚀*