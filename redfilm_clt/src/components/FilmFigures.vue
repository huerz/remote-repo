<script setup lang="ts">
// ============================================================================
// 首页欢迎横幅两侧的装饰：竖向胶片带
// ----------------------------------------------------------------------------
// 用「胶片条」代替具象图标：抽象、左右对称、在浅色宣纸底上不抢眼
// 结构：深褐色片基 + 两列浅色齿孔 + 画格分隔线
// 动画：极缓慢的上下浮动，两条错开相位
// 响应式：<=900px 隐藏
// ============================================================================
</script>

<template>
  <div class="film-stage" aria-hidden="true">
    <!-- 左侧胶片带 -->
    <div class="film-strip film-strip--left">
      <svg viewBox="0 0 84 300" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="stripL" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#3d2c1e" />
            <stop offset="45%" stop-color="#5c4530" />
            <stop offset="100%" stop-color="#33241a" />
          </linearGradient>
        </defs>

        <!-- 片基 -->
        <rect x="0" y="0" width="84" height="300" rx="5" fill="url(#stripL)" />

        <!-- 左右两列齿孔 -->
        <g fill="#fdfaf4" opacity="0.88">
          <rect v-for="i in 11" :key="'l' + i" x="7" :y="8 + (i - 1) * 27" width="11" height="14" rx="2" />
          <rect v-for="i in 11" :key="'r' + i" x="66" :y="8 + (i - 1) * 27" width="11" height="14" rx="2" />
        </g>

        <!-- 画格：深浅交替，模拟一格格的画面 -->
        <g>
          <rect v-for="i in 5" :key="'f' + i" x="24" :y="6 + (i - 1) * 58" width="36" height="52" rx="2"
                :fill="i % 2 === 1 ? '#c9a227' : '#8a6a45'" :opacity="i % 2 === 1 ? 0.34 : 0.24" />
        </g>
      </svg>
    </div>

    <!-- 右侧胶片带（镜像倾斜） -->
    <div class="film-strip film-strip--right">
      <svg viewBox="0 0 84 300" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="stripR" x1="1" y1="0" x2="0" y2="0">
            <stop offset="0%" stop-color="#3d2c1e" />
            <stop offset="45%" stop-color="#5c4530" />
            <stop offset="100%" stop-color="#33241a" />
          </linearGradient>
        </defs>

        <rect x="0" y="0" width="84" height="300" rx="5" fill="url(#stripR)" />

        <g fill="#fdfaf4" opacity="0.88">
          <rect v-for="i in 11" :key="'l2' + i" x="7" :y="8 + (i - 1) * 27" width="11" height="14" rx="2" />
          <rect v-for="i in 11" :key="'r2' + i" x="66" :y="8 + (i - 1) * 27" width="11" height="14" rx="2" />
        </g>

        <g>
          <rect v-for="i in 5" :key="'f2' + i" x="24" :y="6 + (i - 1) * 58" width="36" height="52" rx="2"
                :fill="i % 2 === 1 ? '#8a6a45' : '#c9a227'" :opacity="i % 2 === 1 ? 0.24 : 0.34" />
        </g>
      </svg>
    </div>
  </div>
</template>

<style scoped>
/* 舞台：铺满横幅，两条胶片贴底外扩，不拦截鼠标 */
.film-stage {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.film-strip {
  position: absolute;
  bottom: -46px;
  width: 84px;
  opacity: 0.4;
  filter: drop-shadow(0 6px 14px rgba(60, 40, 20, 0.16));
}

/* 左：逆时针倾斜；右：顺时针，形成对称 */
.film-strip--left {
  --rot: -9deg;
  left: 46px;
  transform: rotate(-9deg);
  animation: strip-float 9s ease-in-out infinite;
}

.film-strip--right {
  --rot: 9deg;
  right: 46px;
  transform: rotate(9deg);
  animation: strip-float 9s ease-in-out infinite;
  animation-delay: -4.5s;
}

@keyframes strip-float {
  0%, 100% { transform: translateY(0) rotate(var(--rot)); }
  50% { transform: translateY(-8px) rotate(var(--rot)); }
}

/* 尊重系统的「减少动态效果」设置 */
@media (prefers-reduced-motion: reduce) {
  .film-strip {
    animation: none;
  }
}

/* 中等宽度：收窄、收边，别顶到标题 */
@media (max-width: 1200px) and (min-width: 901px) {
  .film-strip {
    width: 64px;
    opacity: 0.42;
  }

  .film-strip--left {
    left: 22px;
  }

  .film-strip--right {
    right: 22px;
  }
}

/* 窄屏：横幅宽度不足，整体隐藏 */
@media (max-width: 900px) {
  .film-stage {
    display: none;
  }
}
</style>
