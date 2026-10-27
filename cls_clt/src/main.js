// ============================================================================
// 应用入口
// ----------------------------------------------------------------------------
// 作用：创建 Vue 应用，装配 Pinia / Router / Element Plus，注入 axios，安装缩放锁。
// 约定：全局 provide 的 axios 实例在组件里用 inject('axios') 取用。
// ============================================================================
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './assets/main.css';
// 页面缩放锁：按项目规则禁止任意缩放（Ctrl + 滚轮 / 缩放快捷键 / 双指捏合）
import { installZoomLock } from './utils/zoomLock';
import ElementPlus from 'element-plus'; // 引入 Element Plus 及其样式、图标集合
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import axios from 'axios'; // 引入 axios 和 vue-axios（教材 5.2.4）
import VueAxios from 'vue-axios';
const app = createApp(App);
installZoomLock(); // 安装缩放锁：必须在挂载前执行，保证页面一打开就拦住缩放
app.use(VueAxios, axios); // 挂载 axios 和 vue-axios，然而只是这样全局并不能用
// 将 axios 组件注入全局 axios，这样才能全局使用
// 组件内写法：import { inject } from 'vue' → const axios = inject('axios')
app.provide('axios', app.config.globalProperties.axios);
app.use(ElementPlus); // 挂载 Element Plus
// 注册 Element Plus 的所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}
app.use(createPinia());
app.use(router);
app.mount('#app');
