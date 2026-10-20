import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useTokenStore = defineStore('token', () => {
  // 定义 token（类型为 string，初始值空串）
  const token = ref<string>('')

  // 设置 token
  function setToken(value: string): void {
    token.value = value
    // 将 Token 保存至本地存储
    localStorage.setItem('token', value)
  }

  // 获取 token
  function getToken(): string {
    // 从本地存储中获取 token
    token.value = localStorage.getItem('token') || ''
    return token.value
  }

  // 暴露变量及方法
  return { token, setToken, getToken }
})
