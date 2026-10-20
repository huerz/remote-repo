from flask import Flask
from flask_cors import CORS 
from app.conf.config import ENSURE_ASCII
from flask_jwt_extended import JWTManager             # JWT 相关模块
from datetime import timedelta
from app.conf.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES

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
    
    return app