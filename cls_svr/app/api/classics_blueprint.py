from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
# 引入数据库操作类
from app.dao.ClassicsDao import ClassicsDao
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
#   3) POST /api/classics/search-classics         文学搜索
#          参数：JSON 请求体 {"keyword": "关键字"}（空串=全部）
#          返回：{code, msg, data:[{cid, title, cover, author, ...}]}
#
#   4) GET  /api/classics/get-classics/<tid>      文学列表（教材 6.3.3）
#          参数：路径参数 tid（作品类型编号）
#          返回：{code, msg, data:{tid, name, cover, classics:[{cid, title, ...}]}}
#
#   5) GET  /api/classics/get-classic/<cid>       文学作品信息（教材 6.3.4）
#          参数：路径参数 cid（作品编号）
#          返回：{code, msg, data:{cid, title, author, describes, rating, ...}}
#
#   6) POST /api/classics/judge-classic           文学评价（教材 6.3.5，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"cid": 作品编号, "star": 星级 1-5}
#          返回：{code, msg}
#
#   7) GET  /api/classics/get-discuss/<cid>       书评展示（教材 7.3.1）
#          参数：路径参数 cid（作品编号）
#          返回：{code, msg, data:[{did, cid, comment, cdate, topcount, lowcount,
#                                  user:{uid, uname, nickname, avatar, ...}}]}
#
#   8) POST /api/classics/pub-discuss             发表书评（教材 7.3.2，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"cid": 作品编号, "comment": 书评内容}
#          返回：{code, msg}
#
#   9) POST /api/classics/judge-discuss           书评评价·顶/踩（教材 7.3.3，需 JWT）
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
# 获取所有文学作品类型数据
@classics_blueprint.route('/get-classictypes')
def get_classictypes():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 创建数据库操作对象
    db_op = ClassicsDao()
    # 查询文学作品类型，并将其转换为 JSON 格式的数据
    classictypes = db_op.getClassictypes()
    classictype_Schema = ClassictypeSchema(many=True) # many=True 表示转换多条数据
    classictypes_data = classictype_Schema.dump(classictypes)
    result_msg["data"] = classictypes_data # 将转换后的 JSON 格式的数据存储至返回结果
    # 返回操作结果
    return jsonify(result_msg)

# ============================================================================
# 【接口 2】获取首页轮播图
# 调用方式：GET /api/classics/search-carousels/<int:number>
# 参数：路径参数 number = 返回条数（如 6）
# 返回：{code:'200', msg:'操作成功！', data:[{cid, title, cover, author, rating, ...}]}
# 排序：rating 倒序 → cid 升序
# ============================================================================
# 获取首页轮播图数据（number：需要返回的轮播图数量）
@classics_blueprint.route('/search-carousels/<int:number>')
def search_carousels(number):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 创建数据库操作对象
    db_op = ClassicsDao()
    # 查询轮播图数据，并将其转换为 JSON 格式的数据
    carousels = db_op.getCarousels(number)
    classics_Schema = ClassicsSchema(many=True) # many=True 表示转换多条数据
    carousels_data = classics_Schema.dump(carousels)
    result_msg["data"] = carousels_data # 将转换后的 JSON 格式的数据存储至返回结果
    # 返回操作结果
    return jsonify(result_msg)

# ============================================================================
# 【接口 3】文学搜索
# 调用方式：POST /api/classics/search-classics
# 请求头：Content-Type: application/json
# 请求体：{"keyword": "关键字"}（keyword 为空串时返回全部作品）
# 返回：{code:'200', msg:'操作成功！', data:[{cid, title, cover, author, ...}]}
# 匹配：title LIKE %keyword% OR author LIKE %keyword%，rating 倒序
# ============================================================================
# 检索文学作品（请求体 JSON：{"keyword": "关键字"}）
@classics_blueprint.route('/search-classics', methods=['POST'])
def search_classics():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 获取 JSON 格式的请求体（silent=True：非法 JSON 返回 None，与其它接口保持一致，
    # 不会抛 Flask 默认的 HTML 400）
    request_body = request.get_json(silent=True)
    # 传了请求体但解析不出来 → 属于参数错误；
    # 完全不传请求体时才按「空关键字 = 查全部」处理
    if request_body is None and request.data:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    # 关键字为空时按空串处理（返回全部数据）
    keyword = ''
    if request_body is not None and request_body.get('keyword') is not None:
        keyword = request_body.get('keyword')
    # 创建数据库操作对象
    db_op = ClassicsDao()
    # 按关键字检索文学作品，并转换为 JSON 格式的数据
    classics = db_op.searchClassics(keyword)
    classics_Schema = ClassicsSchema(many=True)
    classics_data = classics_Schema.dump(classics)
    result_msg["data"] = classics_data
    # 返回操作结果
    return jsonify(result_msg)


# ============================================================================
# 【接口 4】按作品类型获取文学列表（教材 6.3.3）
# 调用方式：GET /api/classics/get-classics/<int:tid>
# 参数：路径参数 tid —— 文学作品类型编号
# 返回：{code, msg, data:{tid, name, cover, classics:[...]}}
#       类型不存在 → {code:'404'}
# ============================================================================
@classics_blueprint.route('/get-classics/<int:tid>')
def get_classics(tid):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 判断请求及参数是否正确
    if tid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 创建数据库操作对象
    db_op = ClassicsDao()
    # 查询文学作品类型
    classictype = db_op.getClassictypeByTid(tid)
    # 类型不存在时直接返回，避免下面取属性报错
    if classictype is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
        return jsonify(result_msg)

    # 查询该类型下的文学列表
    classics = db_op.getClassicsByTid(tid)
    # many=True 表示转换多条数据
    classics_Schema = ClassicsSchema(many=True)
    classics_data = classics_Schema.dump(classics)

    # 构建返回数据
    classictype_tmp = {"tid": tid, "name": classictype.name, "cover": classictype.cover}
    classictype_tmp["classics"] = classics_data
    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = classictype_tmp
    return jsonify(result_msg)


# ============================================================================
# 【接口 5】获取文学作品信息（教材 6.3.4）
# 调用方式：GET /api/classics/get-classic/<int:cid>
# 参数：路径参数 cid —— 文学作品编号
# 返回：{code, msg, data:{cid, title, author, year, describes, rating, ...}}
#       作品不存在 → {code:'404'}
# ============================================================================
@classics_blueprint.route('/get-classic/<int:cid>')
def get_classic(cid):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 判断请求及参数是否正确
    if cid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 创建数据库操作对象
    db_op = ClassicsDao()
    # 查询文学作品信息
    classic = db_op.getClassicsByCid(cid)
    if classic is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
        return jsonify(result_msg)

    # 转换 JSON 数据（单条，不需要 many）
    classics_Schema = ClassicsSchema()
    classics_data = classics_Schema.dump(classic)
    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = classics_data
    return jsonify(result_msg)


# ============================================================================
# 【接口 6】文学评价（教材 6.3.5，需要用户身份）
# 调用方式：POST /api/classics/judge-classic
# 请求头：Authorization: Bearer <token>
# 请求体：{"cid": 作品编号, "star": 星级(1-5)}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@classics_blueprint.route('/judge-classic', methods=['POST'])
@jwt_required()  # 用户身份鉴权
def judgeClassic():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析 JSON 格式的请求
    request_body = request.get_json(silent=True)
    # 判断传入的 JSON 格式的数据是否为空
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取评价数据
    cid = request_body.get("cid")    # 文学作品编号
    star = request_body.get("star")  # 星级评价
    if cid is None or star is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取认证的用户编号（登录时通过 uid 生成 Token）
    uid = int(get_jwt_identity())
    jdate = datetime.datetime.now()

    # 新建评价对象
    judge = Classicjudges(cid=cid, uid=uid, rating=star, jdate=jdate)

    # 创建数据库操作对象，评价文学作品
    db_op = ClassicsDao()
    flag = db_op.updateClassicRating(judge)

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)
# ============================================================================
# 【接口 7】书评展示 API（教材 7.3.1）
# 调用方式：GET /api/classics/get-discuss/<cid>
# 参数：路径参数 cid —— 文学作品编号
# 返回：{code:'200', msg:'操作成功！', data:[{did, cid, comment, cdate,
#         topcount, lowcount, user:{uid, uname, nickname, avatar, sex, phone, remark}}]}
# 说明：先按 cid 查评论表，再逐条查评论人信息，一起包装成前端要的结构
# ============================================================================
@classics_blueprint.route('/get-discuss/<int:cid>')
def get_discuss(cid):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 创建数据库操作对象
    db_dis = ClassicsDao()
    db_usr = UsersDao()

    # 查询该作品的评论列表（按时间倒序）
    discuss = db_dis.getDiscussByCid(cid)

    # 循环取出文学评论，并封装评论用户数据
    dis_list = []
    for dis in (discuss or []):
        # 获取用户编号，查询用户信息
        uid = dis.uid
        user = db_usr.getUserByUid(uid)

        # 构建返回数据
        # 时间统一转成 "YYYY-MM-DD HH:MM" 再返回：
        # Flask 默认会把 datetime 序列化成 HTTP 日期串（Tue, 20 Oct 2026 17:11:23 GMT），
        # 但那串里的时间是本地时间却被标成 GMT，浏览器再按本地时区解析会整体偏移 8 小时。
        cdate = dis.cdate.strftime("%Y-%m-%d %H:%M") if dis.cdate else None
        dis_tmp = {"did": dis.did, "comment": dis.comment, "cdate": cdate,
                   "topcount": dis.topcount, "lowcount": dis.lowcount,
                   "cid": dis.cid}

        # 用 UsersSchema 将数据转换为字典格式（不含密码字段）
        if user is not None:
            users_schema = UsersSchema()
            dis_tmp["user"] = users_schema.dump(user)
        else:
            # 用户被删了也要能显示评论，避免整条数据丢掉
            dis_tmp["user"] = {"uid": uid, "uname": "已注销", "nickname": "已注销用户",
                               "avatar": "tx.png", "sex": None, "phone": None,
                               "remark": None}

        # 将构建好的文学评论列表加入返回列表
        dis_list.append(dis_tmp)

    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = dis_list
    return jsonify(result_msg)


# ============================================================================
# 【接口 8】发表书评 API（教材 7.3.2，需 JWT）
# 调用方式：POST /api/classics/pub-discuss
# 请求头：Authorization: Bearer <token>
# 请求体：{"cid": 作品编号, "comment": 书评内容}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@classics_blueprint.route('/pub-discuss', methods=["POST"])
@jwt_required()  # 用户身份鉴权
def pubDiscuss():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析 JSON 格式的请求
    request_body = request.get_json(silent=True)
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取书评数据
    cid = request_body.get("cid")            # 文学作品编号
    comment = request_body.get("comment")    # 书评内容
    if cid is None or not comment:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取认证的用户编号（登录时通过 uid 生成 Token）
    uid = int(get_jwt_identity())
    cdate = datetime.datetime.now()

    # 新建评论对象
    discuss = Discuss(cid=cid, uid=uid, comment=comment, cdate=cdate,
                      topcount=0, lowcount=0)

    # 创建数据库操作对象，发表书评
    db_op = ClassicsDao()
    flag = db_op.addDiscuss(discuss)

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)


# ============================================================================
# 【接口 9】书评评价 API（教材 7.3.3，需 JWT）
# 调用方式：POST /api/classics/judge-discuss
# 请求头：Authorization: Bearer <token>
# 请求体：{"did": 评论编号, "toplow": 0 表示踩 / 1 表示顶}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@classics_blueprint.route('/judge-discuss', methods=["POST"])
@jwt_required()  # 用户身份鉴权
def judgeDiscuss():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析 JSON 格式的请求
    request_body = request.get_json(silent=True)
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取评价数据
    did = request_body.get("did")          # 评论编号
    toplow = request_body.get("toplow")    # 评价标志
    if did is None or toplow is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取认证的用户编号
    uid = int(get_jwt_identity())
    jdate = datetime.datetime.now()

    # 新建评价对象
    judge = Discussjudges(did=did, uid=uid, toplow=toplow, jdate=jdate)

    # 创建数据库操作对象，评价书评
    # 返回值：'ok' 成功 / 'repeat' 同方向重复提交 / 'fail' 失败
    db_op = ClassicsDao()
    flag = db_op.updateDiscussTopLow(judge)

    if flag == 'ok':
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    elif flag == 'repeat':
        # 同一个人对同一条书评反复点同一边，不再累加计数
        result_msg["code"] = "400"
        result_msg["msg"] = "你已经评价过这条书评了！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)
