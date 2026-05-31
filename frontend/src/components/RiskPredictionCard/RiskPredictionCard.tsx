import React from 'react'
import './RiskPredictionCard.module.css'

/**
 * RiskPredictionCard Component
 * 
 * Displays ML-based risk prediction with confidence score and visual indicators.
 * 
 * Features:
 * - Risk level display (LOW/MEDIUM/HIGH)
 * - Confidence score (0-1) displayed as percentage
 * - Visual risk indicators (icons and colors)
 * - Color-coded status (Green/Yellow/Red)
 * - Mandatory disclaimer
 * - Responsive design
 * 
 * @component
 * @example
 * ```tsx
 * <RiskPredictionCard riskLevel="LOW RISK" confidenceScore={0.92} />
 * ```
 */

interface RiskPredictionCardProps {
  riskLevel: 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK'
  confidenceScore: number // 0-1
  className?: string
}

type RiskLevel = 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK'

const RiskPredictionCard: React.FC<RiskPredictionCardProps> = ({ 
  riskLevel, 
  confidenceScore,
  className = '' 
}) => {
  /**
   * Gets color for risk level
   */
  const getRiskColor = (risk: RiskLevel): string => {
    switch (risk) {
      case 'LOW RISK':
        return '#10b981' // green
      case 'MEDIUM RISK':
        return '#f59e0b' // amber
      case 'HIGH RISK':
        return '#ef4444' // red
      default:
        return '#6b7280' // gray
    }
  }

  /**
   * Gets icon for risk level
   */
  const getRiskIcon = (risk: RiskLevel): string => {
    switch (risk) {
      case 'LOW RISK':
        return '✓' // checkmark
      case 'MEDIUM RISK':
        return '⚠' // warning
      case 'HIGH RISK':
        return '✕' // cross
      default:
        return '?'
    }
  }

  /**
   * Gets description for risk level
   */
  const getRiskDescription = (risk: RiskLevel): string => {
    switch (risk) {
      case 'LOW RISK':
        return 'Processo dentro dos parâmetros esperados'
      case 'MEDIUM RISK':
        return 'Desvios moderados detectados'
      case 'HIGH RISK':
        return 'Risco significativo de falha de processo'
      default:
        return ''
    }
  }

  // Ensure confidence score is between 0 and 1
  const normalizedConfidence = Math.max(0, Math.min(1, confidenceScore))
  const confidencePercentage = (normalizedConfidence * 100).toFixed(1)
  const riskColor = getRiskColor(riskLevel)
  const riskIcon = getRiskIcon(riskLevel)
  const description = getRiskDescription(riskLevel)

  return (
    <div className={`risk-prediction-card ${className}`}>
      {/* Header */}
      <div className="card-header">
        <h2 className="card-title">Predição de Risco</h2>
        <span 
          className="risk-badge"
          style={{ backgroundColor: riskColor }}
          data-testid="risk-badge"
        >
          {riskLevel}
        </span>
      </div>

      {/* Risk Display */}
      <div className="risk-display">
        <div 
          className="risk-indicator"
          style={{ backgroundColor: riskColor }}
          data-testid="risk-indicator"
        >
          <span className="risk-icon">{riskIcon}</span>
        </div>
        <div className="risk-info">
          <p className="risk-label">Nível de Risco</p>
          <p className="risk-value" data-testid="risk-value">
            {riskLevel}
          </p>
        </div>
      </div>

      {/* Confidence Score */}
      <div className="confidence-section">
        <div className="confidence-header">
          <p className="confidence-label">Confiança da Predição</p>
          <p className="confidence-percentage" data-testid="confidence-percentage">
            {confidencePercentage}%
          </p>
        </div>

        {/* Confidence Bar */}
        <div className="confidence-bar">
          <div 
            className="confidence-fill"
            style={{ 
              width: `${normalizedConfidence * 100}%`,
              backgroundColor: riskColor
            }}
            data-testid="confidence-fill"
          ></div>
        </div>

        {/* Confidence Levels */}
        <div className="confidence-levels">
          <div className="level-item low">
            <span className="level-label">Baixa</span>
            <span className="level-range">0-33%</span>
          </div>
          <div className="level-item medium">
            <span className="level-label">Média</span>
            <span className="level-range">34-66%</span>
          </div>
          <div className="level-item high">
            <span className="level-label">Alta</span>
            <span className="level-range">67-100%</span>
          </div>
        </div>
      </div>

      {/* Risk Levels Reference */}
      <div className="risk-levels-reference">
        <div className="reference-item low-risk">
          <span className="reference-icon">✓</span>
          <div className="reference-content">
            <p className="reference-label">LOW RISK</p>
            <p className="reference-description">Processo dentro dos parâmetros</p>
          </div>
        </div>
        <div className="reference-item medium-risk">
          <span className="reference-icon">⚠</span>
          <div className="reference-content">
            <p className="reference-label">MEDIUM RISK</p>
            <p className="reference-description">Desvios moderados detectados</p>
          </div>
        </div>
        <div className="reference-item high-risk">
          <span className="reference-icon">✕</span>
          <div className="reference-content">
            <p className="reference-label">HIGH RISK</p>
            <p className="reference-description">Risco significativo de falha</p>
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="description">
        <p className="description-text" data-testid="description-text">
          {description}
        </p>
      </div>

      {/* Disclaimer */}
      <div className="disclaimer">
        <p className="disclaimer-text">
          <strong>Aviso:</strong> Esta análise é baseada em dados históricos de manufatura. 
          Não constitui recomendação de ação. A decisão final sobre ações corretivas é sempre do operador.
        </p>
      </div>
    </div>
  )
}

export default RiskPredictionCard
