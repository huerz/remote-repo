<script setup lang="ts">
import { ref, watch, inject } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AxiosInstance } from 'axios'
import type { Discuss } from '@/types'
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'

const axios = inject('axios') as AxiosInstance // 注入 axios
const route = useRoute()

// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 获取登录用户的 Token（教材写法）
const token = ref(userStore.getToken())

// 电影编号 / 类型编号
const cid = ref<string>('')
const tid = ref<string>('')
// 电影数据
// 教材写法：var clsData = ref({})；strict 下用 any，模板取属性才不报错
var clsData = ref<any>({})
// 电影星级评价
const star = ref(0)
// 影评列表
const disDatas = ref<Discuss[]>([])
// 发表影评的输入内容
const comment = ref<string>('')

cid.value = String(route.params.cid ?? '')
tid.value = String(route.params.tid ?? '')

// 顶部导航栏菜单选中项索引（保持所属类型高亮）
const activeIndex = ref<string>('/filmlist/' + route.params.tid)

// ============================================================================
// 【接口 8】获取电影信息 API
// 调用方式：GET 前端 /svr/api/films/get-film/<cid>
//                 后端 http://127.0.0.1:5383/api/films/get-film/2
// 参数：路径参数 cid —— 电影编号
// 返回结构：{ code:'200', data:{ cid, title, author, year, cover, describes, rating, ... } }
// 说明：教材直接把返回的 rating 赋给 star（本项目数据库 rating 是 0-100，比例问题后面再解决）
// ============================================================================
function initCls() {
  axios({
    method: 'get',
    url: '/svr/api/films/get-film/' + cid.value
  })
  .then(function (response) {
    if (response.data.code == '200') {
      clsData.value = response.data.data
      // 初始化电影星级评价
      star.value = clsData.value.rating
    }
  })
  .catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口 9】电影评价 API
// 调用方式：POST 前端 /svr/api/films/judge-film
//                 后端 http://127.0.0.1:5383/api/films/judge-film
// 请求头：Authorization: Bearer <token>
// 请求体：{ "cid": 影片编号, "star": 星级(1-5) }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：未登录时评分组件为只读（disabled），登录后才可打分
// ============================================================================
// 教材写法是 (value) =>，本项目 strict 下隐式 any 会报错，补上 number 类型，逻辑一致
const judgeCls = (value: number) => {
  console.log('go judge' + value)
  var data = {
    cid: cid.value,
    star: value
  }
  axios({
    method: 'post',
    url: '/svr/api/films/judge-film',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: data
  })
  .then(function (response) {
    console.log(response.data)
    if (response.data.code == '200') {
      // 提示信息
      ElMessage({
        message: '评价成功！',
        type: 'success',
        plain: true
      })
    }
  })
  .catch(function (error) {
    console.log(error)
    // 鉴权判断
    if (error.response.status == 401 || error.response.status == 422) {
      // 设置当前登录用户的 Token 为空
      token.value = ''
      userStore.setToken('')
      // 提示信息
      ElMessage({
        message: '请重新登录！',
        type: 'success',
        plain: true
      })
    }
  })
}

// ============================================================================
// 【接口 10】影评展示 API（教材 7.3.1）
// 调用方式：GET 前端 /svr/api/films/get-discuss/<cid>
//                 后端 http://127.0.0.1:5383/api/films/get-discuss/40
// 参数：路径参数 cid —— 电影编号
// 返回结构：{ code:'200', data:[{ did, cid, comment, cdate, topcount, lowcount,
//            user:{ uid, uname, nickname, avatar, sex, phone, remark } }] }
// 说明：后端已按评论时间倒序返回，前端直接渲染，不用再排序
// ============================================================================
function initDis() {
  axios({
    method: 'get',
    url: '/svr/api/films/get-discuss/' + cid.value
  })
  .then(function (response) {
    if (response.data.code == '200') {
      disDatas.value = response.data.data
    }
  })
  .catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口 11】发表影评 API（教材 7.3.2）
// 调用方式：POST 前端 /svr/api/films/pub-discuss
//                 后端 http://127.0.0.1:5383/api/films/pub-discuss
// 请求头：Authorization: Bearer <token>
// 请求体：{ "cid": 影片编号, "comment": 影评内容 }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：后端会把 films.commentscount +1，前端同步 +1 保持一致
// ============================================================================
// 发表影评
function pubDiscuss() {
  // 数据
  var data = {
    cid: cid.value,
    comment: comment.value
  }
  axios({
    method: 'post',
    url: '/svr/api/films/pub-discuss',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: data
  })
  .then(function (response) {
    if (response.data.code == '200') {
      // 发表影评成功后，刷新影评列表
      initDis()
      // 电影评论数量加 1
      clsData.value.commentscount++
      // 清空评论信息
      comment.value = ''
      // 提示信息
      ElMessage({
        message: '发表影评成功！',
        type: 'success',
        plain: true
      })
    }
  })
  .catch(function (error) {
    console.log(error)
    // 鉴权判断
    if (error.response.status == 401 || error.response.status == 422) {
      // 设置当前登录用户的 Token 为空
      token.value = ''
      userStore.setToken('')
      // 提示信息
      ElMessage({
        message: '请重新登录！',
        type: 'success',
        plain: true
      })
    }
  })
}

// ============================================================================
// 【接口 12】影评评价 API（教材 7.3.3）
// 调用方式：POST 前端 /svr/api/films/judge-discuss
//                 后端 http://127.0.0.1:5383/api/films/judge-discuss
// 请求头：Authorization: Bearer <token>
// 请求体：{ "did": 评论编号, "toplow": 0 表示踩 / 1 表示顶 }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：未登录时按钮为 disabled，不会触发本函数
// ============================================================================
// 顶、踩影评（0 表示踩，1 表示顶）
// 教材写法是 (did, judge) =>，strict 下补上 number 类型，逻辑一致
function judgeDiscuss(did: number, judge: number) {
  let data = {
    did: did,
    toplow: judge
  }
  axios({
    method: 'post',
    url: '/svr/api/films/judge-discuss',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: data
  })
  .then(function (response) {
    if (response.data.code == '200') {
      // 评价成功后，显示影评
      initDis()
      // 提示信息
      ElMessage({
        message: '评价成功！',
        type: 'success',
        plain: true
      })
    }
  })
  .catch(function (error) {
    // 鉴权判断
    if (error.response.status == 401 || error.response.status == 422) {
      // 设置当前登录用户的 Token 为空
      token.value = ''
      userStore.setToken('')
      // 提示信息
      ElMessage({
        message: '请重新登录！',
        type: 'success',
        plain: true
      })
    }
  })
}

// 影评时间格式化
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

// 监听路由参数
watch(
  () => route.params,
  (newValue, oldValue) => {
    cid.value = String(newValue.cid)
    tid.value = String(newValue.tid)
    // 初始化电影信息
    initCls()
    // 初始化影评信息（教材 7.3，保留）
    comment.value = ''
    initDis()
  },
  // 使用 immediate: true 选项来强制侦听器的回调立即执行
  { immediate: true }
)
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
        <!-- 电影展示开始 -->
        <el-result :title="clsData.title">
          <template #icon>
            <el-image
              style="width: auto; height: 300px"
              :src="String('/svr/api/image/display/film/') + clsData.cover"
              fit="contain" />
          </template>
          <template #sub-title>
            <el-text>{{ clsData.author }}</el-text>
            <el-text>{{ clsData.year }}</el-text><br />
            <el-text>评价：</el-text>
            <el-rate v-if="token == ''" disabled v-model="star" @change="judgeCls" />
            <el-rate v-if="token != ''" v-model="star" @change="judgeCls" />
          </template>
          <template #extra>
            <el-row><div v-html="clsData.describes"></div></el-row>
          </template>
        </el-result>
        <!-- 电影展示结束 -->

        <!-- ================= 影评区（教材 7.3） ================= -->
        <!-- 评论展示开始 -->
        <div style="margin: auto">
          <el-divider>影评信息({{ clsData.commentscount }}条)</el-divider>
          <el-descriptions v-for="item in disDatas" :key="item.did" class="margin-top" :column="1">
            <template #title>
              <el-avatar
                :size="35"
                :src="String('/svr/api/image/display/head/') + item.user.avatar"
                style="vertical-align: middle"/>
              <el-text class="mx-1" type="primary" size="large" style="margin-left: 5px">
                {{ item.user.nickname }}
              </el-text>
            </template>
            <template #extra>
              <!-- 影评评价开始 -->
              <!-- 已登录，可以进行评价 -->
              <el-button-group v-if="token != ''" class="ml-4">
                <el-button type="danger" @click="judgeDiscuss(item.did, 1)">
                  <el-icon><Upload /></el-icon>顶({{ item.topcount }})
                </el-button>
                <el-button type="danger" @click="judgeDiscuss(item.did, 0)">
                  <el-icon><Download /></el-icon>踩({{ item.lowcount }})
                </el-button>
              </el-button-group>
              <!-- 没有登录，评价按钮被禁用 -->
              <el-button-group v-if="token == ''" class="ml-4">
                <el-button type="danger" disabled>
                  <el-icon><Upload /></el-icon>顶({{ item.topcount }})
                </el-button>
                <el-button type="danger" disabled>
                  <el-icon><Download /></el-icon>踩({{ item.lowcount }})
                </el-button>
              </el-button-group>
              <!-- 影评评价结束 -->
            </template>
            <el-descriptions-item>
              <div style="margin-left: 80px">
                <el-text class="mx-1" size="large">{{ item.comment }}</el-text>
              </div>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <!-- 评论展示结束 -->

        <!-- 发表影评开始 -->
        <div v-if="token != ''" style="margin: auto; text-align: center">
          <el-divider>发表影评</el-divider>
          <el-input
            v-model="comment"
            style="width: 80%"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="请输入评论信息..."
          /><br />
          <el-button style="margin-top: 5px" type="primary" @click="pubDiscuss">
            发表影评
          </el-button>
        </div>
        <!-- 发表影评结束 -->
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
  --el-rate-void-color: #bda67f;
  --el-rate-disabled-void-color: #bda67f;
}

/* ================= 影评区样式 ================= */
.discuss-card {
  margin-top: 16px;
  border: 1px solid #ece0cb;
  border-radius: 10px;
  /* main.css 里 #app 是整体居中的，影评区要强制左对齐，否则正文会跑到行中间 */
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
  /* 空态只占一两行文字，上下留白收窄一点，否则一张卡片中间空出一大片 */
  padding: 20px 0 8px;
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
  margin: 10px 0 0;
  padding-top: 12px;
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
