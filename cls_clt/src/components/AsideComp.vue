<script setup>
// ============================================================================
// 个人中心侧边栏
// ----------------------------------------------------------------------------
// 作用：登录后的功能入口：个人信息、我的书评、修改密码、退出。
// 约定：菜单项由 Token 是否存在决定，未登录时引导去登录页。
// ============================================================================
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// 引入状态管理文件
import { useTokenStore } from '@/stores/token';
import { ElMessage } from 'element-plus';
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
const token = ref(userStore.getToken()); // 获取登录用户的 Token
const router = useRouter(); // 创建路由对象，用于编程式导航
const props = defineProps({ asideIndex: String }); // 用于接收传递给组件的数据，此处传递的是菜单选中项索引
const asideIndex = props.asideIndex; // 设置菜单选中项索引
function isRight() {
    // 判断 Token 是否为空
    if (token.value == '') {
        // 提示信息
        ElMessage({
            message: '请重新登录！',
            type: 'success',
            plain: true
        });
        router.push('/login'); // 跳转至登录页
    }
}
onMounted(() => {
    isRight(); // 判断是否具有访问权限
});
</script>

<template>
  <!-- 用户中心侧边栏导航功能 -->
  <el-menu :default-active="asideIndex" class="el-menu-vertical-demo" :router="true">
    <el-menu-item index="/user">
      <el-icon><User /></el-icon>
      <span>个人信息</span>
    </el-menu-item>
    <el-menu-item index="/mydis">
      <el-icon><ChatLineRound /></el-icon>
      <span>我的书评</span>
    </el-menu-item>
    <el-menu-item index="/mypwd">
      <el-icon><Edit /></el-icon>
      <span>密码重置</span>
    </el-menu-item>
    <el-menu-item index="/out">
      <el-icon><Back /></el-icon>
      <span>退出</span>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>
/* 侧边栏图标：统一 18px、宣纸色系的褐色，选中时随文字变朱红，
   默认样式下图标跟文字一样黑，在这套浅色背景里偏硬 */
.el-menu-vertical-demo .el-menu-item .el-icon {
  margin-right: 12px;
  font-size: 18px;
  color: #8c7a63;
}

.el-menu-vertical-demo .el-menu-item.is-active .el-icon {
  color: #a8352c;
}

.el-menu-vertical-demo .el-menu-item:hover .el-icon {
  color: #a8352c;
}
</style>
