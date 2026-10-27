# ============================================================================
# 书评示例数据导入脚本：discuss 表 + 回写 classics.commentscount
# ----------------------------------------------------------------------------
# 作用：给热门作品灌入一批示例书评，并把每部作品的评论数校准成 discuss 表的真实条数
#       （原先 commentscount 是随手写的假数字，和实际书评完全对不上，
#         详情页会出现「7620 条」却一条都不显示的情况）。
# 用法：在 cls_svr 目录执行 .venv\Scripts\python.exe scripts\seed_discuss.py
#       --dry-run 只打印将新增的条数，不写库
# 依赖：users 表里已有的账号（作为书评作者）、classics 表、discuss 表
# 约定：按「作品 + 用户 + 评论内容」去重，可反复执行
# ============================================================================
from __future__ import annotations

import argparse
import datetime
import pathlib
import random
import sys

# 本脚本位于 cls_svr/scripts/，把项目根加入模块搜索路径才能 import app 包
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 示例书评：cid -> 评论列表。
# 只挑热度最高的作品，评论写得具体一点（贴近诗句本身），答辩演示更真实。
DISCUSS_SEED: dict[int, list[str]] = {
    7: [  # 关雎
        '「窈窕淑女，君子好逑」两千多年过去，还是最好听的一句表白。',
        '注意「流之」「采之」「芼之」的递进：采摘动作一步步加深，感情也是。',
        '「辗转反侧」四个字，失眠的人一看就懂。',
    ],
    1: [  # 静夜思
        '二十个字没有任何修辞，却比很多长诗更让人想家。',
        '「疑是地上霜」这个错觉写得太准，宿舍地板反光时我也这样以为过。',
    ],
    31: [  # 天净沙·秋思
        '前三句全是名词，没有一个动词，画面却动起来了。',
        '「古道西风瘦马」，瘦的是马，也是人。',
        '最后一句「断肠人在天涯」读出来，前面九种景物一下全活了。',
    ],
    8: [  # 蒹葭
        '「所谓伊人，在水一方」，求而不得写得这么好看。',
        '全篇三章只换了几个字，反复咏叹，越读越冷。',
        '「溯洄从之，道阻且长」，追的过程比结果更像人生。',
    ],
    12: [  # 离骚
        '「路漫漫其修远兮，吾将上下而求索」，读书时抄在桌角的那句。',
        '香草美人的整套比喻，后世文人借了两千年。',
        '太长，但读到「亦余心之所善兮，虽九死其犹未悔」还是会停一下。',
    ],
    30: [  # 满江红
        '「三十功名尘与土，八千里路云和月」，两句把一生说完了。',
        '「莫等闲，白了少年头，空悲切」，中学时当口号，现在当提醒。',
        '气势一路压下来，结尾「朝天阙」反而让人心里一沉。',
    ],
    2: [  # 黄鹤楼送孟浩然之广陵
        '全诗不写一句舍不得，只写帆影越来越小。',
        '「唯见长江天际流」——看得越久，越显得人已经走了。',
    ],
    13: [  # 春夜喜雨
        '「随风潜入夜，润物细无声」，现在常用来形容老师，其实原意就是写雨。',
        '通篇没有一个「喜」字，读完却觉得满心欢喜。',
        '「花重锦官城」的「重」字，是雨水的重量。',
    ],
    15: [  # 江雪
        '千山万径都清空，只为留一个人在江上。',
        '「独钓寒江雪」，冷到极处反而是种倔强。',
    ],
    23: [  # 观沧海
        '「日月之行，若出其中」，曹操的气魄不是吹出来的。',
        '写海却不写浪，写的是吞吐日月的那种静。',
    ],
    42: [  # 饮酒·其五
        '「采菊东篱下，悠然见南山」，最舒服的一句诗。',
        '「此中有真意，欲辨已忘言」，说得出就不叫真意了。',
    ],
    47: [  # 望庐山瀑布
        '「疑是银河落九天」，小学背的时候觉得夸张，去了庐山才知道不算夸张。',
        '一个「挂」字，瀑布就定在眼前了。',
    ],
    53: [  # 行路难
        '前面写得越堵，最后「长风破浪会有时」越痛快。',
        '「停杯投箸不能食，拔剑四顾心茫然」，这种烦躁写得很现代。',
    ],
    54: [  # 春望
        '「感时花溅泪，恨别鸟惊心」，花鸟本来无辜，是人在痛。',
        '「家书抵万金」不是修辞，战乱里就是这样。',
        '满头白发搔得更短，插不住簪子——细节比抒情更狠。',
    ],
    57: [  # 登高
        '八句全对仗，读起来却像一口气说完的。',
        '「无边落木萧萧下，不尽长江滚滚来」，空间和时间一起压过来。',
        '「万里悲秋常作客，百年多病独登台」，十四个字写了六层苦。',
    ],
    80: [  # 登鹳雀楼
        '前两句是眼睛，后两句是心。',
        '「更上一层楼」现在成了口头语，原句其实很朴素。',
    ],
    93: [  # 青玉案·元夕
        '写热闹写到极处，最后把人放在「灯火阑珊处」。',
        '「众里寻他千百度」被引得太多次，但每次读到还是会被击中。',
    ],
    3: [  # 念奴娇·赤壁怀古
        '「大江东去」四个字起手，气就压不住了。',
        '周瑜越英发，苏轼越显老，「多情应笑我」是自嘲里带刺。',
    ],
    9: [  # 子衿
        '「青青子衿，悠悠我心」，曹操后来直接借去写求贤。',
        '「一日不见，如三月兮」，时间在想念的人那里是不准的。',
    ],
    14: [  # 清明
        '「路上行人欲断魂」，短短七个字写出了整个节气的情绪。',
        '末句牧童一指，画面就停在杏花深处，不往下写了。',
    ],
    16: [  # 声声慢
        '开头十四个叠字，念出来就是一个人在屋里来回走。',
        '「梧桐更兼细雨，到黄昏、点点滴滴」，雨声落得太慢。',
    ],
    22: [  # 九歌·国殇
        '「身既死兮神以灵，魂魄毅兮为鬼雄」，写得比任何战歌都硬。',
        '全篇没有哭，读完却难受。',
    ],
    24: [  # 短歌行
        '「对酒当歌，人生几何」，一开头就把时间摆出来。',
        '「周公吐哺，天下归心」，前面所有的愁都是为这几句垫的。',
    ],
    41: [  # 龟虽寿
        '「老骥伏枥，志在千里」，写这句时曹操已经五十三岁。',
        '承认天命，又不服天命，这才是这首诗的劲。',
    ],
    40: [  # 硕鼠
        '「逝将去女，适彼乐土」，最早的移民宣言。',
        '三段递进，从「黍」到「麦」到「苗」，被吃干抹净的过程。',
    ],
}

AUTHOR_UIDS = (1, 2, 5, 6, 9, 13)  # 可选的作者账号（取 users 表里已有的 uid，避免出现不存在的用户）

BASE_DATE = datetime.datetime(2026, 10, 12, 9, 30, 0)  # 评论时间从这里开始按天递增，保证列表里顺序自然


def main(argv: list[str] | None = None) -> int:
    """把示例书评写入 discuss 表，并回写 commentscount。

    Args:
        argv: 命令行参数，支持 --dry-run。

    Returns:
        进程退出码：0 成功，1 有错误。
    """
    parser = argparse.ArgumentParser(description='导入示例书评并校准评论数')
    parser.add_argument('--dry-run', action='store_true', help='只统计，不写库')
    args = parser.parse_args(argv)

    total = sum(len(v) for v in DISCUSS_SEED.values())
    print(f'待写入书评 {total} 条，覆盖 {len(DISCUSS_SEED)} 部作品')
    if args.dry_run:
        for cid, comments in DISCUSS_SEED.items():
            print(f'  cid={cid}: {len(comments)} 条')
        return 0

    from app import create_app, db
    from app.model.models import Classics, Discuss

    random.seed(20261022)  # 固定随机序列，重复执行结果一致
    app = create_app()
    with app.app_context():
        added = 0
        skipped = 0
        for cid, comments in DISCUSS_SEED.items():
            for index, text in enumerate(comments):
                exists = Discuss.query.filter_by(cid=cid, comment=text).first()
                if exists:
                    skipped += 1
                    continue
                db.session.add(Discuss(
                    uid=AUTHOR_UIDS[(cid + index) % len(AUTHOR_UIDS)],
                    cid=cid,
                    comment=text,
                    cdate=BASE_DATE + datetime.timedelta(days=cid % 10, hours=index * 3),
                    topcount=random.randint(0, 8),
                    lowcount=random.randint(0, 2),
                ))
                added += 1
        db.session.commit()

        # 校准：commentscount 一律等于 discuss 表真实条数，
        fixed = 0  # 否则详情页会出现「显示 N 条、列表却是空」的尴尬
        for classic in Classics.query.all():
            real = Discuss.query.filter_by(cid=classic.cid).count()
            if classic.commentscount != real:
                classic.commentscount = real
                fixed += 1
        db.session.commit()

        print(f'[完成] 新增书评 {added} 条，跳过 {skipped} 条；校准评论数 {fixed} 部')
        print(f'[统计] discuss 共 {Discuss.query.count()} 条')
    return 0


if __name__ == '__main__':
    sys.exit(main())
