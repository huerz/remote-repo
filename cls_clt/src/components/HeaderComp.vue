<script setup lang="ts">
import { ref, inject, onMounted, computed } from 'vue'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Classictype } from '@/types'
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token'

// ============================================================================
// 【接口 1】图片显示 API（Logo / 用户头像）
// 调用方式：GET  前端 /svr/api/image/display/head/logo.png
//                 后端 http://127.0.0.1:5382/api/image/display/head/logo.png
// 说明：/svr 是 vite.config.ts 里配置的代理前缀，转发到 5382 并去掉该前缀
// 路径参数：
//   type     = head（用户头像类） / cls（文学作品封面类）
//   filename = 图片文件名，如 logo.png、tx.png
// 返回：图片二进制流（Content-Type: image/jpg）；文件不存在返回 404 + JSON
// ============================================================================
// 构建 Logo 及用户头像默认图片的 URL
const logo_url = ref('/svr/api/image/display/head/logo.png')
const user_url = ref('/svr/api/image/display/head/tx.png')

const axios = inject('axios') as AxiosInstance // 注入 axios（main.ts 中 provide 的是 AxiosInstance）

// 用于接收传递组件的数据，此处传递的是菜单选中项索引
const props = defineProps({ activeIndex: String })
// 设置菜单选中项索引
const activeIndex = props.activeIndex

// 导航栏数据列表
const navDatas = ref<Classictype[]>([])

// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 登录态直接跟随 Store（不要用 ref 拷贝一份值：
// 那样别的页面清掉 Token 时，这里的菜单还停留在「已登录」，两边不一致）
const token = computed(() => userStore.token)

// 当前登录用户昵称（头像图缺失时，用昵称首字作为头像兜底）
const nickname = ref<string>('')
const nickFirst = computed(() => (nickname.value || '我').slice(0, 1))

// ============================================================================
// 【接口 2】文学导航 API（首页顶部导航栏的文学作品类型）
// 调用方式：GET  前端 /svr/api/classics/get-classictypes
//                 后端 http://127.0.0.1:5382/api/classics/get-classictypes
// 请求参数：无
// 返回结构：{ code: '200', msg: '操作成功！', data: [ { tid, name, cover, remark } ] }
// 用途：把 data 列表循环渲染成 el-menu-item，构成动态导航菜单
// ============================================================================
// 调用 API，获取文学作品类型列表，用于初始化导航栏
function initNav() {
  axios<ApiResult<Classictype[]>>({
    method: 'get',
    url: '/svr/api/classics/get-classictypes'
  }).then(function (response) {
    if (response.data.code == '200') {
      navDatas.value = response.data.data
    }
  }).catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口】查询登录用户信息 API（教材 6.2 导航栏用户中心）
// 调用方式：GET  前端 /svr/api/user/get-user
//                 后端 http://127.0.0.1:5382/api/user/get-user
// 请求头：Authorization: Bearer <token>
// 参数：无（用户编号由后端从 Token 中解析）
// 返回结构：{ code:'200', msg, data:{ uid, uname, nickname, avatar, sex, phone } }
// 用途：拿到 avatar 后拼成头像地址，显示在导航栏右上角
// ============================================================================
function initAvatar() {
  // 判断 Token 是否存在
  if (token.value != '') {
    axios({
      method: 'get',
      url: '/svr/api/user/get-user',
      headers: {
        Authorization: 'Bearer ' + token.value
      }
    }).then(function (response) {
      const body = response.data as {
        code: string
        data?: { avatar?: string; nickname?: string; uname?: string }
      }
      if (body.code == '200' && body.data) {
        const user = body.data
        // 记住昵称：头像图缺失时用作兜底文字
        nickname.value = user.nickname || user.uname || ''
        // 用返回的头像文件名拼出图片地址
        user_url.value = '/svr/api/image/display/head/' + (user.avatar || 'tx.png')
      }
    }).catch(function (error) {
      console.log(error)
      // 鉴权判断：401/422 说明 Token 无效或已过期
      if (error.response && (error.response.status == 401 || error.response.status == 422)) {
        // 没有权限或权限已过期，设置 Token 为空
        user_url.value = '/svr/api/image/display/head/tx.png'
        userStore.setToken('')
      }
    })
  }
}

// 完成初始渲染并创建 DOM 节点后，进行页面加载
onMounted(() => {
  initNav() // 初始化导航栏
  initAvatar() // 初始化导航栏头像
})
</script>

<template>
  <!--导航栏标签开始-->
  <el-menu
    :default-active="activeIndex"
    :router="true"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false">
    <el-menu-item index="">
      <img style="width: 60px; height: 60px" :src="logo_url" alt="古典文学" />
    </el-menu-item>
    <el-menu-item index="/">首页</el-menu-item>
    <!-- 类型导航：点击进入对应分类的文学列表 -->
    <el-menu-item
      v-for="item in navDatas"
      :key="item.tid"
      :index="'/clslist/' + item.tid">
      {{ item.name }}
    </el-menu-item>
    <div class="flex-grow" />
    <!-- 未登录：显示注册 / 登录 -->
    <el-menu-item v-if="token === ''" index="/register">注册</el-menu-item>
    <el-menu-item v-if="token === ''" index="/login">登录</el-menu-item>
    <!-- 已登录：显示用户中心（头像 + 退出） -->
    <el-sub-menu v-if="token !== ''" index="user-center">
      <template #title>
        <!-- 头像文件缺失时（如 xm.jpg 根本没放进 images/head）退回「首字」色块，
             不会在导航栏留一个破图或灰色空圆 -->
        <el-avatar class="header-avatar" size="small" :src="user_url">
          {{ nickFirst }}
        </el-avatar>
      </template>
      <el-menu-item index="">用户中心</el-menu-item>
      <el-menu-item index="/out">退出</el-menu-item>
    </el-sub-menu>
  </el-menu>
  <!--导航栏标签结束-->
</template>

<style>
.flex-grow {
  flex-grow: 1;
}
.el-menu-demo {
  border-bottom: 1px solid #e6e6e6;
}

/* 导航栏头像：图片缺失时显示「首字」，配色与站点宣纸质一致 */
.header-avatar {
  font-size: 12px;
  color: #7a6449;
  background: #efe2cc;
  border: 1px solid #e6d8bf;
}

/* 窄屏：7 个分类 + 注册/登录放不下，会把整页撑出横向滚动条。
   这里让菜单自己横向滚动（隐藏滚动条），页面宽度保持视口宽，
   轮播、推荐卡片才能跟着一起正常缩放。 */
@media (max-width: 760px) {
  .el-menu-demo {
    overflow-x: auto;
    overflow-y: hidden;
    flex-wrap: nowrap;
  }

  .el-menu-demo::-webkit-scrollbar {
    display: none;
  }

  /* 菜单项默认允许收缩，会被压扁成「汉魏…」，这里禁止收缩，改用滚动查看 */
  .el-menu-demo > .el-menu-item,
  .el-menu-demo > .el-sub-menu {
    flex: 0 0 auto;
  }
}
</style>
