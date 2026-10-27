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

<script setup>
// ============================================================================
// 组件示例：ImagePreview（教材 6.2）
// ----------------------------------------------------------------------------
// 作用：演示该组件的常用写法，供教学页 /demo5、/demo、/demo7 引用。
// 约定：示例组件不接后端、不含业务状态，改动只影响演示页。
// ============================================================================
// 教材原文：const url = '默认图片URL'
// 这里换成项目「图片显示 API」的真实地址：
// 后端 /api/image/display/head/<filename>，前端走 /svr 代理
const url = '/svr/api/image/display/head/logo.png';
// 教材原文：'图片1的URL'、'图片2的URL'、'图片3的URL'
// initial-index="2" 表示预览时默认打开第 3 张（索引从 0 开始）
const srcList = [
    '/svr/api/image/display/head/logo.png',
    '/svr/api/image/display/head/tx.png',
    '/svr/api/image/display/head/zzbj.png'
];
</script>
