import requests  
import json  
import os  
from datetime import datetime  
  
# Configuration  
API_KEY = "66397f887f1b40c1b1b15faf4779ebd9"  
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
}  
  
# Create a directory for storing logs if it doesn't exist  
os.makedirs("logs", exist_ok=True)  
  
# Input from user  
user_input = input("请输入你想询问的问题：")  
  
# Payload for the request  
payload = {  
    "messages": [  
        {  
            "role": "system",  
            "content": [  
                {  
                    "type": "text",  
                    "text": "你是一个帮助用户查找信息的 AI 助手。"  
                }  
            ]  
        },  
        {  
            "role": "user",  
            "content": [  
                {  
                    "type": "text",  
                    "text": user_input  
                }  
            ]  
        }  
    ],  
    "temperature": 0.7,  
    "top_p": 0.95,  
    "max_tokens": 800  
}  
  
ENDPOINT = "https://vm101a.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"  
  
# Send request  
try:  
    response = requests.post(ENDPOINT, headers=headers, json=payload)  
    response.raise_for_status()  
    result = response.json()  
  
    # Extract AI response  
    translate_result = result['choices'][0]['message']['content']  
  
    # Prepare log entry  
    log_entry = {  
        "timestamp": datetime.now().isoformat(),  
        "user_input": user_input,  
        "translate_result": translate_result  
    }  
  
    # Write to a log file  
    log_file_path = os.path.join("logs", "chat_history.json")  
    if os.path.exists(log_file_path):  
        with open(log_file_path, "r", encoding="utf-8") as log_file:  
            history = json.load(log_file)  
    else:  
        history = []  
  
    history.append(log_entry)  
  
    with open(log_file_path, "w", encoding="utf-8") as log_file:  
        json.dump(history, log_file, ensure_ascii=False, indent=4)  
  
    # Print AI response  
    print(translate_result)  
  
except requests.RequestException as e:  
    raise SystemExit(f"Failed to make the request. Error: {e}")  
