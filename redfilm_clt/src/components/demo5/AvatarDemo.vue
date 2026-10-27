<script lang="ts" setup>
// 头像图走图片显示接口：/svr/api/image/display/head/<filename>
// 后端：http://127.0.0.1:5383/api/image/display/head/tx.png
const avatarUrl = '/svr/api/image/display/head/tx.png'
const logoUrl = '/svr/api/image/display/head/redfilm_logo.png'

// 头像组：模拟「最近浏览的用户」
const groupUsers = [
  '/svr/api/image/display/head/tx.png',
  '/svr/api/image/display/head/xiaobai.jpg',
  '/svr/api/image/display/head/tx.png'
]
</script>

<template>
  <div class="avatar-demo">
    <!-- 1. 基础用法：src 传图片地址，默认圆形 -->
    <div class="row">
      <span class="tag">基础</span>
      <el-avatar :size="40" :src="avatarUrl" />
    </div>

    <!-- 2. 尺寸：size 可写数字，也可写 large / default / small -->
    <div class="row">
      <span class="tag">尺寸</span>
      <el-avatar :size="24" :src="avatarUrl" />
      <el-avatar :size="32" :src="avatarUrl" />
      <el-avatar :size="48" :src="avatarUrl" />
      <el-avatar size="large" :src="avatarUrl" />
      <el-avatar :size="64" :src="avatarUrl" />
    </div>

    <!-- 3. 形状：circle 圆形（默认）/ square 方形 -->
    <div class="row">
      <span class="tag">形状</span>
      <el-avatar shape="circle" :size="48" :src="logoUrl" />
      <el-avatar shape="square" :size="48" :src="logoUrl" />
    </div>

    <!-- 4. 三种内容来源：图片 / 图标 / 文字 -->
    <div class="row">
      <span class="tag">内容</span>
      <el-avatar :size="48" :src="avatarUrl" />
      <el-avatar :size="48" icon="UserFilled" />
      <el-avatar :size="48">影</el-avatar>
    </div>

    <!-- 5. 配合 el-badge 做「有消息」的头像（导航栏用户中心常用） -->
    <div class="row">
      <span class="tag">带徽标</span>
      <el-badge :value="3" :offset="[-4, 4]">
        <el-avatar :size="44" :src="avatarUrl" />
      </el-badge>
      <el-badge is-dot :offset="[-4, 4]">
        <el-avatar :size="44" :src="avatarUrl" />
      </el-badge>
    </div>

    <!-- 6. 头像组：负 margin 叠放，鼠标移上去抬起来 -->
    <div class="row">
      <span class="tag">头像组</span>
      <div class="avatar-group">
        <el-avatar
          v-for="(src, i) in groupUsers"
          :key="i"
          :size="40"
          :src="src"
          class="group-item" />
        <el-avatar :size="40" class="group-item group-more">+5</el-avatar>
      </div>
    </div>
  </div>
</template>

<style scoped>
.avatar-demo {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
}

/* 每组前面的说明标签 */
.tag {
  min-width: 56px;
  font-size: 12px;
  color: #9a7b53;
}

/* 头像组：后一个压在前一个上，只露出 3/4 */
.avatar-group {
  display: flex;
  align-items: center;
}

.group-item {
  border: 2px solid #fdfaf4;
  transition: transform 0.2s ease;
}

.group-item + .group-item {
  margin-left: -12px;
}

.group-item:hover {
  transform: translateY(-4px);
  z-index: 2;
}

.group-more {
  background: #e6d8bf;
  color: #6b4226;
  font-size: 12px;
}
</style>
