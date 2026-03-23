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
          <div 
            class="progress" 
            :style="{ width: file.progress + '%' }"
            :class="{ 'progress-error': file.status === 'error' }"
          ></div>
        </div>
        <span class="progress-text">{{ Math.round(file.progress) }}%</span>
        <span v-if="file.status === 'success'" class="status-icon status-success">✓</span>
        <span v-if="file.status === 'error'" class="status-icon status-error" :title="file.message">✗</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FILE_API } from '../utils/api'

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
    status: 'uploading', // uploading, success, error
    message: '',
    uploadTime: new Date().toLocaleString('zh-CN'),
    filepath: ''
  }))

  uploadingFiles.value = [...uploadingFiles.value, ...newFiles]

  // 真实上传到后端
  for (let i = 0; i < newFiles.length; i++) {
    await uploadToBackend(newFiles[i])
  }

  // 只保留上传成功的文件
  const successFiles = newFiles.filter(f => f.status === 'success')
  
  // 上传完成后通知父组件（只传递成功的文件）
  if (successFiles.length > 0) {
    emit('filesUploaded', successFiles)
  }
  
  // 从上传列表中移除（延迟 2 秒让用户看到结果）
  setTimeout(() => {
    uploadingFiles.value = uploadingFiles.value.filter(
      f => !newFiles.find(nf => nf.id === f.id)
    )
  }, 2000)
}

const uploadToBackend = async (fileObj) => {
  console.log('🚀 [FileUpload.vue] 开始上传文件:', fileObj.name)
  try {
    const formData = new FormData()
    formData.append('file', fileObj.file)

    console.log('📡 [FileUpload.vue] 发送请求到:', FILE_API.UPLOAD)
    
    const response = await fetch(FILE_API.UPLOAD, {
      method: 'POST',
      body: formData
    })

    console.log('📥 [FileUpload.vue] 收到响应状态:', response.status)

    if (!response.ok) {
      const errorData = await response.json()
      console.error('❌ [FileUpload.vue] 后端返回错误:', errorData)
      throw new Error(errorData.detail || '上传失败')
    }

    const result = await response.json()
    console.log('✅ [FileUpload.vue] 上传成功:', result)
    
    fileObj.progress = 100
    fileObj.status = 'success'
    fileObj.message = result.message || '上传成功'
    fileObj.filepath = result.filepath
    
    console.log('✓ [FileUpload.vue] 文件状态已更新:', fileObj.status)
    
  } catch (error) {
    console.error('❌ [FileUpload.vue] 上传失败:', error)
    fileObj.progress = 0
    fileObj.status = 'error'
    fileObj.message = error.message || '上传失败'
  }
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

.status-icon {
  margin-left: 0.5rem;
  font-size: 1rem;
}

.status-success {
  color: #48bb78;
}

.status-error {
  color: #f56565;
}
</style>
