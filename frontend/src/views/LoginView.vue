<template>
  <div class="login-page">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <div class="login-card">
      <div class="brand">书<span>·</span>签</div>
      <div class="brand-sub">BOOKMARK MANAGER</div>

      <p v-if="error" class="error-msg">{{ error }}</p>

      <div class="fields">
        <input
          v-model="username"
          type="text"
          placeholder="用户名"
          autocomplete="username"
          @keyup.enter="doLogin"
        />
        <input
          v-model="password"
          type="password"
          placeholder="密码"
          autocomplete="current-password"
          @keyup.enter="doLogin"
        />
        <button class="btn-login" @click="doLogin" :disabled="loading">
          {{ loading ? '登录中…' : '登录' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function doLogin() {
  if (!username.value || !password.value) return
  loading.value = true
  error.value = ''
  const ok = await auth.login(username.value, password.value)
  if (ok) {
    router.push('/')
  } else {
    error.value = '用户名或密码错误'
  }
  loading.value = false
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

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

.login-card {
  position: relative;
  z-index: 2;
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 28px;
  padding: 44px 40px;
  width: 360px;
  display: flex;
  flex-direction: column;
}

.brand {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: 32px;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
  color: var(--ink);
}
.brand span { color: var(--accent); margin: 0 4px; }

.brand-sub {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-bottom: 32px;
}

.error-msg {
  color: #ff6b9d;
  font-size: 13px;
  padding: 10px 14px;
  background: rgba(255, 107, 157, 0.1);
  border: 1px solid rgba(255, 107, 157, 0.2);
  border-radius: 10px;
  margin-bottom: 16px;
}

.fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.fields input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 13px 16px;
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.fields input:focus { border-color: rgba(255, 180, 122, 0.5); }
.fields input::placeholder { color: var(--ink-faint); }

.btn-login {
  margin-top: 8px;
  background: var(--accent);
  color: #2a1810;
  border: none;
  border-radius: 12px;
  padding: 13px;
  font-family: var(--font-sans);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  letter-spacing: 0.04em;
}
.btn-login:hover:not(:disabled) { background: #ffc99a; }
.btn-login:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
