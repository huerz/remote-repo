<script setup lang="ts">
// ============================================================================
// 右下角浮动导航：回到顶部 / 滚到底部（红影赏析：深色底 + 金边）
// ----------------------------------------------------------------------------
// 只在页面内容超出视口时出现
// 用 ResizeObserver 监听 body 尺寸，数据异步加载完变高时也能及时显示
// ============================================================================
import { ref, onMounted, onUnmounted } from 'vue'

// 页面是否可滚动
const hasScroll = ref(false)

let observer: ResizeObserver | undefined

function check() {
  const doc = document.documentElement
  hasScroll.value = doc.scrollHeight > window.innerHeight + 4
}

function toTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function toBottom() {
  window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' })
}

onMounted(() => {
  check()
  window.addEventListener('scroll', check, { passive: true })
  window.addEventListener('resize', check)
  if (typeof ResizeObserver !== 'undefined') {
    observer = new ResizeObserver(check)
    observer.observe(document.body)
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', check)
  window.removeEventListener('resize', check)
  observer?.disconnect()
})
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

/* 与红影赏析的深底金字风格一致 */
.scroll-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  border: 1px solid rgba(201, 162, 39, 0.55);
  border-radius: 50%;
  background: rgba(26, 22, 19, 0.92);
  color: #d8b45a;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(20, 14, 8, 0.28);
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.scroll-btn:hover {
  background: #c9a227;
  border-color: #c9a227;
  color: #1a1613;
  transform: translateY(-2px);
}

.scroll-btn:active {
  transform: translateY(0);
}

.scroll-fade-enter-active,
.scroll-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.scroll-fade-enter-from,
.scroll-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

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
