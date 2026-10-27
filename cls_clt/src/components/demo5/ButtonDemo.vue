<!--
  组件示例：Button 按钮（教材 5.2.5）
  ----------------------------------------------------------------------------
  作用：演示该组件的常用写法，供教学页 /demo5、/demo 引用。
  约定：纯模板示例，不含脚本、不接后端。
-->
<template>
  <div class="button-demo">
    <!-- 基础按钮：type 决定语义色 -->
    <el-row class="row">
      <el-button>默认按钮</el-button>
      <el-button type="primary">主要按钮</el-button>
      <el-button type="success">成功按钮</el-button>
      <el-button type="warning">警告按钮</el-button>
      <el-button type="danger">危险按钮</el-button>
      <el-button type="info">信息按钮</el-button>
    </el-row>

    <!-- 朴素按钮 plain -->
    <el-row class="row">
      <el-button plain>默认</el-button>
      <el-button type="primary" plain>主要</el-button>
      <el-button type="success" plain>成功</el-button>
      <el-button type="warning" plain>警告</el-button>
      <el-button type="danger" plain>危险</el-button>
    </el-row>

    <!-- 圆角 / 圆形 / 禁用 -->
    <el-row class="row">
      <el-button type="primary" round>圆角按钮</el-button>
      <el-button type="danger" circle>删</el-button>
      <el-button disabled>禁用按钮</el-button>
      <el-button type="primary" loading>加载中</el-button>
    </el-row>
  </div>
</template>

<style scoped>
.button-demo {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
