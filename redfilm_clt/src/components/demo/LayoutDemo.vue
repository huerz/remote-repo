<template>
  <!-- 教材 6.2.2 第 1 个组件：Layout 布局
       基于 24 分栏，el-row 组织行、el-col 划分列，span 控制每列占几栏
       （24 / span = 该行几列：24→1 列、12→2 列、8→3 列、6→4 列、4→6 列）
       教材把样式写成全局 style，这里收在 .layout-demo 里，避免影响其它页面的 el-row -->
  <div class="layout-demo">
    <el-row>
      <el-col :span="24"><div class="grid-content ep-bg-purple-dark" /></el-col>
    </el-row>

    <el-row>
      <el-col :span="12"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="12"><div class="grid-content ep-bg-purple-light" /></el-col>
    </el-row>

    <el-row>
      <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="8"><div class="grid-content ep-bg-purple-light" /></el-col>
      <el-col :span="8"><div class="grid-content ep-bg-purple" /></el-col>
    </el-row>

    <el-row>
      <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
      <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
    </el-row>

    <el-row>
      <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="4"><div class="grid-content ep-bg-purple-light" /></el-col>
      <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="4"><div class="grid-content ep-bg-purple-light" /></el-col>
      <el-col :span="4"><div class="grid-content ep-bg-purple" /></el-col>
      <el-col :span="4"><div class="grid-content ep-bg-purple-light" /></el-col>
    </el-row>
  </div>
</template>

<style scoped>
.layout-demo :deep(.el-row) {
  margin-bottom: 20px;
}

.layout-demo :deep(.el-row:last-child) {
  margin-bottom: 0;
}

.layout-demo :deep(.el-col) {
  border-radius: 4px;
}

/* 这几个类不是 Element Plus 自带的，
   是官方 Layout 示例里的配色约定，需要自己定义 */
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.ep-bg-purple-dark {
  background: #99a9bf;
}

.ep-bg-purple {
  background: #d3dce6;
}

.ep-bg-purple-light {
  background: #e5e9f2;
}
</style>
