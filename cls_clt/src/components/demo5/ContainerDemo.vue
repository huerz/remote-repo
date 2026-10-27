<!--
  组件示例：Container 布局容器（教材 5.2.5）
  ----------------------------------------------------------------------------
  作用：演示该组件的常用写法，供教学页 /demo5、/demo 引用。
  约定：纯模板示例，不含脚本、不接后端。
-->
<template>
  <!-- Container 布局容器：header / main / footer 三段式 -->
  <el-container class="layout-demo">
    <el-header>Header</el-header>
    <el-main>Main</el-main>
    <el-footer>Footer</el-footer>
  </el-container>
</template>

<style scoped>
.layout-demo {
  border: 1px solid #e6d8bf;
  border-radius: 4px;
  overflow: hidden;
}

.layout-demo :deep(.el-header),
.layout-demo :deep(.el-footer) {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f6ecdc;
  color: #5a3a22;
}

.layout-demo :deep(.el-main) {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  background: #fdfaf4;
  color: #8a6a45;
}
</style>
