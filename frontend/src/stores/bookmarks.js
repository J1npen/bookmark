import { defineStore } from 'pinia'
import { listBookmarks, createBookmark, deleteBookmark } from '../api/index.js'

export const useBookmarkStore = defineStore('bookmarks', {
  state: () => ({
    items: [],
    loading: false,
    activeTag: '',
    keyword: '',
  }),
  actions: {
    async load() {
      this.loading = true
      try {
        const params = {}
        if (this.activeTag) params.tag = this.activeTag
        if (this.keyword) params.keyword = this.keyword
        const res = await listBookmarks(params)
        this.items = Array.isArray(res.data) ? res.data : (res.data.results ?? [])
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
      await this.load()
    },
  },
})
