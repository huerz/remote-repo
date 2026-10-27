# -*- coding: utf-8 -*-
"""把「红影赏析」扩到 500 部：10 个类型 × 50 部。

做法：用 TMDB 的 /discover/movie 按类型拉高分片（vote_count ≥ 500），
再对每部取 /movie/{id}?append_to_response=credits 拿导演与主演，
最后下载海报（780×1170）裁成 600×900。

已存在的片名会被跳过，不会重复插入。
"""
import io
import json
import os
import re
import sqlite3
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

# tid, 名称, 文件名前缀, TMDB genre_id, 目录
GENRES = [
    (1, '动作片', 'ac', 28, '动作片'),
    (2, '科幻片', 'kh', 878, '科幻片'),
    (3, '剧情片', 'jq', 18, '剧情片'),
    (4, '动画片', 'dh', 16, '动画片'),
    (5, '喜剧片', 'xj', 35, '喜剧片'),
    (6, '悬疑片', 'xy', 9648, '悬疑片'),
    (7, '爱情片', 'aq', 10749, '爱情片'),
    (8, '犯罪片', 'fz', 80, '犯罪片'),
    (9, '战争片', 'zz', 10752, '战争片'),
    (10, '奇幻片', 'qh', 14, '奇幻片'),
]
PER_TYPE = 50


def api(path, **params):
    params['api_key'] = KEY
    params.setdefault('language', 'zh-CN')
    q = '&'.join(f'{k}={v}' for k, v in params.items())
    url = f'https://api.themoviedb.org/3{path}?{q}'
    for _ in range(3):
        raw = subprocess.run(['curl', '-s', '--noproxy', '*', '-m', '20', url],
                             capture_output=True).stdout
        try:
            return json.loads(raw.decode('utf-8', 'ignore'))
        except Exception:
            time.sleep(1)
    return {}


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


def download_poster(path, out):
    raw = subprocess.run(
        ['curl', '-sL', '--noproxy', '*', '-m', '30', 'https://image.tmdb.org/t/p/w780' + path],
        capture_output=True).stdout
    if len(raw) < 8000:
        return False
    img = Image.open(io.BytesIO(raw)).convert('RGB')
    crop(img).save(out, 'JPEG', quality=90)
    return True


def main():
    if not KEY:
        print('缺少 TMDB_KEY')
        sys.exit(1)

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # 新类型先写进类型表
    for tid, name, _p, _g, _d in GENRES:
        row = cur.execute('SELECT 1 FROM filmtype WHERE tid=?', (tid,)).fetchone()
        if not row:
            cur.execute('INSERT INTO filmtype (tid, name, cover, remark) VALUES (?,?,?,?)',
                        (tid, name, f't{tid}.png', ''))
    conn.commit()

    # 已有片名与已有文件序号
    existing = {r[0] for r in cur.execute('SELECT title FROM films')}
    used_mid = set()
    next_idx = {}
    for tid, _n, prefix, _g, _d in GENRES:
        mx = 0
        for (cover,) in cur.execute('SELECT cover FROM films WHERE tid=?', (tid,)):
            m = re.match(rf'{prefix}(\d+)\.jpg', cover or '')
            if m:
                mx = max(mx, int(m.group(1)))
        next_idx[tid] = mx + 1

    total_added = 0
    for tid, name, prefix, gid, folder in GENRES:
        dirpath = os.path.join(BASE, folder)
        os.makedirs(dirpath, exist_ok=True)

        have = cur.execute('SELECT COUNT(*) FROM films WHERE tid=?', (tid,)).fetchone()[0]
        need = PER_TYPE - have
        if need <= 0:
            print(f'[{name}] 已有 {have} 部，跳过')
            continue

        # 拉候选：按评分降序，每类多拉几页
        cands = []
        for page in range(1, 11):
            d = api('/discover/movie', with_genres=gid, sort_by='vote_average.desc',
                    **{'vote_count.gte': 250, 'page': page})
            for r in d.get('results') or []:
                if r.get('poster_path'):
                    cands.append(r)
            if len(cands) >= need * 3:
                break
            time.sleep(0.05)

        added = 0
        for r in cands:
            if added >= need:
                break
            mid = r['id']
            title = (r.get('title') or r.get('original_title') or '').strip()
            if not title or mid in used_mid or title in existing:
                continue

            det = api(f'/movie/{mid}', append_to_response='credits')
            credits = det.get('credits') or {}
            director = ' / '.join(
                c['name'] for c in (credits.get('crew') or []) if c.get('job') == 'Director'
            ) or '未知'
            cast = ' / '.join(c['name'] for c in (credits.get('cast') or [])[:3]) or '未知'
            year = (r.get('release_date') or '')[:4]
            rating = int(round(float(r.get('vote_average') or 0)))
            desc = (det.get('overview') or r.get('overview') or '').strip()
            if len(desc) > 120:
                desc = desc[:119] + '…'

            cover = f'{prefix}{next_idx[tid]}.jpg'
            out = os.path.join(dirpath, cover)
            try:
                if not download_poster(r['poster_path'], out):
                    continue
            except Exception:
                continue

            cur.execute('''INSERT INTO films (title, tid, cover, year, author, present, describes, rating, commentscount)
                           VALUES (?,?,?,?,?,?,?,?,?)''',
                        (title, tid, cover, year, director, cast, desc, rating, 0))
            existing.add(title)
            used_mid.add(mid)
            next_idx[tid] += 1
            added += 1
            total_added += 1
            if added % 10 == 0:
                conn.commit()
                print(f'  [{name}] +{added}')
            time.sleep(0.03)

        conn.commit()
        print(f'[{name}] 新增 {added} 部（现有 {have + added}）')

    conn.commit()
    print('\n总新增：', total_added)
    for tid, name, *_ in GENRES:
        n = cur.execute('SELECT COUNT(*) FROM films WHERE tid=?', (tid,)).fetchone()[0]
        print(f'  {name}: {n}')
    print('总计：', cur.execute('SELECT COUNT(*) FROM films').fetchone()[0])
    conn.close()


if __name__ == '__main__':
    main()
