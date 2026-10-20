<script setup lang="ts">
import { ref, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
// ElMessage：注册成功 / 失败的顶部轻提示
import { ElMessage } from 'element-plus'
// 表单相关类型：只在开发期做校验，编译后全部擦除
import type { FormInstance, FormItemRule } from 'element-plus'
import type { AxiosInstance } from 'axios'
// 引入顶部导航栏组件
import HeaderComp from '@/components/HeaderComp.vue'
// 引入底部导航栏组件
import FooterComp from '@/components/FooterComp.vue'

// 定义表单数据接口
interface DataForm {
  uname: string
  upwd: string
  nickname: string
  sex: string
  phone: string
}

// 定义表单规则接口
interface RuleForm {
  uname: FormItemRule[]
  upwd: FormItemRule[]
  nickname: FormItemRule[]
  phone: FormItemRule[]
}

// 注册接口返回结构（只有 code 和 msg，没有 data）
interface RegisterResult {
  code: string
  msg: string
}

const axios = inject('axios') as AxiosInstance // 注入 axios（main.ts 中 provide 的是 AxiosInstance）
const router = useRouter()    // 创建路由对象，用于编程式导航

// 顶部导航栏选中项索引（当前在“注册”）
const activeIndex = ref<string>('/register')

// 表单实例：调用 validate() 做校验、resetFields() 做重置
const ruleFormRef = ref<FormInstance>()

// 表单数据（注册数据），与表单双向绑定
const dataForm = reactive<DataForm>({
  uname: '',
  upwd: '',
  nickname: '',
  sex: '男',
  phone: ''
})

// 表单校验规则：required 必填，trigger 触发时机（blur = 失去焦点时校验）
const rules = reactive<RuleForm>({
  uname: [{ required: true, message: '请输入账号...', trigger: 'blur' }],
  upwd: [{ required: true, message: '请输入密码...', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称...', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入电话号码...', trigger: 'blur' }]
})

// “注册”按钮事件：先校验表单，校验通过再调用注册接口
function submitForm(formEl: FormInstance | undefined) {
  if (!formEl) return
  // 同登录页：validate(callback) 的 Promise 在校验失败时会 reject，不加 await 就不会抛未捕获错误
  formEl.validate((valid: boolean) => {
    if (valid) {
      register() // 校验通过，执行注册
    } else {
      console.log('error submit!')
    }
  })
}

// “重置”按钮事件：清空表单数据与校验状态
function resetForm(formEl: FormInstance | undefined) {
  if (!formEl) return
  formEl.resetFields()
}

// ============================================================================
// 【接口 5】用户注册 API
// 调用方式：POST 前端 /svr/api/user/register
//                 后端 http://127.0.0.1:5382/api/user/register
// 请求头：Content-Type: application/json
// 请求体：{
//   "uname":    "登录账号",
//   "upwd":     "登录密码",
//   "nickname": "昵称",
//   "sex":      "男" | "女",
//   "phone":    "电话号码"
// }
// 返回结构：{ code: '200', msg: '操作成功！' }  注册成功
//           { code: '400', msg: '操作失败！' }  账号已存在等写入失败
//           { code: '404', msg: '参数错误' }    请求体为空
// 说明：后端注册成功后的头像统一写死为 tx.png，无需前端传
// ============================================================================
function register() {
  axios<RegisterResult>({
    method: 'post',
    url: '/svr/api/user/register',
    headers: {
      'Content-Type': 'application/json'
    },
    data: dataForm
  }).then(function (response) {
    if (response.data.code == '200') {
      // 提示信息
      ElMessage.success('注册成功！')
      // 注册成功，跳转至登录页
      router.push('/login')
    } else {
      // 后端返回 400/404 时，直接提示后端给的 msg（如账号重复写入失败）
      ElMessage.error(response.data.msg || '注册失败！')
    }
  }).catch(function (error) {
    console.log(error)
    ElMessage.error('注册失败！')
  })
}
</script>

<template>
  <el-container class="register-container">
    <!--顶部导航栏-->
    <el-header height="60px">
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <!--主要区域容器-->
    <el-main>
      <el-divider content-position="center">用户注册</el-divider>
      <!--注册表单卡片：与登录页保持同一套视觉-->
      <div class="register-card">
        <el-form
          ref="ruleFormRef"
          :model="dataForm"
          :rules="rules"
          label-width="auto"
          status-icon
          class="register-form">
          <el-form-item label="账号：" prop="uname">
            <el-input v-model="dataForm.uname" placeholder="请输入登录账号" clearable />
          </el-form-item>
          <el-form-item label="密码：" prop="upwd">
            <el-input
              v-model="dataForm.upwd"
              type="password"
              placeholder="请输入登录密码"
              show-password />
          </el-form-item>
          <el-form-item label="昵称：" prop="nickname">
            <el-input v-model="dataForm.nickname" placeholder="请输入昵称" clearable />
          </el-form-item>
          <el-form-item label="电话号码：" prop="phone">
            <el-input v-model="dataForm.phone" placeholder="请输入电话号码" clearable />
          </el-form-item>
          <el-form-item label="性别" prop="sex">
            <el-radio-group v-model="dataForm.sex">
              <el-radio value="男">男</el-radio>
              <el-radio value="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item class="register-btns">
            <el-button type="primary" @click="submitForm(ruleFormRef)">注册</el-button>
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
.register-container {
  min-height: 100vh;
}

/* 表单卡片：宣纸质感，与登录页、首页风格一致 */
.register-card {
  /* 把 Element Plus 的主色改成站点的朱红，输入框聚焦、主按钮自动跟随 */
  --el-color-primary: #a8352c;
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

.register-form {
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
}

/* 按钮行居中，与教材“width: 65%; margin: 0 auto”效果一致
   （el-form-item 的内容区是 flex，居中要作用在 __content 上） */
.register-btns {
  margin-top: 26px;
  margin-bottom: 4px;
}

.register-btns :deep(.el-form-item__content) {
  justify-content: center;
}

.register-btns :deep(.el-button) {
  min-width: 96px;
  letter-spacing: 2px;
}
</style>
