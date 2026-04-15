import { beforeEach, describe, expect, it, vi } from 'vitest'

const { postMock } = vi.hoisted(() => ({
  postMock: vi.fn()
}))

vi.mock('../../services/api', () => ({
  default: {
    post: postMock
  }
}))

import { authStore } from '../auth'

describe('authStore', () => {
  beforeEach(() => {
    authStore.token = null
    localStorage.clear()
    postMock.mockReset()
  })

  it('logs in and stores token', async () => {
    postMock.mockResolvedValueOnce({ data: { access_token: 'abc123' } })

    await authStore.login('alice', 'pass123')

    const params = postMock.mock.calls[0][1]
    expect(postMock).toHaveBeenCalledWith('/auth/login', expect.any(URLSearchParams), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    expect(params.get('username')).toBe('alice')
    expect(params.get('password')).toBe('pass123')
    expect(authStore.token).toBe('abc123')
    expect(localStorage.getItem('token')).toBe('abc123')
  })

  it('registers user via api', async () => {
    postMock.mockResolvedValueOnce({ data: { message: 'ok' } })

    await authStore.register('new-user', 'secure')

    const params = postMock.mock.calls[0][1]
    expect(postMock).toHaveBeenCalledWith('/auth/register', expect.any(URLSearchParams), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    expect(params.get('username')).toBe('new-user')
    expect(params.get('password')).toBe('secure')
  })

  it('returns auth state correctly', () => {
    expect(authStore.isAuthenticated()).toBe(false)

    authStore.token = 'token-value'
    expect(authStore.isAuthenticated()).toBe(true)
  })

  it('clears token on logout', () => {
    authStore.token = 'token-value'
    localStorage.setItem('token', 'token-value')

    authStore.logout()

    expect(authStore.token).toBeNull()
    expect(localStorage.getItem('token')).toBeNull()
  })
})
