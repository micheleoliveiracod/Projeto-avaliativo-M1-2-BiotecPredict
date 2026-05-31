import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ComplianceScoreCard from './ComplianceScoreCard'

describe('ComplianceScoreCard', () => {
  describe('Rendering', () => {
    it('should render the component with title', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByText('Compliance Score')).toBeInTheDocument()
    })

    it('should display the score value', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByTestId('score-value')).toHaveTextContent('85')
    })

    it('should display the score unit', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByText('/100')).toBeInTheDocument()
    })

    it('should render the disclaimer', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByText(/Esta análise é baseada em dados históricos/)).toBeInTheDocument()
    })
  })

  describe('Classification - ACCEPTABLE (80-100)', () => {
    it('should classify score 80 as ACCEPTABLE', () => {
      render(<ComplianceScoreCard score={80} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('ACCEPTABLE')
    })

    it('should classify score 90 as ACCEPTABLE', () => {
      render(<ComplianceScoreCard score={90} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('ACCEPTABLE')
    })

    it('should classify score 100 as ACCEPTABLE', () => {
      render(<ComplianceScoreCard score={100} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('ACCEPTABLE')
    })

    it('should display green color for ACCEPTABLE status', () => {
      render(<ComplianceScoreCard score={85} />)
      const badge = screen.getByTestId('status-badge')
      expect(badge).toHaveStyle({ backgroundColor: '#10b981' })
    })

    it('should display correct description for ACCEPTABLE', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByTestId('description-text')).toHaveTextContent(
        'Processo conforme especificação'
      )
    })
  })

  describe('Classification - WARNING (60-79)', () => {
    it('should classify score 60 as WARNING', () => {
      render(<ComplianceScoreCard score={60} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('WARNING')
    })

    it('should classify score 70 as WARNING', () => {
      render(<ComplianceScoreCard score={70} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('WARNING')
    })

    it('should classify score 79 as WARNING', () => {
      render(<ComplianceScoreCard score={79} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('WARNING')
    })

    it('should display amber color for WARNING status', () => {
      render(<ComplianceScoreCard score={70} />)
      const badge = screen.getByTestId('status-badge')
      expect(badge).toHaveStyle({ backgroundColor: '#f59e0b' })
    })

    it('should display correct description for WARNING', () => {
      render(<ComplianceScoreCard score={70} />)
      expect(screen.getByTestId('description-text')).toHaveTextContent(
        'Atenção necessária - desvios detectados'
      )
    })
  })

  describe('Classification - CRITICAL (0-59)', () => {
    it('should classify score 0 as CRITICAL', () => {
      render(<ComplianceScoreCard score={0} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('CRITICAL')
    })

    it('should classify score 30 as CRITICAL', () => {
      render(<ComplianceScoreCard score={30} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('CRITICAL')
    })

    it('should classify score 59 as CRITICAL', () => {
      render(<ComplianceScoreCard score={59} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('CRITICAL')
    })

    it('should display red color for CRITICAL status', () => {
      render(<ComplianceScoreCard score={30} />)
      const badge = screen.getByTestId('status-badge')
      expect(badge).toHaveStyle({ backgroundColor: '#ef4444' })
    })

    it('should display correct description for CRITICAL', () => {
      render(<ComplianceScoreCard score={30} />)
      expect(screen.getByTestId('description-text')).toHaveTextContent(
        'Intervenção imediata recomendada'
      )
    })
  })

  describe('Progress Bar', () => {
    it('should set progress bar width to 0% for score 0', () => {
      render(<ComplianceScoreCard score={0} />)
      const progressFill = screen.getByTestId('progress-fill')
      expect(progressFill).toHaveStyle({ width: '0%' })
    })

    it('should set progress bar width to 50% for score 50', () => {
      render(<ComplianceScoreCard score={50} />)
      const progressFill = screen.getByTestId('progress-fill')
      expect(progressFill).toHaveStyle({ width: '50%' })
    })

    it('should set progress bar width to 100% for score 100', () => {
      render(<ComplianceScoreCard score={100} />)
      const progressFill = screen.getByTestId('progress-fill')
      expect(progressFill).toHaveStyle({ width: '100%' })
    })

    it('should set progress bar color based on status', () => {
      render(<ComplianceScoreCard score={85} />)
      const progressFill = screen.getByTestId('progress-fill')
      expect(progressFill).toHaveStyle({ backgroundColor: '#10b981' })
    })
  })

  describe('Edge Cases', () => {
    it('should handle score above 100 by clamping to 100', () => {
      render(<ComplianceScoreCard score={150} />)
      expect(screen.getByTestId('score-value')).toHaveTextContent('100')
    })

    it('should handle negative score by clamping to 0', () => {
      render(<ComplianceScoreCard score={-10} />)
      expect(screen.getByTestId('score-value')).toHaveTextContent('0')
    })

    it('should handle decimal scores', () => {
      render(<ComplianceScoreCard score={85.5} />)
      expect(screen.getByTestId('score-value')).toHaveTextContent('85')
    })

    it('should handle boundary score 79.9 as WARNING', () => {
      render(<ComplianceScoreCard score={79.9} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('WARNING')
    })

    it('should handle boundary score 80.1 as ACCEPTABLE', () => {
      render(<ComplianceScoreCard score={80.1} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('ACCEPTABLE')
    })

    it('should handle boundary score 59.9 as CRITICAL', () => {
      render(<ComplianceScoreCard score={59.9} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('CRITICAL')
    })

    it('should handle boundary score 60.1 as WARNING', () => {
      render(<ComplianceScoreCard score={60.1} />)
      expect(screen.getByTestId('status-badge')).toHaveTextContent('WARNING')
    })
  })

  describe('Props', () => {
    it('should accept custom className', () => {
      const { container } = render(
        <ComplianceScoreCard score={85} className="custom-class" />
      )
      expect(container.querySelector('.compliance-score-card')).toHaveClass('custom-class')
    })

    it('should render with default className when not provided', () => {
      const { container } = render(<ComplianceScoreCard score={85} />)
      expect(container.querySelector('.compliance-score-card')).toBeInTheDocument()
    })
  })

  describe('Visual Elements', () => {
    it('should render score circle', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByTestId('score-circle')).toBeInTheDocument()
    })

    it('should render classification ranges section', () => {
      const { container } = render(<ComplianceScoreCard score={85} />)
      expect(container.querySelector('.classification-ranges')).toBeInTheDocument()
    })

    it('should render all three classification range items', () => {
      const { container } = render(<ComplianceScoreCard score={85} />)
      const rangeItems = container.querySelectorAll('.range-item')
      expect(rangeItems).toHaveLength(3)
    })

    it('should display ACCEPTABLE range label', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByText('ACCEPTABLE')).toBeInTheDocument()
    })

    it('should display WARNING range label', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByText('WARNING')).toBeInTheDocument()
    })

    it('should display CRITICAL range label', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByText('CRITICAL')).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('should have proper heading hierarchy', () => {
      render(<ComplianceScoreCard score={85} />)
      const title = screen.getByText('Compliance Score')
      expect(title.tagName).toBe('H2')
    })

    it('should have descriptive text for status', () => {
      render(<ComplianceScoreCard score={85} />)
      expect(screen.getByTestId('description-text')).toBeInTheDocument()
    })

    it('should include disclaimer for user awareness', () => {
      render(<ComplianceScoreCard score={85} />)
      const disclaimer = screen.getByText(/Esta análise é baseada em dados históricos/)
      expect(disclaimer).toBeInTheDocument()
    })
  })
})
