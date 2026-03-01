<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { GalleryItem } from '@/services/api'
import { apiService } from '@/services/api'

const props = defineProps<{
  project: GalleryItem
}>()

const emit = defineEmits<{
  (e: 'update', projectId: number): void
}>()

const router = useRouter()

const isLiked = ref(false)
const isFavorited = ref(false)
const localLikeCount = ref(props.project.like_count)
const isLoading = ref(false)

const goToDetail = () => {
  router.push(`/gallery/${props.project.id}`)
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleLike = async (event: Event) => {
  event.stopPropagation()
  if (isLoading.value) return
  
  isLoading.value = true
  try {
    if (isLiked.value) {
      await apiService.unlikeProject(props.project.id)
      localLikeCount.value--
      isLiked.value = false
      ElMessage.success('取消点赞')
    } else {
      await apiService.likeProject(props.project.id)
      localLikeCount.value++
      isLiked.value = true
      ElMessage.success('点赞成功')
    }
    emit('update', props.project.id)
  } catch (error: any) {
    if (error.response?.status === 401) {
      ElMessage.warning('请先登录')
      router.push('/login')
    } else {
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  } finally {
    isLoading.value = false
  }
}

const handleFavorite = async (event: Event) => {
  event.stopPropagation()
  if (isLoading.value) return
  
  isLoading.value = true
  try {
    if (isFavorited.value) {
      await apiService.unfavoriteProject(props.project.id)
      isFavorited.value = false
      ElMessage.success('取消收藏')
    } else {
      await apiService.favoriteProject(props.project.id)
      isFavorited.value = true
      ElMessage.success('收藏成功')
    }
    emit('update', props.project.id)
  } catch (error: any) {
    if (error.response?.status === 401) {
      ElMessage.warning('请先登录')
      router.push('/login')
    } else {
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  } finally {
    isLoading.value = false
  }
}

const handleComment = (event: Event) => {
  event.stopPropagation()
  router.push(`/gallery/${props.project.id}#comments`)
}
</script>

<template>
  <el-card class="project-card card-hover" :body-style="{ padding: 0 }" @click="goToDetail">
    <div class="card-thumbnail">
      <img
        v-if="project.thumbnail_url"
        :src="project.thumbnail_url"
        :alt="project.name"
        @error="($event.target as HTMLImageElement).style.display = 'none'"
      />
      <div v-else class="thumbnail-placeholder">
        <el-icon :size="48"><Picture /></el-icon>
      </div>
      <!-- 悬浮操作按钮 -->
      <div class="card-actions">
        <el-button
          circle
          :type="isLiked ? 'danger' : 'info'"
          :loading="isLoading"
          @click="handleLike"
          class="action-btn"
        >
          <el-icon><StarFilled v-if="isLiked" /><Star v-else /></el-icon>
        </el-button>
        <el-button
          circle
          :type="isFavorited ? 'warning' : 'info'"
          :loading="isLoading"
          @click="handleFavorite"
          class="action-btn"
        >
          <el-icon><Collection v-if="isFavorited" /><CollectionTag v-else /></el-icon>
        </el-button>
      </div>
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ project.name }}</h3>
      <p class="card-description" v-if="project.description">
        {{ project.description }}
      </p>
      <div class="card-author">
        <el-avatar :size="24" :src="project.author.avatar_url || undefined">
          {{ project.author.username.charAt(0).toUpperCase() }}
        </el-avatar>
        <span class="author-name">{{ project.author.username }}</span>
      </div>
      <div class="card-stats">
        <span class="stat-item" @click="goToDetail">
          <el-icon><View /></el-icon>
          {{ project.view_count }}
        </span>
        <span class="stat-item" :class="{ 'is-active': isLiked }" @click="handleLike">
          <el-icon><StarFilled v-if="isLiked" /><Star v-else /></el-icon>
          {{ localLikeCount }}
        </span>
        <span class="stat-item" @click="handleComment">
          <el-icon><ChatDotRound /></el-icon>
          {{ project.comment_count || 0 }}
        </span>
        <span class="stat-item" :class="{ 'is-active': isFavorited }" @click="handleFavorite">
          <el-icon><Collection v-if="isFavorited" /><CollectionTag v-else /></el-icon>
          {{ project.favorite_count || 0 }}
        </span>
      </div>
      <div class="card-tags" v-if="project.tags && project.tags.length > 0">
        <el-tag
          v-for="tag in project.tags.slice(0, 3)"
          :key="tag"
          size="small"
          type="info"
          effect="plain"
        >
          {{ tag }}
        </el-tag>
      </div>
      <div class="card-date">
        {{ formatDate(project.created_at) }}
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.project-card {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.card-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #f0f2f5;
  position: relative;
}

.card-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.project-card:hover .card-thumbnail img {
  transform: scale(1.05);
}

.thumbnail-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.card-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}

.project-card:hover .card-actions {
  opacity: 1;
  transform: translateY(0);
}

.action-btn {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-description {
  font-size: 13px;
  color: #909399;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

.card-author {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.author-name {
  font-size: 13px;
  color: #606266;
}

.card-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
  cursor: pointer;
  transition: color 0.2s;
}

.stat-item:hover {
  color: #409eff;
}

.stat-item.is-active {
  color: #f56c6c;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.card-date {
  font-size: 12px;
  color: #c0c4cc;
}
</style>
