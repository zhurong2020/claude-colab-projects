#!/usr/bin/env python3
"""
本地OCR功能测试脚本
用于验证医疗OCR项目在本地环境的运行情况
"""

import warnings
warnings.filterwarnings("ignore")


def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")

    try:
        import google.colab  # noqa: F401
        print("✅ 运行在Google Colab")
        in_colab = True
    except ImportError:
        print("✅ 运行在本地环境")
        in_colab = False

    try:
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"✅ 计算设备: {device}")
        if device == 'cuda':
            print(f"✅ GPU型号: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("ℹ️ PyTorch未安装，使用CPU模式")

    return in_colab


def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")

    required_packages = [
        ('pandas', 'pd'),
        ('PIL', 'Image'),
        ('paddleocr', 'PaddleOCR'),
        ('cv2', 'cv2'),
    ]

    missing_packages = []

    for package_name, import_name in required_packages:
        try:
            if import_name == 'Image':
                from PIL import Image  # noqa: F401
            elif import_name == 'PaddleOCR':
                from paddleocr import PaddleOCR  # noqa: F401
            elif import_name == 'pd':
                import pandas as pd  # noqa: F401
            else:
                exec(f"import {import_name}")
            print(f"✅ {package_name} 已安装")
        except ImportError:
            print(f"❌ {package_name} 未安装")
            missing_packages.append(package_name)

    return missing_packages


def create_test_image():
    """创建测试图像"""
    print("\n🎨 创建测试图像...")

    try:
        from PIL import Image, ImageDraw

        # 创建简单测试图像
        img = Image.new('RGB', (800, 400), color='white')
        draw = ImageDraw.Draw(img)

        # 添加边框
        draw.rectangle([(10, 10), (790, 390)], outline='black', width=2)

        # 测试文本
        test_texts = [
            "Medical OCR Test",
            "Patient: John Doe",
            "Date: 2025-08-17",
            "Diagnosis: Test Case"
        ]

        # 绘制文本
        y_pos = 50
        for text in test_texts:
            draw.text((50, y_pos), text, fill='black')
            y_pos += 60

        # 保存图像
        test_image_path = '../data/test_medical_doc.png'
        img.save(test_image_path)
        print(f"✅ 测试图像已创建: {test_image_path}")

        return test_image_path

    except Exception as e:
        print(f"❌ 测试图像创建失败: {e}")
        return None


def test_ocr_functionality(image_path):
    """测试OCR功能"""
    print("\n🔬 测试OCR功能...")

    try:
        from paddleocr import PaddleOCR

        # 初始化OCR引擎
        print("⚡ 初始化PaddleOCR引擎...")
        ocr = PaddleOCR(use_angle_cls=True, lang='en')

        # 执行OCR识别
        print(f"📄 处理图像: {image_path}")
        result = ocr.ocr(image_path)

        # 提取结果
        extracted_texts = []
        if result and len(result) > 0 and result[0] is not None:
            for line in result[0]:
                if (line and len(line) >= 2
                    and line[1] and len(line[1]) >= 2
                        and isinstance(line[1][0], str)):

                    text = line[1][0]
                    confidence = line[1][1]

                    if text and text.strip():
                        extracted_texts.append({
                            'text': text.strip(),
                            'confidence': confidence
                        })

        # 显示结果
        print("\n📊 OCR识别结果:")
        print("-" * 50)

        if extracted_texts:
            for i, item in enumerate(extracted_texts, 1):
                print(f"{i:2d}. {item['text']} (置信度: {item['confidence']:.3f})")
            print(f"\n✅ 成功识别 {len(extracted_texts)} 行文字")
        else:
            print("⚠️ 未识别到任何文字")

        return extracted_texts

    except Exception as e:
        print(f"❌ OCR测试失败: {e}")
        return []


def test_gradio_interface():
    """测试Gradio界面"""
    print("\n🌐 测试Gradio界面...")

    try:
        import gradio as gr
        print("✅ Gradio已安装")

        def simple_echo(text):
            return f"Echo: {text}"

        # 创建简单界面
        interface = gr.Interface(
            fn=simple_echo,
            inputs=gr.Textbox(label="输入测试"),
            outputs=gr.Textbox(label="输出结果"),
            title="🏥 医疗OCR本地测试",
            description="Gradio界面本地运行测试"
        )

        print("✅ Gradio界面创建成功")
        print("💡 运行 interface.launch() 可启动Web界面")

        return interface

    except Exception as e:
        print(f"❌ Gradio测试失败: {e}")
        return None


def main():
    """主测试函数"""
    print("🏥 医疗OCR项目本地测试")
    print("=" * 40)

    # 检查环境
    check_environment()

    # 检查依赖
    missing_packages = check_dependencies()

    if missing_packages:
        print(f"\n⚠️ 缺少依赖包: {', '.join(missing_packages)}")
        print("💡 请运行: pip install -r requirements-dev.txt")
        return

    # 创建测试图像
    test_image = create_test_image()

    if test_image:
        # 测试OCR功能
        ocr_results = test_ocr_functionality(test_image)

        if ocr_results:
            print("\n✅ OCR功能测试成功")

    # 测试Gradio界面
    test_gradio_interface()

    print("\n🎉 本地测试完成!")
    print("\n💡 使用方法:")
    print("1. 直接运行此脚本: python test_local_ocr.py")
    print("2. 启动完整项目: ./start_local.sh")
    print("3. 手动启动: source venv/bin/activate && python -m jupyter notebook")


if __name__ == "__main__":
    main()
