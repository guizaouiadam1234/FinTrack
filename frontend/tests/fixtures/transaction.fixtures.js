export const summaryFixture = {
  total_balance: 1800,
  monthly_income: 3000,
  monthly_expenses: 1200,
  transaction_count: 3
}

export const recentTransactionsFixture = [
  {
    id: 1,
    title: 'Salary',
    amount: 3000,
    type: 'income',
    category: 'Work',
    date: '2026-04-10T12:00:00.000Z'
  },
  {
    id: 2,
    title: 'Rent',
    amount: 1200,
    type: 'expense',
    category: 'Housing',
    date: '2026-04-08T12:00:00.000Z'
  }
]

export const createdTransactionFixture = {
  id: 99,
  title: 'Coffee',
  amount: 5,
  type: 'expense',
  category: 'Food',
  date: '2026-04-15T12:00:00.000Z'
}
