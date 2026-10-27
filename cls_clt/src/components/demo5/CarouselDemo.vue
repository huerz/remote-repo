<script setup>
// ============================================================================
// 组件示例：Carousel（教材 5.2.5）
// ----------------------------------------------------------------------------
// 作用：演示该组件的常用写法，供教学页 /demo5、/demo、/demo7 引用。
// 约定：示例组件不接后端、不含业务状态，改动只影响演示页。
// ============================================================================
// 走马灯内容：用项目图集里的书封
const coverList = [
    '/svr/api/image/display/cls/gj.jpg',
    '/svr/api/image/display/cls/jys.jpg',
    '/svr/api/image/display/cls/cbhg.jpg',
    '/svr/api/image/display/cls/ls.jpg'
];
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
.carousel-demo :deep(.el-carousel) + :deep(.el-carousel) {
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
