# ============================================================================
# cls_svr 接口总览（Flask 后端，端口 5382）
# ----------------------------------------------------------------------------
# 蓝图前缀          定义文件                          接口
# /api/user         app/api/user_blueprint.py        POST /register
#                                                    POST /login
#                                                    GET  /get-user（需 JWT，查登录用户）
#                                                    GET  /protected（需 JWT）
# /api/classics     app/api/classics_blueprint.py    GET  /get-classictypes
#                                                    GET  /search-carousels/<n>
#                                                    POST /search-classics
#                                                    GET  /get-classics/<tid>
#                                                    GET  /get-classic/<cid>
#                                                    POST /judge-classic（需 JWT）
#                                                    GET  /get-discuss/<cid>（书评展示）
#                                                    POST /pub-discuss（需 JWT，发表书评）
#                                                    POST /judge-discuss（需 JWT，书评顶/踩）
# /api/image        app/api/image_blueprint.py       GET  /display/<type>/<filename>
#                   （该蓝图在 app/__init__.py 的 create_app() 里注册）
# ----------------------------------------------------------------------------
# 前端 cls_clt（http://localhost:5173）调用时统一加代理前缀 /svr：
#   GET  /svr/api/classics/get-classictypes
#   GET  /svr/api/classics/search-carousels/6
#   POST /svr/api/classics/search-classics
#   GET  /svr/api/image/display/head/logo.png
# proxy 配置见 cls_clt/vite.config.ts（转发到 127.0.0.1:5382 并去掉 /svr）
# ----------------------------------------------------------------------------
# 启动：.venv\Scripts\python.exe run.py
# ============================================================================

# 引入应用工厂函数
from app import create_app

# 导入用户蓝图
from app.api.user_blueprint import user_blueprint
from app.api.classics_blueprint import classics_blueprint


# 调用工厂，创建app
app = create_app()
    
# 2. 注册用户蓝图python run.py
app.register_blueprint(user_blueprint, url_prefix="/api/user")
app.register_blueprint(classics_blueprint, url_prefix="/api/classics")


# 启动Flask程序
if __name__ == "__main__":
    # 启动服务，设置主机和端口
    app.run(host="0.0.0.0", port=5382, debug=True)
    