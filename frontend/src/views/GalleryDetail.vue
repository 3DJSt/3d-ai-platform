<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { apiService, type GalleryDetailResponse } from '@/services/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const project = ref<GalleryDetailResponse | null>(null)

const fetchProject = async () => {
  const id = Number(route.params.id)
  if (!id) {
    ElMessage.error('无效的项目ID')
    router.push('/gallery')
    return
  }

  loading.value = true
  try {
    project.value = await apiService.getGalleryDetail(id)
  } catch (error) {
    console.error('获取项目详情失败:', error)
    ElMessage.error('项目不存在或未公开')
    router.push('/gallery')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const goBack = () => {
  router.push('/gallery')
}

onMounted(() => {
  fetchProject()
})
</script>

<template>
  <div class="gallery-detail-page">
    <div class="container">
      <div v-loading="loading" class="detail-content">
        <template v-if="project">
          <div class="back-button">
            <el-button @click="goBack">
              <el-icon><ArrowLeft /></el-icon>
              返回画廊
            </el-button>
          </div>

          <div class="project-header">
            <h1 class="project-title">{{ project.name }}</h1>
            <div class="project-meta">
              <div class="author-info">
                <el-avatar :size="40" :src="project.author.avatar_url || undefined">
                  {{ project.author.username.charAt(0).toUpperCase() }}
                </el-avatar>
                <div class="author-details">
                  <span class="author-name">{{ project.author.username }}</span>
                  <span class="create-date">{{ formatDate(project.created_at) }}</span>
                </div>
              </div>
              <div class="project-stats">
                <span class="stat-item">
                  <el-icon><View /></el-icon>
                  {{ project.view_count }} 次浏览
                </span>
                <span class="stat-item">
                  <el-icon><Star /></el-icon>
                  {{ project.like_count }} 次点赞
                </span>
              </div>
            </div>
          </div>

          <div class="project-thumbnail" v-if="project.thumbnail_url">
            <img :src="project.thumbnail_url" :alt="project.name" />
          </div>
          <div class="project-thumbnail placeholder" v-else>
            <el-icon :size="80"><Picture /></el-icon>
            <span>暂无预览图</span>
          </div>

          <div class="project-info-card">
            <div class="info-section" v-if="project.description">
              <h3>项目描述</h3>
              <p>{{ project.description }}</p>
            </div>

            <div class="info-section" v-if="project.tags && project.tags.length > 0">
              <h3>标签</h3>
              <div class="tags-list">
                <el-tag v-for="tag in project.tags" :key="tag" size="large">
                  {{ tag }}
                </el-tag>
              </div>
            </div>

            <div class="info-section">
              <h3>项目信息</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">状态</span>
                  <el-tag type="success">{{ project.status }}</el-tag>
                </div>
                <div class="info-item">
                  <span class="info-label">创建时间</span>
                  <span>{{ formatDate(project.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">更新时间</span>
                  <span>{{ formatDate(project.updated_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gallery-detail-page {
  min-height: calc(100vh - 104px);
  padding: 24px 0;
}

.detail-content {
  max-width: 900px;
  margin: 0 auto;
}

.back-button {
  margin-bottom: 24px;
}

.project-header {
  margin-bottom: 24px;
}

.project-title {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 16px;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.create-date {
  font-size: 13px;
  color: #909399;
}

.project-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.project-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
  background: #f0f2f5;
}

.project-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.project-thumbnail.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.project-info-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.info-section {
  margin-bottom: 24px;
}

.info-section:last-child {
  margin-bottom: 0;
}

.info-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.info-section p {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-label {
  font-size: 14px;
  color: #909399;
}

@media (max-width: 768px) {
  .project-title {
    font-size: 22px;
  }

  .project-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .project-stats {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
