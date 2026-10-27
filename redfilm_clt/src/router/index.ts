import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import SearchView from '@/views/SearchView.vue'
// 电影列表页、电影展示页、退出页
import FilmListView from '@/views/FilmListView.vue'
import FilmView from '@/views/FilmView.vue'
import OutView from '@/views/OutView.vue'
// 个人中心（教材 8.2：个人信息展示 / 头像上传 / 个人信息修改）
import UserView from '@/views/UserView.vue'
// 我的影评、密码重置（教材 8.3）
import MyDiscussView from '@/views/MyDiscussView.vue'
import MyPwdView from '@/views/MyPwdView.vue'
// 组件示例页（教材 5.2.5：Element Plus 常用组件 11 个）
import Demo5View from '@/views/Demo5View.vue'
// 组件示例页（教材 6.2 图 6.3 / 6.4 / 6.5）
import DemoView from '@/views/DemoView.vue'
// 组件示例页（教材 7.2.3 图 7.3 / 7.4 / 7.5）
import Demo7View from '@/views/Demo7View.vue'
// 404 兜底页
import NotFoundView from '@/views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search/:keyword',
      name: 'search',
      component: SearchView
    },
    {
      // 电影列表：/filmlist/4 → 动画片
      path: '/filmlist/:tid',
      name: 'filmlist',
      component: FilmListView
    },
    {
      // 电影展示：/film/2/4 → 动画片分类下的第 2 部影片
      path: '/film/:cid/:tid',
      name: 'cls',
      component: FilmView
    },
    {
      // 个人中心：个人信息展示 / 头像上传 / 个人信息修改（教材 8.2）
      path: '/user',
      name: 'user',
      component: UserView
    },
    {
      // 我的影评：显示当前登录用户发表的影评（教材 8.3.4）
      path: '/mydis',
      name: 'mydis',
      component: MyDiscussView
    },
    {
      // 密码重置：输入旧密码 / 新密码（教材 8.3.5）
      path: '/mypwd',
      name: 'mypwd',
      component: MyPwdView
    },
    {
      // 组件示例：Container / Icon / Form / Button / Avatar / Card /
      //          Carousel / Menu / PageHeader / Message / Divider（教材 5.2.5）
      path: '/demo5',
      name: 'demo5',
      component: Demo5View
    },
    {
      // 组件示例：Image 预览 / Result / Rate（教材 6.2）
      path: '/demo',
      name: 'demo',
      component: DemoView
    },
    {
      // 组件示例：Text / Input / Radio（教材 7.2.3）
      path: '/demo7',
      name: 'demo7',
      component: Demo7View
    },
    {
      // 退出登录：清 Token 后跳回首页
      path: '/out',
      name: 'out',
      component: OutView
    },
    {
      // 404 兜底：必须放在最后，匹配所有未定义路径，
      // 否则访问不存在的地址会渲染成一片空白
      path: '/:pathMatch(.*)*',
      name: 'notfound',
      component: NotFoundView
    }
  ]
})

export default router