import json
import os
import glob
import re

mapping = {
  "天际唯一的飞机：9/11口述历史": ("The Only Plane in the Sky: An Oral History of 9/11", "Garrett M. Graff"),
  "庞金·塞尔万全集": ("Ponniyin Selvan", "Kalki Krishnamurthy"),
  "海贼王（第41卷）": ("One Piece (Vol. 41)", "Eiichiro Oda"),
  "鬼灭之刃（第23卷）": ("Demon Slayer (Vol. 23)", "Koyoharu Gotouge"),
  "魔戒（广播剧版，双塔）": ("The Lord of the Rings (Radio Dramatization, The Two Towers)", "Brian Sibley"),
  "进击的巨人（第20卷）": ("Attack on Titan (Vol. 20)", "Hajime Isayama"),
  "钢之炼金术师（第23卷）": ("Fullmetal Alchemist (Vol. 23)", "Hiromu Arakawa"),
  "电锯人（第9卷）": ("Chainsaw Man (Vol. 9)", "Tatsuki Fujimoto"),
  "懒惰的周日卡尔文与霍布斯": ("The Lazy Sunday Book (Calvin and Hobbes)", "Bill Watterson"),
  "海贼王（第38卷）": ("One Piece (Vol. 38)", "Eiichiro Oda"),
  "药剂师日记（第6卷）": ("The Apothecary Diaries (Vol. 6)", "Nekokurage"),
  "阿莎塔：自传": ("Assata: An Autobiography", "Assata Shakur"),
  "海在诉说他的名字": ("Laut Bercerita", "Leila S. Chudori"),
  "原始猎人9（原始猎人，第9部）": ("The Primal Hunter 9", "Zogarth"),
  "火影忍者（第43卷）": ("Naruto (Vol. 43)", "Masashi Kishimoto"),
  "我的英雄学院（第5卷）": ("My Hero Academia (Vol. 5)", "Kohei Horikoshi"),
  "未完成的爱情故事": ("An Unfinished Love Story", "Doris Kearns Goodwin"),
  "冒险地带（第2卷）": ("The Adventure Zone (Vol. 2)", "Clint McElroy"),
  "睡魔（第9卷）：仁慈者": ("The Sandman (Vol. 9)", "Neil Gaiman"),
  "浦泽直树的怪物（第1卷）": ("Monster (Vol. 1)", "Naoki Urasawa"),
  "选择：拥抱可能性": ("The Choice: Embrace the Possible", "Edith Eger"),
  "睡魔（第4卷）：雾之季": ("The Sandman (Vol. 4)", "Neil Gaiman"),
  "心跳（第1卷）": ("Heartstopper (Vol. 1)", "Alice Oseman"),
  "艾玛·M·狮子未选日记（第6卷）": ("The Unselected Journals of Emma M. Lion", "Beth Brower"),
  "解绑：我的解放故事与Me Too运动的诞生": ("Unbound: My Story of Liberation", "Tarana Burke"),
  "奥斯维辛": ("Auschwitz: A New History", "Laurence Rees"),
  "白夜行": ("Journey Under the Midnight Sun", "Keigo Higashino"),
  "万历十五年": ("1587, A Year of No Significance", "Ray Huang"),
  "厌女": ("Misogyny", "Chizuko Ueno"),
  "流俗地": ("Bumi Manusia", "Li Zishu"),
  "明亮的夜晚": ("Shoko's Smile", "Choi Eun-young"),
  "始于极限": ("Starting from the Limit", "Chizuko Ueno"),
  "窗边的小豆豆": ("Totto-chan", "Tetsuko Kuroyanagi"),
  "桶川跟踪狂杀人事件": ("The Stalker Murder in Okegawa", "Kiyoshi Shimizu"),
  "克莱因壶": ("Klein Bottle", "Futari Okajima"),
  "强风吹拂": ("Run with the Wind", "Shion Miura"),
  "金色梦乡": ("Golden Slumber", "Kotaro Isaka"),
  "海的女儿": ("The Little Mermaid", "Hans Christian Andersen"),
  "鹿川有许多粪": ("There is A Lot of Shit in Luchuan", "Lee Chang-dong"),
  "足利女童连续失踪事件": ("Ashikaga Girls Disappearance Case", "Kiyoshi Shimizu"),
  "雕刻时光": ("Sculpting in Time", "Andrei Tarkovsky"),
  "父权制与资本主义": ("Patriarchy and Capitalism", "Chizuko Ueno"),
  "情书": ("Love Letter", "Shunji Iwai"),
  "从零开始的女性主义": ("Feminism from Zero", "Chizuko Ueno"),
  "二手时间": ("Secondhand Time", "Svetlana Alexievich"),
  "时间的秩序": ("The Order of Time", "Carlo Rovelli"),
  "解忧杂货店": ("The Miracles of the Namiya General Store", "Keigo Higashino"),
  "危险中的好奇（危险家族，第3部）": ("Curiosity in Danger", "India Karter"),
  "失去控制": ("Out of Control", "Ladii Nesha"),
  "皇帝的刺客（图拉真，第1部）": ("The Emperor's Assassin", "Santiago Posteguillo"),
  "迷雾之子三部曲套装": ("Mistborn Trilogy Boxed Set", "Brandon Sanderson"),
  "迷失孩子的故事（那不勒斯四部曲，第4部）": ("The Story of the Lost Child", "Elena Ferrante"),
  "撒旦探戈": ("Satantango", "László Krasznahorkai"),
  "素食者": ("The Vegetarian", "Han Kang"),
  "有人将至": ("Someone Is Going to Come", "Jon Fosse"),
  "一个女人的故事": ("A Woman's Story", "Annie Ernaux"),
  "天堂": ("Paradise", "Abdulrazak Gurnah"),
  "野鸢尾": ("The Wild Iris", "Louise Glück"),
  "偷水果的姑娘": ("The Fruit Thief", "Peter Handke"),
  "太古和其他的时间": ("Primeval and Other Times", "Olga Tokarczuk"),
  "答案在风中飘荡": ("Blowin' in the Wind", "Bob Dylan"),
  "暗店街": ("Missing Person", "Patrick Modiano"),
  "逃离": ("Runaway", "Alice Munro"),
  "在宇宙中": ("In the Universe", "Tomas Tranströmer"),
  "城市与狗": ("The Time of the Hero", "Mario Vargas Llosa"),
  "心兽": ("The Heart Is a Lonely Hunter", "Herta Müller"),
  "寻金者": ("The Prospector", "J. M. G. Le Clézio"),
  "金色笔记": ("The Golden Notebook", "Doris Lessing"),
  "我的名字叫红": ("My Name Is Red", "Orhan Pamuk"),
  "生日派对": ("The Birthday Party", "Harold Pinter"),
  "钢琴教师": ("The Piano Teacher", "Elfriede Jelinek"),
  "耻": ("Disgrace", "J. M. Coetzee"),
  "无命运的人生": ("Fatelessness", "Imre Kertész"),
  "毕斯沃斯先生的房子": ("A House for Mr Biswas", "V. S. Naipaul"),
  "铁皮鼓": ("The Tin Drum", "Günter Grass"),
  "耶稣基督福音": ("The Gospel According to Jesus Christ", "José Saramago"),
  "一个无政府主义者的意外死亡": ("Accidental Death of an Anarchist", "Dario Fo"),
  "桥上的人们": ("People on a Bridge", "Wisława Szymborska"),
  "一个自然主义者的死亡": ("Death of a Naturalist", "Seamus Heaney"),
  "個人的な体験": ("A Personal Matter", "Kenzaburō Ōe"),
  "宠儿": ("Beloved", "Toni Morrison"),
  "奥麦罗斯": ("Omeros", "Derek Walcott"),
  "伯格的女儿": ("Burger's Daughter", "Nadine Gordimer"),
  "孤独的迷宫": ("The Labyrinth of Solitude", "Octavio Paz"),
  "帕斯夸尔·杜阿尔特一家": ("The Family of Pascual Duarte", "Camilo José Cela"),
  "我们街区的孩子们": ("Children of the Alley", "Naguib Mahfouz"),
  "词语的一部分": ("A Part of Speech", "Joseph Brodsky"),
  "狮子与宝石": ("The Lion and the Jewel", "Wole Soyinka"),
  "弗兰德公路": ("The Flanders Road", "Claude Simon"),
  "鼠疫纪念柱": ("The Plague Column", "Jaroslav Seifert"),
  "蝇王": ("Lord of the Flies", "William Golding"),
  "迷惘": ("Auto-da-Fé", "Elias Canetti"),
  "拯救": ("The Rescue", "Czesław Miłosz"),
  "赞美颂": ("The Axion Esti", "Odysseas Elytis"),
  "莫斯卡特一家": ("The Family Moskat", "Isaac Bashevis Singer"),
  "天堂的影子": ("Shadow of Paradise", "Vicente Aleixandre"),
  "洪堡的礼物": ("Humboldt's Gift", "Saul Bellow"),
  "乌贼骨": ("Cuttlefish Bones", "Eugenio Montale"),
  "重返伊萨卡": ("Return to Ithaca", "Eyvind Johnson"),
  "阿尼亚拉号": ("Aniara", "Harry Martinson"),
  "沃斯": ("Voss", "Patrick White"),
  "丧失名誉的卡塔琳娜·勃罗姆": ("The Lost Honour of Katharina Blum", "Heinrich Böll"),
  "二十首情诗和一首绝望的歌": ("Twenty Love Poems and a Song of Despair", "Pablo Neruda"),
  "伊万·杰尼索维奇的一天": ("One Day in the Life of Ivan Denisovich", "Aleksandr Solzhenitsyn"),
  "等待戈多": ("Waiting for Godot", "Samuel Beckett"),
  "雪国": ("Snow Country", "Yasunari Kawabata"),
  "总统先生": ("El Señor Presidente", "Miguel Ángel Asturias"),
  "哦，烟囱": ("O the Chimneys", "Nelly Sachs"),
  "婚盖": ("The Bridal Canopy", "Shmuel Yosef Agnon"),
  "静静的顿河": ("And Quiet Flows the Don", "Mikhail Sholokhov"),
  "恶心": ("Nausea", "Jean-Paul Sartre"),
  "转折": ("Turning Point", "Giorgos Seferis"),
  "愤怒的葡萄": ("The Grapes of Wrath", "John Steinbeck"),
  "德里纳河上的桥": ("The Bridge on the Drina", "Ivo Andrić"),
  "远征": ("Anabasis", "Saint-John Perse"),
  "忽然黄昏": ("And Suddenly It's Evening", "Salvatore Quasimodo"),
  "日瓦戈医生": ("Doctor Zhivago", "Boris Pasternak"),
  "小银和我": ("Platero and I", "Juan Ramón Jiménez"),
  "独立的人们": ("Independent People", "Halldór Laxness"),
  "老人与海": ("The Old Man and the Sea", "Ernest Hemingway"),
  "第二次世界大战回忆录": ("The Second World War", "Winston Churchill"),
  "毒蛇结": ("Vipers' Tangle", "François Mauriac"),
  "巴拉巴": ("Barabbas", "Pär Lagerkvist"),
  "西方哲学史": ("A History of Western Philosophy", "Bertrand Russell"),
  "喧哗与骚动": ("The Sound and the Fury", "William Faulkner"),
  "四个四重奏": ("Four Quartets", "T. S. Eliot"),
  "伪币制造者": ("The Counterfeiters", "André Gide"),
  "玻璃球游戏": ("The Glass Bead Game", "Hermann Hesse"),
  "绝望": ("Despair", "Gabriela Mistral"),
  "漫长的旅程": ("The Long Journey", "Johannes V. Jensen"),
  "虔诚的农民": ("Meek Heritage", "Frans Eemil Sillanpää"),
  "大地": ("The Good Earth", "Pearl S. Buck"),
  "蒂博一家": ("The Thibaults", "Roger Martin du Gard"),
  "长夜漫漫路迢迢": ("Long Day's Journey into Night", "Eugene O'Neill"),
  "六个寻找剧作家的角色": ("Six Characters in Search of an Author", "Luigi Pirandello"),
  "米佳的爱情": ("Mitya's Love", "Ivan Bunin"),
  "福尔赛世家": ("The Forsyte Saga", "John Galsworthy"),
  "弗里多林的乐园": ("Fridolin's Pleasure Garden", "Erik Axel Karlfeldt"),
  "大街": ("Main Street", "Sinclair Lewis"),
  "魔山": ("The Magic Mountain", "Thomas Mann"),
  "劳伦斯之女克里斯汀": ("Kristin Lavransdatter", "Sigrid Undset"),
  "创造进化论": ("Creative Evolution", "Henri Bergson"),
  "风中芦苇": ("Reeds in the Wind", "Grazia Deledda"),
  "卖花女": ("Pygmalion", "George Bernard Shaw"),
  "农民": ("The Peasants", "Władysław Reymont"),
  "塔": ("The Tower", "W. B. Yeats"),
  "欢乐而自信的城市": ("The Joyous and Confident City", "Jacinto Benavente"),
  "诸神渴了": ("The Gods Will Have Blood", "Anatole France"),
  "大地硕果": ("Growth of the Soil", "Knut Hamsun"),
  "奥林匹亚的春天": ("Olympian Spring", "Carl Spitteler"),
  "敏娜": ("Minna", "Karl Adolph Gjellerup"),
  "幸运的彼尔": ("Lucky Per", "Henrik Pontoppidan"),
  "约翰·克利斯朵夫": ("Jean-Christophe", "Romain Rolland"),
  "吉檀迦利": ("Gitanjali", "Rabindranath Tagore"),
  "织工": ("The Weavers", "Gerhart Hauptmann"),
  "青鸟": ("The Blue Bird", "Maurice Maeterlinck"),
  "尘世之子": ("Children of the World", "Paul Heyse"),
  "戈斯塔·柏林传": ("Gösta Berling's Saga", "Selma Lagerlöf"),
  "宗教的真实": ("The Truth of Religion", "Rudolf Christoph Eucken"),
  "丛林之书": ("The Jungle Book", "Rudyard Kipling"),
  "新诗集": ("Nuove Poesie", "Giosuè Carducci"),
  "你往何处去": ("Quo Vadis", "Henryk Sienkiewicz"),
  "米蕾雅": ("Mireio", "Frédéric Mistral"),
  "伟大的牵线人": ("The Great Galeoto", "José Echegaray"),
  "太阳山庄的西诺芙": ("Synnøve Solbakken", "Bjørnstjerne Bjørnson"),
  "罗马史": ("History of Rome", "Theodor Mommsen"),
  "辞章与诗歌": ("Stances et Poèmes", "Sully Prudhomme"),
}

chinese_authors = set([
    '三毛', '严歌苓', '[明] 施耐庵', '[清] 沈复', '[清] 曹雪芹', '[明] 罗贯中',
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

with open('/root/1CT-Share/20260804-all-book_reviews/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

for b in books:
    cn_name = b.get('cn_name', '')
    author = b.get('author', '')
    if author not in chinese_authors:
        if not b.get('en_author'):
            if cn_name in mapping:
                b['en_name'] = mapping[cn_name][0]
                b['en_author'] = mapping[cn_name][1]
            else:
                # fallback for some missed ones
                pass

with open('/root/1CT-Share/20260804-all-book_reviews/books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

# Update MD files
md_dir = '/root/1CT-Share/20260804-all-book_reviews/all-md'
for md_file in glob.glob(os.path.join(md_dir, '*.md')):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # MD files have tables with columns. Let's assume columns like:
    # | 外文原名 | 外文作者 | ...
    # We will just parse the table, match by `cn_name` (usually in a column like | 书名 |)
    # Actually, the best way to update Markdown tables is by reading line by line.
    lines = content.split('\n')
    header_idx = -1
    cn_name_col = -1
    en_name_col = -1
    en_author_col = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and '书名' in line:
            header_idx = i
            cols = [c.strip() for c in line.split('|')]
            for j, c in enumerate(cols):
                if '书名' in c: cn_name_col = j
                if '外文原名' in c: en_name_col = j
                if '外文作者' in c: en_author_col = j
            break
            
    if header_idx != -1 and cn_name_col != -1 and en_name_col != -1 and en_author_col != -1:
        for i in range(header_idx + 2, len(lines)):
            line = lines[i]
            if not line.strip().startswith('|'):
                continue
            cols = line.split('|')
            if len(cols) > max(cn_name_col, en_name_col, en_author_col):
                cn_name_raw = cols[cn_name_col].strip()
                # remove markdown links if any like [Name](url)
                m = re.match(r'\[(.*?)\]\(.*?\)', cn_name_raw)
                if m:
                    cname = m.group(1)
                else:
                    cname = cn_name_raw
                
                # Check mapping
                if cname in mapping:
                    cols[en_name_col] = ' ' + mapping[cname][0] + ' '
                    cols[en_author_col] = ' ' + mapping[cname][1] + ' '
                    lines[i] = '|'.join(cols)

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
