# redfilm_clt（红影赏析 · 前端）

Vue 3 + Vite + Element Plus + TypeScript + Pinia + Vue Router。
对应教材「红影赏析」拓展任务 4.6 / 5.6 / 6.6 / 7.6 / 8.6。

## 一、启动

```bash
cd D:\高级网页设计\redfilm_clt
npm run dev
```

访问 http://localhost:5175
（后端必须先起：`redfilm_svr`，端口 5383）

## 二、代理

`vite.config.ts` 把 `/svr` 转发到 `http://127.0.0.1:5383` 并去掉前缀：

| 前端调用 | 后端实际地址 |
|---|---|
| `/svr/api/films/get-filmtypes` | `http://127.0.0.1:5383/api/films/get-filmtypes` |
| `/svr/api/image/display/film/ac1.jpg` | `http://127.0.0.1:5383/api/image/display/film/ac1.jpg` |

## 三、目录

```
src/
├── components/
│   ├── HeaderComp.vue      顶部导航（Logo + 类型菜单 + 注册登录 / 用户中心）
│   ├── FooterComp.vue      页脚
│   ├── AsideComp.vue       用户中心侧边栏
│   ├── FilmFigures.vue     首页横幅两侧电影元素（摄影机 / 胶片 / 场记板 / 放映机）
│   ├── demo/               教材 6.2.2 组件示例（Layout / Image / Result / Rate）
│   ├── demo5/              教材 5.2.5 组件示例（11 个）
│   └── demo7/              教材 7.2.3 组件示例（Text / Input / Radio / Descriptions）
├── views/
│   ├── HomeView.vue        首页：横幅 → 轮播 → 搜索 → 电影推荐
│   ├── FilmListView.vue    电影列表（按类型）
│   ├── FilmView.vue        电影详情 + 评分 + 影评
│   ├── SearchView.vue      搜索结果
│   ├── RegisterView.vue / LoginView.vue / OutView.vue
│   ├── UserView.vue        个人中心
│   ├── MyDiscussView.vue   我的影评
│   ├── MyPwdView.vue       密码重置
│   └── Demo5View / DemoView / Demo7View  组件示例页
├── router/index.ts         路由表
├── stores/token.ts         Token 状态管理
├── types/index.ts          接口类型定义
└── main.ts                 入口（Element Plus + 图标 + axios/vue-axios）
```

## 四、类型检查

```bash
npm run type-check
```

## 五、说明

- 教材 JS 写法在本项目已全部转 TypeScript，逻辑一致
- 接口返回值统一用 `axios<ApiResult<T>>({...})` 泛型；`ApiResult` / `Film` / `Filmtype` / `RecommendGroup` 定义在 `src/types/index.ts`
- `inject('axios')` 在 strict 下返回 `unknown`，需 `as AxiosInstance`
