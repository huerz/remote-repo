<script setup lang="ts">
import { ref, inject, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { AxiosInstance } from 'axios'
// 引入 Token 状态管理
import { useTokenStore } from '@/stores/token'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'

const axios = inject('axios') as AxiosInstance // 注入 axios（main.js 中 provide 的是 AxiosInstance）

// 顶部导航栏菜单选中项索引（当前在“登录”）
const activeIndex = ref<string>('/login')
// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 创建路由对象，用于编程式导航
const router = useRouter()

// 以下为表单数据校验代码
interface DataForm {
  uname: string
  upwd: string
}

// 登录接口返回结构（成功时带 token）
interface LoginResult {
  code: string
  msg: string
  token?: string
}

// 表单实例：调用 validate() 做校验、resetFields() 做重置
const ruleFormRef = ref<FormInstance>()

// 表单数据（登录数据）
const dataForm = reactive<DataForm>({
  uname: '',
  upwd: ''
})

// 表单校验规则
const rules = reactive<FormRules<DataForm>>({
  uname: [{ required: true, message: '请输入账号...', trigger: 'blur' }],
  upwd: [{ required: true, message: '请输入密码...', trigger: 'blur' }]
})

// “登录”按钮事件
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  // 注意：validate(callback) 同时返回 Promise，校验不通过时这个 Promise 会 reject；
  // 这里不加 await，避免冒出一个没人处理的 Promise 错误（控制台会飘红）
  formEl.validate((valid: boolean, fields) => {
    if (valid) {
      login() // 用户登录操作
    } else {
      console.log('error submit!', fields)
    }
  })
}

// “重置”按钮事件
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

// ============================================================================
// 【接口 6】用户登录 API
// 调用方式：POST 前端 /svr/api/user/login
//                 后端 http://127.0.0.1:5383/api/user/login
// 请求头：Content-Type: application/json
// 请求体：{ "uname": "登录账号", "upwd": "登录密码" }
// 返回结构：{ code: '200', msg: '操作成功！', token: 'JWT 字符串' }  登录成功
//           { code: '400', msg: '账号或密码错误！' }               登录失败
//           { code: '404', msg: '参数错误' }                       请求体为空
// 说明：登录成功后把 token 存入 Pinia（同时写入 localStorage），供后续接口鉴权使用
// ============================================================================
// 用户登录函数
function login() {
  axios<LoginResult>({
    method: 'post',
    url: '/svr/api/user/login',
    headers: {
      'Content-Type': 'application/json'
    },
    data: dataForm
  }).then(function (response) {
    console.log(response.data)
    if (response.data.code == '200') {
      // 提示信息
      ElMessage.success('登录成功！')
      // 获取登录用户的 Token
      const token = response.data.token ?? ''
      userStore.setToken(token)
      // 登录成功，跳转至首页
      router.push('/')
    } else {
      // 后端返回 400/404 时，直接提示后端给的 msg
      ElMessage.error(response.data.msg || '登录失败！')
    }
  }).catch(function (error) {
    console.log(error)
    ElMessage.error('登录失败！')
  })
}
</script>

<template>
  <el-container class="login-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <el-divider content-position="center">用户登录</el-divider>
      <!--登录表单卡片：与注册页保持同一套视觉-->
      <div class="login-card">
        <el-form
          ref="ruleFormRef"
          :model="dataForm"
          :rules="rules"
          label-width="auto"
          status-icon
          class="login-form">
          <el-form-item label="账号：" prop="uname">
            <el-input v-model="dataForm.uname" placeholder="请输入登录账号" clearable>
              <template #suffix>
                <el-icon class="el-input__icon"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="密码：" prop="upwd">
            <el-input
              v-model="dataForm.upwd"
              type="password"
              placeholder="请输入登录密码"
              show-password
              @keyup.enter="submitForm(ruleFormRef)" />
          </el-form-item>
          <el-form-item class="login-btns">
            <el-button type="primary" @click="submitForm(ruleFormRef)">登录</el-button>
            <el-button @click="resetForm(ruleFormRef)">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-main>
    <!--底部导航栏-->
    <el-footer height="60px"><FooterComp /></el-footer>
  </el-container>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
}

/* 登录卡片：宣纸质感，与注册页、首页保持同一套视觉 */
.login-card {
  max-width: 460px;
  margin: 12px auto 40px;
  padding: 30px 34px 22px;
  border: 1px solid #e6d8bf;
  border-radius: 6px;
  background:
    radial-gradient(circle at 18% 12%, rgba(168, 53, 44, 0.04), transparent 55%),
    linear-gradient(180deg, #fdfaf4 0%, #faf5ec 100%);
  box-shadow: 0 6px 20px rgba(90, 58, 34, 0.08);
}

.login-form {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
}

/* 按钮行居中（el-form-item 的内容区是 flex，居中要作用在 __content 上） */
.login-btns {
  margin-top: 26px;
  margin-bottom: 4px;
}

.login-btns :deep(.el-form-item__content) {
  justify-content: center;
}

.login-btns :deep(.el-button) {
  min-width: 96px;
  letter-spacing: 2px;
}
</style>
