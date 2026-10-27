<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

// 教材 5.2.5 第 3 个：用 Form 组件开发「注册页面」
const registerForm = reactive({
  uname: '',
  upwd: '',
  reupwd: '',
  sex: '男',
  phone: ''
})

const formRef = ref<FormInstance>()

// 自定义校验：两次密码必须一致
function checkRePwd(rule: unknown, value: string, callback: (e?: Error) => void) {
  if (value !== registerForm.upwd) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  uname: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 12, message: '用户名长度 3 到 12 个字符', trigger: 'blur' }
  ],
  upwd: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码不少于 6 位', trigger: 'blur' }
  ],
  reupwd: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: checkRePwd, trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ]
}

// 提交：校验通过才发请求
function submitForm(formEl: FormInstance | undefined) {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      ElMessage.success('校验通过，可以提交注册')
    } else {
      ElMessage.error('请先补全注册信息')
    }
  })
}

function resetForm(formEl: FormInstance | undefined) {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<template>
  <el-form
    ref="formRef"
    :model="registerForm"
    :rules="rules"
    label-width="80px"
    class="form-demo">
    <el-form-item label="用户名" prop="uname">
      <el-input v-model="registerForm.uname" placeholder="3 到 12 个字符" clearable />
    </el-form-item>
    <el-form-item label="密码" prop="upwd">
      <el-input v-model="registerForm.upwd" type="password" placeholder="不少于 6 位" show-password />
    </el-form-item>
    <el-form-item label="确认密码" prop="reupwd">
      <el-input v-model="registerForm.reupwd" type="password" placeholder="再次输入密码" show-password />
    </el-form-item>
    <el-form-item label="性别">
      <el-radio-group v-model="registerForm.sex">
        <el-radio value="男">男</el-radio>
        <el-radio value="女">女</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="手机号" prop="phone">
      <el-input v-model="registerForm.phone" placeholder="11 位手机号" maxlength="11" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(formRef)">注册</el-button>
      <el-button @click="resetForm(formRef)">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped>
.form-demo {
  max-width: 480px;
}
</style>
