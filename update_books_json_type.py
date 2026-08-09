import json
from pathlib import Path

lists_dir = Path("/root/1CT-Share/20260804-all-book_reviews/lists")
books_json_path = Path("/root/1CT-Share/20260804-all-book_reviews/books.json")

# Map of Title -> New Category
title_to_cat = {}

for txt_file in lists_dir.glob("*.txt"):
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = [p.strip() for p in line.split("--")]
            if len(parts) >= 7:
                # Format: Prefix -- Year -- Title -- En Title -- Author -- En Author -- Genre
                title = parts[2]
                cat = parts[6]
                if title and title != "-":
                    title_to_cat[title] = cat

with open(books_json_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

for book in books:
    cn_name = book.get('cn_name', '')
    en_name = book.get('en_name', '')
    
    if cn_name in title_to_cat:
        book['type'] = title_to_cat[cn_name]
    elif en_name in title_to_cat:
        book['type'] = title_to_cat[en_name]
    else:
        # Check subset or super set if necessary
        # Default to Literature if totally unknown, but it should be mapped
        found = False
        for k, v in title_to_cat.items():
            if k in cn_name or cn_name in k:
                book['type'] = v
                found = True
                break
        if not found:
            book['type'] = "8. 文学"

with open(books_json_path, 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print("Updated books.json types.")
