#!/bin/bash

# 本地运行启动脚本
# 用于方便启动Jupyter notebook本地测试

echo "🚀 启动医疗OCR演示项目本地测试环境"
echo "========================================"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "⚡ 激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "🔍 检查依赖安装..."
pip show jupyter > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "📥 安装项目依赖..."
    pip install -r requirements-dev.txt
fi

# 启动Jupyter notebook
echo "📚 启动Jupyter Notebook..."
echo "💡 浏览器将自动打开，或手动访问显示的URL"
echo ""

jupyter notebook demos/medical-ocr-demo.ipynb