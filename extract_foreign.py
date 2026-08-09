import json

with open('/root/1CT-Share/20260804-all-book_reviews/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# list of known chinese authors to exclude
chinese_authors = set([
    '孙立天', '吴晓波', '刘和平', '刘慈欣', '刘擎', '刘瑜', '刘震云', 
    '史铁生', '吴军', '吴念真', '吴承恩', '吴楚材', '当年明月', 
    '曹天元', '曹文轩', '曹禺', '木心', '李娟', '李泽厚', '李硕', 
    '杨本芬', '杨绛', '林奕含', '林崇德', '林海音', '林达', 
    '毛泽东', '江南', '汪曾祺', '沈从文', '海子', '王国维', 
    '王小波', '田余庆', '白先勇', '老舍', '茅海建', '莫言', 
    '萧冬连', '萧红', '蘅塘退士', '费孝通', '迟子建', '都梁', 
    '金庸', '錢穆', '钱穆', '钱锺书', '阿城', '陈凯歌', '陈忠实', 
    '陳浩基', '项飙', '马伯庸', '高行健', '鲁迅', '龙应台',
    '余华', '八月长安', '兰小欢', '妚鹤', '少年儿童出版社', '张爱玲',
])

foreign_books = []
for b in books:
    author = b.get('author', '')
    en_author = b.get('en_author', '')
    cn_name = b.get('cn_name', '')
    if not en_author and author not in chinese_authors:
        foreign_books.append((author, cn_name))

with open('/root/1CT-Share/20260804-all-book_reviews/foreign_books.json', 'w', encoding='utf-8') as f:
    json.dump(foreign_books, f, ensure_ascii=False, indent=2)

print(f"Total foreign books: {len(foreign_books)}")
