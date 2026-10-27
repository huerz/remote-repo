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

    # 5.更新密码（把存量明文密码升级成哈希时使用）
    def updatePassword(self, uid, upwd_hash):
        try:
            user = Users.query.get(uid)
            if user is None:
                return False
            user.upwd = upwd_hash
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    # 6.修改用户个人信息（教材 8.2.3）
    def updateUserBySelf(self, user):
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            # 查询用户
            user_tmp = Users.query.get(user.uid)
            # 设置用户个人信息修改的字段
            user_tmp.nickname = user.nickname
            user_tmp.avatar = user.avatar
            user_tmp.sex = user.sex
            user_tmp.phone = user.phone
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
        return flag

    # 7. 用户密码重置（教材 8.3.5）
    def updateUserByPwd(self, uid, new_pwd):
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            # 查询用户
            user_tmp = Users.query.get(uid)
            # 设置修改的密码字段
            user_tmp.upwd = new_pwd
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag
