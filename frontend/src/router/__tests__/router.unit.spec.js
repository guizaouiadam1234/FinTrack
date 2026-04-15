import { beforeEach, describe, expect, it } from 'vitest'
import router from '../index'
import { authStore } from '../auth'

const safePush = async (path) => {
  try {
    await router.push(path)
  } catch {
    // Ignore duplicate navigation errors between tests.
  }
}

describe('router guards', () => {
  beforeEach(async () => {
    authStore.token = null
    localStorage.clear()
    await safePush('/login')
  })

  it('redirects unauthenticated users away from protected routes', async () => {
    authStore.token = null

    await safePush('/dashboard')

    expect(router.currentRoute.value.fullPath).toBe('/login')
  })

  it('redirects authenticated users away from guest-only routes', async () => {
    authStore.token = 'auth-token'

    await safePush('/dashboard')

    await safePush('/login')

    expect(router.currentRoute.value.fullPath).toBe('/dashboard')
  })

  it('redirects root to dashboard', async () => {
    authStore.token = 'auth-token'

    await safePush('/')

    expect(router.currentRoute.value.fullPath).toBe('/dashboard')
  })
})
