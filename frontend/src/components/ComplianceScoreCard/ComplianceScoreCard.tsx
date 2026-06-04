import React from 'react'
import './ComplianceScoreCard.module.css'

/**
 * ComplianceScoreCard Component
 * 
 * Displays Manufacturing Compliance Score with visual progress bar and classification.
 * 
 * Features:
 * - Score display (0-100)
 * - Visual progress bar with color coding
 * - Classification badge (ACCEPTABLE/WARNING/CRITICAL)
 * - Color-coded status (Green/Yellow/Red)
 * - Mandatory disclaimer
 * - Responsive design
 * 
 * @component
 * @example
 * ```tsx
 * <ComplianceScoreCard score={85} />
 * ```
 */

interface ComplianceScoreCardProps {
  score: number // 0-100
  className?: string
}

type ComplianceStatus = 'ACCEPTABLE' | 'WARNING' | 'CRITICAL'

const ComplianceScoreCard: React.FC<ComplianceScoreCardProps> = ({ 
  score, 
  className = '' 
}) => {
  /**
   * Classifies score into status categories
   */
  const classifyScore = (value: number): ComplianceStatus => {
    if (value >= 80) return 'ACCEPTABLE'
    if (value >= 60) return 'WARNING'
    return 'CRITICAL'
  }

  /**
   * Gets color for status
   */
  const getStatusColor = (status: ComplianceStatus): string => {
    switch (status) {
      case 'ACCEPTABLE':
        return '#10b981' // green
      case 'WARNING':
        return '#f59e0b' // amber
      case 'CRITICAL':
        return '#ef4444' // red
      default:
        return '#6b7280' // gray
    }
  }

  /**
   * Gets description for status
   */
  const getStatusDescription = (status: ComplianceStatus): string => {
    switch (status) {
      case 'ACCEPTABLE':
        return 'Processo conforme especificação'
      case 'WARNING':
        return 'Atenção necessária - desvios detectados'
      case 'CRITICAL':
        return 'Intervenção imediata recomendada'
      default:
        return ''
    }
  }

  const status = classifyScore(score)
  const statusColor = getStatusColor(status)
  const description = getStatusDescription(status)

  // Ensure score is between 0 and 100
  const normalizedScore = Math.max(0, Math.min(100, score))

  return (
    <div className={`compliance-score-card ${className}`}>
      {/* Header */}
      <div className="card-header">
        <h2 className="card-title">Compliance Score</h2>
        <span 
          className="status-badge"
          style={{ backgroundColor: statusColor }}
          data-testid="status-badge"
        >
          {status}
        </span>
      </div>

      {/* Score Display */}
      <div className="score-display">
        <div 
          className="score-circle"
          style={{ borderColor: statusColor }}
          data-testid="score-circle"
        >
          <span className="score-value" data-testid="score-value">
            {normalizedScore}
          </span>
          <span className="score-unit">/100</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-container">
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${normalizedScore}%`,
              backgroundColor: statusColor
            }}
            data-testid="progress-fill"
          ></div>
        </div>
        <div className="progress-labels">
          <span className="progress-label">0</span>
          <span className="progress-label">50</span>
          <span className="progress-label">100</span>
        </div>
      </div>

      {/* Classification Ranges */}
      <div className="classification-ranges">
        <div className="range-item acceptable">
          <span className="range-label">ACCEPTABLE</span>
          <span className="range-values">80-100</span>
        </div>
        <div className="range-item warning">
          <span className="range-label">WARNING</span>
          <span className="range-values">60-79</span>
        </div>
        <div className="range-item critical">
          <span className="range-label">CRITICAL</span>
          <span className="range-values">0-59</span>
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

export default ComplianceScoreCard
