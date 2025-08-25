# 🚀 演示应用目录 (Demos)

本目录包含多个可独立运行的小型应用演示，每个应用都可以直接在Google Colab中运行。

## 📂 目录结构

```
demos/
├── medical-ocr/           # 医疗文档OCR识别应用
├── shared/               # 共享资源和工具
├── dev-tools/            # 开发辅助工具 (非演示)
└── README.md            # 本文件
```

## 🏥 可用演示应用

### 1. 医疗文档OCR识别 (`medical-ocr/`)

**功能**: 使用PaddleOCR对医疗文档进行文字识别和提取

**特性**:
- ✅ 支持中英文混合识别
- ✅ 高精度医疗术语识别  
- ✅ Web界面和Notebook两种使用方式
- ✅ 完善的中文编码处理
- ✅ 结构化CSV结果输出

**快速开始**:
- **Notebook版**: 打开 `medical-ocr/medical-ocr-demo.ipynb`
- **Web界面版**: 运行 `medical-ocr/gradio_demo.py`
- **测试工具**: 运行 `medical-ocr/test_chinese_encoding_fix.py`

**Colab链接**: [在Colab中打开](链接待更新)

## 🛠️ 共享资源

### `shared/` 目录
- **utils/**: 通用工具函数库
- **fonts/**: 共享字体文件
- **templates/**: 项目模板

### `dev-tools/` 目录 (开发者使用)
- **generators/**: 测试文档生成工具
- **legacy-tests/**: 历史测试脚本归档

## 🎯 使用指南

### 在本地运行
```bash
# 1. 激活虚拟环境
source ../venv/bin/activate

# 2. 进入应用目录
cd medical-ocr/

# 3. 运行演示
jupyter notebook medical-ocr-demo.ipynb
# 或
python gradio_demo.py
```

### 在Google Colab运行
1. 上传整个应用目录到Colab
2. 直接打开对应的 `.ipynb` 文件
3. 所有依赖资源都在同一目录下，无需额外配置

## 📋 版本历史

- **v1.3.17**: 彻底修复Colab中文字体显示和Gradio界面识别问题
- **v1.3.16**: 完全解决中文识别和PaddleOCR兼容性问题，统一版本管理
- **v1.3.15**: 修复OCR识别功能和优化用户体验，所有功能完全正常
- **v1.3.14**: 修复Cell顺序和Gradio界面缺失问题，优化IDE警告
- **v1.3.13**: 重组notebook结构优化用户体验和消除重复功能
- **v1.3.12**: 修复Gradio界面调试信息显示和清理不准确描述
- **v1.3.11**: 增强错误处理和调试信息
- **v1.3.2**: 修复IDE诊断问题和代码质量问题
- **v1.3.1**: 完成项目文件和配置的软件工程最佳实践整理
- **v1.3.0**: 完成demos目录软件工程最佳实践重组
- **v1.2.7**: 完全解决中文OCR识别显示问题

## 🤝 贡献指南

欢迎添加新的演示应用！请遵循以下规范：

1. **独立目录**: 每个应用创建独立目录
2. **完整性**: 确保应用可以独立运行
3. **文档**: 每个应用包含独立的README
4. **资源管理**: 将特定资源放在应用目录下
5. **共享优先**: 通用功能放入shared目录

## 📞 技术支持

- 项目地址: https://github.com/zhurong2020/claude-colab-projects
- 使用Claude Code进行开发和维护
- 遵循防御性安全开发原则

---
*📅 最后更新: 2025-08-25*
*🤖 使用 Claude Code 构建 v1.3.17*