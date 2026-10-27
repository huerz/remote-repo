# ============================================================================
# redfilm_svr 接口总览（Flask 后端，端口 5383）——「红影赏析」电影赏析站
# ----------------------------------------------------------------------------
# 蓝图前缀          定义文件                          接口
# /api/user         app/api/user_blueprint.py        POST /register
#                                                    POST /login
#                                                    GET  /get-user（需 JWT，查登录用户）
#                                                    GET  /protected（需 JWT）
#                                                    POST /upload（头像上传）
#                                                    POST /update-user（改资料，需 JWT）
#                                                    POST /update-pwd（改密码，需 JWT）
# /api/films        app/api/films_blueprint.py       GET  /get-filmtypes
#                                                    GET  /search-carousels/<n>
#                                                    GET  /recommend-films/<n>
#                                                    POST /search-films
#                                                    GET  /get-films/<tid>
#                                                    GET  /get-film/<cid>
#                                                    POST /judge-film（需 JWT）
#                                                    GET  /get-discuss/<cid>（影评展示）
#                                                    POST /pub-discuss（需 JWT，发表影评）
#                                                    POST /judge-discuss（需 JWT，影评顶/踩）
#                                                    GET  /get-mydiscuss（需 JWT，我的影评）
# /api/image        app/api/image_blueprint.py       GET  /display/<type>/<filename>
#                   （该蓝图在 app/__init__.py 的 create_app() 里注册）
# ----------------------------------------------------------------------------
# 前端 redfilm_clt（http://localhost:5175）调用时统一加代理前缀 /svr：
#   GET  /svr/api/films/get-filmtypes
#   GET  /svr/api/films/search-carousels/6
#   GET  /svr/api/films/recommend-films/6
#   POST /svr/api/films/search-films
#   GET  /svr/api/image/display/cls/<海报文件名>
#   GET  /svr/api/image/display/head/logo.png
# proxy 配置见 redfilm_clt/vite.config.ts（转发到 127.0.0.1:5383 并去掉 /svr）
# ----------------------------------------------------------------------------
# 启动：.venv\Scripts\python.exe run.py
# ============================================================================

# 引入应用工厂函数
from app import create_app

# 导入用户蓝图
from app.api.user_blueprint import user_blueprint
from app.api.films_blueprint import films_blueprint


# 调用工厂，创建app
app = create_app()
    
# 2. 注册用户蓝图python run.py
app.register_blueprint(user_blueprint, url_prefix="/api/user")
app.register_blueprint(films_blueprint, url_prefix="/api/films")


# 启动Flask程序
if __name__ == "__main__":
    # 启动服务，设置主机和端口
    app.run(host="0.0.0.0", port=5383, debug=True)
    