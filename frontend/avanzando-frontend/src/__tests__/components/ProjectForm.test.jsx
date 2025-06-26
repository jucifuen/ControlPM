import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import ProjectForm from '../../components/ProjectForm'

global.fetch = vi.fn()

describe('ProjectForm Component', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  it('renders project form correctly', () => {
    render(<ProjectForm onProjectCreated={vi.fn()} />)
    
    expect(screen.getByText(/crear nuevo proyecto/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/nombre del proyecto/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/descripción/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/presupuesto/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /crear proyecto/i })).toBeInTheDocument()
  })

  it('validates required fields', async () => {
    render(<ProjectForm onProjectCreated={vi.fn()} />)
    
    const submitButton = screen.getByRole('button', { name: /crear proyecto/i })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/nombre es requerido/i)).toBeInTheDocument()
    })
  })

  it('creates project successfully', async () => {
    const mockOnProjectCreated = vi.fn()
    const mockResponse = {
      ok: true,
      json: () => Promise.resolve({
        message: 'Proyecto creado exitosamente',
        project: { id: 1, nombre: 'Test Project' }
      })
    }
    
    fetch.mockResolvedValueOnce(mockResponse)
    
    render(<ProjectForm onProjectCreated={mockOnProjectCreated} />)
    
    fireEvent.change(screen.getByLabelText(/nombre del proyecto/i), {
      target: { value: 'Test Project' }
    })
    fireEvent.change(screen.getByLabelText(/descripción/i), {
      target: { value: 'Test Description' }
    })
    fireEvent.change(screen.getByLabelText(/presupuesto/i), {
      target: { value: '100000' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /crear proyecto/i }))
    
    await waitFor(() => {
      expect(mockOnProjectCreated).toHaveBeenCalled()
    })
  })

  it('shows error message on failed creation', async () => {
    const mockResponse = {
      ok: false,
      json: () => Promise.resolve({ error: 'Error al crear proyecto' })
    }
    
    fetch.mockResolvedValueOnce(mockResponse)
    
    render(<ProjectForm onProjectCreated={vi.fn()} />)
    
    fireEvent.change(screen.getByLabelText(/nombre del proyecto/i), {
      target: { value: 'Test Project' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: /crear proyecto/i }))
    
    await waitFor(() => {
      expect(screen.getByText(/error al crear proyecto/i)).toBeInTheDocument()
    })
  })
})

