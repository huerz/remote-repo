<script lang="ts" setup>
import { useRouter } from 'vue-router'
// 引入状态管理文件
import { useTokenStore } from '@/stores/token'
// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 设置当前登录用户的 Token 为空
userStore.setToken('')
// 创建路由对象
const router = useRouter()
// 退出后，跳转至首页
router.push('/')
</script>

<template>
  <el-empty description="退出失败！" />
</template>
