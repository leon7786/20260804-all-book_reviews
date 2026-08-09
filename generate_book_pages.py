#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成书殿堂 HTML 页面
参考 awesome-gaming 的 generate_pages.py 风格
"""

import os
import json
from pathlib import Path

BOOKS_DIR = Path("/root/1CT-Share/20260804-all-book_reviews/books")
OUTPUT_DIR = Path("/root/1CT-Share/20260804-all-book_reviews/books")

def extract_book_info(folder_path):
    """从文件夹提取书本信息"""
    info_file = folder_path / "info.txt"
    if not info_file.exists():
        return None
    
    with open(info_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.strip().split(':', 1)
            data[key.strip()] = value.strip()
    
    # 构建显示名称
    chinese = data.get('中文书名', folder_path.name)
    english = data.get('外文书名', chinese)
    author = data.get('作者', '未知')
    book_type = data.get('类型', '未知')
    year = data.get('年代', '未知')
    
    return {
        'chinese': chinese,
        'english': english,
        'author': author,
        'type': book_type,
        'year': year,
        'folder': folder_path.name
    }

def generate_book_page(book_info):
    """生成单个书本 HTML"""
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{book_info['chinese']} - {book_info['year']}</title>
<style>
/* 复用 gaming 的 steam-css */
@import "steam-css/main.css";
/* 或者直接嵌入简单样式 */
body {{ font-family: system-ui, sans-serif; background: #fafbfc; padding: 2rem; max-width: 800px; margin: 0 auto; }}
.book-cover-large {{ height: 400px; background: #f3f4f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 8rem; margin-bottom: 2rem; }}
</style>
</head>
<body>
<div class="book-cover-large">📖</div>
<h1>{book_info['chinese']}</h1>
<p>作者：{book_info['author']}</p>
<p>类型：{book_info['type']}</p>
<p>年份：{book_info['year']}</p>
<div>出现在榜单：{", ".join(book_info.get('appear', []))}</div>
</body>
</html>
'''
    return html

# 主流程
print("开始生成书本页面...")

books = []
for folder in BOOKS_DIR.iterdir():
    if folder.is_dir():
        info = extract_book_info(folder)
        if info:
            books.append(info)
            # 生成页面
            page_html = generate_book_page(info)
            output_file = OUTPUT_DIR / f"{info['folder']}/page.html"
            output_file.write_text(page_html, encoding='utf-8')
            print(f"✓ 生成: {info['chinese']}")

print(f"\n共生成 {len(books)} 本书页面")
