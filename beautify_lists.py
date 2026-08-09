import os
from pathlib import Path
import re

category_mapping = {
    "哲学": "1. 哲学与心理学", "心理": "1. 哲学与心理学", "思想": "1. 哲学与心理学", "逻辑": "1. 哲学与心理学", "伦理": "1. 哲学与心理学",
    "宗教": "2. 宗教", "神话": "2. 宗教", "神学": "2. 宗教", "佛教": "2. 宗教", "基督教": "2. 宗教", "圣经": "2. 宗教",
    "社会": "3. 社会科学", "经济": "3. 社会科学", "政治": "3. 社会科学", "法律": "3. 社会科学", "教育": "3. 社会科学", "管理": "3. 社会科学", "人类": "3. 社会科学", "商业": "3. 社会科学", "文化": "3. 社会科学", "金融": "3. 社会科学", "女性": "3. 社会科学",
    "语言": "4. 语言", "词典": "4. 语言", "字典": "4. 语言",
    "科学": "5. 自然科学与数学", "数学": "5. 自然科学与数学", "物理": "5. 自然科学与数学", "化学": "5. 自然科学与数学", "生物": "5. 自然科学与数学", "天文": "5. 自然科学与数学", "科普": "5. 自然科学与数学",
    "技术": "6. 技术", "计算机": "6. 技术", "工程": "6. 技术", "医学": "6. 技术", "互联网": "6. 技术", "建筑": "6. 技术", "制造": "6. 技术",
    "艺术": "7. 艺术与休闲", "休闲": "7. 艺术与休闲", "音乐": "7. 艺术与休闲", "摄影": "7. 艺术与休闲", "电影": "7. 艺术与休闲", "美术": "7. 艺术与休闲", "体育": "7. 艺术与休闲", "游戏": "7. 艺术与休闲", "画": "7. 艺术与休闲",
    "历史": "9. 历史与地理", "地理": "9. 历史与地理", "传记": "9. 历史与地理", "回忆录": "9. 历史与地理", "游记": "9. 历史与地理", "纪实": "9. 历史与地理", "史": "9. 历史与地理",
    "文学": "8. 文学", "小说": "8. 文学", "诗": "8. 文学", "散文": "8. 文学", "戏剧": "8. 文学", "随笔": "8. 文学", "童话": "8. 文学", "科幻": "8. 文学", "奇幻": "8. 文学", "悬疑": "8. 文学", "名著": "8. 文学", "推理": "8. 文学", "耽美": "8. 文学", "武侠": "8. 文学", "网文": "8. 文学"
}

def classify(genre_str):
    if not genre_str:
        return "8. 文学"
    for k, v in category_mapping.items():
        if k in genre_str:
            return v
    return "8. 文学"

lists_dir = Path("/root/1CT-Share/20260804-all-book_reviews/lists")

for txt_file in lists_dir.glob("*.txt"):
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    # Try to determine file structure based on file name
    # Default is: douban-like (Rank - Title - Author - OrigTitle - Year - Genre - Lang)
    is_nobel = 'nobel' in txt_file.stem
    
    count = 1
    for line in lines:
        line_s = line.strip()
        if not line_s or line_s.startswith("#") or line_s.startswith("=") or line_s.startswith("评分：") or line_s.startswith("Goodreads") or line_s.startswith("数据来源") or line_s.startswith("验证来源") or line_s.startswith("-") or line_s.startswith("说明：") or line_s.startswith("包含") or "排名 -- " in line_s:
            # new_lines.append(line_s) # Skip non-book lines
            continue
            
        parts = [p.strip() for p in line_s.split("--")]
        if len(parts) < 3:
            continue
            
        rank = f"TOP{count}"
        year = "-"
        title = "-"
        en_title = "-"
        author = "-"
        en_author = "-"
        genre_str = ""
        
        if is_nobel:
            # 2025 -- 拉斯洛·克拉斯纳霍尔凯 -- Sátántangó -- 小说 -- 匈牙利语
            year = parts[0]
            author = parts[1]
            title = parts[2]
            genre_str = parts[3] if len(parts) > 3 else "文学"
            rank = "WINNER"
        elif parts[0].isdigit() and int(parts[0]) > 1000:
            # maodun, luxun (Year - Title - Author - ...)
            year = parts[0]
            title = parts[1]
            author = parts[2]
            en_title = parts[3] if len(parts) > 3 else "-"
            genre_str = parts[4] if len(parts) > 4 else "文学"
            rank = "WINNER"
        else:
            # douban top 250 (Rank - Title - Author - Orig - Year - Genre - Lang)
            rank = f"TOP{parts[0]}" if parts[0].isdigit() else f"TOP{count}"
            title = parts[1]
            author = parts[2] if len(parts) > 2 else "-"
            en_title = parts[3] if len(parts) > 3 else "-"
            if en_title == title:
                en_title = "-"
            year = parts[4] if len(parts) > 4 else "-"
            genre_str = parts[5] if len(parts) > 5 else "文学"
            
        cat = classify(genre_str)
        
        # En Author extraction from author field if possible
        # Some authors have English name in brackets or mixed: "[美] Harper Lee / 哈珀·李"
        # We'll just leave en_author as "-" for simplicity, unless it's easy to split
        # Formatting: Prefix -- Year -- Title -- En Title -- Author -- En Author -- Genre
        
        new_line = f"{rank} -- {year} -- {title} -- {en_title} -- {author} -- {en_author} -- {cat}"
        new_lines.append(new_line)
        count += 1
        
    with open(txt_file, 'w', encoding='utf-8') as f:
        for nl in new_lines:
            f.write(nl + "\n")

print("Lists beautified and re-categorized.")
