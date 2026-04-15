import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { pushMock, registerMock } = vi.hoisted(() => ({
  pushMock: vi.fn(),
  registerMock: vi.fn()
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
    register: registerMock
  }
}))

import RegisterView from '../RegisterView.vue'

const renderRegisterView = () => {
  return render(RegisterView, {
    global: {
      stubs: {
        RouterLink: {
          template: '<a><slot /></a>'
        }
      }
    }
  })
}

describe('RegisterView', () => {
  beforeEach(() => {
    pushMock.mockReset()
    registerMock.mockReset()
  })

  it('submits registration and navigates on success', async () => {
    registerMock.mockResolvedValueOnce(undefined)

    const { container } = renderRegisterView()

    await fireEvent.update(screen.getByLabelText('Username'), 'newuser')
    await fireEvent.update(screen.getByLabelText('Password'), 'pass1234')
    await fireEvent.submit(container.querySelector('form'))

    await waitFor(() => {
      expect(registerMock).toHaveBeenCalledWith('newuser', 'pass1234')
      expect(pushMock).toHaveBeenCalledWith('/dashboard')
    })
  })

  it('shows API detail when registration fails', async () => {
    registerMock.mockRejectedValueOnce({ response: { data: { detail: 'Already exists' } } })

    const { container } = renderRegisterView()

    await fireEvent.update(screen.getByLabelText('Username'), 'newuser')
    await fireEvent.update(screen.getByLabelText('Password'), 'pass1234')
    await fireEvent.submit(container.querySelector('form'))

    expect(await screen.findByRole('alert')).toHaveTextContent('Already exists')
  })

  it('disables submit while request is pending', async () => {
    registerMock.mockImplementation(() => new Promise(() => {}))

    const { container } = renderRegisterView()

    await fireEvent.update(screen.getByLabelText('Username'), 'newuser')
    await fireEvent.update(screen.getByLabelText('Password'), 'pass1234')
    await fireEvent.submit(container.querySelector('form'))

    expect(screen.getByRole('button', { name: 'Signing up...' })).toBeDisabled()
  })
})
