<template>
  <el-card class="project-card" shadow="hover" @click="goToDetail">
    <div class="project-thumbnail">
      <div class="placeholder-image">
        <el-icon :size="48"><Box /></el-icon>
        <span class="placeholder-text">3D Model</span>
      </div>
      <div class="project-status">
        <el-tag :type="statusType" size="small">{{ statusLabel }}</el-tag>
      </div>
    </div>
    
    <div class="project-info">
      <h3 class="project-name" :title="project.name">{{ project.name }}</h3>
      <p class="project-description" :title="project.description || ''">
        {{ project.description || '暂无描述' }}
      </p>
      <div class="project-meta">
        <span class="update-time">{{ formatDate(project.updated_at) }}</span>
      </div>
    </div>
    
    <div class="project-actions" @click.stop>
      <el-dropdown trigger="click">
        <el-button type="primary" link>
          <el-icon><More /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleEdit">
              <el-icon><Edit /></el-icon>编辑
            </el-dropdown-item>
            <el-dropdown-item @click="handleDuplicate">
              <el-icon><CopyDocument /></el-icon>复制
            </el-dropdown-item>
            <el-dropdown-item divided @click="handleDelete" class="delete-item">
              <el-icon><Delete /></el-icon>删除
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Box, More, Edit, CopyDocument, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Project } from '@/types/project'
import { ProjectStatusMap } from '@/types/project'
import { useProjectStore } from '@/stores/projects'

const props = defineProps<{
  project: Project
}>()

const emit = defineEmits<{
  edit: [project: Project]
  delete: [id: number]
}>()

const router = useRouter()
const projectStore = useProjectStore()

const statusLabel = computed(() => {
  return ProjectStatusMap[props.project.status]?.label || props.project.status
})

const statusType = computed(() => {
  return ProjectStatusMap[props.project.status]?.type || 'info'
})

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const goToDetail = () => {
  router.push(`/library/project/${props.project.id}`)
}

const handleEdit = () => {
  emit('edit', props.project)
}

const handleDuplicate = async () => {
  try {
    await projectStore.duplicateProject(props.project.id)
    ElMessage.success('项目复制成功')
  } catch (error) {
    ElMessage.error('项目复制失败')
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${props.project.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await projectStore.deleteProject(props.project.id)
    ElMessage.success('项目删除成功')
    emit('delete', props.project.id)
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('项目删除失败')
    }
  }
}
</script>

<style scoped lang="scss">
.project-card {
  position: relative;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  :deep(.el-card__body) {
    padding: 0;
  }
}

.project-thumbnail {
  position: relative;
  width: 100%;
  height: 160px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  
  .placeholder-image {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: rgba(255, 255, 255, 0.8);
    
    .placeholder-text {
      margin-top: 8px;
      font-size: 14px;
    }
  }
  
  .project-status {
    position: absolute;
    top: 12px;
    right: 12px;
  }
}

.project-info {
  padding: 16px;
  
  .project-name {
    margin: 0 0 8px;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .project-description {
    margin: 0 0 12px;
    font-size: 13px;
    color: #606266;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 40px;
  }
  
  .project-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .update-time {
      font-size: 12px;
      color: #909399;
    }
  }
}

.project-actions {
  position: absolute;
  top: 8px;
  left: 8px;
  opacity: 0;
  transition: opacity 0.2s;
  
  .project-card:hover & {
    opacity: 1;
  }
  
  :deep(.el-button) {
    color: white;
    background: rgba(0, 0, 0, 0.3);
    border: none;
    
    &:hover {
      background: rgba(0, 0, 0, 0.5);
    }
  }
}

.delete-item {
  color: #f56c6c;
}
</style>
