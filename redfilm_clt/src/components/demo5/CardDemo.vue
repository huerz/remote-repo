<script lang="ts" setup>
// 走图片显示接口取书封；cover 只存文件名，后端按类型子目录查找
const bookList = [
  { title: '战狼2', cover: 'ac1.jpg' },
  { title: '流浪地球', cover: 'kh1.jpg' },
  { title: '霸王别姬', cover: 'jq2.jpg' }
]
</script>

<template>
  <div class="card-demo">
    <!-- 教材图 5.12：用 Card 组件做「电影」展示布局
         header 放书名，body 放封面 -->
    <el-card v-for="book in bookList" :key="book.cover" class="book-card">
      <template #header>{{ book.title }}</template>
      <img
        :src="String('/svr/api/image/display/film/') + book.cover"
        style="width: 100%; display: block" />
    </el-card>

    <!-- header 与 footer 都是可选的：这里给一张带 footer 的卡片 -->
    <el-card class="book-card">
      <template #header>带 footer 的卡片</template>
      <p class="tip">body 放主要内容，footer 一般放操作按钮。</p>
      <template #footer>
        <el-button type="primary" size="small">查看详情</el-button>
      </template>
    </el-card>
  </div>
</template>

<style scoped>
.card-demo {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 16px;
}

.book-card {
  width: 150px;
  border-color: #e6d8bf;
  background: #fdfaf4;
}

.book-card :deep(.el-card__header) {
  padding: 10px 6px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 13px;
  text-align: center;
  color: #5a3a22;
}

.tip {
  margin: 0;
  font-size: 12px;
  line-height: 1.7;
  color: #8a6a45;
}
</style>
