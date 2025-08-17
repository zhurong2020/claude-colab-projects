#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建中英文混合医疗文档图片
测试OCR对混合语言的识别能力
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_mixed_language_medical_document():
    """创建中英文混合的医疗文档图像"""
    
    # 创建示例图像
    img = Image.new('RGB', (1000, 900), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加边框
    draw.rectangle([(20, 20), (980, 880)], outline='black', width=2)
    
    # 中英文混合医疗内容
    mixed_text = [
        "Medical Report / 医疗报告",
        "Hospital: Beijing International Medical Center",
        "医院：北京国际医疗中心",
        "Patient Name: John Smith (张约翰)",
        "患者姓名：张约翰 (John Smith)",
        "Gender: Male / 性别：男",
        "Age: 35 years old / 年龄：35岁", 
        "Department: Cardiology / 心血管科",
        "Doctor: Dr. Wang / 主治医师：王医生",
        "",
        "Diagnosis / 诊断结果:",
        "1. Hypertension / 高血压",
        "2. Type 2 Diabetes / 二型糖尿病",
        "3. Hyperlipidemia / 高血脂症",
        "",
        "Prescription / 处方:",
        "1. Amlodipine 5mg once daily",
        "   氨氯地平 5mg 每日一次",
        "2. Metformin 500mg twice daily", 
        "   二甲双胍 500mg 每日两次",
        "3. Atorvastatin 20mg at bedtime",
        "   阿托伐他汀 20mg 睡前服用",
        "",
        "Follow-up / 复诊安排:",
        "Next visit in 2 weeks / 两周后复诊",
        "",
        "Doctor Signature / 医生签名: Dr. Wang",
        "Date / 日期: 2025-08-17"
    ]
    
    # 获取字体
    font = None
    font_size = 28
    
    try:
        # 尝试使用系统字体
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
                except Exception as e:
                    print(f"⚠️ 字体加载失败: {path} - {e}")
                    continue
    except Exception as e:
        print(f"⚠️ 字体加载过程异常: {e}")
    
    if font is None:
        try:
            font = ImageFont.load_default()
            print("✅ 使用PIL默认字体")
        except:
            print("⚠️ 使用系统默认字体")
            font = None
    
    # 绘制标题
    title_font_size = 36
    title_font = None
    try:
        if font and hasattr(font, 'path'):
            title_font = ImageFont.truetype(font.path, title_font_size) # type: ignore
        else:
            title_font = font
    except:
        title_font = font
    
    # 绘制文本内容
    y_position = 60
    line_height = 32
    
    for i, text in enumerate(mixed_text):
        try:
            if i == 0:  # 标题
                # 计算居中位置
                if title_font:
                    bbox = draw.textbbox((0, 0), text, font=title_font)
                    text_width = bbox[2] - bbox[0]
                else:
                    text_width = len(text) * 10
                x_position = (1000 - text_width) // 2
                
                # 绘制标题
                if title_font:
                    draw.text((x_position, y_position), text, fill='black', font=title_font)
                else:
                    draw.text((x_position, y_position), text, fill='black')
                
                # 添加下划线
                draw.line([(x_position, y_position + 40), (x_position + text_width, y_position + 40)], 
                         fill='black', width=2)
                y_position += 20  # 标题后额外间距
                
            elif text.strip() == "":  # 空行
                y_position += line_height // 2
                continue
                
            else:  # 普通文本
                x_position = 60
                if font:
                    draw.text((x_position, y_position), text, fill='black', font=font)
                else:
                    draw.text((x_position, y_position), text, fill='black')
            
            print(f"✅ 绘制文本: {text}")
            
        except Exception as e:
            print(f"⚠️ 文字绘制失败: {e} - 文本: {text}")
            try:
                x_pos = 60 if i > 0 else 200
                draw.text((x_pos, y_position), text, fill='black')
                print(f"✅ 备用方式绘制: {text}")
            except Exception as e2:
                print(f"❌ 备用绘制也失败: {e2}")
        
        y_position += line_height
    
    # 添加装饰元素
    try:
        # 医院LOGO占位符
        draw.rectangle([(60, 100), (160, 160)], outline='gray', width=1)
        draw.text((85, 125), "LOGO", fill='gray')
        
        # 签名线
        draw.line([(700, 820), (950, 820)], fill='black', width=1)
        draw.text((700, 830), "Doctor Signature", fill='gray')
        
        print("✅ 装饰元素添加完成")
    except Exception as e:
        print(f"⚠️ 装饰元素添加失败: {e}")
    
    # 保存图像
    output_path = 'mixed_language_medical_doc.png'
    img.save(output_path, quality=95, optimize=True)
    print(f"📄 创建中英文混合医疗文档: {output_path}")
    
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✅ 文件创建成功，大小: {file_size} 字节")
    else:
        print("❌ 文件创建失败")
    
    return output_path

if __name__ == "__main__":
    print("🎨 创建中英文混合医疗文档...")
    doc_path = create_mixed_language_medical_document()
    print(f"✅ 文档已保存: {doc_path}")