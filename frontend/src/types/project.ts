export interface ModelData {
  model: string | null
  textures: string[]
  skeleton: string | null
  animations: string[]
  render_settings: Record<string, any>
}

export interface StoragePaths {
  minio_bucket: string
  model_key: string | null
  texture_keys: string[]
  animation_keys: string[]
}

export interface Project {
  id: number
  name: string
  description: string | null
  user_id: number
  status: 'draft' | 'processing' | 'completed' | 'archived'
  model_data: ModelData
  storage_paths: StoragePaths
  created_at: string
  updated_at: string
}

export interface ProjectListResponse {
  items: Project[]
  total: number
  page: number
  page_size: number
}

export interface ProjectCreateRequest {
  name: string
  description?: string
}

export interface ProjectUpdateRequest {
  name?: string
  description?: string
}

export interface ProjectStatusUpdateRequest {
  status: 'draft' | 'processing' | 'completed' | 'archived'
}

export interface ProjectFilterParams {
  status?: string
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  page?: number
  page_size?: number
}

export const ProjectStatusMap: Record<string, { label: string; type: string }> = {
  draft: { label: '草稿', type: 'info' },
  processing: { label: '处理中', type: 'warning' },
  completed: { label: '已完成', type: 'success' },
  archived: { label: '已归档', type: 'info' }
}
