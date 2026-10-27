<script lang="ts" setup>
// 图标已在 main.ts 里全局注册，模板中可直接写 <Edit /> <Search /> 等；
// 作为 el-button 的 icon 属性传入时需要先 import 成组件变量
import { Search, Edit, Delete } from '@element-plus/icons-vue'
</script>

<template>
  <div class="icon-demo">
    <!-- 基础用法：尺寸由外层 font-size 决定 -->
    <el-icon><Edit /></el-icon>
    <el-icon><Search /></el-icon>
    <el-icon><Delete /></el-icon>

    <!-- 自定义尺寸与颜色 -->
    <el-icon :size="24" color="#a8352c"><Search /></el-icon>
    <el-icon :size="32" color="#8a6a45"><Edit /></el-icon>

    <!-- 配合按钮使用 -->
    <el-button type="primary" :icon="Search">搜索</el-button>
    <el-button :icon="Edit" plain>编辑</el-button>
  </div>
</template>

<style scoped>
.icon-demo {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  font-size: 20px;
  color: #5a3a22;
}
</style>
