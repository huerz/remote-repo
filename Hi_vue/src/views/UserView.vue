<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
// 创建路由对象
const route = useRoute()
// 创建路由器对象，用于编程式导航
const router = useRouter()
// 使用计数器 store，获取 count 的值
const counter = useCounterStore()
counter.count++
var id = ref('')
id.value = route.params.id
// 监听 route.params 的变化，获取最新的用户 id
watch(
  () => route.params,
  (newValue, oldValue) => {
    // 对路由变化做出响应
    console.log(newValue)
    console.log(oldValue)
    id.value = newValue.id
  },
  // 使用 immediate: true 选项来强制侦听器的回调立即执行
  { immediate: true }
)

// ---------- 编程式导航 ----------
// 字符串路径
function goHome() {
  router.push('/home')
}
// 命名路由，并加上参数，让路由建立 URL
function goUser() {
  router.push({ name: 'user', params: { id: '205' } })
}
// 带查询参数，结果是 /about?plan=private
function goAboutQuery() {
  router.push({ path: '/about', query: { plan: 'private' } })
}
// 带 hash，结果是 /about#team
function goAboutHash() {
  router.push({ path: '/about', hash: '#team' })
}
// 后退一步
function goBack() {
  router.back()
}
</script>

<template>
  <div class="user">
    <h1>用户中心，用户 id={{ route.params.id }}-用户 id={{ id }}</h1>
    <!-- 直接从 store 中访问 state -->
    <div>当前计数是：{{ counter.count }}</div>
    <p>
      <button @click="goHome">push 字符串路径</button>
      <button @click="goUser">push 命名路由+params</button>
      <button @click="goAboutQuery">push 带 query</button>
      <button @click="goAboutHash">push 带 hash</button>
      <button @click="goBack">back 后退</button>
    </p>
  </div>
</template>
