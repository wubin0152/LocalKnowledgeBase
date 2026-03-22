<template>
  <div class="app">
    <!-- 头部 -->
    <Header />
    
    <!-- 主内容区 -->
    <main class="main-content">
      <div class="container">
        <!-- 左侧面板：上传 + 文件列表 -->
        <aside class="left-panel">
          <FileUpload @filesUploaded="handleFilesUploaded" />
          <FileList 
            :files="files" 
            @deleteFile="handleDeleteFile" 
            @previewFile="handlePreviewFile"
          />
        </aside>

        <!-- 右侧面板：对话窗口 -->
        <section class="right-panel">
          <ChatWindow :files="files" @sendMessage="handleSendMessage" />
        </section>
      </div>
    </main>

    <!-- 预览对话框 -->
    <div v-if="previewFile" class="modal-overlay" @click="previewFile = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ previewFile.name }}</h3>
          <button class="close-btn" @click="previewFile = null">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="isImage(previewFile.type)" class="image-preview">
            <img :src="getFileUrl(previewFile)" :alt="previewFile.name" />
          </div>
          <div v-else-if="isVideo(previewFile.type)" class="video-preview">
            <video :src="getFileUrl(previewFile)" controls></video>
          </div>
          <div v-else-if="isAudio(previewFile.type)" class="audio-preview">
            <audio :src="getFileUrl(previewFile)" controls></audio>
          </div>
          <div v-else-if="isText(previewFile.type)" class="text-preview">
            <pre>{{ textContent || '加载中...' }}</pre>
          </div>
          <div v-else class="unsupported-preview">
            <p>⚠️ 此文件类型不支持预览</p>
            <p class="hint">请下载后查看</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from './components/Header.vue'
import FileUpload from './components/FileUpload.vue'
import FileList from './components/FileList.vue'
import ChatWindow from './components/ChatWindow.vue'

const files = ref([])
const previewFile = ref(null)
const textContent = ref('')

const handleFilesUploaded = (newFiles) => {
  files.value = [...files.value, ...newFiles]
}

const handleDeleteFile = (fileId) => {
  files.value = files.value.filter(file => file.id !== fileId)
}

const handlePreviewFile = async (file) => {
  previewFile.value = file
  
  if (isText(file.type)) {
    try {
      const reader = new FileReader()
      reader.onload = (e) => {
        textContent.value = e.target.result.substring(0, 5000)
      }
      reader.readAsText(file.file)
    } catch (error) {
      textContent.value = '无法读取文件内容'
    }
  }
}

const handleSendMessage = async (message) => {
  // 这里可以调用真实的 AI API
  console.log('用户发送消息:', message)
  console.log('当前文件列表:', files.value)
  
  // 模拟 AI 响应
  return generateMockResponse(message, files.value)
}

const generateMockResponse = (question, allFiles) => {
  const fileCount = allFiles.length
  if (fileCount === 0) {
    return '请先上传文件，我将基于文件内容回答您的问题。'
  }
  
  const fileNames = allFiles.slice(0, 3).map(f => f.name).join(', ')
  const moreText = fileCount > 3 ? ` 等${fileCount}个文件` : ''
  
  return `基于${fileNames}${moreText}的综合分析：\n\n"${question}"是一个很好的问题。\n\n通过对这些文件的研究，我发现：\n\n1. **主要内容**：文件涵盖了多个方面的信息\n2. **关键点**：包含了丰富的数据和案例\n3. **建议**：结合所有文件全面理解\n\n如需更详细的分析，请告诉我具体关注哪个方面。`
}

const getFileUrl = (file) => {
  return URL.createObjectURL(file.file)
}

const isImage = (type) => type && type.startsWith('image/')
const isVideo = (type) => type && type.startsWith('video/')
const isAudio = (type) => type && type.startsWith('audio/')
const isText = (type) => {
  const textTypes = ['text/', 'application/json', 'application/xml', 'markdown', 'html']
  return textTypes.some(t => type && type.includes(t))
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 1rem;
  overflow: hidden;
}

.container {
  display: flex;
  gap: 1rem;
  height: calc(100vh - 100px);
  max-width: 1920px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.left-panel {
  width: 400px;
  min-width: 400px;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止出现双重滚动条 */
  border-right: 1px solid #e2e8f0;
  padding-right: 1rem;
}

.right-panel {
  flex: 1;
  overflow: hidden;
}

/* 预览对话框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  color: #2d3748;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #e53e3e;
}

.modal-body {
  padding: 1.5rem;
}

.image-preview img,
.video-preview video {
  width: 100%;
  max-height: 60vh;
  object-fit: contain;
}

.text-preview pre {
  background: #f7fafc;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 50vh;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
}

.unsupported-preview {
  text-align: center;
  padding: 3rem;
  color: #718096;
}

.hint {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  color: #a0aec0;
}

@media (max-width: 1024px) {
  .container {
    flex-direction: column;
    height: auto;
  }
  
  .left-panel {
    width: 100%;
    min-width: 100%;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
    padding-right: 0;
    padding-bottom: 1rem;
    max-height: 400px;
  }
  
  .right-panel {
    height: 600px;
  }
}
</style>
