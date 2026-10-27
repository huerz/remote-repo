<script lang="ts" setup>
import { ref } from 'vue'
import { inject } from 'vue'
import { onMounted } from 'vue'
import type { AxiosInstance } from 'axios'
// 引入顶部导航栏组件
import HeaderComp from '../components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'
// 引入侧边栏导航组件
import AsideComp from '@/components/AsideComp.vue'
// 引入状态管理文件
import { useTokenStore } from '@/stores/token'

const axios = inject('axios') as AxiosInstance // 注入 axios

// 顶部导航栏菜单选中项索引
const activeIndex = ref('/user')
// 侧边栏菜单选中项索引
const asideIndex = ref('/mydis')
// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 获取登录用户的 Token
const token = ref(userStore.getToken())
// 电影评论数据
// 教材写法：var disDatas = ref({})；strict 下用 any，模板取属性才不报错
var disDatas = ref<any>({})

// 调用 API，获取影评列表
function initDis() {
  // 判断 Token 是否存在
  if (token.value != '') {
    axios({
      method: 'get',
      url: '/svr/api/films/get-mydiscuss',
      headers: {
        Authorization: 'Bearer ' + token.value
      }
    })
    .then(function (response) {
      if (response.data.code == '200') {
        // 获取影评列表
        disDatas.value = response.data.data
      }
    })
    .catch(function (error) {
      // 鉴权判断
      if (error.response.status == 401 || error.response.status == 422) {
        // 没有权限或权限已过期，设置 Token 为空
        token.value = ''
        userStore.setToken('')
      }
    })
  }
}

// 完成初始渲染并创建 DOM 节点后，进行页面加载
onMounted(() => {
  // 初始化影评列表
  initDis()
})
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
              <template #title>我的影评</template>
              <div style="margin-top: 10px">
                <el-descriptions
                  v-for="item in disDatas"
                  :key="item.did"
                  class="margin-top"
                  :column="1">
                  <template #title>
                    <el-avatar
                      :size="35"
                      :src="String('/svr/api/image/display/film/') + item.classic.cover"
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
