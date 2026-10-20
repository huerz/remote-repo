<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <div>
    <RouterLink to="/home">首页</RouterLink>
    <RouterLink to="/about">关于页</RouterLink>
    <RouterLink to="/users/102">用户中心</RouterLink>
  </div>
  <br />
  <RouterView />
</template>
