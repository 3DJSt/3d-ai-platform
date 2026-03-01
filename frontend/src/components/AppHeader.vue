<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToGallery = () => {
  router.push('/gallery')
}
</script>

<template>
  <header class="app-header">
    <div class="container header-content">
      <div class="logo" @click="goToGallery">
        <el-icon :size="28"><Box /></el-icon>
        <span class="logo-text">3D AI角色创作平台</span>
      </div>
      <nav class="nav-menu">
        <el-button type="primary" text @click="goToGallery">
          <el-icon><PictureFilled /></el-icon>
          <span>画廊</span>
        </el-button>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  color: #409eff;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
