<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside
      :width="isCollapse ? '60px' : '240px'"
      class="sidebar"
      :class="{ 'collapsed': isCollapse }"
    >
      <div class="logo" :class="{ 'collapsed': isCollapse }">
        <span>后台管理</span>
      </div>
      <div class="menu-container">
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapse"
          :collapse-transition="false"
          background-color="transparent"
          text-color="#E0E7FF"
          active-text-color="#FF6B5C"
          unique-opened
          router
          class="custom-menu"
        >
          <template v-for="item in menuList" :key="item.id">
            <el-sub-menu
              v-if="item.children && item.children.length > 0"
              :index="item.path || String(item.id)"
              popper-class="custom-popper"
            >
              <template #title>
                <span class="menu-title">{{ item.meta.title || item.name }}</span>
              </template>
              <template v-for="child in item.children" :key="child.id">
                <el-sub-menu
                  v-if="child.children && child.children.length > 0"
                  :index="child.path || String(child.id)"
                >
                  <template #title>
                    <span class="menu-title">{{ child.meta.title || child.name }}</span>
                  </template>
                  <el-menu-item
                    v-for="grandChild in child.children"
                    :key="grandChild.id"
                    :index="grandChild.path"
                  >
                    <span class="menu-title">{{ grandChild.meta.title || grandChild.name }}</span>
                  </el-menu-item>
                </el-sub-menu>
                <el-menu-item
                  v-else
                  :index="child.path"
                >
                  <span class="menu-title">{{ child.meta.title || child.name }}</span>
                </el-menu-item>
              </template>
            </el-sub-menu>
            <el-menu-item
              v-else
              :index="item.path"
            >
              <span class="menu-title">{{ item.meta.title || item.name }}</span>
            </el-menu-item>
          </template>
        </el-menu>
      </div>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-button
            icon="Operation"
            circle
            @click="toggleCollapse"
            class="collapse-btn"
          />
          <div class="heartbeat-indicator">
            <div class="pulse-line"></div>
          </div>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar
                :src="userInfo.avatar"
                :size="32"
                class="user-avatar"
              />
              <span class="user-name">{{ userInfo.user_name }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="content-main">
        <Main />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { GlobalStore } from "@/stores";
import { AuthStore } from "@/stores/modules/auth";
import Main from "@/layouts/components/Main/index.vue";

const route = useRoute();
const router = useRouter();
const authStore = AuthStore();
const globalStore = GlobalStore();

const isCollapse = ref(false);
const openMenus = ref([]);

const activeMenu = computed(() => route.path);

const toEdit = () => {
  router.push('/user/edit');
};

const logout = () => {
  globalStore.setToken("");
  localStorage.removeItem("menuData");
  globalStore.userInfo = {};
  router.replace('/login');
};

const userInfo = computed(() => globalStore.userInfo);

const menuList = computed(() => authStore.showMenuListGet);

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value;
};

const handleCommand = (command) => {
  if (command == 'profile') {
    toEdit();
  } else if (command == 'logout') {
    logout();
  }
};
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
  background: linear-gradient(180deg, #0F1C3F 0%, #1A2D5E 100%);
  overflow: hidden;
  position: relative;
}

// 心跳脉冲效果
.layout-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #FF6B5C, transparent);
  animation: pulseLine 3s infinite ease-in-out;
  opacity: 0.6;
}

@keyframes pulseLine {
  0%, 100% { transform: translateX(-100%); opacity: 0; }
  50% { opacity: 0.8; }
  60% { transform: translateX(100%); opacity: 0; }
}

.sidebar {
  height: 100%;
  background: rgba(15, 28, 63, 0.85);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 107, 92, 0.3), transparent);
    animation: pulseGlow 2s infinite;
  }

  &.collapsed {
    .logo span {
      opacity: 0;
      width: 0;
      padding: 0;
    }
  }
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);

  span {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
    white-space: nowrap;
    transition: all 0.3s ease;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(255, 107, 92, 0.3);
  }
}

.menu-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.custom-menu {
  border: none;
  height: calc(100% - 10px);
  
  .el-sub-menu,
  .el-menu-item {
    margin: 4px 8px;
    border-radius: 12px;
    transition: all 0.3s ease;
    
    &:hover {
      background: rgba(255, 255, 255, 0.12) !important;
      box-shadow: 0 0 15px rgba(255, 107, 92, 0.2);
    }
  }
  
  .el-menu-item.is-active {
    background: rgba(255, 107, 92, 0.15) !important;
    border-left: 3px solid #FF6B5C;
    box-shadow: 0 0 20px rgba(255, 107, 92, 0.3);
  }
  
  .el-sub-menu.is-active {
    .el-sub-menu__title {
      background: rgba(255, 107, 92, 0.15) !important;
      border-left: 3px solid #FF6B5C;
    }
  }
  
  .el-sub-menu__title,
  .el-menu-item {
    height: 42px;
    line-height: 42px;
    padding: 0 16px !important;
    
    .menu-title {
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.5px;
    }
  }
  
  .el-sub-menu .el-menu-item {
    padding-left: 32px !important;
  }
  
  .el-sub-menu .el-sub-menu .el-menu-item {
    padding-left: 48px !important;
  }
}

.main-container {
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  box-shadow: -5px 0 25px rgba(0, 0, 0, 0.15);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: #FFFFFF;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  height: 60px;
  position: relative;
}

.collapse-btn {
  background: rgba(15, 28, 63, 0.1);
  border: 1px solid rgba(15, 28, 63, 0.2);
  color: #1A2D5E;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 107, 92, 0.1);
    color: #FF6B5C;
    transform: rotate(180deg);
  }
}

.heartbeat-indicator {
  margin-left: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  
  .pulse-line {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, #FF6B5C, #FF8E82, #FF6B5C);
    border-radius: 1px;
    animation: heartbeat 1.2s infinite;
  }
}

@keyframes heartbeat {
  0%, 100% { transform: scaleX(1); opacity: 1; }
  50% { transform: scaleX(1.2); opacity: 0.8; }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 20px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(15, 28, 63, 0.05);
  }
}

.user-avatar {
  border: 2px solid #FF6B5C;
  box-shadow: 0 0 8px rgba(255, 107, 92, 0.3);
}

.user-name {
  color: #1A2D5E;
  font-weight: 500;
  font-size: 14px;
}

.content-main {
  padding: 20px;
  background: #FFFFFF;
  flex: 1;
  overflow-y: auto;
}

// 滚动条样式
.menu-container::-webkit-scrollbar {
  width: 6px;
}

.menu-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.menu-container::-webkit-scrollbar-thumb {
  background: rgba(255, 107, 92, 0.3);
  border-radius: 3px;
  transition: all 0.3s ease;
}

.menu-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 107, 92, 0.5);
}

// 下拉菜单样式
:deep(.custom-popper) {
  background: rgba(15, 28, 63, 0.95) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px 0;
  
  .el-menu--popup {
    background: transparent !important;
    border: none !important;
    
    .el-menu-item {
      margin: 4px 8px !important;
      border-radius: 10px !important;
      
      &:hover {
        background: rgba(255, 255, 255, 0.12) !important;
      }
    }
  }
}
</style>