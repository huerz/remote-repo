<script setup>
// ============================================================================
// 个人中心（/user）
// ----------------------------------------------------------------------------
// 作用：个人信息展示与修改、头像上传。
// 教材：第六章 §6.3.1 用户中心与头像展示（本页骨架来自这一章的既有功能）
//       第八章只在本页新增两处：§8.3.2 头像上传（p239）、§8.3.3 信息修改（p244）
//       参考：§8.3.1 个人信息展示（p230）/ §8.2.1 Flask 文件上传（p224）/ §8.2.3 Upload 组件（p229）
// 约定：头像上传走 /api/image 上传接口，成功后回写用户表。
// ============================================================================
import { ref, inject, reactive, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { ElMessage } from 'element-plus';
import HeaderComp from '../components/HeaderComp.vue'; // 引入顶部导航栏组件
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
import AsideComp from '@/components/AsideComp.vue'; // 引入侧边栏导航组件
import { useTokenStore } from '@/stores/token'; // 引入状态管理文件
const axios = inject('axios'); // 注入 axios
const router = useRouter(); // 创建路由对象，用于编程式导航
const userStore = useTokenStore(); // 创建 Token 状态管理 Store
const token = ref(userStore.getToken()); // 获取登录用户的 Token
const activeIndex = ref('/user'); // 顶部导航栏菜单选中项索引
const asideIndex = ref('/user'); // 侧边栏菜单选中项索引
// 用户数据
// 教材写法：var user = ref({})；strict 下用 any，模板取属性才不报错
var user = ref({});
const avatarUrl = ref('/svr/api/image/display/head/tx.png'); // 头像 URL
const ruleFormRef = ref();
// 表单数据（用户数据）
const dataForm = reactive({
    nickname: '',
    sex: '男',
    phone: '',
    avatar: 'tx.png'
});
// 表单校验规则
const rules = reactive({
    nickname: [{ required: true, message: '请输入昵称...', trigger: 'blur' }],
    phone: { required: true, message: '请输入电话号码...', trigger: 'blur' }
});
function editUser() {
    axios({
        method: 'post',
        url: '/svr/api/user/update-user',
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
                message: '修改成功！',
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
            editUser(); // 修改个人信息
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
function initUser() {
    // 判断 token 是否存在
    if (token.value != '') {
        axios({
            method: 'get',
            url: '/svr/api/user/get-user',
            headers: {
                Authorization: 'Bearer ' + token.value
            }
        })
            .then(function (response) {
            // console.log(response.data)
            if (response.data.code == '200') {
                user.value = response.data.data;
                dataForm.nickname = user.value.nickname; // 初始化表单数据
                dataForm.phone = user.value.phone;
                dataForm.sex = user.value.sex;
                avatarUrl.value = '/svr/api/image/display/head/' + user.value.avatar;
            }
        })
            .catch(function (error) {
            console.log(error);
            // 鉴权判断
            if (error.response.status == 401 || error.response.status == 422) {
                token.value = ''; // 没有权限或权限已过期，设置 Token 为空
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
}
const handleAvatarSuccess = (response, uploadFile) => {
    avatarUrl.value = URL.createObjectURL(uploadFile.raw); // 设置新头像 URL
    dataForm.avatar = response.upFile; // 更新用户数据的头像文件名
};
const beforeAvatarUpload = (rawFile) => {
    const fileSuffix = rawFile.name.substring(rawFile.name.lastIndexOf('.') + 1).toLowerCase(); // 获取上传头像的扩展名
    const whiteList = ['png', 'gif', 'jpg', 'webp', 'jpeg']; // 允许上传的头像扩展名的集合
    // 判断头像是否允许上传
    if (whiteList.indexOf(fileSuffix) === -1) {
        ElMessage.error('头像只能是 PNG、GIF、JPG、WEBP、JPEG 格式');
        return false;
    }
    // 判断头像大小是否符合要求
    if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('头像大小不能超过 2MB！');
        return false;
    }
    return true;
};
onMounted(() => {
    initUser(); // 初始化用户数据
});
</script>

<template>
  <el-container>
    <el-header>
      <HeaderComp :active-index="activeIndex" />
    </el-header>
    <el-container>
      <el-aside width="200px">
        <!--侧边栏导航组件-->
        <AsideComp :aside-index="asideIndex" />
      </el-aside>
      <el-container>
        <el-main>
          <div>
            <!-- 用户信息开始 -->
            <el-page-header>
              <template #icon>
                <el-icon><User /></el-icon>
              </template>
              <template #title>用户信息</template>
              <div style="display: flex; justify-content: center; margin-top: 10px">
                <el-form
                  ref="ruleFormRef"
                  style="max-width: 600px"
                  :model="dataForm"
                  :rules="rules"
                  label-width="auto"
                  status-icon>
                  <el-form-item label="头像">
                    <!-- 用户头像上传功能开始 -->
                    <el-upload
                      class="avatar-uploader"
                      name="file"
                      action="/svr/api/user/upload"
                      :show-file-list="false"
                      :on-success="handleAvatarSuccess"
                      :before-upload="beforeAvatarUpload">
                      <img
                        v-if="avatarUrl"
                        :src="avatarUrl"
                        style="width: 100px; height: 100px"
                        class="avatar"
                      />
                      <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                    </el-upload>
                    <!-- 用户头像上传功能结束 -->
                  </el-form-item>
                  <el-form-item label="昵称" prop="nickname">
                    <el-input v-model="dataForm.nickname" />
                  </el-form-item>
                  <el-form-item label="电话号码" prop="phone">
                    <el-input v-model="dataForm.phone" />
                  </el-form-item>
                  <el-form-item label="性别" prop="sex">
                    <el-radio-group v-model="dataForm.sex">
                      <el-radio value="男">男</el-radio>
                      <el-radio value="女">女</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRef)">
                      修改
                    </el-button>
                    <el-button @click="resetForm(ruleFormRef)">取消</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-page-header>
            <!-- 用户信息结束 -->
          </div>
        </el-main>
        <el-footer>
          <el-footer><FooterComp /></el-footer>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}
.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}
/* 未上传头像时的占位：改用站内色板（淡褐），hover 提示「点这里换头像」时变朱红 */
.el-icon.avatar-uploader-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  font-size: 26px;
  color: var(--app-icon-muted);
  transition: color 0.2s ease;
}
.avatar-uploader .el-upload:hover .avatar-uploader-icon {
  color: var(--app-icon-brand);
}
</style>
