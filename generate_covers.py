import json
import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def get_gradient_color(index):
    palettes = [
        ((2, 0, 36), (9, 9, 121), (0, 212, 255)),     # Ocean Blue
        ((131, 58, 180), (253, 29, 29), (252, 176, 69)), # Sunset
        ((34, 193, 195), (253, 187, 45), (253, 187, 45)), # Tropical
        ((255, 95, 109), (255, 195, 113), (255, 195, 113)), # Peach
        ((44, 62, 80), (52, 152, 219), (41, 128, 185)),   # Night sky
        ((29, 151, 108), (147, 249, 185), (147, 249, 185)), # Emerald
        ((157, 80, 187), (110, 54, 82), (110, 54, 82)),   # Purple
        ((234, 175, 200), (101, 78, 163), (101, 78, 163)), # Lavender
    ]
    return palettes[index % len(palettes)]

def create_gradient(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_text_wrapped(draw, text, font, max_width, start_y, width, fill="white"):
    lines = []
    # If font does not support Chinese, we might just draw a fallback 
    # But Pillow default font is very basic. Let's try to find a system font.
    # We will just write character by character if no spaces.
    words = list(text)
    current_line = ""
    for word in words:
        test_line = current_line + word
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    y = start_y
    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (width - w) / 2
        draw.text((x, y), line, font=font, fill=fill)
        y += h + 10

def main():
    json_path = "/root/1CT-Share/20260804-all-book_reviews/books.json"
    pics_dir = Path("/root/1CT-Share/20260804-all-book_reviews/pics")
    pics_dir.mkdir(exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        books = json.load(f)
        
    width, height = 400, 600
    
    # Try to load a TTF font that supports Chinese. Ubuntu usually has wqy-microhei or similar.
    font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    
    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break
            
    for i, book in enumerate(books):
        folder = book.get('folder')
        if not folder: continue
        cover_path = Path("/root/1CT-Share/20260804-all-book_reviews") / book.get('cover', f"books/{folder}/cover.jpg")
        
        if cover_path.exists():
            continue
            
        c1, c2, c3 = get_gradient_color(i)
        img = create_gradient(width, height, c1, c2)
        draw = ImageDraw.Draw(img)
        
        try:
            if font_path:
                title_font = ImageFont.truetype(font_path, 48)
                author_font = ImageFont.truetype(font_path, 24)
            else:
                title_font = ImageFont.load_default()
                author_font = ImageFont.load_default()
        except:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()

        # Draw Title
        title = book.get('cn_name', 'Unknown')
        draw_text_wrapped(draw, title, title_font, width - 40, 150, width)
        
        # Draw Author
        author = book.get('author', '')
        draw_text_wrapped(draw, author, author_font, width - 40, 450, width, fill=(220, 220, 220))
        
        img.save(cover_path, format="JPEG", quality=85)
        print(f"Generated cover for {title}")

    # Save updated json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
