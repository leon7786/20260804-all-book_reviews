import json
import os
import shutil
from pathlib import Path

BASE_DIR = Path("/root/1CT-Share/20260804-all-book_reviews")
BOOKS_JSON_PATH = BASE_DIR / "books.json"
BOOKS_DIR = BASE_DIR / "books"
PICS_DIR = BASE_DIR / "pics"

def main():
    with open(BOOKS_JSON_PATH, 'r', encoding='utf-8') as f:
        books = json.load(f)
        
    # 1. Add missing Nobel Prize books
    nobel_file = BASE_DIR / "lists/nobel_prize.txt"
    existing_titles = {b.get('cn_name', '') for b in books}
    existing_en = {b.get('en_name', '') for b in books}
    
    with open(nobel_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = [p.strip() for p in line.split("--")]
            if len(parts) >= 5:
                year, author, title, genre, lang = parts[:5]
                if title not in existing_titles and title not in existing_en:
                    # Create new book entry
                    folder_name = f"{year}_{title}_{author}_{genre}_{lang}".replace(" ", "_").replace("/", "_")
                    folder_path = BOOKS_DIR / folder_name
                    folder_path.mkdir(exist_ok=True)
                    
                    # Create info.txt
                    with open(folder_path / "info.txt", "w", encoding='utf-8') as info_f:
                        info_f.write(f"年代: {year}\n作者: {author}\n中文书名: {title}\n类型: {genre}\n语言: {lang}\nappear: 诺贝尔文学奖\n")
                    
                    # Create page.html (basic)
                    with open(folder_path / "page.html", "w", encoding='utf-8') as page_f:
                        page_f.write(f"<html><body><h1>{title}</h1><p>{author}</p></body></html>")
                        
                    # Add to books list
                    books.append({
                        "cn_name": title,
                        "en_name": title,
                        "author": author,
                        "year": year,
                        "type": genre,
                        "cover": f"books/{folder_name}/cover.jpg",
                        "detail": f"books/{folder_name}/page.html",
                        "folder": folder_name,
                        "appear": ["诺贝尔文学奖"],
                        "is_nobel": True,
                        "douban_rank": 9999
                    })
                    print(f"Added missing Nobel book: {title}")

    # 2. Move covers to book folders
    for book in books:
        folder = book.get('folder', '')
        if not folder:
            continue
            
        old_cover_path = BASE_DIR / book.get('cover', '')
        new_cover_rel = f"books/{folder}/cover.jpg"
        new_cover_abs = BASE_DIR / new_cover_rel
        
        # If the image exists at old location and not new location
        if old_cover_path.exists() and old_cover_path.is_file() and old_cover_path != new_cover_abs:
            shutil.move(str(old_cover_path), str(new_cover_abs))
        elif (PICS_DIR / f"{folder}.jpg").exists() and not new_cover_abs.exists():
            shutil.move(str(PICS_DIR / f"{folder}.jpg"), str(new_cover_abs))
            
        # Also need to move if it's already generated there somehow?
        # Update json field
        book['cover'] = new_cover_rel
        
    # Save books.json
    with open(BOOKS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
        
    print("Reorganization complete.")

if __name__ == "__main__":
    main()
