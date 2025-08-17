#!/usr/bin/env python3
"""
Claude Code 项目智能组织工具
专注于集中管理演示项目的快速创建和管理
"""

import json
import subprocess
from pathlib import Path

class ProjectOrganizer:
    def __init__(self, base_dir: str = "/home/wuxia/projects/claude-colab-projects"):
        self.base_dir = Path(base_dir)
        self.structure = {
            'demos': self.base_dir / 'demos',
            'standalone': self.base_dir / 'standalone', 
            'templates': self.base_dir / 'templates',
            'shared': self.base_dir / 'shared',
            'tools': self.base_dir / 'tools',
            'docs': self.base_dir / 'docs'
        }
        
        # 确保目录存在
        for dir_path in self.structure.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def create_demo_project(self, name: str, description: str = ""):
        """创建演示项目（集中管理模式）"""
        notebook_path = self.structure['demos'] / f"{name}.ipynb"
        
        print(f"📋 创建演示项目: {name}")
        print(f"📍 位置: {notebook_path}")
        
        # 创建notebook内容
        content = self._get_demo_template(name, description)
        self._write_notebook(notebook_path, content)
        
        # 保存项目元数据
        self._save_project_metadata(name, 'demo', str(notebook_path), description)
        
        print(f"✅ 演示项目创建完成!")
        return notebook_path
    
    def create_standalone_project(self, name: str, description: str = ""):
        """创建独立项目（独立管理模式）"""
        project_dir = self.structure['standalone'] / name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📋 创建独立项目: {name}")
        print(f"📍 位置: {project_dir}")
        
        # 创建主notebook
        notebook_path = project_dir / f"{name}.ipynb"
        content = self._get_standalone_template(name, description)
        self._write_notebook(notebook_path, content)
        
        # 创建README
        readme_path = project_dir / "README.md"
        readme_content = self._get_readme_template(name, description)
        readme_path.write_text(readme_content, encoding='utf-8')
        
        # 创建requirements.txt
        req_path = project_dir / "requirements.txt"
        requirements_content = self._get_requirements_template()
        req_path.write_text(requirements_content, encoding='utf-8')
        
        # 创建.gitignore
        gitignore_path = project_dir / ".gitignore"
        gitignore_content = self._get_gitignore_template()
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        
        # 初始化git
        try:
            subprocess.run(['git', 'init'], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'Initial commit: {name}'], 
                         cwd=project_dir, check=True, capture_output=True)
            print("✅ Git仓库初始化完成")
        except subprocess.CalledProcessError:
            print("⚠️ Git初始化失败（可能需要配置Git用户信息）")
        
        # 保存项目元数据
        self._save_project_metadata(name, 'standalone', str(project_dir), description)
        
        print(f"✅ 独立项目创建完成!")
        return project_dir
    
    def list_projects(self):
        """列出所有项目"""
        print("\n📁 项目列表:")
        
        # 演示项目
        print("\n🎭 演示项目 (demos/):")
        demo_files = list(self.structure['demos'].glob("*.ipynb"))
        if demo_files:
            for nb in demo_files:
                print(f"   📓 {nb.stem}")
        else:
            print("   (暂无演示项目)")
        
        # 独立项目
        print("\n🏗️ 独立项目 (standalone/):")
        standalone_dirs = [d for d in self.structure['standalone'].iterdir() if d.is_dir()]
        if standalone_dirs:
            for proj_dir in standalone_dirs:
                print(f"   📁 {proj_dir.name}")
        else:
            print("   (暂无独立项目)")
    
    def get_colab_links(self, github_user: str, repo_name: str):
        """生成所有项目的Colab链接"""
        base_url = f"https://colab.research.google.com/github/{github_user}/{repo_name}/blob/main"
        
        print(f"\n🔗 Colab访问链接 ({github_user}/{repo_name}):")
        
        # 演示项目链接
        print("\n🎭 演示项目:")
        demo_files = list(self.structure['demos'].glob("*.ipynb"))
        if demo_files:
            for nb in demo_files:
                rel_path = nb.relative_to(self.base_dir)
                link = f"{base_url}/{rel_path}"
                print(f"   📓 {nb.stem}: {link}")
        else:
            print("   (暂无演示项目)")
        
        # 独立项目链接
        print("\n🏗️ 独立项目:")
        standalone_dirs = [d for d in self.structure['standalone'].iterdir() if d.is_dir()]
        if standalone_dirs:
            for proj_dir in standalone_dirs:
                for nb in proj_dir.glob("*.ipynb"):
                    rel_path = nb.relative_to(self.base_dir)
                    link = f"{base_url}/{rel_path}"
                    print(f"   📁 {proj_dir.name}: {link}")
        else:
            print("   (暂无独立项目)")
    
    def _get_demo_template(self, name: str, description: str) -> str:
        """获取演示项目notebook模板"""
        return f'''"""
{name} - 演示项目
{description}

🎯 使用Claude Code开发，Google Colab运行

📋 功能特性：
- 快速演示核心功能
- 优化的Colab运行体验  
- 简单易用的交互界面

🚀 使用说明：
1. 运行所有代码块
2. 根据提示输入参数
3. 查看运行结果
"""

# ================================
# 环境检查和基础设置
# ================================

import os
import sys
import warnings
warnings.filterwarnings("ignore")

def check_environment():
    """检查运行环境并显示系统信息"""
    print("🔍 检查运行环境...")
    
    # 检查是否在Colab环境
    try:
        import google.colab
        print("✅ 运行在Google Colab")
        in_colab = True
    except ImportError:
        print("ℹ️ 运行在本地环境")
        in_colab = False
    
    # 检查GPU（如果需要）
    try:
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"✅ 计算设备: {{device}}")
        if device == 'cuda':
            print(f"✅ GPU型号: {{torch.cuda.get_device_name(0)}}")
            print(f"✅ GPU内存: {{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}} GB")
    except ImportError:
        print("ℹ️ PyTorch未安装（如果不需要可忽略）")
        if in_colab:
            print("💡 需要时在Colab中运行: !pip install torch")
    
    return in_colab

# ================================
# 依赖安装
# ================================

def install_dependencies():
    """根据环境安装必要的依赖包"""
    in_colab = check_environment()
    
    if in_colab:
        print("📦 检查Colab环境依赖...")
        
        # 在此处添加项目特定的依赖安装
        # 示例：
        # import subprocess
        # import sys
        # packages = ['package1', 'package2']
        # for package in packages:
        #     try:
        #         __import__(package)
        #         print(f"✅ {{package}} 已安装")
        #     except ImportError:
        #         print(f"📥 安装 {{package}}...")
        #         subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        
        print("✅ 依赖检查完成")
    else:
        print("ℹ️ 本地环境请确保已安装项目依赖")

# ================================
# 主要功能实现
# ================================

def main_function():
    """主要业务逻辑"""
    print(f"🚀 {{name}} 启动成功!")
    
    # 在这里实现项目的主要功能
    print("💡 请在这里添加您的项目代码")
    
    # 示例代码框架：
    # 1. 数据加载
    # 2. 数据处理  
    # 3. 模型运行
    # 4. 结果展示
    
    return "功能演示完成"

# ================================
# 交互界面（可选）
# ================================

def create_interface():
    """创建简单的用户界面"""
    try:
        import gradio as gr
        
        def process_input(input_data):
            """处理用户输入"""
            # 在这里处理输入并返回结果
            result = f"处理结果: {{input_data}}"
            return result
        
        # 创建界面
        interface = gr.Interface(
            fn=process_input,
            inputs=gr.Textbox(label="输入", placeholder="请输入内容..."),
            outputs=gr.Textbox(label="输出结果"),
            title=f"{{name}}",
            description="{{description}}"
        )
        
        return interface
    except ImportError:
        print("❌ Gradio未安装，跳过界面创建")
        print("💡 如需界面功能，请运行: !pip install gradio")
        return None

# ================================
# 程序入口
# ================================

if __name__ == "__main__":
    print("="*50)
    print(f"   {{name}}")
    print("="*50)
    
    # 1. 环境检查和依赖安装
    install_dependencies()
    
    # 2. 运行主要功能
    result = main_function()
    print(f"\\n📊 运行结果: {{result}}")
    
    # 3. 创建交互界面（如果需要）
    interface = create_interface()
    if interface:
        print("\\n🌐 启动交互界面...")
        interface.launch(share=True)
    
    print("\\n✅ 演示完成!")
'''
    
    def _get_standalone_template(self, name: str, description: str) -> str:
        """获取独立项目notebook模板"""
        return f'''"""
{name}
{description}

🎯 使用Claude Code开发，Google Colab运行的独立项目

开发环境：
- 本地：VSCode + Claude Code
- 云端：Google Colab

使用说明：
1. 运行环境检查
2. 执行主要功能
3. 查看运行结果
"""

# ================================
# 基础配置
# ================================

import os
import sys
import warnings
warnings.filterwarnings("ignore")

# 检查运行环境
def check_environment():
    """检查运行环境"""
    try:
        import google.colab
        print("✅ 运行在Google Colab")
        return True
    except ImportError:
        print("ℹ️ 运行在本地环境")
        return False

# ================================
# 主要功能
# ================================

def main():
    """主要业务逻辑"""
    print(f"🚀 {{name}} 启动成功!")
    
    # 检查环境
    in_colab = check_environment()
    
    # 在这里添加项目的主要代码
    print("💡 请在这里添加您的项目代码")
    
    return "运行完成"

# ================================
# 程序入口
# ================================

if __name__ == "__main__":
    result = main()
    print(f"结果: {{result}}")
'''
    
    def _get_readme_template(self, name: str, description: str) -> str:
        """获取README模板"""
        return f"""# {name}

> {description}

使用Claude Code开发，Google Colab运行的项目

## 🚀 快速开始

### 在Colab中运行
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/standalone/{name}/{name}.ipynb)

### 本地运行
```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO/standalone/{name}

# 安装依赖
pip install -r requirements.txt

# 启动Jupyter
jupyter notebook {name}.ipynb
```

## 📋 功能特性

- ✅ 特性1：[描述功能]
- ✅ 特性2：[描述功能]
- ✅ 特性3：[描述功能]

## 🛠️ 技术栈

- **开发环境**: VSCode + Claude Code
- **运行环境**: Google Colab / Jupyter Notebook
- **主要技术**: Python

## 📖 使用说明

1. **环境准备**: 确保已安装Python 3.8+
2. **依赖安装**: 运行 `pip install -r requirements.txt`
3. **运行项目**: 在Colab中打开notebook或本地运行
4. **查看结果**: 运行所有代码块查看结果

---

*使用 Claude Code + Google Colab 构建 🚀*
"""
    
    def _get_requirements_template(self) -> str:
        """获取requirements.txt模板"""
        return """# 项目依赖包
# 基础依赖
jupyter>=1.0.0
ipython>=8.0.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0

# 根据项目需要添加其他依赖
# torch>=2.0.0
# transformers>=4.30.0
# gradio>=3.35.0
# requests>=2.30.0
"""
    
    def _get_gitignore_template(self) -> str:
        """获取.gitignore模板"""
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
data/
models/
logs/
outputs/
checkpoints/
*.pkl
*.pth
*.pt
*.h5
*.hdf5

# Large files
*.zip
*.tar.gz
*.rar
"""
    
    def _write_notebook(self, path: Path, content: str):
        """写入notebook文件"""
        # 创建基本的notebook结构
        notebook = {
            "nbformat": 4,
            "nbformat_minor": 0,
            "metadata": {
                "colab": {
                    "name": path.name,
                    "provenance": [],
                    "collapsed_sections": []
                },
                "kernelspec": {
                    "name": "python3",
                    "display_name": "Python 3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.8.0"
                }
            },
            "cells": [{
                "cell_type": "code",
                "metadata": {},
                "source": content.split('\n'),
                "execution_count": None,
                "outputs": []
            }]
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    def _save_project_metadata(self, name: str, project_type: str, location: str, description: str):
        """保存项目元数据"""
        metadata_file = self.base_dir / "projects.json"
        
        # 读取现有数据
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                projects = json.load(f)
        else:
            projects = {}
        
        # 添加新项目
        import datetime
        projects[name] = {
            'type': project_type,
            'location': location,
            'description': description,
            'created_date': datetime.datetime.now().isoformat()
        }
        
        # 保存
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Code 项目组织工具')
    subparsers = parser.add_subparsers(dest='action', help='操作类型')
    
    # 创建演示项目
    demo_parser = subparsers.add_parser('demo', help='创建演示项目')
    demo_parser.add_argument('name', help='项目名称')
    demo_parser.add_argument('--desc', default='', help='项目描述')
    
    # 创建独立项目
    standalone_parser = subparsers.add_parser('standalone', help='创建独立项目')
    standalone_parser.add_argument('name', help='项目名称')
    standalone_parser.add_argument('--desc', default='', help='项目描述')
    
    # 列出项目
    subparsers.add_parser('list', help='列出所有项目')
    
    # 生成链接
    links_parser = subparsers.add_parser('links', help='生成Colab链接')
    links_parser.add_argument('github_repo', help='GitHub仓库 (username/repo)')
    
    args = parser.parse_args()
    
    organizer = ProjectOrganizer()
    
    if args.action == 'demo':
        location = organizer.create_demo_project(args.name, args.desc)
        print(f"\n🎯 下一步:")
        print(f"   1. 使用Claude Code编辑: {location}")
        print(f"   2. 提交到GitHub")
        print(f"   3. 在Colab中运行")
        
    elif args.action == 'standalone':
        location = organizer.create_standalone_project(args.name, args.desc)
        print(f"\n🎯 下一步:")
        print(f"   1. cd {location}")
        print(f"   2. 使用Claude Code编辑代码")
        print(f"   3. git push到GitHub")
        print(f"   4. 在Colab中运行")
        
    elif args.action == 'list':
        organizer.list_projects()
        
    elif args.action == 'links':
        user, repo = args.github_repo.split('/')
        organizer.get_colab_links(user, repo)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()