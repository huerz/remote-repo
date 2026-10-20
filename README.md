# 高级网页设计 · 古典文学网

Flask + Vue 3 前后端分离的古典文学作品展示网站。

## 一、目录结构

| 目录 | 说明 | 端口 |
|---|---|---|
| `cls_svr` | Flask 后端：REST 接口、JWT 鉴权、MySQL | **5382** |
| `cls_clt` | Vue 3 + TypeScript + Element Plus 前端 | **5173** |
| `images` | 共享图集库，各项目共用（详见 `images/README.md`） | — |
| `原始版本_20261020` | 项目 6 改动前的原版复刻，**仅供对照，勿直接运行** | — |
| `Hi_view` | 教材 6.2.2 类视图（MethodView）示例 | **5497（与 cls_svr 5382 不冲突，可并行）** |
| `Hi_db` / `Hi_flask` / `Hi_Jinja2` / `Hi_vue` | 课程其他练习项目 | Hi_db **5663** / Hi_flask **5216** / Hi_Jinja2 **5814** / Hi_vue 5173 |

## 二、启动方式

> **顺序不能反：先起后端，再起前端。** 前端通过 Vite 代理把 `/svr` 转发到 5382，
> 后端没起时页面会"骨架正常、数据全空"。

### 1. 启动后端（先）

```bash
cd D:\高级网页设计\cls_svr && .venv\Scripts\python.exe run.py
```

启动后监听 `http://127.0.0.1:5382`。

### 2. 启动前端（后）

```bash
cd D:\高级网页设计\cls_clt && npm run dev
```

浏览器访问 **http://localhost:5173**

## 三、环境说明

- **Python 一律使用项目内 `.venv`**（3.14.7），不要用全局解释器；`cls_svr / Hi_db / Hi_flask / Hi_Jinja2` 各自有独立 `.venv`
- **Node 22+**，前端依赖已安装，无需重复 `npm install`
- **MySQL 8.4**，库名 `classicsdb`，连接串见 `cls_svr/app/conf/dbconfig.py`
- 前端类型检查：`cd cls_clt && npm run type-check`

## 四、常用访问地址

| 地址 | 说明 |
|---|---|
| http://localhost:5173/ | 首页 |
| http://localhost:5173/search/all | 搜索结果页（全部作品） |
| http://localhost:5173/clslist/4 | 文学列表（4 = 唐诗，换成其他 tid 即对应分类） |
| http://localhost:5173/cls/2/4 | 文学作品展示（作品编号 / 类型编号） |
| http://localhost:5173/register | 注册 |
| http://localhost:5173/login | 登录（演示账号 `xiaobai` / `123456`） |
| http://localhost:5173/out | 退出登录（清 Token 后回首页） |

## 五、常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 页面能开，但轮播/导航/推荐区全空 | 后端没起，`/svr` 代理返回 **502** | 按上面第 1 步启动 `cls_svr` |
| 页面完全打不开 | 前端没起 | 按上面第 2 步启动 `cls_clt` |
| 控制台报 `Network Error` | 后端进程退出 | 同上，重启后端 |
| 书封显示为空白卡片 | 该作品在数据库里没有封面文件名 | 补图到 `images/books/<类型>/`，再把文件名写入 `classics.cover` |

> 判断技巧：F12 控制台里看到 `GET /svr/api/... 502 (Bad Gateway)`，就是后端没启动，不是前端代码问题。

## 六、接口文档位置

- 全局接口总览：`cls_svr/run.py` 文件头
- 单个蓝图接口清单：`cls_svr/app/api/*_blueprint.py` 文件头
- 前端调用位置与注释：`cls_clt/README.md` 的「前端接口清单」
