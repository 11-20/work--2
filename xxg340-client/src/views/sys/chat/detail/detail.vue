<template>
  <div class="chat-container">
    <!-- 顶部用户信息栏 -->
    <div class="user-info-header">
      <img :src="targetUser.avatar || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'" alt="用户头像"
        class="avatar" />
      <div class="user-info">
        <div class="username">{{ targetUser.user_name || '未知用户' }}</div>
        <div class="status online">在线</div>
      </div>
    </div>

    <!-- 消息历史区域 -->
    <div ref="messageContainer" class="message-list">
      <div v-for="msg in messages" :key="msg.id"
        :class="['message-item', msg.fromuserid == userInfo.id ? 'self' : 'other']">
        <!-- 对方消息显示头像在左边 -->
        <div v-if="msg.fromuserid != userInfo.id" class="message-avatar">
          <img :src="targetUser.avatar || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'" alt="用户头像" class="avatar-img" />
        </div>
        
        <div class="message-content">
          <!-- 文本消息 -->
          <div v-if="msg.type === '文本'" class="text-bubble">
            {{ msg.content }}
          </div>
          <!-- 图片消息 -->
          <div v-else-if="msg.type === '图片'" class="image-bubble">
            <img :src="msg.content" @click="previewImage(msg.content)" class="message-image" />
          </div>
          <!-- 其他类型消息（可扩展） -->
          <div v-else class="text-bubble unknown-type">
            [暂不支持的消息类型]
          </div>
          <div class="time">{{ formatTime(msg.cd) }}</div>
        </div>

        <!-- 自己消息显示头像在右边 -->
        <div v-if="msg.fromuserid == userInfo.id" class="message-avatar">
          <img :src="userInfo.avatar || 'https://cdn-icons-png.flaticon.com/512/149/149071.png'" alt="我的头像" class="avatar-img" />
        </div>
      </div>
      <!-- <div v-if="loading" class="loading-indicator">加载中...</div> -->
      <div v-if="messages.length === 0 && !loading" class="empty-message">
        还没有消息，开始聊天吧~
      </div>
    </div>

    <!-- 底部输入区域 -->
    <div class="input-area">
      <div class="input-wrapper">
        <textarea v-model="newMessage" placeholder="请输入消息..." class="message-input" :maxlength="500"
          @keydown.enter.exact.prevent="sendMessage" @input="adjustTextareaHeight" ref="messageInput"></textarea>
        <div class="input-actions">
          <div class="action-left">
            <!-- 图片上传组件 -->
            <UploadImg v-model:imageUrl="imageFile" class="upload-btn" />
          </div>
          <div class="action-right">
            <button @click="sendMessage" :disabled="!newMessage && !imageFile" class="send-btn">
              发送
            </button>
          </div>
        </div>
        <!-- 图片预览 -->
        <div v-if="imageFile" class="image-preview">
          <img :src="imageFile" alt="预览图片" class="preview-image" />
          <button @click="clearImage" class="clear-image-btn">×</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 固定引入只能增加不能减少
import {
  ref,
  reactive,
  onMounted,
  onUpdated,
  onBeforeUnmount,
  computed,
  watch,
  watchEffect,
  provide,
  inject,
  nextTick
} from 'vue';

import { request } from "@/http/index";
import { GlobalStore } from "@/stores";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from "echarts"; // echarts图表 需要时直接使用
import "@/utils/echarts-wordcloud.min.js" // 词云图组件，有词云图组件在引入

const router = useRouter();
const route = useRoute();
const globalStore = GlobalStore();

/**
全局组件可直接使用：
富文本编辑：<WangEditor height="400px" v-model:value="字段名称" />
单图上传：<UploadImg  v-model:imageUrl="字段名称" />
多图上传：<UploadManyImg  v-model:imageUrl="字段名称" />
文件上传： <UploadFile  v-model:fileUrl="字段名称" />
*/

const userInfo = globalStore.userInfo

// 路由参数
const target_id = route.query.target_id
const order_id = route.query.order_id
const house_id = route.query.house_id

// 数据定义
const messages = ref([])
const newMessage = ref('')
const imageFile = ref('')
const loading = ref(false)
const messageContainer = ref(null)
const messageInput = ref(null)

// 对方用户信息
const targetUser = ref({
  id: '',
  user_name: '',
  avatar: ''
})

// 格式化时间
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  
  // 处理不同格式的时间戳
  let date
  if (typeof timestamp === 'string' && timestamp.includes('-')) {
    // 如果是 "2025-11-25 11:43:07" 格式
    date = new Date(timestamp.replace(/-/g, '/'))
  } else {
    // 如果是数字时间戳
    date = new Date(timestamp)
  }
  
  // 检查日期是否有效
  if (isNaN(date.getTime())) {
    return ''
  }
  
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString()
}

// 调整文本框高度
const adjustTextareaHeight = () => {
  if (messageInput.value) {
    messageInput.value.style.height = 'auto'
    messageInput.value.style.height = messageInput.value.scrollHeight + 'px'
    if (messageInput.value.scrollHeight > 120) {
      messageInput.value.style.height = '120px'
      messageInput.value.style.overflowY = 'auto'
    }
  }
}

// 预览图片
const previewImage = (url) => {
  if (url) {
    window.open(url, '_blank')
  }
}

// 清除已选择的图片
const clearImage = () => {
  imageFile.value = ''
}

// 获取对方用户资料
const fetchTargetUser = async () => {
  if (!target_id) return
  try {
    const res = await request('/user/show', {
      id: target_id
    }, 'get')
    targetUser.value = res
    console.log("目标用户信息:", res)
  } catch (error) {
    console.error('获取用户资料失败:', error)
  }
}

// 获取聊天历史
const fetchMessages = async () => {
  if (!target_id || !userInfo.id) return
  
  loading.value = true
  try {
    // 1.先查询这两个用户是否产生过聊天记录 - 这里需要查两次
    const chathistory1 = await request('/chatmsg/index', { 
      fromuserid: globalStore.userInfo.id, 
      touserid: target_id 
    })
    const chathistory2 = await request('/chatmsg/index', { 
      fromuserid: target_id, 
      touserid: globalStore.userInfo.id 
    })
    
    let currentChat = null
    if (chathistory1.data && chathistory1.data.length > 0) {
      currentChat = chathistory1.data[0]
    } else if (chathistory2.data && chathistory2.data.length > 0) {
      currentChat = chathistory2.data[0]
    }

    if (currentChat && currentChat.chatcontent) {
      // 确保 chatcontent 是数组格式
      if (typeof currentChat.chatcontent === 'string') {
        try {
          messages.value = JSON.parse(currentChat.chatcontent)
        } catch (e) {
          console.error('解析聊天内容失败:', e)
          messages.value = []
        }
      } else {
        messages.value = currentChat.chatcontent
      }
    } else {
      messages.value = []
    }
    
    console.log("聊天记录结果:", messages.value)
    
    // 滚动到底部
    nextTick(() => {
      scrollToBottom()
    })
  } catch (error) {
    console.error('获取聊天记录失败:', error)
    ElMessage.error('获取聊天记录失败')
  } finally {
    loading.value = false
  }
}

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value && !imageFile.value) return

  const messageType = imageFile.value ? '图片' : '文本'
  const content = imageFile.value || newMessage.value

  if (!content.trim() && messageType === '文本') return

  try {
    // 1.先查询这两个用户是否产生过聊天记录
    const chathistory1 = await request('/chatmsg/index', { 
      fromuserid: globalStore.userInfo.id, 
      touserid: targetUser.value.id 
    })
    const chathistory2 = await request('/chatmsg/index', { 
      fromuserid: targetUser.value.id, 
      touserid: globalStore.userInfo.id 
    })
    
    let currentChat = null
    if (chathistory1.data && chathistory1.data.length > 0) {
      currentChat = chathistory1.data[0]
    } else if (chathistory2.data && chathistory2.data.length > 0) {
      currentChat = chathistory2.data[0]
    }

    // 构建新消息
    const currentContent = {
      cd: new Date().toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      }).replace(/\//g, '-'),
      content: content,
      type: messageType,
      fromuserid: globalStore.userInfo.id,
      touserid: targetUser.value.id,
    }

    console.log("当前发送聊天内容", currentContent)
    
    let updatedMessages = []
    if (currentChat && currentChat.chatcontent) {
      // 已有聊天记录，追加新消息
      if (typeof currentChat.chatcontent === 'string') {
        try {
          updatedMessages = JSON.parse(currentChat.chatcontent)
        } catch (e) {
          console.error('解析现有聊天内容失败:', e)
          updatedMessages = []
        }
      } else {
        updatedMessages = [...currentChat.chatcontent]
      }
      updatedMessages.push(currentContent)
      
      // 更新会话
      await request('/chatmsg/update?id=' + currentChat.id, { 
        chatcontent: JSON.stringify(updatedMessages, null, 2) 
      }, 'put')
    } else {
      // 新建会话
      updatedMessages = [currentContent]
      await request('/chatmsg/store', {
        fromuserid: globalStore.userInfo.id,
        touserid: targetUser.value.id,
        chatcontent: JSON.stringify(updatedMessages, null, 2),
        chatid: `${globalStore.userInfo.id}_${targetUser.value.id}`
      }, 'post')
    }
    
    // 重新获取消息列表
    await fetchMessages()
    
    // 清空输入框和图片
    newMessage.value = ''
    imageFile.value = ''
    if (messageInput.value) {
      messageInput.value.style.height = 'auto'
    }

    ElMessage.success('发送成功')
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送失败，请重试')
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messageContainer.value) {
    nextTick(() => {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    })
  }
}

// 页面初始化
onMounted(async () => {
  await fetchTargetUser()
  await fetchMessages()

  // 监听窗口大小变化
  window.addEventListener('resize', scrollToBottom)
})

// 组件销毁前移除监听器
onBeforeUnmount(() => {
  window.removeEventListener('resize', scrollToBottom)
})

// 监听新消息变化
watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })


// 轮询相关变量
let pollInterval = null
const pollIntervalTime = 1000 // 3秒轮询一次

// 开始轮询
const startPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
  pollInterval = setInterval(() => {
    if (target_id && userInfo.id) {
      fetchMessages()
    }
  }, pollIntervalTime)
}

// 停止轮询
const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

// 在组件挂载时开始轮询
onMounted(async () => {
  await fetchTargetUser()
  await fetchMessages()
  startPolling()

  // 监听窗口大小变化
  window.addEventListener('resize', scrollToBottom)
})

// 组件销毁前停止轮询和移除监听器
onBeforeUnmount(() => {
  stopPolling()
  window.removeEventListener('resize', scrollToBottom)
})

// 监听路由变化，当离开聊天页面时停止轮询
watch(() => route.path, (newPath) => {
  if (!newPath.includes('/chat')) {
    stopPolling()
  }
})

// 监听 target_id 变化，当切换聊天对象时重新开始轮询
watch(() => target_id, (newTargetId) => {
  if (newTargetId) {
    stopPolling()
    startPolling()
  }
})

// 监听图片上传完成
watch(imageFile, (newVal) => {
  if (newVal) {
    // 如果有图片，自动聚焦到输入框，用户可以继续输入文字
    nextTick(() => {
      if (messageInput.value) {
        messageInput.value.focus()
      }
    })
  }
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
  max-width: 100%;
}

/* 用户信息头部 */
.user-info-header {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background-color: white;
  border-bottom: 1px solid #eaeaea;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
  object-fit: cover;
  border: 2px solid #f0f0f0;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
  margin-top: 4px;
}

.status.online {
  background-color: #e1f5fe;
  color: #0288d1;
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f5f5;
}

.message-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.message-item.self {
  justify-content: flex-end;
}

.message-item.other {
  justify-content: flex-start;
}

/* 消息头像 */
.message-avatar {
  margin: 0 8px;
}

.avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f0f0f0;
}

.message-content {
  max-width: 70%;
  position: relative;
}

.text-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
}

.message-item.self .text-bubble {
  background-color: #00a86b;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-item.other .text-bubble {
  background-color: #ffffff;
  color: #333;
  border: 1px solid #eaeaea;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.text-bubble.unknown-type {
  background-color: #ffebee;
  color: #c62828;
  font-style: italic;
}

.image-bubble {
  margin: 5px 0;
}

.message-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-image:hover {
  transform: scale(1.05);
}

.time {
  font-size: 11px;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

.message-item.other .time {
  text-align: left;
}

.loading-indicator {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 14px;
}

.empty-message {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 14px;
}

/* 输入区域 */
.input-area {
  padding: 15px;
  background-color: white;
  border-top: 1px solid #eaeaea;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message-input {
  width: 100%;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  resize: none;
  outline: none;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.message-input:focus {
  border-color: #00a86b;
  box-shadow: 0 0 0 2px rgba(0, 168, 107, 0.2);
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.upload-btn {
  display: inline-block;
}

.send-btn {
  background-color: #00a86b;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-btn:hover:not(:disabled) {
  background-color: #008c5a;
}

.send-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 图片预览 */
.image-preview {
  position: relative;
  display: inline-block;
  margin-top: 10px;
}

.preview-image {
  max-width: 100px;
  max-height: 100px;
  border-radius: 8px;
  border: 2px solid #eaeaea;
}

.clear-image-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 20px;
  height: 20px;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.clear-image-btn:hover {
  background: #ff3742;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .message-content {
    max-width: 85%;
  }

  .message-input {
    font-size: 16px;
    /* 避免iOS Safari缩放 */
  }
  
  .preview-image {
    max-width: 80px;
    max-height: 80px;
  }
  
  .avatar-img {
    width: 32px;
    height: 32px;
  }
}
</style>