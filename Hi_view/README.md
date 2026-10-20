# Hi_view · 教材 6.2.2 类视图（MethodView）

一个最小的 Flask 类视图示例，对应教材 6.2.2 节与图 6.1。

## 一、接口

| 方法 | 地址 | 返回 |
|---|---|---|
| GET | `/hello/<name>` | `Hello, <name>! Go Get!` |
| POST | `/hello/<name>` | `Hello, <name>! Go Post!` |

- `name` 来自 URL 路径，任意字符串，如 `小白`、`Tom`
- 返回纯文本，不是 JSON
- POST 不需要请求体，姓名从 URL 取

## 二、启动

```bash
cd D:\高级网页设计\Hi_view && .venv\Scripts\python.exe app.py
```

> **端口说明**：本示例用 **5497**；`cls_svr` 现用 **5382**，两者端口不同、不冲突，可同时启动。
> 要改端口就改 `app.py` 末尾的 `app.run(port=5497)`。

## 三、测试

浏览器直接打开（GET）：

```
http://127.0.0.1:5497/hello/小白
```

命令行测 POST：

```bash
curl -X POST http://127.0.0.1:5497/hello/小白
```

用 Postman 的话：方法选 POST，URL 填 `http://127.0.0.1:5497/hello/小白`，
Body 选 `none`，Send 即可 —— 姓名在 URL 里，不需要填 body。

## 四、实测结果

| 请求 | 状态码 | 响应 |
|---|---|---|
| `GET /hello/小白` | 200 | `Hello, 小白! Go Get!` |
| `POST /hello/小白` | 200 | `Hello, 小白! Go Post!` |
| `POST /hello/Tom` | 200 | `Hello, Tom! Go Post!` |
| `PUT /hello/小白` | **405** | Method Not Allowed（类里没定义 put） |
| `DELETE /hello/小白` | **405** | Method Not Allowed（类里没定义 delete） |
| `GET /hello/` | **404** | 缺 `<name>` 参数 |

## 五、这段代码在讲什么

```python
class HelloView(MethodView):
    def get(self, name):
        return f"Hello, {name}! Go Get!"

    def post(self, name):
        return f"Hello, {name}! Go Post!"

app.add_url_rule('/hello/<name>', view_func=HelloView.as_view('hello_view'))
```

四个要点：

1. **一个类对应一个 URL**，类里的 `get` / `post` 方法分别处理不同请求方式。
   不用再写 `@app.route(..., methods=['GET', 'POST'])` 再在函数里判断 `request.method`。
2. **类不能直接当视图函数**，必须 `HelloView.as_view('hello_view')` 转成函数。
   括号里的名字是**视图函数名，必须全局唯一**。
3. **URL 里的 `<name>` 会自动传给方法**，所以 `get(self, name)` 的 `name` 不用自己解析。
4. **没定义的方法自动 405**。这是 MethodView 的好处：只开放声明过的方法，
   不像普通函数视图那样容易漏掉方法限制。
