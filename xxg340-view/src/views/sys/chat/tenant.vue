<template>
  <div class="page-container">
    <!-- 聊天主界面 -->
    <div class="chat-container">
      <!-- 左侧会话列表 -->
      <div class="conversation-list glass-panel">
        <div class="list-header">
          <h3>会话列表</h3>
        </div>
        <el-scrollbar class="scrollbar-wrapper">
          <div 
            v-for="conversation in conversationList" 
            :key="conversation.userId"
            class="conversation-item"
            :class="{ active: activeConversationId == conversation.userId }"
            @click="selectConversation(conversation.userId)"
          >
            <div class="avatar-wrapper">
              <img 
                :src="conversation.avatar || defaultAvatar" 
                alt="用户头像" 
                class="avatar"
              />
              <div class="status-dot" :class="{ online: conversation.lastActive }"></div>
            </div>
            <div class="conversation-info">
              <div class="name-line">
                <span class="user-name">{{ conversation.name }}</span>
                <span class="last-time">{{ formatTime(conversation.lastMessageTime) }}</span>
              </div>
              <div class="preview-text" :title="conversation.lastMessage">
                {{ conversation.lastMessage }}
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>

      <!-- 右侧聊天窗口 -->
      <div class="chat-window card-shadow">
        <div v-if="!activeConversationId" class="empty-placeholder">
          <el-empty description="请选择左侧用户开始聊天" />
        </div>
        
        <template v-else>
          <!-- 聊天头部 -->
          <div class="chat-header">
            <div class="header-left">
              <img 
                :src="currentUserInfo.avatar || defaultAvatar" 
                alt="用户头像" 
                class="header-avatar"
              />
              <div class="header-info">
                <h4>{{ currentUserInfo.name }}</h4>
                <p class="status-text">
                  {{ currentUserInfo.lastActive ? '在线' : '离线' }}
                </p>
              </div>
            </div>
            <div class="header-right">
              <el-button 
                type="primary" 
                size="small" 
                @click="refreshMessages"
                class="refresh-btn"
              >
                刷新消息
              </el-button>
            </div>
          </div>

          <!-- 消息区域 -->
          <el-scrollbar ref="messageContainer" class="message-container">
            <div class="messages-wrapper">
              <!-- 文本消息 -->
              <div 
                v-for="(msg, index) in messages" 
                :key="index" 
                class="message-item"
                :class="{ 'self-message': msg.fromuserid == userInfo.id }"
              >
                <div class="message-avatar">
                  <img 
                    :src="msg.fromuserid == userInfo.id ? globalStore.userInfo.avatar : (currentUserInfo.avatar || defaultAvatar)" 
                    alt="头像" 
                    class="msg-avatar-img"
                  />
                </div>
                <div class="message-content">
                  <div class="message-bubble" :class="{ 'self-bubble': msg.fromuserid == userInfo.id }">
                    <!-- 文本消息 -->
                    <div v-if="msg.type === '文本'" class="bubble-content">{{ msg.content }}</div>
                    <!-- 图片消息 -->
                    <div v-else-if="msg.type === '图片'" class="image-bubble">
                      <img 
                        :src="msg.content" 
                        @click="previewImage(msg.content)" 
                        class="message-image" 
                        alt="图片消息"
                      />
                    </div>
                    <!-- 其他类型消息 -->
                    <div v-else class="bubble-content unknown-type">
                      [暂不支持的消息类型]
                    </div>
                    <div class="message-time">{{ formatTime(msg.cd) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </el-scrollbar>

          <!-- 输入区域 -->
          <div class="input-area">
            <div class="input-wrapper">
              <textarea 
                v-model="newMessage" 
                placeholder="请输入消息..." 
                class="message-input" 
                :maxlength="500"
                @keydown.enter.exact.prevent="sendMessage"
                @input="adjustTextareaHeight"
                ref="messageInput"
              ></textarea>
              <div class="send-actions">
                <UploadImg v-model:imageUrl="imageFile" class="upload-btn" />
                <el-button 
                  type="primary" 
                  @click="sendMessage"
                  :disabled="!newMessage && !imageFile"
                  class="send-btn"
                >
                  发送消息
                </el-button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
// 固定代码只能新增不能修改
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

import { ElMessage, ElMessageBox } from 'element-plus'
import { request } from '@/http/index'; // 请求数据直接用这个
import { GlobalStore } from '@/stores';
const globalStore = GlobalStore();
import * as echarts from "echarts"; // echarts图表 需要时直接使用

const userInfo = globalStore.userInfo

/**
以下属于全局组件可直接使用不要引入：
富文本编辑：<WangEditor height="400px" v-model:value="字段名称" />
单图上传：<UploadImg  v-model:imageUrl="字段名称" />
多图上传：<UploadManyImg  v-model:imageUrl="字段名称" />
文件上传： <UploadFile  v-model:fileUrl="字段名称" />
*/
// 固定代码只能新增不能修改

// 数据定义
const conversationList = ref([])
const activeConversationId = ref(null)
const messages = ref([])
const newMessage = ref('')
const imageFile = ref('')
const currentUserInfo = ref({})
const myAvatar = ref('/default-avatar.png')
const defaultAvatar = ref('/default-avatar.png')
const messageContainer = ref(null)
const messageInput = ref(null)

// 轮询相关变量
let pollInterval = null
const pollIntervalTime = 1000 // 3秒轮询一次

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

// 开始轮询
const startPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
  pollInterval = setInterval(() => {
    // 如果有活跃的会话，轮询更新消息
    if (activeConversationId.value) {
      loadMessages(activeConversationId.value, true) // true 表示是轮询请求
    }
    // 同时更新会话列表
    loadConversationList(true) // true 表示是轮询请求
  }, pollIntervalTime)
}

// 停止轮询
const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

// 页面可见性监听
const handleVisibilityChange = () => {
  if (document.hidden) {
    // 页面不可见时暂停轮询
    stopPolling()
  } else {
    // 页面可见时恢复轮询
    startPolling()
  }
}

// 加载会话列表
const loadConversationList = async (isPolling = false) => {
  try {
    // 获取我相关的所有聊天记录
    const chatRes1 = await request('/chatmsg/index', { 
      fromuserid: userInfo.id,
      "limit": "999"
    }, 'get')
    
    const chatRes2 = await request('/chatmsg/index', { 
      touserid: userInfo.id,
      "limit": "999"
    }, 'get')
    
    const chats = [...(chatRes1.data || []), ...(chatRes2.data || [])]
    
    // 按用户分组构建会话列表
    const userMap = {}
    
    // 先收集所有需要获取的用户ID
    const userIds = []
    chats.forEach(chat => {
      const otherUserId = chat.fromuserid == userInfo.id ? chat.touserid : chat.fromuserid
      if (!userMap[otherUserId]) {
        userIds.push(otherUserId)
        userMap[otherUserId] = {
          userId: otherUserId,
          name: `用户${otherUserId}`, // 先设置默认值
          avatar: defaultAvatar.value,
          lastMessage: '',
          lastMessageTime: '',
          lastActive: true
        }
      }
    })
    
    // 批量获取用户信息
    const userInfos = await Promise.all(
      userIds.map(userId => getUserInfo(userId))
    )
    
    // 更新用户信息
    userInfos.forEach((userInfo, index) => {
      if (userInfo) {
        const userId = userIds[index]
        userMap[userId].name = userInfo.user_name || `用户${userId}`
        userMap[userId].avatar = userInfo.avatar || defaultAvatar.value
      }
    })
    
    // 处理聊天内容
    chats.forEach(chat => {
      const otherUserId = chat.fromuserid == userInfo.id ? chat.touserid : chat.fromuserid
      
      if (userMap[otherUserId] && chat.chatcontent) {
        // 解析聊天内容
        let chatContent = []
        if (typeof chat.chatcontent == 'string') {
          try {
            chatContent = JSON.parse(chat.chatcontent)
          } catch (e) {
            console.error('解析聊天内容失败:', e)
            chatContent = []
          }
        } else {
          chatContent = chat.chatcontent
        }
        
        // 获取最后一条消息
        if (chatContent.length > 0) {
          const lastMsg = chatContent[chatContent.length - 1]
          if (!userMap[otherUserId].lastMessageTime || 
              new Date(lastMsg.cd) > new Date(userMap[otherUserId].lastMessageTime)) {
            userMap[otherUserId].lastMessage = lastMsg.content
            userMap[otherUserId].lastMessageTime = lastMsg.cd
          }
        }
      }
    })
    
    // 将map转换为数组并按最后消息时间排序
    conversationList.value = Object.values(userMap).sort((a, b) => {
      return new Date(b.lastMessageTime) - new Date(a.lastMessageTime)
    })
    
    // 如果是首次加载且有会话，自动选中第一个
    if (!isPolling && conversationList.value.length > 0 && !activeConversationId.value) {
      selectConversation(conversationList.value[0].userId)
    }
  } catch (error) {
    if (!isPolling) {
      ElMessage.error('加载会话列表失败')
    }
    console.error(error)
  }
}

// 获取用户信息
const getUserInfo = async (userId) => {
  try {
    const res = await request('/user/show', { id: userId }, 'get')
    return res
  } catch (error) {
    console.error('获取用户信息失败:', error)
    return null
  }
}

// 选择会话
const selectConversation = async (userId) => {
  activeConversationId.value = userId
  
  // 获取当前用户信息
  const currentConversation = conversationList.value.find(c => c.userId == userId)
  if (currentConversation) {
    currentUserInfo.value = { ...currentConversation }
  }
  
  // 加载该用户的聊天记录
  await loadMessages(userId)
}

// 加载消息
const loadMessages = async (userId, isPolling = false) => {
  try {
    // 查询双方的聊天记录 - 只需要查询一次，找到对应的聊天记录
    const chatRes1 = await request('/chatmsg/index', { 
      fromuserid: userInfo.id,
      touserid: userId
    }, 'get')
    
    const chatRes2 = await request('/chatmsg/index', { 
      fromuserid: userId,
      touserid: userInfo.id
    }, 'get')
    
    let chatRecord = null
    
    // 优先查找 fromuserid 是我的记录
    if (chatRes1.data && chatRes1.data.length > 0) {
      chatRecord = chatRes1.data[0]
    } 
    // 如果没有找到，再查找 touserid 是我的记录
    else if (chatRes2.data && chatRes2.data.length > 0) {
      chatRecord = chatRes2.data[0]
    }
    
    if (chatRecord && chatRecord.chatcontent) {
      // 解析聊天内容
      let chatContent = []
      if (typeof chatRecord.chatcontent === 'string') {
        try {
          chatContent = JSON.parse(chatRecord.chatcontent)
        } catch (e) {
          console.error('解析聊天内容失败:', e)
          chatContent = []
        }
      } else {
        chatContent = chatRecord.chatcontent
      }
      
      // 按时间排序
      const newMessages = chatContent.sort((a, b) => new Date(a.cd) - new Date(b.cd))
      
      // 只有在消息有变化时才更新，避免不必要的渲染
      if (JSON.stringify(newMessages) !== JSON.stringify(messages.value)) {
        messages.value = newMessages
        
        // 如果不是轮询请求，滚动到底部
        if (!isPolling) {
          scrollToBottom()
        }
      }
    } else {
      // 没有聊天记录
      messages.value = []
    }
    
    // 如果不是轮询请求，滚动到底部
    if (!isPolling) {
      scrollToBottom()
    }
  } catch (error) {
    if (!isPolling) {
      ElMessage.error('加载消息失败')
    }
    console.error(error)
  }
}

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value && !imageFile.value) {
    ElMessage.warning('请输入消息内容或选择图片')
    return
  }
  
  if (!activeConversationId.value) {
    ElMessage.warning('请选择用户')
    return
  }
  
  try {
    const messageType = imageFile.value ? '图片' : '文本'
    const content = imageFile.value || newMessage.value

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
      fromuserid: userInfo.id,
      touserid: activeConversationId.value,
    }

    console.log("当前发送聊天内容", currentContent)
    
    // 查询是否已有聊天记录
    const chatRes1 = await request('/chatmsg/index', { 
      fromuserid: userInfo.id,
      touserid: activeConversationId.value
    }, 'get')
    
    const chatRes2 = await request('/chatmsg/index', { 
      fromuserid: activeConversationId.value,
      touserid: userInfo.id
    }, 'get')
    
    let currentChat = null
    if (chatRes1.data && chatRes1.data.length > 0) {
      currentChat = chatRes1.data[0]
    } else if (chatRes2.data && chatRes2.data.length > 0) {
      currentChat = chatRes2.data[0]
    }

    let updatedMessages = []
    if (currentChat) {
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
        fromuserid: userInfo.id,
        touserid: activeConversationId.value,
        chatcontent: JSON.stringify(updatedMessages, null, 2),
        chatid: `${userInfo.id}_${activeConversationId.value}`
      }, 'post')
    }
    
    // 重新加载消息
    await loadMessages(activeConversationId.value)
    
    // 清空输入框和图片
    newMessage.value = ''
    imageFile.value = ''
    if (messageInput.value) {
      messageInput.value.style.height = 'auto'
    }

    // 更新会话列表
    await loadConversationList()

    ElMessage.success('发送成功')
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送失败，请重试')
  }
}

// 刷新消息
const refreshMessages = async () => {
  if (activeConversationId.value) {
    await loadMessages(activeConversationId.value)
    ElMessage.success('消息已刷新')
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messageContainer.value) {
    nextTick(() => {
      const wrap = messageContainer.value.$el.querySelector('.el-scrollbar__wrap')
      if (wrap) {
        wrap.scrollTop = wrap.scrollHeight
      }
    })
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadConversationList()
  startPolling()
  
  // 监听页面可见性变化
  document.addEventListener('visibilitychange', handleVisibilityChange)
})

// 组件销毁前停止轮询和移除监听器
onBeforeUnmount(() => {
  stopPolling()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})

// 监听消息变化，自动滚动到底部
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// 监听图片上传完成
watch(imageFile, (newVal) => {
  if (newVal) {
    // 自动发送图片
    sendMessage()
  }
})

// 监听活跃会话变化
watch(activeConversationId, (newId) => {
  if (newId) {
    // 切换会话时立即加载一次消息
    loadMessages(newId)
  }
})
</script>

<style scoped>
/* 样式保持不变，与之前相同 */
.page-container {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
  position: relative;
}

.chat-container {
  display: flex;
  gap: 24px;
  height: calc(100vh - 48px);
}

/* 左侧会话列表 */
.conversation-list {
  width: 320px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.list-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.list-header h3 {
  color: #1e293b;
  font-weight: 600;
  font-size: 18px;
  margin: 0;
}

.scrollbar-wrapper {
  flex: 1;
  height: calc(100% - 60px);
}

.conversation-item {
  display: flex;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.conversation-item:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
}

.conversation-item.active {
  background: #dbeafe;
  border-left: 3px solid #3b82f6;
}

.avatar-wrapper {
  position: relative;
  margin-right: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e2e8f0;
}

.status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #94a3b8;
  border: 2px solid white;
}

.status-dot.online {
  background: #10b981;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.name-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.last-time {
  font-size: 12px;
  color: #64748b;
}

.preview-text {
  font-size: 13px;
  color: #475569;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 右侧聊天窗口 */
.chat-window {
  flex: 1;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.empty-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 聊天头部 */
.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
  border: 2px solid #e2e8f0;
}

.header-info h4 {
  margin: 0 0 4px 0;
  color: #1e293b;
  font-weight: 600;
}

.status-text {
  margin: 0;
  font-size: 12px;
  color: #64748b;
}

.refresh-btn {
  background: linear-gradient(135deg, #C2E9FB 0%, #A1C4FD 100%);
  border: none;
  color: #1e40af;
  font-weight: 600;
}

/* 消息区域 */
.message-container {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.messages-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  margin-bottom: 16px;
}

.message-item.self-message {
  flex-direction: row-reverse;
}

.message-item.self-message .message-content {
  text-align: right;
}

.message-avatar {
  margin: 0 12px;
}

.msg-avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.message-content {
  max-width: 70%;
  flex: 1;
}

.message-bubble {
  display: inline-block;
  padding: 12px 16px;
  border-radius: 18px;
  background: #f1f5f9;
  color: #1e293b;
  font-size: 14px;
  line-height: 1.5;
  position: relative;
  word-break: break-word;
}

.message-bubble.self-bubble {
  background: linear-gradient(135deg, #C2E9FB 0%, #A1C4FD 100%);
  color: #1e40af;
}

.bubble-content {
  margin-bottom: 4px;
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

.unknown-type {
  background-color: #ffebee;
  color: #c62828;
  font-style: italic;
}

.message-time {
  font-size: 11px;
  color: #94a3b8;
  text-align: right;
}

/* 输入区域 */
.input-area {
  padding: 16px 24px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
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

.send-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-btn {
  display: inline-block;
}

.send-btn {
  background: linear-gradient(135deg, #C2E9FB 0%, #A1C4FD 100%);
  border: none;
  color: #1e40af;
  font-weight: 600;
  padding: 8px 24px;
  border-radius: 8px;
}

.send-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
    height: auto;
  }
  
  .conversation-list {
    width: 100%;
    height: 300px;
  }
  
  .chat-window {
    height: calc(100vh - 380px);
  }
}
</style>