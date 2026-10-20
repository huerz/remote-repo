<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
// 引入状态管理文件
import { useTokenStore } from '@/stores/token'

// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 创建路由对象
const router = useRouter()

// 放在 onMounted 里执行：setup 阶段直接 router.push 是在组件挂载前触发导航，
// 容易与当前渲染流程打架（会报「Redirected when going from ...」之类的警告）
onMounted(() => {
  // 设置当前登录用户的 Token 为空（清除登录态，同时清掉 localStorage）
  userStore.setToken('')
  // 退出后，跳转至首页
  router.push('/')
})
</script>

<template>
  <!-- 跳转过程中短暂显示，正常情况用户几乎看不到 -->
  <el-empty description="已退出登录，正在返回首页…" />
</template>
