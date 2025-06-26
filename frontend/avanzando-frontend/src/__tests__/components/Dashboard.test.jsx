import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Dashboard from '../../components/Dashboard'

// Mock fetch
global.fetch = vi.fn()

const mockUser = {
  id: 1,
  nombre: 'Test User',
  email: 'test@example.com',
  rol: 'administrador'
}

describe('Dashboard Component', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('renders dashboard with user information', () => {
    render(<Dashboard user={mockUser} onLogout={vi.fn()} />)
    
    expect(screen.getByText(/bienvenido/i)).toBeInTheDocument()
    expect(screen.getByText('Test User')).toBeInTheDocument()
    expect(screen.getByText(/administrador/i)).toBeInTheDocument()
  })

  it('shows navigation menu items', () => {
    render(<Dashboard user={mockUser} onLogout={vi.fn()} />)
    
    expect(screen.getByText(/proyectos/i)).toBeInTheDocument()
    expect(screen.getByText(/kpis/i)).toBeInTheDocument()
    expect(screen.getByText(/riesgos/i)).toBeInTheDocument()
    expect(screen.getByText(/recursos/i)).toBeInTheDocument()
  })

  it('calls onLogout when logout button is clicked', () => {
    const mockOnLogout = vi.fn()
    render(<Dashboard user={mockUser} onLogout={mockOnLogout} />)
    
    const logoutButton = screen.getByText(/cerrar sesión/i)
    fireEvent.click(logoutButton)
    
    expect(mockOnLogout).toHaveBeenCalled()
  })

  it('shows different menu items based on user role', () => {
    const clientUser = { ...mockUser, rol: 'cliente' }
    render(<Dashboard user={clientUser} onLogout={vi.fn()} />)
    
    expect(screen.getByText(/proyectos/i)).toBeInTheDocument()
    // Los clientes no deberían ver todas las opciones de administrador
    expect(screen.queryByText(/usuarios/i)).not.toBeInTheDocument()
  })

  it('loads projects on mount', async () => {
    const mockProjects = [
      { id: 1, nombre: 'Proyecto 1', estado: 'activo' },
      { id: 2, nombre: 'Proyecto 2', estado: 'completado' }
    ]
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ projects: mockProjects })
    })
    
    render(<Dashboard user={mockUser} onLogout={vi.fn()} />)
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:5000/api/projects',
      expect.objectContaining({
        headers: expect.objectContaining({
          'Authorization': expect.stringContaining('Bearer')
        })
      })
    )
  })
})

