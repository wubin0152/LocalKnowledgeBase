<template>
  <div class="file-upload">
    <div 
      class="upload-area"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
      :class="{ dragging: isDragging }"
    >
      <div class="upload-icon">📁</div>
      <h3>拖拽文件到此处或点击上传</h3>
      <p class="supported-formats">
        支持格式：PDF, Word, Excel, PPT, TXT, Markdown, HTML, 图片，视频，音频等
      </p>
      <input
        ref="fileInput"
        type="file"
        multiple
        :accept="acceptedFormats"
        @change="handleFileSelect"
        style="display: none"
      />
    </div>

    <div v-if="uploadingFiles.length > 0" class="uploading-list">
      <div v-for="file in uploadingFiles" :key="file.name" class="upload-item">
        <span class="file-name">{{ file.name }}</span>
        <div class="progress-bar">
          <div class="progress" :style="{ width: file.progress + '%' }"></div>
        </div>
        <span class="progress-text">{{ Math.round(file.progress) }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['filesUploaded'])
const fileInput = ref(null)
const isDragging = ref(false)
const uploadingFiles = ref([])

// 支持的格式
const acceptedFormats = '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.md,.html,.htm,.xml,.json,.csv,.png,.jpg,.jpeg,.gif,.bmp,.svg,.webp,.mp4,.avi,.mov,.wmv,.flv,.mp3,.wav,.aac,.wma,.zip,.rar,.7z,.tar,.gz,.py,.java,.cpp,.c,.js,.ts,.vue,.react,.css,.scss,.less,.sql,.sh,.bat,.exe,.dll,.so'

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  uploadFiles(selectedFiles)
  event.target.value = '' // 清空 input
}

const handleDrop = (event) => {
  isDragging.value = false
  const droppedFiles = Array.from(event.dataTransfer.files)
  uploadFiles(droppedFiles)
}

const uploadFiles = async (filesArray) => {
  if (filesArray.length === 0) return

  const newFiles = filesArray.map(file => ({
    id: Date.now() + Math.random(),
    name: file.name,
    size: file.size,
    type: file.type,
    file: file,
    progress: 0,
    uploadTime: new Date().toLocaleString('zh-CN')
  }))

  uploadingFiles.value = [...uploadingFiles.value, ...newFiles]

  // 模拟上传进度
  for (let i = 0; i < newFiles.length; i++) {
    await simulateUpload(newFiles[i])
  }

  // 上传完成后通知父组件
  emit('filesUploaded', newFiles)
  
  // 从上传列表中移除
  uploadingFiles.value = uploadingFiles.value.filter(
    f => !newFiles.find(nf => nf.id === f.id)
  )
}

const simulateUpload = (file) => {
  return new Promise((resolve) => {
    let progress = 0
    const interval = setInterval(() => {
      progress += Math.random() * 20
      if (progress >= 100) {
        progress = 100
        clearInterval(interval)
        resolve()
      }
      file.progress = Math.min(progress, 100)
    }, 200)
  })
}

</script>

<style scoped>
.file-upload {
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.upload-area {
  border: 2px dashed #667eea;
  border-radius: 8px;
  padding: 1.5rem 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(102, 126, 234, 0.05);
}

.upload-area:hover,
.upload-area.dragging {
  border-color: #764ba2;
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.upload-area h3 {
  color: #4a5568;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.supported-formats {
  color: #718096;
  font-size: 0.8rem;
  line-height: 1.4;
}

.uploading-list {
  margin-top: 1rem;
}

.upload-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  background: #f7fafc;
  border-radius: 6px;
  margin-bottom: 0.4rem;
}

.file-name {
  flex: 1;
  color: #2d3748;
  font-weight: 500;
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.progress-bar {
  width: 120px;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
  margin: 0 0.75rem;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
}

.progress-text {
  color: #667eea;
  font-weight: 600;
  font-size: 0.8rem;
  min-width: 35px;
}
</style>
