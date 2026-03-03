<template>
  <div class="gallery-project-detail-view">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div 
        v-for="(bubble, index) in bubbles" 
        :key="index"
        class="bubble"
        :style="{
          left: bubble.x + '%',
          animationDuration: bubble.duration + 's',
          animationDelay: bubble.delay + 's',
          width: bubble.size + 'px',
          height: bubble.size + 'px'
        }"
      >
        <svg viewBox="0 0 100 100" class="silhouette" :class="bubble.type">
          <component :is="getSilhouette(bubble.type)" />
        </svg>
      </div>
    </div>

    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-buttons">
        <el-button @click="goHome">
          <el-icon><House /></el-icon>返回主页
        </el-button>
        <el-button @click="goBack">
          <el-icon><ArrowLeft /></el-icon>返回画廊
        </el-button>
      </div>
      <h1 class="page-title">{{ project?.name }}</h1>
    </div>

    <!-- 项目详情 -->
    <div v-loading="loading" class="project-detail">
      <!-- 项目信息 -->
      <div v-if="project" class="project-info">
        <div class="project-header">
          <div class="project-meta">
            <span class="project-author">作者: <span class="author-name" @click="handleViewAuthor">{{ project.username || project.user_id }}</span></span>
            <span class="project-date">{{ formatDate(project.created_at) }}</span>
          </div>
          <div class="project-actions">
            <el-button 
              :type="isLiked ? 'primary' : 'default'" 
              @click="handleLike"
              :loading="actionLoading"
            >
              <el-icon><Star /></el-icon>{{ isLiked ? '已点赞' : '点赞' }}
            </el-button>
            <el-button 
              :type="isFavorited ? 'primary' : 'default'" 
              @click="handleFavorite"
              :loading="actionLoading"
            >
              <el-icon><Collection /></el-icon>{{ isFavorited ? '已收藏' : '收藏' }}
            </el-button>
            <el-button 
              type="success" 
              @click="handleDownload"
              :loading="actionLoading"
              :disabled="!project.allow_download"
            >
              <el-icon><Download /></el-icon>下载
            </el-button>
          </div>
        </div>

        <div class="project-description">
          <h2>项目描述</h2>
          <p>{{ project.description || '暂无描述' }}</p>
        </div>

        <!-- 3D预览 -->
        <div class="project-preview">
          <h2>3D预览</h2>
          <div class="preview-container">
            <Scene />
          </div>
        </div>

        <!-- 评论区 -->
        <div class="project-comments">
          <h2>评论 ({{ comments.length }})</h2>
          
          <!-- 评论表单 -->
          <div v-if="isLoggedIn" class="comment-form">
            <el-input
              v-model="commentContent"
              type="textarea"
              placeholder="写下你的评论..."
              :rows="3"
              maxlength="1000"
              show-word-limit
            />
            <el-button 
              type="primary" 
              @click="handleAddComment"
              :loading="commentLoading"
              :disabled="!commentContent.trim()"
            >
              发表评论
            </el-button>
          </div>
          
          <!-- 评论列表 -->
          <div class="comments-list">
            <div v-if="comments.length === 0" class="no-comments">
              暂无评论，来发表第一条评论吧
            </div>
            <div v-else v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <span class="comment-author">{{ comment.username || comment.user_id }}</span>
                <div class="comment-actions">
                  <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                  <el-button 
                    v-if="isLoggedIn && comment.user_id === authStore.user?.id" 
                    type="text" 
                    size="small" 
                    @click="handleDeleteComment(comment.id)"
                    class="delete-button"
                  >
                    <el-icon><Delete /></el-icon>删除
                  </el-button>
                </div>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载失败 -->
      <div v-else-if="!loading" class="error-container">
        <el-empty description="项目不存在或未公开" :image-size="200" />
        <el-button type="primary" @click="goBack">返回画廊</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, h } from 'vue'
import { ArrowLeft, Star, Collection, Download, House } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
import Scene from '@/components/3d/Scene.vue'
import { useGalleryStore } from '@/stores/gallery'
import { useAuthStore } from '@/stores/auth'
import type { Project, Comment } from '@/types/project'

const router = useRouter()
const route = useRoute()
const galleryStore = useGalleryStore()
const authStore = useAuthStore()

// 背景动画气泡
const bubbles = ref<Array<{x: number; duration: number; delay: number; size: number; type: string}>>([])
const bubbleTypes = ['man', 'woman', 'child', 'elder']

// 获取剪影SVG组件
const getSilhouette = (type: string) => {
  const silhouettes: Record<string, any> = {
    man: {
      render: () => h('path', { 
        d: 'M50 15 C55 15 60 20 60 25 C60 32 55 37 50 37 C45 37 40 32 40 25 C40 20 45 15 50 15 M45 40 L40 75 L35 75 L38 55 L30 90 L38 90 L42 70 L45 90 L55 90 L58 70 L62 90 L70 90 L62 55 L65 75 L60 75 L55 40 C53 38 47 38 45 40 Z',
        fill: 'rgba(102, 126, 234, 0.15)'
      })
    },
    woman: {
      render: () => h('path', { 
        d: 'M50 15 C55 15 60 20 60 25 C60 32 55 37 50 37 C45 37 40 32 40 25 C40 20 45 15 50 15 M45 40 L42 55 L35 55 L40 40 M55 40 L58 55 L65 55 L60 40 M43 40 L40 90 L45 90 L48 60 L50 75 L52 60 L55 90 L60 90 L57 40 C55 38 45 38 43 40 Z',
        fill: 'rgba(118, 75, 162, 0.15)'
      })
    },
    child: {
      render: () => h('path', { 
        d: 'M50 20 C54 20 58 24 58 28 C58 33 54 37 50 37 C46 37 42 33 42 28 C42 24 46 20 50 20 M46 40 L44 70 L40 70 L43 55 L38 85 L44 85 L47 65 L50 85 L53 85 L56 65 L59 85 L65 85 L60 55 L63 70 L59 70 L57 40 C55 38 45 38 46 40 Z',
        fill: 'rgba(102, 126, 234, 0.12)'
      })
    },
    elder: {
      render: () => h('path', { 
        d: 'M50 12 C56 12 62 18 62 25 C62 33 56 39 50 39 C44 39 38 33 38 25 C38 18 44 12 50 12 M45 42 L38 80 L32 80 L36 58 L28 95 L38 95 L42 72 L45 95 L55 95 L58 72 L62 95 L72 95 L64 58 L68 80 L62 80 L55 42 C53 40 47 40 45 42 Z M35 20 L30 15 M65 20 L70 15',
        fill: 'rgba(118, 75, 162, 0.12)'
      })
    }
  }
  return silhouettes[type] || silhouettes.man
}

// 初始化气泡
const initBubbles = () => {
  const count = 15
  for (let i = 0; i < count; i++) {
    bubbles.value.push({
      x: Math.random() * 100,
      duration: 15 + Math.random() * 20,
      delay: Math.random() * 10,
      size: 60 + Math.random() * 100,
      type: bubbleTypes[Math.floor(Math.random() * bubbleTypes.length)]
    })
  }
}

// 状态
const loading = ref(true)
const actionLoading = ref(false)
const commentLoading = ref(false)
const project = ref<Project | null>(null)
const comments = ref<Comment[]>([])
const commentContent = ref('')

// 计算属性
const projectId = computed(() => route.params.id as string)
const isLoggedIn = computed(() => authStore.isAuthenticated)
const isLiked = ref(false)
const isFavorited = ref(false)

// 加载项目详情
const loadProjectDetail = async () => {
  try {
    loading.value = true
    project.value = await galleryStore.fetchPublicProject(projectId.value)
    await loadComments()
    await checkUserInteractions()
  } catch (error) {
    ElMessage.error('加载项目详情失败')
  } finally {
    loading.value = false
  }
}

// 加载评论
const loadComments = async () => {
  try {
    comments.value = await galleryStore.fetchProjectComments(projectId.value)
  } catch (error) {
    ElMessage.error('加载评论失败')
  }
}

// 检查用户交互状态
const checkUserInteractions = async () => {
  if (isLoggedIn.value) {
    try {
      // 这里应该调用API检查用户是否已点赞和收藏
      // 暂时设为false
      isLiked.value = false
      isFavorited.value = false
    } catch (error) {
      console.error('检查用户交互状态失败', error)
    }
  }
}

// 事件处理
const goBack = () => {
  router.push({ name: 'gallery' })
}

const goHome = () => {
  router.push('/')
}

const handleViewAuthor = () => {
  if (project.value) {
    router.push({ name: 'gallery-user-detail', params: { id: project.value.user_id } })
  }
}

const handleLike = async () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    actionLoading.value = true
    const result = await galleryStore.toggleLike(projectId.value)
    isLiked.value = result.liked
    ElMessage.success(result.message)
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    actionLoading.value = false
  }
}

const handleFavorite = async () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    actionLoading.value = true
    const result = await galleryStore.toggleFavorite(projectId.value)
    isFavorited.value = result.favorited
    ElMessage.success(result.message)
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    actionLoading.value = false
  }
}

const handleDownload = async () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    actionLoading.value = true
    const result = await galleryStore.downloadProject(projectId.value)
    ElMessage.success(result.message)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '下载失败')
  } finally {
    actionLoading.value = false
  }
}

const handleAddComment = async () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }

  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  try {
    commentLoading.value = true
    await galleryStore.addComment(projectId.value, { content: commentContent.value })
    await loadComments()
    commentContent.value = ''
    ElMessage.success('评论发表成功')
  } catch (error) {
    ElMessage.error('发表评论失败')
  } finally {
    commentLoading.value = false
  }
}

const handleDeleteComment = async (commentId: number) => {
  try {
    await galleryStore.deleteComment(Number(projectId.value), commentId)
    ElMessage.success('评论删除成功')
  } catch (error) {
    ElMessage.error('删除评论失败')
  }
}

// 工具函数
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 监听路由参数变化
watch(() => route.params.id, () => {
  loadProjectDetail()
})

// 页面加载时获取数据
onMounted(() => {
  initBubbles()
  loadProjectDetail()
})
</script>

<style scoped lang="scss">
.gallery-project-detail-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  position: relative;
  overflow: hidden;
}

.background-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.bubble {
  position: absolute;
  bottom: -150px;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.08));
  animation: float-up linear infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

@keyframes float-up {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.4;
  }
  100% {
    transform: translateY(-120vh) scale(0.8);
    opacity: 0;
  }
}

.silhouette {
  width: 60%;
  height: 60%;
  opacity: 0.6;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
  position: relative;
  z-index: 1;

  .header-buttons {
    display: flex;
    gap: 12px;

    .el-button {
      background: rgba(26, 26, 46, 0.8);
      border: 1px solid rgba(102, 126, 234, 0.3);
      color: rgba(255, 255, 255, 0.8);
      border-radius: 8px;
      padding: 8px 16px;
      font-size: 14px;

      &:hover {
        background: rgba(102, 126, 234, 0.3);
        border-color: #667eea;
        color: #a8b4ff;
      }
    }
  }

  .page-title {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    background: linear-gradient(135deg, #a8b4ff 0%, #c49bff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.project-detail {
  background: rgba(26, 26, 46, 0.8);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  padding: 24px;
  border: 1px solid rgba(102, 126, 234, 0.2);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
}

.project-info {
  .project-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(102, 126, 234, 0.2);

    .project-meta {
      display: flex;
      gap: 24px;
      font-size: 14px;
      color: rgba(255, 255, 255, 0.7);

      .project-author {
        font-weight: 500;

        .author-name {
          color: #a8b4ff;
          cursor: pointer;
          &:hover {
            text-decoration: underline;
          }
        }
      }
    }

    .project-actions {
      display: flex;
      gap: 12px;
    }
  }

  .project-description {
    margin-bottom: 32px;

    h2 {
      margin: 0 0 16px;
      font-size: 18px;
      font-weight: 600;
      color: #fff;
    }

    p {
      margin: 0;
      font-size: 14px;
      line-height: 1.6;
      color: rgba(255, 255, 255, 0.7);
    }
  }

  .project-preview {
    margin-bottom: 32px;

    h2 {
      margin: 0 0 16px;
      font-size: 18px;
      font-weight: 600;
      color: #fff;
    }

    .preview-container {
      width: 100%;
      height: 400px;
      background: rgba(15, 52, 96, 0.5);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(102, 126, 234, 0.2);
    }
  }

  .project-comments {
    h2 {
      margin: 0 0 24px;
      font-size: 18px;
      font-weight: 600;
      color: #fff;
    }

    .comment-form {
      margin-bottom: 32px;
      display: flex;
      flex-direction: column;
      gap: 12px;

      :deep(.el-textarea__inner) {
        background: rgba(26, 26, 46, 0.6);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #fff;
        border-radius: 8px;
      }

      :deep(.el-textarea__inner::placeholder) {
        color: rgba(255, 255, 255, 0.4);
      }

      :deep(.el-textarea__inner:focus) {
        border-color: #667eea;
      }

      .el-button {
        align-self: flex-end;
      }
    }

    .comments-list {
      .no-comments {
        text-align: center;
        padding: 48px 0;
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
      }

      .comment-item {
        padding: 16px 0;
        border-bottom: 1px solid rgba(102, 126, 234, 0.2);

        &:last-child {
          border-bottom: none;
        }

        .comment-header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;
          font-size: 14px;

          .comment-author {
            font-weight: 500;
            color: #fff;
          }

          .comment-actions {
            display: flex;
            align-items: center;
            gap: 12px;

            .comment-date {
              color: rgba(255, 255, 255, 0.5);
            }

            .delete-button {
              color: #f56c6c;
              &:hover {
                color: #f78989;
              }
            }
          }
        }

        .comment-content {
          font-size: 14px;
          line-height: 1.6;
          color: rgba(255, 255, 255, 0.7);
        }
      }
    }
  }
}

.error-container {
  text-align: center;
  padding: 64px 0;

  .el-button {
    margin-top: 24px;
  }
}

:deep(.el-button--default) {
  background: rgba(26, 26, 46, 0.6);
  border-color: rgba(102, 126, 234, 0.3);
  color: rgba(255, 255, 255, 0.8);
}

:deep(.el-button--default:hover) {
  background: rgba(102, 126, 234, 0.3);
  border-color: #667eea;
  color: #a8b4ff;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

:deep(.el-button--success) {
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  border: none;
}

:deep(.el-empty__description p) {
  color: rgba(255, 255, 255, 0.7);
}
</style>