import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/main.css'

// 引入 Element Plus 及其样式、图标集合
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 引入 axios 和 vue-axios，此时并不能全局使用
import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App)

// 挂载 axios 和 vue-axios
app.use(VueAxios, axios)
// 通过 provide 暴露 axios 实例，组件内可直接 inject('axios') 取用
app.provide('axios', axios)
// 挂载 Element Plus
app.use(ElementPlus)
// 注册 Element Plus 的所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)

app.mount('#app')
