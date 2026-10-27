<script setup>
// ============================================================================
// 注册页（/register）
// ----------------------------------------------------------------------------
// 作用：校验两次密码一致与必填项后调用注册接口。
// 约定：前端校验只为体验，真正的唯一性校验在后端。
// ============================================================================
import { ref, reactive, inject } from 'vue';
import { useRouter } from 'vue-router';
// ElMessage：注册成功 / 失败的顶部轻提示
import { ElMessage } from 'element-plus';
import HeaderComp from '@/components/HeaderComp.vue'; // 引入顶部导航栏组件
import FooterComp from '@/components/FooterComp.vue'; // 引入底部导航栏组件
const axios = inject('axios'); // 注入 axios（main.ts 中 provide 的是 AxiosInstance）
const router = useRouter(); // 创建路由对象，用于编程式导航
const activeIndex = ref('/register'); // 顶部导航栏选中项索引（当前在“注册”）
const ruleFormRef = ref(); // 表单实例：调用 validate() 做校验、resetFields() 做重置
// 表单数据（注册数据），与表单双向绑定
const dataForm = reactive({
    uname: '',
    upwd: '',
    nickname: '',
    sex: '男',
    customSex: '',
    phone: ''
});
const sexOptions = ref(['男', '女', '保密', '自定义']); // 性别候选项：预设值只能选不能改；想用自己的说法就选「自定义」再输入
const SEX_MAX = 10; // 自定义性别的输入框长度上限（数据库字段 varchar(50)，留了余量）
function onSexChange(value) {
    if (value !== '自定义') {
        dataForm.customSex = '';
    }
}
// 表单校验规则：required 必填，trigger 触发时机（blur = 失去焦点时校验）
const rules = reactive({
    uname: [{ required: true, message: '请输入账号...', trigger: 'blur' }],
    upwd: [{ required: true, message: '请输入密码...', trigger: 'blur' }],
    nickname: [{ required: true, message: '请输入昵称...', trigger: 'blur' }],
    // 性别：选预设值直接通过；选「自定义」时必须有 1~10 个字的自定义文本。
    sex: [
        {
            validator: (_rule, value, callback) => {
                if (value === '自定义') {
                    const text = dataForm.customSex.trim();
                    if (!text) {
                        callback(new Error('请输入自定义性别'));
                    }
                    else if (text.length > SEX_MAX) {
                        callback(new Error(`自定义性别最多 ${SEX_MAX} 个字`));
                    }
                    else {
                        callback();
                    }
                }
                else if (!value) {
                    callback(new Error('请选择性别'));
                }
                else {
                    callback();
                }
            },
            trigger: ['change', 'blur']
        }
    ],
    phone: [{ required: true, message: '请输入电话号码...', trigger: 'blur' }]
});
function submitForm(formEl) {
    if (!formEl)
        return;
    // 同登录页：validate(callback) 的 Promise 在校验失败时会 reject，不加 await 就不会抛未捕获错误
    formEl.validate((valid) => {
        if (valid) {
            register(); // 校验通过，执行注册
        }
        else {
            console.log('error submit!');
        }
    });
}
function resetForm(formEl) {
    if (!formEl)
        return;
    formEl.resetFields();
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
//   "sex":      "男" | "女" | "保密" | 自定义文本（选「自定义」时取输入框的值），最多 10 字
//   "phone":    "电话号码"
// }
// 返回结构：{ code: '200', msg: '操作成功！' }  注册成功
//           { code: '400', msg: '操作失败！' }  账号已存在等写入失败
//           { code: '404', msg: '参数错误' }    请求体为空
// 说明：后端注册成功后的头像统一写死为 tx.png，无需前端传
// ============================================================================
function register() {
    // 「自定义」只是界面上的占位选项，真正提交的是输入框里的文本；
    // 后端对 sex 没有白名单限制（varchar(50)），这里统一好值再发出去
    const payload = {
        ...dataForm,
        sex: dataForm.sex === '自定义' ? dataForm.customSex.trim() : dataForm.sex
    };
    axios({
        method: 'post',
        url: '/svr/api/user/register',
        headers: {
            'Content-Type': 'application/json'
        },
        data: payload
    }).then(function (response) {
        if (response.data.code == '200') {
            ElMessage.success('注册成功！'); // 提示信息
            router.push('/login'); // 注册成功，跳转至登录页
        }
        else {
            ElMessage.error(response.data.msg || '注册失败！'); // 后端返回 400/404 时，直接提示后端给的 msg（如账号重复写入失败）
        }
    }).catch(function (error) {
        console.log(error);
        ElMessage.error('注册失败！');
    });
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
          <el-form-item label="性别：" prop="sex">
            <div class="sex-row">
              <!-- 预设值（男/女/保密）只能选、不能清空也不能输入；
                   选「自定义」时右边才出现输入框 -->
              <el-select
                v-model="dataForm.sex"
                placeholder="请选择性别"
                popper-class="sex-select"
                style="width: 150px"
                @change="onSexChange">
                <el-option
                  v-for="item in sexOptions"
                  :key="item"
                  :label="item"
                  :value="item" />
              </el-select>
              <el-input
                v-if="dataForm.sex === '自定义'"
                v-model="dataForm.customSex"
                class="sex-custom"
                :maxlength="SEX_MAX"
                placeholder="请输入自定义性别"
                clearable />
            </div>
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
/* 性别行：下拉 + （仅自定义时的）输入框横排。
   下拉必须 flex:none——弹性布局默认允许收缩，
   输入框一出现就会把下拉挤窄，「自定义」三个字就被截成「自…」 */
.sex-row {
  display: flex;
  gap: 8px;
  width: 100%;
}

.sex-row .el-select {
  flex: none;
}

.sex-custom {
  flex: 1 1 auto;
  min-width: 0;
}

</style>

<style>
/* 性别下拉的浮层是 teleport 到 body 的，scoped 样式够不到，单独写一段全局样式，
   跟站内其他下拉（导航栏用户菜单）保持同一套宣纸配色 */
.el-popper.sex-select {
  padding: 6px;
  border: 1px solid #efe3cc;
  border-radius: 8px;
  box-shadow: 0 10px 26px rgba(90, 58, 34, 0.14);
}

.sex-select .el-popper__arrow {
  display: none;
}

.sex-select .el-select-dropdown__item {
  border-radius: 6px;
  font-size: 14px;
  color: #4a3b2a;
}

.sex-select .el-select-dropdown__item.is-hovering {
  background-color: #f8f1e4;
}

.sex-select .el-select-dropdown__item.is-selected {
  color: #a8352c;
  font-weight: 600;
}

/* allow-create 生成的那一条，右侧给个提示，避免和已有选项混淆 */
.sex-select .el-select-dropdown__item.is-created {
  color: #8c7a63;
}
</style>
