from typing import List, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, Text, text
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

# 导入数据库操作对象
from app import db
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
    upwd: Mapped[str] = mapped_column(VARCHAR(100))
    nickname: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    
    avatar: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    sex: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    remark: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        # 注意：不要把 upwd 放进序列化字段，否则接口会把密码明文返回给前端
        fields = ("uid", "uname", "nickname", "avatar", "sex", "phone",
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
class ClassicsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classics
        fields = ("cid", "title", "tid", "cover", "year", "author", "present",
"describes", "rating", "commentscount")
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