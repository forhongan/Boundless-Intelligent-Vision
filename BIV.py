import json  
import os  
import subprocess  

def say_hello():
    print(
        """
         ____                                __   ___                            
        /\  _`\                             /\ \ /\_ \                           
        \ \ \L\ \    ___   __  __    ___    \_\ \\//\ \      __    ____    ____  
         \ \  _ <'  / __`\/\ \/\ \ /' _ `\  /'_` \ \ \ \   /'__`\ /',__\  /',__\ 
          \ \ \L\ \/\ \L\ \ \ \_\ \/\ \/\ \/\ \L\ \ \_\ \_/\  __//\__, `\/\__, `\
           \ \____/\ \____/\ \____/\ \_\ \_\ \___,_\/\____\ \____\/\____/\/\____/
            \/___/  \/___/  \/___/  \/_/\/_/\/__,_ /\/____/\/____/\/___/  \/___/ 
                                                                         
                                                                         
         ______          __           ___    ___                               __        __  __                                     
        /\__  _\        /\ \__       /\_ \  /\_ \    __                       /\ \__    /\ \/\ \  __          __                    
        \/_/\ \/     ___\ \ ,_\    __\//\ \ \//\ \  /\_\     __      __    ___\ \ ,_\   \ \ \ \ \/\_\    ____/\_\    ___     ___    
           \ \ \   /' _ `\ \ \/  /'__`\\ \ \  \ \ \ \/\ \  /'_ `\  /'__`\/' _ `\ \ \/    \ \ \ \ \/\ \  /',__\/\ \  / __`\ /' _ `\  
            \_\ \__/\ \/\ \ \ \_/\  __/ \_\ \_ \_\ \_\ \ \/\ \L\ \/\  __//\ \/\ \ \ \_    \ \ \_/ \ \ \/\__, `\ \ \/\ \L\ \/\ \/\ \ 
            /\_____\ \_\ \_\ \__\ \____\/\____\/\____\\ \_\ \____ \ \____\ \_\ \_\ \__\    \ `\___/\ \_\/\____/\ \_\ \____/\ \_\ \_\
            \/_____/\/_/\/_/\/__/\/____/\/____/\/____/ \/_/\/___L\ \/____/\/_/\/_/\/__/     `\/__/  \/_/\/___/  \/_/\/___/  \/_/\/_/
                                                     /\____/                                                                
                                                     \_/__/                                                                 
        -----------------------------------------------------------------------------------------------------
            欢迎使用 Boundless Intelligent Vision 
            Boundless Intelligent Vision 是一款正在开发中的,全场景翻译工具
            目前还处在开发阶段
        """
    )
def load_json(file_path):  
    with open(file_path, 'r', encoding='utf-8') as file:  
        return json.load(file)  
  
def update_json(file_path, data):  
    with open(file_path, 'w', encoding='utf-8') as file:  
        json.dump(data, file, ensure_ascii=False, indent=4)  
  
def user_choice(prompt, choices):  
    print(prompt)  
    for i, choice in enumerate(choices, 1):  
        print(f"{i}. {choice}")  
    selection = int(input("请选择选项: "))  
    return choices[selection - 1]  
  
def configure_paths(config_path, default_key):  
    config_data = load_json(config_path)  
    settings = config_data[default_key]  
      
    # 显示默认设置  
    print(f"默认设置:\n图像路径: {settings['img_path']}\n输出路径: {settings['output_path']}")  
      
    choice = user_choice("是否使用默认设置?", ["是", "否"])  
    if choice == "否":  
        img_path = input("请输入图像路径: ")  
        output_path = input("请输入输出路径: ")  
        settings['img_path'] = img_path  
        settings['output_path'] = output_path  
      
    update_json(config_path, config_data)  
    return settings   
  
def main():  
    paddlex_config_path = './config/paddlex_config.json'  
    #ai_config_path = './config/ai_config.json'  
    
    say_hello()
    
    # 配置用户路径  
    print("配置OCR路径:")  
    ocr_settings = configure_paths(paddlex_config_path, "user_setting")  
  
    # 启动pocr.py  
    print("正在启动OCR...")  
    result = subprocess.run(['python', 'pocr.py'], capture_output=True, text=True)  
    if result.returncode == 0:  
        print("OCR成功完成。\n")  
        # 启动translater.py  
        print("正在启动翻译...")  
        subprocess.run(['python', 'translater.py'])  
    else:  
        print("OCR执行失败，请检查错误信息。")  
        print(result.stderr)  
  
if __name__ == "__main__":  
    main()  