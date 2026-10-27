<script lang="ts" setup>
// 走马灯内容：用项目图集里的书封
const coverList = [
  '/svr/api/image/display/film/ac1.jpg',
  '/svr/api/image/display/film/dh1.jpg',
  '/svr/api/image/display/film/xj1.jpg',
  '/svr/api/image/display/film/xy1.jpg'
]
</script>

<template>
  <div class="carousel-demo">
    <!-- 基础走马灯：height 必填，interval 为自动切换毫秒数 -->
    <el-carousel height="200px" :interval="3000">
      <el-carousel-item v-for="(src, i) in coverList" :key="i">
        <div class="slide">
          <img :src="src" alt="" />
        </div>
      </el-carousel-item>
    </el-carousel>

    <!-- card 模式：中间主卡 + 两侧小卡，首页轮播用的就是这种 -->
    <el-carousel type="card" height="220px" :interval="3000">
      <el-carousel-item v-for="(src, i) in coverList" :key="i">
        <div class="slide">
          <img :src="src" alt="" />
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.carousel-demo {
  max-width: 760px;
}

.carousel-demo + .carousel-demo,
.carousel-demo :deep(.el-carousel + .el-carousel) {
  margin-top: 16px;
}

.slide {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: #f6ecdc;
}

.slide img {
  height: 100%;
  object-fit: contain;
}
</style>
