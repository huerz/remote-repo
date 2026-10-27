import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  server: {
    // 「红影赏析」前端固定 5175，避开古典文学网的 5173 与创意版 5174
    port: 5175,
    proxy: {
      '/svr': {
        // 代理接口地址。实际请求地址可能是：http://127.0.0.1:5383/api/×××/×××
        target: 'http://127.0.0.1:5383',
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