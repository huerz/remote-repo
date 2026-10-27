from typing import List, Optional

# 使用通用类型（String / Text），MySQL 与 SQLite 都能编译；
# 若写成 dialects.mysql 的 VARCHAR/TEXT，切到 SQLite 会直接报编译错误
from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

# 导入数据库操作对象
from app import db
from app import ma
class Filmtype(db.Model):
    __tablename__ = 'filmtype'
    __table_args__ = {'comment': '电影类型表'}
    tid: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    cover: Mapped[Optional[str]] = mapped_column(String(200))
    remark: Mapped[Optional[str]] = mapped_column(String(500))
class FilmtypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Filmtype
        fields = ("tid", "name", "cover", "remark") # 序列化的字段
class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'comment': '用户表'}
    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    uname: Mapped[str] = mapped_column(String(100))
    # 存 werkzeug 的加盐哈希（形如 scrypt:32768:8:1$...），长度约 160 字符，
    # 原来的 String(100) 装不下，必须放到 255
    upwd: Mapped[str] = mapped_column(String(255))
    nickname: Mapped[Optional[str]] = mapped_column(String(100))
    
    avatar: Mapped[Optional[str]] = mapped_column(String(200))
    sex: Mapped[Optional[str]] = mapped_column(String(50))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    remark: Mapped[Optional[str]] = mapped_column(String(200))
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        # 注意：不要把 upwd 放进序列化字段，否则接口会把密码明文返回给前端
        fields = ("uid", "uname", "nickname", "avatar", "sex", "phone",
"remark")
class Films(db.Model):
    __tablename__ = 'films'
    __table_args__ = {'comment': '电影表'}
    cid: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    tid: Mapped[int] = mapped_column(Integer, comment='电影类型编号')
    cover: Mapped[Optional[str]] = mapped_column(String(200))
    year: Mapped[Optional[str]] = mapped_column(String(50))
    author: Mapped[Optional[str]] = mapped_column(String(200))
    present: Mapped[Optional[str]] = mapped_column(String(100))
    describes: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    commentscount: Mapped[Optional[int]] = mapped_column(Integer)
class FilmsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Films
        fields = ("cid", "title", "tid", "cover", "year", "author", "present",
"describes", "rating", "commentscount")
class Filmjudges(db.Model):
    __tablename__ = 'filmjudges'
    __table_args__ = {'comment': '电影评价表'}
    cjid: Mapped[int] = mapped_column(Integer, primary_key=True)
    cid: Mapped[int] = mapped_column(Integer)
    uid: Mapped[int] = mapped_column(Integer)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    jdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
class FilmjudgesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Filmjudges
        fields = ("cjid", "cid", "uid", "rating", "jdate")
class Discuss(db.Model):
    __tablename__ = 'discuss'
    __table_args__ = {'comment': '影评表'}
    did: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[int] = mapped_column(Integer)
    cid: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text)
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