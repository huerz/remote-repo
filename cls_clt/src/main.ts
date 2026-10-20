import { createApp } from 'vue'
import type { Component } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/main.css'

// 引入 Element Plus 及其样式、图标集合
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 只保留 axios 本体：组件里统一用 inject('axios') 取用，
// 之前的 vue-axios 插件没人使用（已移除，减少一层全局挂载）
import axios from 'axios'

const app = createApp(App)

// 通过 provide 暴露 axios 实例，组件内可直接 inject('axios') 取用
app.provide('axios', axios)
// 挂载 Element Plus
app.use(ElementPlus)
// 注册 Element Plus 的所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component as Component)
}

app.use(createPinia())
app.use(router)

app.mount('#app')
