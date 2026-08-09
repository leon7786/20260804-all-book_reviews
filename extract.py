import json
import re

with open('/root/1CT-Share/20260804-all-book_reviews/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

missing = set()
for b in books:
    author = b.get('author', '')
    en_author = b.get('en_author', '')
    cn_name = b.get('cn_name', '')
    if not en_author:
        missing.add((author, cn_name))

print(f"Total missing: {len(missing)}")
for a, t in sorted(list(missing)):
    print(f"{a} | {t}")
