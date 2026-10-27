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
// 引入 axios 和 vue-axios（教材 5.2.4）
import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App)

// 挂载 axios 和 vue-axios，然而只是这样全局并不能用
app.use(VueAxios, axios)
// 将 axios 组件注入全局 axios，这样才能全局使用
// 组件内写法：import { inject } from 'vue' → const axios = inject('axios')
app.provide('axios', app.config.globalProperties.axios)
// 挂载 Element Plus
app.use(ElementPlus)
// 注册 Element Plus 的所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component as Component)
}

app.use(createPinia())
app.use(router)

app.mount('#app')
