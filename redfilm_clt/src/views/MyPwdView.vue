<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { inject } from 'vue'
import type { AxiosInstance } from 'axios'
import { ElMessage } from 'element-plus'
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
const asideIndex = ref('/mypwd')
// 创建路由对象
const router = useRouter()
// 创建 Token 状态管理 Store
const userStore = useTokenStore()
// 获取登录用户的 Token
const token = ref(userStore.getToken())

// 以下为表单数据校验代码
interface DataForm {
  oldpwd: string
  newpwd: string
}
const ruleFormRef = ref<FormInstance>()
// 表单数据（密码数据）
const dataForm = reactive<DataForm>({
  oldpwd: '',
  newpwd: ''
})
// 表单校验规则
const rules = reactive<FormRules<DataForm>>({
  oldpwd: [{ required: true, message: '请输入旧密码...', trigger: 'blur' }],
  newpwd: [{ required: true, message: '请输入新密码...', trigger: 'blur' }]
})

// 密码重置函数
function editPwd() {
  axios({
    method: 'post',
    url: '/svr/api/user/update-pwd',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + token.value
    },
    data: dataForm
  })
  .then(function (response) {
    if (response.data.code == '200') {
      // 提示信息
      ElMessage({
        message: response.data.msg,
        type: 'success',
        plain: true
      })
      // 设置当前登录用户的 Token 为空
      userStore.setToken('')
      // 修改成功后，跳转至登录页
      router.push('/login')
    } else {
      // 提示信息
      ElMessage({
        message: response.data.msg,
        type: 'success',
        plain: true
      })
    }
  })
  .catch(function (error) {
    // 鉴权判断
    if (error.response.status == 401 || error.response.status == 422) {
      // 设置当前登录用户的 Token 为空
      token.value = ''
      userStore.setToken('')
      // 提示信息
      ElMessage({
        message: '请重新登录！',
        type: 'success',
        plain: true
      })
    }
  })
}

// "修改"按钮事件
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!')
      // 密码重置函数
      editPwd()
    } else {
      console.log('error submit!', fields)
    }
  })
}
// "取消"按钮事件
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
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
                <el-icon><Edit /></el-icon>
              </template>
              <template #title>我的密码</template>
              <div style="display: flex; justify-content: center; margin-top: 10px">
                <el-form
                  ref="ruleFormRef"
                  style="max-width: 600px"
                  :model="dataForm"
                  :rules="rules"
                  label-width="auto"
                  status-icon>
                  <el-form-item label="旧 密 码：" prop="oldpwd">
                    <el-input v-model="dataForm.oldpwd" type="password" show-password/>
                  </el-form-item>
                  <el-form-item label="新 密 码：" prop="newpwd">
                    <el-input v-model="dataForm.newpwd" type="password" show-password/>
                  </el-form-item>
                  <el-form-item>
                    <el-button
                      style="margin-left: 86px"
                      type="primary"
                      @click="submitForm(ruleFormRef)">
                      修改
                    </el-button>
                    <el-button @click="resetForm(ruleFormRef)">取消</el-button>
                  </el-form-item>
                </el-form>
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
