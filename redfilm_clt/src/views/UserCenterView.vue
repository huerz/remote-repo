<script setup lang="ts">
import { ref, inject, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AxiosInstance } from 'axios'
import type { ApiResult, DiscussUser } from '@/types'
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token'
// 顶部 / 底部导航
import HeaderComp from '@/components/HeaderComp.vue'
import FooterComp from '@/components/FooterComp.vue'

const axios = inject('axios') as AxiosInstance // 注入 axios
const router = useRouter()
const userStore = useTokenStore()

// 登录态直接跟随 Store，别处清 token 时这里同步
const token = computed(() => userStore.token)

// 顶部导航选中项（个人中心不在分类菜单里，保持空）
const activeIndex = ref<string>('')
// 用户信息
const user = ref<DiscussUser | null>(null)
// 头像地址
const userUrl = ref<string>('/svr/api/image/display/head/tx.png')
// 官方 Avatar 回退：图片 404 时返回 true，改渲染插槽（昵称首字）
const onAvatarError = () => true
// 头像兜底文字
const nickFirst = computed(() => {
  const n = user.value?.nickname || user.value?.uname || '我'
  return n.slice(0, 1)
})

// ============================================================================
// 【接口】查询登录用户信息 API
// 调用方式：GET 前端 /svr/api/user/get-user
//                 后端 http://127.0.0.1:5383/api/user/get-user
// 请求头：Authorization: Bearer <token>
// 返回结构：{ code:'200', data:{ uid, uname, nickname, avatar, sex, phone, remark } }
// 说明：未登录直接回登录页；Token 失效（401/422）清登录态并跳登录
// ============================================================================
function initUser() {
  if (!token.value) {
    router.replace('/login')
    return
  }
  axios<ApiResult<DiscussUser>>({
    method: 'get',
    url: '/svr/api/user/get-user',
    headers: { Authorization: 'Bearer ' + token.value }
  }).then(function (response) {
    if (response.data.code === '200') {
      user.value = response.data.data
      userUrl.value = '/svr/api/image/display/head/' + (response.data.data.avatar || 'tx.png')
    }
  }).catch(function (error) {
    console.log(error)
    if (error.response && (error.response.status === 401 || error.response.status === 422)) {
      userStore.setToken('')
      ElMessage.warning('登录已过期，请重新登录')
      router.replace('/login')
    }
  })
}

// 退出登录：清 Token → 提示 → 回首页
function logout() {
  userStore.setToken('')
  ElMessage.success('已退出登录')
  router.push('/')
}

onMounted(initUser)
</script>

<template>
  <el-container class="user-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="user-wrap">
        <div class="user-card">
          <!-- 头像区 -->
          <div class="user-head">
            <el-avatar
              :size="80"
              class="user-avatar"
              :src="userUrl"
              @error="onAvatarError">
              {{ nickFirst }}
            </el-avatar>
            <p class="user-nick">{{ user?.nickname || user?.uname || '未登录' }}</p>
            <p class="user-sub">ID：{{ user?.uid ?? '-' }}</p>
          </div>

          <el-divider border-style="dotted" />

          <!-- 资料区 -->
          <el-descriptions :column="1" class="user-info">
            <el-descriptions-item label="账号">
              {{ user?.uname ?? '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="昵称">
              {{ user?.nickname ?? '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="性别">
              {{ user?.sex ?? '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="电话">
              {{ user?.phone ?? '-' }}
            </el-descriptions-item>
            <el-descriptions-item v-if="user?.remark" label="备注">
              {{ user.remark }}
            </el-descriptions-item>
          </el-descriptions>

          <!-- 操作区 -->
          <div class="user-actions">
            <el-button @click="router.push('/')">返回首页</el-button>
            <el-button type="danger" plain @click="logout">退出登录</el-button>
          </div>
        </div>
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.user-container {
  min-height: 100vh;
}

/* main.css 里 #app 是整体居中的，这里要强制左对齐 */
.user-wrap {
  max-width: 660px;
  margin: 12px auto 40px;
  padding: 12px;
  text-align: left;
}

.user-card {
  padding: 30px 34px 24px;
  border: 1px solid #e6d8bf;
  border-radius: 6px;
  background:
    radial-gradient(circle at 18% 12%, rgba(168, 53, 44, 0.04), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  box-shadow: 0 6px 20px rgba(90, 58, 34, 0.08);
}

.user-head {
  text-align: center;
}

.user-avatar {
  font-size: 28px;
  color: #7a6449;
  background: #efe2cc;
  border: 1px solid #e6d8bf;
}

.user-nick {
  margin: 14px 0 4px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 20px;
  letter-spacing: 3px;
  color: #3b2f24;
}

.user-sub {
  margin: 0;
  font-size: 12px;
  color: #a2917a;
}

.user-info {
  margin-top: 4px;
}

/* Element Plus 的 descriptions 默认给 body 铺白底，放进宣纸卡片里很突兀 */
.user-info :deep(.el-descriptions__body) {
  background: transparent;
}

.user-info :deep(.el-descriptions__label) {
  width: 92px;
  color: #8c7a63;
  font-weight: normal;
}

.user-info :deep(.el-descriptions__content) {
  color: #4a3a2a;
}

.user-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 26px;
  padding-top: 18px;
  border-top: 1px dashed #e6d8bf;
}

.user-actions :deep(.el-button) {
  min-width: 104px;
  letter-spacing: 2px;
}
</style>
