import json
import random

with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

foreign_books = [b for b in books if b.get("is_foreign", False)]
chinese_books = [b for b in books if not b.get("is_foreign", False)]

sampled_foreign = random.sample(foreign_books, min(10, len(foreign_books)))
sampled_chinese = random.sample(chinese_books, min(10, len(chinese_books)))

print("=== FOREIGN BOOKS ===")
for b in sampled_foreign:
    print(f"Title: {b.get('name')}, Author: {b.get('author')}, EN Title: {b.get('en_name')}, EN Author: {b.get('en_author')}")

print("\n=== CHINESE BOOKS ===")
for b in sampled_chinese:
    print(f"Title: {b.get('name')}, Author: {b.get('author')}, EN Title: {b.get('en_name')}, EN Author: {b.get('en_author')}")

