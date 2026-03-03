<template>
  <div v-loading="loading" class="project-detail-view">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div
        v-for="bubble in bubbles"
        :key="bubble.id"
        class="bubble"
        :style="{
          left: bubble.x + 'px',
          animationDelay: bubble.delay + 's',
          animationDuration: bubble.duration + 's',
          width: bubble.size + 'px',
          height: bubble.size + 'px',
          opacity: bubble.opacity
        }"
      >
        <component :is="getSilhouette(bubble.type)" />
      </div>
    </div>

    <!-- 返回按钮 -->
    <div class="back-nav">
      <el-button link @click="goBack">
        <el-icon><ArrowLeft /></el-icon>返回项目库
      </el-button>
    </div>

    <template v-if="project">
      <!-- 项目头部 -->
      <div class="project-header">
        <div class="header-info">
          <h1 class="project-title">{{ project.name }}</h1>
          <div class="project-meta">
            <el-tag :type="statusType" size="large">{{ statusLabel }}</el-tag>
            <span class="meta-divider">|</span>
            <span class="meta-item">创建于 {{ formatDate(project.created_at) }}</span>
            <span class="meta-divider">|</span>
            <span class="meta-item">更新于 {{ formatDate(project.updated_at) }}</span>
          </div>
        </div>
        <div class="header-actions">
          <el-button @click="handleEdit">
            <el-icon><Edit /></el-icon>编辑
          </el-button>
          <el-button type="danger" plain @click="handleDelete">
            <el-icon><Delete /></el-icon>删除
          </el-button>
        </div>
      </div>

      <!-- 项目描述 -->
      <el-card v-if="project.description" class="description-card" shadow="never">
        <template #header>
          <span>项目描述</span>
        </template>
        <p class="description-text">{{ project.description }}</p>
      </el-card>

      <!-- 主要内容区 -->
      <div class="main-content">
        <!-- 3D预览区 -->
        <el-card class="preview-card" shadow="never">
          <template #header>
            <span>3D模型预览</span>
          </template>
          <div class="preview-placeholder">
            <el-icon :size="64"><Box /></el-icon>
            <p>3D模型预览区域</p>
            <p class="placeholder-sub">（后续集成Three.js渲染）</p>
          </div>
        </el-card>

        <!-- 侧边信息栏 -->
        <div class="sidebar">
          <!-- 模型数据 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <span>模型数据</span>
            </template>
            <div class="info-list">
              <div class="info-item">
                <span class="label">模型文件</span>
                <span class="value">{{ project.model_data.model ? '已上传' : '未上传' }}</span>
              </div>
              <div class="info-item">
                <span class="label">纹理数量</span>
                <span class="value">{{ project.model_data.textures?.length || 0 }}</span>
              </div>
              <div class="info-item">
                <span class="label">动画数量</span>
                <span class="value">{{ project.model_data.animations?.length || 0 }}</span>
              </div>
              <div class="info-item">
                <span class="label">骨骼数据</span>
                <span class="value">{{ project.model_data.skeleton ? '有' : '无' }}</span>
              </div>
            </div>
          </el-card>

          <!-- 存储信息 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <span>存储信息</span>
            </template>
            <div class="info-list">
              <div class="info-item">
                <span class="label">存储桶</span>
                <span class="value">{{ project.storage_paths.minio_bucket }}</span>
              </div>
              <div class="info-item">
                <span class="label">模型文件</span>
                <span class="value">{{ project.storage_paths.model_key || '未上传' }}</span>
              </div>
            </div>
          </el-card>

          <!-- 操作按钮 -->
          <el-card class="action-card" shadow="never">
            <el-button type="primary" size="large" style="width: 100%" @click="handleAIEdit">
              <el-icon><MagicStick /></el-icon>AI编辑
            </el-button>
            <el-button size="large" style="width: 100%; margin-top: 12px; margin-left: 0" @click="handleDownload">
              <el-icon><Download /></el-icon>下载模型
            </el-button>
          </el-card>
        </div>
      </div>
    </template>

    <!-- 项目不存在 -->
    <el-empty v-else-if="!loading" description="项目不存在或已被删除">
      <el-button type="primary" @click="goBack">返回项目库</el-button>
    </el-empty>

    <!-- 编辑弹窗 -->
    <ProjectForm
      v-model="formVisible"
      :project="project"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Edit, Delete, Box, MagicStick, Download } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ProjectForm from '@/components/library/ProjectForm.vue'
import { useProjectStore } from '@/stores/projects'
import { ProjectStatusMap } from '@/types/project'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const formVisible = ref(false)
const bubbles = ref<any[]>([])

const projectId = computed(() => Number(route.params.id))
const project = computed(() => projectStore.currentProject)

const statusLabel = computed(() => {
  if (!project.value) return ''
  return ProjectStatusMap[project.value.status]?.label || project.value.status
})

const statusType = computed(() => {
  if (!project.value) return 'info'
  return ProjectStatusMap[project.value.status]?.type || 'info'
})

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadProject = async () => {
  loading.value = true
  try {
    await projectStore.getProjectDetail(projectId.value)
  } catch (error) {
    ElMessage.error('加载项目详情失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/library')
}

const handleEdit = () => {
  formVisible.value = true
}

const handleFormSuccess = () => {
  loadProject()
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${project.value?.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await projectStore.deleteProject(projectId.value)
    ElMessage.success('项目删除成功')
    router.push('/library')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('项目删除失败')
    }
  }
}

const handleAIEdit = () => {
  ElMessage.info('AI编辑功能开发中')
}

const handleDownload = () => {
  ElMessage.info('下载功能开发中')
}

const getSilhouette = (type: string) => {
  switch (type) {
    case 'person':
      return h('svg', { viewBox: '0 0 64 128', width: '50%', height: '50%', fill: 'rgba(168, 180, 255, 0.3)' }, [
        h('path', { d: 'M32 10C36.4 10 40 13.6 40 18v20h-8v-10c0-2.2-1.8-4-4-4s-4 1.8-4 4v10h-8V18c0-4.4 3.6-8 8-8z' }),
        h('path', { d: 'M24 40v60c0 4.4 3.6 8 8 8s8-3.6 8-8V40h-16z' }),
        h('path', { d: 'M16 50h-8v10h8V50z' }),
        h('path', { d: 'M56 50h-8v10h8V50z' }),
        h('path', { d: 'M16 90h-8v10h8V90z' }),
        h('path', { d: 'M56 90h-8v10h8V90z' })
      ])
    case 'child':
      return h('svg', { viewBox: '0 0 48 96', width: '40%', height: '40%', fill: 'rgba(196, 155, 255, 0.3)' }, [
        h('path', { d: 'M24 8C27.3 8 30 10.7 30 14v15h-6v-8c0-1.7-1.3-3-3-3s-3 1.3-3 3v8h-6V14c0-3.3 2.7-6 6-6z' }),
        h('path', { d: 'M18 32v45c0 3.3 2.7 6 6 6s6-2.7 6-6V32h-12z' }),
        h('path', { d: 'M12 40h-4v8h4V40z' }),
        h('path', { d: 'M40 40h-4v8h4V40z' }),
        h('path', { d: 'M12 70h-4v8h4V70z' }),
        h('path', { d: 'M40 70h-4v8h4V70z' })
      ])
    case 'woman':
      return h('svg', { viewBox: '0 0 64 128', width: '50%', height: '50%', fill: 'rgba(221, 161, 255, 0.3)' }, [
        h('path', { d: 'M24 10c0-2.2 1.8-4 4-4s4 1.8 4 4v15c0 2.2-1.8 4-4 4s-4-1.8-4-4V10z' }),
        h('path', { d: 'M16 25c-2.2 0-4 1.8-4 4v15c0 2.2 1.8 4 4 4s4-1.8 4-4V29c0-2.2-1.8-4-4-4z' }),
        h('path', { d: 'M48 25c-2.2 0-4 1.8-4 4v15c0 2.2 1.8 4 4 4s4-1.8 4-4V29c0-2.2-1.8-4-4-4z' }),
        h('path', { d: 'M24 48v60c0 4.4 3.6 8 8 8s8-3.6 8-8V48h-16z' }),
        h('path', { d: 'M16 58h-8v10h8V58z' }),
        h('path', { d: 'M56 58h-8v10h8V58z' }),
        h('path', { d: 'M16 98h-8v10h8V98z' }),
        h('path', { d: 'M56 98h-8v10h8V98z' })
      ])
    default:
      return h('svg', { viewBox: '0 0 64 128', width: '50%', height: '50%', fill: 'rgba(168, 180, 255, 0.3)' }, [
        h('path', { d: 'M32 10C36.4 10 40 13.6 40 18v20h-8v-10c0-2.2-1.8-4-4-4s-4 1.8-4 4v10h-8V18c0-4.4 3.6-8 8-8z' }),
        h('path', { d: 'M24 40v60c0 4.4 3.6 8 8 8s8-3.6 8-8V40h-16z' }),
        h('path', { d: 'M16 50h-8v10h8V50z' }),
        h('path', { d: 'M56 50h-8v10h8V50z' }),
        h('path', { d: 'M16 90h-8v10h8V90z' }),
        h('path', { d: 'M56 90h-8v10h8V90z' })
      ])
  }
}

const initBubbles = () => {
  const newBubbles = []
  const types = ['person', 'child', 'woman']
  
  for (let i = 0; i < 8; i++) {
    newBubbles.push({
      id: i,
      x: Math.random() * window.innerWidth,
      delay: Math.random() * 5,
      duration: 15 + Math.random() * 10,
      size: 100 + Math.random() * 150,
      opacity: 0.1 + Math.random() * 0.15,
      type: types[Math.floor(Math.random() * types.length)]
    })
  }
  
  bubbles.value = newBubbles
}

onMounted(() => {
  loadProject()
  initBubbles()
})
</script>

<style scoped lang="scss">
.project-detail-view {
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
    transform: translateY(0) translateX(0);
  }
  100% {
    transform: translateY(-120vh) translateX(100px);
  }
}

.back-nav {
  margin-bottom: 16px;
  position: relative;
  z-index: 1;

  :deep(.el-button) {
    color: rgba(255, 255, 255, 0.8);
  }
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;

  .header-info {
    .project-title {
      margin: 0 0 12px;
      font-size: 28px;
      font-weight: 600;
      background: linear-gradient(135deg, #a8b4ff 0%, #c49bff 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .project-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;

      .meta-divider {
        color: rgba(255, 255, 255, 0.2);
      }

      .meta-item {
        color: rgba(255, 255, 255, 0.6);
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 12px;

    :deep(.el-button) {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: rgba(255, 255, 255, 0.8);

      &:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
      }
    }
  }
}

.description-card {
  margin-bottom: 24px;
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;

  :deep(.el-card__header) {
    color: rgba(255, 255, 255, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .description-text {
    margin: 0;
    line-height: 1.8;
    color: rgba(255, 255, 255, 0.7);
    white-space: pre-wrap;
  }
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.preview-card {
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);

  :deep(.el-card__header) {
    color: rgba(255, 255, 255, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .preview-placeholder {
    height: 500px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.2) 100%);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.8);

    p {
      margin: 12px 0 0;
      font-size: 16px;
    }

    .placeholder-sub {
      font-size: 14px;
      opacity: 0.7;
    }
  }
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-card {
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);

  :deep(.el-card__header) {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .info-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .label {
      color: rgba(255, 255, 255, 0.6);
      font-size: 14px;
    }

    .value {
      color: rgba(255, 255, 255, 0.8);
      font-size: 14px;
      font-weight: 500;
    }
  }
}

.action-card {
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);

  :deep(.el-card__body) {
    padding: 16px;
  }

  :deep(.el-button) {
    background: rgba(102, 126, 234, 0.2);
    border: 1px solid rgba(102, 126, 234, 0.4);
    color: rgba(255, 255, 255, 0.8);

    &:hover {
      background: rgba(102, 126, 234, 0.3);
      border-color: rgba(102, 126, 234, 0.6);
    }

    &.el-button--primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #768ee8 0%, #8a5bb5 100%);
      }
    }
  }
}

:deep(.el-empty__description) {
  color: rgba(255, 255, 255, 0.6);
}

:deep(.el-empty__button) {
  margin-top: 20px;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;

  &:hover {
    background: linear-gradient(135deg, #768ee8 0%, #8a5bb5 100%);
  }
}

:deep(.el-tag) {
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.4);
  color: rgba(255, 255, 255, 0.8);

  &.el-tag--success {
    background: rgba(103, 194, 58, 0.2);
    border-color: rgba(103, 194, 58, 0.4);
  }

  &.el-tag--warning {
    background: rgba(230, 162, 60, 0.2);
    border-color: rgba(230, 162, 60, 0.4);
  }

  &.el-tag--danger {
    background: rgba(245, 108, 108, 0.2);
    border-color: rgba(245, 108, 108, 0.4);
  }
}
</style>
