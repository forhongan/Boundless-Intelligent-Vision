# config_reader.py  
import json  
  
# 全局变量  
config = {}  
  
def load_config(file_path):  
    global config  
    with open(file_path, 'r') as file:  
        config = json.load(file)  
  
# 在模块加载时读取配置  
load_config('config.json')  