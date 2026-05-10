import http from './http.js'

function getCsrfToken() {
  const m = document.cookie.match(/csrftoken=([^;]+)/)
  return m ? m[1] : ''
}

export const primeCsrf = () => http.get('/api/')

export async function login(username, password) {
  await primeCsrf()
  const params = new URLSearchParams({
    username,
    password,
    csrfmiddlewaretoken: getCsrfToken(),
  })
  await http.post('/accounts/login/', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    maxRedirects: 0,
    validateStatus: s => s < 400,
  })
  try {
    await http.get('/api/bookmarks/')
    return true
  } catch {
    return false
  }
}

export async function logout() {
  const params = new URLSearchParams({ csrfmiddlewaretoken: getCsrfToken() })
  await http.post('/accounts/logout/', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    maxRedirects: 0,
    validateStatus: s => s < 400,
  })
}

// 书签
export const listBookmarks = params => http.get('/api/bookmarks/', { params })
export const getBookmark = id => http.get(`/api/bookmarks/${id}/`)
export const createBookmark = data => http.post('/api/bookmarks/', data)
export const updateBookmark = (id, data) => http.patch(`/api/bookmarks/${id}/`, data)
export const deleteBookmark = id => http.delete(`/api/bookmarks/${id}/`)
export const visitBookmark = id => http.post(`/api/bookmarks/${id}/visit/`)

// 标签
export const listTags = () => http.get('/api/tags/')
export const createTag = data => http.post('/api/tags/', data)
export const updateTag = (id, data) => http.patch(`/api/tags/${id}/`, data)
export const deleteTag = id => http.delete(`/api/tags/${id}/`)

// 工具
export const fetchUrlMeta = url => http.get('/api/fetch-url-meta/', { params: { url } })
