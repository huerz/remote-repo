from app import db
from app.model.models import Classictype, Classics

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
    def updateClassicRating(self, judge):
        flag = True  # 成功标志
        try:
            # 查询文学作品
            classics = Classics.query.get(judge.cid)
            # 设置文学作品星级（取最高评分）
            classics.rating = max(judge.rating, classics.rating)
            # 将评价信息加入文学评价表
            db.session.add(judge)
            db.session.commit()  # 提交至数据库
        except Exception as e:
            flag = False
            print(e)
            db.session.rollback()  # 异常，回滚数据库
        return flag