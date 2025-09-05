#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时截图并比对差异工具
选中控件后定时截图，比较前后两张图片，有差异则保存
"""
import sys
import os
import time
import shutil
from datetime import datetime
import hashlib
import importlib.util
import uiautomation as auto
import requests

def get_file_hash(filepath):
    # 计算文件的MD5哈希值
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def compare_images(img1_path, img2_path):
    # 通过文件哈希值比较两张图片是否相同
    # 返回True表示有差异，False表示无差异
    hash1 = get_file_hash(img1_path)
    hash2 = get_file_hash(img2_path)
    if hash1 is None or hash2 is None:
        return True  # 如果读取失败，认为有差异
    return hash1 != hash2


# 导入 qwen-vl.py 的识别函数
qwen_vl_path = os.path.join(os.path.dirname(__file__), "qwen-vl.py")
spec = importlib.util.spec_from_file_location("qwen_vl", qwen_vl_path)
qwen_vl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qwen_vl)

# 选中要截图的控件
print("请将鼠标放在要截图的控件上...")
time.sleep(3)

control = auto.ControlFromCursor()
if not control:
    print("未找到控件")
    exit()

print(f"已选中: {control.ControlType} - {control.ClassName}")

# 设置截图参数
interval = 10  # 间隔2秒
save_folder = "capture_diff"  # 保存差异图片的文件夹

# 创建保存文件夹
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

print(f"开始定时截图比对：每{interval}秒一次")
print(f"有差异的图片将保存到 '{save_folder}' 文件夹")
print("按 Ctrl+C 停止")

# 用于存储上一张图片的路径
previous_image = None
temp_image = "temp_capture.png"
capture_count = 0
saved_count = 0

# 开始截图循环
try:
    while True:
        capture_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 包含毫秒
        
        control.SetFocus()
        
        # 截图到临时文件
        if control.CaptureToImage(temp_image):
            print(f"第 {capture_count} 次截图完成", end="")
            
            # 如果是第一张图片，直接保存作为基准
            if previous_image is None:
                previous_image = os.path.join(save_folder, f"base_{timestamp}.png")
                if os.path.exists(temp_image):
                    # 复制文件而不是移动，保留临时文件用于下次比较
                    shutil.copy2(temp_image, previous_image)
                    saved_count += 1
                    print(f" -> 保存基准图片: {os.path.basename(previous_image)}")
                else:
                    print(" -> 截图失败")
            else:
                # 比较当前图片与上一张图片
                if os.path.exists(temp_image) and os.path.exists(previous_image):
                    has_difference = compare_images(previous_image, temp_image)
                    
                    if has_difference:
                        # 有差异，保存当前图片
                        new_filename = os.path.join(save_folder, f"diff_{timestamp}.png")
                        shutil.copy2(temp_image, new_filename)
                        saved_count += 1
                        print(f" -> 发现差异！保存: {os.path.basename(new_filename)}")

                        # 调用 Qwen-VL 识别图片内容并保存 JSON
                        try:
                            print("    正在识别图片内容...")
                            json_result = qwen_vl.qwen_vl_recognize(new_filename)
                            json_path = os.path.join(save_folder, f"diff_{timestamp}.json")
                            # 直接保存原始字符串，确保格式
                            with open(json_path, "w", encoding="utf-8") as jf:
                                jf.write(json_result)
                            print(f"    识别结果已保存: {os.path.basename(json_path)}")
                            
                            # 发送 json 到接口
                            try:
                                import json
                                json_obj = json.loads(json_result)
                                url = "http://127.0.0.1:10010/text"
                                if json_obj.get("records") and len(json_obj["records"]) > 0:
                                    for idx, rec in enumerate(json_obj["records"]):
                                        msg_str = f"{rec.get('time','')}\n{rec.get('speaker','')}\n{rec.get('content','')}"
                                        receiver = "家庭组"
                                        post_data = {
                                            "msg": msg_str,
                                            "receiver": receiver
                                        }
                                        resp = requests.post(url, json=post_data, timeout=10)
                                        if resp.status_code == 200:
                                            print(f"    已发送第{idx+1}条到接口，联系人: {receiver}")
                                        else:
                                            print(f"    接口返回异常: {resp.status_code} {resp.text}")
                                else:
                                    print("    识别结果无 records 可发送")
                            except Exception as e:
                                print(f"    发送到接口失败: {e}")
                        except Exception as e:
                            print(f"    识别失败: {e}")

                        # 更新基准图片路径
                        previous_image = new_filename
                    else:
                        print(" -> 无差异")
                else:
                    print(" -> 比较失败")
        else:
            print(f"第 {capture_count} 次截图失败")
        
        time.sleep(interval)
        
except KeyboardInterrupt:
    print("\n\n截图结束！")
    print(f"总共截图: {capture_count} 次")
    print(f"保存图片: {saved_count} 张")
    
    # 清理临时文件
    if os.path.exists(temp_image):
        os.remove(temp_image)
    
    print(f"差异图片保存在: {os.path.abspath(save_folder)}")

print("\n程序结束")

print("截图结束")
