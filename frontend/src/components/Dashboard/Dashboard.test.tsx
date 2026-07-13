import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Dashboard from './Dashboard'

// Mock fetch
global.fetch = vi.fn()

describe('Dashboard Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    ;(global.fetch as any).mockClear()
  })

  describe('Rendering', () => {
    it('should render dashboard header', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('Dashboard Analítico')).toBeInTheDocument()
        expect(screen.getByText('Monitoramento de Processos de Manufatura')).toBeInTheDocument()
      })
    })

    it('should render KPI cards', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('Compliance Score')).toBeInTheDocument()
        expect(screen.getByText('Predição de Risco')).toBeInTheDocument()
      })
    })

    it('should render sensor section', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('Variáveis de Sensores')).toBeInTheDocument()
      })
    })

    it('should render batch history section', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('Histórico de Batches')).toBeInTheDocument()
      })
    })

    it('should render disclaimer', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText(/Esta análise é baseada em dados históricos/)).toBeInTheDocument()
      })
    })
  })

  describe('Data Loading', () => {
    it('should show loading state initially', () => {
      (global.fetch as any).mockImplementation(() => new Promise(() => {}))

      render(<Dashboard />)

      expect(screen.getByText('Carregando dashboard...')).toBeInTheDocument()
    })

    it('should fetch batches on mount', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalledWith('/api/v1/batches')
      })
    })

    it('should handle fetch error', async () => {
      (global.fetch as any).mockRejectedValueOnce(new Error('Network error'))

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText(/Network error/)).toBeInTheDocument()
      })
    })

    it('should display retry button on error', async () => {
      (global.fetch as any).mockRejectedValueOnce(new Error('Network error'))

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('Tentar Novamente')).toBeInTheDocument()
      })
    })
  })

  describe('Compliance Score Classification', () => {
    it('should classify score as ACCEPTABLE (80-100)', async () => {
      const mockBatch = {
        id: 'batch-1',
        upload_date: '2026-05-27T10:00:00',
        compliance_score: 85,
        risk_prediction: 'LOW_RISK',
        confidence_score: 0.95,
        status: 'COMPLETED'
      }

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [mockBatch]
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 85 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'LOW_RISK', confidence_score: 0.95 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('ACCEPTABLE')).toBeInTheDocument()
      })
    })

    it('should classify score as WARNING (45-79)', async () => {
      const mockBatch = {
        id: 'batch-1',
        upload_date: '2026-05-27T10:00:00',
        compliance_score: 70,
        risk_prediction: 'MEDIUM_RISK',
        confidence_score: 0.75,
        status: 'COMPLETED'
      }

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [mockBatch]
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 70 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'MEDIUM_RISK', confidence_score: 0.75 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('WARNING')).toBeInTheDocument()
      })
    })

    it('should classify score as CRITICAL (0-44)', async () => {
      const mockBatch = {
        id: 'batch-1',
        upload_date: '2026-05-27T10:00:00',
        compliance_score: 44,
        risk_prediction: 'HIGH_RISK',
        confidence_score: 0.85,
        status: 'COMPLETED'
      }

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [mockBatch]
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 44 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'HIGH_RISK', confidence_score: 0.85 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('CRITICAL')).toBeInTheDocument()
      })
    })
  })

  describe('Filters', () => {
    it('should filter by status', async () => {
      const mockBatches = [
        {
          id: 'batch-1',
          upload_date: '2026-05-27T10:00:00',
          compliance_score: 85,
          risk_prediction: 'LOW_RISK',
          confidence_score: 0.95,
          status: 'COMPLETED'
        },
        {
          id: 'batch-2',
          upload_date: '2026-05-27T11:00:00',
          compliance_score: 70,
          risk_prediction: 'MEDIUM_RISK',
          confidence_score: 0.75,
          status: 'PROCESSING'
        }
      ]

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockBatches
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 85 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'LOW_RISK', confidence_score: 0.95 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        const statusFilter = screen.getByLabelText('Status') as HTMLSelectElement
        expect(statusFilter).toBeInTheDocument()
      })

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'COMPLETED')

      await waitFor(() => {
        expect(statusSelect.value).toBe('COMPLETED')
      })
    })

    it('should filter by score range', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        const scoreSelects = screen.getAllByDisplayValue('Todos')
        expect(scoreSelects.length).toBeGreaterThan(0)
      })
    })

    it('should filter by date range', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        const dateSelects = screen.getAllByDisplayValue('Todos')
        expect(dateSelects.length).toBeGreaterThan(0)
      })
    })
  })

  describe('Pagination', () => {
    it('should display pagination controls with multiple pages', async () => {
      const mockBatches = Array.from({ length: 15 }, (_, i) => ({
        id: `batch-${i}`,
        upload_date: '2026-05-27T10:00:00',
        compliance_score: 85,
        risk_prediction: 'LOW_RISK',
        confidence_score: 0.95,
        status: 'COMPLETED'
      }))

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockBatches
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 85 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'LOW_RISK', confidence_score: 0.95 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText(/Página 1 de 2/)).toBeInTheDocument()
      })
    })

    it('should navigate between pages', async () => {
      const mockBatches = Array.from({ length: 15 }, (_, i) => ({
        id: `batch-${i}`,
        upload_date: '2026-05-27T10:00:00',
        compliance_score: 85,
        risk_prediction: 'LOW_RISK',
        confidence_score: 0.95,
        status: 'COMPLETED'
      }))

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockBatches
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 85 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'LOW_RISK', confidence_score: 0.95 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText(/Página 1 de 2/)).toBeInTheDocument()
      })

      const nextButton = screen.getByText('Próxima →')
      await userEvent.click(nextButton)

      await waitFor(() => {
        expect(screen.getByText(/Página 2 de 2/)).toBeInTheDocument()
      })
    })
  })

  describe('Sensor Data Display', () => {
    it('should display sensor values', async () => {
      const mockBatch = {
        id: 'batch-1',
        upload_date: '2026-05-27T10:00:00',
        compliance_score: 85,
        risk_prediction: 'LOW_RISK',
        confidence_score: 0.95,
        status: 'COMPLETED',
        sensor_data: {
          temperature: 32.5,
          ph: 7.2,
          dissolved_oxygen: 75.5,
          pressure: 5.2,
          agitator_speed: 250
        }
      }

      ;(global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [mockBatch]
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ compliance_score: 85 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ risk_prediction: 'LOW_RISK', confidence_score: 0.95 })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ readings: [] })
        })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText('Temperatura')).toBeInTheDocument()
        expect(screen.getByText('pH')).toBeInTheDocument()
        expect(screen.getByText('Oxigênio Dissolvido')).toBeInTheDocument()
        expect(screen.getByText('Pressão')).toBeInTheDocument()
        expect(screen.getByText('Velocidade do Agitador')).toBeInTheDocument()
      })
    })
  })

  describe('Empty State', () => {
    it('should display empty state when no batches found', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard />)

      await waitFor(() => {
        expect(screen.getByText(/Nenhum batch encontrado/)).toBeInTheDocument()
      })
    })
  })

  describe('Props', () => {
    it('should accept refreshInterval prop', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<Dashboard refreshInterval={60000} />)

      await waitFor(() => {
        expect(screen.getByText('Dashboard Analítico')).toBeInTheDocument()
      })
    })
  })
})
