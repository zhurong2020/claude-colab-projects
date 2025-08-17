#!/usr/bin/env python3
"""
测试修复后的OCR功能
"""

import warnings
warnings.filterwarnings("ignore")

# 导入必要的库
from paddleocr import PaddleOCR
import pandas as pd  # type: ignore
# from PIL import Image  # 已移除未使用的导入


class MedicalOCRProcessor:
    def __init__(self):
        """初始化医疗OCR处理器"""
        print("🏥 初始化医疗OCR处理器...")
        
        # 检查GPU可用性
        try:
            import torch
            use_gpu = torch.cuda.is_available()
            gpu_info = f"GPU可用: {use_gpu}"
            if use_gpu:
                gpu_info += f" (设备: {torch.cuda.get_device_name(0)})"
            print(f"⚡ {gpu_info}")
        except ImportError:
            use_gpu = False
            print("ℹ️ PyTorch未安装，使用CPU模式")
        
        # 初始化PaddleOCR，支持中英文
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
        
        print("✅ OCR引擎初始化完成")
    
    def extract_text_from_image(self, image_path):
        """从图像中提取文字"""
        try:
            # 使用PaddleOCR识别文字（使用正确的predict方法）
            result = self.ocr.predict(image_path)
            
            # 提取文字内容
            extracted_texts = []
            
            # 新版本predict方法返回的是字典列表格式
            if result and len(result) > 0:
                for page_result in result:
                    # 检查是否有识别到的文本
                    if 'rec_texts' in page_result and 'rec_scores' in page_result:
                        texts = page_result['rec_texts']
                        scores = page_result['rec_scores']
                        
                        for text, score in zip(texts, scores):
                            # 只添加非空文字
                            if text and text.strip():
                                extracted_texts.append({
                                    'text': text.strip(),
                                    'confidence': score
                                })
            
            if not extracted_texts:
                print("⚠️ 未检测到任何文字内容")
                # 调试信息：显示返回结果的结构
                print(f"🔍 调试信息 - 结果类型: {type(result)}")
                if result:
                    print(f"🔍 调试信息 - 结果长度: {len(result)}")
                    if len(result) > 0:
                        print(f"🔍 调试信息 - 第一个元素类型: {type(result[0])}")
                        if isinstance(result[0], dict):
                            print(f"🔍 调试信息 - 字典键: {list(result[0].keys())}")
            else:
                print(f"✅ 成功识别 {len(extracted_texts)} 行文字")
            
            return extracted_texts
        
        except Exception as e:
            print(f"❌ 图像处理失败: {str(e)}")
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")
            return []
    
    def process_single_image(self, image_path):
        """处理单个图像文件"""
        import os
        print(f"📄 处理图像: {os.path.basename(image_path)}")
        
        # 提取文字
        extracted_texts = self.extract_text_from_image(image_path)
        
        # 整理结果
        results = []
        for i, item in enumerate(extracted_texts):
            results.append({
                'file_name': os.path.basename(image_path),
                'line_number': i + 1,
                'extracted_text': item['text'],
                'confidence': round(item['confidence'], 4)
            })
        
        return results
    
    def save_results_to_csv(self, results, output_path):
        """保存结果到CSV文件"""
        if not results:
            # 如果没有结果，创建空的DataFrame
            df = pd.DataFrame(columns=['file_name', 'line_number', 'extracted_text', 'confidence'])
        else:
            df = pd.DataFrame(results)
        
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"💾 结果已保存到: {output_path}")
        return df


def main():
    """主测试函数"""
    print("🧪 开始测试修复后的OCR功能...")
    
    # 初始化OCR处理器
    ocr_processor = MedicalOCRProcessor()
    
    # 测试示例图像
    image_path = 'sample_medical_document.png'
    
    # 处理图像
    results = ocr_processor.process_single_image(image_path)
    
    # 显示识别结果
    print("\n📊 文字识别结果:")
    print("-" * 60)
    
    for result in results:
        print(f"行{result['line_number']:2d}: {result['extracted_text']} "
              f"(置信度: {result['confidence']:.3f})")
    
    # 保存结果到CSV
    csv_path = 'ocr_results_fixed.csv'
    df = ocr_processor.save_results_to_csv(results, csv_path)
    
    print(f"\n📈 共识别出 {len(results)} 行文字")
    print(f"📄 结果已保存到 CSV 文件: {csv_path}")
    
    # 显示CSV内容预览
    print("\n📋 CSV文件预览:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()