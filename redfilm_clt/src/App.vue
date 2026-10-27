<script setup lang="ts">
import { RouterView } from 'vue-router'
// 右下角浮动的「回到顶部 / 滚到底部」按钮（全局一份，所有页面都有）
import ScrollNav from '@/components/ScrollNav.vue'
</script>

<template>
  <RouterView />
  <ScrollNav />
</template>
