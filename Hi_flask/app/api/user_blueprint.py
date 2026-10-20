from flask import Blueprint,request
from flask import jsonify

# ============================================================================
# 本文件接口清单（蓝图前缀 /api/user，在 app.py 注册时指定）
# ----------------------------------------------------------------------------
#   POST /api/user/register   用户注册（教材练习版：仅账号 xiaobai 可注册成功）
#        请求体：{"uname","upwd","nickname","sex","phone"}
#        返回：{code:'200'|'400'|'404', msg}
#
#   POST /api/user/login      用户登录（固定校验 xiaobai / 123456）
#        请求体：{"uname","upwd"}
#        返回：{code, msg, token}（token 在后续章节完善）
# ----------------------------------------------------------------------------
# 启动：.venv\Scripts\python.exe app.py   访问前缀 http://127.0.0.1:5216/api/user/
# ============================================================================

# 创建蓝图
user_blueprint = Blueprint("user_blueprint", __name__)
# ============================================================================
# 【接口】用户注册
# 调用方式：POST /api/user/register
# 请求体：{"uname","upwd","nickname","sex","phone"}
# 返回：{code, msg}
# ============================================================================
# 用户注册接口
@user_blueprint.route('/register',methods=["POST"]) 
def register():
    # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 获取Json格式的请求，并解析JSON
    request_body = request.get_json()
    # 判断传入的Json数据是否为空
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    # 获取注册数据
    uname = request_body.get("uname") # 登录账号
    upwd = request_body.get("upwd") # 登录密码
    nickname = request_body.get("nickname") # 昵称
    avatar = "tx.png" # 默认头像
    sex = request_body.get("sex") # 性别
    phone = request_body.get("phone") # 电话
    # 判断是否注册成功（默认账号为xiaobai的用户可以注册，后续章节将完善该接口）
    if uname == "xiaobai":
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
# 请求体：{"uname","upwd"}（固定校验 xiaobai / 123456）
# 返回：{code, msg, token}
# ============================================================================
# 用户登录接口
@user_blueprint.route('/login',methods=["POST"]) 
def login():
     # 返回信息
    result_msg = {"code": "200", "msg": "操作成功！"}
    # 获取Json格式的请求，并解析JSON
    request_body = request.get_json()
    
    if request.get_json() is None:
        result_msg["code"] = "404"
        result_msg["msg"] = "参数错误"
        return jsonify(result_msg)
    
    # 获取登录数据
    uname = request_body.get("uname") # 登录账号
    upwd = request_body.get("upwd") # 登录密码    
     # 判断是否登录成功（默认账号为xiaobai的用户可以登录，后续章节将完善该接口）
    if uname == "xiaobai" and upwd == "123456":
        result_msg["code"] = "200"
        result_msg["msg"] = "操作成功！"
        result_msg["token"] = "" # 后续开发中完善
    else:
        result_msg["code"] = "400"
        result_msg["msg"] = "操作失败！"
    # 返回操作结果
    return jsonify(result_msg)
