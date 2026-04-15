import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { pushMock, loginMock } = vi.hoisted(() => ({
  pushMock: vi.fn(),
  loginMock: vi.fn()
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: pushMock }),
  RouterLink: {
    name: 'RouterLink',
    template: '<a><slot /></a>'
  }
}))

vi.mock('../../router/auth', () => ({
  authStore: {
    login: loginMock
  }
}))

import LoginView from '../LoginView.vue'

const renderLoginView = () => {
  return render(LoginView, {
    global: {
      stubs: {
        RouterLink: {
          template: '<a><slot /></a>'
        }
      }
    }
  })
}

describe('LoginView', () => {
  beforeEach(() => {
    pushMock.mockReset()
    loginMock.mockReset()
  })

  it('submits credentials and navigates on success', async () => {
    loginMock.mockResolvedValueOnce(undefined)

    const { container } = renderLoginView()

    await fireEvent.update(screen.getByLabelText('Username'), '  alice  ')
    await fireEvent.update(screen.getByLabelText('Password'), 'pass1234')
    await fireEvent.submit(container.querySelector('form'))

    await waitFor(() => {
      expect(loginMock).toHaveBeenCalledWith('alice', 'pass1234')
      expect(pushMock).toHaveBeenCalledWith('/dashboard')
    })
  })

  it('renders API error details when login fails', async () => {
    loginMock.mockRejectedValueOnce({ response: { data: { detail: 'Invalid credentials' } } })

    const { container } = renderLoginView()

    await fireEvent.update(screen.getByLabelText('Username'), 'alice')
    await fireEvent.update(screen.getByLabelText('Password'), 'wrong')
    await fireEvent.submit(container.querySelector('form'))

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid credentials')
  })

  it('disables submit button while request is pending', async () => {
    loginMock.mockImplementation(() => new Promise(() => {}))

    const { container } = renderLoginView()

    await fireEvent.update(screen.getByLabelText('Username'), 'alice')
    await fireEvent.update(screen.getByLabelText('Password'), 'pass1234')
    await fireEvent.submit(container.querySelector('form'))

    expect(screen.getByRole('button', { name: 'Signing in...' })).toBeDisabled()
  })
})
