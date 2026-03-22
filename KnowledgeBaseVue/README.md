# 本地知识库 - Vue3 版本

一个基于 Vue3 的本地知识库界面，支持多种文件格式的上传和管理。

## ✨ 功能特性

- 📁 **多格式支持**：支持 PDF、Word、Excel、PPT、TXT、Markdown、HTML、图片、视频、音频等多种文件格式
- 🎨 **拖拽上传**：支持拖拽文件和点击选择文件两种方式
- 📊 **进度显示**：实时显示文件上传进度
- 🔍 **文件搜索**：快速搜索文件名
- 👁️ **在线预览**：支持图片、视频、音频和文本文件的在线预览
- ⬇️ **文件下载**：支持文件下载到本地
- 🗑️ **文件管理**：支持删除已上传文件
- 📱 **响应式设计**：适配各种屏幕尺寸

## 🚀 快速开始

### 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0

### 安装依赖

```bash
cd KnowledgeBaseVue
npm install
```

### 启动开发服务器

```bash
npm run dev
```

浏览器会自动打开 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 📂 支持的文件格式

### 文档类
- PDF (.pdf)
- Word (.doc, .docx)
- Excel (.xls, .xlsx)
- PowerPoint (.ppt, .pptx)
- 文本 (.txt)
- Markdown (.md)
- HTML (.html, .htm)

### 数据类
- JSON (.json)
- XML (.xml)
- CSV (.csv)

### 图片类
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- SVG (.svg)
- WebP (.webp)

### 视频类
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)

### 音频类
- MP3 (.mp3)
- WAV (.wav)
- AAC (.aac)
- WMA (.wma)

### 压缩类
- ZIP (.zip)
- RAR (.rar)
- 7Z (.7z)
- TAR (.tar)
- GZ (.gz)

### 代码类
- Python (.py)
- Java (.java)
- C++ (.cpp, .c)
- JavaScript (.js)
- TypeScript (.ts)
- Vue (.vue)
- CSS (.css, .scss, .less)
- SQL (.sql)
- Shell (.sh)
- Batch (.bat)

### 其他
- 可执行文件 (.exe)
- 库文件 (.dll, .so)

## 🛠️ 技术栈

- **框架**: Vue 3.4+
- **构建工具**: Vite 5+
- **HTTP 客户端**: Axios (预留后端接口)

## 📁 项目结构

```
KnowledgeBaseVue/
├── src/
│   ├── components/
│   │   ├── Header.vue          # 头部组件
│   │   ├── MainContent.vue     # 主内容组件
│   │   ├── FileUpload.vue      # 文件上传组件
│   │   └── FileList.vue        # 文件列表组件
│   ├── App.vue                 # 根组件
│   └── main.js                 # 入口文件
├── index.html                  # HTML 模板
├── vite.config.js              # Vite 配置
└── package.json                # 项目依赖
```

## 💡 使用说明

1. **上传文件**
   - 点击上传区域或拖拽文件到虚线框内
   - 支持一次选择多个文件
   - 上传进度实时显示

2. **查看文件**
   - 所有上传的文件会显示在下方列表中
   - 每个文件卡片显示：图标、名称、大小、上传时间

3. **搜索文件**
   - 在搜索框输入文件名关键词
   - 列表会实时过滤匹配的文件

4. **预览文件**
   - 点击"预览"按钮可查看支持的文件类型
   - 图片、视频、音频直接播放
   - 文本文件显示内容（前 5000 字符）

5. **下载文件**
   - 点击"下载"按钮保存到本地

6. **删除文件**
   - 点击卡片右上角的删除图标
   - 确认后从列表中移除

## 🔌 后端集成（可选）

当前版本为纯前端实现，文件存储在浏览器内存中。如需持久化存储，可以：

1. 在 `FileUpload.vue` 中的 `uploadFiles` 方法中添加 API 调用
2. 使用 Axios 将文件发送到后端服务器
3. 从后端获取文件列表并展示

示例代码（在 FileUpload.vue 中）：

```javascript
const uploadToServer = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  
  return response.data
}
```

## 🎨 自定义样式

修改 `App.vue` 中的全局样式或各组件的局部样式来自定义界面外观。

主要颜色方案：
- 主色：紫色渐变 (#667eea → #764ba2)
- 背景：白色半透明
- 文字：深灰色系

## 📝 注意事项

1. 当前版本文件存储在内存中，刷新页面后文件会丢失
2. 大文件上传可能会占用较多内存
3. 某些特殊格式可能需要额外的解析库才能预览
4. 建议在现代浏览器中使用（Chrome、Firefox、Edge 等）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
