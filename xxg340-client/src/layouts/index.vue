<template>
  <div class="top-nav-layout">
    <!-- 顶部导航栏 -->
    <header class="navbar">
      <!-- Logo 区域 -->
      <div class="logo" @click="go('/index/index')">
        <svg width="24" height="20" viewBox="0 0 24 20" class="ecg-icon">
          <path
            d="M2 10 Q6 4, 10 10 T18 10"
            stroke="#4CAF50"
            stroke-width="2"
            fill="none"
          />
        </svg>
        <span class="logo-text">心血管疾病风险可视化分析</span>
      </div>

      <!-- 主导航菜单 -->
      <nav class="nav-menu">
        <router-link
          to="/index/index"
          class="nav-item"
          active-class="active"
        >
          首页
        </router-link>
        <router-link
          to="/healthnews/index"
          class="nav-item"
          active-class="active"
        >
          健康资讯列表
        </router-link>
        <router-link
          to="/prediction/single"
          class="nav-item"
          active-class="active"
        >
          单次预测
        </router-link>
        <!-- <router-link
          to="/prediction/batch"
          class="nav-item"
          active-class="active"
        >
          批量预测
        </router-link> -->
        <router-link
          to="/prediction/history"
          class="nav-item"
          active-class="active"
        >
          预测历史
        </router-link>
        <router-link
          to="/healthdata/input"
          class="nav-item"
          active-class="active"
        >
          数据录入
        </router-link>
        <router-link
          to="/healthdata/list"
          class="nav-item"
          active-class="active"
        >
          数据信息
        </router-link>
        <router-link
          to="/visualization/risktrend"
          class="nav-item"
          active-class="active"
        >
          疾病风险趋势分析
        </router-link>
        <router-link
          to="/visualization/healthdist"
          class="nav-item"
          active-class="active"
        >
          健康指标分布图
        </router-link>
        <router-link
          to="/visualization/predstats"
          class="nav-item"
          active-class="active"
        >
          预测结果统计图
        </router-link>
        <router-link
          to="/user/mypredictions"
          class="nav-item"
          active-class="active"
        >
          我的预测
        </router-link>
      </nav>

      <!-- 用户下拉菜单 -->
      <el-dropdown
        class="user-dropdown"
        trigger="click"
        @command="handleCommand"
      >
        <div class="user-trigger">
          <div v-if="userInfo.avatar" class="avatar">
            <img :src="userInfo.avatar" alt="avatar" />
          </div>
          <div v-else class="avatar-placeholder">
            {{ userInfo.user_name ? userInfo.user_name : 'U' }}
          </div>
          <span class="username">{{ userInfo.user_name || '用户' }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="/user/mypredictions">
              <i class="fas fa-chart-bar menu-icon"></i>
              <span>我的预测</span>
            </el-dropdown-item>
            <el-dropdown-item command="/user/edit">
              <i class="fas fa-user menu-icon"></i>
              <span>个人信息</span>
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <i class="fas fa-sign-out-alt menu-icon"></i>
              <span>退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <Main />
    </main>
  </div>
</template>

<script setup lang="ts">
import { GlobalStore } from "@/stores";
import { useRouter } from "vue-router";
import { LOGIN_URL } from "@/config/config";
import { computed } from "vue";

import Main from "@/layouts/components/Main/index.vue";

const globalStore = GlobalStore();
const router = useRouter();
const userInfo = globalStore.userInfo;

const go = (url) => {
  router.push({ path: url });
};

const logout = () => {
  router.replace(LOGIN_URL);
  globalStore.setToken("");
  globalStore.userInfo = {};
};

const handleCommand = (command) => {
  if (command == 'logout') {
    logout();
  } else {
    go(command);
  }
};
</script>

<style scoped>
/* 整体布局 */
.top-nav-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏样式 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #F8F9FA;
  display: flex;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 1000;
  min-width: 1200px;
}

/* Logo 样式 */
.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-right: 40px;
}

.ecg-icon {
  margin-right: 8px;
}

.logo-text {
  font-size: 20px;
  font-weight: 500;
  color: #495057;
  font-family: "Source Han Sans CN", "Microsoft YaHei", sans-serif;
}

/* 导航菜单 */
.nav-menu {
  display: flex;
  flex: 1;
  height: 100%;
}

.nav-item {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 16px;
  color: #495057;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  position: relative;
  transition: all 0.3s ease;
}

/* 悬停效果 */
.nav-item:hover {
  color: #1E88E5;
}

.nav-item:hover::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, #4CAF50, transparent);
  animation: expandLine 0.3s ease forwards;
}

/* 激活状态 */
.nav-item.active {
  color: #1E88E5;
  font-weight: 600;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #4CAF50;
}

/* 动画：下划线从中心展开 */
@keyframes expandLine {
  0% {
    width: 0;
    left: 50%;
    transform: translateX(-50%);
  }
  100% {
    width: 100%;
    left: 0;
    transform: translateX(0);
  }
}

/* 点击反馈 */
.nav-item:active {
  transform: scale(0.98);
  opacity: 0.9;
}

/* 用户下拉触发器 */
.user-dropdown {
  margin-left: auto;
}

.user-trigger {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #495057;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.user-trigger:hover {
  background-color: #F5F7FA;
}

.avatar,
.avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  background-color: #E0E0E0;
  color: #495057;
  font-weight: 600;
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

/* 主内容区 */
.main-content {
  margin-top: 60px;
  flex: 1;
}

/* 自定义下拉菜单容器 */
:deep(.el-dropdown-menu) {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 4px 0;
  min-width: 200px;
  animation: dropdownSlideIn 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}

/* 下拉菜单项 */
:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  font-size: 14px;
  color: #495057;
  line-height: 24px;
  margin: 0 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: #F5F7FA;
  color: #1E88E5;
}

:deep(.el-dropdown-menu__item:hover .menu-icon) {
  color: #1E88E5;
}

/* 菜单项图标 */
:deep(.menu-icon) {
  width: 16px;
  height: 16px;
  margin-right: 12px;
  color: #6C757D;
  font-size: 16px;
}

/* 分隔线 */
:deep(.el-dropdown-menu__item--divided) {
  margin-top: 4px;
  padding-top: 4px;
  border-top: 1px solid #E0E0E0 !important;
}

/* 下拉菜单动画 */
@keyframes dropdownSlideIn {
  0% {
    opacity: 0;
    transform: translateY(-4px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 激活状态的我的预测项 */
:deep(.el-dropdown-menu__item[href="/user/mypredictions"].active),
:deep(.el-dropdown-menu__item[command="/user/mypredictions"].active) {
  font-weight: 600;
}
</style>