# ============================================================================
# 文学数据访问层（DAO）
# ----------------------------------------------------------------------------
# 作用：把 SQLAlchemy 查询收在一处，蓝图只调方法、不写查询语句。
# 教材：第六章 §6.3 评分与顶/踩（基础）
#       第七章新增 §7.3.1 书评展示 / §7.3.2 书评发表 / §7.3.3 书评评价（p204–221）
# 约定：方法编号与 classics_blueprint.py 顶部的接口清单对应；
#       异常只打印不抛出，返回 None 由上层判断（沿用教材写法）。
# ============================================================================
from app import db
from app.model.models import Classictype, Classics, Discuss
from app.model.models import Classicjudges, Discussjudges

# 数据库操作类
class ClassicsDao:
    def __init__(self):
        print("ClassicsDao is running")
    def getClassictypes(self):  # 1. 获取文学作品类型列表
        try:
            classictypes = Classictype.query.all()  # 获取所有文学作品类型
            return classictypes
        except Exception as e:
            print(e)
            pass

    def getCarousels(self, number):  # 2. 获取首页轮播图数据（按评分倒序取前 number 条；只取有封面的作品）
        try:
            carousels = Classics.query.filter(
                Classics.cover.isnot(None), Classics.cover != ''
            ).order_by(
                Classics.rating.desc(), Classics.cid.asc()
            ).limit(number).all()
            return carousels
        except Exception as e:
            print(e)
            pass

    # 3. 按关键字检索文学作品（标题 / 作者 / 类型名 模糊匹配；关键字为空则返回全部）
    def searchClassics(self, keyword):
        try:
            if keyword is None:
                keyword = ''
            # 转义 LIKE 的通配符：否则用户输入 % 会命中全部、输入 _ 会匹配任意单字符
            safe = keyword.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
            like_value = '%' + safe + '%'
            classics = Classics.query.join(
                Classictype, Classics.tid == Classictype.tid
            ).filter(
                db.or_(Classics.title.like(like_value, escape='\\'),
                       Classics.author.like(like_value, escape='\\'),
                       Classictype.name.like(like_value, escape='\\'))
            ).order_by(Classics.rating.desc(), Classics.cid.asc()).all()
            return classics
        except Exception as e:
            print(e)
            pass

    def getClassictypeByTid(self, tid):  # 4. 按类型编号查询文学作品类型（教材 6.3.3）
        try:
            classictype = Classictype.query.get(tid)
            return classictype
        except Exception as e:
            print(e)
            pass

    def getClassicsByTid(self, tid):  # 5. 获取某文学作品类型下的文学列表（教材 6.3.3，按星级评分从高到低）
        try:
            classics = Classics.query.filter(Classics.tid == tid) \
                .order_by(Classics.rating.desc()).all()
            return classics
        except Exception as e:
            print(e)
            pass

    # 5-1. 获取某文学作品类型下评分最高的前 number 部作品（首页文学推荐用，教材 3.3.5）
    def getClassicsByTidLimit(self, tid, number):
        try:
            classics = Classics.query.filter(Classics.tid == tid) \
                .order_by(Classics.rating.desc(), Classics.cid.asc()) \
                .limit(number).all()
            return classics
        except Exception as e:
            print(e)
            pass

    def getClassicsByCid(self, cid):  # 6. 按作品编号查询文学作品（教材 6.3.4）
        try:
            classic = Classics.query.get(cid)
            return classic
        except Exception as e:
            print(e)
            pass

    def updateClassicRating(self, judge):  # 7. 评价文学作品（教材 6.3.5）
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            classic = Classics.query.get(judge.cid)  # 查询文学作品
            if classic is None:  # 作品不存在，直接判失败，避免对 None 取属性
                return False
            # 两个评分字段都可能为 NULL，先 or 0 兜底，再取较高分
            classic.rating = max(judge.rating or 0, classic.rating or 0)  # 设置文学作品星级评价（取最高评价）
            db.session.add(judge)  # 将评价信息插入文学作品评价表
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag

    # 8. 获取某文学作品的评论列表（教材 7.3.1）
    def getDiscussByCid(self, cid):  # 按评论时间从高到低排序，最新的书评排在最前面
        try:
            discuss = Discuss.query.filter(Discuss.cid == cid) \
                .order_by(Discuss.cdate.desc()).all()
            return discuss
        except Exception as e:
            print(e)
            pass

    def addDiscuss(self, discuss):  # 9. 发表文学评论（教材 7.3.2）
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            classic = Classics.query.get(discuss.cid)  # 查询对应的文学作品
            if classic is None:  # 作品不存在，直接判失败，避免对 None 取属性
                return False
            classic.commentscount = (classic.commentscount or 0) + 1  # 设置文学作品的评论数量（加 1）
            db.session.add(discuss)  # 将评论插入文学评论表
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag

    def updateDiscussTopLow(self, judge):  # 10. 评价书评（教材 7.3.3）
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            dis = Discuss.query.get(judge.did)  # 查询书评信息
            if dis is None:  # 书评不存在，直接判失败，避免对 None 取属性
                return False
            # 设置书评的顶、踩的数量
            if judge.toplow == 1:
                dis.topcount = (dis.topcount or 0) + 1
            else:
                dis.lowcount = (dis.lowcount or 0) + 1
            db.session.add(judge)  # 将评价信息插入评论评价表
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag

    def getDiscussesByUid(self, uid):  # 12. 获取登录用户的书评数据（教材 8.3.4）
        try:
            # 排序查询：按评论时间从高到低排序
            discuss = Discuss.query.filter(Discuss.uid == uid) \
                .order_by(Discuss.cdate.desc()).all()
            return discuss
        except Exception as e:
            print(e)
            pass