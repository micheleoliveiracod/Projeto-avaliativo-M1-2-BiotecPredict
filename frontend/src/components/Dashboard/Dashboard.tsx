import React, { useState, useEffect } from 'react'
import './Dashboard.css'

/**
 * Dashboard Component
 * 
 * Main dashboard component that consolidates all unified dashboard elements into a single screen.
 * Displays compliance score, risk prediction, sensor charts, and batch history table.
 * 
 * Features:
 * - Responsive grid layout (mobile, tablet, desktop)
 * - Compliance Score Card (0-100 with classification)
 * - Risk Prediction Card (LOW/MEDIUM/HIGH with confidence)
 * - Sensor Charts (5 sensors: Temperature, pH, DO, Pressure, Agitator Speed)
 * - Batch History Table with filters and pagination
 * - Real-time data updates
 * - TypeScript type safety
 * 
 * @component
 * @example
 * ```tsx
 * <Dashboard />
 * ```
 */

interface SensorData {
  temperature: number
  ph: number
  dissolved_oxygen: number
  pressure: number
  agitator_speed: number
}

interface Batch {
  id: number
  upload_date: string
  compliance_score: number | null
  risk_prediction: string | null
  status: string
}

interface DashboardProps {
  refreshInterval?: number // milliseconds
}

const Dashboard: React.FC<DashboardProps> = ({ refreshInterval = 30000 }) => {
  // State for compliance score
  const [complianceScore, setComplianceScore] = useState<number>(0)
  const [complianceStatus, setComplianceStatus] = useState<'ACCEPTABLE' | 'WARNING' | 'CRITICAL'>('ACCEPTABLE')

  // State for risk prediction
  const [riskPrediction, setRiskPrediction] = useState<'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK'>('LOW_RISK')
  const [confidenceScore, setConfidenceScore] = useState<number>(0)

  // State for sensor data
  const [sensorData, setSensorData] = useState<SensorData>({
    temperature: 0,
    ph: 0,
    dissolved_oxygen: 0,
    pressure: 0,
    agitator_speed: 0
  })

  // State for batch table
  const [batches, setBatches] = useState<Batch[]>([])
  const [filteredBatches, setFilteredBatches] = useState<Batch[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // State for filters
  const [filters, setFilters] = useState({
    status: 'all',
    scoreRange: 'all',
    dateRange: 'all'
  })

  // State for pagination
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  /**
   * Classifies compliance score into status categories
   */
  const classifyComplianceScore = (score: number): 'ACCEPTABLE' | 'WARNING' | 'CRITICAL' => {
    if (score >= 80) return 'ACCEPTABLE'
    if (score >= 60) return 'WARNING'
    return 'CRITICAL'
  }

  /**
   * Fetches dashboard data from API
   */
  const fetchDashboardData = async () => {
    try {
      setIsLoading(true)
      setError(null)

      // Fetch batches list
      const batchesResponse = await fetch('/api/v1/batches')
      if (!batchesResponse.ok) {
        throw new Error('Failed to fetch batches')
      }
      const batchesData = await batchesResponse.json()
      
      // Ensure batches is an array
      const batchesArray = Array.isArray(batchesData) ? batchesData : batchesData.batches || []
      setBatches(batchesArray)

      // If there are batches, fetch details for the latest one
      if (batchesArray.length > 0) {
        const latestBatch = batchesArray[0]
        
        // Fetch compliance score
        const complianceResponse = await fetch(
          `/api/v1/compliance/${latestBatch.id}`
        )
        if (complianceResponse.ok) {
          const complianceData = await complianceResponse.json()
          const score = complianceData.compliance_score || 0
          setComplianceScore(score)
          setComplianceStatus(classifyComplianceScore(score))
        }

        // Fetch prediction
        const predictionResponse = await fetch(
          `/api/v1/prediction/${latestBatch.id}`
        )
        if (predictionResponse.ok) {
          const predictionData = await predictionResponse.json()
          setRiskPrediction(predictionData.risk_prediction || 'LOW_RISK')
          setConfidenceScore(predictionData.confidence_score || 0)
        }

        // Fetch sensor readings and compute averages
        const sensorsResponse = await fetch(`/api/v1/batch/${latestBatch.id}/sensors`)
        if (sensorsResponse.ok) {
          const sensorsData = await sensorsResponse.json()
          const readings = sensorsData.readings || []
          if (readings.length > 0) {
            const avg = (field: string) =>
              readings.reduce((sum: number, r: Record<string, number>) => sum + (r[field] || 0), 0) / readings.length
            setSensorData({
              temperature: avg('temperature'),
              ph: avg('ph'),
              dissolved_oxygen: avg('dissolved_oxygen'),
              pressure: avg('pressure'),
              agitator_speed: avg('agitator_speed'),
            })
          }
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch dashboard data'
      setError(errorMessage)
      console.error('Dashboard error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Applies filters to batches
   */
  const applyFilters = () => {
    let filtered = [...batches]

    // Filter by status
    if (filters.status !== 'all') {
      filtered = filtered.filter(batch => batch.status === filters.status)
    }

    // Filter by score range
    if (filters.scoreRange !== 'all') {
      filtered = filtered.filter(batch => {
        const score = batch.compliance_score ?? -1
        switch (filters.scoreRange) {
          case 'acceptable':
            return score >= 80
          case 'warning':
            return score >= 60 && score < 80
          case 'critical':
            return score < 60
          default:
            return true
        }
      })
    }

    // Filter by date range
    if (filters.dateRange !== 'all') {
      const now = new Date()
      filtered = filtered.filter(batch => {
        const batchDate = new Date(batch.upload_date)
        const daysDiff = (now.getTime() - batchDate.getTime()) / (1000 * 60 * 60 * 24)
        
        switch (filters.dateRange) {
          case 'today':
            return daysDiff < 1
          case 'week':
            return daysDiff < 7
          case 'month':
            return daysDiff < 30
          default:
            return true
        }
      })
    }

    setFilteredBatches(filtered)
    setCurrentPage(1) // Reset to first page
  }

  /**
   * Handles filter change
   */
  const handleFilterChange = (filterName: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }))
  }

  /**
   * Gets color for compliance status
   */
  const getStatusColor = (status: string): string => {
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
   * Gets color for risk level
   */
  const getRiskColor = (risk: string): string => {
    switch (risk) {
      case 'LOW_RISK':
        return '#10b981' // green
      case 'MEDIUM_RISK':
        return '#f59e0b' // amber
      case 'HIGH_RISK':
        return '#ef4444' // red
      default:
        return '#6b7280' // gray
    }
  }

  /**
   * Formats date for display
   */
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  // Fetch data on component mount and set up refresh interval
  useEffect(() => {
    fetchDashboardData()
    const interval = setInterval(fetchDashboardData, refreshInterval)
    return () => clearInterval(interval)
  }, [refreshInterval])

  // Apply filters when batches or filters change
  useEffect(() => {
    applyFilters()
  }, [batches, filters])

  // Calculate pagination
  const totalPages = Math.ceil(filteredBatches.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const paginatedBatches = filteredBatches.slice(startIndex, endIndex)

  if (isLoading && batches.length === 0) {
    return (
      <div className="dashboard-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Carregando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <h2 className="dashboard-title">Dashboard Analítico</h2>
        <p className="dashboard-subtitle">Monitoramento de Processos de Manufatura</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-banner">
          <p>{error}</p>
          <button onClick={fetchDashboardData} className="retry-button">
            Tentar Novamente
          </button>
        </div>
      )}

      {/* KPI Cards Row */}
      <div className="kpi-row">
        {/* Compliance Score Card */}
        <div className="kpi-card compliance-card">
          <div className="card-header">
            <h2 className="card-title">Compliance Score</h2>
            <span className="card-badge" style={{ backgroundColor: getStatusColor(complianceStatus) }}>
              {complianceStatus}
            </span>
          </div>
          <div className="card-content">
            <div className="score-display">
              <div className="score-circle" style={{ borderColor: getStatusColor(complianceStatus) }}>
                <span className="score-value">{complianceScore}</span>
                <span className="score-unit">/100</span>
              </div>
            </div>
            <div className="score-description">
              <p className="description-text">
                {complianceStatus === 'ACCEPTABLE' && 'Processo conforme especificação'}
                {complianceStatus === 'WARNING' && 'Atenção necessária - desvios detectados'}
                {complianceStatus === 'CRITICAL' && 'Intervenção imediata recomendada'}
              </p>
            </div>
          </div>
        </div>

        {/* Risk Prediction Card */}
        <div className="kpi-card risk-card">
          <div className="card-header">
            <h2 className="card-title">Predição de Risco</h2>
            <span className="card-badge" style={{ backgroundColor: getRiskColor(riskPrediction) }}>
              {riskPrediction}
            </span>
          </div>
          <div className="card-content">
            <div className="risk-display">
              <div className="risk-indicator" style={{ backgroundColor: getRiskColor(riskPrediction) }}></div>
              <div className="risk-info">
                <p className="risk-label">Confiança</p>
                <p className="risk-value">{(confidenceScore * 100).toFixed(1)}%</p>
              </div>
            </div>
            <div className="risk-description">
              <p className="description-text">
                {riskPrediction === 'LOW_RISK' && 'Processo dentro dos parâmetros esperados'}
                {riskPrediction === 'MEDIUM_RISK' && 'Desvios moderados detectados'}
                {riskPrediction === 'HIGH_RISK' && 'Risco significativo de falha de processo'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Sensor Charts Row */}
      <div className="charts-row">
        <h2 className="section-title">Variáveis de Sensores</h2>
        
        <div className="sensor-grid">
          {/* Temperature Chart */}
          <div className="sensor-card">
            <div className="sensor-header">
              <h3 className="sensor-name">Temperatura</h3>
              <span className="sensor-unit">°C</span>
            </div>
            <div className="sensor-value-display">
              <span className="sensor-value">{sensorData.temperature.toFixed(1)}</span>
            </div>
            <div className="sensor-range">
              <p className="range-text">Aceitável: 20 – 30°C | Ideal: 24 – 26°C</p>
              <div className="range-bar">
                <div
                  className="range-fill"
                  style={{
                    width: `${Math.min(100, ((sensorData.temperature - 20) / 10) * 100)}%`,
                    backgroundColor: sensorData.temperature >= 20 && sensorData.temperature <= 30 ? '#10b981' : '#ef4444'
                  }}
                ></div>
              </div>
            </div>
          </div>

          {/* pH Chart */}
          <div className="sensor-card">
            <div className="sensor-header">
              <h3 className="sensor-name">pH</h3>
              <span className="sensor-unit">-</span>
            </div>
            <div className="sensor-value-display">
              <span className="sensor-value">{sensorData.ph.toFixed(2)}</span>
            </div>
            <div className="sensor-range">
              <p className="range-text">Aceitável: 6.5 – 7.5 | Ideal: 6.8 – 7.2</p>
              <div className="range-bar">
                <div
                  className="range-fill"
                  style={{
                    width: `${Math.min(100, ((sensorData.ph - 6.5) / 1.0) * 100)}%`,
                    backgroundColor: sensorData.ph >= 6.5 && sensorData.ph <= 7.5 ? '#10b981' : '#ef4444'
                  }}
                ></div>
              </div>
            </div>
          </div>

          {/* Dissolved Oxygen Chart */}
          <div className="sensor-card">
            <div className="sensor-header">
              <h3 className="sensor-name">Oxigênio Dissolvido</h3>
              <span className="sensor-unit">%</span>
            </div>
            <div className="sensor-value-display">
              <span className="sensor-value">{sensorData.dissolved_oxygen.toFixed(1)}</span>
            </div>
            <div className="sensor-range">
              <p className="range-text">Aceitável: 70 – 100% | Ideal: 80 – 95%</p>
              <div className="range-bar">
                <div
                  className="range-fill"
                  style={{
                    width: `${Math.min(100, ((sensorData.dissolved_oxygen - 70) / 30) * 100)}%`,
                    backgroundColor: sensorData.dissolved_oxygen >= 70 && sensorData.dissolved_oxygen <= 100 ? '#10b981' : '#ef4444'
                  }}
                ></div>
              </div>
            </div>
          </div>

          {/* Pressure Chart */}
          <div className="sensor-card">
            <div className="sensor-header">
              <h3 className="sensor-name">Pressão</h3>
              <span className="sensor-unit">bar</span>
            </div>
            <div className="sensor-value-display">
              <span className="sensor-value">{sensorData.pressure.toFixed(2)}</span>
            </div>
            <div className="sensor-range">
              <p className="range-text">Aceitável: 4.5 – 6.0 bar | Ideal: 4.8 – 5.5 bar</p>
              <div className="range-bar">
                <div
                  className="range-fill"
                  style={{
                    width: `${Math.min(100, ((sensorData.pressure - 4.5) / 1.5) * 100)}%`,
                    backgroundColor: sensorData.pressure >= 4.5 && sensorData.pressure <= 6.0 ? '#10b981' : '#ef4444'
                  }}
                ></div>
              </div>
            </div>
          </div>

          {/* Agitator Speed Chart */}
          <div className="sensor-card">
            <div className="sensor-header">
              <h3 className="sensor-name">Velocidade do Agitador</h3>
              <span className="sensor-unit">RPM</span>
            </div>
            <div className="sensor-value-display">
              <span className="sensor-value">{sensorData.agitator_speed.toFixed(0)}</span>
            </div>
            <div className="sensor-range">
              <p className="range-text">Aceitável: 200 – 300 RPM | Ideal: 240 – 280 RPM</p>
              <div className="range-bar">
                <div
                  className="range-fill"
                  style={{
                    width: `${Math.min(100, ((sensorData.agitator_speed - 200) / 100) * 100)}%`,
                    backgroundColor: sensorData.agitator_speed >= 200 && sensorData.agitator_speed <= 300 ? '#10b981' : '#ef4444'
                  }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Batch History Section */}
      <div className="batch-history-section">
        <h2 className="section-title">Histórico de Batches</h2>

        {/* Filters */}
        <div className="filters-row">
          <div className="filter-group">
            <label htmlFor="status-filter" className="filter-label">Status</label>
            <select
              id="status-filter"
              className="filter-select"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <option value="all">Todos</option>
              <option value="COMPLETED">Concluído</option>
              <option value="PROCESSING">Processando</option>
              <option value="FAILED">Falha</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="score-filter" className="filter-label">Score</label>
            <select
              id="score-filter"
              className="filter-select"
              value={filters.scoreRange}
              onChange={(e) => handleFilterChange('scoreRange', e.target.value)}
            >
              <option value="all">Todos</option>
              <option value="acceptable">Aceitável (80-100)</option>
              <option value="warning">Aviso (60-79)</option>
              <option value="critical">Crítico (0-59)</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="date-filter" className="filter-label">Período</label>
            <select
              id="date-filter"
              className="filter-select"
              value={filters.dateRange}
              onChange={(e) => handleFilterChange('dateRange', e.target.value)}
            >
              <option value="all">Todos</option>
              <option value="today">Hoje</option>
              <option value="week">Última Semana</option>
              <option value="month">Último Mês</option>
            </select>
          </div>
        </div>

        {/* Batch Table */}
        <div className="table-container">
          {paginatedBatches.length > 0 ? (
            <table className="batch-table">
              <thead>
                <tr>
                  <th>ID do Batch</th>
                  <th>Data de Upload</th>
                  <th>Compliance Score</th>
                  <th>Predição de Risco</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {paginatedBatches.map((batch) => (
                  <tr key={batch.id} className="table-row">
                    <td className="table-cell batch-id">{batch.id}</td>
                    <td className="table-cell">{formatDate(batch.upload_date)}</td>
                    <td className="table-cell">
                      {batch.compliance_score != null ? (
                        <span
                          className="score-badge"
                          style={{ backgroundColor: getStatusColor(classifyComplianceScore(batch.compliance_score)) }}
                        >
                          {batch.compliance_score}
                        </span>
                      ) : (
                        <span className="score-badge" style={{ backgroundColor: '#6b7280' }}>—</span>
                      )}
                    </td>
                    <td className="table-cell">
                      <span
                        className="risk-badge"
                        style={{ backgroundColor: getRiskColor(batch.risk_prediction ?? '') }}
                      >
                        {batch.risk_prediction ?? '—'}
                      </span>
                    </td>
                    <td className="table-cell">
                      <span className="status-badge">{batch.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <p>Nenhum batch encontrado com os filtros selecionados</p>
            </div>
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="pagination">
            <button
              className="pagination-button"
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            >
              ← Anterior
            </button>

            <div className="pagination-info">
              Página {currentPage} de {totalPages}
            </div>

            <button
              className="pagination-button"
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
            >
              Próxima →
            </button>
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="disclaimer">
        <p>
          <strong>Aviso:</strong> Esta análise é baseada em dados históricos de manufatura. 
          Não constitui recomendação de ação. A decisão final sobre ações corretivas é sempre do operador.
        </p>
      </div>
    </div>
  )
}

export default Dashboard
