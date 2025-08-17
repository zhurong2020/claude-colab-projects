# 测试目录

本目录包含项目的测试代码和测试数据。

## 📁 目录结构

```
tests/
├── unit/                    # 单元测试
│   └── test_local_ocr.py   # OCR功能本地测试
├── data/                   # 测试数据
│   └── test_medical_doc.png # 测试用医疗文档图像
└── README.md              # 本文件
```

## 🧪 运行测试

### 本地OCR功能测试
```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
cd tests/unit
python test_local_ocr.py
```

## 📝 测试说明

- **test_local_ocr.py**: 验证PaddleOCR在本地环境的运行情况
- **test_medical_doc.png**: 测试用的示例医疗文档图像

## 🎯 测试覆盖

- [x] OCR引擎初始化
- [x] GPU支持检测
- [x] 图像文字识别功能
- [x] CSV结果输出
- [ ] 批量处理功能（待添加）
- [ ] 错误处理机制（待添加）

---
*遵循软件工程最佳实践的测试组织结构*