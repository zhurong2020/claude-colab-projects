#!/usr/bin/env python3
"""
测试中文OCR识别功能
"""

import warnings
warnings.filterwarnings("ignore")

import os
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR
import pandas as pd  # type: ignore


def create_chinese_medical_document():
    """创建中文医疗文档用于测试"""
    # 创建示例图像
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加边框
    draw.rectangle([(20, 20), (780, 580)], outline='black', width=2)
    
    # 中文医疗文档内容
    chinese_text = [
        "医疗报告",
        "医院：北京市人民医院",
        "患者姓名：张三",
        "性别：男    年龄：45岁",
        "科室：心血管内科",
        "主治医师：李医生",
        "诊断：高血压、糖尿病",
        "处方：",
        "1. 降压药 10mg 每日一次",
        "2. 降糖药 5mg 每日两次",
        "医生签名：李医生",
        "日期：2025年8月17日"
    ]
    
    # 尝试使用中文字体
    font = None
    font_size = 24
    
    try:
        # 尝试常见的中文字体路径
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, font_size)
                    print(f"✅ 使用字体: {path}")
                    break
                except Exception:
                    continue
    except Exception:
        pass
    
    if font is None:
        font = ImageFont.load_default()
        print("✅ 使用默认字体")
    
    # 绘制文本
    y_position = 50
    line_height = 40
    
    for i, text in enumerate(chinese_text):
        try:
            if i == 0:
                # 标题居中
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = (800 - text_width) // 2
                draw.text((x_position, y_position), text, fill='black', font=font)
                print(f"✅ 绘制标题: {text}")
            else:
                # 普通文本左对齐
                x_position = 50
                draw.text((x_position, y_position), text, fill='black', font=font)
                print(f"✅ 绘制文本: {text}")
        except Exception as e:
            print(f"⚠️ 文字绘制失败: {e} - 文本: {text}")
            # 备用绘制
            x_pos = 50 if i > 0 else 300
            draw.text((x_pos, y_position), text, fill='black')
        
        y_position += line_height
    
    # 保存图像
    chinese_doc_path = 'chinese_medical_document.png'
    img.save(chinese_doc_path, quality=95)
    print(f"📄 创建中文医疗文档: {chinese_doc_path}")
    
    return chinese_doc_path


def test_chinese_ocr(image_path):
    """测试中文OCR识别"""
    print("🔤 初始化中文OCR处理器...")
    
    # 初始化支持中文的OCR
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    
    print(f"📄 处理中文图像: {os.path.basename(image_path)}")
    
    try:
        # 使用OCR识别文字
        result = ocr.predict(image_path)
        
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
        
        # 显示识别结果
        print("\n🔤 中文文字识别结果:")
        print("-" * 60)
        
        results = []
        for i, item in enumerate(extracted_texts):
            print(f"行{i+1:2d}: {item['text']} (置信度: {item['confidence']:.3f})")
            results.append({
                'file_name': os.path.basename(image_path),
                'line_number': i + 1,
                'extracted_text': item['text'],
                'confidence': round(item['confidence'], 4)
            })
        
        # 保存结果
        if results:
            df = pd.DataFrame(results)
            csv_path = 'chinese_ocr_results.csv'
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"\n✅ 中文识别成功！共识别 {len(results)} 行文字")
            print(f"💾 结果已保存到: {csv_path}")
            
            # 显示CSV预览
            print("\n📋 CSV文件预览:")
            print(df.to_string(index=False))
        else:
            print("⚠️ 未检测到任何文字内容")
        
        return results
        
    except Exception as e:
        print(f"❌ 中文OCR处理失败: {str(e)}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return []


def main():
    """主测试函数"""
    print("🧪 开始测试中文OCR识别功能...")
    
    # 创建中文测试文档
    chinese_doc = create_chinese_medical_document()
    
    # 测试中文OCR识别
    results = test_chinese_ocr(chinese_doc)
    
    if results:
        print("\n🎉 中文OCR测试成功完成！")
        print(f"📊 识别率：{len(results)} 行文字")
        
        # 计算平均置信度
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        print(f"📈 平均置信度：{avg_confidence:.3f}")
    else:
        print("\n❌ 中文OCR测试失败")


if __name__ == "__main__":
    main()