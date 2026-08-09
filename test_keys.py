import json

with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

print(list(books[0].keys()))
print(books[0])
