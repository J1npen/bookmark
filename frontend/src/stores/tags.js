import { defineStore } from 'pinia'
import { listTags } from '../api/index.js'

export const useTagStore = defineStore('tags', {
  state: () => ({
    items: [],
  }),
  actions: {
    async load() {
      const res = await listTags()
      this.items = res.data
    },
  },
})
