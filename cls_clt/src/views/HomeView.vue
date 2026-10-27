<script setup>
// ============================================================================
// 首页（教材项目 5「古典文学网」首页模块，教材 140–150 页）
// ----------------------------------------------------------------------------
// 结构严格按教材 5.3 各小节：
//   5.3.1 开发首页导航栏功能   → el-container + HeaderComp + FooterComp
//   5.3.2 开发首页轮播图功能   → search-carousels/6 + el-carousel
//   5.3.3 开发文学搜索功能     → 纯前端路由跳转 SearchView
//   5.3.4 开发文学推荐功能     → recommend-classics/6 + el-page-header + el-card
// 卡片结构按教材图 5.12：书名放 el-card 的 #header，封面放 body
// 额外：欢迎横幅与两侧诗人形象（本需求新增，教材无此模块，放在 el-main 最前）
// ============================================================================
import { ref, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import HeaderComp from '@/components/HeaderComp.vue'; // 引入顶部导航栏组件
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
import PoetIntro from '@/components/PoetIntro.vue'; // 首页「诗人小传」板块：讲诗人 + 作品直达书评区
import PoetFigures from '@/components/PoetFigures.vue'; // 引入欢迎横幅两侧的诗人形象（纯内联 SVG + CSS 动画，不依赖图库文件）
const activeIndex = ref('/'); // 顶部导航栏菜单选中项索引，默认选中“首页”
// 注入 axios（main.ts 中 provide 的是 AxiosInstance 实例）
const axios = inject('axios');
const router = useRouter(); // 创建路由对象，用于编程式导航
const keyword = ref(''); // 搜索框中的关键字
// 说明：此处不调用后端接口，只做纯前端路由跳转（教材 5.3.3）
// 跳转目标路由：name = 'search'，path = '/search/:keyword'（教材 146 页）
// 空关键字统一传 'all'，由 SearchView 解释为「查询全部」
function searchKeyword() {
    var mykeyword = keyword.value; // 获取输入的搜索关键字
    // 当搜索关键字为空时，设置值为 all（表示搜索所有内容）
    if (keyword.value == '') {
        mykeyword = 'all';
    }
    router.push({ name: 'search', params: { keyword: mykeyword } }); // 跳转至搜索结果页，并传递关键字
}
var carouselDatas = ref([]); // 轮播图数据列表
const carouselRef = ref(); // 轮播组件实例：自定义左右箭头通过它调用 prev() / next()
// 上一张 / 下一张：按钮放在卡片外侧，所以不再用组件自带的箭头（arrow="never"）
function prevSlide() {
    carouselRef.value?.prev();
}
function nextSlide() {
    carouselRef.value?.next();
}
// ============================================================================
// 【接口】首页轮播图 API（教材 5.3.2 / 3.3.7）
// 调用方式：GET  前端 /svr/api/classics/search-carousels/6
//                 后端 http://127.0.0.1:5382/api/classics/search-carousels/6
// 路径参数：6 = 需要返回的轮播图条数
// 返回结构：{ code:'200', msg:'操作成功！', data:[{ cid, title, cover, author, rating, ... }] }
// 排序规则（后端）：rating 倒序 → cid 升序
// ============================================================================
function initCarousel() {
    axios({
        method: 'get',
        url: '/svr/api/classics/search-carousels/6'
    }).then(function (response) {
        if (response.data.code == '200') {
            carouselDatas.value = response.data.data;
        }
    }).catch(function (error) {
        console.log(error);
    });
}
var recommendDatas = ref([]); // 推荐的文学列表数据（按作品类型分组）
// ============================================================================
// 【接口】文学推荐 API（教材 5.3.4 / 3.3.5）
// 调用方式：GET  前端 /svr/api/classics/recommend-classics/12
//                 后端 http://127.0.0.1:5382/api/classics/recommend-classics/12
// 路径参数：12 = 每个文学类型下返回的作品条数（首页一行 6 本，共两行）
// 返回结构：{ code:'200', msg:'操作成功！',
//            data:[{ tid, name, cover, remark,
//                    classics:[{ cid, title, cover, author, rating, ... }] }] }
// 排序规则（后端）：类型按 tid 升序；同一类型内 rating 倒序 → cid 升序
// 说明：库里共 108 部作品，每类取 12 部即可铺满两行（不足 12 部的类型返回全部）
// ============================================================================
function initRecommend() {
    axios({
        method: 'get',
        url: '/svr/api/classics/recommend-classics/12'
    }).then(function (response) {
        if (response.data.code == '200') {
            recommendDatas.value = response.data.data;
        }
    }).catch(function (error) {
        console.log(error);
    });
}
onMounted(() => {
    initCarousel(); // 初始化首页轮播图
    initRecommend(); // 初始化文学推荐栏目
});
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
        <!-- 两侧著名诗人形象：李白 / 杜甫 / 苏轼 / 李清照 -->
        <PoetFigures />
        <div class="banner-text">
          <h1 class="banner-title">欢迎访问古典文学网</h1>
          <p class="banner-sub">品读千年文脉 · 传承中华经典</p>
        </div>
      </div>

      <!--搜索框开始（与轮播同宽 760px，位于轮播上方）-->
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
      <!--搜索框结束-->

      <!--轮播图开始-->
      <!--封面图走图片显示接口：/svr/api/image/display/cls/<该项的 cover 文件名>-->
      <div class="carousel-wrap">
        <!-- 封面统一是 600×870 竖版（宽高比 0.69）。卡片位宽度由组件固定为容器的一半
             （760 / 2 = 380px），比封面宽很多，若让封面铺满卡片宽度就会被裁掉上下、
             看起来像被压扁；所以封面只取中间 380px 高（约 262 宽），卡片高 440px，
             上下各留 30px，四周都有留白。
             底部切换按钮用 indicator-position="outside" 放到卡片外面；
             左右箭头也改成外侧自绘按钮（arrow="never" 关掉组件自带的） -->
        <el-carousel
          ref="carouselRef"
          :interval="4000"
          type="card"
          height="440px"
          arrow="never"
          indicator-position="outside">
          <el-carousel-item v-for="item in carouselDatas" :key="item.cid">
            <!-- 教材此处写作 to=""（当时详情页尚未开发）；
                 本项目详情页已实现，填真实路由，避免空 to 渲染成带下划线的裸链接 -->
            <RouterLink
              class="carousel-link"
              :to="String('/cls/' + item.cid) + String('/') + item.tid">
              <!-- 只用封面本身的宽高比撑开图片框，不做任何裁切 -->
              <div class="carousel-figure">
                <el-image
                  class="carousel-img"
                  :src="String('/svr/api/image/display/cls/') + item.cover"
                  fit="cover" />
              </div>
            </RouterLink>
          </el-carousel-item>
        </el-carousel>

        <!-- 左右切换箭头：放在卡片外侧，米白圆底 + 铜棕细折线（不影响封面） -->
        <button
          type="button"
          class="carousel-nav carousel-nav--prev"
          aria-label="上一张"
          @click="prevSlide">
          <span class="carousel-chevron carousel-chevron--prev"></span>
        </button>
        <button
          type="button"
          class="carousel-nav carousel-nav--next"
          aria-label="下一张"
          @click="nextSlide">
          <span class="carousel-chevron carousel-chevron--next"></span>
        </button>
      </div>
      <!--轮播图结束-->
      <el-divider border-style="dashed" />

      <!--诗人介绍开始：先讲人再读诗，作品链接直达书评区-->
      <PoetIntro />
      <!--诗人介绍结束-->

      <!--文学推荐栏目开始-->
      <div v-for="item in recommendDatas" :key="item.tid" class="rec-group">
        <!-- 类型名在左、「查看更多」在右，不放类型图标 -->
        <div class="rec-group-head">
          <span class="rec-group-name">{{ item.name }}</span>
          <RouterLink
            class="rec-more"
            :to="{ name: 'clslist', params: { tid: item.tid } }">
            查看更多 &gt;
          </RouterLink>
        </div>
        <div class="rec-group-body">
            <el-row justify="center" :gutter="5" class="rec-row">
              <el-col :span="4" v-for="classic in item.classics" :key="classic.cid">
                <!-- 教材图 5.12：书名放 #header，封面放 body -->
                <!-- 教材写作 style="padding: '0px'"（CSS 里带引号是无效值），
                     要真正去掉卡片内边距需用 :body-style -->
                <el-card class="rec-card" :body-style="{ padding: '0px' }">
                  <template #header>{{ classic.title }}</template>
                  <RouterLink :to="String('/cls/' + classic.cid) + String('/') + classic.tid">
                    <img
                      :src="String('/svr/api/image/display/cls/') + classic.cover"
                      style="width: 100%; display: block" />
                  </RouterLink>
                </el-card>
              </el-col>
            </el-row>
        </div>
        <el-divider border-style="dotted" />
      </div>
      <!--文学推荐栏目结束-->
    </el-main>

    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
}

/* ==================== 欢迎横幅 ==================== */
/* 宣纸底 + 墨褐字；左右留出诗人形象的位置，避免标题被压住 */
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

/* ==================== 5.3.3 搜索框 ==================== */
/* 与轮播图同一列：限宽 760px 居中，两者左右边缘完全对齐 */
.search-box {
  width: 100%;
  max-width: 760px;
  margin: 14px auto 16px;
}

/* 搜索框内按钮与主题统一（朱红） */
.search-box :deep(.el-input-group__append) {
  background: #a8352c;
  border-color: #a8352c;
  color: #fdf6e8;
}

/* 放大镜图标：EP 默认灰偏冷，换成宣纸色系的褐色，字号提到 16px 更清楚 */
.search-box :deep(.el-input__prefix .el-icon) {
  font-size: 16px;
  color: #8c7a63;
}

.search-box :deep(.el-input-group__append:hover) {
  background: #8f2c24;
  border-color: #8f2c24;
}

/* ==================== 5.3.2 轮播图 ==================== */
/* 与搜索框同宽（760px）：卡片位 = 380px；卡片高 440px，封面占中间 380px。
   position: relative 是给外侧的左右箭头做定位参照 */
.carousel-wrap {
  --cls-cover-h: 380px;
  --cls-stage-h: 440px;
  position: relative;
  width: 100%;
  max-width: 760px;
  margin: 0 auto 8px;
}

/* 教材用 nth-child 给轮播项加交替底色（原为 #99a9bf / #d3dce6 灰蓝），
   换成本站宣纸色系，作用不变：无封面时也能看清轮播卡片轮廓 */
.carousel-wrap :deep(.el-carousel__item:nth-child(2n)) {
  background-color: #efe2ce;
}

.carousel-wrap :deep(.el-carousel__item:nth-child(2n + 1)) {
  background-color: #f6ecdc;
}

/* 卡片位里让书封水平垂直居中 */
.carousel-wrap :deep(.el-carousel__item) {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 封面链接：只作为书封外框的定位容器，不参与尺寸计算 */
.carousel-link {
  display: block;
}

/* 书封外框：宽高按 600:870 直接算出来（380 × 0.6897 ≈ 262px），
   不再被卡片宽度拉宽，所以封面整张可见、不会被裁上下或压扁。
   注意 aspect-ratio 在块级盒宽高都确定时不生效，这里用 calc 写死宽度最稳；
   封面高度 380 + 卡片上下各 30px 留白 = el-carousel 的 height 440px */
.carousel-figure {
  height: var(--cls-cover-h);
  width: calc(var(--cls-cover-h) * 600 / 870);
  overflow: hidden;
  border-radius: 2px;
  box-shadow: 0 8px 22px rgba(90, 58, 34, 0.26);
}

/* 图片框铺满外框；比例已经一致，cover 与 contain 等价，用 cover 兜住个别尺寸不一的图 */
.carousel-img {
  display: block;
  width: 100%;
  height: 100%;
}

/* 非当前卡片的白色遮罩默认 0.24，会把两侧书封冲得发白，降到 0.1 只留一点层次 */
.carousel-wrap :deep(.el-carousel__mask) {
  opacity: 0.1;
}

/* 底部切换按钮（indicator-position="outside"，排在封面下方）
   默认按钮本体 30×2px、白色，又细又看不清，很难点中。
   这里改到 .el-carousel 上覆盖组件变量（写在祖先上会被组件自身的同名变量顶掉）：
     按钮本体 30×2 → 56×8，明显加粗加宽
     加上内边距后单个可点区域 38×26 → 68×32，点击面积翻倍
   6 个点共 408px，760px 宽的轮播放得下 */
.carousel-wrap :deep(.el-carousel) {
  --el-carousel-indicator-width: 56px;
  --el-carousel-indicator-height: 8px;
  --el-carousel-indicator-padding-horizontal: 6px;
  --el-carousel-indicator-padding-vertical: 12px;
}

/* 按钮区与封面之间留一点间距，别贴着卡片底边 */
.carousel-wrap :deep(.el-carousel__indicators--outside) {
  margin-top: 4px;
}

/* 白色在宣纸底上等于隐形，换成铜棕；当前项用主题朱红实心区分 */
.carousel-wrap :deep(.el-carousel__button) {
  background-color: #b08a5d;
  border-radius: 4px;
}

.carousel-wrap :deep(.el-carousel__indicator.is-active .el-carousel__button) {
  background-color: #a8352c;
  opacity: 1;
}

.carousel-wrap :deep(.el-carousel__indicator:hover .el-carousel__button) {
  opacity: 0.72;
}

/* ==================== 轮播左右箭头（自绘，放在卡片外侧） ==================== */
/* 设计稿：米白圆底、铜棕细折线、柔和投影，不压封面。
   直径 56px，距轮播区左右各 12px（即距容器边缘 -68px）。
   .el-carousel--horizontal 有 overflow: hidden，所以箭头不能放在组件里，
   改挂在 .carousel-wrap 上，用绝对定位放到外面 */
.carousel-nav {
  position: absolute;
  top: calc(var(--cls-stage-h) / 2);
  transform: translateY(-50%);
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  padding: 0;
  border: 1px solid #f2e6d0;
  border-radius: 50%;
  background-color: #fffdf6;
  box-shadow: 0 6px 18px rgba(120, 85, 45, 0.12);
  cursor: pointer;
  transition: background-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.carousel-nav:hover {
  background-color: #fdf6e6;
  box-shadow: 0 8px 22px rgba(120, 85, 45, 0.18);
}

.carousel-nav:active {
  transform: translateY(-50%) scale(0.96);
}

.carousel-nav--prev {
  left: -68px;
}

.carousel-nav--next {
  right: -68px;
}

/* 细折线箭头：两条边旋转 45°，不带箭杆，与设计稿一致 */
.carousel-chevron {
  width: 12px;
  height: 12px;
  border-left: 2px solid #8b5a3c;
  border-bottom: 2px solid #8b5a3c;
}

.carousel-chevron--prev {
  transform: rotate(45deg);
  margin-left: 4px;
}

.carousel-chevron--next {
  transform: rotate(-135deg);
  margin-right: 4px;
}

/* ==================== 5.3.4 文学推荐 ==================== */
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
/* 用 flex 居中：el-row 有 gutter 时会写内联负 margin，把 max-width 的居中
   （margin: 0 auto）压掉了，卡片区会整体贴左，跟标题行错位 */
.rec-group-body {
  display: flex;
  justify-content: center;
  margin-top: 12px;
  font-size: 14px;
  font-weight: 600;
}

/* 一行 6 本的总宽度：不限宽时每本会被拉到 230px 宽、封面 330px 高，过于压场 */
.rec-row {
  width: 100%;
  max-width: 1000px;
}

.rec-card {
  /* 教材 :span="4" 一行 6 本不变，只把单张卡收窄居中 */
  max-width: 152px;
  margin: 0 auto 8px;
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
/* 中等宽度：诗人缩小，横幅左右预留同步收紧 */
@media (max-width: 1200px) {
  .welcome-banner {
    padding: 26px 190px;
  }
}

/* 窄屏：诗人隐藏，横幅与搜索框收边 */
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

  /* 视口不够宽时，760px 轮播两侧没有空位，外侧箭头会顶出屏幕：
     直接隐藏，改由底部指示条和手势切换 */
  .carousel-nav {
    display: none;
  }
}

/* 窄屏轮播降高度，避免书封上下空太多。
   el-carousel 的 height 是写在 .el-carousel__container 上的内联样式，只能 !important 覆盖；
   封面高度同步收窄（300 - 上下各 20 留白 = 260），宽度按 600:870 自动跟随。
   指示条已放到卡片外面，不用再跟着调内边距 */
@media (max-width: 760px) {
  .carousel-wrap {
    --cls-cover-h: 260px;
    --cls-stage-h: 300px;
  }

  .carousel-wrap :deep(.el-carousel__container) {
    height: 300px !important;
  }

  /* 窄屏 6 个点若仍是 68px 一个会超出屏宽，收窄到 44×6 */
  .carousel-wrap :deep(.el-carousel) {
    --el-carousel-indicator-width: 44px;
    --el-carousel-indicator-height: 6px;
    --el-carousel-indicator-padding-horizontal: 4px;
  }
}
</style>
