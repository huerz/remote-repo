# -*- coding: utf-8 -*-
"""
教材 7.2.1 Flask 框架的中间件

用法（教材原文）：
    from flask import Flask
    from SimpleMiddleware import SimpleMiddleware

    app = Flask(__name__)
    # 将中间件添加到 Flask 应用
    app.wsgi_app = SimpleMiddleware(app.wsgi_app)

说明：教材用 ...... 表示「省略的业务代码」，Python 里不能直接写 ......，
      这里改成注释占位，逻辑与教材一致。
"""


class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 请求处理前的操作
        # ......
        response = self.app(environ, start_response)
        # 请求处理后的操作
        # ......
        return response
