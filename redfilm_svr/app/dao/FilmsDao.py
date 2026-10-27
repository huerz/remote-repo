from app import db
from app.model.models import Filmtype, Films, Discuss
from app.model.models import Filmjudges, Discussjudges

# 数据库操作类
class FilmsDao:
    def __init__(self):
        print("FilmsDao is running")
    # 1. 获取电影类型列表
    def getFilmtypes(self):
        try:
            # 获取所有电影类型
            filmtypes = Filmtype.query.all()
            return filmtypes
        except Exception as e:
            print(e)
            pass

    # 2. 获取首页轮播图数据（按评分倒序取前 number 条；只取有封面的电影）
    def getCarousels(self, number):
        try:
            carousels = Films.query.filter(
                Films.cover.isnot(None), Films.cover != ''
            ).order_by(
                Films.rating.desc(), Films.cid.asc()
            ).limit(number).all()
            return carousels
        except Exception as e:
            print(e)
            pass

    # 3. 按关键字检索电影电影（标题 / 作者 / 类型名 模糊匹配；关键字为空则返回全部）
    def searchFilms(self, keyword):
        try:
            if keyword is None:
                keyword = ''
            # 转义 LIKE 的通配符：否则用户输入 % 会命中全部、输入 _ 会匹配任意单字符
            safe = keyword.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
            like_value = '%' + safe + '%'
            films = Films.query.join(
                Filmtype, Films.tid == Filmtype.tid
            ).filter(
                db.or_(Films.title.like(like_value, escape='\\'),
                       Films.author.like(like_value, escape='\\'),
                       Filmtype.name.like(like_value, escape='\\'))
            ).order_by(Films.rating.desc(), Films.cid.asc()).all()
            return films
        except Exception as e:
            print(e)
            pass

    # 4. 按类型编号查询电影类型（教材 6.3.3）
    def getFilmtypeByTid(self, tid):
        try:
            filmtype = Filmtype.query.get(tid)
            return filmtype
        except Exception as e:
            print(e)
            pass

    # 5. 获取某电影类型下的电影列表（教材 6.3.3，按星级评分从高到低）
    def getFilmsByTid(self, tid):
        try:
            films = Films.query.filter(Films.tid == tid) \
                .order_by(Films.rating.desc()).all()
            return films
        except Exception as e:
            print(e)
            pass

    # 5-1. 获取某电影类型下评分最高的前 number 部电影（首页电影推荐用，教材 3.3.5）
    def getFilmsByTidLimit(self, tid, number):
        try:
            films = Films.query.filter(Films.tid == tid) \
                .order_by(Films.rating.desc(), Films.cid.asc()) \
                .limit(number).all()
            return films
        except Exception as e:
            print(e)
            pass

    # 6. 按电影编号查询电影电影（教材 6.3.4）
    def getFilmsByCid(self, cid):
        try:
            classic = Films.query.get(cid)
            return classic
        except Exception as e:
            print(e)
            pass

    # 7. 评价电影电影（教材 6.3.5）
    def updateFilmRating(self, judge):
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            # 查询电影电影
            classic = Films.query.get(judge.cid)
            # 设置电影电影星级评价（取最高评价）
            classic.rating = max(judge.rating, classic.rating)
            # 将评价信息插入电影电影评价表
            db.session.add(judge)
            # 提交至数据库
            db.session.commit()
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag

    # 8. 获取某电影电影的评论列表（教材 7.3.1）
    #    按评论时间从高到低排序，最新的影评排在最前面
    def getDiscussByCid(self, cid):
        try:
            discuss = Discuss.query.filter(Discuss.cid == cid) \
                .order_by(Discuss.cdate.desc()).all()
            return discuss
        except Exception as e:
            print(e)
            pass

    # 9. 发表影评（教材 7.3.2）
    def addDiscuss(self, discuss):
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            # 查询对应的电影电影
            classic = Films.query.get(discuss.cid)
            # 设置电影电影的评论数量（加 1）
            classic.commentscount = classic.commentscount + 1
            # 将评论插入影评表
            db.session.add(discuss)
            # 提交至数据库
            db.session.commit()
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag

    # 10. 评价影评（教材 7.3.3）
    def updateDiscussTopLow(self, judge):
        # 成功标志。此处 flag 的值为 True 表示操作成功，为 False 表示操作失败
        flag = True
        try:
            # 查询影评信息
            dis = Discuss.query.get(judge.did)
            # 设置影评的顶、踩的数量
            if judge.toplow == 1:
                dis.topcount = dis.topcount + 1
            else:
                dis.lowcount = dis.lowcount + 1
            # 将评价信息插入评论评价表
            db.session.add(judge)
            # 提交至数据库
            db.session.commit()
        except Exception as e:
            flag = False
            db.session.rollback()  # 异常，回滚数据库
            pass
        return flag

    # 12. 获取登录用户的影评数据（教材 8.3.4）
    def getDiscussesByUid(self, uid):
        try:
            # 排序查询：按评论时间从高到低排序
            discuss = Discuss.query.filter(Discuss.uid == uid) \
                .order_by(Discuss.cdate.desc()).all()
            return discuss
        except Exception as e:
            print(e)
            pass