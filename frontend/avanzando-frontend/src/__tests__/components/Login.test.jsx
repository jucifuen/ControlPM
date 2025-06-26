import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Login from '../../components/Login'

// Mock fetch
global.fetch = vi.fn()

describe('Login Component', () => {
  beforeEach(() => {
    fetch.mockClear()
    localStorage.clear()
  })

  it('renders login form correctly', () => {
    render(<Login onLogin={vi.fn()} />)
    
    expect(screen.getByText('Iniciar Sesión')).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument()
  })

  it('shows validation errors for empty fields', async () => {
    render(<Login onLogin={vi.fn()} />)
    
    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/email es requerido/i)).toBeInTheDocument()
      expect(screen.getByText(/contraseña es requerida/i)).toBeInTheDocument()
    })
  })

  it('calls onLogin with correct data on successful login', async () => {
    const mockOnLogin = vi.fn()
    const mockResponse = {
      ok: true,
      json: () => Promise.resolve({
        token: 'mock-token',
        user: { id: 1, email: 'test@example.com', rol: 'administrador' }
      })
    }
    
    fetch.mockResolvedValueOnce(mockResponse)
    
    render(<Login onLogin={mockOnLogin} />)
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText(/contraseña/i), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /iniciar sesión/i }))
    
    await waitFor(() => {
      expect(mockOnLogin).toHaveBeenCalledWith({
        token: 'mock-token',
        user: { id: 1, email: 'test@example.com', rol: 'administrador' }
      })
    })
  })

  it('shows error message on failed login', async () => {
    const mockResponse = {
      ok: false,
      json: () => Promise.resolve({ error: 'Credenciales inválidas' })
    }
    
    fetch.mockResolvedValueOnce(mockResponse)
    
    render(<Login onLogin={vi.fn()} />)
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText(/contraseña/i), {
      target: { value: 'wrongpassword' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /iniciar sesión/i }))
    
    await waitFor(() => {
      expect(screen.getByText(/credenciales inválidas/i)).toBeInTheDocument()
    })
  })
})

