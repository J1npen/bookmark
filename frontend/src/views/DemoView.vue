<template>
  <div class="demo-page">
    <div class="blob blob-1" aria-hidden="true"></div>
    <div class="blob blob-2" aria-hidden="true"></div>

    <div class="demo-layout">
      <!-- 重力卡片 -->
      <GravityIconsCard
        ref="cardRef"
        title="所有 AI 工具，一处管理"
        description="连接主流 AI 模型，从单一界面快速访问，更快更简洁。"
      />

      <!-- 添加面板 -->
      <div class="add-panel">
        <p class="panel-section-label">自定义添加</p>

        <div class="form-group">
          <label>网站 URL</label>
          <input
            v-model="form.url"
            type="url"
            placeholder="https://example.com"
            @keydown.enter="handleAddCustom"
          />
        </div>

        <div class="form-group">
          <label>Favicon 地址</label>
          <div class="input-row">
            <input
              v-model="form.faviconUrl"
              type="url"
              placeholder="https://example.com/favicon.ico"
              @keydown.enter="handleAddCustom"
            />
            <button class="btn-auto" title="自动填充" @click="autoFillFavicon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
          </div>
          <p v-if="form.url && !form.faviconUrl" class="field-hint">点击 ↑ 自动生成 favicon 地址</p>
        </div>

        <button class="btn-add" @click="handleAddCustom" :disabled="!form.url.trim()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          添加图标
        </button>

        <div class="divider"></div>

        <p class="panel-section-label">快速添加</p>
        <div class="preset-grid">
          <button
            v-for="def in ICON_DEFS"
            :key="def.id"
            class="preset-btn"
            :title="def.label"
            :style="{ background: def.bg }"
            @click="cardRef.addIcon(def)"
          >
            <div class="preset-icon" v-html="def.svg"></div>
          </button>
        </div>

        <button class="btn-add-all" @click="addAllPresets">全部添加</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import GravityIconsCard from '../components/GravityIconsCard.vue'

const cardRef = ref(null)

const form = reactive({ url: '', faviconUrl: '' })

/* ── 颜色轮换 ──────────────────────────────── */
const COLORS = ['#6C63FF','#E05C5C','#43CBFF','#F8B500','#00C9A7','#FF7C5C','#845EF7','#20C997','#FD7E14','#15AABF']
let colorIdx = 0
const nextColor = () => COLORS[colorIdx++ % COLORS.length]

/* ── 自动填充 favicon ──────────────────────── */
function autoFillFavicon() {
  if (!form.url.trim()) return
  try {
    const { origin } = new URL(form.url.trim())
    form.faviconUrl = `${origin}/favicon.ico`
  } catch {
    // 忽略无效 URL
  }
}

/* ── 自定义添加 ────────────────────────────── */
function handleAddCustom() {
  const url = form.url.trim()
  if (!url) return

  let label = url
  try { label = new URL(url).hostname.replace(/^www\./, '').split('.')[0] } catch {}

  cardRef.value.addIcon({
    id:         `custom-${Date.now()}`,
    label:      label,
    url:        url,
    bg:         nextColor(),
    faviconUrl: form.faviconUrl.trim() || null,
    svg:        null,
  })

  form.url = ''
  form.faviconUrl = ''
}

/* ── 预设图标 ──────────────────────────────── */
const ICON_DEFS = [
  {
    id: 'chatgpt', label: 'ChatGPT', bg: '#10A37F', url: 'https://chat.openai.com',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <circle cx="18" cy="18" r="4" fill="white"/>
      <g stroke="white" stroke-width="2.5" stroke-linecap="round">
        <line x1="18" y1="13" x2="18" y2="5"/>
        <line x1="22.3" y1="15.5" x2="29.3" y2="11.5"/>
        <line x1="22.3" y1="20.5" x2="29.3" y2="24.5"/>
        <line x1="18" y1="23" x2="18" y2="31"/>
        <line x1="13.7" y1="20.5" x2="6.7" y2="24.5"/>
        <line x1="13.7" y1="15.5" x2="6.7" y2="11.5"/>
      </g>
    </svg>`,
  },
  {
    id: 'claude', label: 'Claude', bg: '#D97706', url: 'https://claude.ai',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <circle cx="18" cy="18" r="5.5" stroke="white" stroke-width="2.5"/>
      <g stroke="white" stroke-width="2.5" stroke-linecap="round">
        <line x1="18" y1="4"  x2="18" y2="9"/>
        <line x1="18" y1="27" x2="18" y2="32"/>
        <line x1="4"  y1="18" x2="9"  y2="18"/>
        <line x1="27" y1="18" x2="32" y2="18"/>
        <line x1="7.5"  y1="7.5"  x2="11"  y2="11"/>
        <line x1="25"   y1="25"   x2="28.5" y2="28.5"/>
        <line x1="28.5" y1="7.5"  x2="25"   y2="11"/>
        <line x1="11"   y1="25"   x2="7.5"  y2="28.5"/>
      </g>
    </svg>`,
  },
  {
    id: 'gemini', label: 'Gemini', bg: '#4285F4', url: 'https://gemini.google.com',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <path d="M18 3 C18 3 19.8 14 28 18 C19.8 22 18 33 18 33 C18 33 16.2 22 8 18 C16.2 14 18 3 18 3Z" fill="white"/>
    </svg>`,
  },
  {
    id: 'perplexity', label: 'Perplexity', bg: '#1A5C7A', url: 'https://perplexity.ai',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <path d="M18 4 L25 9 L25 15 L31 18 L25 21 L25 27 L18 32 L11 27 L11 21 L5 18 L11 15 L11 9 Z"
        stroke="white" stroke-width="1.8" fill="none" stroke-linejoin="round"/>
      <circle cx="18" cy="18" r="3.5" fill="white"/>
    </svg>`,
  },
  {
    id: 'mistral', label: 'Mistral', bg: '#FF7000', url: 'https://mistral.ai',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <rect x="7"  y="9"  width="22" height="5" rx="2.5" fill="white"/>
      <rect x="7"  y="16" width="15" height="5" rx="2.5" fill="white"/>
      <rect x="7"  y="23" width="9"  height="5" rx="2.5" fill="white"/>
    </svg>`,
  },
  {
    id: 'deepseek', label: 'DeepSeek', bg: '#4D6BFE', url: 'https://chat.deepseek.com',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <path d="M7 21 C7 15 11 10 18 10 C25 10 29 15 29 19 C29 21 28 23 26 24 L28 29 L22 26 C21 26.5 19.5 27 18 27 C11 27 7 24 7 21 Z"
        stroke="white" stroke-width="2" fill="none" stroke-linejoin="round"/>
      <circle cx="13.5" cy="19" r="2" fill="white"/>
      <path d="M24 13 C26 11 28 9 31 8" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
    </svg>`,
  },
  {
    id: 'grok', label: 'Grok', bg: '#111111', url: 'https://grok.com',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <path d="M9 9 L27 27" stroke="white" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M27 9 L9 27" stroke="white" stroke-width="4.5" stroke-linecap="round"/>
    </svg>`,
  },
  {
    id: 'meta', label: 'Meta AI', bg: '#0082FB', url: 'https://ai.meta.com',
    svg: `<svg viewBox="0 0 36 36" fill="none">
      <path d="M7 18 C7 13.5 10 10.5 13.5 10.5 C16.5 10.5 18.5 13 20.5 16 C22.5 19 24.5 21.5 27.5 21.5 C30 21.5 33 19 33 15"
        stroke="white" stroke-width="2.8" fill="none" stroke-linecap="round"/>
      <path d="M33 18 C33 22.5 30 25.5 26.5 25.5 C23.5 25.5 21.5 23 19.5 20 C17.5 17 15.5 14.5 12.5 14.5 C10 14.5 7 17 7 21"
        stroke="white" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    </svg>`,
  },
]

function addAllPresets() {
  ICON_DEFS.forEach(def => cardRef.value.addIcon(def))
}
</script>

<style scoped>
.demo-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0a0612;
  position: relative;
  overflow: hidden;
  padding: 40px 24px;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.18;
  pointer-events: none;
}
.blob-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, #c9a4ff, transparent 70%);
  top: -100px; left: -100px;
  animation: blobFloat 12s ease-in-out infinite;
}
.blob-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #ffb47a, transparent 70%);
  bottom: -80px; right: -80px;
  animation: blobFloat 15s ease-in-out infinite reverse;
}
@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%  { transform: translate(30px, -30px) scale(1.05); }
  66%  { transform: translate(-20px, 20px) scale(0.97); }
}

/* 横向布局 */
.demo-layout {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  width: 100%;
  max-width: 860px;
}

/* 添加面板 */
.add-panel {
  flex-shrink: 0;
  width: 220px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 20px 16px;
  backdrop-filter: blur(12px);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.panel-section-label {
  margin: 0;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.3);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.5);
}

.form-group input {
  width: 100%;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 7px 10px;
  font-size: 0.8rem;
  color: #e8e4f0;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s;
}
.form-group input::placeholder { color: rgba(255, 255, 255, 0.2); }
.form-group input:focus { border-color: rgba(255, 255, 255, 0.25); }

.input-row {
  display: flex;
  gap: 6px;
}
.input-row input { flex: 1; }

.btn-auto {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.btn-auto:hover { background: rgba(255, 255, 255, 0.12); color: white; }

.field-hint {
  margin: 0;
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.25);
  line-height: 1.4;
}

.btn-add {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 12px;
  background: rgba(201, 164, 255, 0.15);
  border: 1px solid rgba(201, 164, 255, 0.25);
  border-radius: 10px;
  color: #c9a4ff;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.btn-add:hover:not(:disabled) { background: rgba(201, 164, 255, 0.25); border-color: rgba(201, 164, 255, 0.4); }
.btn-add:disabled { opacity: 0.35; cursor: not-allowed; }

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.07);
  margin: 2px 0;
}

/* 预设图标网格 */
.preset-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.preset-btn {
  aspect-ratio: 1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.15s, box-shadow 0.15s;
  overflow: hidden;
}
.preset-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
.preset-btn:active { transform: scale(0.95); }

.preset-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.preset-icon svg { width: 20px; height: 20px; }

.btn-add-all {
  padding: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.78rem;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.btn-add-all:hover { background: rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.7); }

/* 移动端：竖向堆叠 */
@media (max-width: 680px) {
  .demo-layout {
    flex-direction: column;
    align-items: stretch;
  }
  .add-panel {
    width: 100%;
  }
  .preset-grid {
    grid-template-columns: repeat(8, 1fr);
  }
}
</style>
