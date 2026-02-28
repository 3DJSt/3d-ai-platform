<template>
  <div class="file-uploader">
    <!-- 拖拽区域 -->
    <div
      class="drop-zone"
      :class="{ dragover: isDragover, 'has-files': uploadedFiles.length > 0 }"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <div v-if="uploadedFiles.length === 0" class="upload-prompt">
        <div class="upload-icon">📁</div>
        <p class="prompt-text">拖拽文件到这里，或点击选择文件</p>
        <p class="file-types">支持 .obj, .fbx, .gltf, .glb 格式</p>
        <p class="file-limit">最大文件大小：{{ maxSizeMB }}MB</p>
      </div>

      <!-- 文件列表 -->
      <div v-else class="file-list">
        <div
          v-for="(file, index) in uploadedFiles"
          :key="index"
          class="file-item"
        >
          <div class="file-info">
            <span class="file-icon">📄</span>
            <div class="file-details">
              <p class="file-name">{{ file.name }}</p>
              <p class="file-size">{{ formatFileSize(file.size) }}</p>
            </div>
          </div>
          <div class="file-actions">
            <!-- 上传进度 -->
            <div v-if="file.status === 'uploading'" class="upload-progress">
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: file.progress + '%' }"
                ></div>
              </div>
              <span class="progress-text">{{ file.progress }}%</span>
            </div>

            <!-- 状态图标 -->
            <div v-else class="status-icons">
              <span v-if="file.status === 'success'" class="success-icon">✅</span>
              <span v-if="file.status === 'error'" class="error-icon">❌</span>
              <button
                v-if="file.status !== 'uploading'"
                @click.stop="removeFile(index)"
                class="remove-btn"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 隐藏的文件输入 -->
    <input
      ref="fileInput"
      type="file"
      :accept="acceptExtensions"
      :multiple="multiple"
      @change="handleFileSelect"
      style="display: none"
    />

    <!-- 上传按钮 -->
    <div v-if="uploadedFiles.length > 0" class="upload-actions">
      <button @click="uploadFiles" :disabled="isUploading" class="upload-btn">
        {{ isUploading ? '上传中...' : '开始上传' }}
      </button>
      <button @click="clearFiles" class="clear-btn">清空列表</button>
    </div>

    <!-- 错误信息 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import type { UploadResponse } from '@/types'

interface Props {
  accept?: string
  maxSize?: number // 字节
  multiple?: boolean
  endpoint?: string
}

const props = withDefaults(defineProps<Props>(), {
  accept: '.obj,.fbx,.gltf,.glb',
  maxSize: 100 * 1024 * 1024, // 100MB
  multiple: true,
  endpoint: '/api/v1/files/upload'
})

interface UploadFile {
  file: File
  name: string
  size: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  progress: number
  response?: UploadResponse
}

const fileInput = ref<HTMLInputElement>()
const uploadedFiles = ref<UploadFile[]>([])
const isDragover = ref(false)
const isUploading = ref(false)
const errorMessage = ref('')

const maxSizeMB = computed(() => Math.round(props.maxSize / (1024 * 1024)))
const acceptExtensions = computed(() => props.accept.split(',').map(ext => ext.trim()).join(','))

const emit = defineEmits<{
  'upload-success': [data: { file: File; response: UploadResponse; index: number }]
  'upload-complete': [responses: UploadResponse[]]
}>()

// 触发文件选择
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// 处理文件选择
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    processFiles(Array.from(target.files))
  }
  target.value = '' // 重置 input
}

// 处理拖拽
const handleDragOver = (event: DragEvent) => {
  isDragover.value = true
  event.preventDefault()
}

const handleDragLeave = () => {
  isDragover.value = false
}

const handleDrop = (event: DragEvent) => {
  isDragover.value = false
  if (event.dataTransfer?.files) {
    processFiles(Array.from(event.dataTransfer.files))
  }
}

// 处理文件验证
const processFiles = (files: File[]) => {
  errorMessage.value = ''

  for (const file of files) {
    // 验证文件大小
    if (file.size > props.maxSize) {
      errorMessage.value = `文件 "${file.name}" 超过${maxSizeMB.value}MB限制`
      continue
    }

    // 验证文件类型
    const extension = file.name.split('.').pop()?.toLowerCase() || ''
    const acceptedExtensions = props.accept
      .split(',')
      .map(ext => ext.replace('.', '').toLowerCase().trim())

    if (!acceptedExtensions.includes(extension)) {
      errorMessage.value = `不支持的文件类型：.${extension}`
      continue
    }

    // 添加到上传列表
    uploadedFiles.value.push({
      file,
      name: file.name,
      size: file.size,
      status: 'pending',
      progress: 0
    })
  }
}

// 上传文件
const uploadFiles = async () => {
  if (uploadedFiles.value.length === 0) return

  isUploading.value = true
  const uploadedResponses: UploadResponse[] = []

  for (let i = 0; i < uploadedFiles.value.length; i++) {
    const uploadFile = uploadedFiles.value[i]

    if (uploadFile.status === 'success') {
      if (uploadFile.response) uploadedResponses.push(uploadFile.response)
      continue
    }

    uploadFile.status = 'uploading'

    const formData = new FormData()
    formData.append('file', uploadFile.file)
    formData.append('type', 'model')

    try {
      const response = await axios.post<{ success: boolean; data: UploadResponse }>(
        props.endpoint,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
              uploadFile.progress = progress
            }
          }
        }
      )

      if (response.data.success) {
        uploadFile.status = 'success'
        uploadFile.response = response.data.data
        uploadedResponses.push(response.data.data)

        emit('upload-success', {
          file: uploadFile.file,
          response: response.data.data,
          index: i
        })
      } else {
        throw new Error('上传失败：服务器返回错误')
      }
    } catch (error: unknown) {
      uploadFile.status = 'error'
      if (error instanceof Error) {
        errorMessage.value = `上传失败: ${error.message}`
      } else {
        errorMessage.value = '上传失败：未知错误'
      }
      console.error('文件上传错误:', error)
    }
  }

  isUploading.value = false

  // 如果所有文件都上传成功，触发完成事件
  const allSuccess = uploadedFiles.value.every(file => file.status === 'success')
  if (allSuccess) {
    emit('upload-complete', uploadedResponses)
  }
}

// 辅助函数
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const removeFile = (index: number) => {
  uploadedFiles.value.splice(index, 1)
}

const clearFiles = () => {
  uploadedFiles.value = []
  errorMessage.value = ''
}

defineExpose({ clearFiles, getUploadedFiles: () => uploadedFiles.value })
</script>

<style scoped>
.file-uploader {
  width: 100%;
}
.drop-zone {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.drop-zone.dragover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}
.drop-zone.has-files {
  padding: 1.5rem;
  justify-content: flex-start;
}
.upload-prompt .upload-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
.prompt-text {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 0.5rem;
}
.file-types {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}
.file-limit {
  color: #999;
  font-size: 0.8rem;
}
.file-list {
  width: 100%;
}
.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}
.file-icon {
  font-size: 1.5rem;
}
.file-details {
  flex: 1;
}
.file-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.25rem;
  word-break: break-all;
}
.file-size {
  color: #666;
  font-size: 0.9rem;
}
.file-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.upload-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 150px;
}
.progress-bar {
  flex: 1;
  height: 6px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.3s;
}
.progress-text {
  font-size: 0.9rem;
  color: #666;
  min-width: 40px;
  text-align: right;
}
.status-icons {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.success-icon {
  color: #52c41a;
}
.error-icon {
  color: #ff4d4f;
}
.remove-btn {
  background: #ff4d4f;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}
.upload-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}
.upload-btn,
.clear-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  border: none;
}
.upload-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}
.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.clear-btn {
  background: #f0f0f0;
  color: #666;
}
.error-message {
  margin-top: 1rem;
  color: #ff4d4f;
  font-size: 0.9rem;
}
</style>