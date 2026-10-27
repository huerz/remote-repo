<script setup>
// ============================================================================
// 诗人介绍板块（首页「文学推荐」之前）
// ----------------------------------------------------------------------------
// 作用：先讲人，再读诗。每张卡片给出诗人小传与代表作品，
//       作品标题是 RouterLink，带 #discuss 锚点——详情页会自动滚动到书评区，
//       实现「点链接即可看见书评」。
// 约定：数据来自 src/data/poets.ts（cid/tid 与 classics 表一一对应）
// ============================================================================
import { poets } from '@/data/poets';
// 统一拼作品链接：/cls/<cid>/<tid>#discuss
function workLink(work) {
    return String('/cls/') + String(work.cid) + String('/') + String(work.tid) + String('#discuss');
}
</script>

<template>
  <section class="poet-section">
    <div class="poet-head">
      <h2 class="poet-heading">诗人小传</h2>
      <span class="poet-sub">先认识写诗的人，再读他的句子 · 点击作品可直接看书评</span>
    </div>

    <!-- 横向可滚动：卡片固定宽度，窄屏左右滑动 -->
    <div class="poet-strip">
      <article v-for="poet in poets" :key="poet.name" class="poet-card">
        <div class="poet-top">
          <!-- 印章：取姓氏首字 -->
          <span class="poet-seal">{{ poet.name.charAt(0) }}</span>
          <div class="poet-id">
            <h3 class="poet-name">{{ poet.name }}</h3>
            <p class="poet-meta">
              <span class="poet-dynasty">{{ poet.dynasty }}</span>
              <span class="poet-title">{{ poet.title }}</span>
            </p>
          </div>
        </div>

        <p class="poet-intro">{{ poet.intro }}</p>

        <div class="poet-works">
          <span class="poet-works-label">代表作品</span>
          <div class="poet-work-list">
            <RouterLink
              v-for="work in poet.works"
              :key="work.cid"
              class="poet-work"
              :to="workLink(work)">
              {{ work.title }}
            </RouterLink>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.poet-section {
  /* 与下方「文学推荐」区同宽（1180px），页面宽度才整齐 */
  max-width: 1180px;
  margin: 0 auto;
  padding: 4px 0 8px;
  /* #app 全局居中，这里强制左对齐，否则正文会缩到行中间 */
  text-align: left;
}

.poet-head {
  display: flex;
  align-items: baseline;
  gap: 14px;
  margin-bottom: 14px;
}

.poet-heading {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 6px;
  color: #3b2f24;
}

.poet-sub {
  font-size: 13px;
  color: #a2917a;
}

/* 卡片带：横向滚动，滚动条隐藏 */
.poet-strip {
  display: flex;
  gap: 16px;
  padding-bottom: 6px;
  overflow-x: auto;
}

.poet-strip::-webkit-scrollbar {
  display: none;
}

.poet-card {
  flex: 0 0 320px;
  padding: 18px 20px 16px;
  border: 1px solid #e6d8bf;
  border-radius: 10px;
  background:
    radial-gradient(circle at 92% 4%, rgba(168, 53, 44, 0.04), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.poet-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 26px rgba(90, 58, 34, 0.14);
}

.poet-top {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 印章：朱红方印 + 白字 */
.poet-seal {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 6px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 24px;
  color: #fdf6e8;
  background-color: #a8352c;
  box-shadow: 0 3px 8px rgba(168, 53, 44, 0.24);
}

.poet-id {
  min-width: 0;
}

.poet-name {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 18px;
  letter-spacing: 2px;
  color: #3b2f24;
}

.poet-meta {
  margin: 4px 0 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.poet-dynasty {
  padding: 1px 8px;
  border-radius: 999px;
  color: #8c7a63;
  background-color: #f3ead9;
}

.poet-title {
  color: #a2917a;
}

.poet-intro {
  margin: 12px 0 14px;
  font-size: 13.5px;
  line-height: 1.85;
  color: #4a3b2a;
  /* 卡片高度统一：超出四行截断 */
  display: -webkit-box;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.poet-works {
  padding-top: 12px;
  border-top: 1px dashed #e6d8bf;
}

.poet-works-label {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  letter-spacing: 2px;
  color: #a2917a;
}

.poet-work-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 8px;
}

/* 作品链接：底色 + hover 朱红，点击直达详情页书评区 */
.poet-work {
  padding: 3px 10px;
  border: 1px solid #ece0cb;
  border-radius: 999px;
  font-size: 13px;
  color: #6b5844;
  text-decoration: none;
  background-color: #fbf6ec;
  transition: color 0.15s ease, border-color 0.15s ease, background-color 0.15s ease;
}

.poet-work:hover {
  color: #a8352c;
  border-color: #d9c3a4;
  background-color: #fff9ef;
}
</style>