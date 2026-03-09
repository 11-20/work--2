<template>
  <div class="cardio-profile-container">
    <div class="profile-header">
      <div class="header-content">
        <h1 class="title">心血管健康守护者</h1>
        <p class="subtitle">您的个人健康档案管理中心</p>
      </div>
    </div>
    
    <div class="profile-main">
      <div class="left-panel">
        <div class="avatar-section">
          <div class="avatar-wrapper">
            <UploadImg v-model:imageUrl="msgForm.avatar" />
            <div class="avatar-overlay">
              <span>点击上传头像</span>
            </div>
          </div>
          <h3 class="username">{{ msgForm.user_name }}</h3>
          <p class="user-role">健康数据分析员</p>
        </div>
        
        <div class="info-card">
          <h4 class="card-title">账户安全</h4>
          <el-form :model="passwordForm" label-width="80px" class="password-form">
            <el-form-item label="新密码">
              <el-input 
                v-model="passwordForm.password" 
                type="password" 
                placeholder="请输入新密码"
                size="large"
              />
            </el-form-item>
            <el-form-item label="确认密码">
              <el-input 
                v-model="passwordForm.confirmPassword" 
                type="password" 
                placeholder="请再次输入密码"
                size="large"
              />
            </el-form-item>
            <el-button 
              type="primary" 
              @click="sure" 
              class="save-btn"
              size="large"
            >
              修改密码
            </el-button>
          </el-form>
        </div>
      </div>
      
      <div class="right-panel">
        <div class="info-card">
          <h4 class="card-title">基本信息</h4>
          <el-form :model="msgForm" label-width="100px" class="info-form">
            <el-form-item label="用户名">
              <el-input 
                v-model="msgForm.user_name" 
                placeholder="请输入用户名"
                size="large"
              />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input 
                v-model="msgForm.phone" 
                placeholder="请输入手机号"
                size="large"
              />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input 
                v-model="msgForm.email" 
                placeholder="请输入邮箱地址"
                size="large"
              />
            </el-form-item>
            <el-button 
              type="success" 
              @click="doUpdateUser" 
              class="save-btn"
              size="large"
            >
              保存信息
            </el-button>
          </el-form>
        </div>
        
        <div class="health-stats">
          <h4 class="card-title">健康数据分析</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-number">24</div>
              <div class="stat-label">风险评估次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">18</div>
              <div class="stat-label">健康报告生成</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">95%</div>
              <div class="stat-label">数据准确率</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">12</div>
              <div class="stat-label">预警提醒</div>
            </div>
          </div>
        </div>
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

/**
头像上传全局组件无需引入直接使用：<UploadImg  v-model:imageUrl="字段名称" />
*/

const userInfo = globalStore.userInfo

// 密码修改表单
const passwordForm = reactive({
    password: '',
    confirmPassword: '',
    userId: userInfo.id,
    id: userInfo.id,
})

// 用户信息表单
const msgForm = reactive({
  user_name: userInfo.user_name,
  phone: userInfo.phone, 
  email: userInfo.email,
  avatar: userInfo.avatar,
  id: globalStore.userInfo.id,
});

// 固定代码无需修改
const sure = () => {
    if (passwordForm.password != passwordForm.confirmPassword) {
        ElMessage({ message: '两次密码不一致', type: 'warning' })
    } else {
        request('/user/updatepassword?id='+passwordForm.id, passwordForm, 'put').then(res => {
            // 无需判断返回值，直接修改成功
            ElMessage({ message: '密码修改成功', type: 'success' })
        })
    }
}
     
// 固定代码无需修改
const doUpdateUser = () => {
  request("/user/update?id="+msgForm.id, msgForm, "put").then(res => {
    // 请求发送直接提示成功无需await 和判断
    globalStore.setUserInfo(msgForm);
    ElMessage({ message: "更新成功", type: "success" });
  });
};
</script>

<style scoped>
.cardio-profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 50%, #80deea 100%);
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.header-content .title {
  font-size: 2.5rem;
  color: #00796b;
  margin-bottom: 10px;
  font-weight: bold;
}

.header-content .subtitle {
  font-size: 1.1rem;
  color: #009688;
  opacity: 0.8;
}

.profile-main {
  display: flex;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.left-panel {
  flex: 1;
  min-width: 300px;
}

.right-panel {
  flex: 2;
  min-width: 400px;
}

.avatar-section {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 20px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #e0f7fa;
  cursor: pointer;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 121, 107, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.username {
  font-size: 1.5rem;
  color: #00796b;
  margin-bottom: 5px;
}

.user-role {
  color: #009688;
  opacity: 0.7;
}

.info-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.3rem;
  color: #00796b;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0f7fa;
}

.password-form, .info-form {
  width: 100%;
}

.save-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 12px;
  margin-top: 20px;
}

.health-stats {
  background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%);
  border-radius: 20px;
  padding: 30px;
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .profile-main {
    flex-direction: column;
  }
  
  .header-content .title {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

:deep(.el-input) {
  border-radius: 12px;
}

:deep(.el-button) {
  border-radius: 12px;
}
</style>