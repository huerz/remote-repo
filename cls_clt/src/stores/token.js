// ============================================================================
// 登录态 Store（Pinia）
// ----------------------------------------------------------------------------
// 作用：统一读写 localStorage 里的 JWT，避免各组件自己拼 key。
// 约定：组件只通过本 Store 取 Token，不直接访问 localStorage。
// ============================================================================
import { ref } from 'vue';
import { defineStore } from 'pinia';
export const useTokenStore = defineStore('token', () => {
    // 定义 token：初始值直接取本地存储，避免刷新页面后
    // 组件用 computed 跟随 Store 时读到空串（表现为刷新后掉登录态）
    const token = ref(localStorage.getItem('token') || '');
    function setToken(value) {
        token.value = value;
        localStorage.setItem('token', value); // 将 Token 保存至本地存储
    }
    // 获取 token（重新从本地存储同步一次，兼容外部直接改 localStorage 的情况）
    function getToken() {
        token.value = localStorage.getItem('token') || ''; // 从本地存储中获取 token
        return token.value;
    }
    return { token, setToken, getToken }; // 暴露变量及方法
});
