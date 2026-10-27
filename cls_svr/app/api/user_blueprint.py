# ============================================================================
# 用户蓝图（前缀 /api/user）
# ----------------------------------------------------------------------------
# 作用：注册、登录、查询登录用户、JWT 保护示例接口。
# 教材：第六章 §6.3.1 注册、登录、查询登录用户（用户中心基础功能）
#       第八章只新增三处：§8.3.2 头像上传、§8.3.3 信息修改、§8.3.5 密码重置
#       参考：§8.2.1 Flask 文件上传（p224）
# 调用：前端 /svr/api/user/... → 后端 /api/user/...
# 约定：需要登录的接口用 @jwt_required()，用户编号一律从 Token 解析，
#       不接受前端传入 uid（防越权）。
# ============================================================================
from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
import re

from app.conf.config import ALLOWED_EXTENSIONS, IMAGE_HEAD_PATH  # 导入上传头像的配置（文件扩展名的集合、头像路径）

from app.dao.UsersDao import UsersDao  # 引入数据库操作类
from app.model.models import Users, UsersSchema

# 账号格式：3~20 位字母、数字、下划线（数据库 uname 是 VARCHAR(100)，
UNAME_RE = re.compile(r'^[A-Za-z0-9_]{3,20}$')  # 不校验长度会让超长账号直接触发数据库报错，变成 500）

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
#        返回：{code, msg, data:{uid, uname, nickname, avatar, sex, phone, remark}}
#        （不返回 upwd：密码属于敏感字段，绝不能下发到前端）
#
#   GET  /api/user/protected  受保护路由（需 JWT 认证）
#        请求头：Authorization: Bearer <token>
#        返回：{logged_in_as: 用户名}
# ----------------------------------------------------------------------------
# 前端调用示例（加代理前缀 /svr）：
#   POST /svr/api/user/register
#   POST /svr/api/user/login
# ============================================================================

user_blueprint = Blueprint("user_blueprint", __name__)  # 创建蓝图

# ============================================================================
# 【接口】用户注册
# 调用方式：POST /api/user/register
# 请求体：{"uname","upwd","nickname","sex","phone"}
# 返回：{code, msg}
# ============================================================================
@user_blueprint.route('/register', methods=["POST"])  # 用户注册 API
def register():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息

    # 获取并解析JSON格式的请求
    # silent=True：请求体不是合法 JSON 时返回 None，而不是让 Flask 直接抛 400
    request_body = request.get_json(silent=True)

    # 判断传入的JSON格式的数据是否为空
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    uname = request_body.get("uname")  # 登录账号  # 获取注册数据
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

    # 格式与长度校验（不校验的话，超长内容会直接触发数据库报错变成 500）
    if not UNAME_RE.match(uname):
        result_msg["code"] = "400"
        result_msg["msg"] = "账号只能是 3~20 位字母、数字或下划线！"
        return jsonify(result_msg)
    if not 6 <= len(upwd) <= 32:
        result_msg["code"] = "400"
        result_msg["msg"] = "密码长度需为 6~32 位！"
        return jsonify(result_msg)
    if nickname and len(nickname) > 20:
        result_msg["code"] = "400"
        result_msg["msg"] = "昵称不能超过 20 个字！"
        return jsonify(result_msg)
    if phone and not re.match(r'^\d{6,20}$', phone):
        result_msg["code"] = "400"
        result_msg["msg"] = "电话号码格式不正确！"
        return jsonify(result_msg)

    db_op = UsersDao()  # 创建数据库操作对象

    # 账号查重：users 表 uname 无唯一约束，必须在此拦截重复注册
    if db_op.existsByUname(uname):
        result_msg["code"] = "400"
        result_msg["msg"] = "该账号已存在，请更换账号！"
        return jsonify(result_msg)

    # 新建用户对象，将用户写入数据库
    # 密码不存明文：用 werkzeug 的加盐哈希（同一密码每次哈希结果都不同）
    user = Users(uname=uname, upwd=generate_password_hash(upwd), nickname=nickname,
                 avatar=avatar, sex=sex, phone=phone)
    flag = db_op.addUser(user)  # 增加用户
    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "400"
        result_msg["msg"] = "操作失败！"

    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口】用户登录
# 调用方式：POST /api/user/login
# 请求体：{"uname","upwd"}
# 返回：{code, msg, token}（成功时 token 为 JWT 字符串）
# 校验规则：按 uname 查 users 表，密码一致才签发 Token（不再固定账号）
# ============================================================================
@user_blueprint.route('/login', methods=["POST"])  # 用户登录 API
def login():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息

    # 获取并解析JSON格式的请求（silent=True：非法 JSON 返回 None 而不是抛 400）
    request_body = request.get_json(silent=True)
    if request_body is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)

    uname = request_body.get("uname")  # 登录账号  # 获取登录数据
    upwd = request_body.get("upwd")    # 登录密码

    if not uname or not upwd:
        result_msg["code"] = "404"
        result_msg["msg"] = "账号和密码不能为空！"
        return jsonify(result_msg)

    db_op = UsersDao()  # 查库校验账号密码
    user = db_op.getUserByUname(uname)

    # 密码校验：库里存的可能是哈希（新注册的用户），也可能是明文（历史数据）
    #   - 哈希：用 check_password_hash 校验
    passed = False  # - 明文：直接比对，比对成功后立刻升级成哈希（无需人工迁移老数据）
    if user is not None:
        stored = user.upwd or ''
        if stored.startswith(('pbkdf2:', 'scrypt:')):
            passed = check_password_hash(stored, upwd)
        else:
            passed = (stored == upwd)
            if passed:
                db_op.updatePassword(user.uid, generate_password_hash(upwd))

    # 判断是否登录成功
    if passed:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"

        # 创建 Token 并返回给客户端（核心代码！）
        # 注意：identity 存的是 uid（不是账号名），后续接口用它查用户；
        access_token = create_access_token(identity=str(user.uid))  # PyJWT 2.10 起 sub 必须是字符串，所以这里转成 str
        result_msg["token"] = access_token
    else:
        result_msg["code"] = "400"
        result_msg["msg"] = "账号或密码错误！"

    return jsonify(result_msg)  # 返回操作结果

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
# 【接口】上传用户头像（教材 8.2.2）
# 调用方式：POST /api/user/upload
# 请求体：form-data，参数名 file（png / gif / jpg / webp / jpeg）
# 返回：{code:'200', msg:'上传成功！', upFile:'<uuid>.<ext>'}
# ============================================================================
def allowed_file(filename):  # 判断头像图片是否允许上传
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_blueprint.route('/upload', methods=['POST'])  # 上传用户头像
def upload():
    result_msg = {"code": "200", "msg": "上传成功！"}  # 返回信息
    # 判断是否有上传文件
    if 'file' not in request.files:
        result_msg["code"] = "404"
        result_msg["msg"] = "文件不存在！"
        return jsonify(result_msg)
    upfile = request.files['file']  # 获取上传文件
    # 判断是否允许上传
    if upfile and allowed_file(upfile.filename):
        upname = secure_filename(upfile.filename)  # 获取文件名称
        fname = str(uuid.uuid4()) + '.' + upname.rsplit('.', 1)[1]  # 为处理重名情况，使用 uuid 生成文件名
        upfile.save(os.path.join(IMAGE_HEAD_PATH, fname))  # 保存文件到存放目录
        result_msg["upFile"] = fname
    else:
        result_msg["code"] = "400"  # 构建返回的 JSON 格式的数据
        result_msg["msg"] = "上传失败！"
    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口】个人信息修改（教材 8.2.3，需 JWT）
# 调用方式：POST /api/user/update-user
# 请求头：Authorization: Bearer <token>
# 请求体：{"nickname", "avatar", "sex", "phone"}
# 返回：{code:'200', msg:'操作成功！'} / {code:'404', msg:'操作失败！'}
# ============================================================================
@user_blueprint.route('/update-user', methods=['POST'])  # 个人信息修改 API
@jwt_required()  # 用户身份鉴权
def updateUser():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    request_body = request.get_json()  # 获取并解析 JSON 格式的请求
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    nickname = request_body.get("nickname")  # 获取参数
    avatar = request_body.get("avatar")
    sex = request_body.get("sex")
    phone = request_body.get("phone")
    uid = get_jwt_identity()  # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    db_op = UsersDao()  # 创建数据库操作对象
    user = Users(uid=uid, nickname=nickname, sex=sex, phone=phone, avatar=avatar)  # 新建用户对象
    flag = db_op.updateUserBySelf(user)  # 修改个人信息
    if flag:
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"
    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口】查询用户信息（教材 6.2）
# 调用方式：GET /api/user/get-user
# 请求头：Authorization: Bearer <token>（必须是登录后拿到的令牌）
# 参数：无（用户编号从 Token 里取，不需要前端传）
# 返回：{code:'200', msg:'操作成功！', data:{uid, uname, nickname, avatar, sex, phone, remark}}
#       注意：不返回 upwd（密码属于敏感字段，绝不能下发到前端）
#       Token 无效/过期 → 401（由 flask_jwt_extended 返回）
#       用户不存在 → {code:'404', msg:'操作失败！'}
# ============================================================================
@user_blueprint.route('/get-user')
@jwt_required()  # 用户身份鉴权
def getUser():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息

    # 获取认证的用户编号（登录时通过 uid 生成 Token）
    # 说明：教材写的是 uid = get_jwt_identity()（教材 Token 里存的是 int）；
    #       本项目 PyJWT 2.10+ 要求 sub 必须是字符串，登录时存的是 str(uid)，
    uid = int(get_jwt_identity())  # 所以这里用 int() 转回数字再查库，效果与教材一致。

    db_op = UsersDao()  # 创建数据库操作对象，查询用户信息
    user = db_op.getUserByUid(uid)

    # 判断查询结果
    if user is not None:
        users_Schema = UsersSchema()  # 将数据转换为 JSON 格式的数据
        users_data = users_Schema.dump(user)
        result_msg["data"] = users_data
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "操作失败！"

    return jsonify(result_msg)  # 返回操作结果


# ============================================================================
# 【接口】密码重置（教材 8.3.5，需 JWT）
# 调用方式：POST /api/user/update-pwd
# 请求头：Authorization: Bearer <token>
# 请求体：{"oldpwd", "newpwd"}
# 返回：{code:'200', msg:'修改成功！'} / {code:'404', msg:'旧密码不正确'}
# ============================================================================
@user_blueprint.route('/update-pwd', methods=["POST"])  # 密码重置 API
@jwt_required()  # 用户身份鉴权
def updatePwd():
    result_msg = {"code": "200", "msg": "操作成功！"}  # 返回信息
    request_body = request.get_json()  # 获取并解析 JSON 格式的请求
    # 判断传入的 JSON 格式的数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    oldpwd = request_body.get("oldpwd")  # 获取参数
    newpwd = request_body.get("newpwd")
    uid = get_jwt_identity()  # 获取认证的用户编号（登录时，通过 uid 生成 Token）
    db_op = UsersDao()  # 创建数据库操作对象
    user = db_op.getUserByUid(uid)  # 查询用户信息
    # 判断旧密码是否正确
    if user.upwd == oldpwd:
        flag = db_op.updateUserByPwd(uid, newpwd)  # 修改用户信息
        if flag:
            result_msg["code"] = "200"
            result_msg["msg"] = "修改成功！"
        else:
            result_msg["code"] = "404"
            result_msg["msg"] = "操作失败！"
    else:
        result_msg["code"] = "404"
        result_msg["msg"] = "旧密码不正确"
    return jsonify(result_msg)  # 返回操作结果
