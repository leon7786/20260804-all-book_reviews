import json
import glob
import os

with open('/root/1CT-Share/20260804-all-book_reviews/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

exact_match = {}
title_match = {}

for b in books:
    cn = b.get('cn_name', '').strip()
    en = b.get('en_name', '').strip()
    author = b.get('author', '').strip()
    
    if cn:
        exact_match[(cn, author)] = b
        title_match.setdefault(cn, []).append(b)
    if en:
        exact_match[(en, author)] = b
        title_match.setdefault(en, []).append(b)

md_dir = '/root/1CT-Share/20260804-all-book_reviews/all-md/'
md_files = glob.glob(os.path.join(md_dir, '*.md'))
updated_count = 0

for md_file in md_files:
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if line.strip().startswith('|'):
            cols = [c.strip() for c in line.split('|')]
            if '排名/标识' in line or '---' in line or len(cols) < 9:
                new_lines.append(line)
                continue
            
            title = cols[3]
            author = cols[5]
            
            match = None
            if (title, author) in exact_match:
                match = exact_match[(title, author)]
            elif title in title_match and len(title_match[title]) == 1:
                match = title_match[title][0]
                
            if match:
                cn_name = match.get('cn_name', '')
                en_name = match.get('en_name', '')
                if not en_name or en_name == cn_name:
                    en_name = '-'
                    
                en_author = match.get('en_author', '')
                if not en_author:
                    en_author = '-'
                    
                book_type = match.get('type', '')
                
                cols[3] = cn_name
                cols[4] = en_name
                cols[6] = en_author
                cols[7] = book_type
                
                new_line = '| ' + ' | '.join(cols[1:-1]) + ' |\n'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(md_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    updated_count += 1

print(f"Sync complete. Processed {updated_count} files.")
