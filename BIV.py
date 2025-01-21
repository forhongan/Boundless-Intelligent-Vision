import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
from PIL import Image, ImageTk  
import json  
import subprocess  
import webbrowser  
import threading  

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
        translate_result = subprocess.run(['python', 'translater.py'], capture_output=True, text=True)  
        if translate_result.returncode == 0:  
            messagebox.showinfo("Success", "翻译完成，正在回填文本并生成译后图像！")  
            # 运行文本回填脚本  
            fill_result = subprocess.run(['python', 'text_fill-in-img.py'], capture_output=True, text=True)  
            if fill_result.returncode == 0:  
                messagebox.showinfo("Success", "文本回填和图像生成完成！")  
            else:  
                messagebox.showerror("Error", "文本回填执行失败，请检查错误信息。")  
                print(fill_result.stderr)  
        else:  
            messagebox.showerror("Error", "翻译执行失败，请检查错误信息。")  
            print(translate_result.stderr)  
    else:  
        messagebox.showerror("Error", "OCR执行失败，请检查错误信息。")  
        print(result.stderr)  
  
# 选择输入文件路径
def select_input_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        img_path_var.set(file_path)
        save_settings()

# 选择输出文件路径
def select_output_file():
    file_path = filedialog.askdirectory()
    if file_path:
        output_path_var.set(file_path)
        save_settings()

# 启动 AI_interaction 脚本  
def start_ai_interaction():  
    def run_ai_interaction():  
        ai_result = subprocess.run(['python', 'AI_interaction.py'], capture_output=True, text=True)  
        if ai_result.returncode == 0:  
            messagebox.showinfo("Success", "AI 交互脚本成功启动！")  
        else:  
            messagebox.showerror("Error", "AI 交互脚本启动失败，请检查错误信息。")  
            print(ai_result.stderr)  
      
    # 在新线程中运行 AI 交互脚本  
    threading.Thread(target=run_ai_interaction).start()  

# 保存设置到 user_setting
def save_settings():
    img_path = img_path_var.get()
    output_path = output_path_var.get()
    config_data = load_json(paddlex_config_path)
    config_data['user_setting']['img_path'] = img_path
    config_data['user_setting']['output_path'] = output_path
    config_data['user_setting']['lang'] = interface_language_var.get()
    update_json(paddlex_config_path, config_data)

# 还原默认设置
def restore_settings():
    config_data = load_json(paddlex_config_path)
    default_settings = config_data['default_setting']
    config_data['user_setting'] = default_settings
    update_json(paddlex_config_path, config_data)
    configure_paths(paddlex_config_path, "user_setting")
    messagebox.showinfo("Success", "已还原默认设置。")

# 更新 Azure_setting 中的 prompt 和 interaction_prompt
def update_prompts(language):
    config_data = load_json(ai_config_path)
    azure_setting = config_data['Azure_setting']
    default_setting = config_data['default_setting']
    
    azure_setting['prompt'] = default_setting[f'prompt_{language}']
    azure_setting['interaction_prompt'] = default_setting[f'interaction_prompt_{language}']
    azure_setting['language'] = language
    
    update_json(ai_config_path, config_data)

# 界面文本字典
ui_texts = {
    "cn": {
        "title": "OCR 和 翻译工具",
        "description": "这是一个简单的OCR和翻译工具，\n请输入路径并点击开始。",
        "img_path_label": "图像路径:",
        "output_path_label": "输出路径:",
        "select_file": "选择文件",
        "select_folder": "选择文件夹",
        "start_button": "开始",
        "save_button": "保存设置",
        "restore_button": "还原设置",
        "help_button": "帮助",
        "feedback_button": "发送反馈",
        "github_button": "访问GitHub",
        "ai_interaction_button": "使用Ai交互-beta",
        "language_label": "选择界面语言:",
        "translation_language_label": "选择翻译语言:"
    },
    "en": {
        "title": "OCR and Translation Tool",
        "description": "This is a simple OCR and translation tool.\nPlease enter the path and click start.",
        "img_path_label": "Image Path:",
        "output_path_label": "Output Path:",
        "select_file": "Select File",
        "select_folder": "Select Folder",
        "start_button": "Start",
        "save_button": "Save Settings",
        "restore_button": "Restore Settings",
        "help_button": "Help",
        "feedback_button": "Send Feedback",
        "github_button": "Visit GitHub",
        "ai_interaction_button": "Use AI Interaction-beta",
        "language_label": "Select Interface Language:",
        "translation_language_label": "Select Translation Language:"
    },
    "cnt": {  
        "title": "OCR 和 翻譯工具",  
        "description": "這是一個簡單的OCR和翻譯工具，\n請輸入路徑並點擊開始。",  
        "img_path_label": "圖像路徑:",  
        "output_path_label": "輸出路徑:",  
        "select_file": "選擇文件",  
        "select_folder": "選擇文件夾",  
        "start_button": "開始",  
        "save_button": "保存設置",  
        "restore_button": "還原設置",  
        "help_button": "幫助",  
        "feedback_button": "發送反饋",  
        "github_button": "訪問GitHub",  
        "ai_interaction_button": "使用Ai交互-beta",  
        "language_label": "選擇界面語言:",  
        "translation_language_label": "選擇翻譯語言:"  
    },  
    "fr": {  
        "title": "Outil OCR et de Traduction",  
        "description": "C'est un outil simple d'OCR et de traduction.\nVeuillez entrer le chemin et cliquer sur démarrer.",  
        "img_path_label": "Chemin de l'image:",  
        "output_path_label": "Chemin de sortie:",  
        "select_file": "Sélectionner le fichier",  
        "select_folder": "Sélectionner le dossier",  
        "start_button": "Démarrer",  
        "save_button": "Sauvegarder les paramètres",  
        "restore_button": "Restaurer les paramètres",  
        "help_button": "Aide",  
        "feedback_button": "Envoyer des commentaires",  
        "github_button": "Visiter GitHub",  
        "ai_interaction_button": "Utiliser l'interaction AI-beta",  
        "language_label": "Sélectionner la langue de l'interface:",  
        "translation_language_label": "Sélectionner la langue de traduction:"  
    },  
    "de": {  
        "title": "OCR- und Übersetzungstool",  
        "description": "Dies ist ein einfaches OCR- und Übersetzungstool.\nBitte geben Sie den Pfad ein und klicken Sie auf Start.",  
        "img_path_label": "Bildpfad:",  
        "output_path_label": "Ausgabepfad:",  
        "select_file": "Datei auswählen",  
        "select_folder": "Ordner auswählen",  
        "start_button": "Starten",  
        "save_button": "Einstellungen speichern",  
        "restore_button": "Einstellungen wiederherstellen",  
        "help_button": "Hilfe",  
        "feedback_button": "Feedback senden",  
        "github_button": "GitHub besuchen",  
        "ai_interaction_button": "AI-Interaktion verwenden-beta",  
        "language_label": "Schnittstellensprache wählen:",  
        "translation_language_label": "Übersetzungssprache wählen:"  
    },
    "ja": {  
        "title": "OCRと翻訳ツール",  
        "description": "これはシンプルなOCRと翻訳ツールです。\nパスを入力して開始をクリックしてください。",  
        "img_path_label": "画像パス:",  
        "output_path_label": "出力パス:",  
        "select_file": "ファイルを選択",  
        "select_folder": "フォルダを選択",  
        "start_button": "開始",  
        "save_button": "設定を保存",  
        "restore_button": "設定を復元",  
        "help_button": "ヘルプ",  
        "feedback_button": "フィードバックを送信",  
        "github_button": "GitHubを訪問",  
        "ai_interaction_button": "AIインタラクションを使用-ベータ",  
        "language_label": "インターフェース言語を選択:",  
        "translation_language_label": "翻訳言語を選択:"  
    },  
    "ko": {  
        "title": "OCR 및 번역 도구",  
        "description": "이것은 간단한 OCR 및 번역 도구입니다.\n경로를 입력하고 시작을 클릭하세요.",  
        "img_path_label": "이미지 경로:",  
        "output_path_label": "출력 경로:",  
        "select_file": "파일 선택",  
        "select_folder": "폴더 선택",  
        "start_button": "시작",  
        "save_button": "설정 저장",  
        "restore_button": "설정 복원",  
        "help_button": "도움말",  
        "feedback_button": "피드백 보내기",  
        "github_button": "GitHub 방문",  
        "ai_interaction_button": "AI 상호작용 사용-베타",  
        "language_label": "인터페이스 언어 선택:",  
        "translation_language_label": "번역 언어 선택:"  
    }  ,
    "pt": {  
        "title": "Ferramenta de OCR e Tradução",  
        "description": "Esta é uma ferramenta simples de OCR e tradução.\nPor favor, insira o caminho e clique em iniciar.",  
        "img_path_label": "Caminho da Imagem:",  
        "output_path_label": "Caminho de Saída:",  
        "select_file": "Selecionar Arquivo",  
        "select_folder": "Selecionar Pasta",  
        "start_button": "Iniciar",  
        "save_button": "Salvar Configurações",  
        "restore_button": "Restaurar Configurações",  
        "help_button": "Ajuda",  
        "feedback_button": "Enviar Feedback",  
        "github_button": "Visitar GitHub",  
        "ai_interaction_button": "Usar Interação com AI-beta",  
        "language_label": "Selecionar Idioma da Interface:",  
        "translation_language_label": "Selecionar Idioma de Tradução:"  
    }  
    # ...add other languages here...
}

# 更新界面文本
def update_ui_texts(language):
    texts = ui_texts[language]
    root.title(texts["title"])
    canvas.itemconfig(title_text, text=texts["title"])
    canvas.itemconfig(description_text, text=texts["description"])
    img_path_label.config(text=texts["img_path_label"])
    output_path_label.config(text=texts["output_path_label"])
    select_input_button.config(text=texts["select_file"])
    select_output_button.config(text=texts["select_folder"])
    start_button.config(text=texts["start_button"])
    restore_button.config(text=texts["restore_button"])
    help_button.config(text=texts["help_button"])
    feedback_button.config(text=texts["feedback_button"])
    github_button.config(text=texts["github_button"])
    ai_interaction_button.config(text=texts["ai_interaction_button"])
    language_label.config(text=texts["language_label"])
    translation_language_label.config(text=texts["translation_language_label"])

# 界面语言选择回调函数
def on_interface_language_change(event):
    selected_language = interface_language_var.get()
    update_ui_texts(selected_language)
    save_settings()
    messagebox.showinfo("Success", f"界面语言已切换到 {selected_language}")

# 翻译语言选择回调函数
def on_translation_language_change(event):
    selected_language = translation_language_var.get()
    update_prompts(selected_language)
    save_settings()
    messagebox.showinfo("Success", f"翻译语言已切换到 {selected_language}")

# 主函数，设置 GUI 和事件绑定  
def main():  
    global img_path_var, output_path_var, paddlex_config_path, ai_config_path, interface_language_var, translation_language_var
    global root, canvas, title_text, description_text
    global img_path_label, output_path_label, select_input_button, select_output_button
    global start_button, restore_button, help_button, feedback_button, github_button, ai_interaction_button, language_label, translation_language_label

    paddlex_config_path = './config/paddlex_config.json'  
    ai_config_path = './config/ai_config.json'
  
    root = tk.Tk()  
    root.title("OCR 和 翻译工具")  
    root.geometry("700x500")  # 增大主界面大小
  
    # 创建画布用于放置背景图片  
    canvas = tk.Canvas(root, width=700, height=500)  
    canvas.pack(fill="both", expand=True)  
  
    # 加载和设置背景图片  
    background_image = Image.open("src/assets/background/background.jpg")  
    background_image = background_image.resize((700, 500), Image.LANCZOS)  
    background_photo = ImageTk.PhotoImage(background_image)  
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  
  
    # 加载和设置 logo 图片  
    logo_image = Image.open("src/assets/logo/logo.png")  
    logo_image = logo_image.resize((50, 50), Image.LANCZOS)  
    logo_photo = ImageTk.PhotoImage(logo_image)  
    canvas.create_image(10, 10, image=logo_photo, anchor="nw")  
  
    # 绘制有阴影的文字  
    title_text = canvas.create_text(350, 30, text="OCR 和 翻译工具", font=("Arial", 16, "bold"), fill="white")
    description_text = canvas.create_text(350, 80, text="这是一个简单的OCR和翻译工具，\n请输入路径并点击开始。", font=("Arial", 12), fill="white")
  
    # 设置图像路径输入框和标签  
    img_path_label = tk.Label(root, text="图像路径:", bg="lightgray")  
    canvas.create_window(150, 130, window=img_path_label)  
  
    img_path_var = tk.StringVar()  
    img_path_entry = tk.Entry(root, textvariable=img_path_var, width=50)  
    canvas.create_window(400, 130, window=img_path_entry)  

    # 新增选择输入文件按钮
    select_input_button = ttk.Button(root, text="选择文件", command=select_input_file, style="TButton")
    canvas.create_window(600, 130, window=select_input_button)
  
    # 设置输出路径输入框和标签  
    output_path_label = tk.Label(root, text="输出路径:", bg="lightgray")  
    canvas.create_window(150, 170, window=output_path_label)  
  
    output_path_var = tk.StringVar()  
    output_path_entry = tk.Entry(root, textvariable=output_path_var, width=50)  
    canvas.create_window(400, 170, window=output_path_entry)  

    # 新增选择输出文件夹按钮
    select_output_button = ttk.Button(root, text="选择文件夹", command=select_output_file, style="TButton")
    canvas.create_window(600, 170, window=select_output_button)
  
    # 界面语言选择标签和下拉菜单
    language_label = tk.Label(root, text="选择界面语言:", bg="lightgray")
    canvas.create_window(150, 210, window=language_label)

    interface_language_var = tk.StringVar()
    interface_language_options = ["cn","cnt","en","fr","de","ja","ko","pt"]  # 添加其他语言选项
    interface_language_menu = ttk.Combobox(root, textvariable=interface_language_var, values=interface_language_options, state="readonly")
    interface_language_menu.current(0)  # 默认选择第一个语言
    interface_language_menu.bind("<<ComboboxSelected>>", on_interface_language_change)
    canvas.create_window(400, 210, window=interface_language_menu)

    # 翻译语言选择标签和下拉菜单
    translation_language_label = tk.Label(root, text="选择翻译语言:", bg="lightgray")
    canvas.create_window(150, 250, window=translation_language_label)

    translation_language_var = tk.StringVar()
    translation_language_options = ["cn", "cnt", "en", "fr", "de", "ja", "ko", "pt"]  # 添加其他语言选项
    translation_language_menu = ttk.Combobox(root, textvariable=translation_language_var, values=translation_language_options, state="readonly")
    translation_language_menu.current(0)  # 默认选择第一个语言
    translation_language_menu.bind("<<ComboboxSelected>>", on_translation_language_change)
    canvas.create_window(400, 250, window=translation_language_menu)

    # 加载默认路径配置  
    configure_paths(paddlex_config_path, "user_setting")  
  
    # 使用 ttk.Button 创建带有样式的按钮  
    style = ttk.Style()  
    style.configure("TButton", font=("Arial", 10, "bold"), relief="raised", padding=6)  
  
    start_button = ttk.Button(root, text="开始", command=start_process, style="TButton")  
    canvas.create_window(350, 290, window=start_button)  

    # 删除保存设置按钮
    # save_button = ttk.Button(root, text="保存设置", command=save_settings, style="TButton")
    # canvas.create_window(150, 290, window=save_button)

    # 新增还原设置按钮
    restore_button = ttk.Button(root, text="还原设置", command=restore_settings, style="TButton")
    canvas.create_window(550, 290, window=restore_button)
  
    help_button = ttk.Button(root, text="帮助", command=lambda: messagebox.showinfo("帮助", "请设置路径后点击开始。"), style="TButton")  
    canvas.create_window(350, 330, window=help_button)  
  
    feedback_button = ttk.Button(root, text="发送反馈", command=send_feedback, style="TButton")  
    canvas.create_window(350, 370, window=feedback_button)  
  
    github_button = ttk.Button(root, text="访问GitHub", command=open_github, style="TButton")  
    canvas.create_window(350, 410, window=github_button)  
  
    # 新增 AI 交互按钮  
    ai_interaction_button = ttk.Button(root, text="使用Ai交互-beta", command=start_ai_interaction, style="TButton")  
    canvas.create_window(350, 450, window=ai_interaction_button)  
  
    root.mainloop()  
  
# 程序入口  
if __name__ == "__main__":  
    main()