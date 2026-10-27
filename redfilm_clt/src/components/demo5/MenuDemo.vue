<script lang="ts" setup>
import { ref } from 'vue'

// 当前激活项，需与 el-menu-item 的 index 一致
const activeIndex = ref('/')

// 电影类型导航（真实项目里由 /get-filmtypes 接口返回，这里写死便于示例）
const navList = [
  { tid: 1, name: '动作片' },
  { tid: 2, name: '科幻片' },
  { tid: 3, name: '动画片' }
]

// 未登录状态：显示注册 / 登录
const token = ref('')
</script>

<template>
  <div class="menu-demo">
    <!-- 教材 5.2.5 第 8 个：用 Menu 做「红影赏析」顶部导航布局
         包含：首页、电影类型导航、注册 / 登录、用户中心 -->
    <el-menu
      :default-active="activeIndex"
      :router="false"
      class="top-menu"
      mode="horizontal"
      :ellipsis="false">
      <!-- Logo -->
      <el-menu-item index="">
        <img class="logo" :src="'/svr/api/image/display/head/logo.png'" alt="红影赏析" />
      </el-menu-item>

      <!-- 首页 -->
      <el-menu-item index="/">首页</el-menu-item>

      <!-- 电影类型导航：由接口数据循环出来 -->
      <el-menu-item
        v-for="item in navList"
        :key="item.tid"
        :index="String('/filmlist/' + item.tid)">
        {{ item.name }}
      </el-menu-item>

      <!-- 占位撑开，把右侧项推到最右 -->
      <div class="flex-grow" />

      <!-- 未登录 -->
      <template v-if="token === ''">
        <el-menu-item index="/register">注册</el-menu-item>
        <el-menu-item index="/login">登录</el-menu-item>
      </template>

      <!-- 已登录：头像 + 下拉二级菜单 -->
      <el-sub-menu v-else index="user">
        <template #title>
          <el-avatar size="small" :src="'/svr/api/image/display/head/tx.png'" />
        </template>
        <el-menu-item index="/user">用户中心</el-menu-item>
        <el-menu-item index="/out">退出</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<style scoped>
.menu-demo {
  border: 1px solid #e6d8bf;
  border-radius: 4px;
  overflow: hidden;
}

.logo {
  width: 48px;
  height: 48px;
}

.flex-grow {
  flex-grow: 1;
}
</style>
