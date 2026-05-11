import axios from 'axios'
import router from '../router/index.js'

function getCsrfToken() {
  const m = document.cookie.match(/csrftoken=([^;]+)/)
  return m ? m[1] : ''
}

const http = axios.create({
  baseURL: '/',
  withCredentials: true,
})

http.interceptors.request.use(config => {
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    config.headers['X-CSRFToken'] = getCsrfToken()
  }
  return config
})

http.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 403 || err.response?.status === 401) {
      router.push('/login')
    }
    return Promise.reject(err)
  }
)

export default http
