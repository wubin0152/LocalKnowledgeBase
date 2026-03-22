<template>
  <main class="main-content">
    <div class="container">
      <!-- 左侧：上传区域 -->
      <div class="left-panel">
        <FileUpload @filesUploaded="handleFilesUploaded" />
        <FileList :files="files" @deleteFile="handleDeleteFile" @fileSelected="handleFileSelected" />
      </div>

      <!-- 右侧：总对话窗口 -->
      <div class="right-panel">
        <ChatWindow :files="files" />
      </div>
```

MainContent.vue
```vue
<<<<<<< SEARCH
import { ref } from 'vue'
import FileUpload from './FileUpload.vue'
import FileList from './FileList.vue'
import ChatWindow from './ChatWindow.vue'

const files = ref([])
const selectedFile = ref(null)

const handleFilesUploaded = (newFiles) => {
  files.value = [...files.value, ...newFiles]
}

const handleDeleteFile = (fileId) => {
  files.value = files.value.filter(file => file.id !== fileId)
  if (selectedFile.value && selectedFile.value.id === fileId) {
    selectedFile.value = null
  }
}

const handleFileSelected = (file) => {
  selectedFile.value = file
}
import { ref } from 'vue'
import FileUpload from './FileUpload.vue'
import FileList from './FileList.vue'
import ChatWindow from './ChatWindow.vue'

const files = ref([])

const handleFilesUploaded = (newFiles) => {
  files.value = [...files.value, ...newFiles]
}

const handleDeleteFile = (fileId) => {
  files.value = files.value.filter(file => file.id !== fileId)
}

const handleFileSelected = (file) => {
  // 不再需要单个文件选择，保留用于其他用途
  console.log('File selected:', file)
}
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import FileUpload from './FileUpload.vue'
import FileList from './FileList.vue'
import ChatWindow from './ChatWindow.vue'

const files = ref([])
const selectedFile = ref(null)

const handleFilesUploaded = (newFiles) => {
  files.value = [...files.value, ...newFiles]
}

const handleDeleteFile = (fileId) => {
  files.value = files.value.filter(file => file.id !== fileId)
  if (selectedFile.value && selectedFile.value.id === fileId) {
    selectedFile.value = null
  }
}

const handleFileSelected = (file) => {
  selectedFile.value = file
}
</script>

<style scoped>
.main-content {
  flex: 1;
  padding: 1rem;
  max-width: 1920px;
  margin: 0 auto;
  width: 100%;
}

.container {
  display: flex;
  gap: 1rem;
  height: calc(100vh - 140px);
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.left-panel {
  width: 400px;
  min-width: 400px;
  overflow-y: auto;
  border-right: 1px solid #e2e8f0;
  padding-right: 1rem;
}

.right-panel {
  flex: 1;
  overflow: hidden;
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
  }
  
  .right-panel {
    height: 600px;
  }
}
</style>
