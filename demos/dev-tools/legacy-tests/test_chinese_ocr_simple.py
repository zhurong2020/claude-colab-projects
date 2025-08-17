#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings('ignore')

from paddleocr import PaddleOCR

print('🔍 初始化中文OCR处理器...')
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

print('📄 开始识别中文医疗文档...')
result = ocr.ocr('chinese_medical_document.png')

if result and len(result) > 0:
    page_result = result[0]
    
    if hasattr(page_result, 'rec_texts') and hasattr(page_result, 'rec_scores'):
        texts = page_result.rec_texts
        scores = page_result.rec_scores
        
        print(f'\n✅ 识别到 {len(texts)} 行中文文字:')
        print('=' * 80)
        for i, (text, score) in enumerate(zip(texts, scores), 1):
            print(f'{i:2d}: {text} (置信度: {score:.3f})')
        print('=' * 80)
        
        # 统计识别质量
        high_conf = sum(1 for score in scores if score > 0.9)
        med_conf = sum(1 for score in scores if 0.7 <= score <= 0.9)
        low_conf = sum(1 for score in scores if score < 0.7)
        
        print(f'\n📈 识别质量统计:')
        print(f'高置信度 (>0.9): {high_conf} 行')
        print(f'中置信度 (0.7-0.9): {med_conf} 行')  
        print(f'低置信度 (<0.7): {low_conf} 行')
        print(f'平均置信度: {sum(scores)/len(scores):.3f}')
        
        # 保存结果
        import pandas as pd
        results = []
        for i, (text, score) in enumerate(zip(texts, scores), 1):
            results.append({
                'file_name': 'chinese_medical_document.png',
                'line_number': i,
                'extracted_text': text,
                'confidence': round(score, 4)
            })
        
        df = pd.DataFrame(results)
        csv_path = 'chinese_ocr_results.csv'
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f'\n💾 中文OCR结果已保存到: {csv_path}')
else:
    print('⚠️ 未识别到任何内容')
