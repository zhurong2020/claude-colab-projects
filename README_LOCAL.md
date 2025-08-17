# 医疗OCR项目本地运行指南

## 🚀 快速开始

### 1. 一键启动脚本
```bash
# 启动完整Jupyter notebook环境
./start_local.sh

# 启动简单的Gradio Web界面演示
source venv/bin/activate && python gradio_demo.py
```

### 2. 手动步骤

#### 环境准备
```bash
# 创建Python虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements-dev.txt
```

#### 运行测试
```bash
# 运行核心功能测试
python test_local_ocr.py

# 启动Gradio界面
python gradio_demo.py

# 启动Jupyter notebook
jupyter notebook demos/medical-ocr-demo.ipynb
```

## 📁 文件说明

- `start_local.sh` - 一键启动脚本
- `test_local_ocr.py` - 本地OCR功能测试
- `gradio_demo.py` - Gradio界面演示
- `requirements-dev.txt` - 开发环境依赖

## ✅ 验证环境

运行测试脚本检查环境是否正确配置：
```bash
source venv/bin/activate && python test_local_ocr.py
```

应该看到：
- ✅ 运行在本地环境
- ✅ 计算设备检测（CPU/GPU）
- ✅ 所有依赖包已安装
- ✅ OCR引擎初始化成功

## 🌐 Web界面访问

启动Gradio演示后，访问：
- 本地地址：http://localhost:7860
- 网络地址：http://0.0.0.0:7860

## 🔧 故障排除

### 依赖安装问题
```bash
# 如果遇到权限问题，使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### GPU支持
- 自动检测CUDA GPU
- 如无GPU，会自动降级到CPU模式
- PaddleOCR支持GPU加速

### 端口占用
```bash
# 检查端口占用
lsof -i :7860

# 或使用其他端口
python gradio_demo.py --port 8080
```

## 📊 性能对比

| 运行方式 | 启动速度 | 调试便利性 | GPU利用 | 网络要求 |
|---------|---------|-----------|---------|----------|
| 本地运行 | ⚡ 快速 | 🔧 优秀 | ✅ 支持 | ❌ 无需 |
| Colab运行 | 🐌 较慢 | 🔧 一般 | ✅ 支持 | ✅ 必需 |

## 💡 开发建议

1. **使用本地环境**进行快速开发和调试
2. **在Colab中**进行最终测试和演示
3. **虚拟环境**避免依赖冲突
4. **GPU模式**提升处理速度

## 🔗 相关链接

- [项目主页](https://github.com/zhurong2020/claude-colab-projects)
- [CLAUDE.md](./CLAUDE.md) - 项目约定
- [原始notebook](./demos/medical-ocr-demo.ipynb)

---
*使用Claude Code开发维护 🚀*