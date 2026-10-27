<script setup>
// ============================================================================
// 组件示例：PageHeader（教材 5.2.5）
// ----------------------------------------------------------------------------
// 作用：演示该组件的常用写法，供教学页 /demo5、/demo、/demo7 引用。
// 约定：示例组件不接后端、不含业务状态，改动只影响演示页。
// ============================================================================
import { ElMessage } from 'element-plus';
// 示例数据：真实项目里由 /recommend-classics/6 返回
const group = {
    name: '诗经',
    cover: 'hfzy.png',
    classics: [
        { cid: 1, title: '关雎', cover: 'gj.jpg' },
        { cid: 2, title: '蒹葭', cover: 'jj.jpg' },
        { cid: 3, title: '桃夭', cover: 'ty.jpg' }
    ]
};
function goClassics() {
    ElMessage.info('跳转到「' + group.name + '」列表页');
}
</script>

<template>
  <div class="page-header-demo">
    <!-- 教材 5.2.5 第 9 个：用 PageHeader 做「文学推荐」布局
         #icon 换成右箭头，#title 放“查看更多”，#content 放类型头像与名称，
         默认插槽放推荐作品列表 -->
    <el-page-header @back="goClassics">
      <template #icon>
        <el-icon><ArrowRight /></el-icon>
      </template>
      <template #title>查看更多</template>
      <template #content>
        <div class="head-flex">
          <el-avatar
            :size="30"
            :src="String('/svr/api/image/display/head/') + group.cover" />
          <span class="group-name">{{ group.name }}</span>
        </div>
      </template>

      <div class="rec-body">
        <el-row justify="center" :gutter="5">
          <el-col :span="6" v-for="item in group.classics" :key="item.cid">
            <el-card class="rec-card" :body-style="{ padding: '0px' }">
              <template #header>{{ item.title }}</template>
              <img
                :src="String('/svr/api/image/display/cls/') + item.cover"
                style="width: 100%; display: block" />
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-page-header>
  </div>
</template>

<style scoped>
.page-header-demo {
  max-width: 720px;
}

.head-flex {
  display: flex;
  align-items: center;
  gap: 10px;
}

.group-name {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 16px;
  letter-spacing: 2px;
  color: #5a3a22;
}

.rec-body {
  margin-top: 12px;
}

.rec-card {
  border-color: #e6d8bf;
  background: #fdfaf4;
}

.rec-card :deep(.el-card__header) {
  padding: 8px 6px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 13px;
  text-align: center;
  color: #5a3a22;
}
</style>
