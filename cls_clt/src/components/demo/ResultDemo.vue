<!--
  组件示例：Result 结果页（教材 6.2）
  ----------------------------------------------------------------------------
  作用：演示该组件的常用写法，供教学页 /demo5、/demo 引用。
  约定：纯模板示例，不含脚本、不接后端。
-->
<template>
  <el-row>
    <el-col :sm="12" :lg="6">
      <el-result
        icon="success"
        title="Success Tip"
        sub-title="Please follow the instructions">
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6">
      <el-result
        icon="warning"
        title="Warning Tip"
        sub-title="Please follow the instructions">
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6">
      <el-result
        icon="error"
        title="Error Tip"
        sub-title="Please follow the instructions">
        <template #extra>
          <el-button type="primary">Back</el-button>
        </template>
      </el-result>
    </el-col>
    <el-col :sm="12" :lg="6">
      <el-result icon="info" title="Info Tip">
        <template #sub-title>
          <p>Using slot as subtitle</p>
        </template>
      </el-result>
    </el-col>
  </el-row>
</template>
