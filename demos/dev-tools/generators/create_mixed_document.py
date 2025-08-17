#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os

def create_mixed_language_document():
    """创建中英文混合医疗文档"""
    img = Image.new('RGB', (1000, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加边框
    draw.rectangle([(20, 20), (980, 780)], outline='black', width=2)
    
    # 中英文混合内容 - 更简单的布局
    mixed_text = [
        "Medical Report 医疗报告",
        "Hospital: Beijing Union Medical College Hospital",
        "医院: 北京协和医院",
        "Patient Name: Zhang San 患者姓名: 张三",
        "Gender: Male 性别: 男",
        "Age: 45 years old 年龄: 45岁",
        "Date: 2025-08-17 日期: 2025年8月17日",
        "Doctor: Dr. Li 医生: 李医生",
        "Diagnosis 诊断:",
        "1. Hypertension 高血压",
        "2. Diabetes 糖尿病", 
        "3. Coronary Heart Disease 冠心病",
        "Treatment 治疗方案:",
        "1. Medicine A 150mg daily 药物A每日150mg",
        "2. Medicine B 500mg twice daily 药物B每日两次500mg",
        "Doctor Signature 医生签名: Dr. Li"
    ]
    
    # 使用系统字体
    font_size = 24
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size)
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
    except:
        font = ImageFont.load_default()
        title_font = font
    
    # 绘制文本
    y_position = 60
    line_height = 40
    
    for i, text in enumerate(mixed_text):
        if i == 0:  # 标题
            # 居中
            bbox = draw.textbbox((0, 0), text, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_position = (1000 - text_width) // 2
            draw.text((x_position, y_position), text, fill='black', font=title_font)
            # 下划线
            draw.line([(x_position, y_position + 35), (x_position + text_width, y_position + 35)], 
                     fill='black', width=2)
            y_position += 20
        else:
            x_position = 60
            draw.text((x_position, y_position), text, fill='black', font=font)
        
        y_position += line_height
        print(f"✅ 绘制: {text}")
    
    # 保存
    output_path = 'mixed_language_document.png'
    img.save(output_path, quality=95)
    print(f"📄 创建混合语言文档: {output_path}")
    return output_path

if __name__ == "__main__":
    create_mixed_language_document()
