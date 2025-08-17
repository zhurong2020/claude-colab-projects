# Claude Code + Google Colab 项目集合

> 使用Claude Code开发，Google Colab运行的项目集合

## 🎯 项目概述

这是一个多项目管理仓库，专注于：
- **本地开发**: VSCode + Claude Code智能辅助
- **云端运行**: Google Colab免费GPU资源
- **便捷分享**: 一键生成Colab演示链接
- **版本管理**: 完整的Git工作流支持

## 📁 项目结构

```
claude-colab-projects/
├── demos/                    # 演示项目（集中管理）
├── standalone/               # 独立项目（完整结构）
├── templates/               # 项目模板
├── shared/                  # 共享资源
├── tools/                   # 管理工具
└── docs/                    # 文档
```

## 🚀 快速开始

### 创建新的演示项目
```bash
cd claude-colab-projects
python tools/project_organizer.py demo your-project-name --desc "项目描述"
```

### 创建独立项目
```bash
python tools/project_organizer.py standalone your-project-name --desc "项目描述"
```

### 同步到GitHub并生成Colab链接
```bash
python tools/sync_tool.py full username/repo-name -m "更新说明"
```

## 📓 演示项目

<!-- 演示项目列表会自动更新 -->

## 🏗️ 独立项目

<!-- 独立项目列表会自动更新 -->

## 🛠️ 工具使用

### 项目管理工具
```bash
# 查看所有项目
python tools/project_organizer.py list

# 生成Colab链接
python tools/project_organizer.py links username/repo-name
```

### 同步工具
```bash
# 同步到GitHub
python tools/sync_tool.py sync -m "提交信息"

# 生成Colab链接
python tools/sync_tool.py links username/repo-name

# 完整流程
python tools/sync_tool.py full username/repo-name -m "提交信息"
```

## 📖 开发工作流

1. **创建项目**: 使用项目管理工具创建新项目
2. **本地开发**: 使用VSCode + Claude Code编辑代码
3. **测试验证**: 本地或Colab中测试功能
4. **同步分享**: 推送到GitHub并生成Colab链接

## 🎯 最佳实践

- **演示项目**: 单一功能展示，代码简洁
- **独立项目**: 完整功能实现，结构清晰
- **版本管理**: 及时提交，清晰的提交信息
- **文档编写**: 详细的使用说明和示例

## 📞 联系方式

如有问题或建议，欢迎反馈交流。

---

*使用 Claude Code + Google Colab 构建 🚀*