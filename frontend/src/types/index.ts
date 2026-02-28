// 模板类型
export interface Template {
  id: number
  name: string
  preview: string
}

// 文件上传响应
export interface UploadResponse {
  file_id: string
  url: string
  stored_name: string
  size: number
  mime_type: string
}

// AI 生成任务
export interface GenerateTask {
  taskId: string
  status: 'processing' | 'completed' | 'failed'
  estimatedTime?: number
}

// 项目模型（可根据后端接口扩展）
export interface Project {
  id: string
  name: string
  description?: string
  status: 'draft' | 'processing' | 'completed' | 'archived'
  createdAt: string
  updatedAt: string
}

// 其他类型（可根据需要添加）