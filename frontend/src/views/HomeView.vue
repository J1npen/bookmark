<template>
  <div class="home">
    <header class="header">
      <h1>书签</h1>
      <div class="header-actions">
        <input v-model="keyword" placeholder="搜索…" @keyup.enter="search" />
        <button @click="search">搜索</button>
        <button @click="showAddForm = true">+ 新增</button>
        <button @click="doLogout">退出</button>
      </div>
    </header>

    <div class="layout">
      <!-- 标签侧边栏 -->
      <aside class="sidebar">
        <div
          class="tag-item"
          :class="{ active: activeTag === '' }"
          @click="setTag('')"
        >全部</div>
        <div
          v-for="tag in tagStore.items"
          :key="tag.id"
          class="tag-item"
          :class="{ active: activeTag === tag.slug }"
          :style="{ borderLeft: `3px solid ${tag.color}` }"
          @click="setTag(tag.slug)"
        >{{ tag.name }}</div>
      </aside>

      <!-- 书签列表 -->
      <main class="content">
        <div v-if="bmStore.loading">加载中…</div>
        <div v-else-if="bmStore.items.length === 0">暂无书签</div>
        <div v-else class="grid">
          <div v-for="bm in bmStore.items" :key="bm.id" class="card">
            <div class="card-title">
              <img v-if="bm.favicon_url" :src="bm.favicon_url" class="favicon" />
              <a :href="bm.url" target="_blank">{{ bm.title || bm.url }}</a>
            </div>
            <p class="card-desc">{{ bm.description }}</p>
            <div class="card-tags">
              <span
                v-for="tag in bm.tags"
                :key="tag.id"
                class="tag-badge"
                :style="{ background: tag.color }"
              >{{ tag.name }}</span>
            </div>
            <button class="del-btn" @click="remove(bm.id)">删除</button>
          </div>
        </div>
      </main>
    </div>

    <!-- 新增书签表单 -->
    <div v-if="showAddForm" class="modal-overlay" @click.self="showAddForm = false">
      <div class="modal">
        <h2>新增书签</h2>
        <input v-model="newUrl" placeholder="URL" />
        <input v-model="newTitle" placeholder="标题（可选）" />
        <button @click="addBookmark" :disabled="!newUrl">保存</button>
        <button @click="showAddForm = false">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { useBookmarkStore } from '../stores/bookmarks.js'
import { useTagStore } from '../stores/tags.js'

const auth = useAuthStore()
const bmStore = useBookmarkStore()
const tagStore = useTagStore()
const router = useRouter()

const activeTag = ref('')
const keyword = ref('')
const showAddForm = ref(false)
const newUrl = ref('')
const newTitle = ref('')

onMounted(async () => {
  await tagStore.load()
  await bmStore.load()
})

function setTag(slug) {
  activeTag.value = slug
  bmStore.activeTag = slug
  bmStore.load()
}

function search() {
  bmStore.keyword = keyword.value
  bmStore.load()
}

async function addBookmark() {
  await bmStore.create({ url: newUrl.value, title: newTitle.value })
  showAddForm.value = false
  newUrl.value = ''
  newTitle.value = ''
}

async function remove(id) {
  if (confirm('确认删除？')) await bmStore.remove(id)
}

async function doLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.home { display: flex; flex-direction: column; height: 100vh; }
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; border-bottom: 1px solid #ddd;
}
.header-actions { display: flex; gap: 8px; align-items: center; }
.header-actions input { padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px; }
.header-actions button { padding: 6px 12px; border-radius: 4px; border: 1px solid #ccc; cursor: pointer; }
.layout { display: flex; flex: 1; overflow: hidden; }
.sidebar { width: 160px; border-right: 1px solid #ddd; overflow-y: auto; padding: 8px 0; }
.tag-item {
  padding: 8px 12px; cursor: pointer; font-size: 13px;
  border-left: 3px solid transparent;
}
.tag-item:hover { background: #f5f5f5; }
.tag-item.active { background: #eef; }
.content { flex: 1; overflow-y: auto; padding: 16px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.card { border: 1px solid #ddd; border-radius: 6px; padding: 12px; position: relative; }
.card-title { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
.card-title a { font-weight: 500; text-decoration: none; color: #333; }
.card-title a:hover { text-decoration: underline; }
.favicon { width: 16px; height: 16px; }
.card-desc { font-size: 12px; color: #666; margin-bottom: 8px; }
.card-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 6px; }
.tag-badge { font-size: 11px; color: #fff; padding: 2px 6px; border-radius: 10px; }
.del-btn { font-size: 12px; color: #e33; background: none; border: none; cursor: pointer; padding: 0; }
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
}
.modal {
  background: #fff; border-radius: 8px; padding: 24px;
  display: flex; flex-direction: column; gap: 10px; width: 320px;
}
.modal input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.modal button { padding: 8px; border-radius: 4px; border: 1px solid #ccc; cursor: pointer; }
</style>
