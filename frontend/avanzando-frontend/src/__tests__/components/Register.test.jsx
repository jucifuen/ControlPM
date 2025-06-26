import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Register from '../../components/Register'

global.fetch = vi.fn()

describe('Register Component', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('renders register form correctly', () => {
    render(<Register onRegister={vi.fn()} />)
    
    expect(screen.getByText(/crear cuenta/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/nombre/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /registrarse/i })).toBeInTheDocument()
  })

  it('validates required fields', async () => {
    render(<Register onRegister={vi.fn()} />)
    
    const submitButton = screen.getByRole('button', { name: /registrarse/i })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/nombre es requerido/i)).toBeInTheDocument()
      expect(screen.getByText(/email es requerido/i)).toBeInTheDocument()
      expect(screen.getByText(/contraseña es requerida/i)).toBeInTheDocument()
    })
  })

  it('registers user successfully', async () => {
    const mockOnRegister = vi.fn()
    const mockResponse = {
      ok: true,
      json: () => Promise.resolve({
        message: 'Usuario creado exitosamente',
        user: { id: 1, nombre: 'Test User', email: 'test@example.com' }
      })
    }
    
    fetch.mockResolvedValueOnce(mockResponse)
    
    render(<Register onRegister={mockOnRegister} />)
    
    fireEvent.change(screen.getByLabelText(/nombre/i), {
      target: { value: 'Test User' }
    })
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText(/contraseña/i), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /registrarse/i }))
    
    await waitFor(() => {
      expect(mockOnRegister).toHaveBeenCalled()
    })
  })
})

