<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Classic, Discuss } from '@/types'
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
// 书评列表
const disDatas = ref<Discuss[]>([])
// 发表书评的输入内容
const comment = ref<string>('')

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
      // 重新拉取作品信息，让「评分 / 评价数」立刻反映这次打分
      initCls()
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

// ============================================================================
// 【接口 10】书评展示 API（教材 7.3.1）
// 调用方式：GET 前端 /svr/api/classics/get-discuss/<cid>
//                 后端 http://127.0.0.1:5382/api/classics/get-discuss/40
// 参数：路径参数 cid —— 文学作品编号
// 返回结构：{ code:'200', data:[{ did, cid, comment, cdate, topcount, lowcount,
//            user:{ uid, uname, nickname, avatar, sex, phone, remark } }] }
// 说明：后端已按评论时间倒序返回，前端直接渲染，不用再排序
// ============================================================================
function initDis() {
  axios<ApiResult<Discuss[]>>({
    method: 'get',
    url: '/svr/api/classics/get-discuss/' + cid.value
  }).then(function (response) {
    if (response.data.code == '200') {
      disDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口 11】发表书评 API（教材 7.3.2）
// 调用方式：POST 前端 /svr/api/classics/pub-discuss
//                 后端 http://127.0.0.1:5382/api/classics/pub-discuss
// 请求头：Authorization: Bearer <token>
// 请求体：{ "cid": 作品编号, "comment": 书评内容 }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：后端会把 classics.commentscount +1，前端同步 +1 保持一致
// ============================================================================
function pubDiscuss() {
  // 空内容不发请求，直接提示
  if (!comment.value.trim()) {
    ElMessage({ message: '请先输入书评内容！', type: 'warning', plain: true })
    return
  }
  const data = {
    cid: cid.value,
    comment: comment.value
  }
  axios({
    method: 'post',
    url: '/svr/api/classics/pub-discuss',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: data
  }).then(function (response) {
    const body = response.data as { code: string; msg: string }
    if (body.code == '200') {
      // 发表书评成功后，刷新书评列表
      initDis()
      // 文学作品评论数量加 1
      clsData.value.commentscount = (clsData.value.commentscount ?? 0) + 1
      // 清空评论信息
      comment.value = ''
      // 提示信息
      ElMessage({ message: '发表书评成功！', type: 'success', plain: true })
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

// ============================================================================
// 【接口 12】书评评价 API（教材 7.3.3）
// 调用方式：POST 前端 /svr/api/classics/judge-discuss
//                 后端 http://127.0.0.1:5382/api/classics/judge-discuss
// 请求头：Authorization: Bearer <token>
// 请求体：{ "did": 评论编号, "toplow": 0 表示踩 / 1 表示顶 }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：未登录时按钮为 disabled，不会触发本函数
// ============================================================================
function judgeDiscuss(did: number, judge: number) {
  const data = {
    did: did,
    toplow: judge
  }
  axios({
    method: 'post',
    url: '/svr/api/classics/judge-discuss',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: data
  }).then(function (response) {
    const body = response.data as { code: string; msg: string }
    if (body.code == '200') {
      // 评价成功后，刷新书评列表（顶/踩数量以数据库为准）
      initDis()
      ElMessage({ message: '评价成功！', type: 'success', plain: true })
    }
  }).catch(function (error) {
    console.log(error)
    if (error.response && (error.response.status == 401 || error.response.status == 422)) {
      token.value = ''
      userStore.setToken('')
      ElMessage({ message: '请重新登录！', type: 'warning', plain: true })
    }
  })
}

// 书评时间格式化
// 后端已统一返回 "YYYY-MM-DD HH:MM"，直接展示；
// 万一返回别的格式（如 HTTP 日期串）再交给 Date 解析兜底
function formatDate(value: string | null): string {
  if (!value) return ''
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(value)) return value
  const d = new Date(value)
  if (isNaN(d.getTime())) return value
  const p = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ` +
    `${p(d.getHours())}:${p(d.getMinutes())}`
}

// 监听路由参数，切换作品时重新加载
watch(() => route.params.cid, (val) => {
  cid.value = String(val ?? '')
  tid.value = String(route.params.tid ?? '')
  myStar.value = 0
  comment.value = ''
  initCls()
  // 初始化书评信息
  initDis()
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

        <!-- ================= 书评区（教材 7.3） ================= -->
        <el-card class="discuss-card" :body-style="{ padding: '22px 28px' }">
          <div class="discuss-head">
            <span class="discuss-title">书评</span>
            <span class="discuss-count">共 {{ disDatas.length }} 条</span>
          </div>

          <!-- 空态 -->
          <div v-if="disDatas.length === 0" class="discuss-empty">
            还没有人留下书评，来做第一个吧。
          </div>

          <!-- 书评列表 -->
          <ul v-else class="discuss-list">
            <li v-for="item in disDatas" :key="item.did" class="discuss-item">
              <el-avatar
                :size="36"
                class="discuss-avatar"
                :src="'/svr/api/image/display/head/' + (item.user.avatar || 'tx.png')">
                {{ (item.user.nickname || item.user.uname || '?').slice(0, 1) }}
              </el-avatar>
              <div class="discuss-main">
                <div class="discuss-meta">
                  <span class="discuss-nick">{{ item.user.nickname || item.user.uname }}</span>
                  <span class="discuss-date">{{ formatDate(item.cdate) }}</span>
                </div>
                <p class="discuss-text">{{ item.comment }}</p>
                <div class="discuss-actions">
                  <!-- 已登录：可以点顶/踩 -->
                  <template v-if="token">
                    <button class="act-btn up" @click="judgeDiscuss(item.did, 1)">
                      ▲ 顶 {{ item.topcount ?? 0 }}
                    </button>
                    <button class="act-btn down" @click="judgeDiscuss(item.did, 0)">
                      ▼ 踩 {{ item.lowcount ?? 0 }}
                    </button>
                  </template>
                  <!-- 未登录：只展示数字，按钮禁用 -->
                  <template v-else>
                    <button class="act-btn up" disabled>▲ 顶 {{ item.topcount ?? 0 }}</button>
                    <button class="act-btn down" disabled>▼ 踩 {{ item.lowcount ?? 0 }}</button>
                  </template>
                </div>
              </div>
            </li>
          </ul>

          <!-- 发表书评：仅登录用户可见 -->
          <div v-if="token" class="discuss-pub">
            <el-input
              v-model="comment"
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 4 }"
              maxlength="300"
              show-word-limit
              placeholder="写下你对这部作品的理解……" />
            <div class="discuss-pub-bar">
              <el-button type="primary" @click="pubDiscuss">发表书评</el-button>
            </div>
          </div>
          <p v-else class="discuss-login-tip">
            登录后可以发表书评 ·
            <RouterLink class="login-link" to="/login">去登录</RouterLink>
          </p>
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

/* ================= 书评区样式 ================= */
.discuss-card {
  margin-top: 16px;
  border: 1px solid #ece0cb;
  border-radius: 10px;
  /* main.css 里 #app 是整体居中的，书评区要强制左对齐，否则正文会跑到行中间 */
  text-align: left;
  background:
    radial-gradient(circle at 88% 6%, rgba(168, 53, 44, 0.03), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
}

/* 头像：文件缺失时退回「首字」色块，避免出现灰色空圆 */
.discuss-avatar {
  flex: none;
  font-size: 14px;
  color: #7a6449;
  background: #efe2cc;
  border: 1px solid #e6d8bf;
}

.discuss-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #e6d8bf;
}

.discuss-title {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 17px;
  letter-spacing: 4px;
  color: #3b2f24;
}

.discuss-count {
  font-size: 12px;
  color: #a2917a;
}

.discuss-empty {
  padding: 34px 0 26px;
  text-align: center;
  font-size: 13px;
  color: #a2917a;
}

.discuss-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.discuss-item {
  display: flex;
  gap: 12px;
  padding: 18px 0;
  border-bottom: 1px solid #f2e8d6;
}

.discuss-item:last-child {
  border-bottom: none;
}

.discuss-main {
  flex: 1;
  min-width: 0;
}

.discuss-meta {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.discuss-nick {
  font-size: 13px;
  color: #6b5844;
}

.discuss-date {
  font-size: 12px;
  color: #b3a48d;
}

.discuss-text {
  margin: 6px 0 8px;
  font-size: 14px;
  line-height: 1.85;
  color: #4a3a2a;
  word-break: break-word;
}

.discuss-actions {
  display: flex;
  gap: 8px;
}

/* 顶/踩：做成低调的胶囊按钮，避免 Element Plus 默认按钮把版面压重 */
.act-btn {
  padding: 3px 12px;
  font-size: 12px;
  line-height: 1.6;
  color: #8c7a63;
  background: #fbf6ec;
  border: 1px solid #ece0cb;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.act-btn:hover:not(:disabled) {
  color: #a8352c;
  border-color: #d9c3a4;
  background: #fff9ef;
}

.act-btn.down:hover:not(:disabled) {
  color: #5a6b7a;
}

.act-btn:disabled {
  color: #bdb0a0;
  cursor: not-allowed;
}

.discuss-pub {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px dashed #e6d8bf;
}

.discuss-pub-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.discuss-login-tip {
  margin: 18px 0 0;
  padding-top: 16px;
  font-size: 13px;
  color: #8c7a63;
  text-align: center;
  border-top: 1px dashed #e6d8bf;
}

.login-link {
  color: #a8352c;
  text-decoration: none;
  border-bottom: 1px solid rgba(168, 53, 44, 0.35);
}

.login-link:hover {
  border-bottom-color: #a8352c;
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
