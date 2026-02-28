import axios from 'axios'
import type { UploadResponse, GenerateTask, Project } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000
})

// 请求拦截器（添加 token）
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器（统一处理）
api.interceptors.response.use(
  (response) => {
    if (response.data.success) {
      return response.data.data
    }
    return Promise.reject(response.data.message || '请求失败')
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 健康检查
export const healthApi = {
  check: (): Promise<{ status: string }> => api.get('/v1/health')
}

// 文件上传
export const uploadApi = {
  upload: (file: File, type = 'model'): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('type', type)
    return api.post('/v1/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

// AI 白模生成
export const aiModelApi = {
  generate: (data: {
    prompt: string
    style_tags?: string[]
    negative_prompt?: string
    num_outputs?: number
    quality?: 'standard' | 'high' | 'premium'
  }): Promise<{ taskId: string; status: string; estimatedTime: number }> =>
    api.post('/v1/ai/models/generate', data),

  checkStatus: (taskId: string): Promise<{ status: string; progress?: number; outputs?: any[] }> =>
    api.get(`/v1/ai/models/status/${taskId}`)
}

// 渲染模块
export const renderApi = {
  getMaterials: (): Promise<any[]> => api.get('/v1/render/materials'),
  applyRender: (data: any): Promise<any> => api.post('/v1/render/apply', data)
}

// 骨骼绑定
export const bindingApi = {
  autoBind: (modelId: string): Promise<any> => api.post('/v1/binding/auto', { model_id: modelId }),
  manualBind: (data: any): Promise<any> => api.post('/v1/binding/manual', data)
}

// 动作生成
export const animationApi = {
  getLibrary: (): Promise<any[]> => api.get('/v1/animations/library'),
  generate: (data: any): Promise<any> => api.post('/v1/animations/generate', data)
}

// 项目相关
export const projectApi = {
  list: (): Promise<Project[]> => api.get('/v1/projects'),
  create: (data: { name: string; description?: string; templateId?: string }): Promise<Project> =>
    api.post('/v1/projects', data),
  get: (id: string): Promise<Project> => api.get(`/v1/projects/${id}`),
  update: (id: string, data: Partial<Project>): Promise<Project> => api.put(`/v1/projects/${id}`, data),
  delete: (id: string): Promise<void> => api.delete(`/v1/projects/${id}`)
}