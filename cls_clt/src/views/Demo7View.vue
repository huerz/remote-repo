<script setup>
// ============================================================================
// 组件示例页（/demo7）
// ----------------------------------------------------------------------------
// 作用：Text / Input / Radio 的集中展示。
// 教材：第七章「古典文学网」书评模块开发 §7.2.3 Element Plus 框架常用组件（p201）
// 约定：示例页只组合演示组件，不写业务逻辑、不发接口请求。
// ============================================================================
import { ref } from 'vue';
// 顶部 / 底部导航
import HeaderComp from '@/components/HeaderComp.vue';
import FooterComp from '@/components/FooterComp.vue';
// 教材 7.2.3 的三个常用组件示例（图 7.3 / 7.4 / 7.5）
import TextDemo from '@/components/demo/TextDemo.vue';
import InputDemo from '@/components/demo/InputDemo.vue';
import RadioDemo from '@/components/demo/RadioDemo.vue';
import DescriptionsDemo from '@/components/demo/DescriptionsDemo.vue';
const activeIndex = ref(''); // 顶部导航选中项（示例页不在分类菜单里，保持空）
</script>

<template>
  <el-container class="demo7-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="demo7-wrap">
        <h2 class="demo7-title">图 7.3 Text 组件</h2>
        <TextDemo />

        <el-divider border-style="dotted" />

        <h2 class="demo7-title">图 7.4 Input 组件</h2>
        <InputDemo />

        <el-divider border-style="dotted" />

        <h2 class="demo7-title">图 7.5 Radio 组件</h2>
        <RadioDemo />

        <el-divider border-style="dotted" />

        <h2 class="demo7-title">图 7.6 Descriptions 组件</h2>
        <DescriptionsDemo />
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.demo7-container {
  min-height: 100vh;
}

/* main.css 里 #app 是整体居中的，这里要强制左对齐 */
.demo7-wrap {
  max-width: 960px;
  margin: 12px auto 40px;
  padding: 12px;
  text-align: left;
}

.demo7-title {
  margin: 18px 0 14px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 18px;
  letter-spacing: 2px;
  color: #3b2f24;
}
</style>
