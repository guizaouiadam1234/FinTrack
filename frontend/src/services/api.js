import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const getApiErrorMessage = (error, fallbackMessage) => {
  return error?.response?.data?.detail || fallbackMessage
}

export const getDashboardSummary = async ({ startDate, endDate } = {}) => {
  try {
    const params = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate

    const response = await api.get('/transactions/summary', { params })
    return response.data
  } catch (error) {
    throw new Error(getApiErrorMessage(error, 'Unable to load dashboard summary.'))
  }
}

export const getRecentTransactions = async (limit = 20) => {
  try {
    const response = await api.get('/transactions/recent', {
      params: { limit }
    })
    return response.data
  } catch (error) {
    throw new Error(getApiErrorMessage(error, 'Unable to load recent transactions.'))
  }
}

export const createTransaction = async (payload) => {
  try {
    const response = await api.post('/transactions/', payload)
    return response.data
  } catch (error) {
    throw new Error(getApiErrorMessage(error, 'Unable to create transaction.'))
  }
}

export const updateTransaction = async (transactionId, payload) => {
  try {
    const response = await api.put(`/transactions/${transactionId}`, payload)
    return response.data
  } catch (error) {
    throw new Error(getApiErrorMessage(error, 'Unable to update transaction.'))
  }
}

export const deleteTransaction = async (transactionId) => {
  try {
    await api.delete(`/transactions/${transactionId}`)
  } catch (error) {
    throw new Error(getApiErrorMessage(error, 'Unable to delete transaction.'))
  }
}


export default api;
