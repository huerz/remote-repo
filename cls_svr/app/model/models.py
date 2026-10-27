# ============================================================================
# ORM 模型与序列化器
# ----------------------------------------------------------------------------
# 作用：数据库表的 Python 映射（classictype / classics / users / discuss / poem 等）
#       以及每个模型对应的 Marshmallow 序列化字段白名单。
# 约定：新增字段要同时改「模型列 + Schema.fields」，否则接口里读不到；
#       序列化字段里禁止出现密码等敏感列。
# ============================================================================
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, Text, text
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

from app import db  # 导入数据库操作对象
from app import ma
class Classictype(db.Model):
    __tablename__ = 'classictype'
    __table_args__ = {'comment': '文学作品类型表'}
    tid: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100))
    cover: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    remark: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
class ClassictypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classictype
        fields = ("tid", "name", "cover", "remark") # 序列化的字段
class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'comment': '用户表'}
    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    uname: Mapped[str] = mapped_column(VARCHAR(100))
    # 存 werkzeug 的加盐哈希（形如 scrypt:32768:8:1$...），长度约 160 字符，
    upwd: Mapped[str] = mapped_column(VARCHAR(255))  # 原来的 VARCHAR(100) 装不下，必须放到 255
    nickname: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    
    avatar: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    sex: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    remark: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        fields = ("uid", "uname", "nickname", "avatar", "sex", "phone",  # 注意：不要把 upwd 放进序列化字段，否则接口会把密码明文返回给前端
"remark")
class Classics(db.Model):
    __tablename__ = 'classics'
    __table_args__ = {'comment': '文学表'}
    cid: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(200))
    tid: Mapped[int] = mapped_column(Integer, comment='文学作品类型编号')
    cover: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    year: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    author: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    present: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    describes: Mapped[Optional[str]] = mapped_column(TEXT)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    commentscount: Mapped[Optional[int]] = mapped_column(Integer)
    summary: Mapped[Optional[str]] = mapped_column(VARCHAR(500))  # 内容简介：详情页左侧「书籍信息」里的主要内容，2026-10-23 新增
class ClassicsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classics
        fields = ("cid", "title", "tid", "cover", "year", "author", "present",
"describes", "rating", "commentscount", "summary")
class Classicjudges(db.Model):
    __tablename__ = 'classicjudges'
    __table_args__ = {'comment': '文学评价表'}
    cjid: Mapped[int] = mapped_column(Integer, primary_key=True)
    cid: Mapped[int] = mapped_column(Integer)
    uid: Mapped[int] = mapped_column(Integer)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    jdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
class ClassicjudgesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classicjudges
        fields = ("cjid", "cid", "uid", "rating", "jdate")
class Discuss(db.Model):
    __tablename__ = 'discuss'
    __table_args__ = {'comment': '文学评论表'}
    did: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[int] = mapped_column(Integer)
    cid: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(TEXT)
    cdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    topcount: Mapped[Optional[int]] = mapped_column(Integer)
    lowcount: Mapped[Optional[int]] = mapped_column(Integer)
class DiscussSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discuss
        fields = ("did", "uid", "cid", "comment", "cdate", "topcount", "lowcount")
class Discussjudges(db.Model):
    __tablename__ = 'discussjudges'
    __table_args__ = {'comment': '评论评价表'}
    djid: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[int] = mapped_column(Integer)
    did: Mapped[int] = mapped_column(Integer)
    toplow: Mapped[Optional[int]] = mapped_column(Integer)
    jdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
class DiscussjudgesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discussjudges
        fields = ("djid", "uid", "did", "toplow", "jdate")

# ============================================================================
# 诗词数据表（唐诗 / 宋词 / 元曲 / 清诗，数据源 app/data/poems/*.json）
# ----------------------------------------------------------------------------
# 字段按课程设计需求设计；cover 是本项目额外加的，用来存封面图文件名
# （图片放在 D:/高级网页设计/images/books/<分类>/ 下，接口按文件名取）
# 建表与灌数据：在 cls_svr 目录执行 .venv\Scripts\python.exe scripts\seed_poems.py
# ============================================================================
class Poem(db.Model):
    """诗词数据表（唐诗 / 宋词 / 元曲 / 清诗）。

    数据源是人工维护的 JSON（app/data/poems/*.json），通过 seed_poems.py 灌入；
    接口层只读这张表，不直接读 JSON，保证线上不依赖文件系统。

    Attributes:
        id: 主键，自增。
        title: 标题，如「静夜思」。
        author: 作者，如「李白」。
        dynasty: 朝代，取值唐 / 宋 / 元 / 清（用于列表页筛选）。
        genre: 体裁，取值诗 / 词 / 曲。
        content: 原文，句中用换行分隔，前端用 white-space: pre-line 还原。
        translation: 白话译文。
        note: 注释，用 ①②③ 编号。
        appreciate: 赏析。
        tag: 标签，单值，取值豪放 / 婉约 / 山水 / 爱国 / 田园 / 边塞 / 咏史 等。
        cover: 封面图文件名（不含路径），对应 images/books/<分类>/，可空。
    """
    __tablename__ = 'poem'
    __table_args__ = {'comment': '诗词数据表'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, comment='标题')
    author = db.Column(db.String(64), nullable=False, comment='作者')
    dynasty = db.Column(db.String(16), nullable=False, comment='朝代：唐/宋/元/清')
    genre = db.Column(db.String(16), comment='体裁：诗/词/曲')
    content = db.Column(db.Text, nullable=False, comment='原文')
    translation = db.Column(db.Text, comment='白话译文')
    note = db.Column(db.Text, comment='注释')
    appreciate = db.Column(db.Text, comment='赏析')
    tag = db.Column(db.String(64), comment='标签：豪放/婉约/山水/爱国/田园/边塞/咏史')
    cover = db.Column(db.String(200), comment='封面图文件名，可空')


class PoemSchema(ma.SQLAlchemyAutoSchema):
    """Poem 的序列化器。

    注意：只暴露接口需要的字段，不返回任何内部字段；
    新增列时记得同步 fields，否则接口里拿不到。
    """

    class Meta:
        model = Poem
        fields = ("id", "title", "author", "dynasty", "genre", "content",
                  "translation", "note", "appreciate", "tag", "cover")
