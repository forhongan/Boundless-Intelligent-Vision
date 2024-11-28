import os  
  
# 列出某个目录下的所有字体文件  
font_dir = "C:/Windows/Fonts"  # 适用于Windows  
# font_dir = "/Library/Fonts"  # 适用于macOS  
# font_dir = "/usr/share/fonts"  # 适用于Linux  
  
for font_file in os.listdir(font_dir):  
    if font_file.endswith(".ttf"):  
        print(font_file)  