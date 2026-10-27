# ============================================================================
# 用户数据访问层（DAO）
# ----------------------------------------------------------------------------
# 作用：用户注册、按账号/编号查询、改密等数据库操作。
# 教材：第六章 §6.3.1 注册、登录、按账号/编号查询（用户中心基础功能）
#       第八章新增三处：§8.3.2 头像上传、§8.3.3 信息修改、§8.3.5 密码重置
# 约定：密码只在 DAO 里做哈希与校验，蓝图不接触明文。
# ============================================================================
from app import db
from app.model.models import Users

# 数据库操作类
class UsersDao:
    def __init__(self):
        print("UsersDao is running")

    def addUser(self, user):  # 1.增加一个用户
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
    def existsByUname(self, uname):  # 所以必须在业务层查重，否则同一账号可以重复注册
        user = Users.query.filter(Users.uname == uname).first()
        return user is not None

    def getUserByUname(self, uname):  # 3.按账号查询用户对象（登录校验用，查不到返回 None）
        user = Users.query.filter(Users.uname == uname).first()
        return user

    def getUserByUid(self, uid):  # 4.通过用户编号查询用户（教材 6.2 查询用户信息）
        try:
            user = Users.query.get(uid)  # 查询
            return user
        except Exception as e:
            print(e)
            pass

    def updatePassword(self, uid, upwd_hash):  # 5.更新密码（把存量明文密码升级成哈希时使用）
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

    def updateUserBySelf(self, user):  # 6.修改用户个人信息（教材 8.2.3）
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            user_tmp = Users.query.get(user.uid)  # 查询用户
            user_tmp.nickname = user.nickname  # 设置用户个人信息修改的字段
            user_tmp.avatar = user.avatar
            user_tmp.sex = user.sex
            user_tmp.phone = user.phone
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
        return flag

    def updateUserByPwd(self, uid, new_pwd):  # 7. 用户密码重置（教材 8.3.5）
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            user_tmp = Users.query.get(uid)  # 查询用户
            user_tmp.upwd = new_pwd  # 设置修改的密码字段
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag
