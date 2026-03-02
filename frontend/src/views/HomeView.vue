<template>
  <div class="home-view">
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
      <div class="gradient-overlay"></div>
    </div>

    <div class="top-buttons">
      <router-link to="/library" class="btn-top">
        <span class="btn-icon">📁</span>我的项目库
      </router-link>
      <router-link to="/profile" class="btn-top">
        <span class="btn-icon">👤</span>个人中心
      </router-link>
    </div>
    
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-highlight">3D AI</span>
          <span class="title-main">角色创作平台</span>
        </h1>
        <p class="subtitle">使用AI技术快速创建3D角色模型</p>
        <div class="cta-buttons">
          <router-link to="/create" class="btn-primary">
            <span class="btn-icon">✨</span>
            <span class="btn-text">开始创作</span>
          </router-link>
          <router-link to="/gallery" class="btn-gallery">
            <span class="btn-icon">🎨</span>
            <span class="btn-text">公共画廊</span>
          </router-link>
        </div>
      </div>
    </div>

    <div class="features-section">
      <h2>核心功能</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>AI智能生成</h3>
          <p>通过文字描述自动生成3D角色</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🎨</div>
          <h3>在线编辑</h3>
          <p>实时预览和调整模型细节</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📦</div>
          <h3>多格式导出</h3>
          <p>支持多种3D模型格式导出</p>
        </div>
      </div>
    </div>

    <div class="quick-start">
      <h2>快速开始</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h4>选择创作方式</h4>
            <p>AI生成、上传模型或使用模板</p>
          </div>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h4>编辑和优化</h4>
            <p>使用3D编辑器调整模型</p>
          </div>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h4>导出使用</h4>
            <p>下载模型应用到你的项目</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'

const bubbles = ref<Array<{
  x: number
  duration: number
  delay: number
  size: number
  type: string
}>>([])

const silhouetteTypes = [
  'man-running',
  'woman-running', 
  'child-jumping',
  'man-walking',
  'woman-dancing',
  'elder-walking',
  'boy-running',
  'girl-jumping'
]

const getSilhouette = (type: string) => {
  const silhouettes: Record<string, any> = {
    'man-running': h('path', { 
      d: 'M50 15 L55 25 L65 30 L60 45 L70 60 L65 75 L55 85 L45 85 L35 75 L40 60 L30 45 L35 30 L45 25 Z',
      fill: 'currentColor'
    }),
    'woman-running': h('path', {
      d: 'M50 10 C55 10 60 15 60 20 C60 25 55 30 50 30 C45 30 40 25 40 20 C40 15 45 10 50 10 M50 35 L55 50 L65 55 L60 70 L70 85 L50 95 L30 85 L40 70 L35 55 L45 50 Z',
      fill: 'currentColor'
    }),
    'child-jumping': h('path', {
      d: 'M50 20 C55 20 58 23 58 28 C58 33 55 36 50 36 C45 36 42 33 42 28 C42 23 45 20 50 20 M50 42 L55 55 L50 70 L55 85 L45 85 L50 70 L45 55 Z',
      fill: 'currentColor'
    }),
    'man-walking': h('path', {
      d: 'M50 12 C56 12 61 17 61 23 C61 29 56 34 50 34 C44 34 39 29 39 23 C39 17 44 12 50 12 M50 40 L60 55 L55 70 L65 90 L55 90 L50 75 L45 90 L35 90 L45 70 L40 55 Z',
      fill: 'currentColor'
    }),
    'woman-dancing': h('path', {
      d: 'M50 8 C56 8 61 13 61 19 C61 25 56 30 50 30 C44 30 39 25 39 19 C39 13 44 8 50 8 M50 36 L58 50 L70 55 L75 70 L65 75 L55 60 L50 75 L45 60 L35 75 L25 70 L30 55 L42 50 Z',
      fill: 'currentColor'
    }),
    'elder-walking': h('path', {
      d: 'M50 15 C55 15 59 19 59 24 C59 29 55 33 50 33 C45 33 41 29 41 24 C41 19 45 15 50 15 M50 40 L55 52 L60 65 L70 85 L60 88 L52 70 L50 85 L48 70 L40 88 L30 85 L40 65 L45 52 Z',
      fill: 'currentColor'
    }),
    'boy-running': h('path', {
      d: 'M50 18 C54 18 57 21 57 25 C57 29 54 32 50 32 C46 32 43 29 43 25 C43 21 46 18 50 18 M50 38 L55 48 L62 52 L58 65 L68 78 L50 88 L32 78 L42 65 L38 52 L45 48 Z',
      fill: 'currentColor'
    }),
    'girl-jumping': h('path', {
      d: 'M50 15 C54 15 58 19 58 23 C58 27 54 31 50 31 C46 31 42 27 42 23 C42 19 46 15 50 15 M50 37 L54 47 L50 60 L54 75 L50 90 L46 75 L50 60 L46 47 Z',
      fill: 'currentColor'
    })
  }
  return silhouettes[type] || silhouettes['man-running']
}

onMounted(() => {
  for (let i = 0; i < 15; i++) {
    bubbles.value.push({
      x: Math.random() * 100,
      duration: 15 + Math.random() * 20,
      delay: Math.random() * 10,
      size: 80 + Math.random() * 60,
      type: silhouetteTypes[Math.floor(Math.random() * silhouetteTypes.length)]
    })
  }
})
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
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
  background: radial-gradient(circle at 30% 30%, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.15));
  border-radius: 50%;
  animation: float-up linear infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 0 30px rgba(255, 255, 255, 0.1),
    0 0 20px rgba(102, 126, 234, 0.2);
  backdrop-filter: blur(2px);
}

@keyframes float-up {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-120vh) rotate(360deg);
    opacity: 0;
  }
}

.silhouette {
  width: 60%;
  height: 60%;
  color: rgba(255, 255, 255, 0.6);
  filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5));
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(ellipse at 20% 20%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(118, 75, 162, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(15, 52, 96, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.top-buttons {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 12px;
  z-index: 100;
}

.btn-top {
  padding: 8px 16px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  backdrop-filter: blur(10px);
}

.btn-top:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.hero-section {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.hero-content {
  text-align: center;
  max-width: 900px;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 24px;
  line-height: 1.2;
}

.title-highlight {
  display: block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 5rem;
  text-shadow: none;
  filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
  animation: glow 3s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.5));
  }
  to {
    filter: drop-shadow(0 0 50px rgba(118, 75, 162, 0.8));
  }
}

.title-main {
  display: block;
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.subtitle {
  font-size: 1.4rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 50px;
  font-weight: 300;
  letter-spacing: 2px;
}

.cta-buttons {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary, .btn-gallery {
  padding: 20px 50px;
  border-radius: 60px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.2rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(135deg, #ffffff 0%, #f0f0ff 100%);
  color: #764ba2;
  border: none;
  box-shadow: 
    0 10px 40px rgba(255, 255, 255, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s;
}

.btn-primary:hover::before {
  left: 100%;
}

.btn-primary:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 
    0 20px 60px rgba(255, 255, 255, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2);
}

.btn-gallery {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  color: white;
  border: none;
  box-shadow: 
    0 10px 40px rgba(102, 126, 234, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.btn-gallery::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.btn-gallery:hover::before {
  left: 100%;
}

.btn-gallery:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 
    0 20px 60px rgba(118, 75, 162, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.2);
}

.btn-icon {
  font-size: 1.5rem;
}

.btn-text {
  position: relative;
  z-index: 1;
}

.features-section {
  position: relative;
  z-index: 1;
  padding: 100px 40px;
  background: linear-gradient(180deg, 
    rgba(15, 52, 96, 0.6) 0%, 
    rgba(22, 33, 62, 0.85) 10%,
    rgba(26, 26, 46, 0.95) 20%,
    rgba(40, 40, 60, 0.9) 35%,
    rgba(80, 80, 100, 0.7) 50%,
    rgba(120, 120, 140, 0.5) 65%,
    rgba(180, 180, 200, 0.3) 80%,
    rgba(240, 240, 250, 0.1) 95%,
    rgba(255, 255, 255, 0.98) 100%
  );
}

.features-section h2 {
  text-align: center;
  font-size: 2.8rem;
  margin-bottom: 60px;
  color: #fff;
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  text-align: center;
  padding: 50px 35px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(102, 126, 234, 0.25);
  backdrop-filter: blur(10px);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 60px rgba(102, 126, 234, 0.25);
  border-color: rgba(102, 126, 234, 0.5);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.08) 100%);
}

.feature-icon {
  font-size: 4rem;
  margin-bottom: 24px;
  display: block;
}

.feature-card h3 {
  font-size: 1.6rem;
  margin-bottom: 16px;
  color: #fff;
  font-weight: 700;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.8;
  font-size: 1rem;
}

.quick-start {
  position: relative;
  z-index: 1;
  padding: 100px 40px;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.98) 0%, 
    #f8f9ff 30%,
    #fff 100%
  );
}

.quick-start h2 {
  text-align: center;
  font-size: 2.8rem;
  margin-bottom: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.steps {
  display: flex;
  justify-content: center;
  gap: 50px;
  flex-wrap: wrap;
  max-width: 1100px;
  margin: 0 auto;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  max-width: 320px;
  padding: 30px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.step:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.3);
}

.step-number {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  font-weight: 800;
  flex-shrink: 0;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.step-content h4 {
  font-size: 1.3rem;
  margin-bottom: 10px;
  color: #1a1a2e;
  font-weight: 700;
}

.step-content p {
  color: #666;
  line-height: 1.7;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .title-highlight {
    font-size: 3rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .btn-primary, .btn-gallery {
    padding: 16px 35px;
    font-size: 1rem;
  }
  
  .cta-buttons {
    gap: 20px;
  }
  
  .features-section h2,
  .quick-start h2 {
    font-size: 2rem;
  }
}
</style>
