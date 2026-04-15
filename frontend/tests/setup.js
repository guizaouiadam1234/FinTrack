import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/vue'
import { afterAll, afterEach, beforeAll, vi } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => {
  server.listen({ onUnhandledRequest: 'error' })
})

afterEach(() => {
  cleanup()
  server.resetHandlers()
  localStorage.clear()
  vi.restoreAllMocks()
  vi.useRealTimers()
})

afterAll(() => {
  server.close()
})
