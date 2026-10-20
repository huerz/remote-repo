import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import SearchView from '@/views/SearchView.vue'
// 文学列表页、文学作品展示页、退出页
import ClassicListView from '@/views/ClassicListView.vue'
import ClassicView from '@/views/ClassicView.vue'
import OutView from '@/views/OutView.vue'

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
      // 文学列表：/clslist/4 → 唐诗
      path: '/clslist/:tid',
      name: 'clslist',
      component: ClassicListView
    },
    {
      // 文学作品展示：/cls/2/4 → 唐诗分类下的第 2 部作品
      path: '/cls/:cid/:tid',
      name: 'cls',
      component: ClassicView
    },
    {
      // 退出登录：清 Token 后跳回首页
      path: '/out',
      name: 'out',
      component: OutView
    }
  ]
})

export default router