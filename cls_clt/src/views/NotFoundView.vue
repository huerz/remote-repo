<script setup lang="ts">
import { ref } from 'vue'
import HeaderComp from '@/components/HeaderComp.vue'
import FooterComp from '@/components/FooterComp.vue'

// 顶部导航栏菜单选中项索引（404 页不属于任何分类，保持空值）
const activeIndex = ref<string>('')
</script>

<template>
  <el-container class="notfound-container">
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <el-main>
      <div class="notfound-card">
        <p class="nf-code">404</p>
        <p class="nf-title">此处无书</p>
        <p class="nf-desc">你访问的页面走丢了，回首页接着读吧。</p>
        <RouterLink class="nf-link" to="/">返回首页</RouterLink>
      </div>
    </el-main>
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.notfound-container {
  min-height: 100vh;
}

.notfound-card {
  max-width: 460px;
  margin: 60px auto;
  padding: 44px 28px 38px;
  text-align: center;
  border: 1px solid #e6d8bf;
  border-radius: 6px;
  background:
    radial-gradient(circle at 18% 12%, rgba(168, 53, 44, 0.04), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  box-shadow: 0 6px 20px rgba(90, 58, 34, 0.08);
}

.nf-code {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 56px;
  letter-spacing: 6px;
  color: #a8352c;
}

.nf-title {
  margin: 6px 0 10px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 20px;
  letter-spacing: 4px;
  color: #3b2f24;
}

.nf-desc {
  margin: 0 0 22px;
  font-size: 13px;
  color: #8c7a63;
}

.nf-link {
  display: inline-block;
  padding: 7px 22px;
  font-size: 13px;
  color: #fdfaf4;
  text-decoration: none;
  background: #a8352c;
  border-radius: 4px;
}

.nf-link:hover {
  background: #922c24;
}
</style>
