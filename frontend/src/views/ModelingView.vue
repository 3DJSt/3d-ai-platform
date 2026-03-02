<template>
  <div class="modeling-view">
    <!-- 顶部标题栏 -->
    <div class="top-bar">
      <div class="top-bar-left">
        <button class="home-btn" @click="goHome">
          <el-icon><HomeFilled /></el-icon>
        </button>
        <div class="project-title">
          <span class="app-name">3D AI Studio</span>
          <span class="project-name" v-if="projectName">| {{ projectName }}</span>
        </div>
      </div>
      <div class="top-bar-center">
        <div class="workflow-steps">
          <button 
            v-for="(step, index) in processSteps" 
            :key="step.id"
            class="workflow-step"
            :class="{ 
              'active': currentStep === step.id, 
              'completed': isStepCompleted(step.id)
            }"
            @click="goToStep(step.id)"
          >
            <el-icon class="step-icon"><component :is="step.icon" /></el-icon>
            <span class="step-label">{{ step.title }}</span>
          </button>
        </div>
      </div>
      <div class="top-bar-right">
        <button class="top-btn" @click="saveProject" title="保存项目">
          <el-icon><Download /></el-icon>
        </button>
      </div>
    </div>

    <!-- 主工作区 -->
    <div class="workspace">
      <!-- 左侧可伸缩流程栏 -->
      <div class="sidebar-left" :class="{ 'collapsed': leftSidebarCollapsed }">
        <div class="sidebar-toggle" @click="leftSidebarCollapsed = !leftSidebarCollapsed">
          <el-icon v-if="leftSidebarCollapsed"><ArrowRightBold /></el-icon>
          <el-icon v-else><ArrowLeftBold /></el-icon>
        </div>
        <div class="sidebar-content" v-show="!leftSidebarCollapsed">
          <div class="sidebar-header">
            <h3>工作流程</h3>
          </div>
          <div class="workflow-list">
            <div 
              v-for="(step, index) in processSteps" 
              :key="step.id"
              class="workflow-item"
              :class="{ 
                'active': currentStep === step.id, 
                'completed': isStepCompleted(step.id)
              }"
              @click="goToStep(step.id)"
            >
              <div class="workflow-number">{{ index + 1 }}</div>
              <div class="workflow-info">
                <div class="workflow-title">{{ step.title }}</div>
                <div class="workflow-desc">{{ step.description }}</div>
              </div>
              <el-icon v-if="isStepCompleted(step.id)" class="completed-icon"><Check /></el-icon>
            </div>
          </div>
        </div>
      </div>

      <!-- 3D视口区域 -->
      <div class="viewport-area">
        <div class="viewport-header">
          <div class="viewport-tabs">
            <div class="viewport-tab active">
              <el-icon><View /></el-icon>
              <span>3D视口</span>
            </div>
          </div>
          
          <!-- 导航按钮 -->
          <div class="viewport-nav">
            <button 
              class="nav-btn prev"
              @click="prevStep"
              :disabled="currentStepIndex === 0"
            >
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </button>
            <button 
              class="nav-btn next"
              @click="nextStep"
              :disabled="currentStepIndex === processSteps.length - 1"
            >
              下一步
              <el-icon><ArrowRight /></el-icon>
            </button>
          </div>
          
          <div class="viewport-tools">
            <button class="tool-btn" @click="resetView" title="重置视图">
              <el-icon><RefreshRight /></el-icon>
            </button>
            <button class="tool-btn" @click="toggleWireframe" title="切换线框模式">
              <el-icon><Grid /></el-icon>
            </button>
            <button class="tool-btn" title="透视/正交">
              <el-icon><Camera /></el-icon>
            </button>
          </div>
        </div>
        <div class="viewport-content" ref="previewContainer">
          <div v-if="loading" class="loading-overlay">
            <div class="spinner"></div>
            <p>加载模型中...</p>
          </div>
          <div v-else-if="!hasModel" class="no-model">
            <div class="no-model-icon">
              <el-icon :size="80"><Box /></el-icon>
            </div>
            <p>请选择或上传模型开始工作</p>
            <button class="action-btn" @click="showUploadModal = true">
              <el-icon><Upload /></el-icon>
              上传模型
            </button>
          </div>
        </div>
        <div class="viewport-footer">
          <div class="viewport-info">
            <span>顶点: {{ vertexCount }}</span>
            <span>面数: {{ faceCount }}</span>
            <span>对象: {{ objectCount }}</span>
          </div>
          <div class="viewport-controls">
            <button class="control-btn" @click="zoomIn">
              <el-icon><Plus /></el-icon>
            </button>
            <button class="control-btn" @click="zoomOut">
              <el-icon><Minus /></el-icon>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧属性面板 -->
      <div class="sidebar-right" :class="{ 'collapsed': rightSidebarCollapsed }">
        <div class="sidebar-toggle" @click="rightSidebarCollapsed = !rightSidebarCollapsed">
          <el-icon v-if="rightSidebarCollapsed"><ArrowLeftBold /></el-icon>
          <el-icon v-else><ArrowRightBold /></el-icon>
        </div>
        <div class="sidebar-content" v-show="!rightSidebarCollapsed">
          <div class="panel-tabs">
            <div 
              v-for="tab in panelTabs" 
              :key="tab.id"
              class="panel-tab"
              :class="{ 'active': activePanelTab === tab.id }"
              @click="activePanelTab = tab.id"
            >
              <el-icon><component :is="tab.icon" /></el-icon>
            </div>
          </div>
          
          <div class="panel-content">
            <!-- 当前步骤控制面板 -->
            <div v-if="activePanelTab === 'properties'" class="step-panel">
              <div class="panel-section">
                <h4 class="section-title">
                  <el-icon><Setting /></el-icon>
                  {{ currentStepTitle }}
                </h4>
                
                <!-- 加载模型 -->
                <div v-if="currentStep === 'load'" class="step-content">
                  <div class="control-group">
                    <label>上传模型</label>
                    <button class="control-btn-primary full-width" @click="showUploadModal = true">
                      <el-icon><Upload /></el-icon>
                      上传模型
                    </button>
                  </div>
                  <div class="control-group">
                    <label>快速加载</label>
                    <div class="btn-group vertical">
                      <button class="control-btn-secondary" @click="loadDefaultModel">
                        <el-icon><Download /></el-icon>
                        加载默认模型
                      </button>
                      <button class="control-btn-secondary" @click="goToTemplates">
                        <el-icon><Files /></el-icon>
                        选择模型模板
                      </button>
                    </div>
                  </div>
                  <div class="control-group">
                    <label>AI智能生成</label>
                    <button class="control-btn-primary full-width" @click="showAIModal = true">
                      <el-icon><MagicStick /></el-icon>
                      AI智能生成
                    </button>
                  </div>
                  <div class="control-group">
                    <label>最近上传文件</label>
                    <div class="recent-files">
                      <div class="recent-file" v-for="file in recentFiles" :key="file.name" @click="loadRecentFile(file)">
                        <el-icon><Document /></el-icon>
                        <span>{{ file.name }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="control-group">
                    <label>生成历史</label>
                    <div class="history-list">
                      <div class="history-item" v-for="item in generationHistory" :key="item.id">
                        <img :src="item.thumbnail" v-if="item.thumbnail" class="history-thumb" />
                        <div class="history-info">
                          <span>{{ item.name }}</span>
                          <small>{{ item.time }}</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 渲染模型 -->
                <div v-else-if="currentStep === 'render'" class="step-content">
                  <div class="control-group">
                    <label>材质类型</label>
                    <el-select v-model="renderSettings.material" class="dark-select">
                      <el-option label="标准材质" value="standard" />
                      <el-option label="金属材质" value="metal" />
                      <el-option label="塑料材质" value="plastic" />
                      <el-option label="玻璃材质" value="glass" />
                    </el-select>
                  </div>
                  <div class="control-group">
                    <label>基础颜色</label>
                    <el-color-picker v-model="renderSettings.color" class="dark-color-picker" />
                  </div>
                  <div class="control-group">
                    <label>金属度</label>
                    <el-slider v-model="renderSettings.metalness" :max="1" :step="0.01" class="dark-slider" />
                  </div>
                  <div class="control-group">
                    <label>粗糙度</label>
                    <el-slider v-model="renderSettings.roughness" :max="1" :step="0.01" class="dark-slider" />
                  </div>
                </div>
                
                <!-- 骨骼绑定 -->
                <div v-else-if="currentStep === 'rig'" class="step-content">
                  <div class="control-group">
                    <label>绑定方式</label>
                    <div class="btn-group vertical">
                      <button class="control-btn-primary" @click="autoRig">
                        <el-icon><MagicStick /></el-icon>
                        自动绑定
                      </button>
                      <button class="control-btn-secondary">
                        <el-icon><EditPen /></el-icon>
                        手动绑定
                      </button>
                    </div>
                  </div>
                  <div class="control-group">
                    <label>骨骼设置</label>
                    <div class="setting-item">
                      <span>骨骼数量</span>
                      <el-input-number v-model="rigSettings.boneCount" :min="1" :max="100" size="small" class="dark-input-number" />
                    </div>
                    <div class="setting-item">
                      <span>IK链</span>
                      <el-switch v-model="rigSettings.useIK" class="dark-switch" />
                    </div>
                  </div>
                </div>
                
                <!-- 动画生成 -->
                <div v-else-if="currentStep === 'animate'" class="step-content">
                  <div class="control-group">
                    <label>动画库</label>
                    <div class="animation-list">
                      <div class="anim-item" v-for="anim in animations" :key="anim.id" @click="loadAnimation(anim)">
                        <div class="anim-preview">
                          <el-icon><VideoPlay /></el-icon>
                        </div>
                        <div class="anim-info">
                          <span>{{ anim.name }}</span>
                          <small>{{ anim.duration }}s</small>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="control-group">
                    <label>时间轴</label>
                    <div class="timeline-controls">
                      <button class="control-btn-icon" @click="playAnimation">
                        <el-icon><VideoPlay /></el-icon>
                      </button>
                      <button class="control-btn-icon" @click="pauseAnimation">
                        <el-icon><VideoPause /></el-icon>
                      </button>
                      <el-slider v-model="timelineProgress" :max="100" class="dark-slider timeline-slider" />
                    </div>
                  </div>
                </div>
                
                <!-- 导出模型 -->
                <div v-else-if="currentStep === 'export'" class="step-content">
                  <div class="control-group">
                    <label>导出格式</label>
                    <el-select v-model="exportSettings.format" class="dark-select">
                      <el-option label="OBJ (.obj)" value="obj" />
                      <el-option label="FBX (.fbx)" value="fbx" />
                      <el-option label="GLTF (.gltf)" value="gltf" />
                      <el-option label="GLB (.glb)" value="glb" />
                      <el-option label="STL (.stl)" value="stl" />
                    </el-select>
                  </div>
                  <div class="control-group">
                    <label>导出选项</label>
                    <div class="checkbox-group">
                      <el-checkbox v-model="exportSettings.includeTextures" class="dark-checkbox">包含纹理</el-checkbox>
                      <el-checkbox v-model="exportSettings.includeAnimation" class="dark-checkbox">包含动画</el-checkbox>
                      <el-checkbox v-model="exportSettings.includeRig" class="dark-checkbox">包含骨骼</el-checkbox>
                    </div>
                  </div>
                  <div class="control-group">
                    <button class="control-btn-primary export-btn" @click="exportModel">
                      <el-icon><Download /></el-icon>
                      导出模型
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 场景大纲 -->
            <div v-else-if="activePanelTab === 'outline'" class="outline-panel">
              <div class="panel-section">
                <h4 class="section-title">
                  <el-icon><List /></el-icon>
                  场景大纲
                </h4>
                <div class="outline-tree">
                  <div class="outline-item" v-for="item in sceneObjects" :key="item.id">
                    <el-icon><component :is="item.icon" /></el-icon>
                    <span>{{ item.name }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 材质编辑器 -->
            <div v-else-if="activePanelTab === 'material'" class="material-panel">
              <div class="panel-section">
                <h4 class="section-title">
                  <el-icon><Brush /></el-icon>
                  材质
                </h4>
                <div class="material-list">
                  <div class="material-item" v-for="mat in materials" :key="mat.id">
                    <div class="material-preview" :style="{ background: mat.color }"></div>
                    <span>{{ mat.name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部时间轴（仅在动画步骤显示） -->
    <div class="timeline-bar" v-if="currentStep === 'animate'">
      <div class="timeline-controls">
        <button class="timeline-btn" @click="goToFirstFrame">
          <el-icon><DArrowLeft /></el-icon>
        </button>
        <button class="timeline-btn" @click="prevFrame">
          <el-icon><ArrowLeft /></el-icon>
        </button>
        <button class="timeline-btn play" @click="togglePlay">
          <el-icon v-if="isPlaying"><VideoPause /></el-icon>
          <el-icon v-else><VideoPlay /></el-icon>
        </button>
        <button class="timeline-btn" @click="nextFrame">
          <el-icon><ArrowRight /></el-icon>
        </button>
        <button class="timeline-btn" @click="goToLastFrame">
          <el-icon><DArrowRight /></el-icon>
        </button>
      </div>
      <div class="timeline-slider-container">
        <span class="frame-number">{{ currentFrame }}</span>
        <el-slider v-model="currentFrame" :max="totalFrames" class="dark-slider" />
        <span class="frame-number">{{ totalFrames }}</span>
      </div>
    </div>

    <!-- 上传模型弹窗 -->
    <el-dialog
      v-model="showUploadModal"
      title="上传模型"
      width="500px"
      class="dark-dialog"
    >
      <el-upload
        class="upload-demo"
        action="/api/files/upload"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :file-list="fileList"
        accept=".obj,.fbx,.gltf,.glb"
        :auto-upload="false"
        drag
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持上传 .obj, .fbx, .gltf, .glb 格式的模型文件
          </div>
        </template>
      </el-upload>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showUploadModal = false">取消</el-button>
          <el-button type="primary" @click="submitUpload">开始上传</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- AI智能生成悬浮聊天框 -->
    <div 
      v-if="showAIModal" 
      class="ai-chat-panel"
      :style="{ left: chatPanel.x + 'px', top: chatPanel.y + 'px' }"
    >
      <div class="chat-header" @mousedown="startDrag">
        <div class="chat-title">
          <el-icon><MagicStick /></el-icon>
          <span>AI智能生成</span>
        </div>
        <div class="chat-actions">
          <button class="chat-btn minimize" @click="toggleMinimize" title="最小化">
            <el-icon><Minus /></el-icon>
          </button>
          <button class="chat-btn close" @click="showAIModal = false" title="关闭">
            <el-icon><Close /></el-icon>
          </button>
        </div>
      </div>
      <div class="chat-body" v-show="!chatPanel.minimized">
        <div class="chat-messages" ref="chatMessagesRef">
          <div class="message ai">
            <div class="message-content">
              您好！我是AI助手，请描述您想要创建的3D模型，我会帮您生成。
            </div>
          </div>
          <div 
            v-for="(msg, index) in chatMessages" 
            :key="index" 
            :class="['message', msg.role]"
          >
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>
        <div class="chat-input-area">
          <el-input
            v-model="aiForm.description"
            type="textarea"
            :rows="2"
            placeholder="描述您想要的模型..."
            @keydown.enter.ctrl="sendAIMessage"
          />
          <div class="input-actions">
            <el-select v-model="aiForm.style" size="small" style="width: 120px;">
              <el-option label="写实风格" value="realistic" />
              <el-option label="卡通风格" value="cartoon" />
              <el-option label="低多边形" value="lowpoly" />
            </el-select>
            <el-button type="primary" size="small" @click="sendAIMessage">
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Download,
  Box,
  RefreshRight,
  View,
  Upload,
  ChatLineRound,
  MagicStick,
  VideoCamera,
  ArrowLeft,
  ArrowRight,
  ArrowUp,
  ArrowDown,
  HomeFilled,
  Plus,
  Minus,
  Grid,
  Camera,
  Setting,
  Document,
  EditPen,
  VideoPlay,
  VideoPause,
  DArrowLeft,
  DArrowRight,
  Check,
  ArrowLeftBold,
  ArrowRightBold,
  List,
  Brush,
  UploadFilled,
  Files,
  Close
} from '@element-plus/icons-vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

const router = useRouter()
const route = useRoute()

// 项目信息
const projectName = ref('')

// 流程步骤
const processSteps = ref([
  { id: 'load', title: '加载模型', description: '导入、上传或AI生成模型', icon: 'Download' },
  { id: 'render', title: '渲染模型', description: '设置材质和光照', icon: 'View' },
  { id: 'rig', title: '骨骼绑定', description: '添加骨骼系统', icon: 'Box' },
  { id: 'animate', title: '动画生成', description: '创建动画效果', icon: 'VideoCamera' },
  { id: 'export', title: '导出模型', description: '导出最终模型', icon: 'Download' }
])

const currentStep = ref('load')
const currentStepIndex = computed(() => processSteps.value.findIndex(step => step.id === currentStep.value))
const currentStepTitle = computed(() => processSteps.value.find(step => step.id === currentStep.value)?.title || '')

// 检查步骤是否已完成
const isStepCompleted = (stepId: string) => {
  const stepIndex = processSteps.value.findIndex(step => step.id === stepId)
  const currentIndex = processSteps.value.findIndex(step => step.id === currentStep.value)
  return stepIndex < currentIndex
}

// 侧边栏状态
const leftSidebarCollapsed = ref(false)
const rightSidebarCollapsed = ref(false)

// 面板标签
const panelTabs = ref([
  { id: 'properties', icon: 'Setting', title: '属性' },
  { id: 'outline', icon: 'List', title: '大纲' },
  { id: 'material', icon: 'Brush', title: '材质' }
])
const activePanelTab = ref('properties')

// 3D场景
const previewContainer = ref<HTMLElement>()
const loading = ref(false)
const hasModel = ref(false)
const wireframe = ref(false)
const vertexCount = ref(0)
const faceCount = ref(0)
const objectCount = ref(0)
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let controls: OrbitControls
let model: THREE.Object3D

// 渲染设置
const renderSettings = ref({
  material: 'standard',
  color: '#ffffff',
  metalness: 0.5,
  roughness: 0.5
})

// 骨骼绑定设置
const rigSettings = ref({
  boneCount: 32,
  useIK: true
})

// 导出设置
const exportSettings = ref({
  format: 'glb',
  includeTextures: true,
  includeAnimation: true,
  includeRig: true
})

// AI生成设置
const aiForm = ref({
  description: '',
  style: 'realistic'
})

// AI聊天面板
const chatMessagesRef = ref<HTMLElement | null>(null)
const chatMessages = ref<{ role: string; content: string }[]>([])
const chatPanel = ref({
  x: window.innerWidth - 420,
  y: window.innerHeight - 350,
  minimized: false
})
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })

// 上传设置
const showUploadModal = ref(false)
const showAIModal = ref(false)
const fileList = ref<any[]>([])

// 最近文件
const recentFiles = ref([
  { name: 'character_base.obj', path: '/models/character_base.obj' },
  { name: 'robot.fbx', path: '/models/robot.fbx' }
])

// 生成历史
const generationHistory = ref([
  { id: 1, name: '战士角色', time: '2分钟前', thumbnail: '' },
  { id: 2, name: '机械手臂', time: '1小时前', thumbnail: '' }
])

// 动画列表
const animations = ref([
  { id: 1, name: '行走', duration: 2.5 },
  { id: 2, name: '跑步', duration: 1.2 },
  { id: 3, name: '跳跃', duration: 1.0 },
  { id: 4, name: ' idle', duration: 3.0 }
])

// 场景对象
const sceneObjects = ref([
  { id: 1, name: 'Cube', icon: 'Box' },
  { id: 2, name: 'Camera', icon: 'Camera' },
  { id: 3, name: 'Light', icon: 'View' }
])

// 材质列表
const materials = ref([
  { id: 1, name: 'Material.001', color: '#0077ff' },
  { id: 2, name: 'Material.002', color: '#ff7700' }
])

// 时间轴
const currentFrame = ref(0)
const totalFrames = ref(250)
const isPlaying = ref(false)
const timelineProgress = ref(0)

// 初始化3D场景
const initScene = () => {
  if (!previewContainer.value) return

  // 创建场景 - 使用深色背景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x2a2a2a)

  // 创建相机
  camera = new THREE.PerspectiveCamera(
    75,
    previewContainer.value.clientWidth / previewContainer.value.clientHeight,
    0.1,
    1000
  )
  camera.position.z = 5

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(previewContainer.value.clientWidth, previewContainer.value.clientHeight)
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  previewContainer.value.appendChild(renderer.domElement)

  // 添加轨道控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05

  // 添加网格辅助线
  const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x333333)
  scene.add(gridHelper)

  // 添加光源
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(5, 10, 7)
  directionalLight.castShadow = true
  scene.add(directionalLight)

  // 渲染循环
  const animate = () => {
    requestAnimationFrame(animate)
    controls.update()
    renderer.render(scene, camera)
  }
  animate()

  // 响应窗口大小变化
  const handleResize = () => {
    if (!previewContainer.value) return
    camera.aspect = previewContainer.value.clientWidth / previewContainer.value.clientHeight
    camera.updateProjectionMatrix()
    renderer.setSize(previewContainer.value.clientWidth, previewContainer.value.clientHeight)
  }
  window.addEventListener('resize', handleResize)
}

// 加载默认模型
const loadDefaultModel = async () => {
  loading.value = true
  try {
    // 创建一个更复杂的默认模型
    const geometry = new THREE.BoxGeometry(1, 2, 0.5)
    const material = new THREE.MeshStandardMaterial({ 
      color: 0x0077ff,
      metalness: 0.3,
      roughness: 0.4
    })
    model = new THREE.Mesh(geometry, material)
    model.castShadow = true
    model.receiveShadow = true
    model.position.y = 1
    scene.add(model)
    
    // 更新统计信息
    vertexCount.value = geometry.attributes.position.count
    faceCount.value = geometry.index ? geometry.index.count / 3 : geometry.attributes.position.count / 3
    objectCount.value = 1
    
    hasModel.value = true
    ElMessage.success('默认模型加载成功')
  } catch (error) {
    ElMessage.error('模型加载失败')
  } finally {
    loading.value = false
  }
}

// 加载最近文件
const loadRecentFile = (file: any) => {
  ElMessage.info(`加载文件: ${file.name}`)
}

// 重置视图
const resetView = () => {
  if (controls) {
    controls.reset()
    camera.position.set(5, 5, 5)
    camera.lookAt(0, 0, 0)
  }
}

// 缩放
const zoomIn = () => {
  if (camera) {
    camera.zoom *= 1.1
    camera.updateProjectionMatrix()
  }
}

const zoomOut = () => {
  if (camera) {
    camera.zoom /= 1.1
    camera.updateProjectionMatrix()
  }
}

// 切换线框模式
const toggleWireframe = () => {
  wireframe.value = !wireframe.value
  if (model) {
    model.traverse((object) => {
      if (object instanceof THREE.Mesh) {
        object.material.wireframe = wireframe.value
      }
    })
  }
}

// 自动绑定骨骼
const autoRig = () => {
  ElMessage.info('骨骼绑定功能开发中')
}

// 加载动画
const loadAnimation = (anim: any) => {
  ElMessage.info(`加载动画: ${anim.name}`)
}

// 播放动画
const playAnimation = () => {
  isPlaying.value = true
}

const pauseAnimation = () => {
  isPlaying.value = false
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
}

const goToFirstFrame = () => {
  currentFrame.value = 0
}

const goToLastFrame = () => {
  currentFrame.value = totalFrames.value
}

const prevFrame = () => {
  if (currentFrame.value > 0) {
    currentFrame.value--
  }
}

const nextFrame = () => {
  if (currentFrame.value < totalFrames.value) {
    currentFrame.value++
  }
}

// 导出模型
const exportModel = () => {
  ElMessage.info('模型导出功能开发中')
}

// 跳转到模板页面
const goToTemplates = () => {
  router.push('/templates')
}

// AI聊天面板拖拽功能
const startDrag = (e: MouseEvent) => {
  isDragging.value = true
  dragOffset.value = {
    x: e.clientX - chatPanel.value.x,
    y: e.clientY - chatPanel.value.y
  }
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e: MouseEvent) => {
  if (!isDragging.value) return
  chatPanel.value.x = e.clientX - dragOffset.value.x
  chatPanel.value.y = e.clientY - dragOffset.value.y
  
  // 边界限制
  const maxX = window.innerWidth - 400
  const maxY = window.innerHeight - 100
  chatPanel.value.x = Math.max(0, Math.min(chatPanel.value.x, maxX))
  chatPanel.value.y = Math.max(0, Math.min(chatPanel.value.y, maxY))
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 最小化聊天面板
const toggleMinimize = () => {
  chatPanel.value.minimized = !chatPanel.value.minimized
}

// 发送AI消息
const sendAIMessage = () => {
  if (!aiForm.value.description.trim()) return
  
  // 添加用户消息
  chatMessages.value.push({
    role: 'user',
    content: aiForm.value.description
  })
  
  const userDesc = aiForm.value.description
  aiForm.value.description = ''
  
  // 滚动到底部
  setTimeout(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  }, 50)
  
  // 模拟AI响应
  setTimeout(() => {
    chatMessages.value.push({
      role: 'ai',
      content: `正在根据您的描述"${userDesc}"生成模型，风格：${aiForm.value.style}，请稍候...`
    })
    setTimeout(() => {
      if (chatMessagesRef.value) {
        chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
      }
    }, 50)
  }, 1000)
}

// 生成模型
const generateModel = () => {
  ElMessage.info('AI生成功能开发中')
  showAIModal.value = false
}

// 处理上传成功
const handleUploadSuccess = (response: any) => {
  ElMessage.success('文件上传成功')
  showUploadModal.value = false
}

// 处理上传错误
const handleUploadError = (error: any) => {
  ElMessage.error('文件上传失败')
}

// 提交上传
const submitUpload = () => {
  // 触发上传
  const uploader = document.querySelector('.el-upload__input') as HTMLInputElement
  if (uploader) {
    uploader.click()
  }
}

// 导航到指定步骤
const goToStep = (stepId: string) => {
  currentStep.value = stepId
}

// 上一步
const prevStep = () => {
  const currentIndex = processSteps.value.findIndex(step => step.id === currentStep.value)
  if (currentIndex > 0) {
    currentStep.value = processSteps.value[currentIndex - 1].id
  }
}

// 下一步
const nextStep = () => {
  const currentIndex = processSteps.value.findIndex(step => step.id === currentStep.value)
  if (currentIndex < processSteps.value.length - 1) {
    currentStep.value = processSteps.value[currentIndex + 1].id
  }
}

// 保存项目
const saveProject = () => {
  ElMessage.success('项目保存成功')
}

// 返回主页
const goHome = () => {
  router.push('/')
}

// 生命周期钩子
onMounted(() => {
  initScene()
  // 从路由参数获取项目信息
  const projectId = route.query.projectId
  if (projectId) {
    projectName.value = `项目 ${projectId}`
  }
})

onUnmounted(() => {
  // 清理3D场景
  if (renderer) {
    renderer.dispose()
  }
  if (model) {
    scene.remove(model)
  }
})
</script>

<style scoped>
/* ========== 基础布局 ========== */
.modeling-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #e0e0e0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ========== 顶部标题栏 ========== */
.top-bar {
  height: 48px;
  background: rgba(26, 26, 46, 0.95);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  flex-shrink: 0;
  backdrop-filter: blur(10px);
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.home-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.home-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  color: #fff;
}

.project-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-name {
  font-weight: 600;
  color: #fff;
  font-size: 14px;
}

.project-name {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
}

.top-bar-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.workflow-steps {
  display: flex;
  gap: 4px;
  background: rgba(0, 0, 0, 0.3);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 12px;
}

.workflow-step:hover {
  background: rgba(102, 126, 234, 0.2);
  color: #fff;
}

.workflow-step.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.workflow-step.completed {
  color: #67c23a;
}

.step-icon {
  font-size: 14px;
}

.step-label {
  white-space: nowrap;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.top-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: #aaa;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.top-btn:hover {
  background: #3a3a3a;
  color: #fff;
}

/* ========== 主工作区 ========== */
.workspace {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* ========== 侧边栏通用样式 ========== */
.sidebar-left,
.sidebar-right {
  width: 280px;
  background: rgba(26, 26, 46, 0.9);
  border-right: 1px solid rgba(102, 126, 234, 0.15);
  display: flex;
  flex-direction: column;
  position: relative;
  transition: width 0.3s ease;
  backdrop-filter: blur(10px);
}

.sidebar-right {
  border-right: none;
  border-left: 1px solid rgba(102, 126, 234, 0.15);
}

.sidebar-left.collapsed,
.sidebar-right.collapsed {
  width: 24px;
}

.sidebar-toggle {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 48px;
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(102, 126, 234, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.6);
  z-index: 10;
  transition: all 0.2s;
}

.sidebar-left .sidebar-toggle {
  right: -8px;
  border-radius: 0 6px 6px 0;
}

.sidebar-right .sidebar-toggle {
  left: -8px;
  border-radius: 6px 0 0 6px;
}

.sidebar-toggle:hover {
  background: rgba(102, 126, 234, 0.4);
  color: #fff;
}

.sidebar-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(102, 126, 234, 0.15);
}

.sidebar-header h3 {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ========== 左侧工作流程列表 ========== */
.workflow-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.workflow-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 4px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.workflow-item:hover {
  background: rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
}

.workflow-item.active {
  background: rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.5);
}

.workflow-item.completed {
  border-left: 3px solid #67c23a;
}

.workflow-number {
  width: 24px;
  height: 24px;
  background: rgba(102, 126, 234, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  flex-shrink: 0;
}

.workflow-item.active .workflow-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.workflow-item.completed .workflow-number {
  background: #67c23a;
  color: #fff;
}

.workflow-info {
  flex: 1;
}

.workflow-title {
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 2px;
}

.workflow-desc {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
}

.completed-icon {
  color: #67c23a;
  font-size: 16px;
}

/* ========== 3D视口区域 ========== */
.viewport-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #0f3460 0%, #16213e 50%, #1a1a2e 100%);
  position: relative;
}

.viewport-header {
  height: 36px;
  background: rgba(26, 26, 46, 0.9);
  border-bottom: 1px solid rgba(102, 126, 234, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
}

.viewport-tabs {
  display: flex;
  gap: 4px;
}

.viewport-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px 6px 0 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

.viewport-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.viewport-nav {
  display: flex;
  gap: 8px;
  align-items: center;
}

.viewport-nav .nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 16px;
  background: #333;
  border: 1px solid #444;
  border-radius: 4px;
  color: #ccc;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 12px;
}

.viewport-nav .nav-btn:hover:not(:disabled) {
  background: #444;
  color: #fff;
}

.viewport-nav .nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.viewport-nav .nav-btn.next {
  background: #4a9eff;
  border-color: #4a9eff;
  color: #fff;
}

.viewport-nav .nav-btn.next:hover:not(:disabled) {
  background: #3a8eef;
}

.viewport-tools {
  display: flex;
  gap: 4px;
}

.tool-btn {
  width: 28px;
  height: 28px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.tool-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  color: #fff;
}

.viewport-content {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.viewport-footer {
  height: 28px;
  background: rgba(26, 26, 46, 0.9);
  border-top: 1px solid rgba(102, 126, 234, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
}

.viewport-info {
  display: flex;
  gap: 16px;
}

.viewport-controls {
  display: flex;
  gap: 4px;
}

.control-btn {
  width: 24px;
  height: 24px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.control-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  color: #fff;
}

/* ========== 加载和空状态 ========== */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(26, 26, 46, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(102, 126, 234, 0.2);
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-model {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.5);
}

.no-model-icon {
  margin-bottom: 16px;
  color: rgba(102, 126, 234, 0.5);
}

.action-btn {
  margin-top: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* ========== 右侧面板标签 ========== */
.panel-tabs {
  display: flex;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(102, 126, 234, 0.15);
}

.panel-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.2s;
}

.panel-tab:hover {
  color: #fff;
  background: rgba(102, 126, 234, 0.15);
}

.panel-tab.active {
  color: #fff;
  border-bottom-color: #667eea;
  background: rgba(102, 126, 234, 0.2);
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* ========== 面板内容 ========== */
.panel-section {
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.control-group {
  margin-bottom: 20px;
}

.control-group label {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-group {
  display: flex;
  gap: 8px;
}

.btn-group.vertical {
  flex-direction: column;
}

.control-btn-primary,
.control-btn-secondary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.control-btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.control-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.control-btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.control-btn-secondary:hover {
  background: rgba(102, 126, 234, 0.2);
  color: #fff;
  border-color: rgba(102, 126, 234, 0.5);
}

.control-btn-primary.full-width {
  width: 100%;
}

.control-btn-icon {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.control-btn-icon:hover {
  background: rgba(102, 126, 234, 0.2);
  color: #fff;
}

.export-btn {
  width: 100%;
  margin-top: 8px;
}

/* ========== 设置项 ========== */
.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(102, 126, 234, 0.15);
}

.setting-item span {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* ========== 列表样式 ========== */
.recent-files,
.history-list,
.animation-list,
.outline-tree,
.material-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.recent-file,
.history-item,
.anim-item,
.outline-item,
.material-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 12px;
}

.recent-file:hover,
.history-item:hover,
.anim-item:hover,
.outline-item:hover,
.material-item:hover {
  background: rgba(102, 126, 234, 0.15);
}

.history-thumb,
.anim-preview,
.material-preview {
  width: 40px;
  height: 40px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.history-info,
.anim-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.history-info span,
.anim-info span {
  color: rgba(255, 255, 255, 0.9);
}

.history-info small,
.anim-info small {
  color: rgba(255, 255, 255, 0.5);
  font-size: 11px;
}

/* ========== 时间轴控制 ========== */
.timeline-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.timeline-slider {
  flex: 1;
}

/* ========== 底部时间轴 ========== */
.timeline-bar {
  height: 48px;
  background: rgba(26, 26, 46, 0.9);
  border-top: 1px solid rgba(102, 126, 234, 0.15);
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 16px;
}

.timeline-controls {
  display: flex;
  gap: 4px;
}

.timeline-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 6px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.timeline-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  color: #fff;
}

.timeline-btn.play {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: #fff;
}

.timeline-btn.play:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.timeline-slider-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.frame-number {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  font-variant-numeric: tabular-nums;
  min-width: 36px;
  text-align: center;
}

/* ========== Element Plus 深色主题覆盖 ========== */
:deep(.dark-select) {
  width: 100%;
}

:deep(.dark-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3);
}

:deep(.dark-select .el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
}

:deep(.dark-color-picker) {
  width: 100%;
}

:deep(.dark-color-picker .el-color-picker__trigger) {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(102, 126, 234, 0.3);
}

:deep(.dark-slider) {
  --el-slider-main-bg-color: #667eea;
  --el-slider-runway-bg-color: rgba(102, 126, 234, 0.2);
}

:deep(.dark-slider .el-slider__button) {
  border-color: #667eea;
  background: #667eea;
}

:deep(.dark-input-number) {
  width: 80px;
}

:deep(.dark-input-number .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3);
}

:deep(.dark-input-number .el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
}

:deep(.dark-switch) {
  --el-switch-on-color: #667eea;
  --el-switch-off-color: rgba(102, 126, 234, 0.3);
}

:deep(.dark-checkbox) {
  --el-checkbox-text-color: rgba(255, 255, 255, 0.8);
  --el-checkbox-checked-text-color: #fff;
  --el-checkbox-checked-bg-color: #667eea;
  --el-checkbox-checked-icon-color: #fff;
  --el-checkbox-checked-border-color: #667eea;
}

:deep(.dark-checkbox .el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #fff;
}

:deep(.dark-dialog) {
  background: rgba(26, 26, 46, 0.95);
}

:deep(.dark-dialog .el-dialog__header) {
  background: rgba(26, 26, 46, 0.9);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  margin-right: 0;
  padding: 16px 20px;
}

:deep(.dark-dialog .el-dialog__title) {
  color: #fff;
}

:deep(.dark-dialog .el-dialog__body) {
  background: rgba(26, 26, 46, 0.95);
  color: rgba(255, 255, 255, 0.9);
}

:deep(.dark-dialog .el-dialog__footer) {
  background: rgba(26, 26, 46, 0.9);
  border-top: 1px solid rgba(102, 126, 234, 0.2);
}

:deep(.dark-dialog .el-upload) {
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(102, 126, 234, 0.4);
  border-radius: 12px;
}

:deep(.dark-dialog .el-upload__text) {
  color: rgba(255, 255, 255, 0.8);
}

:deep(.dark-dialog .el-upload__text em) {
  color: #667eea;
}

/* ========== AI聊天面板样式 ========== */
.ai-chat-panel {
  position: fixed;
  width: 400px;
  background: rgba(26, 26, 46, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  z-index: 1000;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(102, 126, 234, 0.3);
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.2) 100%);
  border-bottom: 1px solid rgba(102, 126, 234, 0.2);
  cursor: move;
  user-select: none;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

.chat-title .el-icon {
  color: #a78bfa;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.chat-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.chat-btn:hover {
  background: rgba(102, 126, 234, 0.4);
  color: #fff;
}

.chat-btn.close:hover {
  background: #ef4444;
  color: #fff;
}

.chat-body {
  display: flex;
  flex-direction: column;
  height: 280px;
}

.chat-messages {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
}

.message.ai {
  align-self: flex-start;
  background: rgba(102, 126, 234, 0.2);
  color: #e0e0e0;
  border-bottom-left-radius: 4px;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message-content {
  word-wrap: break-word;
}

.chat-input-area {
  padding: 12px;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  background: rgba(0, 0, 0, 0.2);
}

.chat-input-area .el-textarea__inner {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #fff;
  border-radius: 8px;
  resize: none;
}

.chat-input-area .el-textarea__inner:focus {
  border-color: #667eea;
}

.chat-input-area .el-textarea__inner::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.input-actions .el-select .el-input__wrapper {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(102, 126, 234, 0.3);
  box-shadow: none;
}

.input-actions .el-select .el-input__inner {
  color: rgba(255, 255, 255, 0.9);
}

/* ========== 滚动条样式 ========== */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(26, 26, 46, 0.5);
}

::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.4);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.6);
}

/* ========== 响应式 ========== */
@media (max-width: 1200px) {
  .workflow-step .step-label {
    display: none;
  }
  
  .sidebar-left,
  .sidebar-right {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .sidebar-left,
  .sidebar-right {
    position: absolute;
    z-index: 100;
    height: 100%;
  }
  
  .sidebar-left {
    left: 0;
  }
  
  .sidebar-right {
    right: 0;
  }
  
  .sidebar-left.collapsed,
  .sidebar-right.collapsed {
    transform: translateX(-100%);
  }
  
  .sidebar-right.collapsed {
    transform: translateX(100%);
  }
}
</style>
