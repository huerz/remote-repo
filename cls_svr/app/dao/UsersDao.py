from app import db
from app.model.models import Users

# 数据库操作类
class UsersDao:
    def __init__(self):
        print("UsersDao is running")

    # 1.增加一个用户
    def addUser(self, user):
        flag = True  # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        try:
            db.session.add(user)
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
        return flag

    # 2.按账号查询用户是否已存在（注册前查重）
    #   说明：users 表主键是自增 uid，uname 没有唯一约束，
    #   所以必须在业务层查重，否则同一账号可以重复注册
    def existsByUname(self, uname):
        user = Users.query.filter(Users.uname == uname).first()
        return user is not None

    # 3.按账号查询用户对象（登录校验用，查不到返回 None）
    def getUserByUname(self, uname):
        user = Users.query.filter(Users.uname == uname).first()
        return user

    # 4.通过用户编号查询用户（教材 6.2 查询用户信息）
    def getUserByUid(self, uid):
        try:
            # 查询
            user = Users.query.get(uid)
            return user
        except Exception as e:
            print(e)
            pass
