from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# 引入数据库操作类
from app.dao.UsersDao import UsersDao
from app.model.models import Users, UsersSchema

# ============================================================================
# 本文件接口清单（蓝图前缀 /api/user，在 run.py 注册时指定）
# ----------------------------------------------------------------------------
#   POST /api/user/register   用户注册
#        请求体：{"uname","upwd","nickname","sex","phone"}
#        返回：{code:'200'|'400'|'404', msg}
#
#   POST /api/user/login      用户登录（成功返回 JWT token）
#        请求体：{"uname","upwd"}（按 uname 查 users 表校验密码）
#        返回：{code, msg, token}（token 的 identity 存 uid）
#
#   GET  /api/user/get-user   查询登录用户信息（需 JWT 认证，教材 6.2）
#        请求头：Authorization: Bearer <token>
#        返回：{code, msg, data:{uid, uname, upwd, nickname, avatar, sex, phone, remark}}
#
#   GET  /api/user/protected  受保护路由（需 JWT 认证）
#        请求头：Authorization: Bearer <token>
#        返回：{logged_in_as: 用户名}
# ----------------------------------------------------------------------------
# 前端调用示例（加代理前缀 /svr）：
#   POST /svr/api/user/register
#   POST /svr/api/user/login
# ============================================================================

# 创建蓝图
user_blueprint = Blueprint("user_blueprint", __name__)

# ============================================================================
# 【接口】用户注册
# 调用方式：POST /api/user/register
# 请求体：{"uname","upwd","nickname","sex","phone"}
# 返回：{code, msg}
# ============================================================================
# 用户注册 API
@user_blueprint.route('/register', methods=["POST"])
def register():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析JSON格式的请求
    # silent=True：请求体不是合法 JSON 时返回 None，而不是让 Flask 直接抛 400
    request_body = request.get_json(silent=True)

    # 判断传入的JSON格式的数据是否为空
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取注册数据
    uname = request_body.get("uname")  # 登录账号
    upwd = request_body.get("upwd")    # 登录密码
    nickname = request_body.get("nickname")  # 昵称
    avatar = "tx.png"  # 头像
    sex = request_body.get("sex")      # 性别
    phone = request_body.get("phone")  # 电话号码

    # 必填项校验
    if not uname or not upwd:
        result_msg["code"] = "404"
        result_msg["msg"] = "账号和密码不能为空！"
        return jsonify(result_msg)

    # 创建数据库操作对象
    db_op = UsersDao()

    # 账号查重：users 表 uname 无唯一约束，必须在此拦截重复注册
    if db_op.existsByUname(uname):
        result_msg["code"] = "400"
        result_msg["msg"] = "该账号已存在，请更换账号！"
        return jsonify(result_msg)

    # 新建用户对象，将用户写入数据库
    user = Users(uname=uname, upwd=upwd, nickname=nickname, avatar=avatar,
                 sex=sex, phone=phone)
    flag = db_op.addUser(user)  # 增加用户
    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "400"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)


# ============================================================================
# 【接口】用户登录
# 调用方式：POST /api/user/login
# 请求体：{"uname","upwd"}
# 返回：{code, msg, token}（成功时 token 为 JWT 字符串）
# 校验规则：按 uname 查 users 表，密码一致才签发 Token（不再固定账号）
# ============================================================================
# 用户登录 API
@user_blueprint.route('/login', methods=["POST"])
def login():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取并解析JSON格式的请求（silent=True：非法 JSON 返回 None 而不是抛 400）
    request_body = request.get_json(silent=True)
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    # 获取登录数据
    uname = request_body.get("uname")  # 登录账号
    upwd = request_body.get("upwd")    # 登录密码

    if not uname or not upwd:
        result_msg["code"] = "404"
        result_msg["msg"] = "账号和密码不能为空！"
        return jsonify(result_msg)

    # 查库校验账号密码
    db_op = UsersDao()
    user = db_op.getUserByUname(uname)

    # 判断是否登录成功
    if user is not None and user.upwd == upwd:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"

        # 创建 Token 并返回给客户端（核心代码！）
        # 注意：identity 存的是 uid（不是账号名），后续接口用它查用户；
        # PyJWT 2.10 起 sub 必须是字符串，所以这里转成 str
        access_token = create_access_token(identity=str(user.uid))
        result_msg["token"] = access_token
    else:
        result_msg["code"] = "400"
        result_msg["msg"] = "账号或密码错误！"

    # 返回操作结果
    return jsonify(result_msg)

# ============================================================================
# 【接口】受保护路由（验证 JWT 是否有效）
# 调用方式：GET /api/user/protected
# 请求头：Authorization: Bearer <token>
# 返回：{logged_in_as: 用户名}
# ============================================================================
# 路由保护，表示该路由只有认证用户才能访问
# 注意：请求时，headers 需要设置 Authorization 参数，其值应为 "Bearer+空格+Token" 格式的字符串
@user_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # 获取用户的 identity 信息
    return jsonify(logged_in_as=current_user), 200


# ============================================================================
# 【接口】查询用户信息（教材 6.2）
# 调用方式：GET /api/user/get-user
# 请求头：Authorization: Bearer <token>（必须是登录后拿到的令牌）
# 参数：无（用户编号从 Token 里取，不需要前端传）
# 返回：{code:'200', msg:'操作成功！', data:{uid, uname, upwd, nickname, avatar, sex, phone, remark}}
#       Token 无效/过期 → 401（由 flask_jwt_extended 返回）
#       用户不存在 → {code:'404', msg:'操作失败！'}
# ============================================================================
@user_blueprint.route('/get-user')
@jwt_required()  # 用户身份鉴权
def getUser():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}

    # 获取认证的用户编号（登录时通过 uid 生成 Token）
    uid = int(get_jwt_identity())

    # 创建数据库操作对象，查询用户信息
    db_op = UsersDao()
    user = db_op.getUserByUid(uid)

    # 判断查询结果
    if user is not None:
        # 将数据转换为 JSON 格式的数据
        users_Schema = UsersSchema()
        users_data = users_Schema.dump(user)
        result_msg["data"] = users_data
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    # 返回操作结果
    return jsonify(result_msg)
