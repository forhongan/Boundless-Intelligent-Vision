import requests  
import json  
import os  
from datetime import datetime  

#读取设置的内容
with open('./config/_config.json', 'r', encoding='utf-8') as file:  
    config_data = json.load(file)  
    ENDPOINT=config_data.get('Azure_setting').get("path").get("azure_chat_api")
    API_KEY=config_data.get('Azure_setting').get("key").get("azure_api_key")

    
#读取需要翻译的内容
with open('./datas/log/test1.json', 'r', encoding='utf-8') as file:  
    data = json.load(file) 
    text_input = data.get('rec_text')
    #print(text_input)

text_input = "This is a test!"
print("Hello,this is biv.")

prompt_input = "请将输入的内容翻译为简体中文"

headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
}  
payload = {  
    "messages": [  
        {  
            "role": "system",  
            "content": [  
                {  
                    "type": "text",  
                    "text": prompt_input 
                }  
            ]  
        },  
        {  
            "role": "user",  
            "content": [  
                {  
                    "type": "text",  
                    "text": text_input
                }  
            ]  
        }  
    ],  
    "temperature": 0.7,  
    "top_p": 0.95,  
    "max_tokens": 800  
}  

# Send request  
try:  
    response = requests.post(ENDPOINT, headers=headers, json=payload)  
    response.raise_for_status()  
    result = response.json()  
  
    # Extract AI response  
    ai_response = result['choices'][0]['message']['content']  
  
    # Prepare log entry  
    log_entry = {  
        "timestamp": datetime.now().isoformat(),  
        "user_input": text_input,  
        "ai_response": ai_response  
    }  

    # Print AI response  
    print(ai_response) 

    # Write to a log file  
    log_file_path = os.path.join("datas", "result", "chat_history.json")   
    if os.path.exists(log_file_path):  
        with open(log_file_path, "r", encoding="utf-8") as log_file:  
            history = json.load(log_file)  
    else:  
        history = []  
  
    history.append(log_entry)  
  
    with open(log_file_path, "w", encoding="utf-8") as log_file:  
        json.dump(history, log_file, ensure_ascii=False, indent=4)  
  
     

except requests.RequestException as e:  
    raise SystemExit(f"Failed to make the request. Error: {e}")  