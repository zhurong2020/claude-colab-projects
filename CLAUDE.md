# Claude Code 项目约定和配置

## 📋 项目概述

本项目是一个医疗文档OCR识别演示项目，使用PaddleOCR进行中文医疗文档的文字识别，并提供结构化的CSV输出。

**当前版本**: v1.3.13 (重组notebook结构优化用户体验和消除重复功能)  
**更新时间**: 2025-08-24

## 🛠️ 开发约定

### 版本管理
- 使用语义化版本号 (Semantic Versioning)
- 格式: `主版本.次版本.修订版本`
- **强制要求**: 每次bug修复或功能改进都必须更新版本号
- **最小版本递增原则**: 每次修订都要进行最小的版本号更新，便于观察版本变化
- **必须同步更新**: notebook第一个cell中的版本信息和CLAUDE.md中的当前版本
- **版本号规则**: 
  - 修订版本(+0.0.1): bug修复、错误处理改进、调试信息增强
  - 次版本(+0.1.0): 新功能添加、API改进
  - 主版本(+1.0.0): 重大架构变更、不兼容更新
- **版本描述**: 版本号后必须添加简短描述说明本次更新内容
- **版本追踪**: 每次更新都必须明确标记版本号变化，方便用户确认使用最新版本

### Git提交规范
- 使用中文commit message
- 格式: `动作 + 具体内容 + 版本号`
- 每次commit都包含Claude Code签名
- 修复/改进后立即提交并推送到远程仓库
- **版本标记**: commit message必须包含明确的版本号，便于版本追踪

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
- 开发依赖: mypy, flake8, jupyter, gradio
- 保持依赖最新且兼容
- **必须使用虚拟环境**: 项目强制要求使用Python虚拟环境隔离依赖

## 📁 项目结构 (v1.3.0 重组后)

```
claude-colab-projects/
├── demos/                      # 演示应用目录 (多小型应用架构)
│   ├── medical-ocr/           # 医疗OCR识别应用 (独立可运行)
│   │   ├── medical-ocr-demo.ipynb  # 主演示notebook
│   │   ├── gradio_demo.py          # Web界面版本
│   │   ├── test_chinese_encoding_fix.py  # 中文编码测试
│   │   ├── assets/                 # 应用专用资源
│   │   │   ├── sample_docs/        # 示例医疗文档
│   │   │   ├── results/           # OCR识别结果
│   │   │   └── samples/           # 其他示例文件
│   │   └── README.md              # 应用说明文档
│   ├── shared/                # 共享资源和工具
│   │   ├── utils/             # 通用工具函数
│   │   ├── fonts/             # 共享字体文件
│   │   └── templates/         # 共享模板
│   ├── dev-tools/             # 开发辅助工具 (非演示)
│   │   ├── generators/        # 文档生成器
│   │   │   ├── create_chinese_medical_doc.py
│   │   │   ├── create_mixed_document.py
│   │   │   └── create_mixed_language_doc.py
│   │   └── legacy-tests/      # 历史测试脚本
│   │       ├── test_chinese_ocr.py
│   │       ├── test_mixed_ocr_final.py
│   │       └── test_ocr_fix.py
│   └── README.md              # demos总导航文档
├── standalone/                # 大型独立项目目录
├── shared/                    # 项目级共享资源
│   ├── utils/                 # 通用工具函数
│   └── assets/                # 共享资源文件
├── templates/                 # 项目模板目录
├── tools/                     # 项目管理工具
│   ├── project_organizer.py  # 项目智能组织工具
│   └── sync_tool.py          # 同步工具
├── tests/                     # 测试目录
│   ├── unit/                  # 单元测试
│   │   └── test_local_ocr.py  # 本地OCR功能测试
│   ├── data/                  # 测试数据
│   │   └── test_medical_doc.png  # 测试用医疗文档
│   └── README.md              # 测试说明
├── docs/                      # 文档目录
├── venv/                      # Python虚拟环境目录
├── .vscode/                   # VSCode配置
├── start_local.sh              # 本地环境一键启动脚本
├── README_LOCAL.md             # 本地运行指南
├── claude-colab-integration-guide.md # 集成指南
├── SESSION_HANDOVER.md         # 对话交接文档
├── requirements-dev.txt        # 开发依赖
└── CLAUDE.md                   # 本文件
```

## 🏗️ 项目架构重组 (v1.3.0)

### 重组背景
v1.3.0进行了重大架构重构，将demos目录从杂乱的单一目录重组为面向多小型应用的清晰结构。

### 设计原则
1. **独立性**: 每个演示应用可独立在Google Colab中运行
2. **可扩展性**: 便于添加新的演示应用
3. **关注点分离**: 演示、开发工具、共享资源分离
4. **Colab友好**: 结构适合云端同步和运行

### 重组成果
- ✅ **医疗OCR应用独立化**: `demos/medical-ocr/` 包含完整功能
- ✅ **资源合理归类**: 图片、结果、工具分类存放
- ✅ **开发工具分离**: 生成器和测试工具不干扰演示
- ✅ **文档体系完善**: 多层级README导航系统
- ✅ **路径引用优化**: 所有文件路径适配新结构

### 应用结构规范
每个演示应用目录应包含：
```
应用名称/
├── 主演示文件.ipynb     # Jupyter notebook
├── 辅助脚本.py          # 可选的Python脚本
├── assets/              # 应用专用资源
│   ├── sample_docs/     # 示例文档
│   └── results/         # 输出结果
└── README.md            # 应用说明
```

## 🔧 IDE配置

### VSCode设置
- **Python解释器**: 自动配置为`./venv/bin/python`
- **终端自动激活**: 新建终端自动激活虚拟环境
- **调试配置**: 包含OCR演示和测试的预设配置
- **任务配置**: 一键运行测试、类型检查、代码风格检查

### IDE启动方式
```bash
# 方式1: 使用workspace文件（推荐）
code claude-colab-projects.code-workspace

# 方式2: 直接打开项目目录
code .
```

### 类型检查配置
- 忽略第三方库的类型检查错误
- 对项目代码进行严格的类型检查
- 使用mypy进行静态类型分析
- IDE终端自动显示虚拟环境提示符

## 🏠 本地开发环境

### 虚拟环境管理
- **强制要求**: 所有开发工作必须在Python虚拟环境中进行
- **自动激活**: 启动脚本会自动创建和激活虚拟环境
- **环境隔离**: 避免系统Python环境污染和依赖冲突
- **版本一致**: 确保团队成员使用相同的依赖版本

### 本地运行约定
```bash
# 1. 一键启动 (推荐方式)
./start_local.sh

# 2. 手动启动
source venv/bin/activate && jupyter notebook

# 3. 功能测试
source venv/bin/activate && cd tests/unit && python test_local_ocr.py

# 4. Web界面演示
source venv/bin/activate && cd demos && python gradio_demo.py
```

### 环境检查清单
- ✅ Python 3.12+ 已安装
- ✅ 虚拟环境已创建 (`venv/` 目录存在)
- ✅ 依赖包已安装 (运行 `test_local_ocr.py` 验证)
- ✅ GPU支持检测 (自动识别CUDA设备)
- ✅ PaddleOCR模型已下载

## 📝 开发工作流

1. **环境准备**: 使用 `./start_local.sh` 确保虚拟环境就绪
2. **代码修改**: 按照项目约定进行开发
3. **功能测试**: 运行 `test_local_ocr.py` 验证核心功能
4. **质量检查**: 在虚拟环境中运行lint和typecheck
5. **解决问题**: 修复所有IDE PROBLEMS
6. **版本更新**: 同步更新CLAUDE.md和notebook中的版本号及描述
7. **调试增强**: 每次修订适当增加调试信息，便于确切定位问题
8. **本地验证**: 先进行本地测试确认功能正常
9. **提交推送**: 使用规范的commit message

## 🚨 注意事项

- **虚拟环境必须**: 禁止在系统Python环境中安装项目依赖
- **启动脚本优先**: 优先使用 `./start_local.sh` 确保环境一致性
- **环境验证**: 开发前运行 `test_local_ocr.py` 确保环境正确
- **版本递增强制**: 每次修订都必须更新版本号，无论修改大小
- **本地测试优先**: 所有修改都必须先本地验证后再提交
- **调试信息充分**: 适当增加调试输出，便于问题定位和排查
- 每次重大修改后需要重启IDE以刷新类型检查
- 确保Jupyter notebook在本地和Colab环境的兼容性
- 保持中文注释和文档的准确性
- GPU模式优先，CPU模式作为备用方案

## 📞 技术支持

- GitHub仓库: https://github.com/zhurong2020/claude-colab-projects
- 使用Claude Code进行开发和维护
- 遵循防御性安全开发原则

---
*本文档随项目发展持续更新*