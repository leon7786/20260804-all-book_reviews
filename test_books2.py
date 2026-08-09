import json
import random

with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

foreign_books = []
chinese_books = []

for b in books:
    folder = b.get("folder", "")
    # A simple heuristic based on folder name ending
    if folder.endswith("_中文"):
        chinese_books.append(b)
    else:
        # Check if author has [美] etc., or folder ends with other language
        foreign_books.append(b)

# Wait, some might just be "未指定"
# Let's filter more carefully
real_foreign = [b for b in books if b.get('en_name') and b.get('en_name') != b.get('cn_name')]
real_chinese = [b for b in books if b.get('en_name') == b.get('cn_name')]

sampled_foreign = random.sample(real_foreign, min(10, len(real_foreign)))
sampled_chinese = random.sample(real_chinese, min(10, len(real_chinese)))

print("=== FOREIGN BOOKS ===")
for b in sampled_foreign:
    print(f"CN Title: {b.get('cn_name')}\nEN Title: {b.get('en_name')}\nAuthor: {b.get('author')}\nEN Author: {b.get('en_author')}\n---")

print("\n=== CHINESE BOOKS ===")
for b in sampled_chinese:
    print(f"CN Title: {b.get('cn_name')}\nEN Title: {b.get('en_name')}\nAuthor: {b.get('author')}\nEN Author: {b.get('en_author')}\n---")

