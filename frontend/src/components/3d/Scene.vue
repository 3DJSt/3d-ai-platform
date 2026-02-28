<template>
  <div ref="container" class="scene-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'

interface Props {
  width?: number
  height?: number
  backgroundColor?: string
  showGrid?: boolean
  showAxes?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  width: 800,
  height: 600,
  backgroundColor: '#f0f0f0',
  showGrid: true,
  showAxes: true
})

const container = ref<HTMLElement>()
const scene = ref<THREE.Scene>()
const camera = ref<THREE.PerspectiveCamera>()
const renderer = ref<THREE.WebGLRenderer>()
const controls = ref<OrbitControls>()

// 初始化场景
const initScene = () => {
  if (!container.value) return

  scene.value = new THREE.Scene()
  scene.value.background = new THREE.Color(props.backgroundColor)

  camera.value = new THREE.PerspectiveCamera(75, props.width / props.height, 0.1, 1000)
  camera.value.position.set(5, 5, 5)
  camera.value.lookAt(0, 0, 0)

  renderer.value = new THREE.WebGLRenderer({ antialias: true })
  renderer.value.setSize(props.width, props.height)
  renderer.value.setPixelRatio(window.devicePixelRatio)
  renderer.value.shadowMap.enabled = true

  controls.value = new OrbitControls(camera.value, renderer.value.domElement)
  controls.value.enableDamping = true
  controls.value.dampingFactor = 0.05

  // 环境光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.value.add(ambientLight)

  // 方向光
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(10, 10, 5)
  directionalLight.castShadow = true
  scene.value.add(directionalLight)

  // 网格
  if (props.showGrid) {
    const gridHelper = new THREE.GridHelper(20, 20)
    scene.value.add(gridHelper)
  }

  // 坐标轴
  if (props.showAxes) {
    const axesHelper = new THREE.AxesHelper(5)
    scene.value.add(axesHelper)
  }

  container.value.appendChild(renderer.value.domElement)
  animate()
}

// 动画循环
const animate = () => {
  requestAnimationFrame(animate)
  if (controls.value) controls.value.update()
  if (renderer.value && scene.value && camera.value) {
    renderer.value.render(scene.value, camera.value)
  }
}

// 加载 GLTF 模型
const loadGLTF = (url: string) => {
  if (!scene.value) return
  const loader = new GLTFLoader()
  loader.load(
    url,
    (gltf) => {
      scene.value?.add(gltf.scene)
    },
    undefined,
    (error) => {
      console.error('GLTF 加载失败:', error)
    }
  )
}

// 加载 OBJ 模型
const loadOBJ = (url: string) => {
  if (!scene.value) return
  const loader = new OBJLoader()
  loader.load(
    url,
    (object) => {
      scene.value?.add(object)
    },
    undefined,
    (error) => {
      console.error('OBJ 加载失败:', error)
    }
  )
}

// 响应尺寸变化
watch(
  () => [props.width, props.height],
  () => {
    if (camera.value && renderer.value) {
      camera.value.aspect = props.width / props.height
      camera.value.updateProjectionMatrix()
      renderer.value.setSize(props.width, props.height)
    }
  }
)

onMounted(() => {
  initScene()
})

onUnmounted(() => {
  if (renderer.value) renderer.value.dispose()
  if (controls.value) controls.value.dispose()
})

defineExpose({ loadGLTF, loadOBJ })
</script>

<style scoped>
.scene-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>