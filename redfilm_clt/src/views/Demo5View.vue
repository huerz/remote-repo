<script lang="ts" setup>
import { ref } from 'vue'
// 顶部 / 底部导航
import HeaderComp from '@/components/HeaderComp.vue'
import FooterComp from '@/components/FooterComp.vue'
// 教材 5.2.5 的 11 个常用组件示例
import ContainerDemo from '@/components/demo5/ContainerDemo.vue'
import IconDemo from '@/components/demo5/IconDemo.vue'
import FormDemo from '@/components/demo5/FormDemo.vue'
import ButtonDemo from '@/components/demo5/ButtonDemo.vue'
import AvatarDemo from '@/components/demo5/AvatarDemo.vue'
import CardDemo from '@/components/demo5/CardDemo.vue'
import CarouselDemo from '@/components/demo5/CarouselDemo.vue'
import MenuDemo from '@/components/demo5/MenuDemo.vue'
import PageHeaderDemo from '@/components/demo5/PageHeaderDemo.vue'
import MessageDemo from '@/components/demo5/MessageDemo.vue'
import DividerDemo from '@/components/demo5/DividerDemo.vue'

// 顶部导航选中项（示例页不在分类菜单里，保持空）
const activeIndex = ref<string>('')
</script>

<template>
  <el-container class="demo5-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="demo5-wrap">
        <h1 class="demo5-title">教材 5.2.5 Element Plus 框架常用组件</h1>
        <p class="demo5-sub">共 11 个组件：Container / Icon / Form / Button / Avatar / Card / Carousel / Menu / PageHeader / Message / Divider</p>

        <section class="demo5-block">
          <h2 class="demo5-label">1. Container 布局容器</h2>
          <ContainerDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">2. Icon 图标</h2>
          <IconDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">3. Form 表单</h2>
          <FormDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">4. Button 按钮</h2>
          <ButtonDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">5. Avatar 头像</h2>
          <AvatarDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">6. Card 卡片</h2>
          <CardDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">7. Carousel 走马灯</h2>
          <CarouselDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">8. Menu 菜单</h2>
          <MenuDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">9. PageHeader 页头</h2>
          <PageHeaderDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">10. Message 消息提示</h2>
          <MessageDemo />
        </section>

        <section class="demo5-block">
          <h2 class="demo5-label">11. Divider 分割线</h2>
          <DividerDemo />
        </section>
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.demo5-container {
  min-height: 100vh;
}

/* main.css 里 #app 是整体居中的，这里要强制左对齐 */
.demo5-wrap {
  max-width: 960px;
  margin: 12px auto 40px;
  padding: 12px;
  text-align: left;
}

.demo5-title {
  margin: 0 0 6px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 22px;
  letter-spacing: 2px;
  color: #5a3a22;
}

.demo5-sub {
  margin: 0 0 8px;
  font-size: 13px;
  color: #9a7b53;
}

/* 每个组件一块：标题 + 示例，块之间用细线分隔 */
.demo5-block {
  padding: 18px 0 6px;
  border-bottom: 1px dashed #e6d8bf;
}

.demo5-block:last-child {
  border-bottom: none;
}

.demo5-label {
  margin: 0 0 14px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  color: #8a2f26;
}
</style>
