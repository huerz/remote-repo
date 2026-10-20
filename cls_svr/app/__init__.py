from flask import Flask, jsonify
from flask_cors import CORS 
from app.conf.config import ENSURE_ASCII
from flask_jwt_extended import JWTManager             # JWT 相关模块
from datetime import timedelta
from app.conf.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from werkzeug.exceptions import HTTPException
import traceback

# 数据库相关
from app.conf.dbconfig import SQLALCHEMY_DATABASE_URI
from app.conf.dbconfig import SQLALCHEMY_ECHO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# 初始化JWTManager
jwt = JWTManager()

db = SQLAlchemy() # 创建数据库的操作对象
ma = Marshmallow() # 初始化 Marshmallow 对象
  

def create_app():
    # 构建app
    app = Flask(__name__)    
    
    #设置JWT的密钥
    app.json.ensure_ascii = ENSURE_ASCII 
    #CORS(app, resources=r'/*')  # 允许所有资源跨域资源共享 
    
    # 设置访问令牌的过期时间
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES)
    
    # 初始化app
    jwt.init_app(app)

    # 注册图片显示蓝图
    from app.api.image_blueprint import image_blueprint
    app.register_blueprint(image_blueprint, url_prefix="/api/image")

    # 载入数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO
    # 将数据库操作对象绑定到 app
    db.init_app(app)
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
        # 真正的程序异常：完整堆栈打到终端，前端只拿到一句中文提示
        traceback.print_exc()
        return jsonify({"code": "500", "msg": "服务器内部错误！"}), 500

    return app