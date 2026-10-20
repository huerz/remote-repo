<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Classic } from '@/types'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'

const axios = inject('axios') as AxiosInstance // 注入 axios
// 创建路由对象
const route = useRoute()

// 文学列表接口返回的 data 结构：类型信息 + 该类型下的作品列表
interface ClsListData {
  tid: number
  name: string
  cover: string | null
  classics: Classic[]
}

// 文学作品分类编号
const tid = ref<string>('')
// 文学列表数据
var clsDatas = ref<ClsListData>({ tid: 0, name: '', cover: null, classics: [] })

tid.value = String(route.params.tid ?? '')

// 顶部导航栏菜单选中项索引（与导航项的 index 对应）
const activeIndex = ref<string>('/clslist/' + route.params.tid)

// ============================================================================
// 【接口 7】按作品类型获取文学列表 API
// 调用方式：GET 前端 /svr/api/classics/get-classics/<tid>
//                 后端 http://127.0.0.1:5382/api/classics/get-classics/4
// 参数：路径参数 tid —— 文学作品类型编号（如 4 = 唐诗）
// 返回结构：{ code:'200', msg, data:{ tid, name, cover, classics:[{cid, title, cover, author, ...}] } }
// ============================================================================
// 初始化文学列表
function initClsList() {
  axios<ApiResult<ClsListData>>({
    method: 'get',
    url: '/svr/api/classics/get-classics/' + tid.value
  }).then(function (response) {
    if (response.data.code == '200') {
      clsDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// 监听路由参数变化，参数更新时重新拉取列表
// immediate: true 让首次进入页面也立即执行一次
watch(() => route.params.tid, (val) => {
  tid.value = String(val ?? '')
  activeIndex.value = '/clslist/' + tid.value
  initClsList()
}, { immediate: true })
</script>

<template>
  <el-container class="clslist-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="clslist-wrap">
        <!-- 类型头部：类型封面 + 类型名 + 作品数量 -->
        <div class="clslist-head">
          <img
            v-if="clsDatas.cover"
            class="type-cover"
            :src="'/svr/api/image/display/head/' + clsDatas.cover"
            :alt="clsDatas.name" />
          <div class="type-info">
            <h2 class="type-name">{{ clsDatas.name }}</h2>
            <p class="type-count">共 {{ clsDatas.classics.length }} 部作品</p>
          </div>
        </div>

        <el-divider border-style="dotted" />

        <!-- 作品网格：一行 6 个 -->
        <el-row :gutter="16" class="cls-grid">
          <el-col
            v-for="item in clsDatas.classics"
            :key="item.cid"
            :xs="12" :sm="8" :md="6" :lg="4">
            <RouterLink :to="'/cls/' + item.cid + '/' + clsDatas.tid" class="cls-link">
              <el-card class="cls-card" :body-style="{ padding: '0px' }">
                <div class="cls-cover">
                  <img v-if="item.cover" :src="'/svr/api/image/display/cls/' + item.cover" :alt="item.title" />
                  <!-- 没有封面时用作品名首字占位，避免出现破图 -->
                  <span v-else class="cls-cover-fallback">{{ item.title.slice(0, 1) }}</span>
                </div>
                <div class="cls-title">{{ item.title }}</div>
              </el-card>
            </RouterLink>
          </el-col>
        </el-row>

        <el-empty v-if="clsDatas.classics.length === 0" description="该分类下暂无作品" />
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.clslist-container {
  min-height: 100vh;
}

.clslist-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 8px 12px 32px;
}

/* 类型头部 */
.clslist-head {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 4px;
}

.type-cover {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e6d8bf;
}

.type-info {
  text-align: left;
}

.type-name {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 22px;
  letter-spacing: 4px;
  color: #3b2f24;
}

.type-count {
  margin: 4px 0 0;
  font-size: 12px;
  color: #8c7a63;
}

/* 作品网格 */
.cls-grid {
  margin-top: 4px;
}

.cls-link {
  text-decoration: none;
  color: inherit;
}

.cls-card {
  margin-bottom: 16px;
  border: 1px solid #ece0cb;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.cls-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(90, 58, 34, 0.12);
}

.cls-cover {
  width: 100%;
  /* 封面原图是 600×870，用 3/4 会被 object-fit:cover 裁掉上下约 8%，
     这里直接按原图比例开框，等于零裁切 */
  aspect-ratio: 600 / 870;
  background: #f5eddd;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cls-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.cls-cover-fallback {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 40px;
  color: #b8a488;
}

.cls-title {
  padding: 8px 6px 10px;
  font-size: 13px;
  color: #4a3a2a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
