<script setup>
// ============================================================================
// 首页欢迎横幅两侧的诗人形象
// ----------------------------------------------------------------------------
// 纯内联 SVG 水墨立像，不依赖图库文件（images/ 缺图也不会变空白）
// 四位：李白（望月）、杜甫（捧卷）、苏轼（执笔）、李清照（执扇）
// 造型要点：修身长袍 + 下摆散开、宽袖垂坠、帽形明显大于头，缩小尺寸后仍可辨识
// 动画：整体浮动 + 宽袖摆动 + 月亮呼吸 + 飘带轻扬，全靠 CSS，无 JS 计时器
// 响应式：<=900px 隐藏，避免挤压横幅标题
// ============================================================================
</script>

<template>
  <div class="poet-stage" aria-hidden="true">
    <!-- ================= 左侧：李白、杜甫 ================= -->
    <div class="poet-side poet-side--left">
      <!-- 李白 · 望月 -->
      <figure class="poet poet--1">
        <svg class="poet-svg" viewBox="0 0 120 180">
          <defs>
            <linearGradient id="lbRobe" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#33231a" />
              <stop offset="100%" stop-color="#6d5440" />
            </linearGradient>
          </defs>
          <!-- 明月 -->
          <circle class="poet-moon" cx="24" cy="28" r="13" fill="#d9b45a" opacity="0.24" />
          <circle class="poet-moon-core" cx="24" cy="28" r="6.5" fill="#d9b45a" opacity="0.4" />
          <!-- 飘带 -->
          <path class="poet-ribbon" d="M42 102 Q20 120 12 144" stroke="#c9a227" stroke-width="2"
                fill="none" opacity="0.5" stroke-linecap="round" />
          <!-- 长袍 -->
          <path d="M60 46 C54 46 50 48 48 52 L44 88 L30 158 Q60 170 90 158 L76 88 L72 52 C70 48 66 46 60 46 Z"
                fill="url(#lbRobe)" />
          <!-- 衣襟留白 -->
          <path d="M60 48 L55 78 L60 88 L65 78 Z" fill="#f7efe1" opacity="0.32" />
          <!-- 腰带 -->
          <path d="M45 88 Q60 94 75 88 L75 96 Q60 102 45 96 Z" fill="#a8352c" opacity="0.72" />
          <!-- 左右宽袖 -->
          <path class="sleeve" d="M48 52 C38 60 33 76 31 94 C30 104 32 110 38 111 C45 112 48 104 49 92 C50 78 51 64 52 56 Z"
                fill="url(#lbRobe)" transform-origin="49px 54px" />
          <path class="sleeve" d="M72 52 C82 60 87 76 89 94 C90 104 88 110 82 111 C75 112 72 104 71 92 C70 78 69 64 68 56 Z"
                fill="url(#lbRobe)" transform-origin="71px 54px" />
          <!-- 衣纹 -->
          <path d="M52 120 Q60 126 68 120" stroke="#8a6a45" stroke-width="1" fill="none" opacity="0.35" />
          <!-- 头颈 -->
          <rect x="56" y="38" width="8" height="10" fill="#33231a" />
          <ellipse cx="60" cy="28" rx="10.5" ry="12" fill="#4a3324" />
          <!-- 软巾（明显宽于头） -->
          <path d="M48 22 Q60 9 72 22 L72 14 Q60 3 48 14 Z" fill="#1e1410" />
          <path d="M48 20 h24" stroke="#1e1410" stroke-width="3.4" stroke-linecap="round" />
          <!-- 短须 -->
          <path d="M55 39 Q60 45 65 39 Q60 42.5 55 39 Z" fill="#1e1410" opacity="0.9" />
        </svg>
        <figcaption class="poet-caption">李白</figcaption>
      </figure>

      <!-- 杜甫 · 捧卷 -->
      <figure class="poet poet--2">
        <svg class="poet-svg" viewBox="0 0 120 180">
          <defs>
            <linearGradient id="dfRobe" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#33231a" />
              <stop offset="100%" stop-color="#6d5440" />
            </linearGradient>
          </defs>
          <!-- 长袍 -->
          <path d="M60 46 C54 46 50 48 48 52 L44 88 L30 158 Q60 170 90 158 L76 88 L72 52 C70 48 66 46 60 46 Z"
                fill="url(#dfRobe)" />
          <path d="M60 48 L55 78 L60 88 L65 78 Z" fill="#f7efe1" opacity="0.28" />
          <!-- 宽袖 -->
          <path class="sleeve" d="M48 52 C38 60 33 76 31 94 C30 104 32 110 38 111 C45 112 48 104 49 92 C50 78 51 64 52 56 Z"
                fill="url(#dfRobe)" transform-origin="49px 54px" />
          <path class="sleeve" d="M72 52 C82 60 87 76 89 94 C90 104 88 110 82 111 C75 112 72 104 71 92 C70 78 69 64 68 56 Z"
                fill="url(#dfRobe)" transform-origin="71px 54px" />
          <!-- 手中卷轴（横放胸前） -->
          <g class="poet-scroll">
            <rect x="38" y="82" width="44" height="9" rx="2" fill="#efe4cf" />
            <rect x="34" y="79" width="6" height="15" rx="2.5" fill="#8a6a45" />
            <rect x="80" y="79" width="6" height="15" rx="2.5" fill="#8a6a45" />
            <path d="M42 86.5 h36" stroke="#c9b492" stroke-width="1" opacity="0.9" />
          </g>
          <!-- 衣纹 -->
          <path d="M52 122 Q60 128 68 122" stroke="#8a6a45" stroke-width="1" fill="none" opacity="0.35" />
          <!-- 头颈 -->
          <rect x="56" y="38" width="8" height="10" fill="#33231a" />
          <ellipse cx="60" cy="28" rx="10.5" ry="12" fill="#4a3324" />
          <!-- 幞头：方顶 + 两侧帽翅 -->
          <path d="M49 20 L71 20 L69 8 L51 8 Z" fill="#1e1410" />
          <path d="M47 20 h26" stroke="#1e1410" stroke-width="3.4" stroke-linecap="round" />
          <path d="M49 15 h-7" stroke="#1e1410" stroke-width="2.6" stroke-linecap="round" />
          <path d="M71 15 h7" stroke="#1e1410" stroke-width="2.6" stroke-linecap="round" />
          <!-- 须 -->
          <path d="M55 39 Q60 46 65 39 Q60 43 55 39 Z" fill="#1e1410" opacity="0.85" />
        </svg>
        <figcaption class="poet-caption">杜甫</figcaption>
      </figure>
    </div>

    <!-- ================= 右侧：苏轼、李清照 ================= -->
    <div class="poet-side poet-side--right">
      <!-- 苏轼 · 执笔 -->
      <figure class="poet poet--3">
        <svg class="poet-svg" viewBox="0 0 120 180">
          <defs>
            <linearGradient id="ssRobe" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#33231a" />
              <stop offset="100%" stop-color="#6d5440" />
            </linearGradient>
          </defs>
          <!-- 长袍 -->
          <path d="M60 46 C54 46 50 48 48 52 L44 88 L30 158 Q60 170 90 158 L76 88 L72 52 C70 48 66 46 60 46 Z"
                fill="url(#ssRobe)" />
          <path d="M60 48 L55 78 L60 88 L65 78 Z" fill="#f7efe1" opacity="0.28" />
          <path d="M45 88 Q60 94 75 88 L75 95 Q60 101 45 95 Z" fill="#8a6a45" opacity="0.5" />
          <!-- 宽袖 -->
          <path class="sleeve" d="M48 52 C38 60 33 76 31 94 C30 104 32 110 38 111 C45 112 48 104 49 92 C50 78 51 64 52 56 Z"
                fill="url(#ssRobe)" transform-origin="49px 54px" />
          <path class="sleeve" d="M72 52 C82 60 87 76 89 94 C90 104 88 110 82 111 C75 112 72 104 71 92 C70 78 69 64 68 56 Z"
                fill="url(#ssRobe)" transform-origin="71px 54px" />
          <!-- 执笔的右臂 + 毛笔 -->
          <path d="M84 104 Q92 90 95 76" stroke="#3a2a1d" stroke-width="6" fill="none" stroke-linecap="round" />
          <path d="M95 78 L100 58" stroke="#8a6a45" stroke-width="3.2" stroke-linecap="round" />
          <path class="poet-brush" d="M98 60 L100 48 L104 53 Z" fill="#1e1410" />
          <!-- 衣纹 -->
          <path d="M52 122 Q60 128 68 122" stroke="#8a6a45" stroke-width="1" fill="none" opacity="0.35" />
          <!-- 头颈 -->
          <rect x="56" y="38" width="8" height="10" fill="#33231a" />
          <ellipse cx="60" cy="28" rx="10.5" ry="12" fill="#4a3324" />
          <!-- 东坡巾：高桶方帽，明显高出头顶 -->
          <path d="M50 18 L70 18 L68 2 L52 2 Z" fill="#1e1410" />
          <path d="M48 18 h24" stroke="#1e1410" stroke-width="3.4" stroke-linecap="round" />
          <!-- 长须 -->
          <path d="M54 39 Q60 50 66 39 Q60 45 54 39 Z" fill="#1e1410" opacity="0.85" />
        </svg>
        <figcaption class="poet-caption">苏轼</figcaption>
      </figure>

      <!-- 李清照 · 执扇 -->
      <figure class="poet poet--4">
        <svg class="poet-svg" viewBox="0 0 120 180">
          <defs>
            <linearGradient id="lqzRobe" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3a2c22" />
              <stop offset="100%" stop-color="#755c46" />
            </linearGradient>
          </defs>
          <!-- 长裙：下摆更开、腰更细 -->
          <path d="M60 46 C55 46 52 48 50 52 L47 84 L24 158 Q60 172 96 158 L73 84 L70 52 C68 48 65 46 60 46 Z"
                fill="url(#lqzRobe)" />
          <!-- 腰带 -->
          <path d="M48 84 Q60 90 72 84 L72 91 Q60 97 48 91 Z" fill="#a8352c" opacity="0.66" />
          <!-- 宽袖 -->
          <path class="sleeve" d="M50 52 C40 60 35 76 33 94 C32 104 34 110 40 111 C47 112 50 104 51 92 C52 78 53 64 54 56 Z"
                fill="url(#lqzRobe)" transform-origin="51px 54px" />
          <path class="sleeve" d="M70 52 C80 60 85 76 87 94 C88 104 86 110 80 111 C73 112 70 104 69 92 C68 78 67 64 66 56 Z"
                fill="url(#lqzRobe)" transform-origin="69px 54px" />
          <!-- 团扇 -->
          <g class="poet-fan">
            <circle cx="94" cy="76" r="11.5" fill="#efe4cf" stroke="#8a6a45" stroke-width="1.5" />
            <path d="M93 88 l-2 12" stroke="#8a6a45" stroke-width="2.4" stroke-linecap="round" />
            <path d="M88 72 q6 -4 12 0" stroke="#c9a227" stroke-width="1.1" fill="none" opacity="0.85" />
          </g>
          <!-- 裙褶 -->
          <path d="M50 120 L46 150 M60 118 L60 154 M70 120 L74 150" stroke="#8a6a45"
                stroke-width="0.9" opacity="0.28" />
          <!-- 头颈 -->
          <rect x="57" y="38" width="7" height="10" fill="#3a2c22" />
          <ellipse cx="60" cy="29" rx="9.5" ry="11" fill="#4a3324" />
          <!-- 高髻 + 簪花 -->
          <path d="M50 24 Q60 10 70 24 Q60 18 50 24 Z" fill="#1e1410" />
          <ellipse cx="60" cy="11" rx="7" ry="6" fill="#1e1410" />
          <circle cx="67" cy="7" r="2.6" fill="#a8352c" />
        </svg>
        <figcaption class="poet-caption">李清照</figcaption>
      </figure>
    </div>
  </div>
</template>

<style scoped>
/* 舞台：铺满横幅，左右两簇人物贴底，不拦截鼠标（搜索框等仍可点） */
.poet-stage {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 6px 34px 10px;
  pointer-events: none;
  z-index: 1;
}

.poet-side {
  display: flex;
  align-items: flex-end;
  gap: 26px;
}

.poet {
  position: relative;
  margin: 0;
  opacity: 0.93;
  /* 整体轻微浮动：每位错开相位，避免整齐划一的机械感 */
  animation: poet-float 7s ease-in-out infinite;
}

.poet--1 { animation-delay: 0s; }
.poet--2 { animation-delay: -1.8s; }
.poet--3 { animation-delay: -3.2s; }
.poet--4 { animation-delay: -4.6s; }

.poet-svg {
  display: block;
  height: 134px;
  width: auto;
  filter: drop-shadow(0 5px 9px rgba(90, 58, 34, 0.16));
}

/* 姓名题款：竖排小楷，落在人物右上侧留白处，不占垂直空间 */
.poet-caption {
  position: absolute;
  top: 6px;
  right: -14px;
  writing-mode: vertical-rl;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 11px;
  letter-spacing: 3px;
  color: #8a6a45;
  opacity: 0.9;
}

/* 宽袖轻摆：绕肩部旋转，幅度很小，避免像在扇风 */
.sleeve {
  animation: sleeve-sway 5.5s ease-in-out infinite;
}

.poet--2 .sleeve { animation-delay: -1.2s; }
.poet--3 .sleeve { animation-delay: -2.4s; }
.poet--4 .sleeve { animation-delay: -3.6s; }

/* 月亮呼吸 */
.poet-moon {
  animation: moon-breathe 6s ease-in-out infinite;
}

.poet-moon-core {
  animation: moon-breathe 6s ease-in-out infinite reverse;
}

/* 飘带 / 笔锋 / 扇面 / 卷轴：更慢的呼吸，制造层次 */
.poet-ribbon {
  animation: ribbon-drift 8s ease-in-out infinite;
}

.poet-brush {
  animation: brush-tip 4.5s ease-in-out infinite;
  transform-origin: 100px 60px;
}

.poet-fan {
  animation: fan-sway 7.5s ease-in-out infinite;
  transform-origin: 92px 98px;
}

.poet-scroll {
  animation: scroll-hold 6.5s ease-in-out infinite;
}

@keyframes poet-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

@keyframes sleeve-sway {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(-2deg); }
}

@keyframes moon-breathe {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.44; }
}

@keyframes ribbon-drift {
  0%, 100% { transform: translate(0, 0); opacity: 0.42; }
  50% { transform: translate(-3px, -4px); opacity: 0.68; }
}

@keyframes brush-tip {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

@keyframes fan-sway {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(-2.6deg); }
}

@keyframes scroll-hold {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-1.4px); }
}

/* 尊重系统的"减少动态效果"设置 */
@media (prefers-reduced-motion: reduce) {
  .poet,
  .sleeve,
  .poet-moon,
  .poet-moon-core,
  .poet-ribbon,
  .poet-brush,
  .poet-fan,
  .poet-scroll {
    animation: none;
  }
}

/* 窄屏：横幅宽度不足以同时容纳标题与人物，整体隐藏 */
@media (max-width: 900px) {
  .poet-stage {
    display: none;
  }
}

/* 中等宽度：缩小人物，保留装饰感 */
@media (max-width: 1200px) and (min-width: 901px) {
  .poet-svg {
    height: 104px;
  }

  .poet-side {
    gap: 16px;
  }

  .poet-caption {
    right: -12px;
    font-size: 10px;
    letter-spacing: 2px;
  }
}
</style>
