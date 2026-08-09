import json
from pathlib import Path

books_json_path = Path("/root/1CT-Share/20260804-all-book_reviews/books.json")
with open(books_json_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Parse Nobel Prize
nobel_authors = set()
nobel_books = set()
with open("/root/1CT-Share/20260804-all-book_reviews/lists/nobel_prize.txt", 'r', encoding='utf-8') as f:
    for line in f:
        parts = [p.strip() for p in line.split("--")]
        if len(parts) >= 3:
            nobel_authors.add(parts[1])
            nobel_books.add(parts[2])

# Parse Douban Top 250
douban_ranks = {}
with open("/root/1CT-Share/20260804-all-book_reviews/lists/douban_top250.txt", 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        parts = [p.strip() for p in line.split("--")]
        if len(parts) >= 3:
            try:
                rank = int(parts[0])
                title = parts[1]
                douban_ranks[title] = rank
            except:
                pass

# Update books
for book in books:
    cn_name = book.get("cn_name", "")
    en_name = book.get("en_name", "")
    author = book.get("author", "")
    
    # Check Nobel
    is_nobel = False
    for na in nobel_authors:
        if na in author or author in na:
            is_nobel = True
            break
    if not is_nobel:
        for nb in nobel_books:
            if nb == cn_name or nb == en_name:
                is_nobel = True
                break
    
    book['is_nobel'] = is_nobel
    
    # Check Douban
    book['douban_rank'] = 9999
    if cn_name in douban_ranks:
        book['douban_rank'] = douban_ranks[cn_name]
    else:
        # Try substring match just in case
        for d_title, rank in douban_ranks.items():
            if d_title in cn_name or cn_name in d_title:
                book['douban_rank'] = rank
                break

with open(books_json_path, 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print("Updated books.json with is_nobel and douban_rank")
