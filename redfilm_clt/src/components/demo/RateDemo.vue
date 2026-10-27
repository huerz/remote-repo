<template>
  <el-rate v-model="star" @change="judgeStar" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

// 默认的星级
const star = ref(3)

// 星级评价方法
// 教材写法是 (value) =>，本项目 tsconfig 开了 strict，
// 隐式 any 会报错，所以补上 number 类型，逻辑与教材一致
const judgeStar = (value: number) => {
  console.log('go judge' + value);
}
</script>
