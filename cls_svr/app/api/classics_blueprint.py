# ============================================================================
# 文学作品蓝图（前缀 /api/classics）
# ----------------------------------------------------------------------------
# 作用：类型列表、轮播、推荐、搜索、详情、评分、书评等全部文学相关接口。
# 教材：第六章 §6.3 文学相关接口（列表、详情、评价，本文件的基础）
#       第七章新增 §7.3.1 书评展示（p204）/ §7.3.2 书评发表（p210）/ §7.3.3 书评评价（p216）
# 调用：前端 /svr/api/classics/... → 代理去掉 /svr → 后端 /api/classics/...
# 约定：每个路由上方写「接口名 / 方法 / 参数 / 返回」，并同步更新下方清单
#       与 run.py 顶部的全局总览。
# ============================================================================
from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
from app.dao.ClassicsDao import ClassicsDao  # 引入数据库操作类
from app.dao.UsersDao import UsersDao
from app.model.models import Classictype, ClassictypeSchema
from app.model.models import Classics, ClassicsSchema
from app.model.models import Classicjudges
from app.model.models import Discuss, Discussjudges
from app.model.models import Users, UsersSchema

# ============================================================================
# 本文件接口清单（蓝图前缀 /api/classics，在 run.py 注册时指定）
# ----------------------------------------------------------------------------
#   1) GET  /api/classics/get-classictypes        获取文学作品类型（首页导航栏）
#          参数：无
#          返回：{code, msg, data:[{tid, name, cover, remark}]}
#
#   2) GET  /api/classics/search-carousels/<n>    获取首页轮播图（n=条数）
#          参数：路径参数 n，如 6
#          返回：{code, msg, data:[{cid, title, cover, author, rating, ...}]}
#
#   3) GET  /api/classics/recommend-classics/<n>  文学推荐（教材 3.3.5，n=每类条数）
#          参数：路径参数 n，如 6
#          返回：{code, msg, data:[{tid, name, cover, remark,
#                                  classics:[{cid, title, cover, author, ...}]}]}
#
#   4) POST /api/classics/search-classics         文学搜索（教材 3.3.6）
#          参数：JSON 请求体 {"keyword": "关键字"}（空串=全部）
#          返回：{code, msg, data:[{cid, title, cover, author, ...}]}
#
#   5) GET  /api/classics/get-classics/<tid>      文学列表（教材 6.3.3）
#          参数：路径参数 tid（作品类型编号）
#          返回：{code, msg, data:{tid, name, cover, classics:[{cid, title, ...}]}}
#
#   6) GET  /api/classics/get-classic/<cid>       文学作品信息（教材 6.3.4）
#          参数：路径参数 cid（作品编号）
#          返回：{code, msg, data:{cid, title, author, describes, rating, ...}}
#
#   7) POST /api/classics/judge-classic           文学评价（教材 6.3.5，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"cid": 作品编号, "star": 星级 1-5}
#          返回：{code, msg}
#
#   8) GET  /api/classics/get-discuss/<cid>       书评展示（教材 7.3.1）
#          参数：路径参数 cid（作品编号）
#          返回：{code, msg, data:[{did, cid, comment, cdate, topcount, lowcount,
#                                  user:{uid, uname, nickname, avatar, ...}}]}
#
#   9) POST /api/classics/pub-discuss             发表书评（教材 7.3.2，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"cid": 作品编号, "comment": 书评内容}
#          返回：{code, msg}
#
#  10) POST /api/classics/judge-discuss           书评评价·顶/踩（教材 7.3.3，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"did": 评论编号, "toplow": 0 踩 / 1 顶}
#          返回：{code, msg}
# ----------------------------------------------------------------------------
# 前端（cls_clt，端口 5173）调用时必须加代理前缀 /svr，
# 例如 GET http://localhost:5173/svr/api/classics/get-classictypes
# → vite.config.js 代理转发到 http://127.0.0.1:5382 并去掉 /svr
# ============================================================================

classics_blueprint = Blueprint("classics_blueprint", __name__) # 创建蓝图
# ============================================================================
# 【接口 1】获取文学作品类型（首页导航栏）
# 调用方式：GET /api/classics/get-classictypes
# 参数：无
# 返回：{code:'200', msg:'操作成功！', data:[{tid, name, cover, remark}]}
# ============================================================================
@classics_blueprint.route('/get-classictypes')  # 获取所有文学作品类型数据
def get_classictypes():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    db_op = ClassicsDao()  # 创建数据库操作对象
    classictypes = db_op.getClassictypes()  # 查询文学作品类型，并将其转换为 JSON 格式的数据
    classictype_Schema = ClassictypeSchema(many=True) # many=True 表示转换多条数据
    classictypes_data = classictype_Schema.dump(classictypes)
    result_msg["data"] = classictypes_data # 将转换后的 JSON 格式的数据存储至返回结果
    return jsonify(result_msg)  # 返回操作结果

# ============================================================================
# 【接口 2】获取首页轮播图
# 调用方式：GET /api/classics/search-carousels/<int:number>
# 参数：路径参数 number = 返回条数（如 6）
# 返回：{code:'200', msg:'操作成功！', data:[{cid, title, cover, author, rating, ...}]}
# 排序：rating 倒序 → cid 升序
# ============================================================================
@classics_blueprint.route('/search-carousels/<int:number>')  # 获取首页轮播图数据（number：需要返回的轮播图数量）
def search_carousels(number):
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    db_op = ClassicsDao()  # 创建数据库操作对象
    carousels = db_op.getCarousels(number)  # 查询轮播图数据，并将其转换为 JSON 格式的数据
    classics_Schema = ClassicsSchema(many=True) # many=True 表示转换多条数据
    carousels_data = classics_Schema.dump(carousels)
    result_msg["data"] = carousels_data # 将转换后的 JSON 格式的数据存储至返回结果
    return jsonify(result_msg)  # 返回操作结果

# ============================================================================
# 【接口 3】文学推荐（教材 3.3.5）
# 调用方式：GET /api/classics/recommend-classics/<int:number>
# 参数：路径参数 number = 每个文学类型下返回的作品条数（如 6）
# 返回：{code:'200', msg:'操作成功！',
#        data:[{tid, name, cover, remark,
#               classics:[{cid, title, cover, author, rating, ...}]}]}
# 排序：类型按 tid 升序；同一类型内作品按 rating 倒序 → cid 升序
# 说明：按类型分组返回，前端用 el-page-header 一组一组地渲染推荐栏目
# ============================================================================
@classics_blueprint.route('/recommend-classics/<int:number>')
def recommend_classics(number):
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    db_op = ClassicsDao()  # 创建数据库操作对象
    classictypes = db_op.getClassictypes()  # 查询所有文学作品类型
    classictype_Schema = ClassictypeSchema()  # 单个类型用单条转换，作品列表用多条转换
    classics_Schema = ClassicsSchema(many=True)
    recommend_data = []
    for classictype in classictypes:
        item = classictype_Schema.dump(classictype)  # 类型自身信息（tid、name、cover、remark）
        classics = db_op.getClassicsByTidLimit(classictype.tid, number)  # 该类型下评分最高的前 number 部作品
        item["classics"] = classics_Schema.dump(classics)
        recommend_data.append(item)
    result_msg["data"] = recommend_data # 将分组后的推荐数据存储至返回结果
    return jsonify(result_msg)  # 返回操作结果

# ============================================================================
# 【接口 4】文学搜索
# 调用方式：POST /api/classics/search-classics
# 请求头：Content-Type: application/json
# 请求体：{"keyword": "关键字"}（keyword 为空串时返回全部作品）
# 返回：{code:'200', msg:'操作成功！', data:[{cid, title, cover, author, ...}]}
# 匹配：title LIKE %keyword% OR author LIKE %keyword%，rating 倒序
# ============================================================================
@classics_blueprint.route('/search-classics', methods=['POST'])  # 检索文学作品（请求体 JSON：{"keyword": "关键字"}）
def search_classics():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    # 获取 JSON 格式的请求体（silent=True：非法 JSON 返回 None，与其它接口保持一致，
    request_body = request.get_json(silent=True)  # 不会抛 Flask 默认的 HTML 400）
    # 传了请求体但解析不出来 → 属于参数错误；
    # 完全不传请求体时才按「空关键字 = 查全部」处理
    if request_body is None and request.data:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    keyword = ''  # 关键字为空时按空串处理（返回全部数据）
    if request_body is not None and request_body.get('keyword') is not None:
        keyword = request_body.get('keyword')
    db_op = ClassicsDao()  # 创建数据库操作对象
    classics = db_op.searchClassics(keyword)  # 按关键字检索文学作品，并转换为 JSON 格式的数据
    classics_Schema = ClassicsSchema(many=True)
    classics_data = classics_Schema.dump(classics)
    result_msg["data"] = classics_data
    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口 5】按作品类型获取文学列表（教材 6.3.3）
# 调用方式：GET /api/classics/get-classics/<int:tid>
# 参数：路径参数 tid —— 文学作品类型编号
# 返回：{code, msg, data:{tid, name, cover, classics:[...]}}
#       类型不存在 → {code:'404'}
# ============================================================================
@classics_blueprint.route('/get-classics/<int:tid>')
def get_classics(tid):
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    # 判断请求及参数是否正确
    if tid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    db_op = ClassicsDao()  # 创建数据库操作对象
    classictype = db_op.getClassictypeByTid(tid)  # 查询文学作品类型
    # 类型不存在时直接返回，避免下面取属性报错
    if classictype is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
        return jsonify(result_msg)

    classics = db_op.getClassicsByTid(tid)  # 查询该类型下的文学列表
    classics_Schema = ClassicsSchema(many=True)  # many=True 表示转换多条数据
    classics_data = classics_Schema.dump(classics)

    classictype_tmp = {"tid": tid, "name": classictype.name, "cover": classictype.cover}  # 构建返回数据
    classictype_tmp["classics"] = classics_data
    result_msg["data"] = classictype_tmp  # 将转换后的 JSON 格式的数据存储至返回结果
    return jsonify(result_msg)


# ============================================================================
# 【接口 6】获取文学作品信息（教材 6.3.4）
# 调用方式：GET /api/classics/get-classic/<int:cid>
# 参数：路径参数 cid —— 文学作品编号
# 返回：{code, msg, data:{cid, title, author, year, describes, rating, ...}}
#       作品不存在 → {code:'404'}
# ============================================================================
@classics_blueprint.route('/get-classic/<int:cid>')
def get_classic(cid):
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    # 判断请求及参数是否正确
    if cid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    db_op = ClassicsDao()  # 创建数据库操作对象
    classic = db_op.getClassicsByCid(cid)  # 查询文学作品信息
    if classic is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
        return jsonify(result_msg)

    classics_Schema = ClassicsSchema()  # 转换 JSON 数据（单条，不需要 many）
    classics_data = classics_Schema.dump(classic)
    result_msg["data"] = classics_data  # 将转换后的 JSON 格式的数据存储至返回结果
    return jsonify(result_msg)


# ============================================================================
# 【接口 7】文学评价（教材 6.3.5，需要用户身份）
# 调用方式：POST /api/classics/judge-classic
# 请求头：Authorization: Bearer <token>
# 请求体：{"cid": 作品编号, "star": 星级(1-5)}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@classics_blueprint.route('/judge-classic', methods=['POST'])
@jwt_required()  # 用户身份鉴权
def judgeClassic():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息

    request_body = request.get_json()  # 获取并解析 JSON 格式的请求
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    cid = request_body.get("cid")    # 文学作品编号  # 获取评价数据
    star = request_body.get("star")  # 星级评价

    uid = get_jwt_identity()  # 获取认证的用户编号（登录时通过 uid 生成 Token）
    jdate = datetime.datetime.now()

    judge = Classicjudges(cid=cid, uid=uid, rating=star, jdate=jdate)  # 新建评价对象

    db_op = ClassicsDao()  # 创建数据库操作对象，评价文学作品
    flag = db_op.updateClassicRating(judge)

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    return jsonify(result_msg)  # 返回操作结果
# ============================================================================
# 【接口 8】书评展示 API（教材 7.3.1）
# 调用方式：GET /api/classics/get-discuss/<cid>
# 参数：路径参数 cid —— 文学作品编号
# 返回：{code:'200', msg:'操作成功！', data:[{did, cid, comment, cdate,
#         topcount, lowcount, user:{uid, uname, nickname, avatar, sex, phone, remark}}]}
# 说明：先按 cid 查评论表，再逐条查评论人信息，一起包装成前端要的结构
# ============================================================================
@classics_blueprint.route('/get-discuss/<int:cid>')
def get_discuss(cid):
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    # 判断请求及参数是否正确
    if cid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    db_dis = ClassicsDao()  # 创建数据库操作对象
    db_usr = UsersDao()
    discuss = db_dis.getDiscussByCid(cid)  # 查询文学作品的评论列表
    # 循环取出文学评论，并封装评论用户数据
    dis_list = []  # 文学评论列表
    for dis in discuss:
        uid = dis.uid  # 获取用户编号
        user = db_usr.getUserByUid(uid)  # 查询用户信息
        dis_tmp = {"did": dis.did, "comment": dis.comment, "cdate": dis.cdate,  # 构建返回数据
                   "topcount": dis.topcount, "lowcount": dis.lowcount, "cid": dis.cid}
        users_Schema = UsersSchema()  # 用户 Schema 将数据转换为字典格式
        users_data = users_Schema.dump(user)
        dis_tmp["user"] = users_data
        dis_list.append(dis_tmp)  # 将构建好的文学评论列表加入返回列表中
    result_msg["data"] = dis_list  # 将转换后的 JSON 格式的数据存储至返回结果
    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口 9】发表书评 API（教材 7.3.2，需 JWT）
# 调用方式：POST /api/classics/pub-discuss
# 请求头：Authorization: Bearer <token>
# 请求体：{"cid": 作品编号, "comment": 书评内容}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@classics_blueprint.route('/pub-discuss', methods=["POST"])
@jwt_required()  # 用户身份鉴权
def pubDiscuss():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息

    request_body = request.get_json()  # 获取并解析 JSON 格式的请求
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    cid = request_body.get("cid")            # 文学作品编号  # 获取评论数据
    comment = request_body.get("comment")    # 评论内容

    uid = get_jwt_identity()  # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    cdate = datetime.datetime.now()

    discuss = Discuss(cid=cid, uid=uid, comment=comment, cdate=cdate)  # 新建评论对象

    db_op = ClassicsDao()  # 创建数据库操作对象，发表书评
    flag = db_op.addDiscuss(discuss)

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口 10】书评评价 API（教材 7.3.3，需 JWT）
# 调用方式：POST /api/classics/judge-discuss
# 请求头：Authorization: Bearer <token>
# 请求体：{"did": 评论编号, "toplow": 0 表示踩 / 1 表示顶}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@classics_blueprint.route('/judge-discuss', methods=["POST"])
@jwt_required()  # 用户身份鉴权
def judgeDiscuss():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息

    request_body = request.get_json()  # 获取并解析 JSON 格式的请求
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    did = request_body.get("did")          # 评论编号  # 获取评价数据
    toplow = request_body.get("toplow")    # 评价标志

    uid = get_jwt_identity()  # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    jdate = datetime.datetime.now()

    judge = Discussjudges(did=did, uid=uid, toplow=toplow, jdate=jdate)  # 新建评价对象

    db_op = ClassicsDao()  # 创建数据库操作对象
    flag = db_op.updateDiscussTopLow(judge)  # 评价书评

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口】我的书评（教材 8.3.4，需 JWT）
# 调用方式：GET /api/classics/get-mydiscuss
# 请求头：Authorization: Bearer <token>
# 返回：{code, msg, data:[{did, comment, cdate, classic:{cid,title,cover}}]}
# ============================================================================
@classics_blueprint.route('/get-mydiscuss')  # 获取用户的书评列表
@jwt_required()  # 用户身份鉴权
def get_mydiscuss():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    uid = get_jwt_identity()  # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    db_op = ClassicsDao()  # 创建数据库操作对象
    discuss = db_op.getDiscussesByUid(uid)  # 查询用户的书评列表
    # 循环取出文学评论，并封装文学作品数据
    dis_list = []  # 文学评论列表
    for dis in discuss:
        cid = dis.cid  # 获取对应的文学编号
        cls = db_op.getClassicsByCid(cid)  # 查询对应文学信息
        dis_tmp = {"did": dis.did,  # 构建返回数据
                   "comment": dis.comment,
                   "cdate": dis.cdate,
                   "classic": {"cid": cls.cid, "title": cls.title, "cover": cls.cover}
                   }
        dis_list.append(dis_tmp)  # 将构建好的文学评论列表加入返回列表中
    result_msg["data"] = dis_list  # 将转换后的 JSON 格式的数据存储至返回结果
    return jsonify(result_msg)
