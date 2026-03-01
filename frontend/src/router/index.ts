import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 1. 合并导入：保留上游所有导入 + 兼容本地画廊组件（统一命名规范）
import HomeView from '../views/HomeView.vue'
import CreateView from '../views/CreateView.vue'
import ModelingView from '../views/ModelingView.vue'
import TemplatesView from '../views/TemplatesView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import ProfileSetupView from '../views/ProfileSetupView.vue'
import LibraryView from '../views/LibraryView.vue'
import ProjectDetailView from '../views/ProjectDetailView.vue'
import GalleryView from '../views/GalleryView.vue'       // 上游画廊组件
import GalleryProjectDetailView from '../views/GalleryProjectDetailView.vue'  // 上游画廊详情
import NotFound from '../views/NotFound.vue'

// Admin 相关导入（保留上游完整管理后台）
import AdminLayout from '../layouts/AdminLayout.vue'
import AdminDashboard from '../views/admin/DashboardView.vue'
import AdminUsers from '../views/admin/UsersView.vue'
import AdminAppeals from '../views/admin/AppealsView.vue'
import AdminProjects from '../views/admin/ProjectsView.vue'
import AdminReports from '../views/admin/ReportsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/gallery'  // 保留本地的默认跳转逻辑
    },
    // 2. 合并画廊路由：优先保留上游规范的命名 + 兼容本地路由结构
    {
      path: '/gallery',
      name: 'gallery',
      component: GalleryView  // 统一使用上游的 GalleryView，避免组件命名冲突
    },
    {
      path: '/gallery/:id',
      name: 'gallery-detail',
      // 兼容本地的懒加载方式，组件指向上游的画廊详情（保持路由参数一致）
      component: GalleryProjectDetailView
    },
    // 3. 保留上游完整的鉴权路由（登录/注册/个人中心等）
    {
      path: '/login',
      name: 'login',
      component: LoginView  // 统一为非懒加载，保持代码风格一致
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guest: true },  // 保留上游的鉴权元信息（关键！）
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
    },
    {
      path: '/profile-setup',
      name: 'profile-setup',
      component: ProfileSetupView,
      meta: { requiresAuth: true },
    },
    {
      path: '/library',
      name: 'library',
      component: LibraryView,
      meta: { requiresAuth: true },
    },
    {
      path: '/library/project/:id',
      name: 'project-detail',
      component: ProjectDetailView,
      meta: { requiresAuth: true },
    },
    // 4. 保留上游完整的管理后台路由（核心功能，不能删）
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          redirect: '/admin/dashboard',
        },
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: AdminDashboard,
        },
        {
          path: 'users',
          name: 'admin-users',
          component: AdminUsers,
        },
        {
          path: 'appeals',
          name: 'admin-appeals',
          component: AdminAppeals,
        },
        {
          path: 'projects',
          name: 'admin-projects',
          component: AdminProjects,
        },
        {
          path: 'reports',
          name: 'admin-reports',
          component: AdminReports,
        },
      ],
    },
    // 5. 保留404路由，保证路由完整性
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFound,
    },
  ],
})

// 6. 保留上游完整的路由守卫（鉴权逻辑，核心！）
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  
  if (to.meta.requiresAdmin) {
    if (!token) {
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
    
    // 如果有 token 但没有用户信息，先获取用户信息
    if (!authStore.user) {
      await authStore.fetchUser()
    }
    
    if (!authStore.isAdmin) {
      next({ name: 'home' })
      return
    }
  }
  
  if (to.meta.guest && token) {
    next({ name: 'home' })
    return
  }
  
  next()
})

export default router