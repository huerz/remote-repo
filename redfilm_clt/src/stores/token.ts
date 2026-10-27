import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useTokenStore = defineStore('token', () => {
  // 定义 token：初始值直接取本地存储，避免刷新页面后
  // 组件用 computed 跟随 Store 时读到空串（表现为刷新后掉登录态）
  const token = ref<string>(localStorage.getItem('token') || '')

  // 设置 token
  function setToken(value: string): void {
    token.value = value
    // 将 Token 保存至本地存储
    localStorage.setItem('token', value)
  }

  // 获取 token（重新从本地存储同步一次，兼容外部直接改 localStorage 的情况）
  function getToken(): string {
    // 从本地存储中获取 token
    token.value = localStorage.getItem('token') || ''
    return token.value
  }

  // 暴露变量及方法
  return { token, setToken, getToken }
})
