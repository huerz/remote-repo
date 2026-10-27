<script setup>
// ============================================================================
// 右下角浮动导航：回到顶部 / 滚到底部
// ----------------------------------------------------------------------------
// 只在页面内容超出视口时出现（内容不够长时按钮没有意义）
// 用 ResizeObserver 监听 body 尺寸，数据异步加载完变高时也能及时显示
// ============================================================================
import { ref, onMounted, onUnmounted } from 'vue';
// 页面是否可滚动
const hasScroll = ref(false);
let observer;
function check() {
    const doc = document.documentElement;
    hasScroll.value = doc.scrollHeight > window.innerHeight + 4;
}
function toTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
function toBottom() {
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
}
onMounted(() => {
    check();
    window.addEventListener('scroll', check, { passive: true });
    window.addEventListener('resize', check);
    // 内容异步渲染（列表 / 影评加载完）后高度会变，这里跟着更新
    if (typeof ResizeObserver !== 'undefined') {
        observer = new ResizeObserver(check);
        observer.observe(document.body);
    }
});
onUnmounted(() => {
    window.removeEventListener('scroll', check);
    window.removeEventListener('resize', check);
    observer?.disconnect();
});
</script>

<template>
  <transition name="scroll-fade">
    <div v-if="hasScroll" class="scroll-nav">
      <button class="scroll-btn" type="button" title="回到顶部" aria-label="回到顶部" @click="toTop">
        <el-icon><ArrowUp /></el-icon>
      </button>
      <button class="scroll-btn" type="button" title="滚到底部" aria-label="滚到底部" @click="toBottom">
        <el-icon><ArrowDown /></el-icon>
      </button>
    </div>
  </transition>
</template>

<style scoped>
.scroll-nav {
  position: fixed;
  right: 24px;
  bottom: 92px;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.scroll-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  border: 1px solid #e6d8bf;
  border-radius: 50%;
  background: rgba(253, 250, 244, 0.94);
  color: #8a6a45;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(90, 58, 34, 0.14);
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.scroll-btn:hover {
  background: #a8352c;
  border-color: #a8352c;
  color: #fdf6e8;
}

/* 只有「回到顶部」才上移；「滚到底部」下移，方向和动作一致 */
.scroll-btn:first-child:hover {
  transform: translateY(-2px);
}

.scroll-btn:last-child:hover {
  transform: translateY(2px);
}

.scroll-btn:active {
  transform: translateY(0);
}

/* 淡入淡出 */
.scroll-fade-enter-active,
.scroll-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.scroll-fade-enter-from,
.scroll-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

/* 窄屏：贴边一点，按钮略小 */
@media (max-width: 760px) {
  .scroll-nav {
    right: 14px;
    bottom: 78px;
    gap: 8px;
  }

  .scroll-btn {
    width: 38px;
    height: 38px;
    font-size: 16px;
  }
}
</style>
