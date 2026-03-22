<template>
  <div class="chat-window">
    <!-- 顶部：文件信息 -->
    <div v-if="files.length > 0" class="chat-header">
      <div class="files-summary">
        <span class="icon">📚</span>
        <div class="details">
          <h4>知识库对话 ({{ files.length }} 个文件)</h4>
          <p class="hint">与所有上传的文件进行智能对话</p>
        </div>
      </div>
      <button class="clear-btn" @click="clearMessages" title="清空对话">
        🗑️
      </button>
    </div>

    <!-- 没有文件时 -->
    <div v-else class="no-files">
      <div class="empty-icon">💬</div>
      <p>请先在左侧上传文件</p>
      <p class="hint">上传后可以与所有文件进行对话</p>
    </div>

    <!-- 消息列表 -->
    <div v-if="files.length > 0" class="messages-container">
      <!-- 欢迎消息 -->
      <div v-if="messages.length === 0 && !isLoading" class="welcome-message">
        <div class="message assistant">
          <div class="message-avatar">🤖</div>
          <div class="message-content">
            <div class="message-text">
              👋 你好！我已经准备好回答关于这些文件的问题了。
              <br><br>
              你可以问我：
              <ul>
                <li>"这些文件主要讲了什么内容？"</li>
                <li>"帮我总结一下关键信息"</li>
                <li>"文件中提到了哪些重要概念？"</li>
                <li>"比较这些文件的异同点"</li>
              </ul>
            </div>
            <div class="message-time">{{ currentTime }}</div>
          </div>
        </div>
      </div>

      <!-- 历史消息 -->
      <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
        <div class="message-avatar">
          {{ message.role === 'user' ? '👤' : '🤖' }}
        </div>
        <div class="message-content">
          <div class="message-text">{{ message.content }}</div>
          <div class="message-time">{{ message.time }}</div>
        </div>
      </div>
      
      <!-- 加载中 -->
      <div v-if="isLoading" class="message assistant loading">
        <div class="message-avatar">🤖</div>
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div v-if="files.length > 0" class="input-area">
      <div class="input-wrapper">
        <textarea
          v-model="userInput"
          placeholder="请输入你的问题..."
          @keydown.enter.exact.prevent="sendMessage"
          rows="3"
          class="chat-input"
        ></textarea>
        <button 
          @click="sendMessage" 
          :disabled="!userInput.trim() || isLoading"
          class="send-btn"
        >
          <span v-if="!isLoading">📤</span>
          <span v-else>⏳</span>
        </button>
      </div>
      <p class="input-hint">按 Enter 发送，Shift + Enter 换行 · 问题将基于所有文件内容回答</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  files: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['sendMessage'])

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)

const currentTime = computed(() => {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
})

const sendMessage = async () => {
  const content = userInput.value.trim()
  if (!content || isLoading.value) return

  // 添加用户消息
  const userMessage = {
    role: 'user',
    content: content,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }
  messages.value.push(userMessage)

  userInput.value = ''
  isLoading.value = true

  try {
    // 调用父组件的 sendMessage 方法
    const aiResponse = await emit('sendMessage', content)
    
    // 添加 AI 响应
    messages.value.push({
      role: 'assistant',
      content: typeof aiResponse === 'string' ? aiResponse : '抱歉，处理您的请求时出现了问题。',
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，处理您的请求时出现了问题，请稍后重试。',
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    })
  } finally {
    isLoading.value = false
  }
}

const clearMessages = () => {
  if (confirm('确定要清空对话记录吗？')) {
    messages.value = []
  }
}
</script>

<style scoped>
.chat-window {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-bottom: 1px solid #e2e8f0;
}

.files-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.files-summary .icon {
  font-size: 2.5rem;
}

.files-summary h4 {
  color: #2d3748;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.files-summary .hint {
  color: #718096;
  font-size: 0.85rem;
}

.clear-btn {
  background: none;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.3s ease;
  padding: 0.5rem;
}

.clear-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}

.no-files {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #a0aec0;
  text-align: center;
  padding: 2rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.no-files p {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.no-files .hint {
  font-size: 0.9rem !important;
  color: #cbd5e0 !important;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.message {
  display: flex;
  gap: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 2rem;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 1rem 1.25rem;
  border-radius: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message.user .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-text {
  background: #f7fafc;
  color: #2d3748;
  border-bottom-left-radius: 4px;
}

.message-text ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.message-text li {
  margin: 0.25rem 0;
  line-height: 1.8;
}

.message-time {
  font-size: 0.75rem;
  color: #a0aec0;
  padding: 0 0.5rem;
}

.typing-indicator {
  display: flex;
  gap: 0.4rem;
  padding: 1rem 1.25rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #cbd5e0;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.welcome-message {
  margin-top: 1rem;
}

.input-area {
  padding: 1.5rem;
  background: #f7fafc;
  border-top: 1px solid #e2e8f0;
}

.input-wrapper {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.95rem;
  resize: none;
  transition: border-color 0.3s ease;
  min-height: 80px;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
}

.send-btn {
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-hint {
  font-size: 0.8rem;
  color: #a0aec0;
  text-align: center;
}

/* 滚动条样式 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style>
