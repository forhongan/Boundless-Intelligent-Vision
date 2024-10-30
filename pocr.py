import json
import glob
import os
#防止编码错误
def convert_json_files_to_utf8(file_path):   
    json_files = glob.glob(os.path.join(file_path, '*.json'))  
  
    for file_path in json_files:   
        with open(file_path, 'r', encoding='gbk') as file:  
            content = file.read()  
          
        # 用UTF-8编码保存文件  
        with open(file_path, 'w', encoding='utf-8') as file:  
            file.write(content)  

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
    res.save_to_json(output_path)

convert_json_files_to_utf8(output_path)

