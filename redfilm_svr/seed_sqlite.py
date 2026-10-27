# -*- coding: utf-8 -*-
"""
把 redfilmdbs.sql 里的建表与数据灌进 SQLite 兜底库（redfilmdbs.db）。
只在 MySQL 不可用时需要；重复运行不会重复插入。
"""
import os
import re

from sqlalchemy import text

from app import create_app, db
from app.model.models import Filmtype

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(BASE_DIR, 'redfilmdbs.sql')

app = create_app()

with app.app_context():
    # 1. 建表（用 models，SQLite 会自动适配）
    db.create_all()

    # 2. 已有数据就跳过
    if Filmtype.query.count() > 0:
        print('已存在数据，跳过。类型数 =', Filmtype.query.count())
    else:
        raw = open(SQL_FILE, encoding='utf-8').read()
        # 只取 INSERT 语句，建表语句交给 models
        statements = re.findall(r'INSERT INTO[\s\S]*?;', raw)
        for stmt in statements:
            db.session.execute(text(stmt.rstrip(';')))
        db.session.commit()
        print('导入完成：类型', Filmtype.query.count())

    # 3. 汇报
    from app.model.models import Films, Users, Discuss
    print('  类型:', Filmtype.query.count())
    print('  电影:', Films.query.count())
    print('  用户:', Users.query.count())
    print('  影评:', Discuss.query.count())
