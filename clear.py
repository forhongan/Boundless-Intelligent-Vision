import os  
  
def clear_all_subfolder_contents(folder_path):  
    # 遍历文件夹中的所有内容，包括子文件夹  
    for root, dirs, files in os.walk(folder_path):  
        for file in files:  
            # 构建文件的完整路径  
            file_path = os.path.join(root, file)  
            try:  
                # 删除文件  
                os.remove(file_path)  
                print(f"已删除文件: {file_path}")  
            except Exception as e:  
                print(f"无法删除文件 {file_path}。错误: {e}")  
  
if __name__ == "__main__":  
    data_folder = './datas'  
    clear_all_subfolder_contents(data_folder)  