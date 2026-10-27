<template>
  <div class="demo-image__preview">
    <el-image
      width="100px" height="100px"
      :src="url"
      :zoom-rate="1.2"
      :max-scale="7"
      :min-scale="0.2"
      :preview-src-list="srcList"
      :initial-index="2"
      fit="cover"
    />
  </div>
</template>

<script lang="ts" setup>
// 教材原文：const url = '默认图片URL'
// 这里换成项目「图片显示 API」的真实地址：
// 后端 /api/image/display/head/<filename>，前端走 /svr 代理
const url = '/svr/api/image/display/head/logo.png'

// 教材原文：'图片1的URL'、'图片2的URL'、'图片3的URL'
// initial-index="2" 表示预览时默认打开第 3 张（索引从 0 开始）
const srcList = [
  '/svr/api/image/display/head/logo.png',
  '/svr/api/image/display/head/tx.png',
  '/svr/api/image/display/head/zzbj.png'
]
</script>
