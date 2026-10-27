<script setup lang="ts">
import { ref, computed, watch, onMounted, inject } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import type { AxiosInstance } from 'axios'
import type { ApiResult, Film, Filmtype } from '@/types'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'

// 教材写法：const axios = inject('axios')
// 本项目 tsconfig 开了 strict，inject 返回 unknown，断言成 AxiosInstance 才能调用
const axios = inject('axios') as AxiosInstance
const route = useRoute()

// 当前类型编号 / 当前类型的电影列表
const tid = ref('')
const clsDatas = ref<any>({})
// 全部类型（筛选栏「类型」那一行用）
const typeList = ref<Filmtype[]>([])

// 顶部导航栏菜单选中项索引
const activeIndex = ref('/filmlist/' + route.params.tid)

// ===== 筛选条件 =====
const decade = ref('')       // '' 全部 / 2020 / 2010 / 2000 / 1990 / older
const minRating = ref(0)     // 0 全部 / 9 / 8 / 7
const sortBy = ref('default') // default / rating / year

const DECADES = [
  { value: '', label: '全部' },
  { value: '2020', label: '2020 年代' },
  { value: '2010', label: '2010 年代' },
  { value: '2000', label: '2000 年代' },
  { value: '1990', label: '90 年代' },
  { value: 'older', label: '更早' }
]

const RATINGS = [
  { value: 0, label: '全部' },
  { value: 9, label: '9 分以上' },
  { value: 8, label: '8 分以上' },
  { value: 7, label: '7 分以上' }
]

const SORTS = [
  { value: 'default', label: '默认' },
  { value: 'rating', label: '评分优先' },
  { value: 'year', label: '年份优先' }
]

// 筛选 + 排序后的列表
const filteredFilms = computed<Film[]>(() => {
  let list = [...((clsDatas.value?.films as Film[]) || [])]

  if (decade.value) {
    list = list.filter(function (f) {
      const y = parseInt(f.year || '0', 10) || 0
      if (decade.value === 'older') return y < 1990
      const start = parseInt(decade.value, 10)
      return y >= start && y < start + 10
    })
  }

  if (minRating.value) {
    list = list.filter(function (f) { return (f.rating || 0) >= minRating.value })
  }

  if (sortBy.value === 'rating') {
    list.sort(function (a, b) { return (b.rating || 0) - (a.rating || 0) })
  } else if (sortBy.value === 'year') {
    list.sort(function (a, b) {
      return (parseInt(b.year || '0', 10) || 0) - (parseInt(a.year || '0', 10) || 0)
    })
  }
  return list
})

// 切换类型时清空筛选，避免「新类型 + 旧条件」筛出空白
function resetFilters() {
  decade.value = ''
  minRating.value = 0
  sortBy.value = 'default'
}

watch(
  () => route.params,
  (newValue) => {
    tid.value = String(newValue.tid)
    resetFilters()
    initClsList()
  },
  { immediate: true }
)

// ============================================================================
// 【接口】电影列表 API（教材 6.3.3）
// 调用方式：GET 前端 /svr/api/films/get-films/<tid>
//                 后端 http://127.0.0.1:5383/api/films/get-films/1
// 返回：{ code:'200', data:{ tid, name, cover, films:[{...}] } }
// ============================================================================
function initClsList() {
  axios<ApiResult<any>>({
    method: 'get',
    url: '/svr/api/films/get-films/' + tid.value
  })
  .then(function (response) {
    if (response.data.code == '200') {
      clsDatas.value = response.data.data
    }
  })
  .catch(function (error) {
    console.log(error)
  })
}

// ============================================================================
// 【接口】电影类型 API（筛选栏「类型」一行）
// 调用方式：GET /svr/api/films/get-filmtypes
// 返回：{ code:'200', data:[{ tid, name, cover, remark }] }
// ============================================================================
function initTypes() {
  axios<ApiResult<Filmtype[]>>({
    method: 'get',
    url: '/svr/api/films/get-filmtypes'
  })
  .then(function (response) {
    if (response.data.code == '200') {
      typeList.value = response.data.data
    }
  })
  .catch(function (error) {
    console.log(error)
  })
}

onMounted(() => {
  initTypes()
})
</script>

<template>
  <el-container>
    <el-header>
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <el-main>
      <!-- ==================== 标题栏 ==================== -->
      <div class="list-head">
        <h1 class="list-title">{{ clsDatas.name || '电影列表' }}</h1>
        <span class="list-count">共 {{ filteredFilms.length }} 部</span>
      </div>

      <!-- ==================== 筛选栏 ==================== -->
      <div class="filter-bar">
        <!-- 类型：切换即跳路由 -->
        <div class="filter-row">
          <span class="filter-label">类型</span>
          <div class="filter-opts">
            <RouterLink class="opt" to="/search/all">全部</RouterLink>
            <RouterLink
              v-for="t in typeList"
              :key="t.tid"
              class="opt"
              :class="{ active: String(t.tid) === tid }"
              :to="String('/filmlist/' + t.tid)">
              {{ t.name }}
            </RouterLink>
          </div>
        </div>

        <!-- 年代 -->
        <div class="filter-row">
          <span class="filter-label">年代</span>
          <div class="filter-opts">
            <button
              v-for="d in DECADES"
              :key="d.value"
              type="button"
              class="opt"
              :class="{ active: decade === d.value }"
              @click="decade = d.value">
              {{ d.label }}
            </button>
          </div>
        </div>

        <!-- 评分 -->
        <div class="filter-row">
          <span class="filter-label">评分</span>
          <div class="filter-opts">
            <button
              v-for="r in RATINGS"
              :key="r.value"
              type="button"
              class="opt"
              :class="{ active: minRating === r.value }"
              @click="minRating = r.value">
              {{ r.label }}
            </button>
          </div>
        </div>

        <!-- 排序 -->
        <div class="filter-row">
          <span class="filter-label">排序</span>
          <div class="filter-opts">
            <button
              v-for="s in SORTS"
              :key="s.value"
              type="button"
              class="opt"
              :class="{ active: sortBy === s.value }"
              @click="sortBy = s.value">
              {{ s.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- ==================== 电影网格 ==================== -->
      <el-row :gutter="18" class="film-grid">
        <el-col
          v-for="item in filteredFilms"
          :key="item.cid"
          :xs="12" :sm="8" :md="6" :lg="4">
          <RouterLink class="film-link" :to="String('/film/' + item.cid) + String('/') + item.tid">
            <el-card class="film-card" shadow="hover" :body-style="{ padding: '0px' }">
              <img
                class="film-cover"
                :src="String('/svr/api/image/display/film/' + item.cover)"
                alt="" />
              <div class="film-info">
                <div class="film-name" :title="item.title">{{ item.title }}</div>
                <div class="film-meta">
                  <span>{{ item.year }}</span>
                  <span class="film-rating">{{ item.rating }}</span>
                </div>
              </div>
            </el-card>
          </RouterLink>
        </el-col>
      </el-row>

      <el-empty v-if="!filteredFilms.length" description="这个条件下没有影片" />
      <el-divider border-style="dotted" />
    </el-main>
    <el-footer><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
/* ==================== 标题 ==================== */
.list-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  max-width: 1320px;
  margin: 8px auto 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e8dcbe;
}

.list-title {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #2a2119;
}

.list-count {
  font-size: 13px;
  color: #9a7b53;
}

/* ==================== 筛选栏 ==================== */
.filter-bar {
  max-width: 1320px;
  margin: 0 auto 18px;
  padding: 14px 18px;
  border: 1px solid #ece0c8;
  border-radius: 8px;
  background: #fffdf8;
}

.filter-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 6px 0;
}

.filter-row + .filter-row {
  border-top: 1px dashed #f0e6cf;
}

.filter-label {
  flex: 0 0 40px;
  padding-top: 4px;
  font-size: 13px;
  color: #b39a78;
}

.filter-opts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 每个筛选项：默认淡，选中变金底白字 */
.opt {
  padding: 4px 12px;
  border: none;
  border-radius: 14px;
  background: transparent;
  font-size: 13px;
  color: #6b5a45;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.18s ease, color 0.18s ease;
}

.opt:hover {
  background: #f6ecdc;
  color: #8a5a20;
}

.opt.active {
  background: #b8892f;
  color: #fff8e6;
}

/* ==================== 卡片 ==================== */
.film-grid {
  max-width: 1320px;
  margin: 0 auto;
}

.film-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.film-card {
  margin-bottom: 18px;
  border-color: #ece0c8;
  background: #fffdf8;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.film-card:hover {
  transform: translateY(-4px);
}

.film-cover {
  display: block;
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  background: #f6ecdc;
}

.film-info {
  padding: 8px 10px 10px;
}

.film-name {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 14px;
  color: #2a2119;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.film-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
  font-size: 12px;
  color: #9a7b53;
}

.film-rating {
  font-weight: 600;
  color: #b8892f;
}
</style>
