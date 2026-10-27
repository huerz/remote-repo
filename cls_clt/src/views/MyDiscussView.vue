<script setup>
// ============================================================================
// 我的书评（/mydis）
// ----------------------------------------------------------------------------
// 作用：列出当前登录用户发表的书评，支持查看与删除。
// 教材：第八章新增功能 §8.3.4 开发我的书评展示功能（p249）
//       第六章的书评只做展示与发表，本页是第八章新加的「我的书评」管理页
// 约定：只显示本人数据，uid 由后端从 Token 解析。
// ============================================================================
import { ref } from 'vue';
import { inject } from 'vue';
import { onMounted } from 'vue';
import HeaderComp from '../components/HeaderComp.vue'; // 引入顶部导航栏组件
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
import AsideComp from '@/components/AsideComp.vue'; // 引入侧边栏导航组件
import { useTokenStore } from '@/stores/token'; // 引入状态管理文件
const axios = inject('axios'); // 注入 axios
const activeIndex = ref('/user'); // 顶部导航栏菜单选中项索引
const asideIndex = ref('/mydis'); // 侧边栏菜单选中项索引
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
const token = ref(userStore.getToken()); // 获取登录用户的 Token
// 文学评论数据
// 教材写法：var disDatas = ref({})；strict 下用 any，模板取属性才不报错
var disDatas = ref({});
function initDis() {
    // 判断 Token 是否存在
    if (token.value != '') {
        axios({
            method: 'get',
            url: '/svr/api/classics/get-mydiscuss',
            headers: {
                Authorization: 'Bearer ' + token.value
            }
        })
            .then(function (response) {
            if (response.data.code == '200') {
                disDatas.value = response.data.data; // 获取书评列表
            }
        })
            .catch(function (error) {
            // 鉴权判断
            if (error.response.status == 401 || error.response.status == 422) {
                token.value = ''; // 没有权限或权限已过期，设置 Token 为空
                userStore.setToken('');
            }
        });
    }
}
onMounted(() => {
    initDis(); // 初始化书评列表
});
</script>

<template>
  <el-container>
    <el-header>
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <el-container>
      <el-aside width="200px">
        <AsideComp :aside-index="asideIndex" />
      </el-aside>
      <el-container>
        <el-main>
          <div>
            <el-page-header>
              <template #icon>
                <el-icon><ChatLineRound /></el-icon>
              </template>
              <template #title>我的书评</template>
              <div style="margin-top: 10px">
                <el-descriptions
                  v-for="item in disDatas"
                  :key="item.did"
                  class="margin-top"
                  :column="1">
                  <template #title>
                    <el-avatar
                      :size="35"
                      :src="String('/svr/api/image/display/cls/') + item.classic.cover"
                      style="vertical-align: middle"/>
                    <el-text type="primary" size="large" style="margin-left: 5px">
                      {{ item.classic.title }}
                    </el-text>
                  </template>
                  <el-descriptions-item>
                    <div style="margin-left: 80px">
                      <el-text class="mx-1" size="large">{{ item.comment }}</el-text>
                    </div>
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </el-page-header>
          </div>
        </el-main>
        <el-footer>
          <el-footer><FooterComp /></el-footer>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<style scoped>
/* 页头图标（el-page-header 的 icon 插槽）：统一尺寸与站点色，
   默认会继承成黑色，在这套宣纸背景里显得突兀 */
.el-page-header__icon .el-icon {
  font-size: 18px;
  color: #a8352c;
}
</style>
