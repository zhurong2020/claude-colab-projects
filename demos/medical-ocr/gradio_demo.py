#!/usr/bin/env python3
"""
Gradio界面演示脚本
用于测试Gradio界面在本地环境的运行情况
"""

import warnings
warnings.filterwarnings("ignore")


def create_simple_gradio_demo():
    """创建简单的Gradio演示界面"""
    import gradio as gr
    from PIL import Image, ImageDraw

    def process_test_image(image):
        """处理测试图像的简单函数"""
        if image is None:
            return "请上传图像文件", None

        # 这里可以调用OCR功能，现在先返回简单信息
        return "✅ 图像处理成功！\n📊 这是一个演示结果", None

    def create_demo_image():
        """创建演示图像"""
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)

        # 添加边框和文字
        draw.rectangle([(10, 10), (390, 190)], outline='black', width=2)
        draw.text((50, 80), "医疗OCR演示图像", fill='black')
        draw.text((50, 120), "Medical OCR Demo", fill='blue')

        demo_path = 'assets/sample_docs/demo_image.png'
        img.save(demo_path)
        return demo_path

    # 创建演示图像
    demo_image = create_demo_image()

    # 创建Gradio界面
    interface = gr.Interface(
        fn=process_test_image,
        inputs=[
            gr.Image(label="上传医疗文档图像", type="numpy")
        ],
        outputs=[
            gr.Textbox(label="处理结果", lines=10),
            gr.File(label="下载结果文件")
        ],
        title="🏥 医疗OCR识别系统 - 本地演示",
        description="本地运行的医疗文档OCR识别演示。上传图像文件进行文字识别测试。",
        examples=[
            [demo_image]
        ],
        theme="soft"
    )

    return interface


def main():
    """主函数"""
    print("🌐 启动Gradio本地演示...")

    try:
        interface = create_simple_gradio_demo()

        print("✅ Gradio界面创建成功!")
        print("🚀 启动本地Web服务...")
        print("💡 浏览器将自动打开，或手动访问显示的URL")
        print("🛑 按 Ctrl+C 停止服务")

        # 启动界面
        interface.launch(
            server_name="0.0.0.0",  # 允许外部访问
            server_port=7860,       # 指定端口
            share=False,            # 本地运行不需要公网分享
            debug=True,             # 启用调试模式
            show_error=True         # 显示错误信息
        )

    except Exception as e:
        print(f"❌ Gradio启动失败: {e}")
        print("💡 请检查端口7860是否被占用")


if __name__ == "__main__":
    main()
