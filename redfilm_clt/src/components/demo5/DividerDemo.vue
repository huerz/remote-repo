<template>
  <div class="divider-demo">
    <p class="label">账号信息</p>

    <!-- 教材 5.2.5 第 11 个：用 Divider 给「注册页面」分区
         content-position 控制文字位置：left / center / right -->
    <el-divider content-position="left">基本信息</el-divider>

    <el-form label-width="72px" class="mini-form">
      <el-form-item label="用户名">
        <el-input placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" placeholder="请输入密码" show-password />
      </el-form-item>
    </el-form>

    <el-divider>其他方式</el-divider>

    <div class="other-way">
      <el-button>手机号注册</el-button>
      <el-button>邮箱注册</el-button>
    </div>

    <!-- 虚线 / 点线：首页轮播下方用的就是 dashed，推荐区之间用 dotted -->
    <el-divider border-style="dashed" />
    <p class="tip">上面是虚线分割线（border-style="dashed"）</p>
    <el-divider border-style="dotted" />
    <p class="tip">上面是点线分割线（border-style="dotted"）</p>
  </div>
</template>

<style scoped>
.divider-demo {
  max-width: 520px;
}

.label {
  margin: 0;
  font-family: 'Songti SC', 'STSong', 'SimSun', serif;
  font-size: 15px;
  color: #5a3a22;
}

.mini-form {
  margin-top: 4px;
}

.other-way {
  display: flex;
  gap: 10px;
}

.tip {
  margin: 0;
  font-size: 12px;
  color: #9a7b53;
}
</style>
