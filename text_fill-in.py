import json  
from PIL import Image, ImageDraw, ImageFont  
font_path = "C:/Windows/Fonts/SimHei.ttf"
# 从JSON文件中读取数据  
def load_data_from_json(filepath):  
    with open(filepath, 'r', encoding='utf-8') as file:  
        data = json.load(file)  
    return data  
  
# 加载数据  
data = load_data_from_json('./datas/ocr_result/test1.json')  
  
# 从指定路径加载原始图片以获取其大小  
input_image_path = data["input_path"]  
original_image = Image.open(input_image_path)  
image_size = original_image.size  
  
# 创建一个透明背景的空白图片  
image = Image.new("RGBA", image_size, (255, 255, 255, 0))  
draw = ImageDraw.Draw(image)  
  
# 加载字体，设定初始字体大小  
font_size = 20  
min_font_size = 10  
try:  
    font = ImageFont.truetype(font_path, font_size)  
except IOError:  
    font = ImageFont.load_default()  
    print("Using default font. Please check the font file availability.")
  
# 绘制文本  
for poly, text in zip(data["dt_polys"], data["rec_text"]):  
    # 计算文本框的宽度和高度  
    min_x = min(point[0] for point in poly)  
    max_x = max(point[0] for point in poly)  
    min_y = min(point[1] for point in poly)  
    max_y = max(point[1] for point in poly)  
    box_width = max_x - min_x  
    box_height = max_y - min_y  
  
    # 自动调整字体大小以适应文本框  
    while True:  
        bbox = draw.textbbox((0, 0), text, font=font)  
        text_width = bbox[2] - bbox[0]  
        text_height = bbox[3] - bbox[1]  
        if text_width <= box_width and text_height <= box_height:  
            break  
        font_size -= 1  
        if font_size < min_font_size:  
            font_size = min_font_size  
            break  
        font = ImageFont.truetype("arial.ttf", font_size)  
  
    # 计算文本位置  
    text_x = min_x + (box_width - text_width) / 2  
    text_y = min_y + (box_height - text_height) / 2  
  
    # 绘制文本，颜色设置为白色  
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))  
  
# 保存图片  
image.save("output.png")  