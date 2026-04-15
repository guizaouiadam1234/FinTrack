import { beforeEach, describe, expect, it } from 'vitest'
import { http, HttpResponse } from 'msw'
import { server } from '../../../tests/mocks/server'
import api, { createTransaction, getDashboardSummary, getRecentTransactions } from '../api'

describe('api service helpers', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('fetches dashboard summary', async () => {
    const result = await getDashboardSummary()

    expect(result.total_balance).toBe(1800)
    expect(result.monthly_income).toBe(3000)
  })

  it('fetches recent transactions with limit', async () => {
    const result = await getRecentTransactions(20)

    expect(Array.isArray(result)).toBe(true)
    expect(result).toHaveLength(2)
    expect(result[0].title).toBe('Salary')
  })

  it('creates transaction', async () => {
    const payload = { title: 'Coffee', amount: 5, type: 'expense', category: 'Food' }

    const result = await createTransaction(payload)

    expect(result.id).toBe(99)
    expect(result.title).toBe('Coffee')
  })

  it('uses API detail message when summary request fails', async () => {
    server.use(
      http.get('http://localhost:8000/transactions/summary', () => {
        return HttpResponse.json({ detail: 'Summary failed' }, { status: 500 })
      })
    )

    await expect(getDashboardSummary()).rejects.toThrow('Summary failed')
  })

  it('falls back to default error message when API detail is missing', async () => {
    server.use(
      http.get('http://localhost:8000/transactions/recent', () => {
        return HttpResponse.json({}, { status: 500 })
      })
    )

    await expect(getRecentTransactions()).rejects.toThrow('Unable to load recent transactions.')
  })

  it('adds authorization header through interceptor when token exists', async () => {
    localStorage.setItem('token', 'secret-token')

    server.use(
      http.get('http://localhost:8000/auth-header-test', ({ request }) => {
        return HttpResponse.json({ auth: request.headers.get('authorization') })
      })
    )

    const response = await api.get('/auth-header-test')

    expect(response.data.auth).toBe('Bearer secret-token')
  })

  it('does not add authorization header when token is missing', async () => {
    server.use(
      http.get('http://localhost:8000/auth-header-test', ({ request }) => {
        return HttpResponse.json({ auth: request.headers.get('authorization') })
      })
    )

    const response = await api.get('/auth-header-test')

    expect(response.data.auth).toBeNull()
  })
})
