import os
from pathlib import Path

lists_dir = Path("/root/1CT-Share/20260804-all-book_reviews/lists")
md_dir = Path("/root/1CT-Share/20260804-all-book_reviews/all-md")
md_dir.mkdir(exist_ok=True)

def generate_md():
    headers = ["排名/标识", "出版年份", "中文书名", "外文原名", "中文作者", "外文作者", "专属分类"]
    
    for txt_file in lists_dir.glob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        md_filename = txt_file.with_suffix('.md').name
        
        with open(md_dir / md_filename, 'w', encoding='utf-8') as f:
            f.write(f"# {txt_file.stem}\n\n")
            
            f.write("| " + " | ".join(headers) + " |\n")
            f.write("|" + "|".join(["---"] * len(headers)) + "|\n")
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"): continue
                parts = [p.strip() for p in line.split("--")]
                
                # Ensure parts matches headers length
                while len(parts) < len(headers):
                    parts.append("-")
                parts = parts[:len(headers)]
                
                f.write("| " + " | ".join(parts) + " |\n")

if __name__ == "__main__":
    generate_md()
