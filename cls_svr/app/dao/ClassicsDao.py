from app import db
from app.model.models import Classictype, Classics, Discuss

# 数据库操作类
class ClassicsDao:
    def __init__(self):
        print("ClassicsDao is running")
    # 1. 获取文学作品类型列表
    def getClassictypes(self):
        try:
            # 获取所有文学作品类型
            classictypes = Classictype.query.all()
            return classictypes
        except Exception as e:
            print(e)
            pass

    # 2. 获取首页轮播图数据（按评分倒序取前 number 条；只取有封面的作品）
    def getCarousels(self, number):
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
            like_value = '%' + keyword + '%'
            classics = Classics.query.join(
                Classictype, Classics.tid == Classictype.tid
            ).filter(
                db.or_(Classics.title.like(like_value),
                       Classics.author.like(like_value),
                       Classictype.name.like(like_value))
            ).order_by(Classics.rating.desc(), Classics.cid.asc()).all()
            return classics
        except Exception as e:
            print(e)
            pass

    # 4. 按类型编号查询文学作品类型（教材 6.3.3）
    def getClassictypeByTid(self, tid):
        try:
            classictype = Classictype.query.get(tid)
            return classictype
        except Exception as e:
            print(e)
            pass

    # 5. 获取某文学作品类型下的文学列表（教材 6.3.3，按星级评分从高到低）
    def getClassicsByTid(self, tid):
        try:
            classics = Classics.query.filter(Classics.tid == tid) \
                .order_by(Classics.rating.desc()).all()
            return classics
        except Exception as e:
            print(e)
            pass

    # 6. 按作品编号查询文学作品（教材 6.3.4）
    def getClassicsByCid(self, cid):
        try:
            classic = Classics.query.get(cid)
            return classic
        except Exception as e:
            print(e)
            pass

    # 7. 评价文学作品（教材 6.3.5）
    #    向评价表插入一条记录，并把作品的星级更新为"已有评分与新评分中的较大值"
    #    注意单位：前端提交的是 1~5 星，classics.rating 存的是 0~100 分
    #    （前端展示时 rating/20 换算成 5 星），所以这里必须先 ×20 再比较，
    #    否则 max(5, 90) 永远等于原值，用户的评价等于白打。
    def updateClassicRating(self, judge):
        flag = True  # 成功标志
        try:
            # 查询文学作品
            classics = Classics.query.get(judge.cid)
            # 星级换算成百分制
            new_rating = judge.rating * 20
            # 设置文学作品星级（取最高评分）
            classics.rating = max(new_rating, classics.rating or 0)
            # 评价数 +1（前端详情页要展示评价人数）
            classics.commentscount = (classics.commentscount or 0) + 1
            # 将评价信息加入文学评价表
            db.session.add(judge)
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            print(e)
            db.session.rollback()  # 异常，回滚数据库
        return flag

    # 8. 获取某文学作品的评论列表（教材 7.3.1）
    #    按评论时间从高到低排序，最新的书评排在最前面
    def getDiscussByCid(self, cid):
        try:
            discuss = Discuss.query.filter(Discuss.cid == cid) \
                .order_by(Discuss.cdate.desc()).all()
            return discuss
        except Exception as e:
            print(e)
            pass

    # 9. 发表文学评论（教材 7.3.2）
    #    向评论表插入一条记录，并把作品的评论数 +1
    def addDiscuss(self, discuss):
        flag = True  # 成功标志
        try:
            # 查询对应的文学作品
            classic = Classics.query.get(discuss.cid)
            # 设置作品的评论数量 +1
            classic.commentscount = (classic.commentscount or 0) + 1
            # 把评论加入文学评论表
            db.session.add(discuss)
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            print(e)
            db.session.rollback()  # 异常，回滚数据库
        return flag

    # 10. 评价书评（教材 7.3.3）
    #     toplow=1 记「顶」，toplow=0 记「踩」；同时把这条评价写进评论评价表
    #     注意：discuss 的 topcount/lowcount 允许为 NULL，累加前要兜底成 0
    def updateDiscussTopLow(self, judge):
        flag = True  # 成功标志
        try:
            # 查询书评信息
            dis = Discuss.query.get(judge.did)
            # 设置书评的顶、踩的数量
            if judge.toplow == 1:
                dis.topcount = (dis.topcount or 0) + 1
            else:
                dis.lowcount = (dis.lowcount or 0) + 1
            # 将评价信息插入评论评价表
            db.session.add(judge)
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            print(e)
            db.session.rollback()  # 异常，回滚数据库
        return flag