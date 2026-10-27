# hi_flash · 教材 7.2.1 中间件 / 7.2.2 消息闪现

项目 7「古典文学网」书评模块的知识储备示例：Flask 中间件（`SimpleMiddleware`）与
消息闪现（`flash` / `get_flashed_messages`）。对应教材图 7.1。

## 一、目录结构

```
hi_flash/
├── app.py                 # 7.2.2 消息闪现实例（/ 与 /login）
├── SimpleMiddleware.py    # 7.2.1 中间件类
├── templates/
│   ├── login.html         # 登录页（表单 + 错误提示）
│   └── index.html         # 首页（显示闪现消息）
├── requirements.txt       # flask==3.1.3
└── .venv/                 # 项目内虚拟环境（Python 3.14.7）
```

## 二、7.2.1 Flask 中间件

`SimpleMiddleware` 在请求处理前后各插入一段逻辑：

```python
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 请求处理前的操作
        response = self.app(environ, start_response)
        # 请求处理后的操作
        return response
```

挂到应用上（教材原文）：

```python
from flask import Flask
from SimpleMiddleware import SimpleMiddleware

app = Flask(__name__)
# 将中间件添加到 Flask 应用
app.wsgi_app = SimpleMiddleware(app.wsgi_app)
```

## 三、7.2.2 消息闪现

- `POST /login`：内置账号 **admin** / 密码 **123456**
  - 成功 → `flash('您已成功登录！')` + `redirect(url_for('index'))`
  - 失败 → 回到登录页并显示 `error`
- `GET /`：`get_flashed_messages()` 取出一次性消息并显示

## 四、启动

```bash
cd D:\高级网页设计\hi_flash && .venv\Scripts\python.exe app.py
```

> **端口说明**：本示例用 **5741**；与 cls_svr(5382)、Hi_upload(5337) 等都不冲突。
> 要改端口就改 `app.py` 末尾的 `app.run(port=5741)`。

## 五、测试

1. 浏览器打开 `http://127.0.0.1:5741/` → 首页，显示"您想要 登录？"
2. 打开 `http://127.0.0.1:5741/login` → 输入 admin / 123456 → 提交
3. 自动跳回首页，页面顶部出现 **您已成功登录！**（刷新一次后消失，这就是"一次性"）

命令行：

```bash
# 错误密码：留在登录页并显示 Error
curl --noproxy '*' -s -X POST -d "uname=admin&upwd=wrong" http://127.0.0.1:5741/login | grep -i error

# 正确密码：302 跳转，随后访问首页能看到闪现消息
curl --noproxy '*' -s -i -X POST -d "uname=admin&upwd=123456" http://127.0.0.1:5741/login | head -5
```

## 六、按书本原样保留的 2 个教材问题

1. **登录判断用了 `and`**：`if uname != 'admin' and upwd != '123456'`。
   结果是"账号对、密码错"也会登录成功（应为 `or`）。按教材原样保留。
2. **`login.html` 里 `<p>` 没有闭合**：`<p><strong>Error:</strong> {{ error }}`。
   浏览器会容错，按教材原样保留。
