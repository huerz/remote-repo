<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// 引入状态管理文件
import { useTokenStore } from '@/stores/token'
import { ElMessage } from 'element-plus'

// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 获取登录用户的 Token
const token = ref(userStore.getToken())
// 创建路由对象，用于编程式导航
const router = useRouter()
// 用于接收传递给组件的数据，此处传递的是菜单选中项索引
const props = defineProps({ asideIndex: String })
// 设置菜单选中项索引
const asideIndex = props.asideIndex

// 判断是否具有访问权限
function isRight() {
  // 判断 Token 是否为空
  if (token.value == '') {
    // 提示信息
    ElMessage({
      message: '请重新登录！',
      type: 'success',
      plain: true
    })
    // 跳转至登录页
    router.push('/login')
  }
}

// 完成初始渲染并创建 DOM 节点后，进行页面加载
onMounted(() => {
  // 判断是否具有访问权限
  isRight()
})
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
      <span>我的影评</span>
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
