import requests  
import json  
import os  
from datetime import datetime  
  
# 读取设置的内容  
with open('./config/ai_config.json', 'r', encoding='utf-8') as file:  
    config_data = json.load(file)  
    ENDPOINT = config_data.get('Azure_setting').get("path").get("azure_chat_api")  
    API_KEY = config_data.get('Azure_setting').get("key").get("azure_api_key")  
    prompt_input = config_data.get('Azure_setting').get("prompt") 
 
with open('./config/paddlex_config.json', 'r', encoding='utf-8') as file: 
    pdx_data=json.load(file)  
    ocr_result_dir = pdx_data.get('user_setting').get('output_path')    

headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
}  
  
# 读取 ./datas/ocr_result/ 文件夹下的所有 .json 文件  
#ocr_result_dir = './datas/ocr_result'  
for filename in os.listdir(ocr_result_dir):  
    if filename.endswith('.json'):  
        file_path = os.path.join(ocr_result_dir, filename)  
        with open(file_path, 'r', encoding='utf-8') as file:  
            data = json.load(file)  
            rec_text_list = data.get('rec_text', [])  
            text_input = ' '.join([f"[{text}]" for text in rec_text_list])  
            print(f"Processing file: {filename}")  
            print(f"Text input: {text_input}")  
  
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
  
                # Write to a log file with the same name as the input file  
                log_file_name = os.path.splitext(filename)[0] + ".json"  
                log_file_path = os.path.join("datas", "result", log_file_name)  
  
                # Ensure the result directory exists  
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  
  
                # Write log entry to the corresponding file  
                with open(log_file_path, "w", encoding="utf-8") as log_file:  
                    json.dump(log_entry, log_file, ensure_ascii=False, indent=4)   
  
            except requests.RequestException as e:  
                raise SystemExit(f"Failed to make the request. Error: {e}")  