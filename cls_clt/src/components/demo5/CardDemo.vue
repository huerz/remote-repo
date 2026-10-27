<script setup>
// ============================================================================
// 组件示例：Card（教材 5.2.5）
// ----------------------------------------------------------------------------
// 作用：演示该组件的常用写法，供教学页 /demo5、/demo、/demo7 引用。
// 约定：示例组件不接后端、不含业务状态，改动只影响演示页。
// ============================================================================
// 走图片显示接口取书封；cover 只存文件名，后端按类型子目录查找
const bookList = [
    { title: '关雎', cover: 'gj.jpg' },
    { title: '蒹葭', cover: 'jj.jpg' },
    { title: '桃夭', cover: 'ty.jpg' }
];
</script>

<template>
  <div class="card-demo">
    <!-- 教材图 5.12：用 Card 组件做「文学作品」展示布局
         header 放书名，body 放封面 -->
    <el-card v-for="book in bookList" :key="book.cover" class="book-card">
      <template #header>{{ book.title }}</template>
      <img
        :src="String('/svr/api/image/display/cls/') + book.cover"
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
