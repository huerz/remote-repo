<script lang="ts" setup>
import { ElMessage } from 'element-plus'

// 消息提示：函数式调用，不写在模板里
function openDefault() {
  ElMessage('这是一条默认消息')
}

function openSuccess() {
  ElMessage({ message: '操作成功', type: 'success' })
}

function openWarning() {
  ElMessage({ message: '请注意检查输入内容', type: 'warning' })
}

function openError() {
  ElMessage({ message: '操作失败，请重试', type: 'error', duration: 5000 })
}

function openPlain() {
  ElMessage({ message: '朴素风格', type: 'info', plain: true })
}
</script>

<template>
  <div class="message-demo">
    <el-button @click="openDefault">默认消息</el-button>
    <el-button type="success" @click="openSuccess">成功</el-button>
    <el-button type="warning" @click="openWarning">警告</el-button>
    <el-button type="danger" @click="openError">错误（5 秒）</el-button>
    <el-button plain @click="openPlain">朴素</el-button>
  </div>
</template>

<style scoped>
.message-demo {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
