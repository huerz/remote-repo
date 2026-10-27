<script setup>
// ============================================================================
// 退出登录（/out）
// ----------------------------------------------------------------------------
// 教材：第六章 §6.3.1 用户退出
// 作用：清空 Token 与本地用户信息后跳回首页。
// 约定：退出只清本地状态，不调用后端注销接口（JWT 无状态）。
// ============================================================================
import { useRouter } from 'vue-router';
// 引入状态管理文件
import { useTokenStore } from '@/stores/token';
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
userStore.setToken(''); // 设置当前登录用户的 Token 为空
const router = useRouter(); // 创建路由对象
router.push('/'); // 退出后，跳转至首页
</script>

<template>
  <el-empty description="退出失败！" />
</template>
