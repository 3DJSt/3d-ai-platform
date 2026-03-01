import client from '../api/client'
import type { AxiosResponse } from 'axios'

interface GalleryParams {
  page?: number
  page_size?: number
  search?: string
  tag?: string
  sort_by?: string
  sort_order?: string
}

interface GalleryItem {
  id: number
  name: string
  description: string | null
  thumbnail_url: string | null
  author: {
    id: number
    username: string
    avatar_url: string | null
  }
  view_count: number
  like_count: number
  comment_count?: number
  favorite_count?: number
  tags: string[]
  created_at: string
  status: string
}

interface GalleryListResponse {
  items: GalleryItem[]
  total: number
  page: number
  page_size: number
}

interface GalleryDetailResponse {
  id: number
  name: string
  description: string | null
  thumbnail_url: string | null
  author: {
    id: number
    username: string
    avatar_url: string | null
  }
  view_count: number
  like_count: number
  tags: string[]
  model_data: Record<string, unknown>
  created_at: string
  updated_at: string
  status: string
}

interface TagResponse {
  tags: Array<{
    name: string
    count: number
  }>
}

// 交互相关接口
interface CommentAuthor {
  id: number
  username: string
  avatar_url: string | null
}

interface Comment {
  id: number
  user_id: number
  project_id: number
  content: string
  parent_id: number | null
  author: CommentAuthor
  created_at: string
  updated_at: string | null
  replies: Comment[]
}

interface CommentListResponse {
  items: Comment[]
  total: number
  page: number
  page_size: number
}

interface ProjectInteractionStats {
  project_id: number
  like_count: number
  comment_count: number
  favorite_count: number
  is_liked: boolean
  is_favorited: boolean
}

class ApiService {
  // 画廊相关
  async getGalleryList(params: GalleryParams = {}): Promise<GalleryListResponse> {
    const response: AxiosResponse<GalleryListResponse> = await client.get('/gallery/', { params })
    return response.data
  }

  async getGalleryDetail(id: number): Promise<GalleryDetailResponse> {
    const response: AxiosResponse<GalleryDetailResponse> = await client.get(`/gallery/${id}`)
    return response.data
  }

  async getPopularTags(limit: number = 20): Promise<TagResponse> {
    const response: AxiosResponse<TagResponse> = await client.get('/gallery/tags/list', {
      params: { limit }
    })
    return response.data
  }

  // 点赞相关
  async likeProject(projectId: number) {
    const response = await client.post('/interactions/like', { project_id: projectId })
    return response.data
  }

  async unlikeProject(projectId: number) {
    const response = await client.delete(`/interactions/like/${projectId}`)
    return response.data
  }

  // 评论相关
  async createComment(projectId: number, content: string, parentId?: number) {
    const response = await client.post('/interactions/comment', {
      project_id: projectId,
      content,
      parent_id: parentId
    })
    return response.data
  }

  async getProjectComments(projectId: number, page: number = 1, pageSize: number = 20): Promise<CommentListResponse> {
    const response: AxiosResponse<CommentListResponse> = await client.get(`/interactions/comments/${projectId}`, {
      params: { page, page_size: pageSize }
    })
    return response.data
  }

  async deleteComment(commentId: number) {
    const response = await client.delete(`/interactions/comment/${commentId}`)
    return response.data
  }

  // 收藏相关
  async favoriteProject(projectId: number) {
    const response = await client.post('/interactions/favorite', { project_id: projectId })
    return response.data
  }

  async unfavoriteProject(projectId: number) {
    const response = await client.delete(`/interactions/favorite/${projectId}`)
    return response.data
  }

  async getUserFavorites() {
    const response = await client.get('/interactions/favorites')
    return response.data
  }

  // 交互统计
  async getProjectInteractionStats(projectId: number): Promise<ProjectInteractionStats> {
    const response: AxiosResponse<ProjectInteractionStats> = await client.get(`/interactions/stats/${projectId}`)
    return response.data
  }
}

export const apiService = new ApiService()
export type { 
  GalleryItem, 
  GalleryListResponse, 
  GalleryDetailResponse, 
  GalleryParams,
  Comment,
  CommentListResponse,
  ProjectInteractionStats
}
