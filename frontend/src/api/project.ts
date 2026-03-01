import apiClient from './client'
import type {
  Project,
  ProjectListResponse,
  ProjectCreateRequest,
  ProjectUpdateRequest,
  ProjectStatusUpdateRequest,
  ProjectFilterParams
} from '@/types/project'

export const projectApi = {
  // 获取项目列表
  getProjects(params?: ProjectFilterParams) {
    return apiClient.get<ProjectListResponse>('/projects/', { params })
  },

  // 创建项目
  createProject(data: ProjectCreateRequest) {
    return apiClient.post<Project>('/projects/', data)
  },

  // 获取项目详情
  getProject(id: number) {
    return apiClient.get<Project>(`/projects/${id}`)
  },

  // 更新项目
  updateProject(id: number, data: ProjectUpdateRequest) {
    return apiClient.put<Project>(`/projects/${id}`, data)
  },

  // 删除项目
  deleteProject(id: number) {
    return apiClient.delete(`/projects/${id}`)
  },

  // 更新项目状态
  updateProjectStatus(id: number, data: ProjectStatusUpdateRequest) {
    return apiClient.put(`/projects/${id}/status`, data)
  },

  // 复制项目
  duplicateProject(id: number) {
    return apiClient.post<Project>(`/projects/${id}/duplicate`)
  }
}

export default projectApi
