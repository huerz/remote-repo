<script setup>
// ============================================================================
// 顶部导航栏
// ----------------------------------------------------------------------------
// 作用：Logo、按数据库动态渲染的类型菜单、右侧用户头像/登录入口。
// 教材：第五章 §5.2.5 Menu 做顶部导航、Avatar 做右上角用户区（图 5.11）
//       第六章 §6.3.1 导航栏用户中心显示（登录后展示头像与昵称）
// 约定：菜单项来自 /api/classics/get-classictypes，不在前端写死类型名。
// ============================================================================
import { ref, inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token';
// ============================================================================
// 【接口 1】图片显示 API（Logo / 用户头像）
// 调用方式：GET  前端 /svr/api/image/display/head/logo.png
//                 后端 http://127.0.0.1:5382/api/image/display/head/logo.png
// 说明：/svr 是 vite.config.ts 里配置的代理前缀，转发到 5382 并去掉该前缀
// 路径参数：
//   type     = head（用户头像类） / cls（文学作品封面类）
//   filename = 图片文件名，如 logo.png、tx.png
// 返回：图片二进制流（Content-Type: image/jpg）；文件不存在返回 404 + JSON
// ============================================================================
const logo_url = ref('/svr/api/image/display/head/logo.png'); // 构建 Logo 及用户头像默认图片的 URL
const user_url = ref('/svr/api/image/display/head/tx.png');
const axios = inject('axios'); // 注入 axios（main.ts 中 provide 的是 AxiosInstance）
const props = defineProps({ activeIndex: String }); // 用于接收传递组件的数据，此处传递的是菜单选中项索引
const activeIndex = props.activeIndex; // 设置菜单选中项索引
const navDatas = ref([]); // 导航栏数据列表
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
const token = ref(userStore.getToken()); // 获取登录用户的 Token
const router = useRouter(); // 路由对象：下拉菜单里的「个人中心 / 评价记录 / 退出登录」都是编程式跳转
const nickname = ref(''); // 登录用户的昵称，显示在头像右侧（后端没给昵称时退化成账号名）
/**
 * 处理头像下拉菜单的点击。
 *
 * @param command 菜单项标识：user=个人中心，mydiscuss=评价记录，logout=退出登录，
 *                login=登录，register=注册（未登录时用）
 */
function handleCommand(command) {
    if (command === 'user') {
        router.push({ name: 'user' });
    }
    else if (command === 'mydiscuss') {
        router.push({ name: 'mydis' });
    }
    else if (command === 'logout') {
        // 教材 6.3.1 用户退出：退出页会清 Token 并跳回首页，逻辑收在 OutView 里，这里只负责跳转
        router.push({ name: 'out' });
    }
    else if (command === 'login') {
        router.push({ name: 'login' });
    }
    else if (command === 'register') {
        router.push({ name: 'register' });
    }
}
// ============================================================================
// 【接口 2】文学导航 API（首页顶部导航栏的文学作品类型）
// 调用方式：GET  前端 /svr/api/classics/get-classictypes
//                 后端 http://127.0.0.1:5382/api/classics/get-classictypes
// 请求参数：无
// 返回结构：{ code: '200', msg: '操作成功！', data: [ { tid, name, cover, remark } ] }
// 用途：把 data 列表循环渲染成 el-menu-item，构成动态导航菜单
// ============================================================================
function initNav() {
    axios({
        method: 'get',
        url: '/svr/api/classics/get-classictypes'
    }).then(function (response) {
        if (response.data.code == '200') {
            navDatas.value = response.data.data;
        }
    }).catch(function (error) {
        console.log(error);
    });
}
// ============================================================================
// 【接口】查询登录用户信息 API（教材 6.3.1 导航栏用户中心显示）
// 调用方式：GET  前端 /svr/api/user/get-user
//                 后端 http://127.0.0.1:5382/api/user/get-user
// 请求头：Authorization: Bearer <token>
// 参数：无（用户编号由后端从 Token 中解析）
// 返回结构：{ code:'200', msg, data:{ uid, uname, nickname, avatar, sex, phone } }
// 用途：拿到 avatar 后拼成头像地址，显示在导航栏右上角
// ============================================================================
function initAvatar() {
    // 判断 Token 是否存在
    if (token.value != '') {
        axios({
            method: 'get',
            url: '/svr/api/user/get-user',
            headers: {
                Authorization: 'Bearer ' + token.value
            }
        }).then(function (response) {
            // console.log(response.data)
            if (response.data.code == '200') {
                let user = response.data.data;
                user_url.value = '/svr/api/image/display/head/' + user.avatar;
                nickname.value = user.nickname || user.uname || ''; // 昵称用于头像右边的文字，没有昵称时退回账号名
            }
        }).catch(function (error) {
            console.log(error);
            // 鉴权判断：注意后端未启动时 error.response 是 undefined，
            // 不先判空会在这里抛 TypeError，把整个导航栏带崩
            if (error.response && (error.response.status == 401 || error.response.status == 422)) {
                user_url.value = '/svr/api/image/display/head/tx.png'; // 没有权限或权限已过期，设置 token 为空
                token.value = '';
                userStore.setToken('');
            }
        });
    }
}
onMounted(() => {
    initNav(); // 初始化导航栏
    initAvatar(); // 初始化导航栏头像
});
</script>

<template>
  <!--导航栏标签开始-->
  <el-menu
    :default-active="activeIndex"
    :router="true"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false">
    <el-menu-item index="">
      <img style="width: 60px; height: 60px" :src="logo_url" alt="古典文学" />
    </el-menu-item>
    <el-menu-item index="/">首页</el-menu-item>
    <!-- 类型导航：点击进入对应分类的文学列表 -->
    <el-menu-item
      v-for="item in navDatas"
      :key="item.tid"
      :index="String('/clslist/' + item.tid)">
      {{ item.name }}
    </el-menu-item>
    <div class="flex-grow" />
    <!-- 右上角用户区：登录与未登录都统一用 Avatar（教材 5.2.5 图 5.11），
         未登录时显示默认人像占位，点开是「登录 / 注册」 -->
    <div class="user-entry">
      <!-- 未登录：人像占位头像 + 「未登录」 -->
      <el-dropdown
        v-if="token == ''"
        trigger="click"
        placement="bottom-end"
        popper-class="user-dropdown"
        @command="handleCommand">
        <span class="user-trigger">
          <el-avatar :size="34" class="user-avatar user-avatar--guest">
            <el-icon><UserFilled /></el-icon>
          </el-avatar>
          <span class="user-name user-name--guest">未登录</span>
          <el-icon class="user-caret"><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="login">
              <el-icon><Right /></el-icon><span>登录</span>
            </el-dropdown-item>
            <el-dropdown-item command="register">
              <el-icon><EditPen /></el-icon><span>注册</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 已登录：头像 + 昵称，点开是个人中心 / 评价记录 / 退出登录 -->
      <el-dropdown
        v-else
        trigger="click"
        placement="bottom-end"
        popper-class="user-dropdown"
        @command="handleCommand">
        <span class="user-trigger">
          <!-- 头像文件缺失时 el-avatar 会自动退回「昵称首字」色块 -->
          <el-avatar :size="34" :src="user_url" class="user-avatar">
            {{ nickname ? nickname.charAt(0) : '诗' }}
          </el-avatar>
          <span class="user-name">{{ nickname }}</span>
          <el-icon class="user-caret"><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="user">
              <el-icon><User /></el-icon><span>个人中心</span>
            </el-dropdown-item>
            <el-dropdown-item command="mydiscuss">
              <el-icon><Notebook /></el-icon><span>评价记录</span>
            </el-dropdown-item>
            <el-dropdown-item command="logout" divided>
              <el-icon><SwitchButton /></el-icon><span>退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-menu>
  <!--导航栏标签结束-->
</template>

<style>
.flex-grow {
  flex-grow: 1;
}
.el-menu-demo {
  border-bottom: 1px solid #e6e6e6;
}

/* 已登录头像在 sub-menu 的标题里，收起一点内边距，避免头像撑得太开 */
.el-menu-demo .el-sub-menu__title {
  padding-right: 12px;
}

/* ================= 右上角用户区（头像 + 昵称 + 下拉） ================= */
.user-entry {
  display: flex;
  align-items: center;
  padding-right: 8px;
}

.user-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 6px;
  border-radius: 22px;
  cursor: pointer;
  outline: none;
  transition: background-color 0.2s ease;
}

.user-trigger:hover {
  background-color: #f7efe1;
}

/* 头像文件缺失时 el-avatar 会显示昵称首字，这里给一个宣纸底色兜底。
   加 .el-menu-demo 提权，否则会被 Element Plus 默认的灰色 .el-avatar 底色盖掉 */
.el-menu-demo .user-avatar {
  background-color: #efe2ce;
  color: #7a6449;
  font-size: 14px;
  border: 1px solid #e6d8bf;
}

.user-name {
  max-width: 120px;
  overflow: hidden;
  font-size: 14px;
  color: #5a3a22;
  white-space: nowrap;
  text-overflow: ellipsis;
}

/* 未登录：文字用浅一档的褐色，和已登录状态区分开 */
.user-name--guest {
  color: #8c7a63;
}

/* 未登录的人像占位：比已登录头像再淡一点 */
.el-menu-demo .user-avatar--guest {
  color: #a2917a;
  background-color: #f6efe2;
  border-color: #ece0cb;
}

.el-menu-demo .user-avatar--guest .el-icon {
  font-size: 18px;
}

.user-caret {
  font-size: 12px;
  color: #9a7b53;
}

/* 下拉面板：白底卡片 + 圆角阴影，条目 44px 高、左图标右文字（对齐设计稿） */
.el-popper.user-dropdown {
  padding: 6px;
  border: 1px solid #efe3cc;
  border-radius: 10px;
  box-shadow: 0 10px 26px rgba(90, 58, 34, 0.14);
}

/* 设计稿里没有小尖角，去掉；留着会切断面板的上边框 */
.el-popper.user-dropdown .el-popper__arrow {
  display: none;
}

.user-dropdown .el-dropdown-menu {
  padding: 0;
}

.user-dropdown .el-dropdown-menu__item {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 148px;
  padding: 11px 14px;
  border-radius: 6px;
  font-size: 14px;
  color: #4a3b2a;
}

.user-dropdown .el-dropdown-menu__item .el-icon {
  font-size: 16px;
  color: #8c7a63;
}

.user-dropdown .el-dropdown-menu__item:not(.is-disabled):hover,
.user-dropdown .el-dropdown-menu__item:not(.is-disabled):focus {
  background-color: #f8f1e4;
  color: #a8352c;
}

.user-dropdown .el-dropdown-menu__item:not(.is-disabled):hover .el-icon {
  color: #a8352c;
}

.user-dropdown .el-dropdown-menu__item--divided {
  margin-top: 6px;
  border-top: 1px solid #f2e8d6;
}

/* 窄屏：7 个分类 + 注册/登录放不下，会把整页撑出横向滚动条。
   这里让菜单自己横向滚动（隐藏滚动条），页面宽度保持视口宽，
   轮播、推荐卡片才能跟着一起正常缩放。 */
@media (max-width: 760px) {
  .el-menu-demo {
    overflow-x: auto;
    overflow-y: hidden;
    flex-wrap: nowrap;
  }

  .el-menu-demo::-webkit-scrollbar {
    display: none;
  }

  /* 菜单项默认允许收缩，会被压扁成「汉魏…」，这里禁止收缩，改用滚动查看 */
  .el-menu-demo > .el-menu-item,
  .el-menu-demo > .el-sub-menu {
    flex: 0 0 auto;
  }
}
</style>
