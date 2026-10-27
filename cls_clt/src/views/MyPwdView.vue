<script setup>
// ============================================================================
// 修改密码（/mypwd）
// ----------------------------------------------------------------------------
// 作用：校验旧密码后设置新密码。
// 教材：第八章新增功能 §8.3.5 开发密码重置功能（p256）
//       第六章的用户中心没有改密入口，本页是第八章新加的独立页面
// 约定：新旧密码不能相同；成功后需要重新登录。
// ============================================================================
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { inject } from 'vue';
import { ElMessage } from 'element-plus';
import HeaderComp from '../components/HeaderComp.vue'; // 引入顶部导航栏组件
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
import AsideComp from '@/components/AsideComp.vue'; // 引入侧边栏导航组件
import { useTokenStore } from '@/stores/token'; // 引入状态管理文件
const axios = inject('axios'); // 注入 axios
const activeIndex = ref('/user'); // 顶部导航栏菜单选中项索引
const asideIndex = ref('/mypwd'); // 侧边栏菜单选中项索引
const router = useRouter(); // 创建路由对象
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
const token = ref(userStore.getToken()); // 获取登录用户的 Token
const ruleFormRef = ref();
// 表单数据（密码数据）
const dataForm = reactive({
    oldpwd: '',
    newpwd: ''
});
// 表单校验规则
const rules = reactive({
    oldpwd: [{ required: true, message: '请输入旧密码...', trigger: 'blur' }],
    newpwd: [{ required: true, message: '请输入新密码...', trigger: 'blur' }]
});
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
            });
            userStore.setToken(''); // 设置当前登录用户的 Token 为空
            router.push('/login'); // 修改成功后，跳转至登录页
        }
        else {
            // 提示信息
            ElMessage({
                message: response.data.msg,
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
const submitForm = async (formEl) => {
    if (!formEl)
        return;
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('submit!');
            editPwd(); // 密码重置函数
        }
        else {
            console.log('error submit!', fields);
        }
    });
};
const resetForm = (formEl) => {
    if (!formEl)
        return;
    formEl.resetFields();
};
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

<style scoped>
/* 页头图标（el-page-header 的 icon 插槽）：统一尺寸与站点色，
   默认会继承成黑色，在这套宣纸背景里显得突兀 */
.el-page-header__icon .el-icon {
  font-size: 18px;
  color: #a8352c;
}
</style>
