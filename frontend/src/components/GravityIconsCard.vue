<template>
  <div class="gravity-card">
    <div class="physics-stage" ref="stageRef">
      <div class="grid-bg" aria-hidden="true"></div>
      <Transition name="hint-fade">
        <div v-if="icons.length === 0" class="empty-hint">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
          <span>从右侧添加图标</span>
        </div>
      </Transition>
      <div
        v-for="icon in icons"
        :key="icon.id"
        class="icon-disc"
        :class="{ 'has-url': icon.url }"
        :style="{
          width: DISC_SIZE + 'px',
          height: DISC_SIZE + 'px',
          background: (icon.faviconUrl && icon.faviconLoaded && !icon.faviconError) ? 'transparent' : icon.bg,
          transform: `translate(${icon.x}px, ${icon.y}px) rotate(${icon.angle}rad)`,
        }"
        @click="handleIconClick(icon, $event)"
      >
        <div v-if="icon.svg" class="icon-inner" v-html="icon.svg"></div>
        <!-- favicon：img 与 fallback 叠层，交叉淡入淡出 -->
        <div v-else-if="icon.faviconUrl" class="favicon-stack">
          <span
            class="icon-fallback"
            :style="{ opacity: icon.faviconLoaded && !icon.faviconError ? 0 : 1 }"
          >{{ icon.label?.[0]?.toUpperCase() }}</span>
          <img
            class="icon-img"
            :src="icon.faviconUrl"
            :alt="icon.label"
            :style="{ opacity: icon.faviconLoaded && !icon.faviconError ? 1 : 0 }"
            @load="icon.faviconLoaded = true"
            @error="icon.faviconError = true"
          />
        </div>
        <span v-else class="icon-fallback">{{ icon.label?.[0]?.toUpperCase() }}</span>
      </div>
    </div>
    <div class="card-body">
      <h2 class="card-title">{{ title }}</h2>
      <p class="card-desc">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Matter from 'matter-js'

defineProps({
  title:       { type: String, default: '所有 AI 工具，一处管理' },
  description: { type: String, default: '连接主流 AI 模型，从单一界面快速访问，更快更简洁。' },
})

const DISC_SIZE = 72
const DISC_R    = 36

const stageRef = ref(null)
const icons    = ref([])   // 默认空，通过 addIcon() 动态添加

let engine = null
let world  = null
let bodies = {}
let rafId  = null
let resizeObserver = null
let idCounter = 0

// 点击 vs 拖拽判断
let mouseDownX = 0
let mouseDownY = 0
function onMouseDown(e) { mouseDownX = e.clientX; mouseDownY = e.clientY }

function handleIconClick(icon, event) {
  const dx = event.clientX - mouseDownX
  const dy = event.clientY - mouseDownY
  if (dx * dx + dy * dy > 36) return  // 移动超过 6px → 是拖拽，不是点击
  if (!icon.url) return
  window.open(icon.url, '_blank', 'noopener,noreferrer')
}

/* ── 核心：动态添加图标 ────────────────────── */
function addIcon(def) {
  const id = def.id ? `${def.id}-${++idCounter}` : `icon-${++idCounter}`
  const icon = { ...def, id, x: 0, y: 0, angle: 0, faviconLoaded: false, faviconError: false }
  icons.value.push(icon)

  if (engine && world && stageRef.value) {
    const W = stageRef.value.offsetWidth
    const x = DISC_R + 10 + Math.random() * Math.max(0, W - DISC_SIZE - 20)
    const y = DISC_R + 10
    const body = Matter.Bodies.circle(x, y, DISC_R - 2, {
      restitution: 0.5,
      friction:    0.05,
      frictionAir: 0.008,
      density:     0.002,
      label:       id,
    })
    Matter.Body.setVelocity(body, {
      x: (Math.random() - 0.5) * 5,
      y: 1 + Math.random() * 2,
    })
    bodies[id] = body
    Matter.Composite.add(world, body)
  }
}

defineExpose({ addIcon })

/* ── 物理引擎 ─────────────────────────────── */
function initPhysics() {
  const stage = stageRef.value
  if (!stage) return
  const W = stage.offsetWidth
  const H = stage.offsetHeight

  engine = Matter.Engine.create({ gravity: { y: 0.35 } })
  world  = engine.world

  Matter.Composite.add(world, [
    Matter.Bodies.rectangle(W / 2,   H + 25,   W + 100, 50,    { isStatic: true }),
    Matter.Bodies.rectangle(-25,     H / 2,    50,      H * 2, { isStatic: true }),
    Matter.Bodies.rectangle(W + 25,  H / 2,    50,      H * 2, { isStatic: true }),
    Matter.Bodies.rectangle(W / 2,  -25,       W + 100, 50,    { isStatic: true }),
  ])

  // 已有图标（resize 后重建）需恢复物理体
  icons.value.forEach(icon => {
    if (bodies[icon.id]) return
    const x = DISC_R + 10 + Math.random() * Math.max(0, W - DISC_SIZE - 20)
    const y = icon.y + DISC_R  // 尽量保持原位
    const body = Matter.Bodies.circle(x, y, DISC_R - 2, {
      restitution: 0.5, friction: 0.05, frictionAir: 0.008, density: 0.002, label: icon.id,
    })
    bodies[icon.id] = body
    Matter.Composite.add(world, body)
  })

  // 鼠标拖拽约束
  const mouse = Matter.Mouse.create(stage)
  const mc = Matter.MouseConstraint.create(engine, {
    mouse,
    constraint: { stiffness: 0.2, render: { visible: false } },
  })
  // 释放拖拽后缩减速度，避免过猛飞出
  Matter.Events.on(mc, 'enddrag', event => {
    if (!event.body) return
    const v = event.body.velocity
    Matter.Body.setVelocity(event.body, { x: v.x * 0.15, y: v.y * 0.15 })
  })
  Matter.Composite.add(world, mc)

  stage.addEventListener('mousedown', onMouseDown)
  stage.addEventListener('wheel', onWheel, { passive: false })
  stage.addEventListener('touchmove', preventScroll, { passive: false })

  function tick() {
    Matter.Engine.update(engine, 1000 / 60)
    icons.value.forEach(icon => {
      const body = bodies[icon.id]
      if (!body) return
      icon.x     = body.position.x - DISC_R
      icon.y     = body.position.y - DISC_R
      icon.angle = body.angle
    })
    rafId = requestAnimationFrame(tick)
  }
  rafId = requestAnimationFrame(tick)
}

function preventScroll(e) { e.preventDefault() }

function onWheel(e) {
  e.preventDefault()
  if (!engine || !world) return
  const stage = stageRef.value
  const rect = stage.getBoundingClientRect()
  const px = e.clientX - rect.left
  const py = e.clientY - rect.top

  // 找到鼠标下方的非静态物理体
  const hit = Matter.Query.point(Matter.Composite.allBodies(world), { x: px, y: py })
    .find(b => !b.isStatic)
  if (!hit) return

  // 随机方向冲量，速度区间 4–9，叠加到当前速度后限制最大值
  const angle = Math.random() * Math.PI * 2
  const kick  = 4 + Math.random() * 5
  const vx = hit.velocity.x + Math.cos(angle) * kick
  const vy = hit.velocity.y + Math.sin(angle) * kick
  const total = Math.sqrt(vx * vx + vy * vy)
  const CAP = 12
  Matter.Body.setVelocity(hit, total > CAP
    ? { x: vx / total * CAP, y: vy / total * CAP }
    : { x: vx, y: vy }
  )
}

function cleanup() {
  if (rafId)  { cancelAnimationFrame(rafId); rafId = null }
  if (world)  Matter.Composite.clear(world)
  if (engine) Matter.Engine.clear(engine)
  engine = null
  world  = null
  bodies = {}
  stageRef.value?.removeEventListener('mousedown', onMouseDown)
  stageRef.value?.removeEventListener('wheel', onWheel)
  stageRef.value?.removeEventListener('touchmove', preventScroll)
}

onMounted(() => {
  initPhysics()
  let firstFire = true
  resizeObserver = new ResizeObserver(() => {
    if (firstFire) { firstFire = false; return }
    cleanup()
    initPhysics()
  })
  resizeObserver.observe(stageRef.value)
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  cleanup()
})
</script>

<style scoped>
.gravity-card {
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5);
}

.physics-stage {
  position: relative;
  overflow: hidden;
  background: #0f0d18;
  height: 300px;
}

.grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
}

/* 空状态提示 */
.empty-hint {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.2);
  font-size: 0.85rem;
  pointer-events: none;
}

.hint-fade-enter-active, .hint-fade-leave-active { transition: opacity 0.4s; }
.hint-fade-enter-from, .hint-fade-leave-to { opacity: 0; }

/* 图标圆盘 */
.icon-disc {
  position: absolute;
  left: 0; top: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  user-select: none;
  will-change: transform;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.12), 0 6px 20px rgba(0, 0, 0, 0.45);
  transition: box-shadow 0.15s;
}
.icon-disc:active { cursor: grabbing; box-shadow: 0 0 0 2px rgba(255,255,255,0.3), 0 12px 32px rgba(0,0,0,0.6); }
.icon-disc.has-url { cursor: grab; }
.icon-disc.has-url:active { cursor: grabbing; }

.icon-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.icon-inner svg { width: 36px; height: 36px; }

/* favicon 叠层容器：img 与 fallback 绝对定位叠放，交叉淡入淡出 */
.favicon-stack {
  position: relative;
  width: 42px;
  height: 42px;
  pointer-events: none;
}

.favicon-stack .icon-fallback,
.favicon-stack .icon-img {
  position: absolute;
  inset: 0;
  margin: auto;
  transition: opacity 0.25s ease;
}

.icon-img {
  width: 42px;
  height: 42px;
  object-fit: contain;
  border-radius: 4px;
  pointer-events: none;
  display: block;
}

.icon-fallback {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  pointer-events: none;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 文字区 */
.card-body {
  background: #0a0612;
  padding: 24px 28px 28px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.card-title {
  margin: 0 0 8px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #f0eefc;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.card-desc {
  margin: 0;
  font-size: 0.88rem;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.6;
}
</style>
