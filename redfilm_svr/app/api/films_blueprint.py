from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
# 引入数据库操作类
from app.dao.FilmsDao import FilmsDao
from app.dao.UsersDao import UsersDao
from app.model.models import Filmtype, FilmtypeSchema
from app.model.models import Films, FilmsSchema
from app.model.models import Filmjudges
from app.model.models import Discuss, Discussjudges
from app.model.models import Users, UsersSchema

# ============================================================================
# 本文件接口清单（蓝图前缀 /api/films，在 run.py 注册时指定）
# ----------------------------------------------------------------------------
#   1) GET  /api/films/get-filmtypes        获取电影类型（首页导航栏）
#          参数：无
#          返回：{code, msg, data:[{tid, name, cover, remark}]}
#
#   2) GET  /api/films/search-carousels/<n>    获取首页轮播图（n=条数）
#          参数：路径参数 n，如 6
#          返回：{code, msg, data:[{cid, title, cover, author, rating, ...}]}
#
#   3) GET  /api/films/recommend-films/<n>  电影推荐（教材 3.3.5，n=每类条数）
#          参数：路径参数 n，如 6
#          返回：{code, msg, data:[{tid, name, cover, remark,
#                                  films:[{cid, title, cover, author, ...}]}]}
#
#   4) POST /api/films/search-films         电影搜索（教材 3.3.6）
#          参数：JSON 请求体 {"keyword": "关键字"}（空串=全部）
#          返回：{code, msg, data:[{cid, title, cover, author, ...}]}
#
#   5) GET  /api/films/get-films/<tid>      电影列表（教材 6.3.3）
#          参数：路径参数 tid（电影类型编号）
#          返回：{code, msg, data:{tid, name, cover, films:[{cid, title, ...}]}}
#
#   6) GET  /api/films/get-film/<cid>       电影电影信息（教材 6.3.4）
#          参数：路径参数 cid（电影编号）
#          返回：{code, msg, data:{cid, title, author, describes, rating, ...}}
#
#   7) POST /api/films/judge-film           电影评价（教材 6.3.5，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"cid": 电影编号, "star": 星级 1-5}
#          返回：{code, msg}
#
#   8) GET  /api/films/get-discuss/<cid>       影评展示（教材 7.3.1）
#          参数：路径参数 cid（电影编号）
#          返回：{code, msg, data:[{did, cid, comment, cdate, topcount, lowcount,
#                                  user:{uid, uname, nickname, avatar, ...}}]}
#
#   9) POST /api/films/pub-discuss             发表影评（教材 7.3.2，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"cid": 电影编号, "comment": 影评内容}
#          返回：{code, msg}
#
#  10) POST /api/films/judge-discuss           影评评价·顶/踩（教材 7.3.3，需 JWT）
#          请求头：Authorization: Bearer <token>
#          请求体：{"did": 评论编号, "toplow": 0 踩 / 1 顶}
#          返回：{code, msg}
# ----------------------------------------------------------------------------
# 前端（cls_clt，端口 5173）调用时必须加代理前缀 /svr，
# 例如 GET http://localhost:5173/svr/api/films/get-filmtypes
# → vite.config.js 代理转发到 http://127.0.0.1:5383 并去掉 /svr
# ============================================================================

films_blueprint = Blueprint("films_blueprint", __name__) # 创建蓝图
# ============================================================================
# 【接口 1】获取电影类型（首页导航栏）
# 调用方式：GET /api/films/get-filmtypes
# 参数：无
# 返回：{code:'200', msg:'操作成功！', data:[{tid, name, cover, remark}]}
# ============================================================================
# 获取所有电影类型数据
@films_blueprint.route('/get-filmtypes')
def get_filmtypes():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 创建数据库操作对象
    db_op = FilmsDao()
    # 查询电影类型，并将其转换为 JSON 格式的数据
    filmtypes = db_op.getFilmtypes()
    filmtype_Schema = FilmtypeSchema(many=True) # many=True 表示转换多条数据
    filmtypes_data = filmtype_Schema.dump(filmtypes)
    result_msg["data"] = filmtypes_data # 将转换后的 JSON 格式的数据存储至返回结果
    # 返回操作结果
    return jsonify(result_msg)

# ============================================================================
# 【接口 2】获取首页轮播图
# 调用方式：GET /api/films/search-carousels/<int:number>
# 参数：路径参数 number = 返回条数（如 6）
# 返回：{code:'200', msg:'操作成功！', data:[{cid, title, cover, author, rating, ...}]}
# 排序：rating 倒序 → cid 升序
# ============================================================================
# 获取首页轮播图数据（number：需要返回的轮播图数量）
@films_blueprint.route('/search-carousels/<int:number>')
def search_carousels(number):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 创建数据库操作对象
    db_op = FilmsDao()
    # 查询轮播图数据，并将其转换为 JSON 格式的数据
    carousels = db_op.getCarousels(number)
    films_Schema = FilmsSchema(many=True) # many=True 表示转换多条数据
    carousels_data = films_Schema.dump(carousels)
    result_msg["data"] = carousels_data # 将转换后的 JSON 格式的数据存储至返回结果
    # 返回操作结果
    return jsonify(result_msg)

# ============================================================================
# 【接口 3】电影推荐（教材 3.3.5）
# 调用方式：GET /api/films/recommend-films/<int:number>
# 参数：路径参数 number = 每个电影类型下返回的电影条数（如 6）
# 返回：{code:'200', msg:'操作成功！',
#        data:[{tid, name, cover, remark,
#               films:[{cid, title, cover, author, rating, ...}]}]}
# 排序：类型按 tid 升序；同一类型内电影按 rating 倒序 → cid 升序
# 说明：按类型分组返回，前端用 el-page-header 一组一组地渲染推荐栏目
# ============================================================================
@films_blueprint.route('/recommend-films/<int:number>')
def recommend_films(number):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 创建数据库操作对象
    db_op = FilmsDao()
    # 查询所有电影类型
    filmtypes = db_op.getFilmtypes()
    # 单个类型用单条转换，电影列表用多条转换
    filmtype_Schema = FilmtypeSchema()
    films_Schema = FilmsSchema(many=True)
    recommend_data = []
    for filmtype in filmtypes:
        # 类型自身信息（tid、name、cover、remark）
        item = filmtype_Schema.dump(filmtype)
        # 该类型下评分最高的前 number 部电影
        films = db_op.getFilmsByTidLimit(filmtype.tid, number)
        item["films"] = films_Schema.dump(films)
        recommend_data.append(item)
    result_msg["data"] = recommend_data # 将分组后的推荐数据存储至返回结果
    # 返回操作结果
    return jsonify(result_msg)

# ============================================================================
# 【接口 4】电影搜索
# 调用方式：POST /api/films/search-films
# 请求头：Content-Type: application/json
# 请求体：{"keyword": "关键字"}（keyword 为空串时返回全部电影）
# 返回：{code:'200', msg:'操作成功！', data:[{cid, title, cover, author, ...}]}
# 匹配：title LIKE %keyword% OR author LIKE %keyword%，rating 倒序
# ============================================================================
# 检索电影电影（请求体 JSON：{"keyword": "关键字"}）
@films_blueprint.route('/search-films', methods=['POST'])
def search_films():
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
    db_op = FilmsDao()
    # 按关键字检索电影电影，并转换为 JSON 格式的数据
    films = db_op.searchFilms(keyword)
    films_Schema = FilmsSchema(many=True)
    films_data = films_Schema.dump(films)
    result_msg["data"] = films_data
    # 返回操作结果
    return jsonify(result_msg)


# ============================================================================
# 【接口 5】按电影类型获取电影列表（教材 6.3.3）
# 调用方式：GET /api/films/get-films/<int:tid>
# 参数：路径参数 tid —— 电影类型编号
# 返回：{code, msg, data:{tid, name, cover, films:[...]}}
#       类型不存在 → {code:'404'}
# ============================================================================
@films_blueprint.route('/get-films/<int:tid>')
def get_films(tid):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 判断请求及参数是否正确
    if tid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 创建数据库操作对象
    db_op = FilmsDao()
    # 查询电影类型
    filmtype = db_op.getFilmtypeByTid(tid)
    # 类型不存在时直接返回，避免下面取属性报错
    if filmtype is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
        return jsonify(result_msg)

    # 查询该类型下的电影列表
    films = db_op.getFilmsByTid(tid)
    # many=True 表示转换多条数据
    films_Schema = FilmsSchema(many=True)
    films_data = films_Schema.dump(films)

    # 构建返回数据
    filmtype_tmp = {"tid": tid, "name": filmtype.name, "cover": filmtype.cover}
    filmtype_tmp["films"] = films_data
    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = filmtype_tmp
    return jsonify(result_msg)


# ============================================================================
# 【接口 6】获取电影电影信息（教材 6.3.4）
# 调用方式：GET /api/films/get-film/<int:cid>
# 参数：路径参数 cid —— 电影编号
# 返回：{code, msg, data:{cid, title, author, year, describes, rating, ...}}
#       电影不存在 → {code:'404'}
# ============================================================================
@films_blueprint.route('/get-film/<int:cid>')
def get_film(cid):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 判断请求及参数是否正确
    if cid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 创建数据库操作对象
    db_op = FilmsDao()
    # 查询电影电影信息
    classic = db_op.getFilmsByCid(cid)
    if classic is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
        return jsonify(result_msg)

    # 转换 JSON 数据（单条，不需要 many）
    films_Schema = FilmsSchema()
    films_data = films_Schema.dump(classic)
    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = films_data
    return jsonify(result_msg)


# ============================================================================
# 【接口 7】电影评价（教材 6.3.5，需要用户身份）
# 调用方式：POST /api/films/judge-film
# 请求头：Authorization: Bearer <token>
# 请求体：{"cid": 电影编号, "star": 星级(1-5)}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@films_blueprint.route('/judge-film', methods=['POST'])
@jwt_required()  # 用户身份鉴权
def judgeFilm():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析 JSON 格式的请求
    request_body = request.get_json()
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取评价数据
    cid = request_body.get("cid")    # 电影编号
    star = request_body.get("star")  # 星级评价

    # 获取认证的用户编号（登录时通过 uid 生成 Token）
    uid = get_jwt_identity()
    jdate = datetime.datetime.now()

    # 新建评价对象
    judge = Filmjudges(cid=cid, uid=uid, rating=star, jdate=jdate)

    # 创建数据库操作对象，评价电影电影
    db_op = FilmsDao()
    flag = db_op.updateFilmRating(judge)

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)
# ============================================================================
# 【接口 8】影评展示 API（教材 7.3.1）
# 调用方式：GET /api/films/get-discuss/<cid>
# 参数：路径参数 cid —— 电影编号
# 返回：{code:'200', msg:'操作成功！', data:[{did, cid, comment, cdate,
#         topcount, lowcount, user:{uid, uname, nickname, avatar, sex, phone, remark}}]}
# 说明：先按 cid 查评论表，再逐条查评论人信息，一起包装成前端要的结构
# ============================================================================
@films_blueprint.route('/get-discuss/<int:cid>')
def get_discuss(cid):
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 判断请求及参数是否正确
    if cid is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    # 创建数据库操作对象
    db_dis = FilmsDao()
    db_usr = UsersDao()
    # 查询电影电影的评论列表
    discuss = db_dis.getDiscussByCid(cid)
    # 循环取出影评，并封装评论用户数据
    # 影评列表
    dis_list = []
    for dis in discuss:
        # 获取用户编号
        uid = dis.uid
        # 查询用户信息
        user = db_usr.getUserByUid(uid)
        # 构建返回数据
        dis_tmp = {"did": dis.did, "comment": dis.comment, "cdate": dis.cdate,
                   "topcount": dis.topcount, "lowcount": dis.lowcount, "cid": dis.cid}
        # 用户 Schema 将数据转换为字典格式
        users_Schema = UsersSchema()
        users_data = users_Schema.dump(user)
        dis_tmp["user"] = users_data
        # 将构建好的影评列表加入返回列表中
        dis_list.append(dis_tmp)
    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = dis_list
    # 返回操作结果
    return jsonify(result_msg)


# ============================================================================
# 【接口 9】发表影评 API（教材 7.3.2，需 JWT）
# 调用方式：POST /api/films/pub-discuss
# 请求头：Authorization: Bearer <token>
# 请求体：{"cid": 电影编号, "comment": 影评内容}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@films_blueprint.route('/pub-discuss', methods=["POST"])
@jwt_required()  # 用户身份鉴权
def pubDiscuss():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析 JSON 格式的请求
    request_body = request.get_json()
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取评论数据
    cid = request_body.get("cid")            # 电影编号
    comment = request_body.get("comment")    # 评论内容

    # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    uid = get_jwt_identity()
    cdate = datetime.datetime.now()

    # 新建评论对象
    discuss = Discuss(cid=cid, uid=uid, comment=comment, cdate=cdate)

    # 创建数据库操作对象，发表影评
    db_op = FilmsDao()
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
# 【接口 10】影评评价 API（教材 7.3.3，需 JWT）
# 调用方式：POST /api/films/judge-discuss
# 请求头：Authorization: Bearer <token>
# 请求体：{"did": 评论编号, "toplow": 0 表示踩 / 1 表示顶}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'参数错误'}
# ============================================================================
@films_blueprint.route('/judge-discuss', methods=["POST"])
@jwt_required()  # 用户身份鉴权
def judgeDiscuss():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析 JSON 格式的请求
    request_body = request.get_json()
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取评价数据
    did = request_body.get("did")          # 评论编号
    toplow = request_body.get("toplow")    # 评价标志

    # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    uid = get_jwt_identity()
    jdate = datetime.datetime.now()

    # 新建评价对象
    judge = Discussjudges(did=did, uid=uid, toplow=toplow, jdate=jdate)

    # 创建数据库操作对象
    db_op = FilmsDao()
    # 评价影评
    flag = db_op.updateDiscussTopLow(judge)

    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)


# ============================================================================
# 【接口】我的影评（教材 8.3.4，需 JWT）
# 调用方式：GET /api/films/get-mydiscuss
# 请求头：Authorization: Bearer <token>
# 返回：{code, msg, data:[{did, comment, cdate, classic:{cid,title,cover}}]}
# ============================================================================
# 获取用户的影评列表
@films_blueprint.route('/get-mydiscuss')
@jwt_required()  # 用户身份鉴权
def get_mydiscuss():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    uid = get_jwt_identity()
    # 创建数据库操作对象
    db_op = FilmsDao()
    # 查询用户的影评列表
    discuss = db_op.getDiscussesByUid(uid)
    # 循环取出影评，并封装电影电影数据
    # 影评列表
    dis_list = []
    for dis in discuss:
        # 获取对应的电影编号
        cid = dis.cid
        # 查询对应电影信息
        cls = db_op.getFilmsByCid(cid)
        # 构建返回数据
        dis_tmp = {"did": dis.did,
                   "comment": dis.comment,
                   "cdate": dis.cdate,
                   "classic": {"cid": cls.cid, "title": cls.title, "cover": cls.cover}
                   }
        # 将构建好的影评列表加入返回列表中
        dis_list.append(dis_tmp)
    # 将转换后的 JSON 格式的数据存储至返回结果
    result_msg["data"] = dis_list
    return jsonify(result_msg)
