<template>
  <div class="login-container">
    <!-- 左侧区域：主题展示区 -->
    <div class="left-panel">
      <div class="title-container">
        <h1 class="main-title">基于Django的心血管疾病风险可视化分析平台的设计与实现</h1>
      </div>
      <div class="background-wave">
        <svg viewBox="0 0 800 600" preserveAspectRatio="none">
          <path
            d="M0,300 Q200,250 400,300 T800,300 L800,600 L0,600 Z"
            fill="rgba(200, 220, 240, 0.15)"
          />
          <path
            d="M0,200 Q150,180 300,220 T600,200 T800,220 L800,600 L0,600 Z"
            fill="rgba(200, 220, 240, 0.1)"
          />
          <path
            d="M0,400 Q250,380 500,420 T800,400 L800,600 L0,600 Z"
            fill="rgba(200, 220, 240, 0.08)"
          />
        </svg>
      </div>
    </div>

    <!-- 右侧区域：表单卡片 -->
    <div class="right-panel">
      <div class="form-card">
        <!-- 标签切换 -->
        <div class="tab-container">
          <div 
            class="tab-item" 
            :class="{ active: currentTab == 'login' }"
            @click="currentTab = 'login'"
          >
            登录
            <div class="tab-indicator" v-if="currentTab == 'login'"></div>
          </div>
          <div 
            class="tab-item" 
            :class="{ active: currentTab == 'register' }"
            @click="currentTab = 'register'"
          >
            注册
            <div class="tab-indicator" v-if="currentTab == 'register'"></div>
          </div>
        </div>

        <!-- 表单内容区域 -->
        <div class="form-content">
          <!-- 登录表单 -->
          <div 
            v-if="currentTab == 'login'" 
            class="form-section"
            :class="{ 'fade-out': currentTab != 'login' }"
          >
            <el-form 
              ref="loginFormRef" 
              :model="loginForm" 
              :rules="loginRules" 
              label-width="0"
              @submit.prevent
            >
              <el-form-item prop="phone">
                <div class="input-wrapper">
                  <i class="icon user-icon"></i>
                  <el-input 
                    v-model="loginForm.phone" 
                    placeholder="请输入手机号"
                    class="custom-input"
                  />
                </div>
              </el-form-item>
              
              <el-form-item prop="password">
                <div class="input-wrapper">
                  <i class="icon lock-icon"></i>
                  <el-input 
                    v-model="loginForm.password" 
                    type="password"
                    placeholder="请输入密码"
                    class="custom-input"
                  />
                </div>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  class="submit-btn"
                  @click="login"
                >
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </div>

          <!-- 注册表单 -->
          <div 
            v-if="currentTab == 'register'" 
            class="form-section"
            :class="{ 'fade-out': currentTab != 'register' }"
          >
            <el-form 
              ref="registerFormRef" 
              :model="registerForm" 
              :rules="registerRules" 
              label-width="0"
              @submit.prevent
            >
              <el-form-item prop="user_name">
                <div class="input-wrapper">
                  <i class="icon user-icon"></i>
                  <el-input 
                    v-model="registerForm.user_name" 
                    placeholder="请输入用户名"
                    class="custom-input"
                  />
                </div>
              </el-form-item>
              
              <el-form-item prop="phone">
                <div class="input-wrapper">
                  <i class="icon phone-icon"></i>
                  <el-input 
                    v-model="registerForm.phone" 
                    placeholder="请输入手机号"
                    class="custom-input"
                  />
                </div>
              </el-form-item>
              
              <el-form-item prop="email">
                <div class="input-wrapper">
                  <i class="icon email-icon"></i>
                  <el-input 
                    v-model="registerForm.email" 
                    placeholder="请输入邮箱"
                    class="custom-input"
                  />
                </div>
              </el-form-item>
              
              <el-form-item prop="sex">
                <div class="gender-group">
                  <el-button 
                    :class="['gender-btn', { active: registerForm.sex == 1 }]"
                    @click="registerForm.sex = 1"
                  >
                    男
                  </el-button>
                  <el-button 
                    :class="['gender-btn', { active: registerForm.sex == 0 }]"
                    @click="registerForm.sex = 0"
                  >
                    女
                  </el-button>
                  <el-button 
                    :class="['gender-btn', { active: registerForm.sex == 2 }]"
                    @click="registerForm.sex = 2"
                  >
                    保密
                  </el-button>
                </div>
              </el-form-item>
              
              <el-form-item prop="password">
                <div class="input-wrapper">
                  <i class="icon lock-icon"></i>
                  <el-input 
                    v-model="registerForm.password" 
                    type="password"
                    placeholder="请输入密码"
                    class="custom-input"
                    @blur="updatePasswordStrength"
                  />
                </div>
                <!-- 密码强度指示器 -->
                <div class="password-strength" v-if="passwordStrength > 0">
                  <div 
                    class="strength-bar" 
                    :class="getStrengthClass(passwordStrength)"
                    :style="{ width: passwordStrength * 25 + '%' }"
                  ></div>
                </div>
              </el-form-item>
              
              <el-form-item prop="comfirmpassword">
                <div class="input-wrapper">
                  <i class="icon lock-icon"></i>
                  <el-input 
                    v-model="registerForm.comfirmpassword" 
                    type="password"
                    placeholder="请确认密码"
                    class="custom-input"
                  />
                </div>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  class="submit-btn"
                  @click="doRegister"
                >
                  注册
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup name="login">
import { ref, reactive, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { GlobalStore } from "@/stores";
import { request } from '@/http/index';
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter();
const globalStore = GlobalStore();
const currentTab = ref('login');
const loginFormRef = ref();
const registerFormRef = ref();

// 密码强度计算
const passwordStrength = ref(0);

const loginForm = reactive({ phone: "", password: "" });
const registerForm = reactive({
    user_name: "",
    phone: "", 
    sex: 1, // 1 男 2 女 0 女（根据现有选项调整）
    email: "",
    password:"",
    comfirmpassword:"",
})

// 密码确认验证函数
const validateConfirmPassword = (rule, value, callback) => {
  if (value != registerForm.password) {
    callback(new Error('两次输入密码不一致'));
  } else {
    callback();
  }
};

// 注册表单验证规则
const registerRules = {
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
  comfirmpassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
};

// 登录表单验证规则
const loginRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
};

// 性别选项
const sexOptions = [
  { label: '女', value: 0 },
  { label: '男', value: 1 }
];

// 计算密码强度
const updatePasswordStrength = () => {
  const password = registerForm.password;
  if (!password) {
    passwordStrength.value = 0;
    return;
  }
  
  let strength = 0;
  if (password.length >= 6) strength += 1;
  if (/[a-z]/.test(password)) strength += 1;
  if (/[A-Z]/.test(password)) strength += 1;
  if (/\d/.test(password)) strength += 1;
  if (/[^A-Za-z0-9]/.test(password)) strength += 1;
  
  passwordStrength.value = Math.min(strength, 4);
};

const getStrengthClass = (strength) => {
  if (strength <= 1) return 'weak';
  if (strength <= 2) return 'medium';
  if (strength <= 3) return 'strong';
  return 'very-strong';
};

const login = async () => {
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const data = await request('/signin', loginForm, 'post');
        globalStore.setToken(data.authToken);
        if (data.authToken) {
            // 获取网站信息
            await globalStore.getWebSiteMsg()
            // 4.跳转到首页
            router.push('/');
        }
      } catch (error) {
        ElMessage.error('登录失败，请检查账号密码');
      }
    }
  });
};

// 检查手机号是否存在固定函数不要修改
const checkPhoneDuplicate = async (phone, excludeId = null) => {
  try {
    // 1. 获取用户列表
    const { data: userList } = await request('/user/index',{phone:phone});
    return userList.length > 0
  } catch (error) {
    console.error('检查手机号重复时出错:', error);
    // 如果请求失败，默认返回false，避免阻塞用户操作
    return false;
  }
};

const doRegister = async () => {
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      const isDuplicate = await checkPhoneDuplicate(registerForm.phone);
      if (isDuplicate) {
        ElMessage.error('该手机号已被注册');
        return;
      } 
      try {
        await request('/register', registerForm, 'post');
        ElMessage({ message: '注册成功，请重新登录', type: 'success' });
        currentTab.value = 'login';
        // 重置注册表单
        Object.assign(registerForm, {
          user_name: "",
          phone: "", 
          sex: 1,
          email: "",
          password: "",
          comfirmpassword: ""
        });
        passwordStrength.value = 0;
      } catch (error) {
        ElMessage.error('注册失败，请稍后重试');
      }
    }
  });
}
</script>

<style lang="scss">
.login-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
  
  // 左侧面板样式
  .left-panel {
    flex: 0 0 60%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
    overflow: hidden;
    
    .title-container {
      position: relative;
      z-index: 2;
      text-align: center;
      padding: 0 40px;
      
      .main-title {
        font-size: 28px;
        font-weight: 600;
        color: #1a365d;
        line-height: 1.4;
        max-width: 800px;
        margin: 0 auto;
      }
    }
    
    .background-wave {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      opacity: 0.7;
      
      svg {
        width: 100%;
        height: 100%;
      }
    }
  }
  
  // 右侧面板样式
  .right-panel {
    flex: 0 0 40%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    
    .form-card {
      width: 100%;
      max-width: 420px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 100, 0.05);
      padding: 40px 30px;
      position: relative;
      
      // 标签切换样式
      .tab-container {
        display: flex;
        margin-bottom: 32px;
        position: relative;
        
        .tab-item {
          flex: 1;
          text-align: center;
          font-size: 18px;
          font-weight: 600;
          color: #718096;
          padding: 12px 0;
          cursor: pointer;
          position: relative;
          transition: color 0.3s ease;
          
          &.active {
            color: #1a365d;
          }
          
          .tab-indicator {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 3px;
            background: linear-gradient(90deg, #1a365d, #0ea5e9);
            border-radius: 2px;
            animation: slideIn 0.3s ease;
          }
        }
      }
      
      // 表单内容区域
      .form-content {
        .form-section {
          transition: all 0.3s ease;
          
          &.fade-out {
            opacity: 0;
            transform: translateY(-10px);
          }
        }
        
        // 输入框包装
        .input-wrapper {
          position: relative;
          margin-bottom: 24px;
          
          .icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: #718096;
            font-size: 16px;
            width: 16px;
            height: 16px;
            
            &.user-icon::before {
              content: "👤";
            }
            &.phone-icon::before {
              content: "📱";
            }
            &.email-icon::before {
              content: "✉️";
            }
            &.lock-icon::before {
              content: "🔒";
            }
          }
          
          .custom-input {
            width: 100%;
            
            .el-input__inner {
              height: 48px;
              border: 1px solid #e2e8f0;
              border-radius: 8px;
              padding-left: 48px;
              font-size: 16px;
              transition: all 0.3s ease;
              
              &:focus {
                border-color: #1a365d;
                box-shadow: 0 0 0 3px rgba(26, 54, 93, 0.1);
              }
            }
          }
        }
        
        // 性别选择按钮组
        .gender-group {
          display: flex;
          gap: 12px;
          margin-bottom: 24px;
          
          .gender-btn {
            flex: 1;
            height: 48px;
            border: 1px solid #e2e8f0;
            background: white;
            border-radius: 8px;
            color: #718096;
            font-size: 16px;
            transition: all 0.3s ease;
            
            &.active {
              background: #f0f9ff;
              border-color: #1a365d;
              color: #1a365d;
            }
            
            &:hover {
              border-color: #1a365d;
            }
          }
        }
        
        // 密码强度指示器
        .password-strength {
          height: 6px;
          background: #f1f5f9;
          border-radius: 3px;
          margin-top: 8px;
          overflow: hidden;
          
          .strength-bar {
            height: 100%;
            border-radius: 3px;
            transition: all 0.3s ease;
            
            &.weak {
              background: #dc2626;
            }
            &.medium {
              background: #f59e0b;
            }
            &.strong {
              background: #10b981;
            }
            &.very-strong {
              background: #0ea5e9;
            }
          }
        }
        
        // 提交按钮
        .submit-btn {
          width: 100%;
          height: 48px;
          background: linear-gradient(135deg, #1a365d 0%, #0ea5e9 100%);
          border: none;
          border-radius: 8px;
          color: white;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          
          &:hover {
            background: linear-gradient(135deg, #162e4d 0%, #0c8bc7 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(26, 54, 93, 0.2);
          }
          
          &:active {
            transform: translateY(0);
            box-shadow: 0 2px 6px rgba(26, 54, 93, 0.2);
          }
        }
      }
    }
  }
}

// 动画定义
@keyframes slideIn {
  from {
    width: 0;
  }
  to {
    width: 40px;
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .login-container {
    flex-direction: column;
    
    .left-panel {
      flex: 0 0 auto;
      height: 40vh;
      padding: 20px;
      
      .main-title {
        font-size: 20px;
      }
    }
    
    .right-panel {
      flex: 0 0 auto;
      width: 100%;
      padding: 20px;
      
      .form-card {
        max-width: 100%;
        margin: 0 20px;
      }
    }
  }
}

// Element Plus 表单错误样式覆盖
.el-form-item.is-error {
  .el-input__inner {
    border-color: #dc2626 !important;
    animation: shake 0.5s ease-in-out;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}
</style>