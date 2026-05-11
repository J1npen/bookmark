<template>
  <!-- Background blobs -->
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
  <div class="blob blob-4"></div>

  <!-- 移动端遮罩 -->
  <div class="scrim" :class="{ open: drawerOpen }" @click="closeDrawer"></div>

  <!-- 移动端抽屉 -->
  <aside class="drawer" :class="{ open: drawerOpen }">
    <div class="drawer-head">
      <div class="drawer-brand">书<span>·</span>签</div>
      <button class="icon-btn" @click="closeDrawer" aria-label="关闭菜单">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>
    <div class="drawer-scroll">
      <div class="nav-label">资料库</div>
      <button class="nav-item" :class="{ active: activeTag === '' }" @click="setTag('')">
        <span class="dot"></span>全部书签
        <span class="nav-count">{{ bmStore.total }}</span>
      </button>
      <template v-if="tagStore.items.length">
        <div class="nav-label">标签</div>
        <button
          v-for="tag in tagStore.items"
          :key="tag.id"
          class="nav-item"
          :class="{ active: activeTag === tag.slug }"
          @click="setTag(tag.slug)"
        >
          <span class="dot" :style="{ color: tag.color || 'var(--ink-dim)' }"></span>
          {{ tag.name }}
        </button>
      </template>
    </div>
    <div class="drawer-foot">
      <div class="avatar">{{ userInitial }}</div>
      <div class="user-info">
        <div class="user-name">{{ auth.username || '用户' }}</div>
        <div class="user-sub">书签管理器</div>
      </div>
    </div>
  </aside>

  <div class="layout">
    <!-- ── Sidebar ── -->
    <aside class="sidebar">
      <div class="brand">书<span>·</span>签</div>
      <div class="brand-sub">BOOKMARK MANAGER</div>

      <div class="sidebar-scroll">
        <div class="nav-label">资料库</div>
        <button class="nav-item" :class="{ active: activeTag === '' }" @click="setTag('')">
          <span class="dot"></span>
          全部书签
          <span class="nav-count">{{ bmStore.total }}</span>
        </button>

        <template v-if="tagStore.items.length">
          <div class="nav-label">标签</div>
          <button
            v-for="tag in tagStore.items"
            :key="tag.id"
            class="nav-item"
            :class="{ active: activeTag === tag.slug }"
            @click="setTag(tag.slug)"
          >
            <span class="dot" :style="{ color: tag.color || 'var(--ink-dim)' }"></span>
            {{ tag.name }}
          </button>
        </template>
      </div>

      <div class="sidebar-footer-wrap" @click.stop>
        <Transition name="menu-up">
          <div v-if="footerMenuOpen" class="footer-menu">
            <button class="footer-menu-item" @click="openSettings">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
              设置
            </button>
            <div class="footer-menu-sep"></div>
            <button class="footer-menu-item footer-menu-logout" @click="doLogout">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              退出登录
            </button>
          </div>
        </Transition>

        <div class="sidebar-footer" @click="toggleFooterMenu">
          <div class="avatar">{{ userInitial }}</div>
          <div class="user-info">
            <div class="user-name">{{ auth.username || '用户' }}</div>
            <div class="user-sub">书签管理器</div>
          </div>
          <svg class="footer-chevron" :class="{ open: footerMenuOpen }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"/>
          </svg>
        </div>
      </div>
    </aside>

    <!-- ── Main ── -->
    <main class="main">
      <!-- Topbar -->
      <div class="topbar">
        <!-- 移动端顶栏行 -->
        <div class="topbar-mobile-row">
          <button class="icon-btn" @click="openDrawer" aria-label="打开菜单">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="14" y2="18"/>
            </svg>
          </button>
          <div class="mobile-brand">书<span>·</span>签</div>
          <button class="icon-btn icon-btn-primary" @click="showAddForm = true" aria-label="添加书签">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </button>
          <button class="icon-btn icon-btn-ghost" @click="doLogout" aria-label="登出">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </button>
        </div>
        <div class="search" @click="focusSearch">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.5;flex-shrink:0">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            ref="searchInput"
            v-model="keyword"
            placeholder="搜索书签、标签或域名…"
            @keyup.enter="search"
            @input="debouncedSearch"
          />
          <span class="kbd">⌘K</span>
        </div>
        <div class="top-actions">
          <button class="btn btn-primary" @click="showAddForm = true">＋ 新建书签</button>
        </div>
      </div>

      <!-- 移动端标签芯片 -->
      <div class="chips-wrap">
        <div class="chips">
          <div class="chip" :class="{ active: activeTag === '' }" @click="setTag('')">
            全部 <span class="chip-count">{{ bmStore.total }}</span>
          </div>
          <div
            v-for="tag in tagStore.items"
            :key="tag.id"
            class="chip"
            :class="{ active: activeTag === tag.slug }"
            @click="setTag(tag.slug)"
          >
            {{ tag.name }}
          </div>
        </div>
      </div>

      <!-- Header -->
      <div class="header">
        <h1 v-if="!activeTag">全部<em>书签</em></h1>
        <h1 v-else>{{ activeTagName }}</h1>
        <p v-if="bmStore.total > 0">
          共 {{ bmStore.total }} 条书签
          <template v-if="latestTime"> · 最近添加于 {{ latestTime }}</template>
        </p>
        <p v-else-if="!bmStore.loading" style="color:var(--ink-faint)">暂无书签</p>
      </div>

      <!-- Cards -->
      <div v-if="bmStore.loading" class="state-msg">加载中…</div>
      <div v-else-if="bmStore.items.length === 0" class="state-msg">
        暂无书签，点击右上角新建
      </div>
      <div v-else class="grid">
        <article
          v-for="bm in bmStore.items"
          :key="bm.id"
          class="card"
          @click="openUrl(bm)"
        >
          <div class="card-head">
            <div class="favicon-wrap">
              <img
                v-if="bm.favicon_url && !failedFavicons[bm.id]"
                :src="bm.favicon_url"
                class="favicon-img"
                @error="failedFavicons[bm.id] = true"
              />
              <div v-else class="favicon-letter" :style="{ background: domainGradient(bm.url) }">
                {{ domainLetter(bm.url) }}
              </div>
            </div>
            <div class="domain">{{ extractDomain(bm.url) }}</div>
            <button class="card-edit" @click.stop="openEditModal(bm)" title="编辑书签">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="card-del" @click.stop="remove(bm.id)" title="删除书签">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <h3>{{ bm.title || bm.url }}</h3>
          <p v-if="bm.description">{{ bm.description }}</p>
          <div class="card-foot">
            <div class="tags">
              <span v-for="tag in bm.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
            </div>
            <div class="meta">{{ bm.visit_count ?? 0 }} 次浏览</div>
            <div class="card-actions-mobile">
              <span class="visits">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                </svg>
                {{ bm.visit_count ?? 0 }}
              </span>
              <button class="card-act-btn" @click.stop="openEditModal(bm)" aria-label="编辑">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
              <button class="card-act-btn del" @click.stop="remove(bm.id)" aria-label="删除">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1.5 14a2 2 0 0 1-2 2h-7a2 2 0 0 1-2-2L5 6"/>
                  <path d="M10 11v6M14 11v6"/>
                </svg>
              </button>
            </div>
          </div>
        </article>
      </div>

      <!-- Pagination -->
      <div v-if="bmStore.totalPages > 1" class="pagination">
        <div class="page-info">
          共 {{ bmStore.total }} 条
          <span class="page-sep">·</span>
          第 {{ bmStore.page }} / {{ bmStore.totalPages }} 页
        </div>
        <div class="page-controls">
          <button class="page-btn" :disabled="bmStore.page <= 1" @click="prevPage">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
            上一页
          </button>
          <div class="page-jump">
            <input
              v-model.number="jumpInput"
              type="number"
              :min="1"
              :max="bmStore.totalPages"
              @change="doJump"
            />
            <span class="page-slash">/ {{ bmStore.totalPages }}</span>
          </div>
          <button class="page-btn" :disabled="bmStore.page >= bmStore.totalPages" @click="nextPage">
            下一页
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
        </div>
      </div>
    </main>
  </div>

  <!-- ── Settings Modal ── -->
  <Transition name="fade">
    <div v-if="showSettings" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h2>设置</h2>
          <button class="modal-close" @click="showSettings = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-field">
          <label>每页显示书签数量</label>
          <input v-model.number="settingsPageSize" type="number" min="1" max="100" placeholder="默认 8" />
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showSettings = false">取消</button>
          <button class="btn btn-primary modal-save" @click="saveSettings">保存</button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- ── Add Bookmark Modal ── -->
  <Transition name="fade">
    <div v-if="showAddForm" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? '编辑书签' : '新建书签' }}</h2>
          <button class="modal-close" @click="closeModal">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-field">
          <label>URL</label>
          <div class="url-row">
            <input
              v-model="form.url"
              placeholder="https://…"
              @blur="autoFetchOnBlur"
            />
            <button
              class="btn fetch-btn"
              :disabled="describing || !form.url"
              @click="describe"
            >
              {{ describing ? '生成中…' : '获取描述' }}
            </button>
          </div>
        </div>

        <div class="modal-field">
          <label>标题</label>
          <input v-model="form.title" placeholder="网页标题（可自动识别）" />
        </div>

        <div class="modal-field">
          <label>描述 <span class="opt">（可选）</span></label>
          <textarea v-model="form.description" placeholder="简要描述这个网页…" rows="2"></textarea>
        </div>

        <div class="modal-field">
          <label>Favicon URL <span class="opt">（可选）</span></label>
          <input v-model="form.favicon_url" placeholder="https://…/favicon.ico" />
        </div>

        <div v-if="tagStore.items.length" class="modal-field">
          <label>标签</label>
          <div class="tag-checks">
            <label
              v-for="tag in tagStore.items"
              :key="tag.id"
              class="tag-check"
              :class="{ selected: form.tagIds.includes(tag.id) }"
            >
              <input type="checkbox" :value="tag.id" v-model="form.tagIds" class="sr-only" />
              <span class="tag-color-dot" :style="{ background: tag.color || '#888' }"></span>
              {{ tag.name }}
            </label>
          </div>
        </div>

        <div class="modal-actions">
          <button class="btn" @click="closeModal">取消</button>
          <button class="btn btn-primary modal-save" :disabled="!form.url || saving" @click="save">
            {{ saving ? '保存中…' : (editingId ? '保存修改' : '保存书签') }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useBookmarkStore } from '../stores/bookmarks.js'
import { useTagStore } from '../stores/tags.js'
import { fetchUrlMeta, describeUrl, updateBookmark, visitBookmark } from '../api/index.js'

const auth = useAuthStore()
const bmStore = useBookmarkStore()
const tagStore = useTagStore()
const router = useRouter()

const activeTag = ref('')
const keyword = ref('')
const showAddForm = ref(false)
const showSettings = ref(false)
const footerMenuOpen = ref(false)
const settingsPageSize = ref(bmStore.pageSize)
const searchInput = ref(null)
const fetching = ref(false)
const describing = ref(false)
const saving = ref(false)
const editingId = ref(null)
const failedFavicons = reactive({})
const jumpInput = ref(1)
const drawerOpen = ref(false)

// 翻页状态与 store.page 保持同步
watch(() => bmStore.page, v => { jumpInput.value = v })

const form = reactive({
  url: '',
  title: '',
  description: '',
  tagIds: [],
  favicon_url: '',
})

const userInitial = computed(() => {
  const name = auth.username || ''
  return name ? name[0].toUpperCase() : 'U'
})

const activeTagName = computed(() => {
  const tag = tagStore.items.find(t => t.slug === activeTag.value)
  return tag?.name || ''
})

const latestTime = computed(() => {
  if (!bmStore.items.length) return ''
  return timeAgo(bmStore.items[0].created_at)
})

onMounted(async () => {
  await Promise.all([tagStore.load(), bmStore.load()])
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('click', handleDocClick)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('click', handleDocClick)
})

function openDrawer() { drawerOpen.value = true }
function closeDrawer() { drawerOpen.value = false }

function handleKeydown(e) {
  if (e.key === 'Escape') {
    if (showAddForm.value) closeModal()
    else if (showSettings.value) showSettings.value = false
    else if (footerMenuOpen.value) footerMenuOpen.value = false
    else if (drawerOpen.value) closeDrawer()
  }
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    searchInput.value?.focus()
  }
}

function handleDocClick() {
  footerMenuOpen.value = false
}

function toggleFooterMenu() {
  footerMenuOpen.value = !footerMenuOpen.value
}

function openSettings() {
  settingsPageSize.value = bmStore.pageSize
  footerMenuOpen.value = false
  showSettings.value = true
}

function saveSettings() {
  const size = Math.max(1, Math.min(100, Math.round(settingsPageSize.value) || 8))
  localStorage.setItem('bm_pageSize', size)
  bmStore.pageSize = size
  bmStore.page = 1
  bmStore.load()
  showSettings.value = false
}

function setTag(slug) {
  activeTag.value = slug
  bmStore.activeTag = slug
  bmStore.keyword = ''
  bmStore.page = 1
  keyword.value = ''
  bmStore.load()
  closeDrawer()
}

let searchTimer = null
function debouncedSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(search, 350)
}

function search() {
  bmStore.keyword = keyword.value
  bmStore.page = 1
  bmStore.load()
}

function prevPage() {
  if (bmStore.page > 1) {
    bmStore.page--
    bmStore.load()
  }
}

function nextPage() {
  if (bmStore.page < bmStore.totalPages) {
    bmStore.page++
    bmStore.load()
  }
}

function doJump() {
  const p = Math.max(1, Math.min(bmStore.totalPages, Math.round(Number(jumpInput.value)) || 1))
  jumpInput.value = p
  if (p !== bmStore.page) {
    bmStore.page = p
    bmStore.load()
  }
}

function focusSearch() {
  searchInput.value?.focus()
}

async function autoFetch() {
  const url = form.url.trim()
  if (!url) return
  fetching.value = true
  try {
    const res = await fetchUrlMeta(url)
    if (res.data.title && !form.title) form.title = res.data.title
    if (res.data.favicon_url) form.favicon_url = res.data.favicon_url
  } catch {
    // ignore network errors
  } finally {
    fetching.value = false
  }
}

function autoFetchOnBlur() {
  if (form.url.trim().startsWith('http') && !form.title) {
    autoFetch()
  }
}

function openEditModal(bm) {
  editingId.value = bm.id
  Object.assign(form, {
    url: bm.url,
    title: bm.title,
    description: bm.description || '',
    favicon_url: bm.favicon_url || '',
    tagIds: (bm.tags || []).map(t => t.id),
  })
  showAddForm.value = true
}

async function describe() {
  const url = form.url.trim()
  if (!url) return
  describing.value = true
  try {
    const res = await describeUrl(url)
    if (res.data.description) form.description = res.data.description
  } catch {
    // ignore
  } finally {
    describing.value = false
  }
}

async function save() {
  saving.value = true
  try {
    const payload = {
      url: form.url.trim(),
      title: form.title || form.url.trim(),
      description: form.description,
      favicon_url: form.favicon_url,
      tag_ids: form.tagIds,
    }
    if (editingId.value) {
      await updateBookmark(editingId.value, payload)
      await bmStore.load()
    } else {
      await bmStore.create(payload)
    }
    closeModal()
  } finally {
    saving.value = false
  }
}

function closeModal() {
  showAddForm.value = false
  editingId.value = null
  Object.assign(form, { url: '', title: '', description: '', tagIds: [], favicon_url: '' })
}

async function remove(id) {
  if (confirm('确认删除此书签？')) await bmStore.remove(id)
}

function openUrl(bm) {
  window.open(bm.url, '_blank', 'noopener,noreferrer')
  visitBookmark(bm.id).catch(() => {})
}

async function doLogout() {
  footerMenuOpen.value = false
  await auth.logout()
  router.push('/login')
}

// ── Utilities ──
function extractDomain(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '')
  } catch {
    return url
  }
}

function domainLetter(url) {
  return extractDomain(url)[0]?.toUpperCase() || '?'
}

const GRADIENTS = [
  'linear-gradient(135deg,#24292e,#586069)',
  'linear-gradient(135deg,#42b883,#35495e)',
  'linear-gradient(135deg,#fc466b,#3f5efb)',
  'linear-gradient(135deg,#ff6b9d,#c9a4ff)',
  'linear-gradient(135deg,#0db7ed,#384d54)',
  'linear-gradient(135deg,#ffb47a,#ff6b9d)',
  'linear-gradient(135deg,#7dd6a7,#5b8def)',
  'linear-gradient(135deg,#c9a4ff,#5b8def)',
]

function domainGradient(url) {
  const d = extractDomain(url)
  const idx = ((d.charCodeAt(0) || 0) + (d.charCodeAt(1) || 0)) % GRADIENTS.length
  return GRADIENTS[idx]
}

function timeAgo(dateStr) {
  if (!dateStr) return ''
  const diff = Date.now() - new Date(dateStr).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 1) return '刚刚'
  if (m < 60) return `${m} 分钟前`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h} 小时前`
  const d = Math.floor(h / 24)
  if (d < 30) return `${d} 天前`
  const mo = Math.floor(d / 30)
  if (mo < 12) return `${mo} 个月前`
  return `${Math.floor(mo / 12)} 年前`
}
</script>

<style scoped>
/* ── Blobs ── */
.blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.55;
  z-index: 0;
  pointer-events: none;
  animation: drift 22s ease-in-out infinite alternate;
}
.blob-1 { width: 600px; height: 600px; background: #ff6b9d; top: -150px; left: -100px; }
.blob-2 { width: 500px; height: 500px; background: #5b8def; top: 20%; right: -120px; animation-delay: -7s; }
.blob-3 { width: 700px; height: 700px; background: #c9a4ff; bottom: -200px; left: 30%; animation-delay: -14s; }
.blob-4 { width: 400px; height: 400px; background: var(--accent); top: 50%; left: 40%; animation-delay: -3s; opacity: 0.35; }

/* ── Layout ── */
.layout {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
  gap: 24px;
  padding: 24px;
}

/* ── Sidebar ── */
.sidebar {
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 28px 20px 10px;
  height: calc(100vh - 48px);
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 4px 0 8px;
  /* 顶部和底部渐变蒙版，让滚动边缘自然淡出 */
  mask-image: linear-gradient(
    to bottom,
    transparent 0,
    black 28px,
    black calc(100% - 28px),
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to bottom,
    transparent 0,
    black 28px,
    black calc(100% - 28px),
    transparent 100%
  );
  /* Firefox scrollbar */
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}
.sidebar:hover .sidebar-scroll {
  scrollbar-color: rgba(244, 241, 234, 0.18) transparent;
}

/* Webkit scrollbar — 默认隐藏，hover sidebar 才显示 */
.sidebar-scroll::-webkit-scrollbar {
  width: 3px;
}
.sidebar-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.sidebar-scroll::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 2px;
  transition: background 0.25s ease;
}
.sidebar:hover .sidebar-scroll::-webkit-scrollbar-thumb {
  background: rgba(244, 241, 234, 0.2);
}
.sidebar:hover .sidebar-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(244, 241, 234, 0.38);
}

.brand {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: 26px;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
  color: var(--ink);
}
.brand span { color: var(--accent); margin: 0 4px; }

.brand-sub {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 36px;
}

.nav-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin: 24px 8px 10px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13.5px;
  font-family: var(--font-sans);
  color: var(--ink-dim);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 2px;
  background: none;
  border: 1px solid transparent;
  width: 100%;
  text-align: left;
}
.nav-item:hover { background: var(--glass-hover); color: var(--ink); }
.nav-item.active {
  background: rgba(255, 180, 122, 0.12);
  color: var(--accent);
  border-color: rgba(255, 180, 122, 0.2);
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.7;
  flex-shrink: 0;
}

.nav-count {
  margin-left: auto;
  font-family: var(--font-mono);
  font-size: 11px;
  opacity: 0.5;
}

/* ── Sidebar Footer ── */
.sidebar-footer-wrap {
  margin-top: auto;
  position: relative;
}

.sidebar-footer {
  border-top: 1px solid var(--glass-border);
  margin-top: 12px;
  padding: 14px 8px 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border-radius: 12px;
  transition: background 0.2s;
}
.sidebar-footer:hover { background: var(--glass-hover); }

.footer-chevron {
  color: var(--ink-faint);
  flex-shrink: 0;
  transition: transform 0.25s ease;
}
.footer-chevron.open { transform: rotate(180deg); }

.footer-menu {
  position: absolute;
  bottom: calc(100% + 4px);
  left: 0;
  right: 0;
  background: rgba(18, 12, 28, 0.97);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 6px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  z-index: 20;
}

.footer-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  font-size: 13.5px;
  font-family: var(--font-sans);
  color: var(--ink-dim);
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  text-align: left;
}
.footer-menu-item:hover { background: var(--glass-hover); color: var(--ink); }
.footer-menu-logout:hover { color: #ff6b9d; background: rgba(255, 107, 157, 0.08); }

.footer-menu-sep {
  height: 1px;
  background: var(--glass-border);
  margin: 4px 0;
}

/* menu-up transition */
.menu-up-enter-active { transition: opacity 0.18s ease, transform 0.18s ease; }
.menu-up-leave-active { transition: opacity 0.14s ease, transform 0.14s ease; }
.menu-up-enter-from { opacity: 0; transform: translateY(6px); }
.menu-up-leave-to { opacity: 0; transform: translateY(6px); }

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: grid;
  place-items: center;
  font-weight: 600;
  font-size: 13px;
  color: #0a0612;
  font-family: var(--font-serif);
  flex-shrink: 0;
}

.user-info { flex: 1; min-width: 0; }
.user-name { font-weight: 500; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.user-sub { font-size: 11px; color: var(--ink-faint); }


/* ── Main ── */
.main { padding: 8px 12px 48px; }

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40px;
  gap: 20px;
}

.search {
  flex: 1;
  max-width: 480px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  padding: 11px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: text;
}
.search input {
  background: transparent;
  border: none;
  outline: none;
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 13.5px;
  flex: 1;
  min-width: 0;
}
.search input::placeholder { color: var(--ink-faint); }

.kbd {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-faint);
  border: 1px solid var(--glass-border);
  padding: 2px 6px;
  border-radius: 4px;
  flex-shrink: 0;
}

.top-actions { display: flex; gap: 10px; }

.btn {
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--glass-border);
  color: var(--ink);
  padding: 10px 18px;
  border-radius: 999px;
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.btn:hover:not(:disabled) { background: var(--glass-hover); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-primary {
  background: var(--accent);
  color: #2a1810;
  border-color: transparent;
}
.btn-primary:hover:not(:disabled) { background: #ffc99a; }

/* ── Header ── */
.header { margin-bottom: 32px; }

.header h1 {
  font-family: var(--font-serif);
  font-weight: 300;
  font-size: 56px;
  letter-spacing: 0.02em;
  line-height: 1.1;
  margin-bottom: 10px;
  color: var(--ink);
}
.header h1 em {
  font-style: normal;
  color: var(--accent);
  font-weight: 500;
}
.header p {
  color: var(--ink-dim);
  font-size: 14px;
}

/* ── State ── */
.state-msg {
  color: var(--ink-faint);
  font-size: 14px;
  padding: 40px 0;
}

/* ── Grid ── */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* ── Card ── */
.card {
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 20px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent 50%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
.card:hover {
  transform: translateY(-4px);
  background: var(--glass-hover);
  border-color: rgba(255,255,255,0.2);
}

.card-head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.favicon-wrap { width: 36px; height: 36px; flex-shrink: 0; }

.favicon-img {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  object-fit: cover;
}

.favicon-letter {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 14px;
  color: #fff;
  font-family: var(--font-mono);
}

.domain {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-faint);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.card-edit,
.card-del {
  opacity: 0;
  background: none;
  border: none;
  color: var(--ink-faint);
  cursor: pointer;
  padding: 5px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}
.card:hover .card-edit,
.card:hover .card-del { opacity: 1; }
.card-edit:hover { color: #5b8def; background: rgba(91, 141, 239, 0.1); }
.card-del:hover { color: #ff6b9d; background: rgba(255, 107, 157, 0.1); }

.card h3 {
  font-family: var(--font-serif);
  font-weight: 500;
  font-size: 15px;
  line-height: 1.4;
  letter-spacing: 0.01em;
  margin-bottom: 8px;
  color: var(--ink);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card p {
  font-size: 13px;
  color: var(--ink-dim);
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid var(--glass-border);
  gap: 8px;
}

.tags { display: flex; gap: 6px; flex-wrap: wrap; flex: 1; min-width: 0; }

.tag {
  font-size: 11px;
  padding: 3px 9px;
  border-radius: 6px;
  background: rgba(255,255,255,0.06);
  color: var(--ink-dim);
  white-space: nowrap;
}

.meta {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--ink-faint);
  flex-shrink: 0;
}

/* ── Modal ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 6, 18, 0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal {
  background: rgba(18, 12, 28, 0.97);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 28px 28px 10px;
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 0 24px 80px rgba(0,0,0,0.5);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.modal h2 {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: 20px;
  color: var(--ink);
}
.modal-close {
  background: none;
  border: none;
  color: var(--ink-faint);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}
.modal-close:hover { color: var(--ink); }

.modal-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.modal-field label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--ink-faint);
}
.opt { font-size: 10px; text-transform: none; letter-spacing: 0; }

.modal-field input,
.modal-field textarea {
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 11px 14px;
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  resize: none;
}
.modal-field input:focus,
.modal-field textarea:focus { border-color: rgba(255, 180, 122, 0.4); }
.modal-field input::placeholder,
.modal-field textarea::placeholder { color: var(--ink-faint); }

.url-row { display: flex; gap: 8px; }
.url-row input { flex: 1; }

.fetch-btn {
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 12px;
  flex-shrink: 0;
}

.tag-checks { display: flex; flex-wrap: wrap; gap: 8px; }

.tag-check {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 10px;
  border: 1px solid var(--glass-border);
  background: rgba(255,255,255,0.04);
  cursor: pointer;
  font-size: 13px;
  color: var(--ink-dim);
  transition: all 0.2s;
  user-select: none;
}
.tag-check:hover { background: var(--glass-hover); color: var(--ink); }
.tag-check.selected {
  background: rgba(255, 180, 122, 0.12);
  border-color: rgba(255, 180, 122, 0.3);
  color: var(--accent);
}

.tag-color-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 10px;
  border-top: 1px solid var(--glass-border);
}
.modal-actions .btn { border-radius: 12px; }
.modal-save { border-radius: 12px; }

/* ── Fade Transition ── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ── Pagination ── */
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 36px;
  padding-top: 20px;
  border-top: 1px solid var(--glass-border);
  gap: 16px;
  flex-wrap: wrap;
}

.page-info {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-faint);
  letter-spacing: 0.03em;
}
.page-sep { margin: 0 6px; opacity: 0.5; }

.page-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  color: var(--ink-dim);
  padding: 7px 14px;
  border-radius: 10px;
  font-family: var(--font-sans);
  font-size: 12.5px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.page-btn:hover:not(:disabled) { background: var(--glass-hover); color: var(--ink); }
.page-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.page-jump {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  padding: 6px 12px;
  transition: border-color 0.2s;
}
.page-jump:focus-within { border-color: rgba(255, 180, 122, 0.35); }

.page-jump input {
  background: transparent;
  border: none;
  outline: none;
  color: var(--ink);
  font-family: var(--font-mono);
  font-size: 13px;
  width: 32px;
  text-align: center;
  -moz-appearance: textfield;
}
.page-jump input::-webkit-outer-spin-button,
.page-jump input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

.page-slash {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-faint);
  white-space: nowrap;
}

/* ── 移动端新增基础类（默认隐藏）── */
.scrim { display: none; }
.drawer { display: none; }
.topbar-mobile-row { display: none; }
.mobile-brand { display: none; font-family: var(--font-serif); font-size: 20px; font-weight: 500; letter-spacing: 0.05em; flex: 1; margin-left: 4px; }
.mobile-brand span { color: var(--accent); margin: 0 3px; }
.chips-wrap { display: none; }
.card-actions-mobile { display: none; }

.icon-btn {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  color: var(--ink);
  display: grid; place-items: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s;
}
.icon-btn:active { background: var(--glass-hover); transform: scale(0.95); }
.icon-btn-primary { background: var(--accent); border-color: transparent; color: #2a1810; }
.icon-btn-primary:active { background: #ffc99a; }
.icon-btn-ghost { background: transparent; border-color: rgba(255,255,255,0.1); color: var(--ink-dim); }
.icon-btn-ghost:active { background: rgba(255,107,138,0.1); color: var(--danger); }

.visits {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 8px; border-radius: 6px;
  background: rgba(255,180,122,0.08); border: 1px solid rgba(255,180,122,0.15);
  color: var(--accent); font-family: var(--font-mono); font-size: 10.5px;
  margin-right: 2px;
}
.visits svg { stroke: currentColor; opacity: 0.85; }

.card-act-btn {
  width: 26px; height: 26px; border-radius: 7px;
  background: transparent; border: none; color: var(--ink-faint);
  display: grid; place-items: center; cursor: pointer;
  transition: color 0.15s, background 0.15s;
}
.card-act-btn:active { background: var(--glass-hover); color: var(--ink); }
.card-act-btn.del:active { background: rgba(255,107,138,0.1); color: var(--danger); }

.chip {
  flex-shrink: 0; padding: 7px 14px; border-radius: 999px;
  background: var(--glass-bg); border: 1px solid var(--glass-border);
  font-size: 12.5px; color: var(--ink-dim); white-space: nowrap; cursor: pointer;
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
  transition: transform 0.15s;
}
.chip:active { transform: scale(0.94); }
.chip.active { background: var(--ink); color: #0a0612; border-color: var(--ink); font-weight: 500; }
.chip-count { font-family: var(--font-mono); font-size: 10.5px; margin-left: 4px; opacity: 0.55; }
.chip.active .chip-count { opacity: 0.6; }

/* ── Responsive ── */
@media (max-width: 900px) {
  /* 隐藏桌面端元素 */
  .sidebar { display: none; }
  .top-actions { display: none; }
  .card-edit, .card-del { display: none; }
  .meta { display: none; }
  .kbd { display: none; }
  .header { display: none; }

  /* 布局 */
  .layout { grid-template-columns: 1fr; padding: 0; gap: 0; }
  .main { padding: 0; overflow-x: hidden; }

  /* 粘性顶栏 */
  .topbar {
    position: sticky; top: 0; z-index: 50;
    background: rgba(10,6,18,0.65);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: calc(var(--safe-top) + 12px) 14px 12px;
    margin-bottom: 0;
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  /* 移动端顶栏行 */
  .topbar-mobile-row { display: flex; align-items: center; gap: 8px; }
  .mobile-brand { display: block; }

  /* 搜索框 */
  .search { max-width: none; }
  .search input:focus { font-size: 16px; }

  /* 标签芯片 */
  .chips-wrap { display: block; padding: 14px 0 8px; overflow: hidden; }
  .chips {
    display: flex; gap: 8px; padding: 0 16px;
    overflow-x: auto; overflow-y: hidden;
    -webkit-overflow-scrolling: touch; scrollbar-width: none;
    scroll-snap-type: x proximity;
  }
  .chips::-webkit-scrollbar { display: none; }

  /* 卡片网格 */
  .grid { display: flex; flex-direction: column; gap: 12px; padding: 0 16px 24px; }

  /* 卡片交互 */
  .card:active { transform: scale(0.98); }
  .card:hover { transform: none; background: var(--glass-bg); border-color: var(--glass-border); }

  /* 移动端卡片操作区 */
  .card-actions-mobile { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }

  /* 分页 */
  .pagination {
    padding: 4px 16px calc(16px + var(--safe-bottom));
    margin-top: 4px;
    border-top: 1px solid var(--glass-border);
    flex-direction: column;
    align-items: center;
  }

  /* 遮罩 */
  .scrim {
    display: block;
    position: fixed; inset: 0; z-index: 200;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s;
  }
  .scrim.open { opacity: 1; pointer-events: auto; }

  /* 抽屉 */
  .drawer {
    display: flex; flex-direction: column;
    position: fixed; top: 0; bottom: 0; left: 0;
    width: min(82%, 320px); z-index: 201;
    background: rgba(20,14,32,0.92);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    border-right: 1px solid var(--glass-border);
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
    padding: calc(var(--safe-top) + 24px) 0 calc(var(--safe-bottom) + 16px);
    overflow: hidden;
  }
  .drawer.open { transform: translateX(0); }

  .drawer-head {
    padding: 0 24px 20px;
    border-bottom: 1px solid var(--glass-border);
    display: flex; align-items: center; justify-content: space-between;
  }
  .drawer-brand { font-family: var(--font-serif); font-size: 24px; font-weight: 500; letter-spacing: 0.05em; }
  .drawer-brand span { color: var(--accent); margin: 0 3px; }
  .drawer-scroll {
    flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch;
    padding: 16px 16px 8px; overscroll-behavior: contain;
  }
  .drawer-foot {
    padding: 16px 24px 0; border-top: 1px solid var(--glass-border);
    display: flex; align-items: center; gap: 10px;
  }
}

@media (max-width: 900px) {
  .url-row { flex-direction: column; }
  .url-row .fetch-btn { width: 100%; text-align: center; }
}

@media (max-width: 360px) {
  .card { padding: 14px; }
  .mobile-brand { font-size: 18px; }
  .topbar-mobile-row { gap: 6px; }
  .page-btn { padding: 8px 10px; font-size: 12px; }
}
</style>
