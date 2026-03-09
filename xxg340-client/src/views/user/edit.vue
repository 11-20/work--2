<template>
  <div class="main-page">
    <div class="user-card">
      <div class="card-header">
        <h2>个人健康档案</h2>
        <p>您的心血管健康，我们共同守护</p>
      </div>

      <div class="avatar-section">
        <div class="avatar-wrapper">
          <UploadImg v-model:imageUrl="msgForm.avatar" />
        </div>
        <h3>{{ msgForm.user_name || '用户' }}</h3>
      </div>

      <el-form
        ref="userMsgFormRef"
        :model="msgForm"
        :rules="rules"
        label-position="top"
        class="user-form"
      >
        <el-form-item label="用户名" prop="user_name">
          <el-input v-model="msgForm.user_name" placeholder="请输入您的用户名" />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input v-model="msgForm.phone" placeholder="请输入您的手机号" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="msgForm.email" placeholder="请输入您的邮箱地址" />
        </el-form-item>

        <el-form-item label="性别" prop="sex">
          <el-radio-group v-model="msgForm.sex">
            <el-radio
              v-for="option in sexOptions"
              :key="option.value"
              :label="option.value"
              border
            >
              {{ option.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>

      <div class="form-divider">
        <span>修改密码</span>
      </div>

      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="rules"
        label-position="top"
        class="password-form"
      >
        <el-form-item label="新密码" prop="password">
          <el-input
            v-model="passwordForm.password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>

      <div class="action-buttons">
        <el-button type="primary" @click="doUpdateUser">保存个人信息</el-button>
        <el-button type="success" @click="sure">修改密码</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { ElMessage } from "element-plus";

const globalStore = GlobalStore();
const userMsgFormRef = ref(null);
const passwordFormRef = ref(null);

const userInfo = globalStore.userInfo;

// 密码修改表单
const passwordForm = reactive({
  password: '',
  confirmPassword: '',
  userId: userInfo.id,
  id: userInfo.id,
});

// 用户信息表单
const msgForm = reactive({
  user_name: userInfo.user_name,
  phone: userInfo.phone, 
  email: userInfo.email,
  avatar: userInfo.avatar,
  sex: userInfo.sex, // 性别字段：1-男，2-女
  id: globalStore.userInfo.id,
});

// 性别选项
const sexOptions = [
  { label: '男', value: 1 },
  { label: '女', value: 2 }
];

// 密码确认验证函数
const validatePassword = (rule, value, callback) => {
  if (value != passwordForm.password) {
    callback(new Error('两次输入密码不一致'));
  } else {
    callback();
  }
};

// 表单验证规则
const rules = {
  user_name: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  sex: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ]
};

// 修改密码
const sure = () => {
  passwordFormRef.value.validate((valid) => {
    if (valid) {
      request('/user/updatepassword?id=' + passwordForm.id, passwordForm, 'put').then(res => {
        ElMessage({ message: '密码修改成功', type: 'success' });
        // 重置密码表单
        passwordForm.password = '';
        passwordForm.confirmPassword = '';
      });
    }
  });
};

// 更新用户信息
const doUpdateUser = () => {
  userMsgFormRef.value.validate((valid) => {
    if (valid) {
      request("/user/update?id=" + msgForm.id, msgForm, "put").then((res) => {
        globalStore.setUserInfo({ ...globalStore.userInfo, ...msgForm });
        ElMessage({ message: "更新成功", type: "success" });
      });
    }
  });
};
</script>

<style scoped>
.main-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
  padding: 20px;
}

.user-card {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  padding: 32px;
  position: relative;
}

.user-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #e74c3c, #ff6b6b, #ff8e8e);
}

.card-header {
  text-align: center;
  margin-bottom: 24px;
}

.card-header h2 {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 8px;
  font-weight: 600;
}

.card-header p {
  color: #7f8c8d;
  font-size: 14px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 28px;
}

.avatar-wrapper {
  margin-bottom: 16px;
}

.avatar-wrapper :deep(.el-upload) {
  border: none;
}

.avatar-wrapper :deep(img) {
  border: 3px solid #e0f7fa;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar-section h3 {
  font-size: 20px;
  color: #2c3e50;
  font-weight: 500;
}

.user-form,
.password-form {
  margin-bottom: 24px;
}

.user-form .el-form-item,
.password-form .el-form-item {
  margin-bottom: 20px;
}

.user-form .el-form-item__label,
.password-form .el-form-item__label {
  font-weight: 500;
  color: #34495e;
  margin-bottom: 6px;
}

.user-form .el-input__wrapper,
.password-form .el-input__wrapper {
  border-radius: 8px;
  border: 1px solid #e0e6ed;
  background-color: #fafbfd;
}

.user-form .el-input__wrapper:focus-within,
.password-form .el-input__wrapper:focus-within {
  border-color: #4fc3f7;
  box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.2);
}

.el-radio.is-bordered {
  margin-right: 16px;
  border-radius: 8px;
  border: 1px solid #e0e6ed;
  padding: 8px 16px;
  transition: all 0.3s;
}

.el-radio.is-bordered:hover,
.el-radio.is-bordered.is-checked {
  border-color: #4fc3f7;
  background-color: #f0f9ff;
}

.form-divider {
  position: relative;
  margin: 28px 0 20px;
  text-align: center;
}

.form-divider span {
  background: white;
  position: relative;
  z-index: 1;
  padding: 0 12px;
  color: #7f8c8d;
  font-size: 14px;
}

.form-divider::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e0e6ed;
  z-index: 0;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.action-buttons .el-button {
  padding: 12px 32px;
  font-size: 16px;
  border-radius: 8px;
  font-weight: 500;
}

.action-buttons .el-button--primary {
  background: linear-gradient(135deg, #3498db, #2980b9);
  border: none;
}

.action-buttons .el-button--success {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  border: none;
}

@media (max-width: 600px) {
  .user-card {
    padding: 24px 20px;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>