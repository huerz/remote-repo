# cls_clt（古典文学网 · 前端）

Vue 3 + Vite + Element Plus + TypeScript + Pinia + Vue Router。

## 一、教材 JS 写法 → 本项目 TS 对照

本项目已全量迁移 TypeScript。教材第 5 章写的是 JS 版，照着做时按下表换一下即可，**逻辑完全一致**。

| 教材（JS 版） | 本项目（TS 版） | 说明 |
|---|---|---|
| `src/main.js` | `src/main.js` | **入口沿用 JS，与教材完全一致**（其余文件为 TS） |
| `vite.config.js` | `vite.config.ts` | 扩展名变了，内容一致 |
| `src/router/index.js` | `src/router/index.ts` | 同上 |
| `src/stores/token.js` | `src/stores/token.ts` | 同上 |
| `jsconfig.json` | `tsconfig.json` | 路径别名 `@/*` 改在 tsconfig 里配 |
| `<script setup>` | `<script setup lang="ts">` | 每个组件都要加 `lang="ts"` |
| `ref('')` | `ref<string>('')` | 加类型参数 |
| `reactive({...})` | `reactive<DataForm>({...})` | 配合 `interface DataForm` |
| `inject('axios')` | `inject('axios') as AxiosInstance` | strict 模式下返回 `unknown`，必须断言 |

> 入口文件 **`src/main.js` 保持 JS 不变**，和教材第 5 章完全一致，可直接对照。
> 其余文件为 TS，照着书上写时，把 `ref('')` 这类加上类型参数即可（不加也能跑）。

## 二、前端接口清单

所有接口都走 Vite 代理前缀 `/svr` → `http://127.0.0.1:5000`（配置见 `vite.config.ts`）。

| 调用位置 | 接口 | 调用方式 | 用途 |
|---|---|---|---|
| `components/HeaderComp.vue` | 图片显示 | `GET /svr/api/image/display/head/logo.png` | 导航栏 Logo、头像 |
| `components/HeaderComp.vue` | 文学导航 | `GET /svr/api/classics/get-classictypes` | 动态导航菜单 |
| `views/HomeView.vue` | 首页轮播 | `GET /svr/api/classics/search-carousels/6` | 轮播图 |
| `views/HomeView.vue` | 文学导航 | `GET /svr/api/classics/get-classictypes` | 推荐区分组标题 |
| `views/HomeView.vue` | 文学搜索 | `POST /svr/api/classics/search-classics` | 传空串取全部，本地分组 |
| `views/SearchView.vue` | 文学搜索 | `POST /svr/api/classics/search-classics` | 按关键字查询 |
| `views/RegisterView.vue` | 用户注册 | `POST /svr/api/user/register` | 注册 |
| `views/LoginView.vue` | 用户登录 | `POST /svr/api/user/login` | 登录并保存 token |
| `components/HeaderComp.vue` | 查询登录用户 | `GET /svr/api/user/get-user` | 取头像、判断登录态 |
| `views/ClassicListView.vue` | 文学列表 | `GET /svr/api/classics/get-classics/:tid` | 按类型列出作品 |
| `views/ClassicView.vue` | 文学作品信息 | `GET /svr/api/classics/get-classic/:cid` | 作品详情 |
| `views/ClassicView.vue` | 文学评价 | `POST /svr/api/classics/judge-classic` | 打分（需 token） |

> 每个调用点上方都有 `【接口 N】` 注释块，写明：接口名 / 前端与后端地址 / 请求参数 / 返回结构。
> 后端接口总览见 `cls_svr/run.py` 文件头。

## 三、常用命令

### 启动顺序（先后端，后前端）

```bash
# 1. 后端：Flask，监听 5000
cd D:\高级网页设计\cls_svr && .venv\Scripts\python.exe run.py

# 2. 前端：Vite，监听 5173
cd D:\高级网页设计\cls_clt && npm run dev
```

> 前端通过 `vite.config.ts` 的代理把 `/svr` 转发到 `127.0.0.1:5000`。
> **后端没起时页面不会报错，但数据全空**（接口返回 502），别误判成前端坏了。

### 前端命令

```sh
npm install          # 安装依赖
npm run dev          # 开发服务（默认 5173）
npm run build        # 生产构建
npm run type-check   # 只做 TypeScript 类型检查（vue-tsc --noEmit）
```

## 四、类型定义位置

`src/types/index.ts`：`Classictype` / `Classic` / `ApiResult<T>` / `RecommendGroup`，与后端表结构一一对应。

## 五、样式文件

| 文件 | 作用 |
|---|---|
| `src/assets/main.css` | 全局基础样式 + Element Plus 主色（朱红） |
| `src/assets/auth.css` | 登录 / 注册页共用视觉：纯色底 + 毛玻璃卡片，类名统一 `auth-` 前缀 |

---

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).
