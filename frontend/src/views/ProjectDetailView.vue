<template>
  <div v-loading="loading" class="project-detail-view">
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
import { ref, computed, onMounted } from 'vue'
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

onMounted(() => {
  loadProject()
})
</script>

<style scoped lang="scss">
.project-detail-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.back-nav {
  margin-bottom: 16px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e4e7ed;

  .header-info {
    .project-title {
      margin: 0 0 12px;
      font-size: 28px;
      font-weight: 600;
      color: #303133;
    }

    .project-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      color: #606266;
      font-size: 14px;

      .meta-divider {
        color: #dcdfe6;
      }

      .meta-item {
        color: #909399;
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 12px;
  }
}

.description-card {
  margin-bottom: 24px;

  .description-text {
    margin: 0;
    line-height: 1.8;
    color: #606266;
    white-space: pre-wrap;
  }
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
}

.preview-card {
  .preview-placeholder {
    height: 500px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  :deep(.el-card__header) {
    font-weight: 600;
    color: #303133;
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
      color: #606266;
      font-size: 14px;
    }

    .value {
      color: #303133;
      font-size: 14px;
      font-weight: 500;
    }
  }
}

.action-card {
  :deep(.el-card__body) {
    padding: 16px;
  }
}
</style>
