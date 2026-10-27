# ============================================================================
# Flask 应用工厂
# ----------------------------------------------------------------------------
# 作用：创建 app、初始化 JWT / 数据库 / Marshmallow，注册蓝图，兜住全局异常。
# 用法：from app import create_app；app = create_app()
# 约定：蓝图在 run.py 里注册，图片蓝图因路径前缀不同在本文件内注册；
#       异常统一返回 {code, msg}，避免前端拿到 Flask 默认 HTML 错误页。
# ============================================================================
from flask import Flask, jsonify
from flask_cors import CORS 
from app.conf.config import ENSURE_ASCII
from flask_jwt_extended import JWTManager             # JWT 相关模块
from datetime import timedelta
from app.conf.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from werkzeug.exceptions import HTTPException
import traceback

from app.conf.dbconfig import SQLALCHEMY_DATABASE_URI  # 数据库相关
from app.conf.dbconfig import SQLALCHEMY_ECHO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

jwt = JWTManager()  # 初始化JWTManager

db = SQLAlchemy() # 创建数据库的操作对象
ma = Marshmallow() # 初始化 Marshmallow 对象
  

def create_app():
    app = Flask(__name__)  # 构建app
    
    app.json.ensure_ascii = ENSURE_ASCII  # 设置JWT的密钥
    #CORS(app, resources=r'/*')  # 允许所有资源跨域资源共享 
    
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # 设置访问令牌的过期时间
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES)
    
    jwt.init_app(app)  # 初始化app

    from app.api.image_blueprint import image_blueprint  # 注册图片显示蓝图
    app.register_blueprint(image_blueprint, url_prefix="/api/image")

    # 注册业务蓝图：放在工厂里，保证 run.py（开发）、run_prod.py（waitress）、
    # wsgi.py（mod_wsgi）三种入口拿到的 app 都是完整的，不必各自重复注册
    from app.api.user_blueprint import user_blueprint
    from app.api.classics_blueprint import classics_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/api/user")
    app.register_blueprint(classics_blueprint, url_prefix="/api/classics")

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # 载入数据库配置
    app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO
    db.init_app(app)  # 将数据库操作对象绑定到 app
    ma.init_app(app)

    # ========================================================================
    # 全局异常兜底：任何未捕获异常都返回 JSON，而不是 Flask 默认的 HTML 错误页
    #   否则前端 axios 拿到的是 HTML，catch 里看不出到底错在哪
    #   注意：flask_jwt_extended 对 401/422 有自己的处理器（更具体的异常类型），
    #        会优先于这里的 Exception 处理器，不会被吞掉
    # ========================================================================
    @app.errorhandler(Exception)
    def handle_exception(e):
        # HTTP 异常（404/405 等）保持原状态码，但响应体也统一成 JSON
        if isinstance(e, HTTPException):
            # Werkzeug 默认给的是英文 description，这里换成站点统一的中文提示
            msg_map = {404: "请求的接口不存在！", 405: "请求方法不允许！"}
            msg = msg_map.get(e.code, e.description)
            return jsonify({"code": str(e.code), "msg": msg}), e.code
        traceback.print_exc()  # 真正的程序异常：完整堆栈打到终端，前端只拿到一句中文提示
        return jsonify({"code": "500", "msg": "服务器内部错误！"}), 500

    return app