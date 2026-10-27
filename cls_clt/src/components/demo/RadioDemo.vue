<template>
  <el-radio-group v-model="radio">
    <el-radio :value="3">Option A</el-radio>
    <el-radio :value="6">Option B</el-radio>
    <el-radio :value="9">Option C</el-radio>
  </el-radio-group>
</template>

<script setup>
// ============================================================================
// 组件示例：Radio（教材 6.2）
// ----------------------------------------------------------------------------
// 作用：演示该组件的常用写法，供教学页 /demo5、/demo、/demo7 引用。
// 约定：示例组件不接后端、不含业务状态，改动只影响演示页。
// ============================================================================
import { ref } from 'vue';
// 教材只给了模板，没给脚本；按图 7.5 的效果默认选中 Option B（value = 6）
const radio = ref(6);
</script>
