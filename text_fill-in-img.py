import os  
import json  
from PIL import Image, ImageDraw, ImageFont, ImageStat  
  
# 默认字体路径（请根据操作系统调整路径）  
font_path = "C:/Windows/Fonts/SimHei.ttf"  
  
with open('./config/paddlex_config.json', 'r', encoding='utf-8') as file:  
    config_data = json.load(file)  
    biv_result_folder=config_data.get('user_setting').get('output_path')
    img_folder = os.path.dirname(config_data.get('user_setting').get('img_path'))  # 修正原始图像文件夹路径
    #output_path=config_data.get('user_setting').get('output_path')
    ocr_result_folder="datas\ocr_result"
  
# 定义文件夹路径   
result_folder = 'datas/result'  
textfill_folder = 'datas/textfill'   
   
  
# 确保目标文件夹存在  
os.makedirs(textfill_folder, exist_ok=True)  
os.makedirs(biv_result_folder, exist_ok=True)  
  
def merge_json_files_and_fill_image():  
    for filename in os.listdir(ocr_result_folder):  
        if filename.endswith('.json'):  
            ocr_result_path = os.path.join(ocr_result_folder, filename)  
            result_path = os.path.join(result_folder, filename)  
  
            if os.path.exists(result_path):  
                with open(ocr_result_path, 'r', encoding='utf-8') as f:  
                    ocr_data = json.load(f)  
  
                with open(result_path, 'r', encoding='utf-8') as f:  
                    result_data = json.load(f)  
  
                translate_result = result_data.get("translate_result", "")  
                textfill = translate_result.strip('[]').split('] [')  
  
                ocr_data["textfill"] = textfill  
                textfill_path = os.path.join(textfill_folder, filename)  
                with open(textfill_path, 'w', encoding='utf-8') as f:  
                    json.dump(ocr_data, f, ensure_ascii=False, indent=4)  
                print(f"合并完成: {filename}")  
                fill_text_to_image(ocr_data, filename)  
  
def calculate_average_color(image, box):  
    region = image.crop(box)  
    stat = ImageStat.Stat(region)  
    r, g, b = stat.mean[:3]  
    return (r, g, b)  
  
def is_dark_color(color):  
    # 使用简单的亮度公式来判断颜色是否较暗  
    brightness = sum(color) / 3  
    return brightness < 128  
  
def fill_text_to_image(data, filename):  
    image_base_name = filename.replace('.json', '')  
  
    # 尝试打开图像文件，检查不同的扩展名  
    input_image_path_png = os.path.join(img_folder, f"{image_base_name}.png")  
    input_image_path_jpg = os.path.join(img_folder, f"{image_base_name}.jpg")  
  
    if os.path.exists(input_image_path_png):  
        original_image = Image.open(input_image_path_png)  
    elif os.path.exists(input_image_path_jpg):  
        original_image = Image.open(input_image_path_jpg)  
    else:  
        print(f"未找到图像文件: {input_image_path_png} 或 {input_image_path_jpg}")  
        return  
  
    draw = ImageDraw.Draw(original_image)  
  
    font_size = 60  # 初始字体大小  
    min_font_size = 30  # 最小字体大小  
  
    try:  
        font = ImageFont.truetype(font_path, font_size)  
    except IOError:  
        font = ImageFont.load_default()  
        print("Using default font. Please check the font file availability.")  
  
    for poly, text in zip(data["dt_polys"], data["textfill"]):  
        min_x = min(point[0] for point in poly)  
        max_x = max(point[0] for point in poly)  
        min_y = min(point[1] for point in poly)  
        max_y = max(point[1] for point in poly)  
        box_width = max_x - min_x  
        box_height = max_y - min_y  
  
        # 计算新文本框的位置，放在原文本框的2/3下方  
        new_min_y = min_y + box_height * 2 / 3  
  
        while True:  
            bbox = draw.textbbox((0, 0), text, font=font)  
            text_width = bbox[2] - bbox[0]  
            text_height = bbox[3] - bbox[1]  
  
            # 确保文本不会超出图片边界  
            if text_width <= box_width and (new_min_y + text_height) <= original_image.size[1]:  
                break  
  
            font_size -= 1  
            if font_size < min_font_size:  
                font_size = min_font_size  
                break  
  
            font = ImageFont.truetype(font_path, font_size)  
  
        # 左对齐文本  
        text_x = min_x  
        text_y = new_min_y  
  
        # 获取背景颜色并判断文本颜色  
        background_color = calculate_average_color(original_image, (min_x, min_y, max_x, max_y))  
        if is_dark_color(background_color):  
            text_color = (255, 255, 255, 255)  # 白色文本  
            outline_color = (0, 0, 0, 255)    # 黑色描边  
        else:  
            text_color = (0, 0, 0, 255)       # 黑色文本  
            outline_color = (255, 255, 255, 255)  # 白色描边  
  
        # 描边粗细  
        outline_range = 1  
  
        # 添加文本描边  
        for offset in [(outline_range, 0), (-outline_range, 0), (0, outline_range), (0, -outline_range),  
                       (outline_range, outline_range), (-outline_range, -outline_range),  
                       (outline_range, -outline_range), (-outline_range, outline_range)]:  
            draw.text((text_x + offset[0], text_y + offset[1]), text, font=font, fill=outline_color)  
  
        # 绘制文本  
        draw.text((text_x, text_y), text, font=font, fill=text_color)  
  
    output_image_path = os.path.join(biv_result_folder, f"biv_{image_base_name}.png")  
    original_image.save(output_image_path)  
    print(f"图像填充完成: {output_image_path}")  
  
if __name__ == "__main__":  
    merge_json_files_and_fill_image()