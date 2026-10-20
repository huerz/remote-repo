# ============================================================================
# Hi_view 接口清单（教材 6.2.2 类视图 MethodView 示例）
# ----------------------------------------------------------------------------
#   GET  /hello/<name>    返回 "Hello, <name>! Go Get!"
#   POST /hello/<name>    返回 "Hello, <name>! Go Post!"
#
#   路径参数：name —— 任意字符串，如 小白、Tom
#   返回类型：纯文本（text/html，不是 JSON）
#   请求体：POST 不需要传任何数据，姓名从 URL 里取
# ----------------------------------------------------------------------------
# 调用方式（前端没有页面，直接用浏览器 / Postman / curl）：
#   GET  http://127.0.0.1:5497/hello/小白
#   POST http://127.0.0.1:5497/hello/小白
#   curl -X POST http://127.0.0.1:5497/hello/小白
# ----------------------------------------------------------------------------
# 核心知识点：
#   1) MethodView 让"一个 URL 对应一个类"，类里的 get/post 方法分别处理不同请求方式
#   2) 类不能直接当视图函数用，必须 HelloView.as_view('hello_view') 转成函数
#   3) 参数 name 来自 URL 规则 /hello/<name>，会自动传给 get(self, name) / post(self, name)
#   4) as_view() 里的 'hello_view' 是视图函数名，必须全局唯一
# ----------------------------------------------------------------------------
# 启动：.venv\Scripts\python.exe app.py
# 注意：本示例占用 5497 端口；cls_svr 现用 5382，两者不冲突，可并行启动
# ============================================================================

from flask.views import MethodView
from flask import Flask

app = Flask(__name__)


# 定义类视图：继承 MethodView，一个方法对应一种请求方式
class HelloView(MethodView):
    # 处理 GET 请求
    def get(self, name):
        return f"Hello, {name}! Go Get!"

    # 处理 POST 请求
    def post(self, name):
        return f"Hello, {name}! Go Post!"


# 将类视图添加到路由上
# 如果不写 name，也可以使用其他名称，如 'hello_view'、'view_func_hello_view' 等
app.add_url_rule('/hello/<name>', view_func=HelloView.as_view('hello_view'))

if __name__ == '__main__':
    # 设置主机 IP 和端口
    app.run(host='127.0.0.1', port=5497, debug=True)
