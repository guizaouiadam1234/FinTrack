import { reactive } from 'vue'
import api from '../services/api'

export const authStore = reactive({
  token: localStorage.getItem('token') || null,
  isAuthenticated() {
    return !!this.token
  },
  async login(username, password) {
    const params = new URLSearchParams({ username, password })
    const res = await api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    this.token = res.data.access_token
    localStorage.setItem('token', this.token)
  },
  async register(username, password) {
    const params = new URLSearchParams({ username, password })
    await api.post('/auth/register', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  logout() {
    this.token = null
    localStorage.removeItem('token')
  }
})