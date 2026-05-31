import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import RiskPredictionCard from './RiskPredictionCard'

describe('RiskPredictionCard', () => {
  describe('Rendering', () => {
    it('should render the component with title', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByText('Predição de Risco')).toBeInTheDocument()
    })

    it('should display the risk level', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('risk-value')).toHaveTextContent('LOW RISK')
    })

    it('should display the confidence percentage', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('92.0%')
    })

    it('should render the disclaimer', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByText(/Esta análise é baseada em dados históricos/)).toBeInTheDocument()
    })
  })

  describe('Risk Levels - LOW RISK', () => {
    it('should display LOW RISK badge', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('risk-badge')).toHaveTextContent('LOW RISK')
    })

    it('should display green color for LOW RISK', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      const badge = screen.getByTestId('risk-badge')
      expect(badge).toHaveStyle({ backgroundColor: '#10b981' })
    })

    it('should display correct description for LOW RISK', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('description-text')).toHaveTextContent(
        'Processo dentro dos parâmetros esperados'
      )
    })

    it('should display checkmark icon for LOW RISK', () => {
      const { container } = render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      const icon = container.querySelector('.risk-icon')
      expect(icon?.textContent).toBe('✓')
    })
  })

  describe('Risk Levels - MEDIUM RISK', () => {
    it('should display MEDIUM RISK badge', () => {
      render(<RiskPredictionCard riskLevel="MEDIUM RISK" confidenceScore={0.75} />)
      expect(screen.getByTestId('risk-badge')).toHaveTextContent('MEDIUM RISK')
    })

    it('should display amber color for MEDIUM RISK', () => {
      render(<RiskPredictionCard riskLevel="MEDIUM RISK" confidenceScore={0.75} />)
      const badge = screen.getByTestId('risk-badge')
      expect(badge).toHaveStyle({ backgroundColor: '#f59e0b' })
    })

    it('should display correct description for MEDIUM RISK', () => {
      render(<RiskPredictionCard riskLevel="MEDIUM RISK" confidenceScore={0.75} />)
      expect(screen.getByTestId('description-text')).toHaveTextContent(
        'Desvios moderados detectados'
      )
    })

    it('should display warning icon for MEDIUM RISK', () => {
      const { container } = render(<RiskPredictionCard riskLevel="MEDIUM RISK" confidenceScore={0.75} />)
      const icon = container.querySelector('.risk-icon')
      expect(icon?.textContent).toBe('⚠')
    })
  })

  describe('Risk Levels - HIGH RISK', () => {
    it('should display HIGH RISK badge', () => {
      render(<RiskPredictionCard riskLevel="HIGH RISK" confidenceScore={0.88} />)
      expect(screen.getByTestId('risk-badge')).toHaveTextContent('HIGH RISK')
    })

    it('should display red color for HIGH RISK', () => {
      render(<RiskPredictionCard riskLevel="HIGH RISK" confidenceScore={0.88} />)
      const badge = screen.getByTestId('risk-badge')
      expect(badge).toHaveStyle({ backgroundColor: '#ef4444' })
    })

    it('should display correct description for HIGH RISK', () => {
      render(<RiskPredictionCard riskLevel="HIGH RISK" confidenceScore={0.88} />)
      expect(screen.getByTestId('description-text')).toHaveTextContent(
        'Risco significativo de falha de processo'
      )
    })

    it('should display cross icon for HIGH RISK', () => {
      const { container } = render(<RiskPredictionCard riskLevel="HIGH RISK" confidenceScore={0.88} />)
      const icon = container.querySelector('.risk-icon')
      expect(icon?.textContent).toBe('✕')
    })
  })

  describe('Confidence Score', () => {
    it('should display confidence score as percentage', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.85} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('85.0%')
    })

    it('should set confidence bar width to 0% for score 0', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0} />)
      const confidenceFill = screen.getByTestId('confidence-fill')
      expect(confidenceFill).toHaveStyle({ width: '0%' })
    })

    it('should set confidence bar width to 50% for score 0.5', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.5} />)
      const confidenceFill = screen.getByTestId('confidence-fill')
      expect(confidenceFill).toHaveStyle({ width: '50%' })
    })

    it('should set confidence bar width to 100% for score 1', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={1} />)
      const confidenceFill = screen.getByTestId('confidence-fill')
      expect(confidenceFill).toHaveStyle({ width: '100%' })
    })

    it('should set confidence bar color based on risk level', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      const confidenceFill = screen.getByTestId('confidence-fill')
      expect(confidenceFill).toHaveStyle({ backgroundColor: '#10b981' })
    })

    it('should display confidence percentage with one decimal place', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.333} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('33.3%')
    })
  })

  describe('Edge Cases', () => {
    it('should handle confidence score above 1 by clamping to 1', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={1.5} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('100.0%')
    })

    it('should handle negative confidence score by clamping to 0', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={-0.5} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('0.0%')
    })

    it('should handle confidence score 0', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('0.0%')
    })

    it('should handle confidence score 1', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={1} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('100.0%')
    })

    it('should handle very small confidence score', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.001} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('0.1%')
    })

    it('should handle very high confidence score', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.999} />)
      expect(screen.getByTestId('confidence-percentage')).toHaveTextContent('99.9%')
    })
  })

  describe('Props', () => {
    it('should accept custom className', () => {
      const { container } = render(
        <RiskPredictionCard 
          riskLevel="LOW RISK" 
          confidenceScore={0.92}
          className="custom-class"
        />
      )
      expect(container.querySelector('.risk-prediction-card')).toHaveClass('custom-class')
    })

    it('should render with default className when not provided', () => {
      const { container } = render(
        <RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />
      )
      expect(container.querySelector('.risk-prediction-card')).toBeInTheDocument()
    })
  })

  describe('Visual Elements', () => {
    it('should render risk indicator', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('risk-indicator')).toBeInTheDocument()
    })

    it('should render confidence bar', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('confidence-fill')).toBeInTheDocument()
    })

    it('should render risk levels reference section', () => {
      const { container } = render(
        <RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />
      )
      expect(container.querySelector('.risk-levels-reference')).toBeInTheDocument()
    })

    it('should render all three risk level reference items', () => {
      const { container } = render(
        <RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />
      )
      const referenceItems = container.querySelectorAll('.reference-item')
      expect(referenceItems).toHaveLength(3)
    })

    it('should render confidence levels section', () => {
      const { container } = render(
        <RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />
      )
      expect(container.querySelector('.confidence-levels')).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('should have proper heading hierarchy', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      const title = screen.getByText('Predição de Risco')
      expect(title.tagName).toBe('H2')
    })

    it('should have descriptive text for risk level', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByTestId('description-text')).toBeInTheDocument()
    })

    it('should include disclaimer for user awareness', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      const disclaimer = screen.getByText(/Esta análise é baseada em dados históricos/)
      expect(disclaimer).toBeInTheDocument()
    })

    it('should display confidence label', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      expect(screen.getByText('Confiança da Predição')).toBeInTheDocument()
    })
  })

  describe('Color Consistency', () => {
    it('should use consistent green color for LOW RISK across elements', () => {
      render(<RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />)
      const badge = screen.getByTestId('risk-badge')
      const indicator = screen.getByTestId('risk-indicator')
      const confidenceFill = screen.getByTestId('confidence-fill')
      
      expect(badge).toHaveStyle({ backgroundColor: '#10b981' })
      expect(indicator).toHaveStyle({ backgroundColor: '#10b981' })
      expect(confidenceFill).toHaveStyle({ backgroundColor: '#10b981' })
    })

    it('should use consistent amber color for MEDIUM RISK across elements', () => {
      render(<RiskPredictionCard riskLevel="MEDIUM RISK" confidenceScore={0.75} />)
      const badge = screen.getByTestId('risk-badge')
      const indicator = screen.getByTestId('risk-indicator')
      const confidenceFill = screen.getByTestId('confidence-fill')
      
      expect(badge).toHaveStyle({ backgroundColor: '#f59e0b' })
      expect(indicator).toHaveStyle({ backgroundColor: '#f59e0b' })
      expect(confidenceFill).toHaveStyle({ backgroundColor: '#f59e0b' })
    })

    it('should use consistent red color for HIGH RISK across elements', () => {
      render(<RiskPredictionCard riskLevel="HIGH RISK" confidenceScore={0.88} />)
      const badge = screen.getByTestId('risk-badge')
      const indicator = screen.getByTestId('risk-indicator')
      const confidenceFill = screen.getByTestId('confidence-fill')
      
      expect(badge).toHaveStyle({ backgroundColor: '#ef4444' })
      expect(indicator).toHaveStyle({ backgroundColor: '#ef4444' })
      expect(confidenceFill).toHaveStyle({ backgroundColor: '#ef4444' })
    })
  })
})
