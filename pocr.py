import json
import glob
import os
import re  
#防止编码错误
# def convert_json_files_to_utf8(file_path):   
#     json_files = glob.glob(os.path.join(file_path, '*.json'))  
  
#     for file_path in json_files:   
#         with open(file_path, 'r', encoding='gbk') as file:  
#             content = file.read()  
          
#         # 用UTF-8编码保存文件  
#         with open(file_path, 'w', encoding='utf-8') as file:  
#             file.write(content)  
def convert_unicode_to_utf8_in_folder(folder_path):  
    # 获取文件夹中所有的 JSON 文件  
    json_files = glob.glob(os.path.join(folder_path, '*.json'))  
  
    for file_path in json_files:  
        try:  
            # 读取文件内容  
            with open(file_path, 'r', encoding='utf-8') as f:  
                content = f.read()  
  
            # 修复无效的转义序列  
            content = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', content)  
  
            # 尝试解析 JSON 数据  
            data = json.loads(content)  
        except json.JSONDecodeError as e:  
            print(f"Error decoding JSON from file {file_path}: {e}")  
            continue  
        except UnicodeDecodeError as e:  
            print(f"Error decoding text from file {file_path}: {e}")  
            continue  
  
        # 将数据以 UTF-8 编码写回原文件  
        with open(file_path, 'w', encoding='utf-8') as f:  
            json.dump(data, f, ensure_ascii=False, indent=4)  
        
with open('./config/paddlex_config.json', 'r', encoding='utf-8') as file:  
    config_data = json.load(file)  
    input_path=config_data.get('user_setting').get('img_path')
    output_path=config_data.get('user_setting').get('output_path')

from paddlex import create_pipeline

pipeline = create_pipeline(pipeline="OCR")
output = pipeline.predict([input_path])
for res in output:
    res.print()
    res.save_to_img(output_path)
    res.save_to_json(output_path,ensure_ascii = True)

#convert_json_files_to_utf8(output_path)

convert_unicode_to_utf8_in_folder(output_path)

