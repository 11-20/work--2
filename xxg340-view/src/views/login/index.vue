<template>
  <div class="login-container">
    <!-- 背景装饰元素 -->
    <div class="background-decorations">
      <div class="heart-beat"></div>
      <div class="medical-icon-1"></div>
      <div class="medical-icon-2"></div>
      <div class="pulse-wave"></div>
    </div>

    <!-- 主登录卡片 -->
    <div class="login-card">
      <!-- 左侧健康主题区域 -->
      <div class="left-section">
        <div class="health-stats">
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">准确率</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">案例分析</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">实时监控</div>
          </div>
        </div>
        
        <div class="health-text">
          <h3>心血管疾病风险可视化分析平台</h3>
          <p>智能预警 • 精准分析 • 科学管理</p>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="right-section">
        <div class="login-header">
          <h2>基于Django的心血管疾病风险可视化分析平台的设计与实现</h2>
          <p>管理员登录</p>
        </div>

        <el-form :model="loginForm" @submit.prevent="login" class="login-form">
          <el-form-item>
            <el-input 
              v-model="loginForm.phone" 
              placeholder="请输入手机号码"
              prefix-icon="el-icon-phone"
              size="large"
              clearable
            />
          </el-form-item>

          <el-form-item>
            <el-input 
              v-model="loginForm.password" 
              type="password"
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
              size="large"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item>
            <el-button 
              type="primary" 
              @click="login" 
              class="login-btn"
              size="large"
              :loading="loading"
            >
              登录系统
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <div class="security-info">
            <i class="el-icon-lock"></i>
            <span>安全加密传输</span>
          </div>
          <div class="support-info">
            <i class="el-icon-headset"></i>
            <span>技术支持</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部装饰 -->
    <div class="bottom-decoration">
      <div class="data-flow"></div>
      <div class="analysis-node"></div>
    </div>
  </div>
</template>

<script setup name="login">
// 固定代码开发人员不要删除
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { GlobalStore } from "@/stores";
import { AuthStore } from "@/stores/modules/auth.js";
import { getHomeUrl } from "@/utils/util.js"; // 获取登录后跳转的第一个菜单
import { request } from '@/http/index';
import { ElMessage, ElMessageBox } from 'element-plus'
import { initDynamicRouter } from "@/routers/modules/dynamicRouter";

const router = useRouter();
const globalStore = GlobalStore();
const authStore = AuthStore();
/**
全局组件可直接使用无需引入：
富文本编辑：<WangEditor height="400px" v-model:value="字段名称" />
单图（头像）上传：<UploadImg  v-model:imageUrl="字段名称" />
多图上传：<UploadManyImg  v-model:imageUrl="字段名称" />
文件上传： <UploadFile  v-model:fileUrl="字段名称" />
*/

const loginForm = reactive({ phone: "", password: "" });
const loading = ref(false);

const login = async () => {
  if (!loginForm.phone || !loginForm.password) {
    ElMessage.error('请输入手机号和密码');
    return;
  }

  loading.value = true;
  try {
    const data = await request('/signin', loginForm, 'post');
    globalStore.setToken(data.authToken);
    if (data.authToken) {
      // 获取用户信息
       /**
      用户信息返回部分字段
      {
        user_name:'',
        role_id:''
      }
      */
     const userInfo =  await globalStore.getWebSiteMsg()
 
     await initDynamicRouter();
     // 获取当前用户菜单，登录后跳转第一个菜单页面
      const userMenus = await authStore.authMenuList
      const HOME_URL = getHomeUrl(userMenus)

    router.push(HOME_URL);
    ElMessage.success('登录成功');
    } else {
      ElMessage.error('登录失败');
    }
  } catch (error) {
    ElMessage.error('登录失败：' + error.message);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  // 初始化时的一些操作
});
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 25%, #3a7bd5 50%, #00d2ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.background-decorations {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.heart-beat {
  position: absolute;
  top: 20%;
  right: 15%;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: heartBeat 2s infinite;
}

.medical-icon-1 {
  position: absolute;
  top: 30%;
  left: 15%;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  content: '❤️';
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.medical-icon-2 {
  position: absolute;
  bottom: 25%;
  right: 20%;
  width: 70px;
  height: 70px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.pulse-wave {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  animation: pulseWave 3s infinite;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  14% { transform: scale(1.1); }
  28% { transform: scale(1); }
  42% { transform: scale(1.1); }
  70% { transform: scale(1); }
}

@keyframes pulseWave {
  0% { 
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% { 
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}

.login-card {
  display: flex;
  width: 900px;
  height: 550px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.left-section {
  flex: 1;
  background: linear-gradient(135deg, rgba(30, 60, 114, 0.9) 0%, rgba(42, 82, 152, 0.9) 100%);
  padding: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.health-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #40c4ff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.health-text h3 {
  font-size: 24px;
  margin-bottom: 15px;
  line-height: 1.4;
}

.health-text p {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 20px;
}

.right-section {
  flex: 1;
  padding: 50px 40px;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h2 {
  color: #1e3c72;
  font-size: 20px;
  margin-bottom: 10px;
  line-height: 1.4;
}

.login-header p {
  color: #666;
  font-size: 16px;
}

.login-form {
  width: 100%;
}

.login-form .el-form-item {
  margin-bottom: 25px;
}

.login-form .el-input {
  height: 50px;
}

.login-form .el-input__inner {
  border-radius: 10px;
  border: 2px solid #e1e5eb;
}

.login-btn {
  width: 100%;
  height: 50px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  border: none;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(30, 60, 114, 0.4);
}

.login-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.security-info, .support-info {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 14px;
}

.security-info i, .support-info i {
  margin-right: 8px;
  color: #1e3c72;
}

.bottom-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background: linear-gradient(to top, rgba(30, 60, 114, 0.3), transparent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-flow {
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  position: relative;
}

.data-flow::after {
  content: '';
  position: absolute;
  top: -4px;
  left: 0;
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  animation: dataFlow 3s infinite linear;
}

@keyframes dataFlow {
  0% { left: 0; }
  100% { left: 100%; }
}

.analysis-node {
  position: absolute;
  bottom: 20px;
  right: 20%;
  width: 12px;
  height: 12px;
  background: rgba(64, 196, 255, 0.6);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(64, 196, 255, 0.8);
  animation: analysisPulse 2s infinite;
}

@keyframes analysisPulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-card {
    width: 95%;
    height: auto;
    flex-direction: column;
  }
  
  .left-section, .right-section {
    width: 100%;
    padding: 30px 20px;
  }
  
  .health-stats {
    flex-direction: column;
    gap: 20px;
  }
}
</style>