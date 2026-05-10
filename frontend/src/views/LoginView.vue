<template>
  <div class="login-wrap">
    <h1>书签</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="form">
      <input v-model="username" type="text" placeholder="用户名" @keyup.enter="doLogin" />
      <input v-model="password" type="password" placeholder="密码" @keyup.enter="doLogin" />
      <button @click="doLogin" :disabled="loading">
        {{ loading ? '登录中…' : '登录' }}
      </button>
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
.login-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 16px;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 280px;
}
input {
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 8px;
  background: #4f6ef7;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.error {
  color: #e33;
  font-size: 13px;
}
</style>
