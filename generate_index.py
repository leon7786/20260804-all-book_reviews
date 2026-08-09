import os
from pathlib import Path

def generate_index():
    md_dir = Path("/root/1CT-Share/20260804-all-book_reviews/all-md")
    md_files = [f.name for f in md_dir.glob("*.md")]
    
    # We can categorize them manually or just put them in one block.
    # Let's map some known ones
    international = [f for f in md_files if "nobel" in f or "booker" in f or "pulitzer" in f or "hugo" in f or "kafka" in f or "prix_goncourt" in f or "national_book" in f]
    chinese = [f for f in md_files if "maodun" in f or "luxun" in f or "hongloumeng" in f or "china_good_book" in f or "douban" in f]
    others = [f for f in md_files if f not in international and f not in chinese]

    def make_items(files):
        items = []
        for file in files:
            name = file.replace('.md', '').replace('_', ' ').title()
            items.append(f"{{ name: '{name}', file: '{file}' }}")
        return ",\n      ".join(items)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>书殿堂 - 精选书单与资源</title>
<style>
:root {{
  --bg: #fafbfc;
  --surface: #ffffff;
  --border: #e5e7eb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --accent: #3b82f6;
  --accent-light: #dbeafe;
  --success: #10b981;
  --warning: #f59e0b;
  --radius: 12px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'Source Han Sans SC', sans-serif;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  background: var(--bg);
  color: var(--text-primary);
  line-height: 1.6;
}}

/* 顶部导航 */
.navbar {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 2rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.navbar-brand {{
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

.navbar-brand span {{
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.navbar-links {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

/* 新搜索框 */
.search-box {{
  position: relative;
  width: 300px;
  max-width: 100%;
}}

.search-input-wrap {{
  position: relative;
  display: flex;
  align-items: center;
}}

.search-icon {{
  position: absolute;
  left: 0.75rem;
  width: 1rem;
  height: 1rem;
  color: var(--text-muted);
  pointer-events: none;
}}

.search-input {{
  width: 100%;
  height: 38px;
  padding: 0 3rem 0 2.5rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: #ffffff;
  color: var(--text-primary);
  font-size: 0.875rem;
  outline: none;
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
}}

.search-input::placeholder {{
  color: var(--text-muted);
}}

.search-input:focus {{
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.14);
}}

.search-close {{
  position: absolute;
  right: 0.6rem;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
}}

.search-input:not(:placeholder-shown) + .search-close {{
  display: flex;
}}

.search-results {{
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 420px;
  max-height: 520px;
  overflow: hidden;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: var(--shadow-lg);
  display: none;
  z-index: 200;
}}

.search-results.open {{
  display: block;
}}

.search-result-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.78rem;
}}

.search-result-list {{
  max-height: 460px;
  overflow-y: auto;
  padding: 0.5rem;
}}

.search-item {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.55rem;
  border-radius: 10px;
  text-decoration: none;
  color: var(--text-primary);
  transition: background .15s ease;
}}

.search-item:hover {{
  background: #eef4ff;
}}

.search-item img {{
  width: 44px;
  height: 66px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  flex: 0 0 44px;
}}

.search-item-info {{
  min-width: 0;
}}

.search-item-title {{
  font-size: 0.9rem;
  font-weight: 650;
  line-height: 1.25;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

.search-item-meta {{
  margin-top: 0.15rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
}}

.search-highlight {{
  color: #f59e0b;
  font-weight: 700;
  background: rgba(245, 158, 11, 0.12);
  border-radius: 3px;
  padding: 0 1px;
}}

@media (max-width: 640px) {{
  .search-box {{ width: 100%; }}
  .search-results {{ width: calc(100vw - 2rem); right: 0; }}
}}

/* 主布局 */
.layout {{
  display: flex;
  max-width: 1600px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}}

/* 侧边栏 */
.sidebar {{
  width: 260px;
  flex-shrink: 0;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1.5rem 0;
  position: sticky;
  top: 64px;
  height: calc(100vh - 64px);
  overflow-y: auto;
}}

.sidebar::-webkit-scrollbar {{ width: 4px; }}
.sidebar::-webkit-scrollbar-track {{ background: transparent; }}
.sidebar::-webkit-scrollbar-thumb {{ background: #d1d5db; border-radius: 2px; }}

.sidebar-section {{
  margin-bottom: 1.5rem;
}}

.sidebar-title {{
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 0 1.5rem;
  margin-bottom: 0.5rem;
}}

.sidebar-link {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.5rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: var(--transition);
  border-left: 3px solid transparent;
}}

.sidebar-link:hover {{
  background: #f3f4f6;
  color: var(--text-primary);
}}

.sidebar-link.active {{
  background: var(--accent-light);
  color: var(--accent);
  border-left-color: var(--accent);
  font-weight: 600;
}}

/* 主内容区 */
.main {{
  flex: 1;
  min-width: 0;
  padding: 2rem;
}}

/* 游戏卡片网格 - 调整为书籍尺寸 */
.games-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}}

.game-card {{
  background: var(--surface);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
}}

.game-card:hover {{
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent);
}}

.game-cover {{
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  position: relative;
  padding: 0;
  aspect-ratio: 2 / 3;
  overflow: hidden;
}}

.game-cover::after {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-shadow: inset 4px 0 12px rgba(0,0,0,0.15), inset -1px 0 2px rgba(255,255,255,0.3);
  pointer-events: none;
  z-index: 2;
}}

.game-cover img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94), filter 0.5s ease;
}}

.game-card:hover .game-cover img {{
  transform: scale(1.06);
  filter: brightness(1.08);
}}

.game-info {{
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}}

.game-title {{
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}}

.game-subtitle {{
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}}

.game-meta {{
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.25rem;
}}

.tag {{
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  background: #f3f4f6;
  color: var(--text-secondary);
}}

.tag.year {{
  background: #fef3c7;
  color: #92400e;
}}
.tag.type {{
  background: var(--accent-light);
  color: var(--accent);
}}

/* Markdown 内容 */
.md-content {{
  background: var(--surface);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  display: none;
}}

.md-content.active {{
  display: block;
}}

/* 复用原版 MD 样式 */
.md-content h1 {{ font-size: 2rem; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 2px solid var(--border); }}
.md-content h2 {{ font-size: 1.5rem; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }}
.md-content table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.875rem; }}
.md-content th {{ background: #f9fafb; padding: 0.75rem 1rem; text-align: left; border-bottom: 2px solid var(--border); }}
.md-content td {{ padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); color: var(--text-secondary); }}
.md-content tr:hover td {{ background: #f9fafb; }}

@media (max-width: 1024px) {{
  .layout {{ flex-direction: column; }}
  .sidebar {{ width: 100%; position: static; height: auto; border-right: none; border-bottom: 1px solid var(--border); padding: 1rem 0; }}
}}
</style>
</head>
<body>

<nav class="navbar">
  <a href="#" class="navbar-brand" onclick="showGames(); return false;">
    📚 <span>书殿堂</span>
  </a>
  <div class="navbar-links">
    <div class="search-box" id="searchBox">
      <div class="search-input-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" d="m21 21-4.35-4.35M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/></svg>
        <input type="text" id="searchInput" class="search-input" placeholder="搜索书名、作者..." autocomplete="off" />
        <button type="button" class="search-close" aria-label="清空搜索">
          <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
        </button>
      </div>
      <div class="search-results" id="searchResults">
        <div class="search-result-header"><span>搜索结果</span><span id="searchCount"></span></div>
        <div class="search-result-list" id="searchResultList"></div>
      </div>
    </div>
  </div>
</nav>

<div class="layout">
  <aside class="sidebar" id="sidebar"></aside>
  <main class="main">
    <div class="games-grid" id="gamesGrid"></div>
    <div class="md-content" id="mdContent"></div>
  </main>
</div>

<script>
const sidebarConfig = [
  {{
    title: '国际榜单',
    items: [
      {make_items(international)}
    ]
  }},
  {{
    title: '国内榜单',
    items: [
      {make_items(chinese)}
    ]
  }},
  {{
    title: '其他推荐',
    items: [
      {make_items(others)}
    ]
  }}
];

function renderSidebar() {{
  const sidebar = document.getElementById('sidebar');
  let html = '<div class="sidebar-section">';
  html += '<div class="sidebar-title">导航</div>';
  html += '<a href="#" class="sidebar-link active" onclick="showGames(); return false;">📚 全部书籍</a>';
  html += '</div>';
  
  for (const group of sidebarConfig) {{
    html += `<div class="sidebar-section">`;
    if (group.title) html += `<div class="sidebar-title">${{group.title}}</div>`;
    for (const item of group.items) {{
      html += `<a href="#" class="sidebar-link" onclick="loadMd('${{item.file}}', this); return false;">${{item.name}}</a>`;
    }}
    html += `</div>`;
  }}
  sidebar.innerHTML = html;
}}

function showGames() {{
  document.getElementById('gamesGrid').style.display = 'grid';
  document.getElementById('mdContent').classList.remove('active');
  document.querySelectorAll('.sidebar-link').forEach(a => a.classList.remove('active'));
  document.querySelector('.sidebar-link').classList.add('active');
}}

async function loadMd(file, el) {{
  document.getElementById('gamesGrid').style.display = 'none';
  const content = document.getElementById('mdContent');
  content.classList.add('active');
  content.innerHTML = '<p style="text-align:center;color:var(--text-muted);padding:2rem">加载中...</p>';
  
  document.querySelectorAll('.sidebar-link').forEach(a => a.classList.remove('active'));
  if (el) el.classList.add('active');

  try {{
    const resp = await fetch(`all-md/${{file}}`);
    if (!resp.ok) throw new Error(`HTTP ${{resp.status}}`);
    const md = await resp.text();
    content.innerHTML = renderMarkdown(md);
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }} catch (e) {{
    content.innerHTML = `<p style="color:#ef4444;padding:2rem">加载失败: ${{e.message}}</p>`;
  }}
}}

function renderMarkdown(md) {{
  let html = md;
  html = html.replace(/^(\\|.+\\|)\\n(\\|[-:| ]+\\|)\\n((?:\\|.+\\|\\n?)*)/gm, (match, header, sep, body) => {{
    const heads = header.split('|').filter(c => c.trim()).map(c => `<th>${{c.trim()}}</th>`).join('');
    const rows = body.trim().split('\\n').map(row => {{
      const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${{c.trim()}}</td>`).join('');
      return `<tr>${{cells}}</tr>`;
    }}).join('');
    return `<table><thead><tr>${{heads}}</tr></thead><tbody>${{rows}}</tbody></table>`;
  }});
  
  html = html.replace(/^######\\s+(.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\\s+(.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\\s+(.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\\s+(.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\\s+(.+)$/gm, '<h1>$1</h1>');
  
  html = html.replace(/\\n\\n/g, '</p><p>');
  html = '<p>' + html + '</p>';
  html = html.replace(/<p>\\s*<(h[1-6]|table|ul|ol|hr|blockquote)/g, '<$1');
  html = html.replace(/<\\/(h[1-6]|table|ul|ol|hr|blockquote)>\\s*<\\/p>/g, '</$1>');
  
  return html;
}}

function renderBookCard(book) {{
  return `
    <div class="game-card">
      <a href="${{book.detail}}" style="text-decoration:none;color:inherit;display:block">
        <div class="game-cover">
          <img src="${{book.cover}}" alt="${{book.en_name}}" loading="lazy" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'400\\' height=\\'600\\' style=\\'background:%23eee\\'><text x=\\'50%\\' y=\\'50%\\' font-size=\\'24\\' fill=\\'%23999\\' text-anchor=\\'middle\\' dominant-baseline=\\'middle\\'>暂无封面</text></svg>'">
        </div>
      </a>
      <div class="game-info">
        <div class="game-title">${{book.cn_name}}</div>
        <div class="game-subtitle">${{book.author}}</div>
        <div class="game-meta">
          <span class="tag year">${{book.year}}</span>
          <span class="tag type">${{book.type}}</span>
        </div>
      </div>
    </div>
  `;
}}

let allBooks = [];

function renderGames(books) {{
  const grid = document.getElementById('gamesGrid');
  grid.innerHTML = books.map(renderBookCard).join('');
}}

async function loadBooks() {{
  try {{
    const resp = await fetch('books.json');
    allBooks = await resp.json();
    
    // Sort logic: Nobel first, then Douban Rank, then the rest
    allBooks.sort((a, b) => {{
      if (a.is_nobel && !b.is_nobel) return -1;
      if (!a.is_nobel && b.is_nobel) return 1;
      
      const rankA = a.douban_rank || 9999;
      const rankB = b.douban_rank || 9999;
      
      return rankA - rankB;
    }});

    renderGames(allBooks);
  }} catch (e) {{
    console.error('加载书籍数据失败:', e);
  }}
}}

(function initSearch() {{
  const input = document.getElementById('searchInput');
  const closeBtn = document.querySelector('#searchBox .search-close');
  const resultsBox = document.getElementById('searchResults');
  const resultList = document.getElementById('searchResultList');
  const countEl = document.getElementById('searchCount');
  let timer = null;

  function escapeHtml(str) {{ return String(str).replace(/[&<>"]/g, (c) => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }}[c])); }}
  function highlightText(text, query) {{
    if (!query) return escapeHtml(text);
    const safe = escapeHtml(text);
    const regex = new RegExp(`(${{query.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')}})`, 'gi');
    return safe.replace(regex, '<span class="search-highlight">$1</span>');
  }}

  function search(query) {{
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => runSearch(query.trim()), 60);
  }}

  function runSearch(query) {{
    const list = document.createElement('div');
    list.style.cssText = 'padding:0.5rem;';

    if (!query || allBooks.length === 0) {{
      list.innerHTML = '<div style="padding:1.5rem;text-align:center;color:#9ca3af">开始输入搜索书籍…</div>';
      resultList.innerHTML = '';
      resultList.appendChild(list);
      countEl.textContent = '';
      if (query) resultsBox.classList.add('open');
      else resultsBox.classList.remove('open');
      return;
    }}

    const q = query.toLowerCase();
    const matched = allBooks.filter(g => {{
      const cn = (g.cn_name || '').toLowerCase();
      const author = (g.author || '').toLowerCase();
      return cn.includes(q) || author.includes(q);
    }}).slice(0, 12);

    if (matched.length === 0) {{
      list.innerHTML = '<div style="padding:1.5rem;text-align:center;color:#9ca3af">没有找到书籍</div>';
      resultList.innerHTML = '';
      resultList.appendChild(list);
      countEl.textContent = '0 项';
      resultsBox.classList.add('open');
      return;
    }}

    countEl.textContent = `${{matched.length}} 项`;
    resultList.innerHTML = '';
    resultList.appendChild(list);

    matched.forEach(g => {{
      const a = document.createElement('a');
      a.className = 'search-item';
      a.href = g.detail || '#';
      const titleText = g.cn_name || '';
      const metaText = (g.author || '') + (g.year ? ' · ' + g.year : '');

      a.innerHTML = `
        <img src="${{escapeHtml(g.cover || '')}}" alt="" loading="lazy">
        <div class="search-item-info">
          <div class="search-item-title">${{highlightText(titleText, query)}}</div>
          <div class="search-item-meta">${{highlightText(metaText, query)}}</div>
        </div>
      `;
      list.appendChild(a);
    }});
    resultsBox.classList.add('open');
  }}

  input.addEventListener('input', () => search(input.value));
  if (closeBtn) {{
    closeBtn.addEventListener('click', () => {{
      input.value = '';
      resultsBox.classList.remove('open');
      countEl.textContent = '';
      input.focus();
    }});
  }}
  input.addEventListener('blur', () => {{
    setTimeout(() => {{ if (!input.matches(':focus')) resultsBox.classList.remove('open'); }}, 150);
  }});
  input.addEventListener('focus', () => {{
    if (input.value.trim()) resultsBox.classList.add('open');
  }});
}})();

renderSidebar();
loadBooks();
</script>
</body>
</html>
"""
    with open('/root/1CT-Share/20260804-all-book_reviews/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Generated index.html")

if __name__ == "__main__":
    generate_index()
