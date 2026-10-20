<script setup lang="ts">
import { ref, inject, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Classic, Classictype, RecommendGroup } from '@/types'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'


// 顶部导航栏菜单选中项索引，默认选中“首页”
const activeIndex = ref<string>('/')

const axios = inject('axios') as AxiosInstance // 注入 axios（main.ts 中 provide 的是 AxiosInstance）

// 创建路由对象，用于编程式导航
const router = useRouter()

// 搜索框中的关键字
const keyword = ref<string>('')

// 说明：此处不调用后端接口，只做纯前端路由跳转
// 跳转目标路由：name = 'search'，path = '/search/:keyword'
// 空关键字统一传 'all'，由 SearchView 解释为「查询全部」
// 搜索跳转方法，用于跳转至搜索结果页
function searchKeyword() {
  // 获取输入的搜索关键字
  var mykeyword = keyword.value
  // 当搜索关键字为空时，设置值为 all（表示搜索所有内容）
  if (keyword.value == '') {
    mykeyword = 'all'
  }
  // 跳转至搜索结果页，并传递关键字
  router.push({ name: 'search', params: { keyword: mykeyword } })
}

// 轮播图数据列表
var carouselDatas = ref<Classic[]>([])

// ============================================================================
// 【接口 3】首页轮播图 API
// 调用方式：GET  前端 /svr/api/classics/search-carousels/6
//                 后端 http://127.0.0.1:5382/api/classics/search-carousels/6
// 路径参数：6 = 需要返回的轮播图条数
// 返回结构：{ code: '200', msg: '操作成功！', data: [ { cid, title, cover, author, rating, ... } ] }
// 排序规则（后端）：rating 倒序 → cid 升序
// ============================================================================
// 调用 API，获取轮播图数据列表，用于初始化首页轮播图
function initCarousel() {
  axios<ApiResult<Classic[]>>({
    method: 'get',
    url: '/svr/api/classics/search-carousels/6'
  }).then(function (response) {
    if (response.data.code == '200') {
      carouselDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// 完成初始渲染并创建 DOM 节点后，进行页面加载
onMounted(() => {
  // 初始化轮播图
  initCarousel()
  // 初始化文学推荐
  initRecommend()
})

// ============================ 5.3.4 文学推荐 ============================
// 类型列表（提供给推荐区做分组标题）
var typeDatas = ref<Classictype[]>([])
// 全部作品（用于按 tid 分组渲染）
var classicDatas = ref<Classic[]>([])

// ============================================================================
// 【接口 2】文学导航 API（复用导航栏接口，取类型名做分组标题）
// 调用方式：GET /svr/api/classics/get-classictypes
// 参数：无
// 返回：{ code:'200', data:[{tid, name, cover, remark}] }
// ============================================================================
function initClassictypes() {
  axios<ApiResult<Classictype[]>>({
    method: 'get',
    url: '/svr/api/classics/get-classictypes'
  }).then(function (response) {
    if (response.data.code == '200') {
      typeDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口 4】文学搜索 API（keyword 传空串 = 取全部作品，供本地分组）
// 调用方式：POST /svr/api/classics/search-classics
// 请求体：{ "keyword": "" }
// 返回：{ code:'200', data:[{cid, title, cover, author, tid, ...}] }
// ============================================================================
function initRecommend() {
  initClassictypes()
  axios<ApiResult<Classic[]>>({
    method: 'post',
    url: '/svr/api/classics/search-classics',
    headers: { 'Content-Type': 'application/json' },
    data: { keyword: '' }
  }).then(function (response) {
    if (response.data.code == '200') {
      classicDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// 按文学作品类型分组（无作品的类型不展示）
const recommendGroups = computed<RecommendGroup[]>(() => {
  return typeDatas.value
    .map(function (t: Classictype): RecommendGroup {
      return {
        tid: t.tid,
        name: t.name,
        list: classicDatas.value.filter(function (c: Classic) {
          return c.tid === t.tid
        })
      }
    })
    .filter(function (g: RecommendGroup) {
      return g.list.length > 0
    })
})
</script>

<template>
  <el-container class="home-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <!--欢迎横幅开始-->
      <div class="welcome-banner">
        <div class="banner-text">
          <h1 class="banner-title">欢迎访问古典文学网</h1>
          <p class="banner-sub">品读千年文脉 · 传承中华经典</p>
        </div>
      </div>
      <!--欢迎横幅结束-->
      <!--搜索框开始（紧跟横幅，作为首页主入口）-->
      <div class="search-box">
        <el-input
          v-model="keyword"
          size="large"
          placeholder="书名 / 作者，如：静夜思"
          clearable
          @keyup.enter="searchKeyword">
          <template #prefix>
            <el-icon class="el-input__icon"><Search /></el-icon>
          </template>
          <template #append>
            <el-button @click="searchKeyword">搜索</el-button>
          </template>
        </el-input>
      </div>
      <!--搜索框结束-->
      <!--轮播图开始-->
      <!--封面图走【接口 1】图片显示 API：/svr/api/image/display/cls/<该项的 cover 文件名>-->
      <div class="carousel-wrap">
        <el-carousel :interval="4000" type="card" height="340px">
          <el-carousel-item v-for="item in carouselDatas" :key="item.cid">
            <!-- 点击轮播图进入作品展示页：/cls/<作品编号>/<类型编号> -->
            <RouterLink :to="'/cls/' + item.cid + '/' + item.tid">
              <el-image
                class="carousel-img"
                :src="String('/svr/api/image/display/cls/') + item.cover"
                fit="contain"/>
            </RouterLink>
          </el-carousel-item>
        </el-carousel>
      </div>
      <!--轮播图结束-->
      <!--文学推荐开始（5.3.4：按文学作品类型分组推荐）-->
      <div class="recommend">
        <div class="section-head">
          <span class="section-title">文学推荐</span>
          <span class="section-sub">按类型精选</span>
        </div>
        <div v-for="g in recommendGroups" :key="g.tid" class="rec-group">
          <div class="rec-group-head">
            <span class="rec-group-name">{{ g.name }}</span>
            <span class="rec-group-count">共 {{ g.list.length }} 部</span>
            <RouterLink
              class="rec-more"
              :to="{ name: 'clslist', params: { tid: g.tid } }">
              查看全部 &gt;
            </RouterLink>
          </div>
          <el-row :gutter="16">
            <el-col
              v-for="item in g.list.slice(0, 6)"
              :key="item.cid"
              :xs="12" :sm="8" :md="6" :lg="4">
              <RouterLink class="rec-link" :to="'/cls/' + item.cid + '/' + g.tid">
                <el-card class="rec-card" shadow="hover" :body-style="{ padding: '10px' }">
                  <!--有封面图用图片，无封面时用 CSS 排版一张宣纸感封面-->
                  <el-image
                    v-if="item.cover"
                    class="rec-cover"
                    :src="String('/svr/api/image/display/cls/') + item.cover"
                    fit="contain"/>
                  <div v-else class="rec-cover rec-cover-text">
                    <span class="cover-title">{{ item.title }}</span>
                    <span class="cover-author">{{ item.author }}</span>
                  </div>
                  <div class="rec-title" :title="item.title">{{ item.title }}</div>
                  <div class="rec-meta">{{ item.year }} · {{ item.author }}</div>
                </el-card>
              </RouterLink>
            </el-col>
          </el-row>
        </div>
      </div>
      <!--文学推荐结束-->
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
}

/* 欢迎横幅：宣纸底 + 墨褐字，与古典文学主题一致 */
.welcome-banner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 4px 0 24px;
  padding: 30px 32px;
  border: 1px solid #e6d8bf;
  border-radius: 10px;
  background:
    radial-gradient(circle at 14% 18%, rgba(168, 53, 44, 0.06), transparent 46%),
    radial-gradient(circle at 86% 82%, rgba(107, 66, 38, 0.05), transparent 48%),
    linear-gradient(135deg, #fdfaf4 0%, #f6ecdc 55%, #efe2ce 100%);
  box-shadow: 0 2px 12px rgba(107, 66, 38, 0.07);
  overflow: hidden;
}

/* 顶部细金线装饰 */
.welcome-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 8%;
  right: 8%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #c9a227, transparent);
}

.banner-text {
  width: 100%;
  text-align: center;
}

.banner-title {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif;
  font-size: 30px;
  font-weight: 600;
  letter-spacing: 8px;
  text-indent: 8px;
  color: #5a3a22;
}

.banner-sub {
  margin: 8px 0 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 13px;
  letter-spacing: 4px;
  text-indent: 4px;
  color: #9a7b53;
}

/* 搜索框：紧跟横幅、居中、限宽，作为首页主入口 */
.search-box {
  max-width: 640px;
  margin: 4px auto 34px;
}

/* 搜索框内按钮与主题统一（朱红描边） */
.search-box :deep(.el-input-group__append) {
  background: #a8352c;
  border-color: #a8352c;
  color: #fdf6e8;
}

.search-box :deep(.el-input-group__append:hover) {
  background: #8f2c24;
  border-color: #8f2c24;
}

/* 轮播区：限宽让书封靠紧，避免 1200px 下三本书拉得过开 */
.carousel-wrap {
  max-width: 820px;
  margin: 16px auto 12px;
}

/* ===== 文学推荐（5.3.4） ===== */
.recommend {
  margin-top: 10px;
  text-align: left;
}

.section-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 18px;
  padding-left: 12px;
  border-left: 4px solid #a8352c;
}

.section-title {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #5a3a22;
}

.section-sub {
  font-size: 12px;
  letter-spacing: 2px;
  color: #9a7b53;
}

.rec-group {
  margin-bottom: 26px;
}

.rec-group-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px dashed #e6d8bf;
}

.rec-group-count {
  font-size: 12px;
  color: #b39a78;
}

.rec-group-name {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 16px;
  letter-spacing: 2px;
  color: #6b4226;
}

.rec-group-name::before {
  content: '·';
  margin-right: 6px;
  color: #a8352c;
}

.rec-more {
  margin-left: auto;
  font-size: 12px;
  color: #9a7b53;
  text-decoration: none;
}

.rec-more:hover {
  color: #a8352c;
}

/* 卡片整体可点击，去掉链接默认的蓝色下划线 */
.rec-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.rec-card {
  margin-bottom: 16px;
  border-color: #e6d8bf;
  background: linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  transition: transform 0.2s ease;
}

.rec-card:hover {
  transform: translateY(-3px);
}

.rec-cover {
  width: 100%;
  height: 170px;
  border-radius: 4px;
}

/* 无封面作品：CSS 生成的宣纸封面（书名 + 作者） */
.rec-cover-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 11px;
  box-sizing: border-box;
  padding: 16px 12px;
  border: 1px solid #e0d0b4;
  background:
    radial-gradient(circle at 22% 16%, rgba(168, 53, 44, 0.06), transparent 58%),
    linear-gradient(160deg, #fbf6ea 0%, #f2e6d1 100%);
  /* 内嵌双线框，模仿线装书封的边框 */
  box-shadow: inset 0 0 0 5px #fbf6ea, inset 0 0 0 6px #ece0c8;
}

.cover-title {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.55;
  letter-spacing: 2px;
  text-indent: 2px; /* 抵消末字字间距造成的视觉偏右 */
  text-align: center;
  word-break: break-all;
  color: #4a2f1b;
}

/* 作者名上方加一条短横线，与书名分层 */
.cover-author {
  position: relative;
  padding-top: 10px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 12px;
  letter-spacing: 1px;
  color: #8a6a45;
}

.cover-author::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  width: 26px;
  height: 1px;
  margin-left: -13px;
  background: #cbb492;
}

.rec-title {
  margin-top: 8px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 14px;
  color: #5a3a22;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rec-meta {
  margin-top: 3px;
  font-size: 12px;
  color: #9a7b53;
}
</style>

<style scoped>
/* 竖版书封不适合铺满横排卡片：
   去掉卡片的米色底板、让封面在卡片内居中悬浮
   （用 .carousel-wrap 前缀提高权重，覆盖 Element Plus 的 .el-carousel__item 默认值） */
.carousel-wrap :deep(.el-carousel__item) {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  overflow: visible;
}

/* RouterLink 是内联 <a>，高度 auto，会让内部 height:100% 全部失效
   → 先让它撑满卡片高度，图片的 100% 才有参照 */
.carousel-wrap :deep(.el-carousel__item > a) {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  /* card 模式下相邻卡片会贴在一起，补一点内边距当间隔 */
  padding: 0 14px;
}

/* 轮播封面：竖版书封按高度铺满、宽度自适应
   关键：img 必须显式给 width/height 100% + object-fit: contain。
   只写 width:auto 时，Element Plus 内部的 .el-image__inner 宽度是 100%、
   高度却是 auto，图片会按容器宽度等比撑高（410×595 撑出 260 的卡片），
   看起来就像书封被裁掉上下、比例被压扁。 */
.carousel-img {
  height: 100%;
  width: 100%;
  display: block;
}

.carousel-img :deep(img) {
  height: 100%;
  width: 100%;
  object-fit: contain;
  border-radius: 5px;
  box-shadow: 0 8px 20px rgba(90, 58, 34, 0.22);
}

/* 窄屏：卡片宽度只剩约 195px，若沿用 340px 高度，书封上下会各空出 70px。
   el-carousel 的 height 是写在 .el-carousel__container 上的内联样式，只能 !important 覆盖 */
@media (max-width: 760px) {
  .carousel-wrap :deep(.el-carousel__container) {
    height: 200px !important;
  }

  .carousel-wrap :deep(.el-carousel__item > a) {
    padding: 0 8px;
  }
}
</style>
