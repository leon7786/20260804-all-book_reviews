#!/usr/bin/env python3
import os
import json
from pathlib import Path

BOOKS_DIR = Path("/root/1CT-Share/20260804-all-book_reviews/books")

books = []
for folder in BOOKS_DIR.iterdir():
    if folder.is_dir():
        info_file = folder / "info.txt"
        if info_file.exists():
            data = {}
            with open(info_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        key, val = line.strip().split(':', 1)
                        data[key.strip()] = val.strip()
            
            # The gaming json uses cn_name, en_name, year, cover, detail, tags, etc.
            # Let's map book info to a similar structure.
            chinese = data.get('中文书名', folder.name)
            english = data.get('外文书名', '')
            author = data.get('作者', '未知')
            book_type = data.get('类型', '未知')
            year = data.get('年代', '未知')
            cover_path = f"pics/{folder.name}.jpg" # Just a placeholder or we can use a generic cover if doesn't exist
            
            books.append({
                "cn_name": chinese,
                "en_name": english,
                "author": author,
                "year": year,
                "type": book_type,
                "cover": cover_path, # We will handle cover in CSS or JS if missing
                "detail": f"books/{folder.name}/page.html",
                "folder": folder.name,
                "appear": data.get("appear", [])
            })

with open('/root/1CT-Share/20260804-all-book_reviews/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f"Generated books.json with {len(books)} books")
