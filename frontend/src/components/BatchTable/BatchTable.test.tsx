import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BatchTable, Batch } from './BatchTable'

describe('BatchTable Component', () => {
  const mockBatches: Batch[] = [
    {
      id: 'batch-001',
      upload_date: '2026-05-27T10:00:00Z',
      compliance_score: 85,
      risk_level: 'LOW RISK',
      status: 'ACCEPTABLE',
    },
    {
      id: 'batch-002',
      upload_date: '2026-05-26T14:30:00Z',
      compliance_score: 72,
      risk_level: 'MEDIUM RISK',
      status: 'WARNING',
    },
    {
      id: 'batch-003',
      upload_date: '2026-05-25T09:15:00Z',
      compliance_score: 45,
      risk_level: 'HIGH RISK',
      status: 'CRITICAL',
    },
  ]

  describe('Rendering', () => {
    it('should render table with all batches', () => {
      render(<BatchTable batches={mockBatches} />)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.getByText('batch-003')).toBeInTheDocument()
    })

    it('should render table headers', () => {
      render(<BatchTable batches={mockBatches} />)

      expect(screen.getByText('ID do Batch')).toBeInTheDocument()
      expect(screen.getByText('Data Upload')).toBeInTheDocument()
      expect(screen.getByText('Compliance Score')).toBeInTheDocument()
      expect(screen.getByText('Nível de Risco')).toBeInTheDocument()
      expect(screen.getByText('Status')).toBeInTheDocument()
    })

    it('should render empty message when no batches', () => {
      render(<BatchTable batches={[]} />)

      expect(screen.getByText(/Nenhum batch encontrado/)).toBeInTheDocument()
    })

    it('should render filters section', () => {
      render(<BatchTable batches={mockBatches} />)

      expect(screen.getByText('Filtros')).toBeInTheDocument()
      expect(screen.getByLabelText('Data Inicial')).toBeInTheDocument()
      expect(screen.getByLabelText('Data Final')).toBeInTheDocument()
      expect(screen.getByLabelText('Status')).toBeInTheDocument()
      expect(screen.getByLabelText('Score Mínimo')).toBeInTheDocument()
      expect(screen.getByLabelText('Score Máximo')).toBeInTheDocument()
    })

    it('should render pagination controls', () => {
      render(<BatchTable batches={mockBatches} />)

      expect(screen.getByText(/Página 1 de/)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Primeira/ })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Anterior/ })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Próxima/ })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Última/ })).toBeInTheDocument()
    })
  })

  describe('Data Formatting', () => {
    it('should format dates in pt-BR format', () => {
      render(<BatchTable batches={mockBatches} />)

      // Verificar que a data está formatada (contém / e :)
      const dateElements = screen.getAllByText(/\d{2}\/\d{2}\/\d{4}/)
      expect(dateElements.length).toBeGreaterThan(0)
    })

    it('should format compliance scores with 2 decimal places', () => {
      render(<BatchTable batches={mockBatches} />)

      // Verificar formatação de números
      expect(screen.getByText(/85,00|85\.00/)).toBeInTheDocument()
      expect(screen.getByText(/72,00|72\.00/)).toBeInTheDocument()
      expect(screen.getByText(/45,00|45\.00/)).toBeInTheDocument()
    })

    it('should display risk levels correctly', () => {
      render(<BatchTable batches={mockBatches} />)

      expect(screen.getByText('LOW RISK')).toBeInTheDocument()
      expect(screen.getByText('MEDIUM RISK')).toBeInTheDocument()
      expect(screen.getByText('HIGH RISK')).toBeInTheDocument()
    })

    it('should display status correctly', () => {
      render(<BatchTable batches={mockBatches} />)

      expect(screen.getByText('ACCEPTABLE')).toBeInTheDocument()
      expect(screen.getByText('WARNING')).toBeInTheDocument()
      expect(screen.getByText('CRITICAL')).toBeInTheDocument()
    })
  })

  describe('Filters - Date Range', () => {
    it('should filter by date from', async () => {
      render(<BatchTable batches={mockBatches} />)

      const dateFromInput = screen.getByLabelText('Data Inicial') as HTMLInputElement
      await userEvent.type(dateFromInput, '2026-05-26')

      // Apenas batches de 26/05 em diante devem aparecer
      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.queryByText('batch-003')).not.toBeInTheDocument()
    })

    it('should filter by date to', async () => {
      render(<BatchTable batches={mockBatches} />)

      const dateToInput = screen.getByLabelText('Data Final') as HTMLInputElement
      await userEvent.type(dateToInput, '2026-05-26')

      // Apenas batches até 26/05 devem aparecer
      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.getByText('batch-003')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
    })

    it('should filter by date range', async () => {
      render(<BatchTable batches={mockBatches} />)

      const dateFromInput = screen.getByLabelText('Data Inicial') as HTMLInputElement
      const dateToInput = screen.getByLabelText('Data Final') as HTMLInputElement

      await userEvent.type(dateFromInput, '2026-05-26')
      await userEvent.type(dateToInput, '2026-05-26')

      // Apenas batch-002 deve aparecer
      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
      expect(screen.queryByText('batch-003')).not.toBeInTheDocument()
    })
  })

  describe('Filters - Status', () => {
    it('should filter by status ACCEPTABLE', async () => {
      render(<BatchTable batches={mockBatches} />)

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'ACCEPTABLE')

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.queryByText('batch-002')).not.toBeInTheDocument()
      expect(screen.queryByText('batch-003')).not.toBeInTheDocument()
    })

    it('should filter by status WARNING', async () => {
      render(<BatchTable batches={mockBatches} />)

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'WARNING')

      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
      expect(screen.queryByText('batch-003')).not.toBeInTheDocument()
    })

    it('should filter by status CRITICAL', async () => {
      render(<BatchTable batches={mockBatches} />)

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'CRITICAL')

      expect(screen.getByText('batch-003')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
      expect(screen.queryByText('batch-002')).not.toBeInTheDocument()
    })
  })

  describe('Filters - Score Range', () => {
    it('should filter by minimum score', async () => {
      render(<BatchTable batches={mockBatches} />)

      const scoreMinInput = screen.getByLabelText('Score Mínimo') as HTMLInputElement
      await userEvent.clear(scoreMinInput)
      await userEvent.type(scoreMinInput, '70')

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.queryByText('batch-003')).not.toBeInTheDocument()
    })

    it('should filter by maximum score', async () => {
      render(<BatchTable batches={mockBatches} />)

      const scoreMaxInput = screen.getByLabelText('Score Máximo') as HTMLInputElement
      await userEvent.clear(scoreMaxInput)
      await userEvent.type(scoreMaxInput, '50')

      expect(screen.getByText('batch-003')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
      expect(screen.queryByText('batch-002')).not.toBeInTheDocument()
    })

    it('should filter by score range', async () => {
      render(<BatchTable batches={mockBatches} />)

      const scoreMinInput = screen.getByLabelText('Score Mínimo') as HTMLInputElement
      const scoreMaxInput = screen.getByLabelText('Score Máximo') as HTMLInputElement

      await userEvent.clear(scoreMinInput)
      await userEvent.type(scoreMinInput, '70')
      await userEvent.clear(scoreMaxInput)
      await userEvent.type(scoreMaxInput, '80')

      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
      expect(screen.queryByText('batch-003')).not.toBeInTheDocument()
    })
  })

  describe('Clear Filters', () => {
    it('should clear all filters', async () => {
      render(<BatchTable batches={mockBatches} />)

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'ACCEPTABLE')

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.queryByText('batch-002')).not.toBeInTheDocument()

      const clearButton = screen.getByRole('button', { name: /Limpar Filtros/ })
      await userEvent.click(clearButton)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-002')).toBeInTheDocument()
      expect(screen.getByText('batch-003')).toBeInTheDocument()
    })
  })

  describe('Pagination', () => {
    const manyBatches = Array.from({ length: 25 }, (_, i) => ({
      id: `batch-${String(i + 1).padStart(3, '0')}`,
      upload_date: new Date(2026, 4, 27 - Math.floor(i / 10)).toISOString(),
      compliance_score: 50 + Math.random() * 50,
      risk_level: ['LOW RISK', 'MEDIUM RISK', 'HIGH RISK'][i % 3] as any,
      status: ['ACCEPTABLE', 'WARNING', 'CRITICAL'][i % 3] as any,
    }))

    it('should paginate with 10 items per page by default', () => {
      render(<BatchTable batches={manyBatches} />)

      // Primeira página deve ter 10 items
      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-010')).toBeInTheDocument()
      expect(screen.queryByText('batch-011')).not.toBeInTheDocument()
    })

    it('should navigate to next page', async () => {
      render(<BatchTable batches={manyBatches} />)

      const nextButton = screen.getByRole('button', { name: /Próxima/ })
      await userEvent.click(nextButton)

      expect(screen.getByText('batch-011')).toBeInTheDocument()
      expect(screen.getByText('batch-020')).toBeInTheDocument()
      expect(screen.queryByText('batch-001')).not.toBeInTheDocument()
    })

    it('should navigate to previous page', async () => {
      render(<BatchTable batches={manyBatches} />)

      const nextButton = screen.getByRole('button', { name: /Próxima/ })
      await userEvent.click(nextButton)

      const prevButton = screen.getByRole('button', { name: /Anterior/ })
      await userEvent.click(prevButton)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-010')).toBeInTheDocument()
    })

    it('should navigate to first page', async () => {
      render(<BatchTable batches={manyBatches} />)

      const nextButton = screen.getByRole('button', { name: /Próxima/ })
      await userEvent.click(nextButton)
      await userEvent.click(nextButton)

      const firstButton = screen.getByRole('button', { name: /Primeira/ })
      await userEvent.click(firstButton)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
    })

    it('should navigate to last page', async () => {
      render(<BatchTable batches={manyBatches} />)

      const lastButton = screen.getByRole('button', { name: /Última/ })
      await userEvent.click(lastButton)

      expect(screen.getByText('batch-021')).toBeInTheDocument()
      expect(screen.getByText('batch-025')).toBeInTheDocument()
    })

    it('should disable previous button on first page', () => {
      render(<BatchTable batches={manyBatches} />)

      const prevButton = screen.getByRole('button', { name: /Anterior/ })
      expect(prevButton).toBeDisabled()
    })

    it('should disable next button on last page', async () => {
      render(<BatchTable batches={manyBatches} />)

      const lastButton = screen.getByRole('button', { name: /Última/ })
      await userEvent.click(lastButton)

      const nextButton = screen.getByRole('button', { name: /Próxima/ })
      expect(nextButton).toBeDisabled()
    })

    it('should change items per page', async () => {
      render(<BatchTable batches={manyBatches} />)

      const itemsSelect = screen.getByLabelText('Items por página:') as HTMLSelectElement
      await userEvent.selectOptions(itemsSelect, '20')

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-020')).toBeInTheDocument()
      expect(screen.queryByText('batch-021')).not.toBeInTheDocument()
    })

    it('should show correct page info', () => {
      render(<BatchTable batches={manyBatches} />)

      expect(screen.getByText(/Página 1 de 3/)).toBeInTheDocument()
    })
  })

  describe('Row Click Handler', () => {
    it('should call onRowClick when row is clicked', async () => {
      const onRowClick = vi.fn()
      render(<BatchTable batches={mockBatches} onRowClick={onRowClick} />)

      const firstRow = screen.getByText('batch-001').closest('tr')
      if (firstRow) {
        await userEvent.click(firstRow)
      }

      expect(onRowClick).toHaveBeenCalledWith(mockBatches[0])
    })

    it('should call onRowClick on Enter key', async () => {
      const onRowClick = vi.fn()
      render(<BatchTable batches={mockBatches} onRowClick={onRowClick} />)

      const firstRow = screen.getByText('batch-001').closest('tr')
      if (firstRow) {
        fireEvent.keyDown(firstRow, { key: 'Enter' })
      }

      expect(onRowClick).toHaveBeenCalledWith(mockBatches[0])
    })

    it('should call onRowClick on Space key', async () => {
      const onRowClick = vi.fn()
      render(<BatchTable batches={mockBatches} onRowClick={onRowClick} />)

      const firstRow = screen.getByText('batch-001').closest('tr')
      if (firstRow) {
        fireEvent.keyDown(firstRow, { key: ' ' })
      }

      expect(onRowClick).toHaveBeenCalledWith(mockBatches[0])
    })
  })

  describe('Combined Filters and Pagination', () => {
    const manyBatches = Array.from({ length: 25 }, (_, i) => ({
      id: `batch-${String(i + 1).padStart(3, '0')}`,
      upload_date: new Date(2026, 4, 27 - Math.floor(i / 10)).toISOString(),
      compliance_score: 50 + (i % 3) * 15,
      risk_level: ['LOW RISK', 'MEDIUM RISK', 'HIGH RISK'][i % 3] as any,
      status: ['ACCEPTABLE', 'WARNING', 'CRITICAL'][i % 3] as any,
    }))

    it('should apply filters and then paginate', async () => {
      render(<BatchTable batches={manyBatches} />)

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'ACCEPTABLE')

      // Deve mostrar apenas batches ACCEPTABLE
      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.queryByText('batch-002')).not.toBeInTheDocument()
    })

    it('should reset pagination when filters change', async () => {
      render(<BatchTable batches={manyBatches} />)

      const nextButton = screen.getByRole('button', { name: /Próxima/ })
      await userEvent.click(nextButton)

      expect(screen.getByText(/Página 2 de/)).toBeInTheDocument()

      const statusSelect = screen.getByLabelText('Status') as HTMLSelectElement
      await userEvent.selectOptions(statusSelect, 'ACCEPTABLE')

      expect(screen.getByText(/Página 1 de/)).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('should have proper heading hierarchy', () => {
      render(<BatchTable batches={mockBatches} />)

      const filterTitle = screen.getByText('Filtros')
      expect(filterTitle.tagName).toBe('H3')
    })

    it('should have proper table structure', () => {
      render(<BatchTable batches={mockBatches} />)

      const table = screen.getByRole('table')
      expect(table).toBeInTheDocument()

      const headers = screen.getAllByRole('columnheader')
      expect(headers.length).toBe(5)
    })

    it('should have keyboard accessible rows', async () => {
      const onRowClick = vi.fn()
      render(<BatchTable batches={mockBatches} onRowClick={onRowClick} />)

      const firstRow = screen.getByText('batch-001').closest('tr')
      expect(firstRow).toHaveAttribute('tabIndex', '0')
      expect(firstRow).toHaveAttribute('role', 'button')
    })
  })

  describe('Edge Cases', () => {
    it('should handle empty batches array', () => {
      render(<BatchTable batches={[]} />)

      expect(screen.getByText(/Nenhum batch encontrado/)).toBeInTheDocument()
    })

    it('should handle single batch', () => {
      render(<BatchTable batches={[mockBatches[0]]} />)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText(/Página 1 de 1/)).toBeInTheDocument()
    })

    it('should handle batches with same score', () => {
      const sameBatches = [
        { ...mockBatches[0], compliance_score: 75 },
        { ...mockBatches[1], id: 'batch-004', compliance_score: 75 },
      ]

      render(<BatchTable batches={sameBatches} />)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-004')).toBeInTheDocument()
    })

    it('should handle batches with same date', () => {
      const sameDateBatches = [
        mockBatches[0],
        { ...mockBatches[1], id: 'batch-004', upload_date: mockBatches[0].upload_date },
      ]

      render(<BatchTable batches={sameDateBatches} />)

      expect(screen.getByText('batch-001')).toBeInTheDocument()
      expect(screen.getByText('batch-004')).toBeInTheDocument()
    })
  })
})
