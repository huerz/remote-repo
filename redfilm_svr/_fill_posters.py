# -*- coding: utf-8 -*-
"""给缺海报的影片生成设计海报（兜底，保证页面不出现破图）。

只处理文件不存在的记录；已有原版海报的一律不动。
"""
import math
import os
import random
import sqlite3

from PIL import Image, ImageDraw, ImageFilter, ImageFont

DB = r'D:/高级网页设计/redfilm_svr/redfilmdbs.db'
BASE = r'D:/高级网页设计/电影海报'
TID_DIR = {1: '动作片', 2: '科幻片', 3: '剧情片', 4: '动画片',
           5: '喜剧片', 6: '悬疑片', 7: '爱情片', 8: '犯罪片',
           9: '战争片', 10: '奇幻片'}
W, H = 600, 900

# 类型：深底 / 亮色 / 主文字 / 副文字
THEME = {
    1: ((18, 10, 9), (198, 62, 40), (244, 226, 200), (196, 152, 120)),
    2: ((6, 12, 26), (58, 132, 214), (226, 238, 252), (150, 180, 214)),
    3: ((10, 20, 17), (52, 116, 96), (236, 228, 206), (176, 164, 132)),
    4: ((46, 26, 10), (232, 150, 52), (255, 240, 210), (222, 188, 140)),
    5: ((44, 34, 8), (214, 182, 48), (255, 248, 214), (214, 196, 140)),
    6: ((26, 14, 32), (128, 88, 178), (232, 220, 246), (176, 156, 200)),
    7: ((52, 18, 32), (206, 110, 140), (252, 226, 234), (200, 160, 176)),
    8: ((18, 18, 22), (120, 120, 136), (232, 232, 238), (160, 160, 172)),
    9: ((14, 20, 18), (76, 108, 74), (238, 234, 206), (178, 176, 140)),
    10: ((22, 14, 34), (110, 76, 176), (240, 226, 252), (182, 158, 214)),
}
FONT = r'C:/Windows/Fonts/simhei.ttf'
FONT_L = r'C:/Windows/Fonts/msyh.ttc'


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_pattern(d, tid, cx, cy, seed, accent):
    rnd = random.Random(seed)
    if tid in (1, 8):                      # 放射光束 / 斜切光
        for _ in range(rnd.randint(14, 20)):
            ang = rnd.uniform(0, 6.283)
            ln = rnd.uniform(150, 320)
            d.line([cx, cy, cx + ln * math.cos(ang), cy + ln * math.sin(ang)],
                   fill=accent, width=rnd.randint(1, 3))
    elif tid in (2, 6):                    # 同心环
        for i in range(4):
            r = 60 + i * 46 + rnd.randint(-8, 8)
            d.ellipse([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62],
                      outline=accent, width=rnd.randint(1, 2))
        for _ in range(50):
            d.point([rnd.randint(0, W), rnd.randint(0, H)], fill=accent)
    elif tid == 3:                         # 横向光带
        for _ in range(rnd.randint(5, 8)):
            y = rnd.randint(120, H - 200)
            d.rectangle([0, y, W, y + rnd.randint(2, 7)], fill=accent)
    elif tid == 4:                         # 气泡
        for _ in range(rnd.randint(16, 24)):
            r = rnd.randint(10, 54)
            x, y = rnd.randint(0, W), rnd.randint(60, H - 240)
            d.ellipse([x - r, y - r, x + r, y + r], outline=accent, width=rnd.randint(1, 3))
    elif tid == 5:                         # 笑弧
        for _ in range(rnd.randint(4, 7)):
            r = rnd.randint(70, 180)
            x, y = rnd.randint(0, W), rnd.randint(80, H - 220)
            d.arc([x - r, y - r, x + r, y + r], 200, 340, fill=accent, width=rnd.randint(2, 4))
    else:                                  # 爱情：交叠的圆
        for i in range(3):
            r = rnd.randint(90, 150)
            x = cx + rnd.randint(-70, 70)
            y = cy + rnd.randint(-50, 50)
            d.ellipse([x - r, y - r, x + r, y + r], outline=accent, width=2)


def make(title, director, year, tid, cid, out):
    dark, accent, main, sub = THEME.get(tid, THEME[1])
    rnd = random.Random(cid * 977)

    img = Image.new('RGB', (W, H), dark)
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(lerp(dark, accent, 0.26), dark, y / H))

    gx, gy = W // 2 + rnd.randint(-70, 70), int(H * 0.36) + rnd.randint(-30, 30)
    g = Image.new('RGB', (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([gx - 195, gy - 195, gx + 195, gy + 195], fill=accent)
    g = g.filter(ImageFilter.GaussianBlur(108))
    mask = g.convert('L').point(lambda v: int(v * 110 / 255))
    img = Image.composite(g, img, mask)

    layer = Image.new('RGB', (W, H), (0, 0, 0))
    draw_pattern(ImageDraw.Draw(layer), tid, gx, gy, cid, accent)
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.blend(img, Image.blend(img, layer, 0.52), 0.78)

    for _ in range(2200):
        x, y = rnd.randint(0, W - 1), rnd.randint(0, H - 1)
        p = img.getpixel((x, y))
        v = rnd.randint(-14, 14)
        img.putpixel((x, y), tuple(max(0, min(255, p[i] + v)) for i in range(3)))

    d = ImageDraw.Draw(img)
    d.line([(40, 54), (W - 40, 54)], fill=accent, width=1)
    d.text((44, 26), TID_DIR.get(tid, ''), font=ImageFont.truetype(FONT_L, 22), fill=sub)

    n = len(title)
    size = 76 if n <= 4 else (62 if n <= 6 else 50)
    f = ImageFont.truetype(FONT, size)
    lines = [title] if n <= 6 else [title[:(n + 1) // 2], title[(n + 1) // 2:]]
    y0 = H - 210 - len(lines) * int(size * 1.22)
    for i, ln in enumerate(lines):
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y0 + i * size * 1.22), ln, font=f, fill=main)

    d.line([(W / 2 - 40, H - 176), (W / 2 + 40, H - 176)], fill=accent, width=2)
    meta = f'{director} · {year}' if director and year else (director or year or '')
    fm = ImageFont.truetype(FONT_L, 24)
    if len(meta) > 22:
        meta = meta[:21] + '…'
    mw = d.textlength(meta, font=fm)
    d.text(((W - mw) / 2, H - 156), meta, font=fm, fill=sub)

    x = 20
    while x + 24 < W - 20:
        d.rectangle([x, H - 40, x + 24, H - 24], fill=(12, 12, 12))
        x += 38

    img.save(out, 'JPEG', quality=90)


def main():
    conn = sqlite3.connect(DB)
    rows = list(conn.execute('SELECT cid, title, tid, cover, year, author FROM films ORDER BY tid, cid'))
    made = 0
    for cid, title, tid, cover, year, author in rows:
        folder = TID_DIR.get(tid)
        if not folder:
            continue
        out = os.path.join(BASE, folder, cover or f'{cid}.jpg')
        if os.path.exists(out):
            continue
        make(title, author or '', year or '', tid, cid, out)
        made += 1
    print('补生成海报：', made, '张')


if __name__ == '__main__':
    main()
