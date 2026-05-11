import { defineStore } from 'pinia'
import { listBookmarks, createBookmark, deleteBookmark } from '../api/index.js'

export const useBookmarkStore = defineStore('bookmarks', {
  state: () => ({
    items: [],
    total: 0,
    page: 1,
    pageSize: Number(localStorage.getItem('bm_pageSize')) || 8,
    loading: false,
    activeTag: '',
    keyword: '',
  }),
  getters: {
    totalPages: state => Math.max(1, Math.ceil(state.total / state.pageSize)),
  },
  actions: {
    async load() {
      this.loading = true
      try {
        const params = {
          page: this.page,
          page_size: this.pageSize,
        }
        if (this.activeTag) params.tag = this.activeTag
        if (this.keyword) params.keyword = this.keyword
        const res = await listBookmarks(params)
        if (Array.isArray(res.data)) {
          this.items = res.data
          this.total = res.data.length
        } else {
          this.items = res.data.results ?? []
          this.total = res.data.count ?? this.items.length
        }
      } finally {
        this.loading = false
      }
    },
    async create(data) {
      await createBookmark(data)
      await this.load()
    },
    async remove(id) {
      await deleteBookmark(id)
      // 当前页删完后退一页
      if (this.items.length === 1 && this.page > 1) this.page--
      await this.load()
    },
  },
})
