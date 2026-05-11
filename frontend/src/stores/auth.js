import { defineStore } from 'pinia'
import { login as apiLogin, logout as apiLogout, primeCsrf } from '../api/index.js'
import http from '../api/http.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    username: localStorage.getItem('bm_username') || '',
    checked: false,
  }),
  actions: {
    async check() {
      await primeCsrf()
      try {
        const res = await http.get('/api/bookmarks/')
        this.user = res.status === 200 ? 'authenticated' : null
      } catch {
        this.user = null
      }
      this.checked = true
    },
    async login(username, password) {
      const ok = await apiLogin(username, password)
      if (ok) {
        this.user = 'authenticated'
        this.username = username
        localStorage.setItem('bm_username', username)
      }
      return ok
    },
    async logout() {
      await apiLogout()
      this.user = null
      this.username = ''
      localStorage.removeItem('bm_username')
    },
  },
})
