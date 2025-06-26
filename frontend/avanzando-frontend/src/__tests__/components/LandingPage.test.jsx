import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import LandingPage from '../../components/LandingPage'

describe('LandingPage Component', () => {
  it('renders landing page content correctly', () => {
    render(<LandingPage onNavigateToRegister={vi.fn()} onNavigateToLogin={vi.fn()} />)
    
    expect(screen.getByText(/avanzando/i)).toBeInTheDocument()
    expect(screen.getByText(/gestión de proyectos/i)).toBeInTheDocument()
    expect(screen.getByText(/comenzar gratis/i)).toBeInTheDocument()
    expect(screen.getByText(/iniciar sesión/i)).toBeInTheDocument()
  })

  it('shows key features', () => {
    render(<LandingPage onNavigateToRegister={vi.fn()} onNavigateToLogin={vi.fn()} />)
    
    expect(screen.getByText(/gestión integral/i)).toBeInTheDocument()
    expect(screen.getByText(/kpis en tiempo real/i)).toBeInTheDocument()
    expect(screen.getByText(/control de riesgos/i)).toBeInTheDocument()
    expect(screen.getByText(/recursos optimizados/i)).toBeInTheDocument()
  })

  it('shows pricing plans', () => {
    render(<LandingPage onNavigateToRegister={vi.fn()} onNavigateToLogin={vi.fn()} />)
    
    expect(screen.getByText(/gratuito/i)).toBeInTheDocument()
    expect(screen.getByText(/profesional/i)).toBeInTheDocument()
    expect(screen.getByText(/empresarial/i)).toBeInTheDocument()
  })

  it('calls onNavigateToRegister when register button is clicked', () => {
    const mockNavigateToRegister = vi.fn()
    render(<LandingPage onNavigateToRegister={mockNavigateToRegister} onNavigateToLogin={vi.fn()} />)
    
    const registerButton = screen.getByText(/comenzar gratis/i)
    fireEvent.click(registerButton)
    
    expect(mockNavigateToRegister).toHaveBeenCalled()
  })

  it('calls onNavigateToLogin when login button is clicked', () => {
    const mockNavigateToLogin = vi.fn()
    render(<LandingPage onNavigateToRegister={vi.fn()} onNavigateToLogin={mockNavigateToLogin} />)
    
    const loginButton = screen.getByText(/iniciar sesión/i)
    fireEvent.click(loginButton)
    
    expect(mockNavigateToLogin).toHaveBeenCalled()
  })
})

