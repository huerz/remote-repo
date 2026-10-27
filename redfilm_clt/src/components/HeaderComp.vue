<script setup lang="ts">
import { ref, inject, onMounted } from 'vue'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Filmtype } from '@/types'
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token'

// ============================================================================
// 【接口 1】图片显示 API（Logo / 用户头像）
// 调用方式：GET  前端 /svr/api/image/display/head/redfilm_logo.png
//                 后端 http://127.0.0.1:5383/api/image/display/head/redfilm_logo.png
// 说明：/svr 是 vite.config.ts 里配置的代理前缀，转发到 5383 并去掉该前缀
// 路径参数：
//   type     = head（用户头像类） / cls（电影封面类）
//   filename = 图片文件名，如 redfilm_logo.png、tx.png
// 返回：图片二进制流（Content-Type: image/jpg）；文件不存在返回 404 + JSON
// ============================================================================
// 构建 Logo 及用户头像默认图片的 URL
const logo_url = ref('/svr/api/image/display/head/redfilm_logo.png')
const user_url = ref('/svr/api/image/display/head/tx.png')

const axios = inject('axios') as AxiosInstance // 注入 axios（main.ts 中 provide 的是 AxiosInstance）

// 用于接收传递组件的数据，此处传递的是菜单选中项索引
const props = defineProps({ activeIndex: String })
// 设置菜单选中项索引
const activeIndex = props.activeIndex

// 导航栏数据列表
const navDatas = ref<Filmtype[]>([])

// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 获取登录用户的 Token
const token = ref(userStore.getToken())

// ============================================================================
// 【接口 2】电影导航 API（首页顶部导航栏的电影类型）
// 调用方式：GET  前端 /svr/api/films/get-filmtypes
//                 后端 http://127.0.0.1:5383/api/films/get-filmtypes
// 请求参数：无
// 返回结构：{ code: '200', msg: '操作成功！', data: [ { tid, name, cover, remark } ] }
// 用途：把 data 列表循环渲染成 el-menu-item，构成动态导航菜单
// ============================================================================
// 调用 API，获取电影类型列表，用于初始化导航栏
function initNav() {
  axios<ApiResult<Filmtype[]>>({
    method: 'get',
    url: '/svr/api/films/get-filmtypes'
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
//                 后端 http://127.0.0.1:5383/api/user/get-user
// 请求头：Authorization: Bearer <token>
// 参数：无（用户编号由后端从 Token 中解析）
// 返回结构：{ code:'200', msg, data:{ uid, uname, nickname, avatar, sex, phone } }
// 用途：拿到 avatar 后拼成头像地址，显示在导航栏右上角
// ============================================================================
// 调用 API，获取当前登录用户的信息
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
      // console.log(response.data)
      if (response.data.code == '200') {
        let user = response.data.data
        user_url.value = '/svr/api/image/display/head/' + user.avatar
      }
    }).catch(function (error) {
      console.log(error)
      // 鉴权判断
      if (error.response.status == 401 || error.response.status == 422) {
        // 没有权限或权限已过期，设置 token 为空
        user_url.value = '/svr/api/image/display/head/tx.png'
        token.value = ''
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
      <img style="width: 60px; height: 60px" :src="logo_url" alt="红影赏析" />
    </el-menu-item>
    <el-menu-item index="/">首页</el-menu-item>
    <!-- 类型导航：点击进入对应分类的电影列表 -->
    <el-menu-item
      v-for="item in navDatas"
      :key="item.tid"
      :index="String('/filmlist/' + item.tid)">
      {{ item.name }}
    </el-menu-item>
    <div class="flex-grow" />
    <!-- 未登录：注册 / 登录 -->
    <el-menu-item v-if="token == ''" index="/register">注册</el-menu-item>
    <el-menu-item v-if="token == ''" index="/login">登录</el-menu-item>
    <!-- 已登录：用户中心（头像 + 用户中心 + 退出） -->
    <el-sub-menu v-if="token != ''" index="">
      <template #title>
        <el-avatar size="small" :src="user_url" />
      </template>
      <el-menu-item index="/user">用户中心</el-menu-item>
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

/* 已登录头像在 sub-menu 的标题里，收起一点内边距，避免头像撑得太开 */
.el-menu-demo .el-sub-menu__title {
  padding-right: 12px;
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
