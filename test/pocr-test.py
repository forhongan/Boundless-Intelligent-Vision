import json

with open('./config/config.json', 'r', encoding='utf-8') as file:  
    config_data = json.load(file)  
    input_path=config_data.get('img_path'+'/test1.png')
    output_path=config_data.get('output_path')

from paddlex import create_pipeline

pipeline = create_pipeline(pipeline="OCR")
output = pipeline.predict([input_path])
for res in output:
    res.print()
    res.save_to_img(output_path)
    res.save_to_json(output_path)