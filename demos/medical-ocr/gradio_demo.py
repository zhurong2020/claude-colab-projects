#!/usr/bin/env python3
"""
医疗OCR Gradio演示
PaddleOCR医疗文档识别Web界面
版本: v1.3.12
"""

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import numpy as np
from PIL import Image as PILImage
import pandas as pd
import gradio as gr

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class MedicalOCRProcessor:
    """医疗OCR处理器"""
    
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
        
        # 初始化PaddleOCR，使用兼容的配置
        try:
            from paddleocr import PaddleOCR
            
            # 使用兼容的参数初始化PaddleOCR (v3.1.1)
            self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
            print("✅ 使用兼容参数初始化OCR引擎")
        except Exception as e:
            print(f"❌ OCR初始化失败: {e}")
            self.ocr = None
            raise RuntimeError(f"PaddleOCR初始化失败: {e}")
        
        print("✅ OCR引擎初始化完成")
    
    def _preprocess_image(self, image_path):
        """预处理图像，确保格式和质量适合OCR"""
        try:
            # 打开并验证图像
            with PILImage.open(image_path) as img:
                print(f"📊 原始图像信息: 尺寸={img.size}, 模式={img.mode}")
                
                # 转换为RGB格式（如果不是的话）
                if img.mode != 'RGB':
                    print(f"🔄 转换图像模式: {img.mode} -> RGB")
                    img = img.convert('RGB')
                
                # 检查图像尺寸，如果过大则适当缩小
                max_size = 2048
                if max(img.size) > max_size:
                    print(f"🔄 调整图像尺寸: {img.size}")
                    ratio = max_size / max(img.size)
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, PILImage.Resampling.LANCZOS)
                    print(f"✅ 新尺寸: {img.size}")
                
                # 保存预处理后的图像
                processed_path = image_path.replace('.png', '_processed.png').replace('.jpg', '_processed.jpg').replace('.jpeg', '_processed.jpg')
                if processed_path == image_path:
                    processed_path = image_path.replace('.', '_processed.')
                
                img.save(processed_path, quality=95, optimize=False)
                print(f"💾 预处理图像已保存: {processed_path}")
                
                return processed_path
                
        except Exception as e:
            print(f"⚠️ 图像预处理失败: {e}，使用原始图像")
            return image_path
    
    def _parse_ocr_result(self, result):
        """解析OCR结果 - 兼容多种PaddleOCR返回格式 - v1.3.11增强调试版"""
        print(f"🔍 [DEBUG] _parse_ocr_result 开始解析，输入类型: {type(result)}")
        
        extracted_texts = []
        try:
            # 详细的输入验证和调试
            if not result:
                print("❌ [DEBUG] result为None或空")
                return []
            
            if not isinstance(result, list):
                print(f"❌ [DEBUG] result不是列表类型，实际类型: {type(result)}")
                return []
            
            if len(result) == 0:
                print("❌ [DEBUG] result列表为空")
                return []
            
            page_result = result[0]
            print(f"🔍 [DEBUG] 第一页结果类型: {type(page_result)}")
            print(f"🔍 [DEBUG] 第一页结果长度: {len(page_result) if hasattr(page_result, '__len__') else 'N/A'}")

            # 新版 PaddleOCR v3.1.1+ (返回带 .json 属性的 OCRResult 对象)
            if hasattr(page_result, 'json'):
                print("✅ [DEBUG] 检测到PaddleOCR v3.1.1+ OCRResult对象格式")
                json_result = page_result.json
                print(f"🔍 [DEBUG] json_result类型: {type(json_result)}")
                
                if isinstance(json_result, dict):
                    print(f"🔍 [DEBUG] json_result键: {list(json_result.keys())}")
                    
                    if 'res' in json_result:
                        res_data = json_result['res']
                        print(f"🔍 [DEBUG] res_data类型: {type(res_data)}")
                        print(f"🔍 [DEBUG] res_data键: {list(res_data.keys()) if isinstance(res_data, dict) else 'not dict'}")
                        
                        if res_data and 'rec_texts' in res_data and 'rec_scores' in res_data:
                            texts, scores = res_data['rec_texts'], res_data['rec_scores']
                            print(f"📊 [DEBUG] 识别到文本数量: {len(texts) if texts else 0}")
                            print(f"📊 [DEBUG] 置信度数量: {len(scores) if scores else 0}")
                            
                            if texts and scores:
                                print(f"🔍 [DEBUG] 前3个文本: {texts[:3] if len(texts) >= 3 else texts}")
                                for i, (text, score) in enumerate(zip(texts, scores)):
                                    if text and text.strip():
                                        extracted_texts.append({'text': text.strip(), 'confidence': float(score)})
                                        if i < 3:  # 只打印前3个
                                            print(f"✅ [DEBUG] 提取文本 {i+1}: {text.strip()[:30]}... (置信度: {score:.3f})")
                                        
                                print(f"✅ [DEBUG] OCRResult对象格式处理完成，提取了{len(extracted_texts)}个文本")
                                return extracted_texts
                        else:
                            print("❌ [DEBUG] res_data中缺少rec_texts或rec_scores")
                    else:
                        print("❌ [DEBUG] json_result中缺少res键")
                else:
                    print(f"❌ [DEBUG] json_result不是字典类型: {type(json_result)}")
                        
            # 兼容直接返回字典列表的格式
            elif isinstance(page_result, list) and page_result and isinstance(page_result[0], dict) and 'text' in page_result[0]:
                print("✅ [DEBUG] 检测到字典列表格式")
                for i, line in enumerate(page_result):
                    text, confidence = line.get('text', ''), line.get('confidence', 0.0)
                    if text.strip():
                        extracted_texts.append({'text': text.strip(), 'confidence': float(confidence)})
                        if i < 3:
                            print(f"✅ [DEBUG] 字典格式文本 {i+1}: {text.strip()[:30]}... (置信度: {confidence:.3f})")
                            
                print(f"✅ [DEBUG] 字典列表格式处理完成，提取了{len(extracted_texts)}个文本")
                return extracted_texts

            # 兼容旧版 PaddleOCR (返回包含元组的列表)
            elif isinstance(page_result, list):
                print("✅ [DEBUG] 检测到传统列表格式")
                print(f"🔍 [DEBUG] 列表长度: {len(page_result)}")
                
                for i, line_result in enumerate(page_result):
                    print(f"🔍 [DEBUG] 第{i+1}行结果类型: {type(line_result)}, 长度: {len(line_result) if hasattr(line_result, '__len__') else 'N/A'}")
                    
                    if (line_result and len(line_result) >= 2 and
                        line_result[1] and len(line_result[1]) >= 2):
                        text, confidence = line_result[1]
                        if text and text.strip():
                            extracted_texts.append({'text': text.strip(), 'confidence': float(confidence)})
                            if i < 3:
                                print(f"✅ [DEBUG] 传统格式文本 {i+1}: {text.strip()[:30]}... (置信度: {confidence:.3f})")
                    else:
                        print(f"⚠️ [DEBUG] 第{i+1}行格式不符合预期")
                        
                print(f"✅ [DEBUG] 传统列表格式处理完成，提取了{len(extracted_texts)}个文本")
                return extracted_texts
            
            else:
                print(f"❌ [DEBUG] 未知的OCR结果格式: {type(page_result)}")
                print(f"🔍 [DEBUG] page_result详情: {str(page_result)[:200]}...")
                self._debug_result_structure(result)

        except Exception as e:
            print(f"❌ [DEBUG] 结果解析异常: {e}")
            import traceback
            print(f"🔍 [DEBUG] 详细错误: {traceback.format_exc()}")
        
        print(f"⚠️ [DEBUG] _parse_ocr_result 结束，最终提取了{len(extracted_texts)}个文本")
        return extracted_texts
    
    def extract_text_from_image(self, image_path):
        """从图像中提取文字 - 增强版本"""
        if self.ocr is None:
            print("❌ OCR引擎未初始化")
            return []
        
        try:
            # 验证图像文件
            if not os.path.exists(image_path):
                print(f"❌ 图像文件不存在: {image_path}")
                return []
            
            if os.path.getsize(image_path) == 0:
                print(f"❌ 图像文件为空: {image_path}")
                return []
            
            print(f"📄 正在处理图像: {image_path}")
            print(f"📊 文件大小: {os.path.getsize(image_path)} 字节")
            
            # 预处理图像：确保图像格式和质量适合OCR
            processed_image_path = self._preprocess_image(image_path)
            
            # 使用PaddleOCR进行识别
            result = None
            extracted_texts = []
            
            # 使用predict方法 (推荐的新版本API)
            try:
                print("🔄 尝试使用predict方法...")
                result = self.ocr.predict(processed_image_path)
                print(f"✅ predict方法调用成功，结果类型: {type(result)}")
                extracted_texts = self._parse_ocr_result(result)
                
                if extracted_texts:
                    print(f"✅ 成功识别 {len(extracted_texts)} 行文字")
                    return extracted_texts
                
            except Exception as e1:
                print(f"⚠️ predict方法失败: {e1}")
                
                # 尝试使用传统的ocr方法
                try:
                    print("🔄 尝试使用传统ocr方法...")
                    result = self.ocr.ocr(processed_image_path)  # type: ignore
                    print(f"✅ OCR方法调用成功，结果类型: {type(result)}")
                    extracted_texts = self._parse_ocr_result(result)
                    
                    if extracted_texts:
                        print(f"✅ 成功识别 {len(extracted_texts)} 行文字")
                        return extracted_texts
                        
                except Exception as e2:
                    print(f"❌ 所有可用的OCR调用方法都失败")
                    print(f"详细错误: predict={e1}, ocr={e2}")
            
            # 如果所有方法都没有识别到文字
            if not extracted_texts:
                print("⚠️ 未检测到任何文字内容")
                self._debug_result_structure(result)
                self._check_image_quality(processed_image_path)
                
                return []
            
            return extracted_texts
        
        except Exception as e:
            print(f"❌ 图像处理失败: {str(e)}")
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")
            return []
    
    def _debug_result_structure(self, result):
        """调试结果结构"""
        try:
            print(f"🔍 调试信息: result类型={type(result)}")
            if result:
                print(f"🔍 result长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
                if isinstance(result, list) and len(result) > 0:
                    first_item = result[0]
                    print(f"🔍 第一项类型: {type(first_item)}")
                    if isinstance(first_item, dict):
                        print(f"🔍 字典键: {list(first_item.keys())}")
                    elif hasattr(first_item, '__dict__'):
                        print(f"🔍 对象属性: {list(vars(first_item).keys())}")
                    elif isinstance(first_item, list) and len(first_item) > 0:
                        print(f"🔍 嵌套列表长度: {len(first_item)}")
                        if len(first_item) > 0:
                            print(f"🔍 嵌套项类型: {type(first_item[0])}")
        except Exception as e:
            print(f"🔍 调试信息获取失败: {e}")
    
    def _check_image_quality(self, image_path):
        """检查图像质量"""
        try:
            if not os.path.exists(image_path):
                print("🔍 图像文件不存在")
                return
            
            with PILImage.open(image_path) as img:
                width, height = img.size
                total_pixels = width * height
                
                print(f"🔍 图像质量检查:")
                print(f"   尺寸: {width}x{height} ({total_pixels:,} 像素)")
                print(f"   格式: {img.format}")
                print(f"   模式: {img.mode}")
                
                # 质量评估
                if total_pixels < 50000:
                    print("   ⚠️ 图像分辨率较低，可能影响识别效果")
                elif total_pixels > 4000000:
                    print("   ℹ️ 图像分辨率很高，处理速度可能较慢")
                else:
                    print("   ✅ 图像分辨率适中")
                
        except Exception as e:
            print(f"🔍 图像质量检查失败: {e}")
    
    def process_single_image(self, image_path):
        """处理单个图像文件"""
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


def process_uploaded_image(image, processor=None):
    """处理上传的图像 - Gradio接口函数"""
    if image is None:
        return "请上传图像文件", None
    
    try:
        print("🔍 开始处理上传的图像...")
        
        # 确保assets目录存在
        os.makedirs('assets/sample_docs', exist_ok=True)
        
        # 创建临时文件名
        temp_filename = "temp_uploaded_image.png"
        temp_path = os.path.join('assets/sample_docs', temp_filename)
        
        # 处理不同类型的输入图像
        processed_successfully = False
        
        try:
            if isinstance(image, np.ndarray):
                # Gradio上传的numpy数组格式
                print("📥 处理numpy数组格式图像...")
                
                # 确保数组是正确的形状和数据类型
                if len(image.shape) != 3:
                    return "❌ 不支持的图像维度，请上传标准图像文件", None
                
                # 数据类型转换
                if image.dtype != np.uint8:
                    if image.max() <= 1.0:
                        # 浮点数格式 (0-1)
                        image = (image * 255).astype(np.uint8)
                    else:
                        # 其他格式
                        image = image.astype(np.uint8)
                
                # 转换为PIL图像
                if image.shape[2] == 3:
                    # RGB格式
                    pil_image = PILImage.fromarray(image, mode='RGB')
                elif image.shape[2] == 4:
                    # RGBA格式，转换为RGB
                    pil_image = PILImage.fromarray(image, mode='RGBA').convert('RGB')
                else:
                    return f"❌ 不支持的颜色通道数: {image.shape[2]}", None
                
                print(f"✅ 成功转换图像，尺寸: {pil_image.size}")
                processed_successfully = True
                
            elif isinstance(image, str):
                # 文件路径
                print(f"📥 处理文件路径: {image}")
                if not os.path.exists(image):
                    return "❌ 文件路径不存在", None
                pil_image = PILImage.open(image).convert('RGB')
                processed_successfully = True
                
            elif isinstance(image, PILImage.Image):
                # PIL图像对象
                print("📥 处理PIL图像对象...")
                pil_image = image.convert('RGB')
                processed_successfully = True
                
            elif hasattr(image, 'save'):
                # 可能是PIL图像或类似对象
                print("📥 处理可保存图像对象...")
                pil_image = image.convert('RGB')
                processed_successfully = True
                
            else:
                return f"❌ 无法处理的图像类型: {type(image)}", None
            
            if not processed_successfully:
                return "❌ 图像处理失败", None
            
            # 图像质量检查和优化
            width, height = pil_image.size
            print(f"📊 图像尺寸: {width}x{height}")
            
            # 如果图像太小，可能影响识别效果
            if width < 100 or height < 50:
                return "❌ 图像尺寸过小，可能影响识别效果。请上传分辨率更高的图像。", None
            
            # 如果图像过大，进行适当缩放
            max_dimension = 2048
            if max(width, height) > max_dimension:
                print("🔄 图像过大，进行缩放...")
                ratio = max_dimension / max(width, height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                pil_image = pil_image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                print(f"✅ 缩放后尺寸: {pil_image.size}")
            
            # 保存处理后的图像
            try:
                pil_image.save(temp_path, format='PNG', quality=95, optimize=True)
                print(f"💾 图像已保存到: {temp_path}")
            except Exception as save_error:
                print(f"⚠️ PNG保存失败: {save_error}，尝试JPEG格式")
                temp_path = temp_path.replace('.png', '.jpg')
                pil_image.save(temp_path, format='JPEG', quality=95)
                print(f"💾 图像已保存到: {temp_path}")
            
            # 验证保存的文件
            if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                return "❌ 图像保存失败，请重试", None
            
            print(f"✅ 文件验证成功，大小: {os.path.getsize(temp_path)} 字节")
            
        except Exception as img_error:
            print(f"❌ 图像处理错误: {img_error}")
            return f"❌ 图像处理失败: {str(img_error)}", None
        
        # 检查OCR处理器是否可用
        if processor is not None:
            # 优先使用传入的处理器
            active_processor = processor
        else:
            # 尝试获取全局变量
            try:
                if 'ocr_processor' not in globals():
                    return "❌ OCR处理器未初始化，请重新运行初始化代码", None
                
                global ocr_processor
                if ocr_processor is None:
                    return "❌ OCR处理器未初始化，请重新运行初始化代码", None
                active_processor = ocr_processor
            except NameError:
                return "❌ OCR处理器未初始化，请重新运行初始化代码", None
        
        # 最终检查
        if active_processor is None:
            return "❌ OCR处理器未初始化，请重新运行初始化代码", None
        
        # 使用OCR处理图像
        debug_info = ["🔍 开始OCR识别..."]
        try:
            # 捕获OCR处理过程中的调试信息
            import io
            from contextlib import redirect_stdout
            
            # 创建字符串缓冲区捕获print输出
            debug_buffer = io.StringIO()
            
            with redirect_stdout(debug_buffer):
                results = active_processor.process_single_image(temp_path)
            
            # 获取调试信息
            debug_output = debug_buffer.getvalue()
            if debug_output:
                debug_info.append("\n📊 OCR处理过程调试信息:")
                debug_info.append(debug_output)
            
            if not results:
                # 详细的失败分析，包含调试信息
                analysis_result = "😞 未检测到任何文字内容\n\n"
                analysis_result += "\n".join(debug_info) + "\n\n"
                analysis_result += "🔍 可能的原因分析:\n"
                analysis_result += "1. 图像中没有清晰的文字\n"
                analysis_result += "2. 文字过小、模糊或倾斜角度过大\n"
                analysis_result += "3. 图像背景复杂，干扰了文字识别\n"
                analysis_result += "4. 图像对比度不足\n"
                analysis_result += "5. PaddleOCR版本兼容性问题\n\n"
                analysis_result += "💡 改进建议:\n"
                analysis_result += "• 确保图像清晰，文字大小适中\n"
                analysis_result += "• 调整图像亮度和对比度\n"
                analysis_result += "• 尽量保持文档平整，减少倾斜\n"
                analysis_result += "• 避免复杂背景，使用纯色背景\n"
                analysis_result += "• 尝试不同的拍摄角度和光线条件\n"
                analysis_result += f"\n📊 图像信息: 尺寸={pil_image.size}, 文件大小={os.path.getsize(temp_path)}字节"
                
                return analysis_result, None
            
            # 生成结果文本
            result_text = "📊 OCR识别结果:\n" + "="*50 + "\n\n"
            
            high_confidence_count = 0
            medium_confidence_count = 0
            low_confidence_count = 0
            
            for i, result in enumerate(results, 1):
                confidence = result['confidence']
                
                # 分类置信度
                if confidence > 0.8:
                    confidence_indicator = "🟢"
                    high_confidence_count += 1
                elif confidence > 0.6:
                    confidence_indicator = "🟡"
                    medium_confidence_count += 1
                else:
                    confidence_indicator = "🔴"
                    low_confidence_count += 1
                
                result_text += f"{i:2d}. {confidence_indicator} {result['extracted_text']}\n"
                result_text += f"     (置信度: {confidence:.3f})\n\n"
            
            # 保存CSV文件
            os.makedirs('assets/results', exist_ok=True)
            csv_path = "assets/results/ocr_results_uploaded.csv"
            active_processor.save_results_to_csv(results, csv_path)
            
            # 添加统计信息
            avg_confidence = sum(r['confidence'] for r in results) / len(results)
            result_text += f"\n📈 识别统计:\n"
            result_text += f"• 总计识别文字行数: {len(results)}\n"
            result_text += f"• 平均置信度: {avg_confidence:.3f}\n"
            result_text += f"• 高置信度(>0.8): {high_confidence_count}行\n"
            result_text += f"• 中等置信度(0.6-0.8): {medium_confidence_count}行\n"
            result_text += f"• 低置信度(<0.6): {low_confidence_count}行\n"
            result_text += f"\n💾 CSV结果文件: {csv_path}\n"
            result_text += f"📄 可下载CSV文件查看详细数据"
            
            # 添加质量评估
            if avg_confidence > 0.8:
                result_text += "\n\n🌟 识别质量: 优秀"
            elif avg_confidence > 0.6:
                result_text += "\n\n👍 识别质量: 良好"
            else:
                result_text += "\n\n⚠️ 识别质量: 一般，建议改进图像质量"
            
            print(f"✅ OCR识别完成，共识别{len(results)}行文字，平均置信度:{avg_confidence:.3f}")
            return result_text, csv_path
            
        except Exception as ocr_error:
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ OCR识别错误: {ocr_error}")
            print(f"详细错误: {error_trace}")
            
            error_message = f"❌ OCR识别失败: {str(ocr_error)}\n\n"
            error_message += "🔧 可能的解决方案:\n"
            error_message += "1. 重新运行脚本\n"
            error_message += "2. 检查PaddleOCR是否正确安装\n"
            error_message += "3. 尝试重启Python环境\n"
            error_message += "4. 确认图像格式是否支持\n\n"
            error_message += "📋 技术信息:\n"
            error_message += f"错误类型: {type(ocr_error).__name__}\n"
            error_message += f"错误详情: {str(ocr_error)}"
            
            return error_message, None
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ 处理过程中发生未预期错误: {e}")
        print(f"详细错误: {error_trace}")
        
        error_message = f"❌ 处理失败: {str(e)}\n\n"
        error_message += "🔧 通用解决方案:\n"
        error_message += "1. 检查图像文件是否完整\n"
        error_message += "2. 尝试上传不同格式的图像\n"
        error_message += "3. 确认图像文件大小合理(<10MB)\n"
        error_message += "4. 重新运行脚本并重试\n"
        error_message += f"\n📋 错误详情: {str(e)}"
        
        return error_message, None


def create_gradio_interface():
    """创建Gradio界面"""
    
    interface = gr.Interface(
        fn=process_uploaded_image,
        inputs=[
            gr.Image(
                label="📤 上传医疗文档图像", 
                type="numpy",  # 使用numpy格式便于处理
                sources=["upload", "clipboard"],  # 支持上传和剪贴板
            )
        ],
        outputs=[
            gr.Textbox(
                label="📊 OCR识别结果", 
                lines=20,
                max_lines=30,
                show_copy_button=True
            ),
            gr.File(
                label="📥 下载CSV结果文件",
                file_types=[".csv"]
            )
        ],
        title="🏥 医疗文档OCR识别系统 v1.3.7",
        description="""
        **🎯 功能说明**: 上传医疗文档图像，自动识别其中的文字内容并生成CSV报告
        
        **📋 支持格式**: PNG、JPG、JPEG等常见图像格式
        
        **🌟 特色功能**: 
        • 支持中英文混合识别  
        • 自动置信度评估  
        • 结构化CSV输出  
        • 高精度OCR引擎
        • 图像质量自动优化
        
        **💡 使用提示**: 
        • 确保图像清晰，文字大小适中
        • 避免图像过暗或过亮
        • 建议文档平整，避免严重倾斜
        • 推荐使用高分辨率图像以获得更好效果
        
        **🔧 更新内容 (v1.3.7)**:
        • 修复了Colab和本地环境的OCR兼容性问题
        • 增强图像预处理和错误处理机制
        • 改进了识别结果的展示和分析
        • 优化了多种PaddleOCR API调用方式
        """,
        theme="soft",
        css="""
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .output-text {
            font-family: 'Courier New', monospace;
        }
        """,
        analytics_enabled=False  # 禁用分析以保护隐私
    )
    
    return interface


def main():
    """主函数"""
    global ocr_processor
    
    print("🌐 启动医疗OCR Gradio演示...")
    print("📋 版本: v1.3.12 - 修复Gradio界面调试信息显示和清理不准确描述")
    
    try:
        # 初始化OCR处理器
        print("🔧 正在初始化OCR处理器...")
        ocr_processor = MedicalOCRProcessor()
        print("✅ OCR处理器初始化成功!")
        
        # 创建界面
        interface = create_gradio_interface()
        
        print("✅ Gradio界面创建成功!")
        print("🚀 启动本地Web服务...")
        print("💡 浏览器将自动打开，或手动访问显示的URL")
        print("🛑 按 Ctrl+C 停止服务")
        
        # 启动界面
        interface.launch(
            server_name="0.0.0.0",  # 允许外部访问
            server_port=7860,       # 指定端口
            share=False,            # 本地运行不需要公网分享
            debug=False,            # 关闭调试模式
            show_error=True,        # 显示错误信息
            inbrowser=True,         # 自动打开浏览器
            max_threads=4           # 限制线程数
        )
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查：")
        print("1. PaddleOCR是否正确安装")
        print("2. 端口7860是否被占用")
        print("3. Python环境是否正确")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")


if __name__ == "__main__":
    # 初始化全局OCR处理器
    ocr_processor = None
    main()