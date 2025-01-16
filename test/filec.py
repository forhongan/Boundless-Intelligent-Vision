import tkinter as tk  
from tkinter import filedialog  
  
def select_file():  
    # 使用文件选择对话框打开文件，并返回选择的文件路径  
    file_path = filedialog.askopenfilename(title="Select a file")  
    if file_path:  # 如果用户选择了文件，打印文件路径  
        print("Selected file:", file_path)  
    else:  
        print("No file selected.")  
  
def create_gui():  
    # 创建主窗口  
    root = tk.Tk()  
    root.withdraw()  # 隐藏主窗口，因为我们只需要文件选择对话框  
  
    # 调用文件选择函数  
    select_file()  
  
if __name__ == "__main__":  
    create_gui()  