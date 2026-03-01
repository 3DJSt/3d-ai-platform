<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiService, type GalleryItem } from '@/services/api'
import ProjectCard from '@/components/ProjectCard.vue'
import SearchFilter from '@/components/SearchFilter.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const projects = ref<GalleryItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(12)

const search = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')

const fetchProjects = async () => {
  loading.value = true
  try {
    const response = await apiService.getGalleryList({
      page: page.value,
      page_size: pageSize.value,
      search: search.value || undefined,
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    })
    projects.value = response.items
    total.value = response.total
  } catch (error) {
    console.error('获取项目列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  updateUrlParams()
  fetchProjects()
}

const handlePageChange = (newPage: number) => {
  page.value = newPage
  updateUrlParams()
  fetchProjects()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleSizeChange = (newSize: number) => {
  pageSize.value = newSize
  page.value = 1
  updateUrlParams()
  fetchProjects()
}

const updateUrlParams = () => {
  const query: Record<string, string | number> = {}
  if (page.value > 1) query.page = page.value
  if (pageSize.value !== 12) query.pageSize = pageSize.value
  if (search.value) query.search = search.value
  if (sortBy.value !== 'created_at') query.sortBy = sortBy.value
  if (sortOrder.value !== 'desc') query.sortOrder = sortOrder.value
  
  router.push({ query })
}

const initFromUrl = () => {
  const query = route.query
  if (query.page) page.value = Number(query.page)
  if (query.pageSize) pageSize.value = Number(query.pageSize)
  if (query.search) search.value = String(query.search)
  if (query.sortBy) sortBy.value = String(query.sortBy)
  if (query.sortOrder) sortOrder.value = String(query.sortOrder)
}

watch([sortBy, sortOrder], () => {
  page.value = 1
  updateUrlParams()
  fetchProjects()
})

onMounted(() => {
  initFromUrl()
  fetchProjects()
})
</script>

<template>
  <div class="gallery-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">
          <el-icon><PictureFilled /></el-icon>
          3D模型画廊
        </h1>
        <p class="page-subtitle">探索精彩的3D角色作品</p>
      </div>

      <SearchFilter
        v-model:search="search"
        v-model:sort-by="sortBy"
        v-model:sort-order="sortOrder"
        @search="handleSearch"
      />

      <div v-loading="loading" class="gallery-content">
        <div v-if="!loading && projects.length === 0" class="empty-state">
          <el-empty description="暂无公开项目">
            <template #image>
              <el-icon :size="64" color="#c0c4cc"><FolderOpened /></el-icon>
            </template>
          </el-empty>
        </div>

        <div v-else class="gallery-grid">
          <ProjectCard
            v-for="project in projects"
            :key="project.id"
            :project="project"
          />
        </div>

        <div v-if="total > pageSize" class="pagination-wrapper">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 48, 96]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="handlePageChange"
            @size-change="handleSizeChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gallery-page {
  min-height: calc(100vh - 104px);
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 40px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.page-subtitle {
  font-size: 16px;
  opacity: 0.9;
}

.gallery-content {
  min-height: 400px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

@media (max-width: 1199px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 767px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .page-title {
    font-size: 24px;
  }
}

@media (max-width: 575px) {
  .gallery-grid {
    grid-template-columns: 1fr;
  }
}
</style>
