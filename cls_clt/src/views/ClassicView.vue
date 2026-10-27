<script setup>
// ============================================================================
// 作品详情页（/cls/:cid/:tid）
// ----------------------------------------------------------------------------
// 作用：展示原文、评分与书评区，支持发表书评与顶/踩。
// 教材：第六章 §6.3.1 作品详情与文学评价（本页基础）
//       第七章新增三处：§7.3.1 书评展示（p204）/ §7.3.2 书评发表（p210）/ §7.3.3 书评评价（p216）
// 约定：写操作必须带 JWT；未登录时按钮引导登录而不是静默失败。
// ============================================================================
import { ref, watch, inject, nextTick, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { poets } from '@/data/poets'; // 作者小传数据：用于右侧「作者画像」栏的朝代 / 头衔 / 简介
import { useTokenStore } from '@/stores/token'; // 引入 Token 状态管理
import HeaderComp from '@/components/HeaderComp.vue'; // 引入顶部导航栏组件
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
const axios = inject('axios'); // 注入 axios
const route = useRoute();
const router = useRouter(); // 书评区空态的「登录 / 注册」按钮跳转用
function goLogin() {
    router.push({ name: 'login' });
}
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
const token = ref(userStore.getToken()); // 获取登录用户的 Token（教材写法）
// ============================================================================
// 右侧「作者画像」栏所需数据
// ----------------------------------------------------------------------------
// portraitSrc：按作者名从头像映射表取 URL（src/assets/poets/<作者>.webp）。
//   clsData.author 与 poets.ts 的 name 一致（如「李白」），文件名即作者名。
// imgError：图片加载失败时翻成「朱红印章首字」兜底，避免出现裂图。
// authorInfo：从 poets.ts 取朝代 / 头衔 / 简介，丰富画像卡；取不到时仅显示姓名。
// ============================================================================
// 文学作品数据
// 教材写法：var clsData = ref({})；strict 下用 any，模板取属性才不报错
// 位置要求：必须声明在 portraitSrc / authorInfo 之前。watch(portraitSrc) 注册时会立即
//           求值一次以收集依赖，此时若 clsData 尚未赋值会抛 TypeError（页面整块白屏）。
var clsData = ref({});
const imgError = ref(false);
// 头像映射表：Vite 构建时把 src/assets/poets 下的图片输出为带哈希的 URL，
// 键取文件名去掉扩展名（即作者名），供下方按 clsData.author 直接查找。
const portraitMap = Object.fromEntries(Object.entries(import.meta.glob('../assets/poets/*.{png,webp}', {
    eager: true,
    query: '?url',
    import: 'default'
})).map(([path, url]) => [path.split('/').pop().replace(/\.(png|webp)$/, ''), url]));
const portraitSrc = computed(() => clsData.value.author ? portraitMap[clsData.value.author] || '' : '');
watch(portraitSrc, () => {
    imgError.value = false;
});
const authorInfo = computed(() => poets.find((p) => p.name === clsData.value.author) || null);
const cid = ref(''); // 文学作品编号 / 类型编号
const tid = ref('');
const star = ref(0); // 文学作品星级评价
const disDatas = ref([]); // 书评列表
const comment = ref(''); // 发表书评的输入内容
cid.value = String(route.params.cid ?? '');
tid.value = String(route.params.tid ?? '');
const activeIndex = ref('/clslist/' + route.params.tid); // 顶部导航栏菜单选中项索引（保持所属类型高亮）
// ============================================================================
// 【接口 8】获取文学作品信息 API
// 调用方式：GET 前端 /svr/api/classics/get-classic/<cid>
//                 后端 http://127.0.0.1:5382/api/classics/get-classic/2
// 参数：路径参数 cid —— 文学作品编号
// 返回结构：{ code:'200', data:{ cid, title, author, year, cover, describes, rating, ... } }
// 说明：教材直接把返回的 rating 赋给 star（本项目数据库 rating 是 0-100，比例问题后面再解决）
// ============================================================================
function initCls() {
    axios({
        method: 'get',
        url: '/svr/api/classics/get-classic/' + cid.value
    })
        .then(function (response) {
        if (response.data.code == '200') {
            clsData.value = response.data.data;
            star.value = clsData.value.rating; // 初始化文学星级评价
        }
    })
        .catch(function (error) {
        console.log(error);
    });
}
// ============================================================================
// 【接口 9】文学评价 API（教材 6.3.1 文学评价）
// 调用方式：POST 前端 /svr/api/classics/judge-classic
//                 后端 http://127.0.0.1:5382/api/classics/judge-classic
// 请求头：Authorization: Bearer <token>
// 请求体：{ "cid": 作品编号, "star": 星级(1-5) }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：未登录时评分组件为只读（disabled），登录后才可打分
// ============================================================================
// 教材写法是 (value) =>，本项目 strict 下隐式 any 会报错，补上 number 类型，逻辑一致
const judgeCls = (value) => {
    console.log('go judge' + value);
    var data = {
        cid: cid.value,
        star: value
    };
    axios({
        method: 'post',
        url: '/svr/api/classics/judge-classic',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + token.value
        },
        data: data
    })
        .then(function (response) {
        console.log(response.data);
        if (response.data.code == '200') {
            // 提示信息
            ElMessage({
                message: '评价成功！',
                type: 'success',
                plain: true
            });
        }
    })
        .catch(function (error) {
        console.log(error);
        // 鉴权判断
        if (error.response.status == 401 || error.response.status == 422) {
            token.value = ''; // 设置当前登录用户的 Token 为空
            userStore.setToken('');
            // 提示信息
            ElMessage({
                message: '请重新登录！',
                type: 'success',
                plain: true
            });
        }
    });
};
// ============================================================================
// 【接口 10】书评展示 API（教材 7.3.1）
// 调用方式：GET 前端 /svr/api/classics/get-discuss/<cid>
//                 后端 http://127.0.0.1:5382/api/classics/get-discuss/40
// 参数：路径参数 cid —— 文学作品编号
// 返回结构：{ code:'200', data:[{ did, cid, comment, cdate, topcount, lowcount,
//            user:{ uid, uname, nickname, avatar, sex, phone, remark } }] }
// 说明：后端已按评论时间倒序返回，前端直接渲染，不用再排序
// ============================================================================
function initDis() {
    axios({
        method: 'get',
        url: '/svr/api/classics/get-discuss/' + cid.value
    })
        .then(function (response) {
        if (response.data.code == '200') {
            disDatas.value = response.data.data;
            scrollToDiscuss(); // 列表渲染完再滚，否则高度还没撑开，定位会偏
        }
    })
        .catch(function (error) {
        console.log(error);
    });
}
// ============================================================================
// 【接口 11】发表书评 API（教材 7.3.2）
// 调用方式：POST 前端 /svr/api/classics/pub-discuss
//                 后端 http://127.0.0.1:5382/api/classics/pub-discuss
// 请求头：Authorization: Bearer <token>
// 请求体：{ "cid": 作品编号, "comment": 书评内容 }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：后端会把 classics.commentscount +1 保持库里同步；
//       前端不再跟着 +1，页面条数一律取 disDatas.length（以真实列表为准）
// ============================================================================
function pubDiscuss() {
    // 数据
    var data = {
        cid: cid.value,
        comment: comment.value
    };
    axios({
        method: 'post',
        url: '/svr/api/classics/pub-discuss',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + token.value
        },
        data: data
    })
        .then(function (response) {
        if (response.data.code == '200') {
            initDis(); // 发表书评成功后，刷新书评列表（列表长度即最新条数，无需手动加 1）
            comment.value = ''; // 清空评论信息
            // 提示信息
            ElMessage({
                message: '发表书评成功！',
                type: 'success',
                plain: true
            });
        }
    })
        .catch(function (error) {
        console.log(error);
        // 鉴权判断
        if (error.response.status == 401 || error.response.status == 422) {
            token.value = ''; // 设置当前登录用户的 Token 为空
            userStore.setToken('');
            // 提示信息
            ElMessage({
                message: '请重新登录！',
                type: 'success',
                plain: true
            });
        }
    });
}
// ============================================================================
// 【接口 12】书评评价 API（教材 7.3.3）
// 调用方式：POST 前端 /svr/api/classics/judge-discuss
//                 后端 http://127.0.0.1:5382/api/classics/judge-discuss
// 请求头：Authorization: Bearer <token>
// 请求体：{ "did": 评论编号, "toplow": 0 表示踩 / 1 表示顶 }
// 返回结构：{ code:'200', msg:'操作成功！' } / { code:'404', msg:'参数错误' }
// 说明：未登录时按钮为 disabled，不会触发本函数
// ============================================================================
// 顶、踩书评（0 表示踩，1 表示顶）
// 教材写法是 (did, judge) =>，strict 下补上 number 类型，逻辑一致
function judgeDiscuss(did, judge) {
    let data = {
        did: did,
        toplow: judge
    };
    axios({
        method: 'post',
        url: '/svr/api/classics/judge-discuss',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + token.value
        },
        data: data
    })
        .then(function (response) {
        if (response.data.code == '200') {
            initDis(); // 评价成功后，显示书评
            // 提示信息
            ElMessage({
                message: '评价成功！',
                type: 'success',
                plain: true
            });
        }
    })
        .catch(function (error) {
        // 鉴权判断
        if (error.response.status == 401 || error.response.status == 422) {
            token.value = ''; // 设置当前登录用户的 Token 为空
            userStore.setToken('');
            // 提示信息
            ElMessage({
                message: '请重新登录！',
                type: 'success',
                plain: true
            });
        }
    });
}
// 书评时间格式化
// 后端已统一返回 "YYYY-MM-DD HH:MM"，直接展示；
function formatDate(value) {
    if (!value)
        return '';
    if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(value))
        return value;
    const d = new Date(value);
    if (isNaN(d.getTime()))
        return value;
    const p = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ` +
        `${p(d.getHours())}:${p(d.getMinutes())}`;
}
/**
 * 从首页「诗人小传」点作品链接进来时（地址带 #discuss），自动滚动到书评区。
 * 目的：让「点链接即可看见书评」成立，不必再手动往下翻。
 */
function scrollToDiscuss() {
    if (route.hash !== '#discuss')
        return;
    nextTick(() => {
        const box = document.querySelector('.discuss-card');
        if (box) {
            box.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
}
watch(// 监听路由参数
() => route.params, (newValue, oldValue) => {
    cid.value = String(newValue.cid);
    tid.value = String(newValue.tid);
    imgError.value = false; // 切到另一本书时，重置画像加载失败标志（否则旧书的兜底印章会残留）
    initCls(); // 初始化文学作品信息
    comment.value = ''; // 初始化书评信息（教材 7.3，保留）
    initDis();
}, { immediate: true } // 使用 immediate: true 选项来强制侦听器的回调立即执行
);
</script>

<template>
  <el-container class="classic-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <div class="classic-wrap">
        <!-- 两栏布局：左侧书籍信息 + 右侧原文/评分/书评 -->
        <div class="classic-layout">
          <!-- 左侧：书籍信息（主要内容与时间）开始 -->
          <aside class="classic-side">
            <div class="side-card">
              <h3 class="side-title">书籍信息</h3>
              <dl class="side-list">
                <div class="side-row">
                  <dt class="side-label">书名</dt>
                  <dd class="side-value">{{ clsData.title }}</dd>
                </div>
                <div class="side-row">
                  <dt class="side-label">作者</dt>
                  <dd class="side-value">{{ clsData.author }}</dd>
                </div>
                <div class="side-row">
                  <dt class="side-label">成书时间</dt>
                  <dd class="side-value">{{ clsData.year }}</dd>
                </div>
                <div class="side-row">
                  <dt class="side-label">体裁出处</dt>
                  <dd class="side-value">{{ clsData.present }}</dd>
                </div>
                <div class="side-row">
                  <dt class="side-label">平均评分</dt>
                  <dd class="side-value">{{ clsData.rating }}</dd>
                </div>
                <div class="side-row">
                  <dt class="side-label">书评数量</dt>
                  <dd class="side-value">{{ disDatas.length }} 条</dd>
                </div>
              </dl>

              <h4 class="side-subtitle">主要内容</h4>
              <p class="side-summary">
                {{ clsData.summary || '暂无简介' }}
              </p>
              <!-- 书评区锚点：首页诗人小传的作品链接带 #discuss -->
              <a class="side-jump" href="#discuss">直达本书书评 ↓</a>
            </div>
          </aside>
          <!-- 左侧：书籍信息结束 -->

          <!-- 右侧：原有内容开始 -->
          <div class="classic-main">
        <!-- 教材 6.3.1 文学作品展示开始 -->
        <el-result :title="clsData.title">
          <template #icon>
            <el-image
              style="width: auto; height: 300px"
              :src="String('/svr/api/image/display/cls/') + clsData.cover"
              fit="contain" />
          </template>
          <template #sub-title>
            <el-text>{{ clsData.author }}</el-text>
            <el-text>{{ clsData.year }}</el-text><br />
            <el-text>评价：</el-text>
            <el-rate v-if="token == ''" disabled v-model="star" @change="judgeCls" />
            <el-rate v-if="token != ''" v-model="star" @change="judgeCls" />
          </template>
          <template #extra>
            <el-row><div v-html="clsData.describes"></div></el-row>
          </template>
        </el-result>
        <!-- 教材 6.3.1 文学作品展示结束 -->

        <!-- ================= 书评区（教材 7.3） ================= -->
        <!-- 结构用样式表里已有的 .discuss-card 一套：卡片自带 text-align:left，
             否则会跟随 #app 的居中，正文缩到行中间去 -->
        <!-- id="discuss"：左侧书籍信息里的「直达本书书评」以及首页诗人小传的作品链接
             都指向这个锚点 -->
        <div id="discuss" class="discuss-card">
          <div class="discuss-head">
            <span class="discuss-title">书评信息</span>
            <!-- 条数取实际拿到的数组长度：classics.commentscount 是历史遗留的静态数字，
                 会和列表对不上（显示几千条却一条都没有） -->
            <span class="discuss-count">{{ disDatas.length }} 条</span>
          </div>

          <!-- 空态：图标 + 标题 + 引导按钮，替代原来孤零零的一行字 -->
          <div v-if="disDatas.length === 0" class="discuss-empty">
            <div class="discuss-empty-glyph">评</div>
            <p class="discuss-empty-title">还没有书评</p>
            <p class="discuss-empty-sub">读后感想值得被看见——来做第一个写书评的人</p>
            <el-button
              v-if="token == ''"
              class="discuss-empty-btn"
              type="primary"
              plain
              size="small"
              @click="goLogin">
              登录 / 注册
            </el-button>
          </div>

          <div v-else class="discuss-list">
            <div v-for="item in disDatas" :key="item.did" class="discuss-item">
              <el-avatar
                :size="38"
                class="discuss-avatar"
                :src="String('/svr/api/image/display/head/') + item.user.avatar">
                {{ item.user.nickname ? item.user.nickname.charAt(0) : '诗' }}
              </el-avatar>
              <div class="discuss-main">
                <div class="discuss-meta">
                  <span class="discuss-nick">{{ item.user.nickname }}</span>
                  <span class="discuss-date">{{ formatDate(item.cdate) }}</span>
                </div>
                <p class="discuss-text">{{ item.comment }}</p>
              </div>
              <!-- 顶/踩：登录后可点，未登录置灰（样式见 .act-btn） -->
              <div class="discuss-actions">
                <button type="button" class="act-btn" :disabled="token == ''"
                        @click="judgeDiscuss(item.did, 1)">
                  <el-icon><CaretTop /></el-icon><span>顶 {{ item.topcount }}</span>
                </button>
                <button type="button" class="act-btn down" :disabled="token == ''"
                        @click="judgeDiscuss(item.did, 0)">
                  <el-icon><CaretBottom /></el-icon><span>踩 {{ item.lowcount }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 发表书评：登录后显示输入框；未登录只在「有书评」时提示，
               空态的引导已经在上面出现过，不重复 -->
          <div v-if="token != ''" class="discuss-pub">
            <el-input
              v-model="comment"
              :autosize="{ minRows: 2, maxRows: 4 }"
              type="textarea"
              placeholder="说说你读这首诗的感受…"
            />
            <div class="discuss-pub-bar">
              <el-button type="primary" @click="pubDiscuss">发表书评</el-button>
            </div>
          </div>
          <p v-else-if="disDatas.length > 0" class="discuss-login-tip">
            登录后可以发表书评，与更多读者交流读后感
          </p>
        </div>
          <!-- 右侧：原有内容结束 -->
        </div>

        <!-- 右栏：作者画像（与左侧书籍信息对称，滚动长文时跟随）开始 -->
        <aside class="classic-author">
          <div class="author-card">
            <div class="author-portrait">
              <img
                v-if="!imgError"
                :src="portraitSrc"
                :alt="clsData.author"
                @error="imgError = true" />
              <!-- 无画像时退回朱红印章首字，风格与首页「诗人小传」一致 -->
              <div v-else class="author-seal">{{ (clsData.author || '作').charAt(0) }}</div>
            </div>
            <h3 class="author-name">{{ clsData.author }}</h3>
            <p v-if="authorInfo" class="author-meta">
              <span class="author-dynasty">{{ authorInfo.dynasty }}</span>
              <span class="author-title">{{ authorInfo.title }}</span>
            </p>
            <p v-if="authorInfo" class="author-intro">{{ authorInfo.intro }}</p>
          </div>
        </aside>
        <!-- 右栏：作者画像结束 -->
      </div>
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.classic-container {
  min-height: 100vh;
}

.classic-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 12px 32px;
}

.classic-card {
  border: 1px solid #ece0cb;
  border-radius: 10px;
  background:
    radial-gradient(circle at 12% 10%, rgba(168, 53, 44, 0.035), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
}

.classic-body {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

/* 封面：固定宽高比，避免不同尺寸图片把版式撑歪 */
.classic-cover {
  flex: 0 0 260px;
  width: 260px;
  aspect-ratio: 3 / 4;
  border-radius: 8px;
  overflow: hidden;
  background: #f5eddd;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ece0cb;
}

.classic-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.cover-fallback {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 72px;
  color: #b8a488;
}

.classic-info {
  flex: 1;
  text-align: left;
  min-width: 0;
}

.classic-title {
  margin: 4px 0 10px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 26px;
  letter-spacing: 3px;
  color: #3b2f24;
}

.classic-meta {
  margin: 0 0 14px;
  font-size: 13px;
  color: #8c7a63;
}

.meta-sep {
  margin: 0 6px;
}

.classic-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-label,
.judge-label {
  font-size: 13px;
  color: #8c7a63;
}

.rating-num {
  font-size: 13px;
  color: #a8352c;
}

.classic-describes {
  margin: 0;
  font-size: 14px;
  line-height: 1.9;
  color: #4a3a2a;
  text-indent: 2em;
}

.classic-judge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px dashed #e6d8bf;
}

/* 可打分星级：未点亮图标默认近白色，在宣纸底上几乎看不见，统一调深 */
.classic-judge :deep(.el-rate) {
  --el-rate-void-color: #bda67f;
  --el-rate-disabled-void-color: #bda67f;
}

/* ==================== 详情页两栏布局 ==================== */
/* 左：书籍信息卡（固定 280px）；右：原文 + 评分 + 书评。
   窄屏改为上下堆叠，信息卡收窄成整行，不挤压正文 */
.classic-layout {
  display: flex;
  align-items: flex-start;
  gap: 22px;
}

.classic-side {
  flex: 0 0 280px;
  position: sticky;      /* 滚动长文时信息卡跟随 */
  top: 76px;
}

.classic-main {
  flex: 1 1 auto;
  min-width: 0;
}

/* 右栏：作者画像卡（固定 240px，与左栏书籍信息对称，滚动时跟随） */
.classic-author {
  flex: 0 0 240px;
  position: sticky;
  top: 76px;
}

.author-card {
  padding: 16px 16px 18px;
  border: 1px solid #e6d8bf;
  border-radius: 10px;
  background:
    radial-gradient(circle at 90% 4%, rgba(168, 53, 44, 0.04), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  text-align: center;
}

/* 画像：固定 3:4 竖版，避免不同尺寸把卡片撑歪 */
.author-portrait {
  width: 100%;
  aspect-ratio: 3 / 4;
  border-radius: 8px;
  overflow: hidden;
  background: #f5eddd;
  border: 1px solid #ece0cb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 无画像兜底：朱红方印 + 首字，与首页「诗人小传」印章同款 */
.author-seal {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 8px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 34px;
  color: #fdf6e8;
  background-color: #a8352c;
  box-shadow: 0 3px 8px rgba(168, 53, 44, 0.24);
}

.author-name {
  margin: 14px 0 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 18px;
  letter-spacing: 2px;
  color: #3b2f24;
}

.author-meta {
  margin: 8px 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
}

.author-dynasty {
  padding: 1px 8px;
  border-radius: 999px;
  color: #8c7a63;
  background-color: #f3ead9;
}

.author-title {
  color: #a2917a;
}

.author-intro {
  margin: 10px 0 0;
  text-align: left;
  font-size: 13px;
  line-height: 1.85;
  color: #4a3b2a;
  /* 卡片高度统一：超出四行截断 */
  display: -webkit-box;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.side-card {
  padding: 18px 20px 16px;
  border: 1px solid #e6d8bf;
  border-radius: 10px;
  background:
    radial-gradient(circle at 90% 4%, rgba(168, 53, 44, 0.04), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  text-align: left;
}

.side-title {
  margin: 0 0 14px;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 17px;
  letter-spacing: 4px;
  color: #3b2f24;
}

.side-list {
  margin: 0;
}

.side-row {
  display: flex;
  gap: 10px;
  padding: 7px 0;
  border-bottom: 1px dashed #f2e8d6;
}

.side-label {
  flex: 0 0 62px;
  font-size: 13px;
  color: #a2917a;
}

.side-value {
  margin: 0;
  font-size: 14px;
  color: #4a3b2a;
  word-break: break-word;
}

.side-subtitle {
  margin: 16px 0 8px;
  font-size: 14px;
  letter-spacing: 2px;
  color: #6b5844;
}

.side-summary {
  margin: 0;
  font-size: 13.5px;
  line-height: 1.9;
  color: #4a3b2a;
}

/* 左侧卡片里的「直达书评」按钮 */
.side-jump {
  display: inline-block;
  margin-top: 16px;
  padding: 5px 14px;
  border: 1px solid #d9c3a4;
  border-radius: 999px;
  font-size: 13px;
  color: #a8352c;
  text-decoration: none;
  background-color: #fff9ef;
  transition: background-color 0.15s ease;
}

.side-jump:hover {
  background-color: #f8f1e4;
}

@media (max-width: 1000px) {
  .classic-layout {
    flex-direction: column;
  }

  .classic-side,
  .classic-author {
    flex: none;
    position: static;
    width: 100%;
  }

  /* 窄屏下画像别拉太宽，居中显示更像一张立像 */
  .author-portrait {
    width: 200px;
    margin: 0 auto;
  }
}

/* ================= 书评区样式 ================= */
.discuss-card {
  margin-top: 16px;
  padding: 4px 20px 12px;
  border: 1px solid #ece0cb;
  border-radius: 10px;
  /* main.css 里 #app 是整体居中的，书评区要强制左对齐，否则正文会跑到行中间 */
  text-align: left;
  background:
    radial-gradient(circle at 88% 6%, rgba(168, 53, 44, 0.03), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
}

/* 头像：文件缺失时退回「首字」色块，避免出现灰色空圆 */
.discuss-avatar {
  flex: none;
  font-size: 14px;
  color: #7a6449;
  background: #efe2cc;
  border: 1px solid #e6d8bf;
}

.discuss-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px dashed #e6d8bf;
}

.discuss-title {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 17px;
  letter-spacing: 4px;
  color: #3b2f24;
}

.discuss-count {
  /* 条数做成小徽章，比裸文字更像「统计」 */
  padding: 1px 10px;
  border-radius: 999px;
  font-size: 12px;
  color: #8c7a63;
  background-color: #f3ead9;
}

.discuss-empty {
  /* 空态：图标 + 标题 + 引导，纵向居中，别再是一条孤零零的字 */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 0 26px;
  text-align: center;
}

.discuss-empty-glyph {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  margin-bottom: 12px;
  border-radius: 50%;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 20px;
  color: #b3a48d;
  background-color: #f3ead9;
}

.discuss-empty-title {
  margin: 0;
  font-size: 15px;
  color: #6b5844;
}

.discuss-empty-sub {
  margin: 6px 0 0;
  font-size: 13px;
  color: #a2917a;
}

.discuss-empty-btn {
  margin-top: 14px;
}

.discuss-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.discuss-item {
  display: flex;
  gap: 12px;
  padding: 18px 0;
  border-bottom: 1px solid #f2e8d6;
}

.discuss-item:last-child {
  border-bottom: none;
}

.discuss-main {
  flex: 1;
  min-width: 0;
}

.discuss-meta {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.discuss-nick {
  font-size: 13px;
  color: #6b5844;
}

.discuss-date {
  font-size: 12px;
  color: #b3a48d;
}

.discuss-text {
  margin: 6px 0 8px;
  font-size: 14px;
  line-height: 1.85;
  color: #4a3a2a;
  word-break: break-word;
}

.discuss-actions {
  /* flex:none 防止按钮被压窄导致「顶 5」折行；
     align-items/align-self 让按钮保持胶囊高度——
     默认 stretch 会把按钮拉到整行高，胶囊就成了一个个圆 */
  display: flex;
  flex: none;
  align-self: flex-start;
  align-items: center;
  gap: 8px;
}

/* 顶/踩：做成低调的胶囊按钮，避免 Element Plus 默认按钮把版面压重 */
.act-btn {
  /* 图标 + 文字横向居中，图标不会和文字错行 */
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 12px;
  font-size: 12px;
  line-height: 1.6;
  color: #8c7a63;
  background: #fbf6ec;
  border: 1px solid #ece0cb;
  border-radius: 999px;
  cursor: pointer;
  white-space: nowrap;   /* 同上：绝不折行 */
  transition: all 0.15s ease;
}

.act-btn .el-icon {
  font-size: 14px;
}

.act-btn:hover:not(:disabled) {
  color: #a8352c;
  border-color: #d9c3a4;
  background: #fff9ef;
}

.act-btn.down:hover:not(:disabled) {
  color: #5a6b7a;
}

.act-btn:disabled {
  color: #bdb0a0;
  cursor: not-allowed;
}

/* 未登录禁用时图标一起变灰，避免文字灰了图标还亮着 */
.act-btn:disabled .el-icon {
  color: #cdc2b2;
}

.discuss-pub {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px dashed #e6d8bf;
}

.discuss-pub-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.discuss-login-tip {
  margin: 10px 0 0;
  padding-top: 12px;
  font-size: 13px;
  color: #8c7a63;
  text-align: center;
  border-top: 1px dashed #e6d8bf;
}

.login-link {
  color: #a8352c;
  text-decoration: none;
  border-bottom: 1px solid rgba(168, 53, 44, 0.35);
}

.login-link:hover {
  border-bottom-color: #a8352c;
}

/* 窄屏：封面在上，信息在下 */
@media (max-width: 760px) {
  .classic-body {
    flex-direction: column;
    align-items: center;
  }

  .classic-cover {
    flex: none;
    width: 60%;
  }

  .classic-info {
    width: 100%;
  }
}
</style>
