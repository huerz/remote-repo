# ============================================================================
# 诗词数据导入脚本：app/data/poems/*.json → MySQL（表名 poem）
# ----------------------------------------------------------------------------
# 作用：把人工维护的 JSON 数据源灌进数据库，是数据源与接口之间唯一的写入口。
#       JSON 改了只需重跑本脚本，不必手写 SQL。
# 用法（在 cls_svr 目录下执行）：
#   .venv\Scripts\python.exe scripts\seed_poems.py           只补新增，已在库里的跳过
#   .venv\Scripts\python.exe scripts\seed_poems.py --reset   先清空 poem 表再全量导入
#   .venv\Scripts\python.exe scripts\seed_poems.py --dry-run 只校验 JSON，不连数据库
# 依赖：app/model/models.py 的 Poem 模型、app/conf/dbconfig.py 的数据库连接、
#       app/data/poems/{tang,song,yuan,qing}.json
# 约定：
#   1) 去重键 = 标题 + 作者 + 朝代，重复导入不会产生脏数据（可反复执行）
#   2) JSON 出现未知字段直接报错，避免字段名写错却悄悄丢数据
#   3) 空字符串统一转 None，数据库里不出现 "" 与 NULL 两种空值
# ============================================================================
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

# 本脚本位于 cls_svr/scripts/，项目根目录是上一级。
# 把项目根加入模块搜索路径，才能 import 到 app 包（否则只能从 cls_svr 目录执行才碰巧成功）。
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / 'app' / 'data' / 'poems'  # JSON 目录：<项目根>/app/data/poems，不依赖当前工作目录

DATA_FILES = ('tang.json', 'song.json', 'yuan.json', 'qing.json')  # 每个朝代一个文件，按固定顺序读取（顺序只影响导入先后，不影响去重）

FIELDS = ('title', 'author', 'dynasty', 'genre', 'content',  # 与 Poem 模型字段一一对应；cover 可空，其余按需可为空
          'translation', 'note', 'appreciate', 'tag', 'cover')

REQUIRED = ('title', 'author', 'dynasty', 'content')  # 缺任何一项都不允许入库

PoemDict = dict[str, Any]  # 单条数据的类型别名，便于阅读与后续类型检查


def load_poems(data_dir: pathlib.Path = DATA_DIR) -> tuple[list[PoemDict], list[str]]:
    """读取并校验全部诗词 JSON。

    Args:
        data_dir: JSON 所在目录。文件不存在时跳过并提示，不算错误。

    Returns:
        (诗词列表, 错误信息列表)。错误列表非空时调用方应终止导入，
        这样一次就能看到全部问题，而不是改一条跑一次。

    Raises:
        FileNotFoundError: 目录本身不存在（属于配置错误，不静默）。
    """
    if not data_dir.exists():
        raise FileNotFoundError(f'数据目录不存在：{data_dir}')

    poems: list[PoemDict] = []
    errors: list[str] = []

    for name in DATA_FILES:
        path = data_dir / name
        if not path.exists():
            print(f'[跳过] {name} 不存在')
            continue

        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            errors.append(f'{name} JSON 格式错误：{exc}')
            continue

        if not isinstance(data, list):
            errors.append(f'{name} 顶层必须是数组')
            continue

        for index, item in enumerate(data):
            where = f'{name}[{index}]'
            if not isinstance(item, dict):
                errors.append(f'{where} 不是对象')
                continue

            unknown = set(item) - set(FIELDS)  # 字段名写错时应当立刻发现，而不是被模型静默忽略
            if unknown:
                errors.append(f'{where} 含未知字段 {sorted(unknown)}')

            for key in REQUIRED:
                if not str(item.get(key) or '').strip():
                    errors.append(f'{where} 缺少必填字段 {key}')

            poems.append(item)

    return poems, errors


def find_duplicates(poems: list[PoemDict]) -> list[tuple[str, str, str]]:
    """找出同一份数据内「标题 + 作者 + 朝代」重复的条目。

    Args:
        poems: load_poems 返回的列表。

    Returns:
        重复键的列表；只用于提示，不影响入库（入库时会逐个查库跳过）。
    """
    seen: set[tuple[str, str, str]] = set()
    duplicates: list[tuple[str, str, str]] = []
    for poem in poems:
        key = (str(poem.get('title')), str(poem.get('author')), str(poem.get('dynasty')))
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    return duplicates


def count_by_dynasty(poems: list[PoemDict]) -> dict[str, int]:
    """按朝代统计条数，用于导入前的体量核对。

    Args:
        poems: load_poems 返回的列表。

    Returns:
        形如 {'唐': 237, '宋': 218} 的映射。
    """
    stat: dict[str, int] = {}
    for poem in poems:
        dynasty = str(poem.get('dynasty') or '?')
        stat[dynasty] = stat.get(dynasty, 0) + 1
    return stat


def import_to_db(poems: list[PoemDict], reset: bool = False) -> None:
    """把校验通过的数据写入数据库。

    Args:
        poems: 已通过校验的诗词列表。
        reset: True 时先清空 poem 表；False 时只补新增。

    Raises:
        sqlalchemy.exc.SQLAlchemyError: 数据库连接或写入失败，由调用方决定退出码。
    """
    from app import create_app, db  # 延迟导入：--dry-run 时不需要连数据库（也避免无库环境跑不起来）
    from app.model.models import Poem

    app = create_app()
    with app.app_context():
        db.create_all()  # 已存在的表不会被改动，只补建缺失的 poem 表

        if reset:
            deleted = db.session.query(Poem).delete()
            db.session.commit()
            print(f'[重置] 已清空 poem 表（{deleted} 条）')

        added = 0
        skipped = 0
        for item in poems:
            exists = Poem.query.filter_by(
                title=item['title'],
                author=item['author'],
                dynasty=item['dynasty']
            ).first()
            if exists:
                skipped += 1
                continue

            row = {key: (item.get(key) or None) for key in FIELDS}  # 只取模型里存在的字段；空串统一成 None，避免 "" 与 NULL 混用
            db.session.add(Poem(**row))
            added += 1

        db.session.commit()
        print(f'[完成] 新增 {added} 条，跳过 {skipped} 条，表内现有 {Poem.query.count()} 条')


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。

    Args:
        argv: 参数列表，默认取 sys.argv[1:]，便于单测传入。

    Returns:
        含 reset / dry_run 两个布尔开关的命名空间。
    """
    parser = argparse.ArgumentParser(description='导入诗词 JSON 到 MySQL')
    parser.add_argument('--reset', action='store_true', help='先清空 poem 表')
    parser.add_argument('--dry-run', action='store_true', help='只校验，不写库')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """脚本入口：校验 → 统计 → 入库。

    Args:
        argv: 透传给 parse_args，便于测试。

    Returns:
        进程退出码：0 成功，1 数据有错（便于 CI 或批处理判断）。
    """
    args = parse_args(argv)

    try:
        poems, errors = load_poems()
    except FileNotFoundError as exc:
        print(f'[错误] {exc}')
        return 1

    stat = count_by_dynasty(poems)
    print('读到 %d 首：%s' % (len(poems), '，'.join(f'{k} {v}' for k, v in stat.items())))

    duplicates = find_duplicates(poems)
    if duplicates:
        print(f'[警告] 有 {len(duplicates)} 组标题+作者+朝代重复：')
        for key in duplicates[:20]:
            print('   ', key)

    if errors:
        print(f'[错误] 共 {len(errors)} 处：')
        for error in errors[:40]:
            print('   ', error)
        if len(errors) > 40:
            print('    ...')
        return 1

    if args.dry_run:
        print('[dry-run] 校验通过，未写数据库')
        return 0

    import_to_db(poems, reset=args.reset)
    return 0


if __name__ == '__main__':
    sys.exit(main())
