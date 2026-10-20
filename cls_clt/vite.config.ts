import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  server: {
    proxy: {
      '/svr': {
        // 代理接口地址。实际请求地址可能是：http://127.0.0.1:5382/api/×××/×××
        target: 'http://127.0.0.1:5382',
        // changeOrigin 用于指定是否需要将原始主机头更改为目标 URL，默认为 false
        changeOrigin: true,
        // 重写请求。实际接口中并没有 /svr，所以需要替换为空（''）
        rewrite: (path: string) => path.replace(/^\/svr/, '')
      }
    }
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})