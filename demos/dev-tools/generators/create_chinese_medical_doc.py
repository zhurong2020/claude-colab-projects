#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建中文医疗文档样本用于OCR测试
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_chinese_medical_document():
    """创建中文医疗文档图像用于测试"""
    # 创建图像 - 使用更大尺寸确保文字清晰
    img = Image.new('RGB', (1000, 900), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加边框
    draw.rectangle([(20, 20), (980, 880)], outline='black', width=2)
    
    # 中文医疗文档内容
    chinese_text = [
        "医疗诊断报告",
        "医院名称：北京协和医院",
        "科室：心血管内科",
        "患者姓名：张三",
        "性别：男    年龄：45岁",
        "身份证号：110101198001011234",
        "就诊日期：2025年8月17日",
        "主治医师：李医生",
        "临床诊断：",
        "1. 高血压病（2级）",
        "2. 糖尿病（2型）",
        "3. 冠心病",
        "治疗方案：",
        "1. 厄贝沙坦片 150mg 每日一次",
        "2. 二甲双胍片 500mg 每日两次",
        "3. 阿司匹林肠溶片 100mg 每日一次",
        "复查时间：一个月后复查",
        "医生签名：李医生",
        "日期：2025-08-17"
    ]
    
    # 获取中文字体
    font = None
    title_font = None
    font_size = 28  # 稍小的字体确保显示完整
    title_font_size = 36
    
    font_paths = [
        # 常见的中文字体路径
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        'C:/Windows/Fonts/simsun.ttc',  # Windows
    ]
    
    # 尝试加载中文字体
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                title_font = ImageFont.truetype(font_path, title_font_size)
                print(f"✅ 使用字体: {font_path}")
                break
            except Exception as e:
                print(f"⚠️ 字体加载失败: {font_path} - {e}")
                continue
    
    # 使用默认字体作为备用
    if font is None:
        try:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            print("✅ 使用PIL默认字体")
        except:
            print("⚠️ 使用系统默认字体")
            font = None
            title_font = None
    
    # 绘制文本内容
    y_position = 60
    line_height = 42  # 适合中文的行高
    
    for i, text in enumerate(chinese_text):
        try:
            # 第一行标题居中加粗
            if i == 0:
                # 计算居中位置
                if title_font:
                    bbox = draw.textbbox((0, 0), text, font=title_font)
                    text_width = bbox[2] - bbox[0]
                else:
                    # 估算中文字符宽度
                    text_width = len(text) * 24
                
                x_position = (1000 - text_width) // 2
                
                # 绘制标题
                if title_font:
                    draw.text((x_position, y_position), text, fill='black', font=title_font)
                else:
                    draw.text((x_position, y_position), text, fill='black')
                print(f"✅ 绘制标题: {text}")
                
                # 添加下划线
                draw.line([(x_position, y_position + 40), (x_position + text_width, y_position + 40)], 
                         fill='black', width=2)
                y_position += 20  # 标题后额外间距
            else:
                # 普通文本左对齐
                x_position = 60
                if font:
                    draw.text((x_position, y_position), text, fill='black', font=font)
                else:
                    draw.text((x_position, y_position), text, fill='black')
                print(f"✅ 绘制文本: {text}")
            
        except Exception as e:
            print(f"⚠️ 文字绘制失败: {e} - 文本: {text}")
            # 简单备用绘制
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
        draw.rectangle([(60, 110), (160, 170)], outline='gray', width=1)
        draw.text((80, 135), "医院", fill='gray')
        draw.text((80, 150), "LOGO", fill='gray')
        
        # 签名线
        draw.line([(700, 800), (950, 800)], fill='black', width=1)
        draw.text((700, 810), "医生签名", fill='gray')
        
        # 盖章位置
        draw.circle((850, 750), 40, outline='red', width=2)
        draw.text((820, 740), "医院", fill='red')
        draw.text((820, 755), "印章", fill='red')
        
        print("✅ 装饰元素添加完成")
    except Exception as e:
        print(f"⚠️ 装饰元素添加失败: {e}")
    
    # 保存图像
    output_path = 'chinese_medical_document.png'
    img.save(output_path, quality=95, optimize=True)
    print(f"📄 创建中文医疗文档: {output_path}")
    
    # 验证文件创建
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✅ 文件创建成功，大小: {file_size} 字节")
    else:
        print("❌ 文件创建失败")
    
    return output_path

if __name__ == "__main__":
    print("🎨 创建中文医疗文档样本...")
    doc_path = create_chinese_medical_document()
    print(f"📄 中文医疗文档已创建: {doc_path}")