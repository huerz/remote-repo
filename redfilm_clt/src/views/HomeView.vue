<script setup lang="ts">
// ============================================================================
// 首页（教材项目 5「红影赏析」首页模块，教材 140–150 页）
// ----------------------------------------------------------------------------
// 结构严格按教材 5.3 各小节：
//   5.3.1 开发首页导航栏功能   → el-container + HeaderComp + FooterComp
//   5.3.2 开发首页轮播图功能   → search-carousels/6 + el-carousel
//   5.3.3 开发电影搜索功能     → 纯前端路由跳转 SearchView
//   5.3.4 开发电影推荐功能     → recommend-films/6 + el-page-header + el-card
// 卡片结构按教材图 5.12：书名放 el-card 的 #header，封面放 body
// 额外：欢迎横幅与两侧电影元素（本需求新增，教材无此模块，放在 el-main 最前）
// ============================================================================
import { ref, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Film, RecommendGroup } from '@/types'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'
// 引入欢迎横幅两侧的电影元素（纯内联 SVG + CSS 动画，不依赖图库文件）
import FilmFigures from '@/components/FilmFigures.vue'

// 顶部导航栏菜单选中项索引，默认选中“首页”
const activeIndex = ref<string>('/')

// 注入 axios（main.ts 中 provide 的是 AxiosInstance 实例）
const axios = inject('axios') as AxiosInstance

// 创建路由对象，用于编程式导航
const router = useRouter()

// 搜索框中的关键字
const keyword = ref<string>('')

// 说明：此处不调用后端接口，只做纯前端路由跳转（教材 5.3.3）
// 跳转目标路由：name = 'search'，path = '/search/:keyword'（教材 146 页）
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
var carouselDatas = ref<Film[]>([])

// ============================================================================
// 【接口】首页轮播图 API（教材 5.3.2 / 3.3.7）
// 调用方式：GET  前端 /svr/api/films/search-carousels/6
//                 后端 http://127.0.0.1:5383/api/films/search-carousels/6
// 路径参数：6 = 需要返回的轮播图条数
// 返回结构：{ code:'200', msg:'操作成功！', data:[{ cid, title, cover, author, rating, ... }] }
// 排序规则（后端）：rating 倒序 → cid 升序
// ============================================================================
// 调用 API，获取轮播图数据列表，用于初始化首页轮播图
function initCarousel() {
  axios<ApiResult<Film[]>>({
    method: 'get',
    url: '/svr/api/films/search-carousels/6'
  }).then(function (response) {
    if (response.data.code == '200') {
      carouselDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// 推荐的电影列表数据（按影片类型分组）
var recommendDatas = ref<RecommendGroup[]>([])

// ============================================================================
// 【接口】电影推荐 API（教材 5.3.4 / 3.3.5）
// 调用方式：GET  前端 /svr/api/films/recommend-films/6
//                 后端 http://127.0.0.1:5383/api/films/recommend-films/6
// 路径参数：6 = 每个电影类型下返回的影片条数
// 返回结构：{ code:'200', msg:'操作成功！',
//            data:[{ tid, name, cover, remark,
//                    films:[{ cid, title, cover, author, rating, ... }] }] }
// 排序规则（后端）：类型按 tid 升序；同一类型内 rating 倒序 → cid 升序
// ============================================================================
// 调用 API，获取推荐的电影列表数据，用于初始化首页电影推荐栏目
function initRecommend() {
  axios<ApiResult<RecommendGroup[]>>({
    method: 'get',
    url: '/svr/api/films/recommend-films/6'
  }).then(function (response) {
    if (response.data.code == '200') {
      recommendDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// 完成初始渲染并创建 DOM 节点后，进行页面加载
onMounted(() => {
  initCarousel() // 初始化首页轮播图
  initRecommend() // 初始化电影推荐栏目
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
      <!--==================== 欢迎横幅（本需求新增，教材无此模块） ====================-->
      <div class="welcome-banner">
        <!-- 两侧电影元素：摄影机 / 胶片卷 / 场记板 / 放映机 -->
        <FilmFigures />
        <div class="banner-text">
          <h1 class="banner-title">欢迎访问红影赏析</h1>
          <p class="banner-sub">光影之间 · 定格经典</p>
        </div>
      </div>

      <!--搜索框开始-->
      <div class="search-box">
        <el-input
          v-model="keyword"
          placeholder="请输入搜索关键字"
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
      <el-divider border-style="dashed" />
      <!--搜索框结束-->
      <!--轮播图开始-->
      <!--封面图走图片显示接口：/svr/api/image/display/film/<该项的 cover 文件名>-->
      <div class="carousel-wrap">
        <!-- 教材为 height="200px"；封面是 600×870 竖版，200px 高时只有 138px 宽，
             在卡片位里显得偏小，这里放大到 300px 高（封面约 207px 宽） -->
        <el-carousel :interval="4000" type="card" height="280px">
          <el-carousel-item v-for="item in carouselDatas" :key="item.cid">
            <!-- 教材此处写作 to=""（当时详情页尚未开发）；
                 本项目详情页已实现，填真实路由，避免空 to 渲染成带下划线的裸链接 -->
            <RouterLink :to="String('/film/' + item.cid) + String('/') + item.tid">
              <el-image
                class="carousel-img"
                :src="String('/svr/api/image/display/film/') + item.cover"
                fit="contain" />
            </RouterLink>
          </el-carousel-item>
        </el-carousel>
      </div>
      <!--轮播图结束-->
      <el-divider border-style="dotted" />


      <!--电影推荐栏目开始-->
      <div v-for="item in recommendDatas" :key="item.tid" class="rec-group">
        <!-- 类型名在左、「查看更多」在右，不放类型图标 -->
        <div class="rec-group-head">
          <span class="rec-group-name">{{ item.name }}</span>
          <RouterLink
            class="rec-more"
            :to="{ name: 'filmlist', params: { tid: item.tid } }">
            查看更多 &gt;
          </RouterLink>
        </div>
        <div class="rec-group-body">
            <el-row justify="center" :gutter="5" class="rec-row">
              <el-col :span="4" v-for="classic in item.films" :key="classic.cid">
                <!-- 教材图 5.12：书名放 #header，封面放 body -->
                <!-- 教材写作 style="padding: '0px'"（CSS 里带引号是无效值），
                     要真正去掉卡片内边距需用 :body-style -->
                <el-card class="rec-card" :body-style="{ padding: '0px' }">
                  <template #header>{{ classic.title }}</template>
                  <RouterLink :to="String('/film/' + classic.cid) + String('/') + classic.tid">
                    <img
                      :src="String('/svr/api/image/display/film/') + classic.cover"
                      style="width: 100%; display: block" />
                  </RouterLink>
                </el-card>
              </el-col>
            </el-row>
        </div>
        <el-divider border-style="dotted" />
      </div>
      <!--电影推荐栏目结束-->
    </el-main>

    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
}

/* 全站分隔线统一成淡金，比默认灰更贴合主题 */
.home-container :deep(.el-divider) {
  --el-border-color: #e8dcbe;
}

/* ==================== 欢迎横幅 ==================== */
/* 宣纸底 + 墨褐字；左右留出电影元素的位置，避免标题被压住 */
.welcome-banner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 190px;
  margin: 4px 0 18px;
  padding: 26px 258px;
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
  z-index: 2;
}

.banner-text {
  position: relative;
  z-index: 2;
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

/* ==================== 5.3.2 轮播图 ==================== */
/* 限宽让书封靠紧；配合 300px 高度，主卡位 380px 宽、封面 207px 宽 */
.carousel-wrap {
  max-width: 800px;
  margin: 10px auto 6px;
}

/* 教材用 nth-child 给轮播项加交替底色（原为 #99a9bf / #d3dce6 灰蓝），
   换成本站宣纸色系，作用不变：无封面时也能看清轮播卡片轮廓 */
/* 海报本身是满幅深色图，不需要再垫一层米色底板（教材的交替底色是为纯色块演示准备的） */
.carousel-wrap :deep(.el-carousel__item) {
  background-color: transparent;
  text-align: center;
}

/* 竖版海报：按容器高度铺满、宽度自适应。
   只给 el-image 外层写 height 不够——它内部的 img 默认 width:100%、height:auto，
   会按卡片宽度等比撑高，超出容器的部分被裁掉（表现为海报只剩上半截） */
.carousel-img {
  height: 100%;
  width: auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
}

.carousel-img :deep(img) {
  height: 100%;
  width: auto;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 8px 20px rgba(60, 40, 20, 0.22);
}

/* 指示器（可点的小条）从海报内部挪到海报下方 */
:global(.carousel-wrap .el-carousel) {
  padding-bottom: 66px;
}

:global(.carousel-wrap .el-carousel__indicators) {
  bottom: 10px;
}

:global(.carousel-wrap .el-carousel__indicator .el-carousel__button) {
  width: 34px;
  height: 3px;
  border-radius: 2px;
  background: #cbb492;
  opacity: 0.55;
}

:global(.carousel-wrap .el-carousel__indicator.is-active .el-carousel__button) {
  background: #b8892f;
  opacity: 1;
}

/* card 模式的左右箭头：Element Plus 默认用内联 display:none 隐藏，
   改色后仍是两个灰点，反而突兀 —— 保持隐藏，交互走「点左右卡片」 */
:global(.carousel-wrap .el-carousel__arrow) {
  display: none !important;
}

/* ==================== 5.3.3 搜索框 ==================== */
.search-box {
  max-width: 620px;
  margin: 18px auto 6px;
}

/* 输入框：淡金描边，聚焦时描边加深 */
.search-box :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #e3d3ab inset;
  background: #fffdf8;
}

.search-box :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #c9a227 inset;
}

/* 搜索按钮：琥珀金，与电影主题一致 */
.search-box :deep(.el-input-group__append) {
  background: #b8892f;
  border-color: #b8892f;
  color: #fff8e6;
}

.search-box :deep(.el-input-group__append:hover) {
  background: #a2761f;
  border-color: #a2761f;
}

/* ==================== 5.3.4 电影推荐 ==================== */
/* 类型行：类型名在左，「查看更多」靠右，下面一条点状分隔线 */
.rec-group {
  /* 与下方卡片区同宽居中，否则「查看更多」会贴到页面最右边 */
  max-width: 1180px;
  margin: 0 auto 18px;
}

.rec-group-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #e6d8bf;
}

.rec-more {
  font-size: 13px;
  letter-spacing: 1px;
  color: #9a7b53;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.2s ease;
}

.rec-more:hover {
  color: #a8352c;
}

.rec-group-name {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #5a3a22;
}

/* 卡片区：教材用 mt-4 text-sm font-bold，这里换成等价样式 */
.rec-group-body {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 600;
}

/* 一行 6 本的总宽度：不限宽时每本会被拉到 230px 宽、封面 330px 高，过于压场 */
.rec-row {
  /* 6 列的总宽：再宽单张海报就撑不开了，再窄书名会被挤成两行 */
  max-width: 1180px;
  margin: 0 auto;
}

.rec-card {
  /* 教材 :span="4" 一行 6 本；卡片宽度交给列宽，只留一点内收 */
  margin: 0 auto 10px;
  max-width: 168px;
  border-color: #e6d8bf;
  background: #fdfaf4;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.rec-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 18px rgba(90, 58, 34, 0.14);
}

/* 卡片标题（书名）居中，与封面上下对齐 */
.rec-card :deep(.el-card__header) {
  padding: 10px 6px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 13px;
  letter-spacing: 1px;
  text-align: center;
  color: #5a3a22;
}

/* ==================== 响应式 ==================== */
/* 中等宽度：电影元素缩小，横幅左右预留同步收紧 */
@media (max-width: 1200px) {
  .welcome-banner {
    padding: 26px 190px;
  }
}

/* 窄屏：电影元素隐藏，横幅与搜索框收边 */
@media (max-width: 900px) {
  .welcome-banner {
    min-height: 140px;
    padding: 26px 26px;
  }

  .banner-title {
    font-size: 22px;
    letter-spacing: 4px;
    text-indent: 4px;
  }
}

/* 窄屏轮播降高度，避免书封上下空太多。
   el-carousel 的 height 是写在 .el-carousel__container 上的内联样式，只能 !important 覆盖 */
@media (max-width: 760px) {
  .carousel-wrap :deep(.el-carousel__container) {
    height: 200px !important;
  }
}
</style>
