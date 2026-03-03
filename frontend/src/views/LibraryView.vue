<template>
  <div class="library-view">
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
      <div class="header-left">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span> 返回主页
        </button>
        <div class="title-area">
          <h1 class="page-title">我的项目库</h1>
          <p class="page-subtitle">管理和查看您的所有3D项目</p>
        </div>
      </div>
      <el-button type="primary" size="large" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建项目
      </el-button>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索项目名称"
        clearable
        class="search-input"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select v-model="filterStatus" placeholder="筛选状态" clearable @change="handleFilter">
        <el-option label="草稿" value="draft" />
        <el-option label="处理中" value="processing" />
        <el-option label="已完成" value="completed" />
        <el-option label="已归档" value="archived" />
      </el-select>

      <el-select v-model="sortBy" placeholder="排序方式" @change="handleSort">
        <el-option label="最新创建" value="created_at" />
        <el-option label="最近更新" value="updated_at" />
        <el-option label="项目名称" value="name" />
      </el-select>

      <el-radio-group v-model="sortOrder" size="small" @change="handleSort">
        <el-radio-button label="desc">
          <el-icon><SortDown /></el-icon>
        </el-radio-button>
        <el-radio-button label="asc">
          <el-icon><SortUp /></el-icon>
        </el-radio-button>
      </el-radio-group>


    </div>

    <!-- 项目列表 -->
    <div v-loading="projectStore.loading" class="projects-container">
      <!-- 空状态 -->
      <el-empty
        v-if="!projectStore.hasProjects && !projectStore.loading"
        description="暂无项目"
        :image-size="200"
      >
        <template #description>
          <div class="empty-content">
            <p class="empty-title">还没有任何项目</p>
            <p class="empty-desc">点击上方按钮创建您的第一个3D项目</p>
          </div>
        </template>
        <el-button type="primary" @click="handleCreate">立即创建</el-button>
      </el-empty>

      <!-- 项目网格 -->
      <div v-else class="projects-grid">
        <div class="project-item" v-for="project in projectStore.projects" :key="project.id">
          <ProjectCard
            :project="project"
            :is-public="false"
            @edit="handleEdit"
            @delete="handleDeleteSuccess"
            @view="handleViewProject"
          />
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="projectStore.total > 0" class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="projectStore.total"
          :page-sizes="[12, 24, 48]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 项目表单弹窗 -->
    <ProjectForm
      v-model="formVisible"
      :project="editingProject"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, h } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, SortDown, SortUp, House } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import ProjectCard from '@/components/library/ProjectCard.vue'
import ProjectForm from '@/components/library/ProjectForm.vue'
import { useProjectStore } from '@/stores/projects'
import type { Project } from '@/types/project'

const projectStore = useProjectStore()
const router = useRouter()

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

// 返回主页
const goHome = () => {
  router.push('/')
}

// 搜索和筛选状态
const searchQuery = ref('')
const filterStatus = ref('')
const sortBy = ref('created_at')
const sortOrder = ref<'asc' | 'desc'>('desc')
const currentPage = ref(1)
const pageSize = ref(12)



// 表单状态
const formVisible = ref(false)
const editingProject = ref<Project | null>(null)

// 加载项目列表
const loadProjects = async () => {
  try {
    await projectStore.fetchProjects({
      search: searchQuery.value || undefined,
      status: filterStatus.value || undefined,
      sort_by: sortBy.value,
      sort_order: sortOrder.value,
      page: currentPage.value,
      page_size: pageSize.value
    })
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  }
}

// 事件处理
const handleCreate = () => {
  editingProject.value = null
  formVisible.value = true
}

const handleEdit = (project: Project) => {
  editingProject.value = project
  formVisible.value = true
}

const handleFormSuccess = () => {
  loadProjects()
}

const handleDeleteSuccess = () => {
  loadProjects()
}

const handleViewProject = (project: Project) => {
  router.push(`/library/project/${project.id}`)
}

const handleSearch = () => {
  currentPage.value = 1
  loadProjects()
}

const handleFilter = () => {
  currentPage.value = 1
  loadProjects()
}

const handleSort = () => {
  loadProjects()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadProjects()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadProjects()
}

// 监听分页变化
watch([currentPage, pageSize], () => {
  projectStore.setPage(currentPage.value)
})

// 页面加载时获取数据
onMounted(() => {
  initBubbles()
  loadProjects()
})
</script>

<style scoped lang="scss">
.library-view {
  padding: 24px;
  max-width: 1400px;
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
    opacity: 0.8;
  }
  90% {
    opacity: 0.5;
  }
  100% {
    transform: translateY(-120vh) scale(0.8);
    opacity: 0;
  }
}

.silhouette {
  width: 60%;
  height: 60%;
  opacity: 0.7;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  position: relative;
  z-index: 1;

  .header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
    
    .home-btn {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      padding: 0.6rem 1.2rem;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s;
      color: #fff;
      font-weight: 500;
      font-size: 14px;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
      }
      
      .home-icon {
        font-size: 1.1rem;
      }
    }
    
    .title-area {
      .page-title {
        margin: 0 0 4px;
        font-size: 28px;
        font-weight: 600;
        color: #fff;
      }

      .page-subtitle {
        margin: 0;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.7);
      }
    }
  }
  
  :deep(.el-button--primary) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 10px;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
  }
  
  :deep(.el-button.is-plain) {
    border-radius: 10px;
    border-color: rgba(102, 126, 234, 0.3);
    color: #fff;
    background: rgba(102, 126, 234, 0.1);
    
    &:hover {
      background: rgba(102, 126, 234, 0.2);
      border-color: #667eea;
    }
  }
}

.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: rgba(26, 26, 46, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(102, 126, 234, 0.2);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;

  .search-input {
    width: 300px;
  }
  
  :deep(.el-input__wrapper) {
    border-radius: 8px;
    box-shadow: none;
    border: 1px solid rgba(102, 126, 234, 0.3);
    background: rgba(255, 255, 255, 0.05);
    
    &:focus-within {
      border-color: #667eea;
      box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
  }
  
  :deep(.el-input__inner) {
    color: #fff;
    
    &::placeholder {
      color: rgba(255, 255, 255, 0.5);
    }
  }
  
  :deep(.el-select .el-input__wrapper) {
    border-radius: 8px;
  }
  
  :deep(.el-radio-button__inner) {
    border-radius: 8px !important;
    border: 1px solid rgba(102, 126, 234, 0.3);
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.7);
  }
  
  :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: #667eea;
    color: #fff;
    box-shadow: none;
  }
}

.projects-container {
  min-height: 400px;
  position: relative;
  z-index: 1;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.project-item {
  position: relative;
}

.project-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
}

.batch-actions {
  margin-left: auto;
  
  :deep(.el-button--danger) {
    border-radius: 8px;
  }
}

.empty-content {
  text-align: center;

  .empty-title {
    font-size: 16px;
    font-weight: 500;
    color: #fff;
    margin: 0 0 8px;
  }

  .empty-desc {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0;
  position: relative;
  z-index: 1;
  
  :deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  :deep(.el-pagination.is-background .el-pager li:not(.is-disabled):hover) {
    color: #667eea;
  }
  
  :deep(.el-pagination.is-background .btn-prev),
  :deep(.el-pagination.is-background .btn-next),
  :deep(.el-pagination.is-background .el-pager li) {
    background: rgba(26, 26, 46, 0.8);
    color: rgba(255, 255, 255, 0.7);
  }
}
</style>
