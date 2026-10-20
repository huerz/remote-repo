# ============================================================================
# Hi_flask 接口总览（Flask 后端，端口 5216）
# ----------------------------------------------------------------------------
# 蓝图前缀          定义文件                          接口
# /api/user         app/api/user_blueprint.py        POST /register   用户注册
#                                                    POST /login      用户登录
# ----------------------------------------------------------------------------
# 调用方式（本项目无前端工程，直接用接口工具 / 浏览器控制台请求）：
#   POST http://127.0.0.1:5216/api/user/register
#   POST http://127.0.0.1:5216/api/user/login
#   请求头：Content-Type: application/json
# ----------------------------------------------------------------------------
# 启动：.venv\Scripts\python.exe app.py
# ============================================================================

# 引入应用工厂函数
from app import create_app
from app.api.user_blueprint import user_blueprint
# 调用工厂，创建app
app = create_app()
# 注册蓝图：把 user_blueprint 里的路由挂到 /api/user 前缀下
app.register_blueprint(user_blueprint,url_prefix="/api/user")  
# 启动Flask程序
if __name__ == "__main__":
    # 启动服务，设置主机和端口
    app.run(host="0.0.0.0", port=5216, debug=True)
