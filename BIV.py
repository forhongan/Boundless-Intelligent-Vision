import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
from PIL import Image, ImageTk  
import json  
import subprocess  
import webbrowser  
  
# 加载 JSON 配置文件并返回数据  
def load_json(file_path):  
    with open(file_path, 'r', encoding='utf-8') as file:  
        return json.load(file)  
  
# 更新 JSON 配置文件的数据  
def update_json(file_path, data):  
    with open(file_path, 'w', encoding='utf-8') as file:  
        json.dump(data, file, ensure_ascii=False, indent=4)  
  
# 配置路径信息，通过加载默认配置  
def configure_paths(config_path, default_key):  
    config_data = load_json(config_path)  
    settings = config_data[default_key]  
    img_path_var.set(settings['img_path'])  
    output_path_var.set(settings['output_path'])  
  
# 打开 GitHub 项目页面  
def open_github():  
    webbrowser.open('https://github.com/forhongan/Boundless-Intelligent-Vision')  
  
# 打开邮件客户端发送反馈  
def send_feedback():  
    email = '1220023205@student.must.edu.mo'  
    subject = '反馈主题'  
    body = '这是反馈内容。'  
    webbrowser.open(f'mailto:{email}?subject={subject}&body={body}')  
  
# 启动 OCR 处理过程并处理结果  
def start_process():  
    img_path = img_path_var.get()  
    output_path = output_path_var.get()  
    config_data = load_json(paddlex_config_path)  
    config_data['user_setting']['img_path'] = img_path  
    config_data['user_setting']['output_path'] = output_path  
    update_json(paddlex_config_path, config_data)  
      
    # 运行 OCR 脚本  
    result = subprocess.run(['python', 'pocr.py'], capture_output=True, text=True)  
    if result.returncode == 0:  
        messagebox.showinfo("Success", "OCR成功完成。\n正在启动翻译...")  
        # 运行翻译脚本  
        subprocess.run(['python', 'translater.py'])  
    else:  
        messagebox.showerror("Error", "OCR执行失败，请检查错误信息。")  
        print(result.stderr)  
  
# 主函数，设置 GUI 和事件绑定  
def main():  
    global img_path_var, output_path_var, paddlex_config_path  
    paddlex_config_path = './config/paddlex_config.json'  
      
    root = tk.Tk()  
    root.title("OCR 和 翻译工具")  
    root.geometry("600x400")  
      
    # 创建画布用于放置背景图片  
    canvas = tk.Canvas(root, width=600, height=400)  
    canvas.pack(fill="both", expand=True)  
      
    # 加载和设置背景图片  
    background_image = Image.open("src/assets/background/background.png")  
    background_image = background_image.resize((600, 400), Image.LANCZOS)  
    background_photo = ImageTk.PhotoImage(background_image)  
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  
      
    # 加载和设置 logo 图片  
    logo_image = Image.open("src/assets/logo/logo.png")  
    logo_image = logo_image.resize((50, 50), Image.LANCZOS)  
    logo_photo = ImageTk.PhotoImage(logo_image)  
    canvas.create_image(10, 10, image=logo_photo, anchor="nw")  
      
    # 绘制有阴影的文字  
    canvas.create_text(300, 30, text="OCR 和 翻译工具", font=("Arial", 16, "bold"), fill="white")  
    canvas.create_text(300, 80, text="这是一个简单的OCR和翻译工具，\n请输入路径并点击开始。", font=("Arial", 12), fill="white")  
      
    # 设置图像路径输入框和标签  
    img_path_label = tk.Label(root, text="图像路径:", bg="lightgray")  
    canvas.create_window(100, 130, window=img_path_label)  
      
    img_path_var = tk.StringVar()  
    img_path_entry = tk.Entry(root, textvariable=img_path_var, width=50)  
    canvas.create_window(350, 130, window=img_path_entry)  
      
    # 设置输出路径输入框和标签  
    output_path_label = tk.Label(root, text="输出路径:", bg="lightgray")  
    canvas.create_window(100, 170, window=output_path_label)  
      
    output_path_var = tk.StringVar()  
    output_path_entry = tk.Entry(root, textvariable=output_path_var, width=50)  
    canvas.create_window(350, 170, window=output_path_entry)  
      
    # 加载默认路径配置  
    configure_paths(paddlex_config_path, "user_setting")  
      
    # 使用 ttk.Button 创建带有样式的按钮  
    style = ttk.Style()  
    style.configure("TButton", font=("Arial", 10, "bold"), relief="raised", padding=6)  
      
    start_button = ttk.Button(root, text="开始", command=start_process, style="TButton")  
    canvas.create_window(300, 220, window=start_button)  
      
    help_button = ttk.Button(root, text="帮助", command=lambda: messagebox.showinfo("帮助", "请设置路径后点击开始。"), style="TButton")  
    canvas.create_window(300, 260, window=help_button)  
      
    feedback_button = ttk.Button(root, text="发送反馈", command=send_feedback, style="TButton")  
    canvas.create_window(300, 300, window=feedback_button)  
      
    github_button = ttk.Button(root, text="访问GitHub", command=open_github, style="TButton")  
    canvas.create_window(300, 340, window=github_button)  
      
    root.mainloop()  
  
# 程序入口  
if __name__ == "__main__":  
    main() 