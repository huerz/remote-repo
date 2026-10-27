# cls_svr — 古典文学网后端（Flask）

接口前缀 `/api`，端口 `5382`，数据库 MySQL `classicsdb`。
前端 `cls_clt`（Vite，5173）通过代理前缀 `/svr` 转发到本服务。

## 目录结构

```
cls_svr/
├─ app/                     Flask 应用包（业务代码只放这里）
│  ├─ __init__.py           应用工厂 create_app()：JWT / DB / Marshmallow / 蓝图注册 / 全局异常
│  ├─ api/                  蓝图：user_blueprint、classics_blueprint、image_blueprint
│  ├─ conf/                 config.py（JWT、图片根路径）、dbconfig.py（数据库连接）
│  ├─ dao/                  ClassicsDao、UsersDao —— 只跟数据库打交道
│  ├─ model/                SQLAlchemy 模型（Poem、Classics、Discuss、Users …）
│  └─ data/poems/           诗词 JSON 数据源（seed_poems.py 的输入，见该目录 README）
├─ scripts/                 数据脚本（可反复执行，均支持 --dry-run）
│  ├─ seed_poems.py         app/data/poems/*.json → poem 表
│  ├─ seed_discuss.py       示例书评 → discuss 表，并校准 classics.commentscount
│  └─ seed_summary.py       作品简介 → classics.summary
├─ deploy/                  部署运维脚本
│  └─ switch_to_mod_wsgi.py httpd.conf 在 mod_proxy / mod_wsgi 两种方案间切换（--revert 回滚）
├─ run.py                   开发入口：Flask 内置服务器 + 热重载
├─ run_prod.py              生产入口：waitress，8 线程，只绑 127.0.0.1
├─ wsgi.py                  mod_wsgi 入口：Apache 直接加载，导出 application
└─ requirements.txt         依赖锁定（Python 3.14.7 虚拟环境）
```

`wsgi.py` 必须留在根目录：`httpd.conf` 的 `WSGIScriptAlias` 和 `deploy/switch_to_mod_wsgi.py`
都按 `cls_svr/wsgi.py` 这个绝对路径写死，挪位置会让 mod_wsgi 加载失败。

## 三种入口，按场景选一个

| 场景 | 命令 | 说明 |
|---|---|---|
| 日常开发 | `.venv\Scripts\python.exe run.py` | 改代码自动重载，`debug=True` |
| 生产（waitress） | `.venv\Scripts\python.exe run_prod.py` | 配合 Apache 反向代理 `:8088` |
| 生产（mod_wsgi） | 跑 `启用mod_wsgi.bat` | Apache 自己加载，不用另起 Python 进程 |

后两种二选一，不要同时开——会抢 `5382` 端口。

## 常用命令

```bash
cd cls_svr

# 装依赖
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 灌数据（--dry-run 先看一眼，确认无误再去掉）
.venv\Scripts\python.exe scripts\seed_poems.py --dry-run
.venv\Scripts\python.exe scripts\seed_poems.py
.venv\Scripts\python.exe scripts\seed_discuss.py --dry-run
.venv\Scripts\python.exe scripts\seed_summary.py --dry-run

# 冒烟测试
curl --noproxy '*' http://127.0.0.1:5382/api/classics/get-classictypes

# 部署方式切换 / 回滚
.venv\Scripts\python.exe deploy\switch_to_mod_wsgi.py
.venv\Scripts\python.exe deploy\switch_to_mod_wsgi.py --revert
```

脚本内部已把项目根加入 `sys.path`，**在任何目录执行都能跑**，不必先 `cd cls_svr`。

## 请求链路

```
浏览器 → cls_clt (Vite :5173, /svr 代理)
       → Apache :8088（mod_proxy 或 mod_wsgi）
       → Flask :5382 → 蓝图 → DAO → MySQL classicsdb
```

图片不走 Flask 转发，`image_blueprint` 按文件名在
`D:/高级网页设计/images/books/<分类>/` 下查找后直接返回。

## 约定

- 蓝图统一在 `create_app()` 里注册，三个入口共享同一份注册逻辑，不要在入口文件里重复注册。
- 接口异常统一返回 `{code, msg}` JSON，不返回 Flask 默认 HTML 错误页。
- 数据只从 `scripts/seed_*.py` 写入，接口层只读表、不读 JSON。
- `.venv/`、`__pycache__/`、`*.bak-*` 的忽略规则在仓库根 `.gitignore`，版本留痕交给 git，
  目录内不再放 `.bak` 副本（历史副本已移到 `../_archive/cls_svr_bak_20261021/`）。
