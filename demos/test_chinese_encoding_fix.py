#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文OCR识别编码问题修复测试
针对方案A：环境修复 + 代码优化
"""

import os
import sys
import warnings
import locale
import pandas as pd
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

# 设置编码和警告
warnings.filterwarnings('ignore')
os.environ['PYTHONIOENCODING'] = 'utf-8'

def setup_encoding():
    """设置编码环境"""
    print("🔧 设置编码环境...")
    
    # 尝试设置UTF-8编码
    try:
        if sys.platform.startswith('linux'):
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        else:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        print("✅ Locale设置成功")
    except locale.Error as e:
        print(f"⚠️ Locale设置失败: {e}")
        print("📝 使用默认编码设置")
    
    # 强制设置stdout编码
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        print("✅ 标准输出编码设置为UTF-8")
    
    return True

def safe_chinese_print(text, confidence=None):
    """安全的中文字符打印函数"""
    try:
        # 方法1：直接打印（适用于UTF-8环境）
        if confidence is not None:
            output = f"{text} (置信度: {confidence:.3f})"
        else:
            output = text
        print(output)
        return True
    except UnicodeEncodeError:
        try:
            # 方法2：使用ASCII表示不可打印字符
            safe_text = text.encode('ascii', 'replace').decode('ascii')
            if confidence is not None:
                output = f"{safe_text} (置信度: {confidence:.3f})"
            else:
                output = safe_text
            print(output)
            return True
        except Exception as e:
            # 方法3：显示字节表示
            try:
                byte_repr = text.encode('utf-8')
                print(f"[字节表示: {byte_repr}] (置信度: {confidence:.3f})" if confidence else f"[字节表示: {byte_repr}]")
                return True
            except Exception as final_e:
                print(f"❌ 字符显示失败: {final_e}")
                return False

def analyze_chinese_characters(text):
    """分析字符串中的中文字符"""
    chinese_chars = []
    ascii_chars = []
    other_chars = []
    
    for char in text:
        if '\u4e00' <= char <= '\u9fff':  # 中文字符范围
            chinese_chars.append(char)
        elif char.isascii():
            ascii_chars.append(char)
        else:
            other_chars.append(char)
    
    return {
        'chinese_count': len(chinese_chars),
        'ascii_count': len(ascii_chars),
        'other_count': len(other_chars),
        'chinese_chars': chinese_chars,
        'ascii_chars': ascii_chars,
        'has_chinese': len(chinese_chars) > 0
    }

def create_test_chinese_document():
    """创建测试用的中文医疗文档"""
    print("📄 创建测试中文医疗文档...")
    
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加边框
    draw.rectangle([(10, 10), (790, 590)], outline='black', width=2)
    
    # 简单的中文文本（避免复杂字符）
    test_texts = [
        "医疗报告",
        "患者：张三",
        "年龄：45岁",
        "诊断：高血压",
        "药物：降压片",
        "剂量：10mg",
        "频次：每日一次",
        "医生：李医生"
    ]
    
    # 使用简单字体绘制
    try:
        font_paths = [
            '~/.fonts/simhei.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        ]
        
        font = None
        for path in font_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                try:
                    font = ImageFont.truetype(expanded_path, 36)
                    print(f"✅ 使用字体: {expanded_path}")
                    break
                except Exception as e:
                    print(f"⚠️ 字体加载失败: {path} - {e}")
        
        if font is None:
            font = ImageFont.load_default()
            print("⚠️ 使用默认字体")
        
        # 绘制文字
        y_pos = 50
        for i, text in enumerate(test_texts):
            x_pos = 50 if i > 0 else 200  # 标题居中
            draw.text((x_pos, y_pos), text, fill='black', font=font)
            y_pos += 60
        
        output_path = 'test_chinese_simple.png'
        img.save(output_path, quality=95)
        print(f"✅ 中文测试文档已创建: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 创建中文文档失败: {e}")
        return None

def test_ocr_with_encoding_fix():
    """测试带编码修复的OCR识别"""
    
    print("🏥 中文OCR识别编码修复测试")
    print("=" * 50)
    
    # 设置编码环境
    setup_encoding()
    
    # 创建测试文档
    test_doc = create_test_chinese_document()
    if not test_doc:
        print("❌ 无法创建测试文档")
        return
    
    # 初始化OCR
    print("\n🔧 初始化PaddleOCR...")
    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='ch')
        print("✅ OCR引擎初始化成功")
    except Exception as e:
        print(f"❌ OCR初始化失败: {e}")
        return
    
    # 进行OCR识别
    print(f"\n🔍 识别测试文档: {test_doc}")
    try:
        result = ocr.ocr(test_doc)
        
        if not result or len(result) == 0:
            print("❌ OCR无识别结果")
            return
        
        page_result = result[0]
        extracted_texts = []
        
        # 处理识别结果
        if isinstance(page_result, dict) and 'rec_texts' in page_result:
            texts = page_result['rec_texts']
            scores = page_result['rec_scores']
            for text, score in zip(texts, scores):
                if text and text.strip():
                    extracted_texts.append({
                        'text': text.strip(),
                        'confidence': score
                    })
        elif page_result is not None:
            try:
                for line in page_result:
                    if (line and len(line) >= 2 and 
                        line[1] and len(line[1]) >= 2 and 
                        isinstance(line[1][0], str)):
                        
                        text = line[1][0]
                        confidence = line[1][1]
                        
                        if text and text.strip():
                            extracted_texts.append({
                                'text': text.strip(),
                                'confidence': confidence
                            })
            except Exception as e:
                print(f"⚠️ 处理识别结果失败: {e}")
        
        # 显示识别结果
        print(f"\n📊 识别结果 (共{len(extracted_texts)}行):")
        print("-" * 60)
        
        chinese_detected = 0
        encoding_issues = 0
        successful_displays = 0
        
        for i, item in enumerate(extracted_texts, 1):
            text = item['text']
            confidence = item['confidence']
            
            # 分析字符组成
            char_analysis = analyze_chinese_characters(text)
            
            print(f"\n行 {i:2d}:")
            print(f"  原始文本: {repr(text)}")
            print(f"  置信度: {confidence:.3f}")
            print(f"  字符分析: 中文{char_analysis['chinese_count']}个, ASCII{char_analysis['ascii_count']}个")
            
            # 尝试安全显示
            print(f"  显示测试: ", end="")
            if safe_chinese_print(text, confidence):
                successful_displays += 1
                if char_analysis['has_chinese']:
                    chinese_detected += 1
            else:
                encoding_issues += 1
        
        # 统计报告
        print(f"\n📈 测试统计:")
        print(f"  总识别行数: {len(extracted_texts)}")
        print(f"  包含中文行数: {chinese_detected}")
        print(f"  成功显示行数: {successful_displays}")
        print(f"  编码问题行数: {encoding_issues}")
        
        # 保存结果到CSV
        if extracted_texts:
            results_df = pd.DataFrame([
                {
                    'line_number': i,
                    'text': item['text'],
                    'confidence': item['confidence'],
                    'has_chinese': analyze_chinese_characters(item['text'])['has_chinese']
                }
                for i, item in enumerate(extracted_texts, 1)
            ])
            
            csv_path = 'chinese_ocr_encoding_test_results.csv'
            results_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"\n💾 结果已保存到: {csv_path}")
        
        # 结论
        print(f"\n🎯 测试结论:")
        if chinese_detected > 0:
            print(f"✅ 成功检测到中文字符！")
            print(f"✅ 中文识别功能正常")
            if encoding_issues == 0:
                print(f"✅ 编码显示问题已解决")
            else:
                print(f"⚠️ 部分编码显示仍需优化")
        else:
            print(f"⚠️ 未检测到中文字符，可能是图片质量或字体问题")
        
    except Exception as e:
        print(f"❌ OCR测试失败: {e}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")

if __name__ == "__main__":
    test_ocr_with_encoding_fix()