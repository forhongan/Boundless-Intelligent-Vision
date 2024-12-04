import os  
import json  
from PIL import Image, ImageDraw, ImageFont  
  
# 默认字体路径（请根据操作系统调整路径）  
font_path = "C:/Windows/Fonts/SimHei.ttf"  
  
# 定义文件夹路径  
ocr_result_folder = 'datas/ocr_result'  
result_folder = 'datas/result'  
textfill_folder = 'datas/textfill'  
biv_result_folder = 'datas/biv_result'  
  
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
  
def fill_text_to_image(data, filename):  
    input_image_path = data["input_path"]  
    original_image = Image.open(input_image_path)  
    image_size = original_image.size  
  
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))  
    draw = ImageDraw.Draw(image)  
  
    font_size = 20  
    min_font_size = 10  
  
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
            font = ImageFont.truetype(font_path, font_size)  
  
        # 左对齐文本  
        text_x = min_x  
        text_y = min_y + (box_height - text_height) / 2  
  
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))  
  
    output_image_path = os.path.join(biv_result_folder, f"filled_{filename.replace('.json', '.png')}")  
    image.save(output_image_path)  
    print(f"图像填充完成: {output_image_path}")  
  
if __name__ == "__main__":  
    merge_json_files_and_fill_image()  