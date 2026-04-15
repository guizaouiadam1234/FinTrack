import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const {
  pushMock,
  logoutMock,
  getDashboardSummaryMock,
  getRecentTransactionsMock,
  createTransactionMock
} = vi.hoisted(() => ({
  pushMock: vi.fn(),
  logoutMock: vi.fn(),
  getDashboardSummaryMock: vi.fn(),
  getRecentTransactionsMock: vi.fn(),
  createTransactionMock: vi.fn()
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: pushMock })
}))

vi.mock('../../router/auth', () => ({
  authStore: {
    logout: logoutMock
  }
}))

vi.mock('../../services/api', () => ({
  getDashboardSummary: getDashboardSummaryMock,
  getRecentTransactions: getRecentTransactionsMock,
  createTransaction: createTransactionMock
}))

import DashboardView from '../DashboardView.vue'

const summaryFixture = {
  total_balance: 1800,
  monthly_income: 3000,
  monthly_expenses: 1200,
  transaction_count: 3
}

const recentFixture = [
  {
    id: 1,
    title: 'Salary',
    amount: 3000,
    type: 'income',
    category: 'Work',
    date: '2026-04-10T12:00:00.000Z'
  }
]

describe('DashboardView', () => {
  beforeEach(() => {
    pushMock.mockReset()
    logoutMock.mockReset()
    getDashboardSummaryMock.mockReset()
    getRecentTransactionsMock.mockReset()
    createTransactionMock.mockReset()

    getDashboardSummaryMock.mockResolvedValue(summaryFixture)
    getRecentTransactionsMock.mockResolvedValue(recentFixture)
    createTransactionMock.mockResolvedValue({ id: 2 })
  })

  it('loads summary and recent transactions on mount', async () => {
    render(DashboardView)

    expect(await screen.findByText('Salary')).toBeInTheDocument()
    expect(screen.getByText('$1,800.00')).toBeInTheDocument()
    expect(getDashboardSummaryMock).toHaveBeenCalledTimes(1)
    expect(getRecentTransactionsMock).toHaveBeenCalledWith(20)
  })

  it('shows validation error when title is missing', async () => {
    const { container } = render(DashboardView)
    await screen.findByText('Salary')

    await fireEvent.update(screen.getByLabelText('Amount'), '10')
    await fireEvent.submit(container.querySelector('form'))

    expect(await screen.findByText('Title is required.')).toBeInTheDocument()
  })

  it('shows validation error when amount is invalid', async () => {
    const { container } = render(DashboardView)
    await screen.findByText('Salary')

    await fireEvent.update(screen.getByLabelText('Title'), 'Coffee')
    await fireEvent.update(screen.getByLabelText('Amount'), '0')
    await fireEvent.submit(container.querySelector('form'))

    expect(await screen.findByText('Amount must be greater than 0.')).toBeInTheDocument()
  })

  it('creates transaction then reloads dashboard data', async () => {
    const { container } = render(DashboardView)
    await screen.findByText('Salary')

    await fireEvent.update(screen.getByLabelText('Title'), 'Coffee')
    await fireEvent.update(screen.getByLabelText('Amount'), '5')
    await fireEvent.update(screen.getByLabelText('Type'), 'expense')
    await fireEvent.update(screen.getByLabelText('Category'), 'Food')
    await fireEvent.update(screen.getByLabelText('Date'), '2026-04-15')
    await fireEvent.submit(container.querySelector('form'))

    await waitFor(() => {
      expect(createTransactionMock).toHaveBeenCalledTimes(1)
    })

    expect(getDashboardSummaryMock).toHaveBeenCalledTimes(2)
    expect(getRecentTransactionsMock).toHaveBeenCalledTimes(2)
  })

  it('shows dashboard load errors', async () => {
    getDashboardSummaryMock.mockRejectedValueOnce(new Error('Unable to load dashboard summary.'))
    getRecentTransactionsMock.mockResolvedValueOnce([])

    render(DashboardView)

    expect(await screen.findByText('Unable to load dashboard summary.')).toBeInTheDocument()
  })

  it('logs out and navigates to login', async () => {
    render(DashboardView)
    await screen.findByText('Salary')

    await fireEvent.click(screen.getByRole('button', { name: 'Log Out' }))

    expect(logoutMock).toHaveBeenCalledTimes(1)
    expect(pushMock).toHaveBeenCalledWith('/login')
  })
})
