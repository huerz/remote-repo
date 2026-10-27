<script setup>
// ============================================================================
// 文学列表页（/clslist/:tid）
// ----------------------------------------------------------------------------
// 作用：按类型编号拉该类型下的全部作品并以卡片列出。
// 约定：tid 只从路由参数取，不依赖 query。
// ============================================================================
import { ref, watch } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { inject } from 'vue';
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue';
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
// 教材写法：const axios = inject('axios')
// 本项目 tsconfig 开了 strict，inject 返回 unknown，断言成 AxiosInstance 才能调用
const axios = inject('axios'); // 注入 axios
const route = useRoute(); // 创建路由对象
const tid = ref(''); // 文学作品类型编号
// 文学列表
// 教材写法：var clsDatas = ref({})
// strict 下 ref({}) 会被推断成 {}，模板里取 .cover / .classics 会报属性不存在，故用 any
var clsDatas = ref({});
// 教材写法：tid.value = route.params.tid
// route.params.tid 的类型是 string | string[]，这里用 String() 取字符串
tid.value = String(route.params.tid);
watch(// 监听路由参数变化
() => route.params, (newValue, oldValue) => {
    tid.value = String(newValue.tid);
    initClsList(); // 初始化文学列表
}, { immediate: true } // 使用 immediate: true 选项来强制侦听器的回调立即执行
);
const activeIndex = ref('/clslist/' + route.params.tid); // 顶部导航栏菜单选中项索引
function initClsList() {
    axios({
        method: 'get',
        url: '/svr/api/classics/get-classics/' + tid.value
    })
        .then(function (response) {
        if (response.data.code == '200') {
            clsDatas.value = response.data.data;
        }
    })
        .catch(function (error) {
        console.log(error);
    });
}
</script>

<template>
  <el-container>
    <el-header>
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <el-main>
      <div>
        <!-- 教材 6.3.1 文学列表展示开始 -->
        <el-page-header>
          <template #icon>
            <el-avatar
              :size="30"
              class="mr-3"
              :src="String('/svr/api/image/display/head/' + clsDatas.cover)"
              style="vertical-align: middle" />
          </template>
          <template #title>{{ clsDatas.name }}</template>
          <div class="mt-4 text-sm font-bold">
            <el-row justify="center" :gutter="20">
              <el-col :span="4" v-for="item in clsDatas.classics" :key="item.cid">
                <el-card style="padding: '0px'">
                  <template #header>{{ item.title }}</template>
                  <RouterLink :to="String('/cls/' + item.cid) + String('/') + item.tid">
                    <img
                      :src="String('/svr/api/image/display/cls/' + item.cover)"
                      style="width: 100%; display: block"/>
                  </RouterLink>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-page-header>
        <!-- 教材 6.3.1 文学列表展示结束 -->
        <el-divider border-style="dotted" />
      </div>
    </el-main>
    <el-footer><FooterComp /></el-footer>
  </el-container>
</template>
