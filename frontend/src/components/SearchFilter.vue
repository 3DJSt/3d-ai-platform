<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  search: string
  sortBy: string
  sortOrder: string
}>()

const emit = defineEmits<{
  (e: 'update:search', value: string): void
  (e: 'update:sortBy', value: string): void
  (e: 'update:sortOrder', value: string): void
  (e: 'search'): void
}>()

const localSearch = ref(props.search)

watch(() => props.search, (val) => {
  localSearch.value = val
})

const handleSearch = () => {
  emit('update:search', localSearch.value)
  emit('search')
}

const handleSortChange = (value: string) => {
  emit('update:sortBy', value)
}

const handleOrderChange = (value: string) => {
  emit('update:sortOrder', value)
}

const sortOptions = [
  { label: '最新发布', value: 'created_at' },
  { label: '最多浏览', value: 'view_count' },
  { label: '最多点赞', value: 'like_count' }
]

const orderOptions = [
  { label: '降序', value: 'desc' },
  { label: '升序', value: 'asc' }
]
</script>

<template>
  <div class="search-filter">
    <div class="search-box">
      <el-input
        v-model="localSearch"
        placeholder="搜索项目名称..."
        clearable
        @keyup.enter="handleSearch"
        @clear="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-button type="primary" @click="handleSearch">
        搜索
      </el-button>
    </div>
    <div class="filter-options">
      <div class="filter-item">
        <span class="filter-label">排序：</span>
        <el-select
          :model-value="sortBy"
          @update:model-value="handleSortChange"
          style="width: 120px"
        >
          <el-option
            v-for="opt in sortOptions"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>
      </div>
      <div class="filter-item">
        <el-select
          :model-value="sortOrder"
          @update:model-value="handleOrderChange"
          style="width: 100px"
        >
          <el-option
            v-for="opt in orderOptions"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.search-box {
  display: flex;
  gap: 12px;
  flex: 1;
  max-width: 500px;
}

.filter-options {
  display: flex;
  gap: 16px;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .search-filter {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: none;
  }

  .filter-options {
    justify-content: flex-end;
  }
}
</style>
