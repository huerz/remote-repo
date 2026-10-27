// ============================================================================
// 路由表
// ----------------------------------------------------------------------------
// 作用：声明全部页面路由（首页 / 列表 / 详情 / 搜索 / 登录注册 / 个人中心）。
// 约定：跳转统一用 name，不硬编码 path；带参路由的参数在组件里用 route.params 取。
// ============================================================================
import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import SearchView from '@/views/SearchView.vue'
// 文学列表页、文学作品展示页、退出页
import ClassicListView from '@/views/ClassicListView.vue'
import ClassicView from '@/views/ClassicView.vue'


import OutView from '@/views/OutView.vue'   // 个人中心（教材 8.2：个人信息展示 / 头像上传 / 个人信息修改）

import UserView from '@/views/UserView.vue'
// 我的书评、密码重置（教材 8.3）
import MyDiscussView from '@/views/MyDiscussView.vue'
import MyPwdView from '@/views/MyPwdView.vue'
import Demo5View from '@/views/Demo5View.vue'  // 组件示例页（教材 5.2.5：Element Plus 常用组件 11 个）
import DemoView from '@/views/DemoView.vue'  // 组件示例页（教材 6.2 图 6.3 / 6.4 / 6.5）
import Demo7View from '@/views/Demo7View.vue'  // 组件示例页（教材 7.2.3 图 7.3 / 7.4 / 7.5）
import NotFoundView from '@/views/NotFoundView.vue'  // 404 兜底页

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
      path: '/clslist/:tid',  // 文学列表：/clslist/4 → 唐诗
      name: 'clslist',
      component: ClassicListView
    },
    {
      path: '/cls/:cid/:tid',  // 文学作品展示：/cls/2/4 → 唐诗分类下的第 2 部作品
      name: 'cls',
      component: ClassicView
    },
    {
      path: '/user',  // 个人中心：个人信息展示 / 头像上传 / 个人信息修改（教材 8.2）
      name: 'user',
      component: UserView
    },
    {
      path: '/mydis',  // 我的书评：显示当前登录用户发表的书评（教材 8.3.4）
      name: 'mydis',
      component: MyDiscussView
    },
    {
      path: '/mypwd',  // 密码重置：输入旧密码 / 新密码（教材 8.3.5）
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
      path: '/demo',  // 组件示例：Image 预览 / Result / Rate（教材 6.2）
      name: 'demo',
      component: DemoView
    },
    {
      path: '/demo7',  // 组件示例：Text / Input / Radio（教材 7.2.3）
      name: 'demo7',
      component: Demo7View
    },
    {
      path: '/out',  // 退出登录：清 Token 后跳回首页
      name: 'out',
      component: OutView
    },
    {
      // 404 兜底：必须放在最后，匹配所有未定义路径，
      path: '/:pathMatch(.*)*',  // 否则访问不存在的地址会渲染成一片空白
      name: 'notfound',
      component: NotFoundView
    }
  ]
})

export default router