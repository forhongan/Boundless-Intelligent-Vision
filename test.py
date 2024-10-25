import requests  
import json  
import os  
from datetime import datetime  

#读取设置的内容
with open('./config/_config.json', 'r', encoding='utf-8') as file:  
    config_data = json.load(file)  
    ENDPOINT=config_data.get('Azure_setting').get("path").get("azure_chat_api")
    print(ENDPOINT)
    
#读取需要翻译的内容
with open('./datas/log/test1.json', 'r', encoding='utf-8') as file:  
    data = json.load(file) 
    text_input = data.get('rec_text')
    print(text_input)