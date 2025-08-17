#!/bin/bash

# 医疗OCR项目本地环境启动脚本
# 根据CLAUDE.md约定，强制使用虚拟环境进行开发

set -e  # 遇到错误立即退出

echo "🏥 医疗OCR项目本地环境启动器"
echo "========================================"
echo "📋 根据CLAUDE.md约定，强制使用虚拟环境"
echo ""

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "❌ Python版本过低 (当前: $PYTHON_VERSION, 要求: >= $REQUIRED_VERSION)"
    echo "💡 请升级Python版本后重试"
    exit 1
fi

echo "✅ Python版本检查通过: $PYTHON_VERSION"

# 强制虚拟环境检查
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        echo "💡 请确保python3-venv已安装: sudo apt install python3-venv"
        exit 1
    fi
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "⚡ 激活虚拟环境..."
source venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ 虚拟环境激活失败"
    exit 1
fi

echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"

# 升级pip
echo "🔄 更新pip..."
pip install --upgrade pip > /dev/null 2>&1

# 检查关键依赖
echo "🔍 检查依赖安装状态..."
MISSING_DEPS=()

if ! pip show jupyter > /dev/null 2>&1; then
    MISSING_DEPS+=("jupyter")
fi

if ! pip show paddleocr > /dev/null 2>&1; then
    MISSING_DEPS+=("paddleocr")
fi

if ! pip show gradio > /dev/null 2>&1; then
    MISSING_DEPS+=("gradio")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "📥 安装缺失的依赖包: ${MISSING_DEPS[*]}"
    pip install -r requirements-dev.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 所有依赖已安装"
fi

# 环境验证
echo "🧪 运行环境验证..."
cd tests/unit
python test_local_ocr.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 环境验证通过"
else
    echo "⚠️ 环境验证有警告，但将继续启动"
fi
cd ../..

# 提供启动选项
echo ""
echo "🎯 请选择启动方式:"
echo "1) Jupyter Notebook (默认)"
echo "2) Gradio Web界面演示"
echo "3) 仅激活虚拟环境"
echo ""
read -p "请输入选择 (1-3，回车默认选择1): " choice

case $choice in
    2)
        echo "🌐 启动Gradio Web界面..."
        echo "💡 访问 http://localhost:7860 查看界面"
        echo "🛑 按 Ctrl+C 停止服务"
        cd demos/medical-ocr && python gradio_demo.py
        ;;
    3)
        echo "⚡ 虚拟环境已激活，可以手动运行命令"
        echo "💡 使用以下命令："
        echo "   - 测试功能: cd tests/unit && python test_local_ocr.py"
        echo "   - 启动Jupyter: jupyter notebook"
        echo "   - 启动Gradio: cd demos/medical-ocr && python gradio_demo.py"
        echo "🛑 输入 'deactivate' 退出虚拟环境"
        bash
        ;;
    *)
        echo "📚 启动Jupyter Notebook..."
        echo "💡 浏览器将自动打开，或手动访问显示的URL"
        echo "🛑 按 Ctrl+C 停止服务"
        echo ""
        
        # 检查notebook是否存在
        if [ ! -f "demos/medical-ocr/medical-ocr-demo.ipynb" ]; then
            echo "❌ notebook文件不存在: demos/medical-ocr/medical-ocr-demo.ipynb"
            echo "💡 启动Jupyter主界面..."
            jupyter notebook
        else
            jupyter notebook demos/medical-ocr/medical-ocr-demo.ipynb
        fi
        ;;
esac