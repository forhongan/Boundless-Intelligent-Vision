import os  
import json  
  
# 定义文件夹路径  
ocr_result_folder = 'datas/ocr_result'  
result_folder = 'datas/result'  
textfill_folder = 'datas/textfill'  
  
# 确保目标文件夹存在  
os.makedirs(textfill_folder, exist_ok=True)  
  
# 遍历ocr_result文件夹中的每个文件  
for filename in os.listdir(ocr_result_folder):  
    if filename.endswith('.json'):  
        ocr_result_path = os.path.join(ocr_result_folder, filename)  
        result_path = os.path.join(result_folder, filename)  
  
        # 检查对应的result文件是否存在  
        if os.path.exists(result_path):  
            # 读取ocr_result文件  
            with open(ocr_result_path, 'r', encoding='utf-8') as f:  
                ocr_data = json.load(f)  
  
            # 读取result文件  
            with open(result_path, 'r', encoding='utf-8') as f:  
                result_data = json.load(f)  
  
            # 提取ai_response内容并分割  
            ai_response = result_data.get("ai_response", "")  
            textfill = ai_response.strip('[]').split('] [')  
  
            # 添加textfill到ocr_data中  
            ocr_data["textfill"] = textfill  
  
            # 合并后的文件路径  
            textfill_path = os.path.join(textfill_folder, filename)  
  
            # 写入合并后的文件  
            with open(textfill_path, 'w', encoding='utf-8') as f:  
                json.dump(ocr_data, f, ensure_ascii=False, indent=4)  
  
            print(f"合并完成: {filename}")  
  