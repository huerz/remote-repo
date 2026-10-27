# -*- coding: utf-8 -*-
"""补齐最后 31 部（犯罪片 11 + 奇幻片 20），用 TMDB 的按片名搜索。

比 discover 稳：片名精确，命中率高；抓不到海报的用设计海报兜底。
"""
import io
import json
import os
import subprocess
import sys
import time
import urllib.parse

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

KEY = os.environ.get('TMDB_KEY', '')
DB = r'D:/高级网页设计/redfilm_svr/redfilmdbs.db'
BASE = r'D:/高级网页设计/电影海报'
TARGET = 2 / 3

FILL = {
    (8, '犯罪片', 'fz'): [
        ('教父3', 'The Godfather Part III', '1990', '弗朗西斯·福特·科波拉', '阿尔·帕西诺', 8, '权力的最后一段路，代价是孤独。'),
        ('美国往事', 'Once Upon a Time in America', '1984', '赛尔乔·莱昂内', '罗伯特·德尼罗', 9, '一生兄弟，一场背叛，一段旧梦。'),
        ('这个杀手不太冷', 'Léon: The Professional', '1994', '吕克·贝松', '让·雷诺 / 娜塔莉·波特曼', 9, '杀手与女孩，两个孤独的人互相照亮。'),
        ('情枭的黎明', 'Carlito\'s Way', '1993', '布莱恩·德·帕尔玛', '阿尔·帕西诺', 8, '想洗手不干，可这条路没有出口。'),
        ('纽约黑帮', 'Gangs of New York', '2002', '马丁·斯科塞斯', '莱昂纳多·迪卡普里奥', 8, '纽约的街头，是刀与血写的历史。'),
        ('窃听风云', 'Overheard', '2009', '麦兆辉 / 庄文强', '古天乐 / 刘青云 / 吴彦祖', 8, '一条情报，三个警察，一起沉沦。'),
        ('门徒', 'Protégé', '2007', '尔冬升', '刘德华 / 吴彦祖', 8, '卧底八年，分不清自己是兵是贼。'),
        ('黑社会', 'Election', '2005', '杜琪峰', '任达华 / 梁家辉', 8, '一个龙头的位置，照出所有人的贪。'),
        ('暗战', 'Running Out of Time', '1999', '杜琪峰', '刘德华 / 刘青云', 8, '只有四十八小时寿命的贼，与警察下棋。'),
        ('枪火', 'The Mission', '1999', '杜琪峰', '黄秋生 / 吴镇宇', 9, '五个保镖站成一排，就是江湖。'),
        ('一个字头的诞生', 'Too Many Ways to Be No. 1', '1997', '韦家辉', '刘青云', 8, '命运分岔两次，怎么走都是江湖。'),
    ],
    (10, '奇幻片', 'qh'): [
        ('指环王1：护戒使者', 'The Lord of the Rings: The Fellowship of the Ring', '2001', '彼得·杰克逊', '伊利亚·伍德', 10, '一个霍比特人，接下整个中土的重量。'),
        ('指环王2：双塔奇兵', 'The Lord of the Rings: The Two Towers', '2002', '彼得·杰克逊', '伊利亚·伍德', 10, '圣盔谷的夜，守住的是最后一点希望。'),
        ('指环王3：王者无敌', 'The Lord of the Rings: The Return of the King', '2003', '彼得·杰克逊', '伊利亚·伍德', 10, '魔戒归于末日火山，王者重返白城。'),
        ('霍比特人1：意外之旅', 'The Hobbit: An Unexpected Journey', '2012', '彼得·杰克逊', '马丁·弗瑞曼', 8, '一扇门被推开，旅程就从这里开始。'),
        ('哈利·波特与魔法石', 'Harry Potter and the Sorcerer\'s Stone', '2001', '克里斯·哥伦布', '丹尼尔·雷德克里夫', 9, '十一岁那年的信，把他送进了魔法世界。'),
        ('哈利·波特与阿兹卡班的囚徒', 'Harry Potter and the Prisoner of Azkaban', '2004', '阿方索·卡隆', '丹尼尔·雷德克里夫', 9, '时间倒转一圈，救下的是自己的过去。'),
        ('加勒比海盗', 'Pirates of the Caribbean: The Curse of the Black Pearl', '2003', '戈尔·维宾斯基', '约翰尼·德普', 9, '黑珍珠号上，疯子船长最清醒。'),
        ('纳尼亚传奇', 'The Chronicles of Narnia: The Lion, the Witch and the Wardrobe', '2005', '安德鲁·亚当森', '蒂尔达·斯文顿', 8, '衣柜的另一边，是一个等雪融化的王国。'),
        ('潘神的迷宫', 'Pan\'s Labyrinth', '2006', '吉尔莫·德尔·托罗', '伊万娜·巴克罗', 9, '童话与暴政，在同一个女孩眼里重叠。'),
        ('水形物语', 'The Shape of Water', '2017', '吉尔莫·德尔·托罗', '莎莉·霍金斯', 8, '两个无法言语的人，在水里彼此听懂。'),
        ('大鱼', 'Big Fish', '2003', '蒂姆·波顿', '伊万·麦克格雷格', 9, '父亲的一生是故事，也是真的。'),
        ('剪刀手爱德华', 'Edward Scissorhands', '1990', '蒂姆·波顿', '约翰尼·德普 / 薇诺娜·瑞德', 9, '他有一双手，却抱不住任何东西。'),
        ('查理和巧克力工厂', 'Charlie and the Chocolate Factory', '2005', '蒂姆·波顿', '约翰尼·德普', 8, '糖果工厂里，藏着五种孩子的结局。'),
        ('少年派的奇幻漂流', 'Life of Pi', '2012', '李安', '苏拉·沙玛', 9, '一条船、一只虎，和一片不肯沉默的海。'),
        ('捉妖记', 'Monster Hunt', '2015', '许诚毅', '白百何 / 井柏然', 7, '生了只小妖，就得护它到底。'),
        ('画皮', 'Painted Skin', '2008', '陈嘉上', '周迅 / 赵薇 / 陈坤', 7, '皮相之下，是妖也想要的一颗心。'),
        ('西游降魔篇', 'Journey to the West: Conquering the Demons', '2013', '周星驰', '文章 / 舒淇', 8, '降的是魔，渡的是人。'),
        ('与神同行', 'Along with the Gods: The Two Worlds', '2017', '金容华', '河正宇 / 车太铉', 8, '死后四十九天，七场审判走完一生。'),
        ('幽灵公主', 'Princess Mononoke', '1997', '宫崎骏', '松田洋治 / 石田百合子', 9, '森林与铁镇，谁也说不清谁是恶。'),
        ('爱丽丝梦游仙境', 'Alice in Wonderland', '2010', '蒂姆·波顿', '米娅·华希科沃斯卡 / 约翰尼·德普', 7, '掉进兔子洞，回来时已经长大。'),
    ],
}


def curl(url, timeout=20):
    return subprocess.run(['curl', '-s', '--noproxy', '*', '-m', str(timeout), url],
                          capture_output=True).stdout


def search(name, year):
    url = (f'https://api.themoviedb.org/3/search/movie?api_key={KEY}'
           f'&query={urllib.parse.quote(name)}&language=zh-CN&include_adult=false')
    try:
        data = json.loads(curl(url).decode('utf-8', 'ignore'))
    except Exception:
        return None
    for r in data.get('results') or []:
        if (r.get('release_date') or '')[:4] == year and r.get('poster_path'):
            return r['poster_path']
    for r in data.get('results') or []:
        if r.get('poster_path'):
            return r['poster_path']
    return None


def crop(img):
    w, h = img.size
    if w / h > TARGET:
        nw = int(h * TARGET)
        left = (w - nw) // 2
        img = img.crop((left, 0, left + nw, h))
    else:
        nh = int(w / TARGET)
        top = (h - nh) // 2
        img = img.crop((0, top, w, top + nh))
    return img.resize((600, 900), Image.LANCZOS)


def main():
    import sqlite3
    if not KEY:
        sys.exit('缺少 TMDB_KEY')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    added = 0
    for (tid, folder, prefix), films in FILL.items():
        dirpath = os.path.join(BASE, folder)
        os.makedirs(dirpath, exist_ok=True)
        n = cur.execute('SELECT COUNT(*) FROM films WHERE tid=?', (tid,)).fetchone()[0]
        idx = 1
        for title, en, year, director, cast, rating, desc in films:
            if cur.execute('SELECT 1 FROM films WHERE title=?', (title,)).fetchone():
                continue
            poster = search(title, year) or search(en, year)
            cover = f'{prefix}{n + 1}.jpg'
            out = os.path.join(dirpath, cover)
            ok = False
            if poster:
                try:
                    raw = curl('https://image.tmdb.org/t/p/w780' + poster, timeout=30)
                    img = Image.open(io.BytesIO(raw)).convert('RGB')
                    crop(img).save(out, 'JPEG', quality=92)
                    ok = True
                except Exception:
                    pass
            if not ok:
                print(f'  [无海报] {title}')
                cover = None
            cur.execute('''INSERT INTO films (title, tid, cover, year, author, present, describes, rating, commentscount)
                           VALUES (?,?,?,?,?,?,?,?,?)''',
                        (title, tid, cover or f'{prefix}{n+1}.jpg', year, director, cast, desc, rating, 0))
            n += 1
            added += 1
            print(f'[OK] {title}')
            time.sleep(0.15)
        conn.commit()
    print('\n补齐：', added, '部')
    for tid, name, k in cur.execute('SELECT t.tid,t.name,COUNT(f.cid) FROM filmtype t LEFT JOIN films f ON f.tid=t.tid GROUP BY t.tid ORDER BY t.tid'):
        print(f'  {name}: {k}')
    print('总计', cur.execute('SELECT COUNT(*) FROM films').fetchone()[0])
    conn.close()


if __name__ == '__main__':
    main()
