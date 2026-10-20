# 共享图集库（images）

`D:\高级网页设计` 下所有项目共用的图片资源，统一放这里，不要在各自项目里另存一份。

## 一、目录结构

```
images/
├── books/                 文学作品封面（按文学类型分目录，与数据库 classictype.name 一一对应）
│   ├── 诗经/       6 张
│   ├── 楚辞/       3 张
│   ├── 汉魏诗歌/   7 张
│   ├── 唐诗/       5 张
│   ├── 宋词/       5 张
│   ├── 元曲/      10 张
│   ├── 辞赋/       1 张
│   └── 先秦散文/   3 张（暂未入库，留作后续 5.4 详情页扩展）
└── head/                  头像、站点 Logo 等通用图（10 张）
```

合计：封面 40 张 + 通用图 10 张。

## 二、命名规则

封面文件名 = **作品名的拼音首字母缩写** + `.jpg`，例如 `jys.jpg` = 静夜思、`cbhg.jpg` = 念奴娇·赤壁怀古。

数据库 `classics.cover` 字段**只存文件名**（不带类型目录），后端会自动在 `books/` 的各类型子目录中查找，所以：

- 新增作品时，把图按类型丢进对应目录即可，`cover` 仍填文件名，**不用改数据库结构**；
- 文件移动 / 换类型目录也不影响接口，只要文件名唯一。

### 封面文件名对照表

| 类型 | 文件 | 作品 | 类型 | 文件 | 作品 |
|---|---|---|---|---|---|
| 诗经 | gj.jpg | 关雎 | 唐诗 | jys.jpg | 静夜思 |
| 诗经 | jj.jpg | 蒹葭 | 唐诗 | hhl.jpg | 黄鹤楼送孟浩然之广陵 |
| 诗经 | zj.jpg | 子衿 | 唐诗 | cyxy.jpg | 春夜喜雨 |
| 诗经 | ty.jpg | 桃夭 | 唐诗 | qm.jpg | 清明 |
| 诗经 | wy.jpg | 无衣 | 唐诗 | jx.jpg | 江雪 |
| 诗经 | jn.jpg | 静女 | 宋词 | cbhg.jpg | 念奴娇·赤壁怀古 |
| 楚辞 | qfc.jpg | 秋风辞 | 宋词 | myjsy.jpg | 水调歌头·明月几时有 |
| 楚辞 | ls.jpg | 离骚 | 宋词 | bzz.jpg | 破阵子·为陈同甫赋壮词以寄之 |
| 楚辞 | jggs.jpg | 九歌·国殇 | 宋词 | ssm.jpg | 声声慢·寻寻觅觅 |
| 汉魏诗歌 | gch.jpg | 观沧海 | 宋词 | mjh.jpg | 满江红·写怀 |
| 汉魏诗歌 | dgx.jpg | 短歌行 | 元曲 | jtmx.jpg | 寿阳曲·江天暮雪 |
| 汉魏诗歌 | cgx.jpg | 长歌行 | 元曲 | skyxs.jpg | 四块玉·闲适 |
| 汉魏诗歌 | hjn.jpg | 江南 | 元曲 | zglzq.jpg | 折桂令·中秋 |
| 汉魏诗歌 | sx.jpg | 上邪 | 元曲 | qh.jpg | 清江引·秋怀 |
| 汉魏诗歌 | xbygl.jpg | 西北有高楼 | 元曲 | tjsqs.jpg | 天净沙·秋思 |
| 汉魏诗歌 | dfg.jpg | 大风歌 | 元曲 | tjsqq.jpg | 天净沙·秋 |
| 辞赋 | lsf.jpg | 洛神赋 | 元曲 | lhhg.jpg | 山坡羊·骊山怀古 |
| 先秦散文 | cslz.jpg | 曹刿论战 | 元曲 | jr.jpg | 蟾宫曲·九日 |
| 先秦散文 | ddzx.jpg | 大道之行也 | 元曲 | sxzyy.jpg | 水仙子·夜雨 |
| 先秦散文 | yhal.jpg | 生于忧患死于安乐 | 元曲 | ypfg.jpg | 寿阳曲·远浦帆归 |

## 三、各项目怎么引用

### 1. Vue 项目（cls_clt）

走 cls_svr 的图片接口，不要在 `src/assets` 里再放一份：

```html
<!-- 代理前缀 /svr 已在 vite.config.js 配好 -->
<el-image :src="'/svr/api/image/display/cls/' + item.cover" fit="contain" />
<img src="/svr/api/image/display/head/logo.png" />
```

### 2. Flask 项目（cls_svr / Hi_flask / Hi_Jinja2）

`cls_svr` 已内置接口（`app/api/image_blueprint.py`）：

| 接口 | 说明 |
|---|---|
| `GET /api/image/display/cls/<文件名>` | 作品封面，自动在类型子目录里找 |
| `GET /api/image/display/cls/<类型>/<文件名>` | 指定类型直接取，如 `cls/唐诗/jys.jpg` |
| `GET /api/image/display/head/<文件名>` | 头像 / Logo |

其他 Flask 项目想共用，把下面这段放进蓝图即可（路径指到本目录）：

```python
from flask import send_from_directory
import os

IMAGE_ROOT = r'D:/高级网页设计/images'

@app.route('/img/<path:filepath>')
def shared_image(filepath):
    return send_from_directory(IMAGE_ROOT, filepath)
```

> 注意：Werkzeug 的 `safe_join` 不认 Windows 反斜杠，路径里的分隔符务必统一成 `/`，否则会 404。

### 3. Jinja2 模板

```html
<img src="{{ url_for('shared_image', filepath='head/logo.png') }}" />
<img src="{{ url_for('shared_image', filepath='books/唐诗/jys.jpg') }}" />
```

## 四、新增图片的规范

1. 按类型放进 `books/<类型>/`，文件名用拼音缩写、保持唯一；
2. 数据库 `classics.cover` 只填文件名（如 `xxx.jpg`）；
3. 接口有索引缓存，文件名没命中时会自动重建一次，**新增图片无需重启后端**；
4. 通用图（头像、Logo、二维码等）放 `head/`。

## 五、变更记录

- 2026-10-20：由 `cls_image/` 迁入本目录并按文学类型重新归档，原目录改名 `cls_image.bak-20261020` 留存；`cls_svr` 图片路径与接口同步改造。
