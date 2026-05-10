import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '../stores/auth.js'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/', component: HomeView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async to => {
  const auth = useAuthStore()
  if (!auth.checked) await auth.check()
  if (to.meta.requiresAuth && !auth.user) return '/login'
})

export default router
