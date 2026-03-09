<template>
  <div class="header-container">
    <!-- Logo 区域 -->
    <div class="logo" @click="go('/index/index')">
     前台
    </div>

    <!-- 导航菜单 -->
    <div class="nav-menu">
      <div
        v-for="item in navItems"
        :key="item.path"
        class="nav-item"
        @click="go(item.path)"
      >
        {{ item.name }}
      </div>
    </div>

    <!-- 用户区域 -->
    <el-dropdown trigger="click">
      <div class="user-msg">
        <span class="username">{{ userInfo.user_name }}</span>
        <div class="avatar-wrapper">
          <img
            v-if="userInfo.avatar"
            :src="userInfo.avatar"
            alt="avatar"
            class="avatar"
          />
          <div v-else class="default-avatar">👤</div>
        </div>
      </div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            v-for="item in userMenuItems"
            :key="item.path"
            @click="go(item.path)"
          >
            {{ item.name }}
          </el-dropdown-item>
          <el-dropdown-item @click="go('/user/edit')">
            个人信息
          </el-dropdown-item>
          <el-dropdown-item @click="logout" style="color: #ff4757;">
            退出登录
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { GlobalStore } from "@/stores";
import { LOGIN_URL } from "@/config/config";
import { useRouter } from "vue-router";
import dynamicRouter from '@/routers/modules/dynamicRouter';

/*** 固定代码部分 不要更改 */
const router = useRouter();
const globalStore = GlobalStore();

const userInfo = globalStore.userInfo;

// 过滤导航项和用户菜单项
const navItems = computed(() => dynamicRouter.filter(item => item.isNav));
const userMenuItems = computed(() => dynamicRouter.filter(item => item.isUserMenu));

const go = (url) => {
  router.push({ path: url });
};

const logout = () => {
  router.replace(LOGIN_URL);
  globalStore.setToken("");
  globalStore.userInfo = {};
};
/*** 固定代码部分 不要更改 */
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 100;
  font-family: 'Segoe UI', sans-serif;
  color: white;
  border-bottom: 3px solid #ff5e5b;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: 1px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.logo:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(255, 150, 0, 0.6);
}

.logo-text {
  background: linear-gradient(to right, #fff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.highlight {
  color: #ff4757;
  font-weight: 900;
  text-shadow: 0 0 8px rgba(255, 71, 87, 0.6);
}

.logo-icon {
  font-size: 1.5rem;
  animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
  from { transform: scale(1); }
  to { transform: scale(1.2); }
}

.nav-menu {
  display: flex;
  gap: 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.nav-item {
  padding: 0.6rem 1.2rem;
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-item::before {
  content: '';
  position: absolute;
  top: -100%;
  left: -100%;
  width: 300%;
  height: 300%;
  background: radial-gradient(circle, transparent 20%, rgba(255, 255, 255, 0.3) 60%, rgba(255, 255, 255, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
}

.nav-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
  background: rgba(255, 255, 255, 0.3);
}

.nav-item:hover::before {
  opacity: 1;
  top: 0;
  left: 0;
}

.nav-item.active,
.nav-item:focus {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: white;
  box-shadow: 0 0 15px rgba(255, 107, 107, 0.6);
  border: 1px solid #ff5e5b;
}

.user-msg {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 1rem;
  color: white;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

.username {
  transition: color 0.3s ease;
}

.user-msg:hover .username {
  color: #ffeb3b;
}

.avatar-wrapper {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #ffeb3b;
  box-shadow: 0 0 10px rgba(255, 235, 59, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.avatar-wrapper:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(255, 235, 59, 0.8);
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #6a11cb, #2575fc);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
}

/* 高级光效：顶部波纹动画 */
.header-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 50 Q30 10 50 50 T90 50' stroke='%23ffffff' stroke-width='1' fill='none' stroke-opacity='0.1'/%3E%3C/svg%3E");
  background-size: 100% 100%;
  opacity: 0.2;
  pointer-events: none;
  animation: wave 8s linear infinite;
}

@keyframes wave {
  0% { background-position: 0% 0%; }
  100% { background-position: 100% 100%; }
}
</style>