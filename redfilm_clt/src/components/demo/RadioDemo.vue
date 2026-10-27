<template>
  <el-radio-group v-model="radio">
    <el-radio :value="3">Option A</el-radio>
    <el-radio :value="6">Option B</el-radio>
    <el-radio :value="9">Option C</el-radio>
  </el-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

// 教材只给了模板，没给脚本；按图 7.5 的效果默认选中 Option B（value = 6）
const radio = ref(6)
</script>
