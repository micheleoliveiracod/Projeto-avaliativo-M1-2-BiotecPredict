import React, { useState, useMemo, useCallback } from 'react'
import styles from './BatchTable.module.css'

export interface Batch {
  id: string
  upload_date: string
  compliance_score: number
  risk_level: 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK'
  status: 'ACCEPTABLE' | 'WARNING' | 'CRITICAL'
}

export interface BatchTableProps {
  batches: Batch[]
  onRowClick?: (batch: Batch) => void
  className?: string
}

export interface FilterState {
  dateFrom: string
  dateTo: string
  status: '' | 'ACCEPTABLE' | 'WARNING' | 'CRITICAL'
  scoreMin: number
  scoreMax: number
}

export interface PaginationState {
  currentPage: number
  itemsPerPage: number
}

/**
 * Componente BatchTable com filtros e paginação
 * Exibe tabela de batches processados com histórico
 *
 * Colunas: ID, Data Upload, Compliance Score, Risk Level, Status
 * Dados formatados em pt-BR (datas, números)
 * Linhas clicáveis para detalhes
 */
export const BatchTable: React.FC<BatchTableProps> = ({ batches, onRowClick, className = '' }) => {
  const [filters, setFilters] = useState<FilterState>({
    dateFrom: '',
    dateTo: '',
    status: '',
    scoreMin: 0,
    scoreMax: 100,
  })

  const [pagination, setPagination] = useState<PaginationState>({
    currentPage: 1,
    itemsPerPage: 10,
  })

  // Aplicar filtros
  const filteredBatches = useMemo(() => {
    return batches.filter((batch) => {
      // Filtro por data
      if (filters.dateFrom) {
        const batchDate = new Date(batch.upload_date)
        const fromDate = new Date(filters.dateFrom)
        if (batchDate < fromDate) return false
      }

      if (filters.dateTo) {
        const batchDate = new Date(batch.upload_date)
        const toDate = new Date(filters.dateTo)
        toDate.setHours(23, 59, 59, 999) // Incluir todo o dia
        if (batchDate > toDate) return false
      }

      // Filtro por status
      if (filters.status && batch.status !== filters.status) {
        return false
      }

      // Filtro por score
      if (batch.compliance_score < filters.scoreMin || batch.compliance_score > filters.scoreMax) {
        return false
      }

      return true
    })
  }, [batches, filters])

  // Aplicar paginação
  const paginatedBatches = useMemo(() => {
    const startIndex = (pagination.currentPage - 1) * pagination.itemsPerPage
    const endIndex = startIndex + pagination.itemsPerPage
    return filteredBatches.slice(startIndex, endIndex)
  }, [filteredBatches, pagination])

  const totalPages = Math.ceil(filteredBatches.length / pagination.itemsPerPage)

  // Handlers para filtros
  const handleFilterChange = useCallback(
    (key: keyof FilterState, value: any) => {
      setFilters((prev) => ({ ...prev, [key]: value }))
      setPagination((prev) => ({ ...prev, currentPage: 1 })) // Reset para página 1
    },
    []
  )

  const handleClearFilters = useCallback(() => {
    setFilters({
      dateFrom: '',
      dateTo: '',
      status: '',
      scoreMin: 0,
      scoreMax: 100,
    })
    setPagination((prev) => ({ ...prev, currentPage: 1 }))
  }, [])

  // Handlers para paginação
  const handlePreviousPage = useCallback(() => {
    setPagination((prev) => ({
      ...prev,
      currentPage: Math.max(1, prev.currentPage - 1),
    }))
  }, [])

  const handleNextPage = useCallback(() => {
    setPagination((prev) => ({
      ...prev,
      currentPage: Math.min(totalPages, prev.currentPage + 1),
    }))
  }, [totalPages])

  const handleFirstPage = useCallback(() => {
    setPagination((prev) => ({ ...prev, currentPage: 1 }))
  }, [])

  const handleLastPage = useCallback(() => {
    setPagination((prev) => ({ ...prev, currentPage: totalPages }))
  }, [totalPages])

  // Formatar data para pt-BR
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  }

  // Formatar número para pt-BR
  const formatNumber = (num: number): string => {
    return num.toLocaleString('pt-BR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  }

  // Obter cor do status
  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'ACCEPTABLE':
        return styles.statusAcceptable
      case 'WARNING':
        return styles.statusWarning
      case 'CRITICAL':
        return styles.statusCritical
      default:
        return ''
    }
  }

  // Obter cor do risco
  const getRiskColor = (risk: string): string => {
    switch (risk) {
      case 'LOW RISK':
        return styles.riskLow
      case 'MEDIUM RISK':
        return styles.riskMedium
      case 'HIGH RISK':
        return styles.riskHigh
      default:
        return ''
    }
  }

  return (
    <div className={`${styles.container} ${className}`}>
      {/* Seção de Filtros */}
      <div className={styles.filtersSection}>
        <h3 className={styles.filtersTitle}>Filtros</h3>

        <div className={styles.filtersGrid}>
          {/* Filtro de Data */}
          <div className={styles.filterGroup}>
            <label htmlFor="dateFrom" className={styles.filterLabel}>
              Data Inicial
            </label>
            <input
              id="dateFrom"
              type="date"
              value={filters.dateFrom}
              onChange={(e) => handleFilterChange('dateFrom', e.target.value)}
              className={styles.filterInput}
            />
          </div>

          <div className={styles.filterGroup}>
            <label htmlFor="dateTo" className={styles.filterLabel}>
              Data Final
            </label>
            <input
              id="dateTo"
              type="date"
              value={filters.dateTo}
              onChange={(e) => handleFilterChange('dateTo', e.target.value)}
              className={styles.filterInput}
            />
          </div>

          {/* Filtro de Status */}
          <div className={styles.filterGroup}>
            <label htmlFor="status" className={styles.filterLabel}>
              Status
            </label>
            <select
              id="status"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className={styles.filterInput}
            >
              <option value="">Todos</option>
              <option value="ACCEPTABLE">Aceitável</option>
              <option value="WARNING">Aviso</option>
              <option value="CRITICAL">Crítico</option>
            </select>
          </div>

          {/* Filtro de Score */}
          <div className={styles.filterGroup}>
            <label htmlFor="scoreMin" className={styles.filterLabel}>
              Score Mínimo
            </label>
            <input
              id="scoreMin"
              type="number"
              min="0"
              max="100"
              value={filters.scoreMin}
              onChange={(e) => handleFilterChange('scoreMin', parseInt(e.target.value))}
              className={styles.filterInput}
            />
          </div>

          <div className={styles.filterGroup}>
            <label htmlFor="scoreMax" className={styles.filterLabel}>
              Score Máximo
            </label>
            <input
              id="scoreMax"
              type="number"
              min="0"
              max="100"
              value={filters.scoreMax}
              onChange={(e) => handleFilterChange('scoreMax', parseInt(e.target.value))}
              className={styles.filterInput}
            />
          </div>

          {/* Botão Limpar Filtros */}
          <div className={styles.filterGroup}>
            <button onClick={handleClearFilters} className={styles.clearButton}>
              Limpar Filtros
            </button>
          </div>
        </div>

        {/* Informação de Resultados */}
        <div className={styles.resultsInfo}>
          Mostrando {paginatedBatches.length} de {filteredBatches.length} batches
        </div>
      </div>

      {/* Tabela */}
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>ID do Batch</th>
              <th>Data Upload</th>
              <th>Compliance Score</th>
              <th>Nível de Risco</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {paginatedBatches.length > 0 ? (
              paginatedBatches.map((batch) => (
                <tr
                  key={batch.id}
                  className={styles.tableRow}
                  onClick={() => onRowClick?.(batch)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      onRowClick?.(batch)
                    }
                  }}
                >
                  <td className={styles.cellId}>{batch.id}</td>
                  <td className={styles.cellDate}>{formatDate(batch.upload_date)}</td>
                  <td className={styles.cellScore}>{formatNumber(batch.compliance_score)}</td>
                  <td className={`${styles.cellRisk} ${getRiskColor(batch.risk_level)}`}>
                    {batch.risk_level}
                  </td>
                  <td className={`${styles.cellStatus} ${getStatusColor(batch.status)}`}>
                    {batch.status}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className={styles.emptyMessage}>
                  Nenhum batch encontrado com os filtros aplicados
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Paginação */}
      {filteredBatches.length > 0 && (
        <div className={styles.paginationSection}>
          <div className={styles.paginationButtons}>
            <button
              onClick={handleFirstPage}
              disabled={pagination.currentPage === 1}
              className={styles.paginationButton}
              title="Primeira página"
            >
              ⏮ Primeira
            </button>
            <button
              onClick={handlePreviousPage}
              disabled={pagination.currentPage === 1}
              className={styles.paginationButton}
              title="Página anterior"
            >
              ◀ Anterior
            </button>

            <div className={styles.paginationInfo}>
              Página {pagination.currentPage} de {totalPages}
            </div>

            <button
              onClick={handleNextPage}
              disabled={pagination.currentPage === totalPages}
              className={styles.paginationButton}
              title="Próxima página"
            >
              Próxima ▶
            </button>
            <button
              onClick={handleLastPage}
              disabled={pagination.currentPage === totalPages}
              className={styles.paginationButton}
              title="Última página"
            >
              Última ⏭
            </button>
          </div>

          <div className={styles.itemsPerPageControl}>
            <label htmlFor="itemsPerPage">Items por página:</label>
            <select
              id="itemsPerPage"
              value={pagination.itemsPerPage}
              onChange={(e) =>
                setPagination((prev) => ({
                  ...prev,
                  itemsPerPage: parseInt(e.target.value),
                  currentPage: 1,
                }))
              }
              className={styles.itemsPerPageSelect}
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
            </select>
          </div>
        </div>
      )}
    </div>
  )
}

export default BatchTable
