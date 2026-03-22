<template>
  <div class="file-list">
    <div v-if="files.length === 0" class="empty-state">
      <div class="empty-icon">📂</div>
      <p>暂无文件，请上传</p>
      <p class="hint">上传后可以与所有文件对话</p>
    </div>

    <div v-else>
      <h3 class="list-title">知识库文件 ({{ files.length }})</h3>
      
      <!-- 搜索框 -->
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="🔍 搜索文件名..."
          class="search-input"
        />
      </div>

      <div class="files-list">
        <div 
          v-for="file in filteredFiles" 
          :key="file.id" 
          class="file-item"
        >
          <div class="file-item-header">
            <span class="file-icon">{{ getFileIcon(file.type) }}</span>
            <div class="file-item-info">
              <h4 class="file-name" :title="file.name">{{ file.name }}</h4>
              <p class="file-meta">{{ formatFileSize(file.size) }}</p>
            </div>
          </div>
          
          <div class="file-item-actions">
            <button 
              class="action-btn-small preview" 
              @click.stop="handlePreview(file)"
              title="预览"
            >
              👁️
            </button>
            <button 
              class="action-btn-small download" 
              @click.stop="handleDownload(file)"
              title="下载"
            >
              ⬇️
            </button>
            <button 
              class="action-btn-small delete" 
              @click.stop="handleDelete(file.id)"
              title="删除"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- 批量操作提示 -->
      <div class="batch-hint">
        <p>💡 已上传 <strong>{{ files.length }}</strong> 个文件</p>
        <p>可以在右侧与<strong>所有文件</strong>进行对话</p>
      </div>
    </div>

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
            <p class="hint-modal">请下载后查看</p>
          </div>
        </div>
      </div>
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

const emit = defineEmits(['deleteFile', 'previewFile'])

const searchQuery = ref('')
const previewFile = ref(null)
const textContent = ref('')

const filteredFiles = computed(() => {
  if (!searchQuery.value) return props.files
  
  return props.files.filter(file => 
    file.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const getFileIcon = (type) => {
  if (!type) return '📄'
  
  const icons = {
    'pdf': '📕',
    'word': '📘',
    'excel': '📊',
    'powerpoint': '📊',
    'image': '🖼️',
    'video': '🎬',
    'audio': '🎵',
    'text': '📝',
    'code': '💻',
    'archive': '📦'
  }
  
  for (const [key, icon] of Object.entries(icons)) {
    if (type.includes(key)) return icon
  }
  
  return '📄'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateTimeStr) => {
  try {
    const date = new Date(dateTimeStr)
    return date.toLocaleDateString('zh-CN', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateTimeStr
  }
}

const handleDelete = (fileId) => {
  if (confirm('确定要删除这个文件吗？')) {
    emit('deleteFile', fileId)
  }
}

const handlePreview = (file) => {
  emit('previewFile', file)
}

const handleDownload = (file) => {
  const url = getFileUrl(file)
  const a = document.createElement('a')
  a.href = url
  a.download = file.name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

</script>

<style scoped>
.file-list-container {
  flex: 1;
  overflow-y: auto;
  margin-top: 1rem;
  min-height: 0; /* 关键：让 flex 子项正确滚动 */
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #a0aec0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.hint {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  color: #cbd5e0;
}

.list-title {
  color: #2d3748;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #667eea;
  flex-shrink: 0; /* 防止标题被压缩 */
}

.search-box {
  margin-bottom: 1rem;
  flex-shrink: 0; /* 防止搜索框被压缩 */
}

.search-input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box; /* 确保 padding 不增加总宽度 */
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  /* 移除固定高度限制，让内容自然撑开 */
  /* overflow-y: auto; */
  min-height: 0; /* 关键：让 flex 子项正确滚动 */
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0; /* 防止文件项被压缩 */
}

.file-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateX(2px);
}

.file-item-header {
  display: flex;
  align-items: center;
  flex: 1;
  overflow: hidden;
  min-width: 0; /* 关键：允许文本溢出处理 */
}

.file-icon {
  font-size: 2rem;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.file-item-info {
  flex: 1;
  overflow: hidden;
  min-width: 0; /* 关键：允许文本溢出处理 */
}

.file-name {
  color: #2d3748;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.file-meta {
  color: #718096;
  font-size: 0.75rem;
}

.file-item-actions {
  display: flex;
  gap: 0.4rem;
  flex-shrink: 0;
}

.action-btn-small {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.download {
  background: #edf2f7;
  color: #4a5568;
}

.delete {
  background: #fed7d7;
  color: #e53e3e;
}

.action-btn-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.batch-hint {
  margin-top: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 8px;
  border-left: 4px solid #667eea;
  flex-shrink: 0; /* 防止提示框被压缩 */
}

.batch-hint p {
  margin: 0.25rem 0;
  color: #4a5568;
  font-size: 0.9rem;
}

.batch-hint strong {
  color: #667eea;
  font-weight: 600;
}

/* 优化滚动条样式 - 更细更优雅 */
.file-list-container::-webkit-scrollbar {
  width: 6px;
}

.file-list-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.file-list-container::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.file-list-container::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

.files-list::-webkit-scrollbar {
  width: 6px;
}

.files-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.files-list::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.files-list::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style>
