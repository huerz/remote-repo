<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Classic } from '@/types'
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'

const axios = inject('axios') as AxiosInstance // 注入 axios
const route = useRoute()

// 创建 Token 状态管理 Store，并读取当前登录用户的 Token
const userStore = useTokenStore()
const token = ref<string>(userStore.getToken())

// 文学作品编号 / 类型编号
const cid = ref<string>('')
const tid = ref<string>('')
// 文学作品数据
var clsData = ref<Classic>({
  cid: 0, title: '', tid: 0, cover: null, year: null, author: null,
  present: null, describes: null, rating: null, commentscount: null
})
// 星级评价（作品当前评分，满分 100 换算成 5 星）
const star = ref<number>(0)
// 评价按钮初始值
const myStar = ref<number>(0)

cid.value = String(route.params.cid ?? '')
tid.value = String(route.params.tid ?? '')

// 顶部导航栏菜单选中项索引（保持所属类型高亮）
const activeIndex = ref<string>('/clslist/' + route.params.tid)

// ============================================================================
// 【接口 8】获取文学作品信息 API
// 调用方式：GET 前端 /svr/api/classics/get-classic/<cid>
//                 后端 http://127.0.0.1:5382/api/classics/get-classic/2
// 参数：路径参数 cid —— 文学作品编号
// 返回结构：{ code:'200', data:{ cid, title, author, year, cover, describes, rating, ... } }
// 说明：数据库 rating 是 0-100 的整数，页面按 5 星展示，所以要除以 20
// ============================================================================
function initCls() {
  axios<ApiResult<Classic>>({
    method: 'get',
    url: '/svr/api/classics/get-classic/' + cid.value
  }).then(function (response) {
    if (response.data.code == '200') {
      clsData.value = response.data.data
      star.value = (clsData.value.rating ?? 0) / 20
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口 9】文学评价 API
// 调用方式：POST 前端 /svr/api/classics/judge-classic
//                 后端 http://127.0.0.1:5382/api/classics/judge-classic
// 请求头：Authorization: Bearer <token>
// 请求体：{ "cid": 作品编号, "star": 星级(1-5) }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：未登录时评分组件为只读（disabled），登录后才可打分
// ============================================================================
function judgeCls(value: number) {
  const data = {
    cid: cid.value,
    star: value
  }
  axios({
    method: 'post',
    url: '/svr/api/classics/judge-classic',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: data
  }).then(function (response) {
    const body = response.data as { code: string; msg: string }
    if (body.code == '200') {
      ElMessage({ message: '评价成功！', type: 'success', plain: true })
    }
  }).catch(function (error) {
    console.log(error)
    // 鉴权判断：401/422 说明 Token 无效或已过期
    if (error.response && (error.response.status == 401 || error.response.status == 422)) {
      token.value = ''
      userStore.setToken('')
      ElMessage({ message: '请重新登录！', type: 'warning', plain: true })
    }
  })
}

// 监听路由参数，切换作品时重新加载
watch(() => route.params.cid, (val) => {
  cid.value = String(val ?? '')
  tid.value = String(route.params.tid ?? '')
  myStar.value = 0
  initCls()
}, { immediate: true })
</script>

<template>
  <el-container class="classic-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="classic-wrap">
        <el-card class="classic-card" :body-style="{ padding: '26px 28px' }">
          <div class="classic-body">
            <!-- 左：封面 -->
            <div class="classic-cover">
              <img v-if="clsData.cover" :src="'/svr/api/image/display/cls/' + clsData.cover" :alt="clsData.title" />
              <span v-else class="cover-fallback">{{ clsData.title.slice(0, 1) }}</span>
            </div>

            <!-- 右：信息 -->
            <div class="classic-info">
              <h1 class="classic-title">{{ clsData.title }}</h1>
              <p class="classic-meta">
                <span v-if="clsData.author">{{ clsData.author }}</span>
                <span v-if="clsData.present" class="meta-sep">·</span>
                <span v-if="clsData.present">{{ clsData.present }}</span>
                <span v-if="clsData.year" class="meta-sep">·</span>
                <span v-if="clsData.year">{{ clsData.year }}</span>
              </p>

              <div class="classic-rating">
                <span class="rating-label">评分</span>
                <el-rate v-model="star" disabled allow-half />
                <span class="rating-num">{{ clsData.rating ?? 0 }}</span>
              </div>

              <el-divider border-style="dotted" />

              <p class="classic-describes">{{ clsData.describes }}</p>

              <div class="classic-judge">
                <span class="judge-label">{{ token ? '打个分：' : '登录后可评价：' }}</span>
                <el-rate
                  v-if="!token"
                  disabled
                  v-model="myStar" />
                <el-rate
                  v-else
                  v-model="myStar"
                  @change="judgeCls" />
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.classic-container {
  min-height: 100vh;
}

.classic-wrap {
  max-width: 1000px;
  margin: 0 auto;
  padding: 12px 12px 32px;
}

.classic-card {
  border: 1px solid #ece0cb;
  border-radius: 10px;
  background:
    radial-gradient(circle at 12% 10%, rgba(168, 53, 44, 0.035), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
}

.classic-body {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

/* 封面：固定宽高比，避免不同尺寸图片把版式撑歪 */
.classic-cover {
  flex: 0 0 260px;
  width: 260px;
  aspect-ratio: 3 / 4;
  border-radius: 8px;
  overflow: hidden;
  background: #f5eddd;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ece0cb;
}

.classic-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.cover-fallback {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 72px;
  color: #b8a488;
}

.classic-info {
  flex: 1;
  text-align: left;
  min-width: 0;
}

.classic-title {
  margin: 4px 0 10px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 26px;
  letter-spacing: 3px;
  color: #3b2f24;
}

.classic-meta {
  margin: 0 0 14px;
  font-size: 13px;
  color: #8c7a63;
}

.meta-sep {
  margin: 0 6px;
}

.classic-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-label,
.judge-label {
  font-size: 13px;
  color: #8c7a63;
}

.rating-num {
  font-size: 13px;
  color: #a8352c;
}

.classic-describes {
  margin: 0;
  font-size: 14px;
  line-height: 1.9;
  color: #4a3a2a;
  text-indent: 2em;
}

.classic-judge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px dashed #e6d8bf;
}

/* 可打分星级：未点亮图标默认近白色，在宣纸底上几乎看不见，统一调深 */
.classic-judge :deep(.el-rate) {
  --el-rate-void-color: #cbb693;
  --el-rate-disabled-void-color: #cbb693;
}

/* 窄屏：封面在上，信息在下 */
@media (max-width: 760px) {
  .classic-body {
    flex-direction: column;
    align-items: center;
  }

  .classic-cover {
    flex: none;
    width: 60%;
  }

  .classic-info {
    width: 100%;
  }
}
</style>
