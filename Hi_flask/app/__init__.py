from flask import Flask
from flask_cors import CORS 
from app.conf.config import ENSURE_ASCII


def create_app():
    # 构建app
    app = Flask(__name__)    
    
    app.json.ensure_ascii = ENSURE_ASCII # 解决中文乱码问题
    CORS(app, resources=r'/*')  # 允许所有资源跨域   
    
       	
    return app
