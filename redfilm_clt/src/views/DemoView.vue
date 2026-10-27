<script setup lang="ts">
import { ref } from 'vue'
// 顶部 / 底部导航
import HeaderComp from '@/components/HeaderComp.vue'
import FooterComp from '@/components/FooterComp.vue'
// 教材 6.2.2 的四段组件示例：Layout → Image（图 6.3）→ Result（图 6.4）→ Rate（图 6.5）
import LayoutDemo from '@/components/demo/LayoutDemo.vue'
import ImagePreviewDemo from '@/components/demo/ImagePreviewDemo.vue'
import ResultDemo from '@/components/demo/ResultDemo.vue'
import RateDemo from '@/components/demo/RateDemo.vue'

// 顶部导航选中项（示例页不在分类菜单里，保持空）
const activeIndex = ref<string>('')
</script>

<template>
  <el-container class="demo-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="demo-wrap">
        <h2 class="demo-title">1. Layout 布局（24 分栏）</h2>
        <LayoutDemo />

        <el-divider border-style="dotted" />

        <h2 class="demo-title">2. Image 图片预览（图 6.3）</h2>
        <ImagePreviewDemo />

        <el-divider border-style="dotted" />

        <h2 class="demo-title">3. Result 结果反馈（图 6.4）</h2>
        <ResultDemo />

        <el-divider border-style="dotted" />

        <h2 class="demo-title">4. Rate 星级评价（图 6.5）</h2>
        <RateDemo />
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.demo-container {
  min-height: 100vh;
}

/* main.css 里 #app 是整体居中的，这里要强制左对齐 */
.demo-wrap {
  max-width: 960px;
  margin: 12px auto 40px;
  padding: 12px;
  text-align: left;
}

.demo-title {
  margin: 18px 0 14px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 18px;
  letter-spacing: 2px;
  color: #3b2f24;
}
</style>
