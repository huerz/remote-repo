<template>
  <el-rate v-model="star" @change="judgeStar" />
</template>

<script setup>
// ============================================================================
// 组件示例：Rate（教材 6.2）
// ----------------------------------------------------------------------------
// 作用：演示该组件的常用写法，供教学页 /demo5、/demo、/demo7 引用。
// 约定：示例组件不接后端、不含业务状态，改动只影响演示页。
// ============================================================================
import { ref } from 'vue';
const star = ref(3); // 默认的星级
// 星级评价方法
// 教材写法是 (value) =>，本项目 tsconfig 开了 strict，
const judgeStar = (value) => {
    console.log('go judge' + value);
};
</script>
