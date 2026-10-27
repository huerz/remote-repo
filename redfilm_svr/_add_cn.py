# -*- coding: utf-8 -*-
"""批量添加 41 部国产经典电影（TMDB 抓原版海报）。"""
import io
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.parse

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

KEY = os.environ.get('TMDB_KEY', '')
# OFFLINE=1：跳过网络抓图，只入库 + 预留封面文件名，海报交给 _fill_posters.py 生成
OFFLINE = os.environ.get('OFFLINE') == '1'
DB = r'D:/高级网页设计/redfilm_svr/redfilmdbs.db'
BASE = r'D:/高级网页设计/电影海报'
TARGET = 2 / 3

TID_DIR = {1: '动作片', 2: '科幻片', 3: '剧情片', 4: '动画片',
           5: '喜剧片', 6: '悬疑片', 7: '爱情片', 8: '犯罪片',
           9: '战争片', 10: '奇幻片'}

# (tid, 片名, 英文名, 文件名, 年份, 导演, 主演, 评分, 简介)
FILMS = [
    (1, '卧虎藏龙', 'Crouching Tiger, Hidden Dragon', None, '2000', '李安', '周润发 / 杨紫琼 / 章子怡', 8, '一把青冥剑，牵出两代人的江湖恩怨。'),
    (1, '英雄', 'Hero', None, '2002', '张艺谋', '李连杰 / 梁朝伟 / 张曼玉', 8, '无名刺客面圣，讲出三个刺秦的版本。'),
    (1, '十面埋伏', 'House of Flying Daggers', None, '2004', '张艺谋', '章子怡 / 刘德华 / 金城武', 8, '飞刀门与官府的追捕里，夹着一段情。'),
    (1, '一代宗师', 'The Grandmaster', None, '2013', '王家卫', '梁朝伟 / 章子怡', 8, '叶问与宫二，武学里见天地、见众生。'),
    (1, '黄飞鸿', 'Once Upon a Time in China', None, '1991', '徐克', '李连杰 / 关之琳', 9, '狮王争霸的时代，宗师也在找中国的答案。'),
    (1, '新龙门客栈', 'New Dragon Gate Inn', None, '1992', '李惠民', '张曼玉 / 林青霞 / 梁家辉', 9, '大漠客栈里，各方人马刀刀见血。'),
    (3, '鬼子来了', 'Devils on the Doorstep', None, '2000', '姜文', '姜文 / 姜鸿波', 9, '村里来了两个俘虏，笑过之后全是冷。'),
    (3, '芙蓉镇', 'Hibiscus Town', None, '1987', '谢晋', '刘晓庆 / 姜文', 9, '一场运动，压垮了小镇上好好的人。'),
    (3, '大红灯笼高高挂', 'Raise the Red Lantern', None, '1991', '张艺谋', '巩俐', 9, '深宅大院里，女人活成了规矩。'),
    (3, '秋菊打官司', 'The Story of Qiu Ju', None, '1992', '张艺谋', '巩俐', 8, '她只是想讨个说法，一路讨到了市里。'),
    (3, '饮食男女', 'Eat Drink Man Woman', None, '1994', '李安', '吴倩莲 / 杨贵媚', 9, '父亲每周的家宴，藏着说不出口的爱。'),
    (3, '芳华', 'Youth', None, '2017', '冯小刚', '黄轩 / 苗苗', 8, '文工团的青春，散场后各奔天涯。'),
    (3, '唐山大地震', 'Aftershock', None, '2010', '冯小刚', '徐帆 / 张静初', 8, '二十三秒的地震，三十二年的心结。'),
    (3, '悲情城市', 'A City of Sadness', None, '1989', '侯孝贤', '梁朝伟 / 辛树芬', 9, '二二八前后的家族，沉默地扛着时代。'),
    (3, '牯岭街少年杀人事件', 'A Brighter Summer Day', None, '1991', '杨德昌', '张震 / 杨静怡', 9, '少年的刀，刺向的是整个时代。'),
    (3, '喜宴', 'The Wedding Banquet', None, '1993', '李安', '赵文瑄 / 归亚蕾', 9, '一场假结婚的喜宴，办出了真的家事。'),
    (3, '我不是潘金莲', 'I Am Not Madame Bovary', None, '2016', '冯小刚', '范冰冰 / 郭涛', 8, '为一句真话，她告了十年。'),
    (5, '九品芝麻官', 'Hail the Judge', None, '1994', '王晶', '周星驰 / 吴孟达', 8, '贪官包龙星，最后成了青天。'),
    (5, '食神', 'God of Cookery', None, '1996', '周星驰 / 李力持', '周星驰 / 莫文蔚', 8, '跌落神坛的食神，用一碗叉烧饭翻身。'),
    (5, '国产凌凌漆', 'From Beijing with Love', None, '1994', '周星驰 / 李力持', '周星驰 / 袁咏仪', 8, '卖肉摊的特工，一把杀猪刀走天下。'),
    (5, '审死官', 'Justice, My Foot!', None, '1992', '杜琪峰', '周星驰 / 梅艳芳', 8, '讼师铁嘴，也怕官官相护。'),
    (6, '白日焰火', 'Black Coal, Thin Ice', None, '2014', '刁亦男', '廖凡 / 桂纶镁', 8, '碎尸案里的爱情，冷得像雪。'),
    (6, '烈日灼心', 'The Dead End', None, '2015', '曹保平', '邓超 / 段奕宏', 8, '三个协警养着秘密，也养着一个女儿。'),
    (6, '神探', 'Mad Detective', None, '2007', '杜琪峰', '刘青云 / 林家栋', 8, '他看得见人心里的鬼。'),
    (6, '唐人街探案', 'Detective Chinatown', None, '2015', '陈思诚', '王宝强 / 刘昊然', 7, '曼谷的唐人街，一桩离奇的密室案。'),
    (6, '扫毒', 'The White Storm', None, '2013', '陈木胜', '古天乐 / 刘青云 / 张家辉', 7, '兄弟与毒贩之间，三选二的抉择。'),
    (9, '集结号', 'Assembly', None, '2007', '冯小刚', '张涵予 / 邓超', 9, '一声没吹响的集结号，等了半个世纪。'),
    (9, '八佰', 'The Eight Hundred', None, '2020', '管虎', '王千源 / 张译', 8, '四行仓库八百壮士，隔岸看尽人间。'),
    (9, '长津湖', 'The Battle at Lake Changjin', None, '2021', '陈凯歌 / 徐克 / 林超贤', '吴京 / 易烊千玺', 8, '冰天雪地里，新兵打成了老兵。'),
    (9, '赛德克·巴莱', 'Warriors of the Rainbow: Seediq Bale', None, '2011', '魏德圣', '林庆台 / 马志翔', 9, '如果文明要我们卑躬屈膝，那就抗争到底。'),
    (10, '倩女幽魂', 'A Chinese Ghost Story', None, '1987', '程小东', '张国荣 / 王祖贤', 9, '兰若寺里，书生恋上女鬼。'),
    (10, '大话西游之月光宝盒', 'A Chinese Odyssey Part One', None, '1995', '刘镇伟', '周星驰 / 莫文蔚', 9, '月光宝盒能回到过去，改不了结局。'),
    (7, '甜蜜蜜', 'Comrades: Almost a Love Story', None, '1996', '陈可辛', '张曼玉 / 黎明', 9, '两个异乡人，兜了十年才相遇。'),
    (7, '北京遇上西雅图', 'Finding Mr. Right', None, '2013', '薛晓路', '汤唯 / 吴秀波', 8, '隔着太平洋的两封信，落在一个机场。'),
    (7, '后来的我们', 'Us and Them', None, '2018', '刘若英', '井柏然 / 周冬雨', 8, '后来我们什么都有了，却没有了我们。'),
    (2, '疯狂的外星人', 'Crazy Alien', None, '2019', '宁浩', '黄渤 / 沈腾', 7, '外星人落到猴戏艺人手里，成了猴。'),
    (4, '白蛇：缘起', 'White Snake', None, '2019', '黄家康 / 赵霁', '张喆 / 杨天翔', 8, '白蛇与许仙的前世，是一场追与逃。'),
    (4, '姜子牙', 'Jiang Ziya', None, '2020', '程腾 / 李炜', '郑希 / 杨凝', 7, '封神之后，他偏要救眼前这一人一狐。'),
    (4, '雄狮少年', 'I Am What I Am', None, '2021', '孙海鹏', '大昕', 9, '留守少年舞狮，从病猫到雄狮。'),
    (4, '大鱼海棠', 'Big Fish & Begonia', None, '2016', '梁旋 / 张春', '季冠霖 / 苏尚卿', 7, '掌管海棠的少女，欠人类一条命。'),
    (4, '罗小黑战记', 'The Legend of Hei', None, '2019', 'MTJJ木头', '山新 / 郝祥海', 9, '猫妖小黑，在人类世界里找家。'),
    # ===== 追加：补齐奇幻片 + 更多国产经典 =====
    (10, '大话西游之大圣娶亲', 'A Chinese Odyssey Part Two: Cinderella', None, '1995', '刘镇伟', '周星驰 / 朱茵', 9, '曾经有一份真挚的爱情放在我面前……'),
    (10, '捉妖记', 'Monster Hunt', None, '2015', '许诚毅', '白百何 / 井柏然', 7, '天荫怀了妖后之子，一路逃，一路生。'),
    (10, '画皮', 'Painted Skin', None, '2008', '陈嘉上', '甄子丹 / 周迅 / 赵薇', 7, '狐妖要一张人皮，也要一颗人心。'),
    (10, '西游·降魔篇', 'Journey to the West: Conquering the Demons', None, '2013', '周星驰', '文章 / 舒淇 / 黄渤', 7, '降魔之前，先要懂得什么是情。'),
    (3, '无间道', 'Infernal Affairs', None, '2002', '刘伟强 / 麦兆辉', '刘德华 / 梁朝伟', 9, '出来混，迟早要还的。'),
    (3, '花样年华', 'In the Mood for Love', None, '2000', '王家卫', '梁朝伟 / 张曼玉', 9, '那些消逝了的岁月，隔着一层雾。'),
    (3, '重庆森林', 'Chungking Express', None, '1994', '王家卫', '金城武 / 林青霞 / 梁朝伟', 9, '凤梨罐头会过期，感情也会。'),
    (3, '春光乍泄', 'Happy Together', None, '1997', '王家卫', '张国荣 / 梁朝伟', 9, '不如，我们从头来过。'),
    (3, '阳光灿烂的日子', 'In the Heat of the Sun', None, '1994', '姜文', '夏雨 / 宁静', 9, '记忆里的夏天，总是亮得刺眼。'),
    (3, '蓝风筝', 'The Blue Kite', None, '1993', '田壮壮', '吕丽萍 / 濮存昕', 9, '风筝断了线，家也就散了。'),
    (3, '变脸', 'The King of Masks', None, '1996', '吴天明', '朱旭 / 周任莹', 9, '传男不传女，可他偏遇到个女娃。'),
    (3, '那人那山那狗', 'Postmen in the Mountains', None, '1999', '霍建起', '刘烨 / 滕汝骏', 9, '父子走一趟邮路，走完了一辈子。'),
    (3, '城南旧事', 'Memories of Old Beijing', None, '1983', '吴贻弓', '沈洁 / 张闽', 9, '长亭外，古道边，童年一去不返。'),
    (5, '疯狂的石头', 'Crazy Stone', None, '2006', '宁浩', '郭涛 / 刘桦 / 黄渤', 8, '一块翡翠，引来三拨贼。'),
    (5, '人在囧途', 'Lost on Journey', None, '2010', '叶伟民', '徐峥 / 王宝强', 8, '回家路上，两种人生撞了个满怀。'),
    (5, '夏洛特烦恼', 'Goodbye Mr. Loser', None, '2015', '闫非 / 彭大魔', '沈腾 / 马丽', 7, '梦里什么都有，醒来才知道什么最贵。'),
    (5, '功夫', 'Kung Fu Hustle', None, '2004', '周星驰', '周星驰 / 元华 / 元秋', 9, '猪笼城寨里，藏着真正的绝世高手。'),
    (2, '流浪地球', 'The Wandering Earth', None, '2019', '郭帆', '吴京 / 屈楚萧 / 李光洁', 8, '带着地球去流浪，一千代人的归途。'),
    (2, '流浪地球2', 'The Wandering Earth II', None, '2023', '郭帆', '吴京 / 刘德华 / 李雪健', 8, '移山计划之前，先得有人愿意点灯。'),
    (8, '无双', 'Project Gutenberg', None, '2018', '庄文强', '周润发 / 郭富城', 8, '假钞画师，画出真假难辨的人生。'),
    (8, '暗战', 'Running Out of Time', None, '1999', '杜琪峰', '刘德华 / 刘青云', 8, '只剩四周的命，他要打完最后一场。'),
    (8, '窃听风云', 'Overheard', None, '2009', '麦兆辉 / 庄文强', '刘青云 / 古天乐 / 吴彦祖', 8, '听到的秘密，最后都砸回自己头上。'),
    (9, '高山下的花环', 'Wreath at the Foot of the Mountain', None, '1984', '谢晋', '吕晓禾 / 唐国强', 9, '阵亡通知书上的名字，一个都不能少。'),
    (9, '地雷战', 'Landmine Warfare', None, '1962', '唐英奇', '白大钧 / 赵长瑞', 8, '不见鬼子不挂弦。'),
    (9, '小兵张嘎', 'Little Soldier Zhang Ga', None, '1963', '崔嵬 / 欧阳红樱', '安吉斯 / 张莹', 8, '白洋淀上的嘎子，从淘气鬼长成战士。'),
    (6, '暴裂无声', 'Wrath of Silence', None, '2017', '忻钰坤', '宋洋 / 姜武 / 袁文康', 8, '哑巴矿工找儿子，山里没有答案。'),
    (6, '心迷宫', 'Deep in the Heart', None, '2014', '忻钰坤', '霍卫民 / 王笑天', 8, '一具尸体，三个家庭各有说法。'),
    (1, '战狼2', 'Wolf Warrior 2', None, '2017', '吴京', '吴京 / 弗兰克·格里罗', 7, '犯我中华者，虽远必诛。'),
    (1, '叶问', 'Ip Man', None, '2008', '叶伟信', '甄子丹 / 熊黛林 / 任达华', 8, '我要打十个。'),
    (4, '哪吒之魔童降世', 'Ne Zha', None, '2019', '饺子', '吕艳婷 / 囧森瑟夫', 9, '我命由我不由天。'),
    (4, '西游记之大圣归来', 'Monkey King: Hero Is Back', None, '2015', '田晓鹏', '张磊 / 林子杰', 8, '五行山下五百年，他终于又戴上了金箍。'),
    (4, '大闹天宫', 'Havoc in Heaven', None, '1961', '万籁鸣', '邱岳峰（配音）', 9, '锣鼓一响，齐天大圣就是一辈子。'),
    (7, '山楂树之恋', 'Under the Hawthorn Tree', None, '2010', '张艺谋', '周冬雨 / 窦骁', 8, '等一等，等到下辈子再告诉你。'),
    (7, '如果·爱', 'Perhaps Love', None, '2005', '陈可辛', '周迅 / 金城武 / 张学友', 8, '十年后再相遇，我们都演不回自己。'),
]


def curl(url, timeout=25):
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


PREFIX = {1: "ac", 2: "kh", 3: "jq", 4: "dh", 5: "xj", 6: "xy", 7: "aq", 8: "fz", 9: "zz", 10: "qh"}


def next_cover(cur, tid, prefix):
    n = cur.execute('SELECT COUNT(*) FROM films WHERE tid=?', (tid,)).fetchone()[0]
    i = 1
    while cur.execute('SELECT 1 FROM films WHERE tid=? AND cover=?', (tid, f'{prefix}{i}.jpg')).fetchone():
        i += 1
    return f'{prefix}{i}.jpg'


def main():
    if not KEY and not OFFLINE:
        sys.exit('缺少 TMDB_KEY（或设 OFFLINE=1 跳过抓图）')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    added = skipped = 0
    for row in FILMS:
        tid, title, en, _cover, year, director, cast, rating, desc = row
        if cur.execute('SELECT 1 FROM films WHERE title=?', (title,)).fetchone():
            skipped += 1
            continue
        folder = TID_DIR[tid]
        os.makedirs(os.path.join(BASE, folder), exist_ok=True)
        poster = None if OFFLINE else (search(title, year) or search(en, year))
        cover = next_cover(cur, tid, PREFIX[tid])
        out = os.path.join(BASE, folder, cover)
        saved = False
        if poster:
            try:
                raw = curl('https://image.tmdb.org/t/p/w780' + poster, timeout=30)
                img = Image.open(io.BytesIO(raw)).convert('RGB')
                crop(img).save(out, 'JPEG', quality=92)
                saved = True
            except Exception:
                saved = False
        cur.execute('''INSERT INTO films (title, tid, cover, year, author, present, describes, rating, commentscount)
                       VALUES (?,?,?,?,?,?,?,?,?)''',
                    (title, tid, cover, year, director, cast, desc, rating, 0))
        added += 1
        print('[OK]  ', title, '(海报)' if saved else '(暂无海报)')
        time.sleep(0.25)
    conn.commit()
    print(f'\n新增 {added}，跳过（已存在）{skipped}')
    for tid, name, n in cur.execute('SELECT t.tid,t.name,COUNT(f.cid) FROM filmtype t LEFT JOIN films f ON f.tid=t.tid GROUP BY t.tid ORDER BY t.tid'):
        print(f'  {name}: {n}')
    print('总计', cur.execute('SELECT COUNT(*) FROM films').fetchone()[0])
    conn.close()


if __name__ == '__main__':
    main()
