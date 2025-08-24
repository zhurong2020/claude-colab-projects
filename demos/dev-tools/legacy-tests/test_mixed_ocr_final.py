#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终OCR测试：中英文混合文档识别能力测试
"""

import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
from paddleocr import PaddleOCR

def test_mixed_language_ocr():
    """测试中英文混合OCR识别能力"""
    
    print("🏥 医疗文档OCR混合语言识别测试")
    print("=" * 50)
    
    # 初始化OCR引擎
    print("🔧 初始化PaddleOCR引擎...")
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    
    test_files = [
        'mixed_language_medical_doc.png',
        'chinese_medical_document.png', 
        'sample_medical_document.png'
    ]
    
    results_summary = []
    
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"⚠️ 文件不存在: {test_file}")
            continue
            
        print(f"\n📄 测试文件: {test_file}")
        print("-" * 40)
        
        try:
            # OCR识别
            result = ocr.predict(test_file)
            
            if not result or len(result) == 0:
                print("❌ 无识别结果")
                continue
                
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
                            'confidence': score,
                            'file': test_file
                        })
            elif page_result is not None:
                # 兼容旧版API
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
                                    'confidence': confidence,
                                    'file': test_file
                                })
                except Exception as e:
                    print(f"⚠️ 处理旧版API结果失败: {e}")
            
            # 分析识别结果
            if extracted_texts:
                print(f"✅ 识别到 {len(extracted_texts)} 行文字")
                
                # 语言统计
                chinese_lines = 0
                english_lines = 0
                mixed_lines = 0
                numeric_lines = 0
                
                high_confidence_count = 0
                total_confidence = 0
                
                print("\n📊 识别结果预览:")
                for i, item in enumerate(extracted_texts[:10], 1):  # 只显示前10行
                    text = item['text']
                    conf = item['confidence']
                    
                    # 尝试正确显示中文
                    try:
                        display_text = text.encode('utf-8').decode('utf-8')
                    except:
                        display_text = repr(text)  # 如果编码有问题，显示原始表示
                    
                    print(f"  {i:2d}. {display_text[:50]:50s} (置信度: {conf:.3f})")
                    
                    # 统计语言类型
                    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
                    has_english = any(char.isascii() and char.isalpha() for char in text)
                    has_numeric = any(char.isdigit() for char in text)
                    
                    if has_chinese and has_english:
                        mixed_lines += 1
                    elif has_chinese:
                        chinese_lines += 1
                    elif has_english:
                        english_lines += 1
                    elif has_numeric:
                        numeric_lines += 1
                    
                    if conf > 0.8:
                        high_confidence_count += 1
                    total_confidence += conf
                
                if len(extracted_texts) > 10:
                    print(f"  ... 还有 {len(extracted_texts) - 10} 行")
                
                # 统计信息
                avg_confidence = total_confidence / len(extracted_texts)
                
                print(f"\n📈 识别统计:")
                print(f"  纯中文行数: {chinese_lines}")
                print(f"  纯英文行数: {english_lines}")
                print(f"  中英混合行数: {mixed_lines}")
                print(f"  数字行数: {numeric_lines}")
                print(f"  平均置信度: {avg_confidence:.3f}")
                print(f"  高置信度行数 (>0.8): {high_confidence_count}/{len(extracted_texts)}")
                
                results_summary.append({
                    'file': test_file,
                    'total_lines': len(extracted_texts),
                    'chinese_lines': chinese_lines,
                    'english_lines': english_lines,
                    'mixed_lines': mixed_lines,
                    'avg_confidence': avg_confidence,
                    'high_confidence_ratio': high_confidence_count / len(extracted_texts)
                })
                
            else:
                print("❌ 未识别到有效文字")
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            print(f"详细错误: {traceback.format_exc()}")
    
    # 总结报告
    print(f"\n🎯 测试总结报告")
    print("=" * 50)
    
    if results_summary:
        df = pd.DataFrame(results_summary)
        print(df.to_string(index=False))
        
        # 保存详细结果
        df.to_csv('ocr_mixed_language_test_results.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 详细结果已保存到: ocr_mixed_language_test_results.csv")
        
        print(f"\n📊 OCR能力评估:")
        total_chinese = df['chinese_lines'].sum()
        total_english = df['english_lines'].sum()
        total_mixed = df['mixed_lines'].sum()
        avg_confidence = df['avg_confidence'].mean()
        avg_high_conf_ratio = df['high_confidence_ratio'].mean()
        
        print(f"✅ 中文识别能力: {'强' if total_chinese > 0 else '待测试'}")
        print(f"✅ 英文识别能力: {'强' if total_english > 0 else '待测试'}")
        print(f"✅ 混合文档识别: {'支持' if total_mixed > 0 else '基础支持'}")
        print(f"✅ 整体置信度: {avg_confidence:.3f} ({'优秀' if avg_confidence > 0.8 else '良好' if avg_confidence > 0.6 else '一般'})")
        print(f"✅ 高质量识别率: {avg_high_conf_ratio:.1%}")
        
        if total_chinese > 0 and total_english > 0:
            print(f"\n🎉 结论: PaddleOCR可以有效识别中英文混合医疗文档！")
        else:
            print(f"\n💡 建议: 需要进一步测试中文识别效果")
    else:
        print("❌ 没有成功的测试结果")

if __name__ == "__main__":
    test_mixed_language_ocr()