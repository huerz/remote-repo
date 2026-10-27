<script setup>
// ============================================================================
// 搜索结果页（/search/:keyword）
// ----------------------------------------------------------------------------
// 作用：按关键字检索作品；keyword 为 all 时返回全部作品。
// 约定：关键字只从路由参数取，空串统一转 all 由本页解释。
// ============================================================================
import { ref, inject, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue';
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
const axios = inject('axios'); // 注入 axios（main.ts 中 provide 的是 AxiosInstance）
const activeIndex = ref('/'); // 默认选中“首页”
const route = useRoute(); // 创建路由对象，用于获取传递的参数
const router = useRouter();
// 搜索关键字（route.params 的值类型是 string | string[]，统一转成 string）
var keyword = ref('');
keyword.value = String(route.params.keyword ?? ''); // 获取传递过来的关键字
// 如果传递的参数值为 all，则设置关键字为空字符
if (route.params.keyword == 'all') {
    keyword.value = '';
}
var searchDatas = ref([]); // 查询的数据列表
// ============================================================================
// 【接口 4】文学搜索 API
// 调用方式：POST 前端 /svr/api/classics/search-classics
//                 后端 http://127.0.0.1:5382/api/classics/search-classics
// 请求头：Content-Type: application/json
// 请求体：{ "keyword": "搜索关键字" }（keyword 为空串时返回全部作品）
// 返回结构：{ code: '200', msg: '操作成功！', data: [ { cid, title, cover, author, ... } ] }
// 匹配规则（后端）：title 或 author 模糊匹配 %keyword%，rating 倒序
// ============================================================================
function searchKeyword() {
    let data = {
        keyword: keyword.value
    };
    axios({
        method: 'post',
        url: '/svr/api/classics/search-classics',
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    }).then(function (response) {
        if (response.data.code == '200') {
            searchDatas.value = response.data.data;
        }
    }).catch(function (error) {
        console.log(error);
    });
}
onMounted(() => {
    searchKeyword(); // 查询操作
});
function submitSearch() {
    var mykeyword = keyword.value;
    if (keyword.value == '') {
        mykeyword = 'all';
    }
    if (route.params.keyword == mykeyword) {
        searchKeyword(); // 关键字未变，直接重新查询
    }
    else {
        router.push({ name: 'search', params: { keyword: mykeyword } });
    }
}
watch(() => route.params.keyword, (val) => {
    keyword.value = (val == 'all' || val == null) ? '' : String(val);
    searchKeyword();
});
</script>

<template>
  <el-container class="search-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <!--搜索框开始-->
      <div class="search-box">
        <el-input
          v-model="keyword"
          size="large"
          placeholder="请输入书名、作者关键字，如：静夜思 / 李白"
          clearable
          @keyup.enter="submitSearch">
          <template #prefix>
            <el-icon class="el-input__icon"><Search /></el-icon>
          </template>
          <template #append>
            <el-button @click="submitSearch">搜索</el-button>
          </template>
        </el-input>
      </div>
      <el-divider border-style="dotted" />
      <!--搜索框结束-->
      <!--结果概要-->
      <div class="result-summary">
        <span class="result-key">{{ keyword ? `“${keyword}”` : '全部作品' }}</span>
        <span class="result-count">共 {{ searchDatas.length }} 条</span>
      </div>
      <!--搜索结果列表开始-->
      <el-row v-if="searchDatas.length" :gutter="20">
        <el-col
          v-for="item in searchDatas"
          :key="item.cid"
          :xs="12" :sm="8" :md="6" :lg="4">
          <el-card style="padding: '0px'">
            <template #header>{{ item.title }}</template>
            <RouterLink :to="String('/cls/' + item.cid) + String('/') + item.tid">
              <img
                :src="String('/svr/api/image/display/cls/') + item.cover"
                style="width: 100%; display: block" />
            </RouterLink>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-else description="没有找到相关作品" />
      <!--搜索结果列表结束-->
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.search-container {
  min-height: 100vh;
}

/* 搜索框：居中、限宽，与首页保持一致 */
.search-box {
  max-width: 640px;
  margin: 4px auto 0;
}

/* 搜索按钮与首页统一（朱红） */
.search-box :deep(.el-input-group__append) {
  background: #a8352c;
  border-color: #a8352c;
  color: #fdf6e8;
}

.search-box :deep(.el-input-group__append:hover) {
  background: #8f2c24;
  border-color: #8f2c24;
}

/* 结果概要 */
.result-summary {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto 16px;
  padding: 0 4px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  color: #5a3a22;
}

.result-key {
  font-size: 18px;
  letter-spacing: 2px;
}

.result-count {
  font-size: 13px;
  color: #9a7b53;
}

/* 结果卡片 */
/* 卡片整体可点击，去掉链接默认的蓝色下划线 */
.cls-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.cls-card {
  margin-bottom: 20px;
  border-color: #e6d8bf;
  background: linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cls-card:hover {
  transform: translateY(-3px);
}

.cls-cover {
  width: 100%;
  height: 185px;
  border-radius: 4px;
}

/* 无封面作品：CSS 生成的宣纸封面（书名 + 作者） */
.cls-cover-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  box-sizing: border-box;
  padding: 18px 14px;
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
  font-size: 17px;
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
  padding-top: 11px;
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
  width: 28px;
  height: 1px;
  margin-left: -14px;
  background: #cbb492;
}

.cls-title {
  margin-top: 10px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 15px;
  color: #5a3a22;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cls-meta {
  margin-top: 4px;
  font-size: 12px;
  color: #9a7b53;
}

.cls-rating {
  margin-top: 6px;
}
</style>
