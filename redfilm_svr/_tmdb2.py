# -*- coding: utf-8 -*-
"""给新增的 60 部电影抓 TMDB 原版海报。

策略：先用中文名搜（TMDB 中文库能命中一部分），失败再用英文名；按年份过滤。
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
BASE = r'D:/高级网页设计/电影海报'
TID_DIR = {1: '动作片', 2: '科幻片', 3: '剧情片', 4: '动画片',
           5: '喜剧片', 6: '悬疑片', 7: '爱情片', 8: '犯罪片'}
TARGET = 2 / 3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _expand import NEW_FILMS  # noqa: E402


def curl(url, timeout=20):
    return subprocess.run(['curl', '-s', '--noproxy', '*', '-m', str(timeout), url],
                          capture_output=True).stdout


def search_one(name, year):
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
    if not KEY:
        print('缺少 TMDB_KEY')
        sys.exit(1)

    ok = fail = 0
    for tid, films in NEW_FILMS.items():
        folder = os.path.join(BASE, TID_DIR[tid])
        os.makedirs(folder, exist_ok=True)
        for title, en, cover, year, *_rest in films:
            out = os.path.join(folder, cover)
            if os.path.exists(out) and os.path.getsize(out) > 60000:
                ok += 1
                continue
            poster = search_one(title, year)
            if not poster:
                poster = search_one(en, year)
            if not poster:
                print(f'[跳过] {title} / {en}')
                fail += 1
                continue
            try:
                raw = curl('https://image.tmdb.org/t/p/w780' + poster, timeout=30)
                img = Image.open(io.BytesIO(raw)).convert('RGB')
                crop(img).save(out, 'JPEG', quality=92)
                print(f'[OK]   {title}')
                ok += 1
            except Exception as e:
                print(f'[失败] {title} —— {type(e).__name__}')
                fail += 1
            time.sleep(0.2)
    print(f'\n完成：成功 {ok}，失败 {fail}')


if __name__ == '__main__':
    main()
