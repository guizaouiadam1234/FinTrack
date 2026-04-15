import { http, HttpResponse } from 'msw'
import { loginSuccessFixture, registerSuccessFixture } from '../fixtures/auth.fixtures'
import {
  createdTransactionFixture,
  recentTransactionsFixture,
  summaryFixture
} from '../fixtures/transaction.fixtures'

const API_BASE = 'http://localhost:8000'

export const handlers = [
  http.post(`${API_BASE}/auth/login`, () => {
    return HttpResponse.json(loginSuccessFixture)
  }),

  http.post(`${API_BASE}/auth/register`, () => {
    return HttpResponse.json(registerSuccessFixture, { status: 201 })
  }),

  http.get(`${API_BASE}/transactions/summary`, () => {
    return HttpResponse.json(summaryFixture)
  }),

  http.get(`${API_BASE}/transactions/recent`, () => {
    return HttpResponse.json(recentTransactionsFixture)
  }),

  http.post(`${API_BASE}/transactions/`, () => {
    return HttpResponse.json(createdTransactionFixture, { status: 201 })
  })
]
