# Hi_upload · 教材 8.2.1 / 8.2.2 文件上传与下载

项目 8「古典文学网」用户中心模块的**知识储备**示例：Flask 文件上传、`send_file()` 下载、
`send_from_directory()` 下载。对应教材图 8.1～8.4。

## 一、目录结构

```
Hi_upload/
├── app.py              # 视图函数：上传 + 两种下载
├── config.py           # FILE_PATH / ALLOWED_EXTENSIONS
├── requirements.txt    # flask==3.1.3
├── .venv/              # 项目内虚拟环境（Python 3.14.7）
└── upload_file/        # 上传文件存放目录（首次上传自动创建）
```

## 二、接口

| 方法 | 地址 | 说明 |
|---|---|---|
| POST | `/upload` | 上传文件，`form-data`，参数名 **file** |
| GET | `/download/<filename>` | 下载文件（`send_file()` 实现，教材 8.2.2 方式一） |
| GET | `/download-from-dir/<filename>` | 下载文件（`send_from_directory()` 实现，教材 8.2.2 方式二） |

上传返回：

```json
{"code": "200", "msg": "上传成功！", "upFile": "<uuid>.<ext>"}
```

- 允许扩展名：`png / gif / jpg / jpeg / jpe`
- 非法扩展名 → `{"code":"400","msg":"上传失败！"}`
- 未带 file 参数 → `{"code":"404","msg":"文件不存在！"}`
- 文件落盘名 = `uuid4` + 原扩展名，避免重名覆盖

## 三、启动

```bash
cd D:\高级网页设计\Hi_upload && .venv\Scripts\python.exe app.py
```

> **端口说明**：本示例用 **5337**；`cls_svr` 用 5382，两者不冲突，可同时启动。
> 要改端口就改 `app.py` 末尾的 `app.run(port=5337)`。

## 四、测试（对应教材图 8.2 / 8.3 / 8.4）

### 1. 上传（Postman：POST + form-data + key=file）

```bash
curl --noproxy '*' -X POST -F "file=@D:\高级网页设计\images\head\xiaobai.jpg" http://127.0.0.1:5337/upload
```

### 2. 下载方式一（send_file）

```bash
curl --noproxy '*' -OJ "http://127.0.0.1:5337/download/<upFile>"
```

### 3. 下载方式二（send_from_directory）

```bash
curl --noproxy '*' -OJ "http://127.0.0.1:5337/download-from-dir/<upFile>"
```

## 五、实测结果（2026-10-21）

| # | 用例 | 请求 | 结果 |
|---|---|---|---|
| 1 | 上传 jpg | `POST /upload`，xiaobai.jpg 29398 B | **PASS**：200，`upFile=5f5b…jpg`，落盘 29398 B，**SHA256 与源文件一致** |
| 2 | 下载方式一 | `GET /download/5f5b…jpg` | **PASS**：200，29398 B，SHA256 一致，`Content-Disposition: attachment` |
| 3 | 下载方式二 | `GET /download-from-dir/5f5b…jpg` | **PASS**：200，29398 B，SHA256 一致 |
| 4 | 非法扩展名 | `POST /upload`，bad.txt | **PASS**：`code=400` 上传失败 |
| 5 | 缺 file 参数 | `POST /upload` | **PASS**：`code=404` 文件不存在 |
| 6 | 中文文件名 | `POST /upload`，中文头像.jpg | **PASS**：200，`upFile=3207…jpg`（兜底逻辑生效） |
| 7 | 下载不存在文件 | `GET /download/nope.png` | **PASS**：HTTP 404 |

## 六、和教材的 4 处差异（都是有意的）

1. **上传目录**：教材 `FILE_PATH = r'D:\upload_file'`；这里改成项目内 `Hi_upload/upload_file/`，
   不在 D 盘根目录建目录。想完全照教材，把 `config.py` 里 `FILE_PATH` 改回去即可。
2. **两种下载路由分离**：教材两段代码都写 `@app.route('/download/<filename>')`，
   同一路由注册两次会冲突；这里把 `send_from_directory` 版本改成 `/download-from-dir/<filename>`，
   两种实现都能单独测。
3. **中文文件名兜底**：`secure_filename()` 会过滤中文，教材原写法在中文文件名下
   `upname.rsplit('.', 1)[1]` 会越界 500；这里补了扩展名兜底。
4. **端口**：教材 5000；本机统一随机到 5000–5900 段，本示例 5337。

## 七、知识点（对应教材 8.2）

- **上传四步**：`<input type="file">` 提交 → 服务端 `request.files` 取文件 →
  `secure_filename()` 清洗文件名 → `文件.save(路径)` 落盘。
- **`allowed_file()`**：用扩展名白名单校验，`rsplit('.', 1)[1]` 取最后一段扩展名。
- **`uuid4`**：解决同名覆盖，保证每个上传文件唯一。
- **`send_file()`**：需自己拼完整路径；`as_attachment=True` 让浏览器下载而非打开。
- **`send_from_directory()`**：只给「目录 + 文件名」，自带路径安全检查，更推荐。
- **目录遍历防护**：`'..' in filename or filename.startswith('/')` → 400。
