# 红影赏析 · 拓展任务（教材 1.6–8.6）

《Python Web 全栈开发项目式教程（慕课版）》「红影赏析」同步练习项目，与「古典文学网」同构：
**Flask + Vue 3 + TypeScript + Element Plus + MySQL**，前后端分离。

> 对应关系：文学 → 电影 / 类型 → 电影类型 / 作品 → 影片 / 书评 → 影评

---

## 一、目录与端口

| 目录 | 说明 | 端口 |
|---|---|---|
| `redfilm_svr` | Flask 后端：REST 接口、JWT 鉴权、MySQL（库 `redfilmdbs`） | **5383** |
| `redfilm_clt` | Vue 3 + TypeScript + Element Plus 前端 | **5175** |
| `电影海报` | 电影海报，按类型分 6 个子目录（**独立文件夹，直接打开即可替换**） | — |
| `images/head` | 头像与 Logo（`redfilm_logo.png` 为本项目 Logo） | — |

## 二、首次运行（三步）

### 1. 数据库（二选一，已自动处理）

后端启动时会自动探测：

| 情况 | 实际使用 |
|---|---|
| MySQL 已起且 `redfilmdbs` 库存在 | MySQL（教材标准配置） |
| MySQL 没起 / 库不存在 | **自动改用同目录 `redfilmdbs.db`（SQLite）**，开箱即有 36 部电影 |

所以**什么都不做也能直接跑出完整页面**。想切到 MySQL 再执行：

```bash
mysql -u root -p < D:\高级网页设计\redfilm_svr\redfilmdbs.sql
```

或用 Navicat / DBeaver 打开 `redfilm_svr/redfilmdbs.sql` 直接执行。

脚本会建库 `redfilmdbs`、建 6 张表、灌入 **6 个电影类型 + 36 部电影 + 1 个演示账号 + 2 条示例影评**。
演示账号：**xiaobai / 123456**

> SQLite 兜底库已预置数据；若想重建，删掉 `redfilmdbs.db` 后执行
> `.venv\Scripts\python.exe seed_sqlite.py`

### 2. 启动后端（先）

```bash
cd D:\高级网页设计\redfilm_svr
.venv\Scripts\python.exe run.py
```

监听 `http://127.0.0.1:5383`。首次运行 `.venv` 已装好依赖，无需重装。

### 3. 启动前端（后）

```bash
cd D:\高级网页设计\redfilm_clt
npm run dev
```

浏览器访问 **http://localhost:5175**

> 顺序不能反：前端通过 Vite 代理把 `/svr` 转发到 5383，后端没起时页面「骨架正常、数据全空」。

## 三、接口清单（前缀 `/api`）

### 用户 `/api/user`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/register` | 注册 |
| POST | `/login` | 登录，返回 JWT |
| GET | `/get-user` | 查登录用户（需 JWT） |
| POST | `/upload` | 上传头像，字段名 `file` |
| POST | `/update-user` | 改资料（需 JWT） |
| POST | `/update-pwd` | 改密码（需 JWT） |
| GET | `/protected` | 鉴权测试（需 JWT） |

### 电影 `/api/films`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/get-filmtypes` | 电影类型（导航栏） |
| GET | `/search-carousels/<n>` | 轮播图，按评分倒序取前 n 条 |
| GET | `/recommend-films/<n>` | 按类型分组推荐，每类 n 部 |
| POST | `/search-films` | 搜索，请求体 `{"keyword": "..."}` |
| GET | `/get-films/<tid>` | 某类型的电影列表 |
| GET | `/get-film/<cid>` | 单部电影详情 |
| POST | `/judge-film` | 电影评分（需 JWT） |
| GET | `/get-discuss/<cid>` | 影评列表 |
| POST | `/pub-discuss` | 发表影评（需 JWT） |
| POST | `/judge-discuss` | 影评顶/踩（需 JWT） |
| GET | `/get-mydiscuss` | 我的影评（需 JWT） |

### 图片 `/api/image`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/display/film/<文件名>` | 电影海报，自动在类型子目录里找 |
| GET | `/display/head/<文件名>` | 头像 / Logo |

## 四、页面路由

| 地址 | 页面 |
|---|---|
| `/` | 首页：横幅 + 搜索 + 轮播 + 电影推荐 |
| `/search/:keyword` | 搜索结果（`all` 表示全部） |
| `/filmlist/:tid` | 电影列表（按类型） |
| `/film/:cid/:tid` | 电影详情 + 评分 + 影评 |
| `/register`、`/login`、`/out` | 注册 / 登录 / 退出 |
| `/user` | 个人中心（资料、头像上传） |
| `/mydis` | 我的影评 |
| `/mypwd` | 密码重置 |
| `/demo5` | 教材 5.2.5 组件示例（11 个） |
| `/demo` | 教材 6.2.2 组件示例（4 个） |
| `/demo7` | 教材 7.2.3 组件示例（4 个） |

## 五、拓展任务覆盖（教材 1.6–8.6）

| 章节 | 任务 | 落地 |
|---|---|---|
| 1.6 | 1.6.1 WBS 图、1.6.2 环境 | 见本文件「一、二」 |
| 2.6 | 2.6.1 后端框架、2.6.2 注册 API、2.6.3 登录 API、2.6.4 图片显示 API | `user_blueprint.py`、`image_blueprint.py` |
| 3.6 | 3.6.1 数据库模块、3.6.2 完善注册登录、3.6.3 导航 API、3.6.4 推荐 API、3.6.5 搜索 API、3.6.6 轮播图 API | `FilmsDao.py`、`films_blueprint.py` |
| 4.6 | 4.6.1 前端框架、4.6.2 Token 管理、4.6.3 跨域、4.6.4 路由 | `main.ts`、`stores/token.ts`、`vite.config.ts`、`router/index.ts` |
| 5.6 | 5.6.1 导航栏、5.6.2 轮播、5.6.3 搜索、5.6.4 推荐、5.6.5 注册登录 | `HomeView`、`HeaderComp`、`RegisterView`、`LoginView` |
| 6.6 | 6.6.1 用户中心显示、6.6.2 退出、6.6.3 列表、6.6.4 详情、6.6.5 评价 | `HeaderComp`、`OutView`、`FilmListView`、`FilmView` |
| 7.6 | 7.6.1 影评展示、7.6.2 发表、7.6.3 评价 | `FilmView` + `discuss` 系列接口 |
| 8.6 | 8.6.1 个人资料、8.6.2 头像上传、8.6.3 资料修改、8.6.4 我的影评、8.6.5 密码重置 | `UserView`、`MyDiscussView`、`MyPwdView` |

## 六、数据说明

- 电影海报：**36 张全部为 TMDB 官方原版海报**（780×1170 下载，统一裁成 600×900）
- 海报统一裁成 600×900（2:3），放在 `电影海报/<类型>/` 下
- 若想换图，按下面的对照表把同名文件丢进 `D://高级网页设计//电影海报//<类型>//` 覆盖即可（**不用改数据库**）

### 海报文件名对照表

| 类型 | 文件 → 电影 | 文件 → 电影 | 文件 → 电影 | 文件 → 电影 | 文件 → 电影 | 文件 → 电影 |
|---|---|---|---|---|---|---|
| 动作片 | ac1 战狼2 | ac2 湄公河行动 | ac3 红海行动 | ac4 英雄本色 | ac5 碟中谍6 | ac6 叶问 |
| 科幻片 | kh1 流浪地球 | kh2 星际穿越 | kh3 盗梦空间 | kh4 火星救援 | kh5 阿凡达 | kh6 黑客帝国 |
| 剧情片 | jq1 肖申克的救赎 | jq2 霸王别姬 | jq3 活着 | jq4 阿甘正传 | jq5 我不是药神 | jq6 教父 |
| 动画片 | dh1 千与千寻 | dh2 哪吒之魔童降世 | dh3 疯狂动物城 | dh4 龙猫 | dh5 蜘蛛侠：平行宇宙 | dh6 寻梦环游记 |
| 喜剧片 | xj1 让子弹飞 | xj2 夏洛特烦恼 | xj3 疯狂的石头 | xj4 唐伯虎点秋香 | xj5 三傻大闹宝莱坞 | xj6 功夫 |
| 悬疑片 | xy1 看不见的客人 | xy2 沉默的羔羊 | xy3 七宗罪 | xy4 调音师 | xy5 无双 | xy6 记忆碎片 |

> 换成豆瓣导出的图也可以，系统对尺寸没有硬要求——卡片按容器宽度铺满，比例不一致只会让高度略有差异。

- 海报来源：TMDB（The Movie Database）官方接口，`/search/movie` 查 `poster_path`，再从 `image.tmdb.org/t/p/w780` 下载
- 数据库 `films` 表沿用教材字段名：`title` 片名、`author` 导演、`present` 主演、`year` 年份、`rating` 评分、`commentscount` 影评数
- 类型头像复用 `images/head/hfzy.png`
- 类型圆标：`images/head/t1-t6.png`（武/星/情/画/喜/疑）

## 七、常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 页面能开，但导航只有「首页」、轮播区空白 | 后端没起或数据库没导入 | 先启后端，再执行 `redfilmdbs.sql` |
| 控制台 `502 (Bad Gateway)` | 后端进程没起 | 启动 `redfilm_svr` |
| 海报显示为空白 | 该影片 `cover` 文件名与 `images/films` 里不一致 | 核对文件名 |
| 端口冲突 | 5175 / 5383 被占用 | 改 `vite.config.ts` 的 `port` 与 `run.py` 的端口，两处要一致 |
