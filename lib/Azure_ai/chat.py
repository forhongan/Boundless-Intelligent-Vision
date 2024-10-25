import requests  
  
# Configuration  
API_KEY = "66397f887f1b40c1b1b15faf4779ebd9"  
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
}  
  
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
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code  
except requests.RequestException as e:  
    raise SystemExit(f"Failed to make the request. Error: {e}")  
  
# Handle the response as needed (e.g., print or process)  
print(response.json())  
