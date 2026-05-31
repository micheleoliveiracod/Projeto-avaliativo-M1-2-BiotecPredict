import React from 'react'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import './SensorCharts.module.css'

/**
 * SensorCharts Component
 * 
 * Displays 5 sensor data charts using Recharts with responsive design.
 * 
 * Features:
 * - 5 LineCharts for sensor data (Temperature, pH, DO, Pressure, Agitator Speed)
 * - Responsive design (mobile, tablet, desktop)
 * - Color-coded by sensor type
 * - X-axis: time/index, Y-axis: sensor value
 * - Interactive tooltips
 * - Legend for each chart
 * - Proper scaling and ranges
 * 
 * @component
 * @example
 * ```tsx
 * const sensorData = [
 *   { index: 0, temperature: 25, ph: 7.0, dissolved_oxygen: 50, pressure: 2.5, agitator_speed: 100 },
 *   { index: 1, temperature: 26, ph: 7.1, dissolved_oxygen: 52, pressure: 2.6, agitator_speed: 105 },
 * ]
 * <SensorCharts data={sensorData} />
 * ```
 */

interface SensorDataPoint {
  index: number
  temperature: number
  ph: number
  dissolved_oxygen: number
  pressure: number
  agitator_speed: number
}

interface SensorChartsProps {
  data: SensorDataPoint[]
  className?: string
}

const SensorCharts: React.FC<SensorChartsProps> = ({ data, className = '' }) => {
  // Default data if none provided
  const chartData = data && data.length > 0 ? data : [
    { index: 0, temperature: 25, ph: 7.0, dissolved_oxygen: 50, pressure: 2.5, agitator_speed: 100 },
    { index: 1, temperature: 26, ph: 7.1, dissolved_oxygen: 52, pressure: 2.6, agitator_speed: 105 },
    { index: 2, temperature: 27, ph: 7.2, dissolved_oxygen: 54, pressure: 2.7, agitator_speed: 110 },
    { index: 3, temperature: 28, ph: 7.1, dissolved_oxygen: 56, pressure: 2.8, agitator_speed: 115 },
    { index: 4, temperature: 29, ph: 7.0, dissolved_oxygen: 58, pressure: 2.9, agitator_speed: 120 },
  ]

  /**
   * Custom tooltip for charts
   */
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{`Índice: ${payload[0].payload.index}`}</p>
          <p className="tooltip-value" style={{ color: payload[0].color }}>
            {`${payload[0].name}: ${payload[0].value.toFixed(2)}`}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className={`sensor-charts-container ${className}`}>
      <div className="charts-header">
        <h2 className="charts-title">Variáveis de Sensores</h2>
        <p className="charts-subtitle">Monitoramento em tempo real dos 5 sensores principais</p>
      </div>

      <div className="charts-grid">
        {/* Temperature Chart */}
        <div className="chart-card" data-testid="temperature-chart">
          <div className="chart-header">
            <h3 className="chart-title">Temperatura</h3>
            <span className="chart-unit">°C</span>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="index" 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                  domain={[20, 45]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ fontSize: '12px' }}
                  iconType="line"
                />
                <Line
                  type="monotone"
                  dataKey="temperature"
                  stroke="#ef4444"
                  strokeWidth={2}
                  dot={{ fill: '#ef4444', r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Temperatura"
                  isAnimationActive={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-info">
            <p className="info-text">Range: 20 - 45°C</p>
          </div>
        </div>

        {/* pH Chart */}
        <div className="chart-card" data-testid="ph-chart">
          <div className="chart-header">
            <h3 className="chart-title">pH</h3>
            <span className="chart-unit">-</span>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="index" 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                  domain={[4, 9]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ fontSize: '12px' }}
                  iconType="line"
                />
                <Line
                  type="monotone"
                  dataKey="ph"
                  stroke="#8b5cf6"
                  strokeWidth={2}
                  dot={{ fill: '#8b5cf6', r: 4 }}
                  activeDot={{ r: 6 }}
                  name="pH"
                  isAnimationActive={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-info">
            <p className="info-text">Range: 4.0 - 9.0</p>
          </div>
        </div>

        {/* Dissolved Oxygen Chart */}
        <div className="chart-card" data-testid="dissolved-oxygen-chart">
          <div className="chart-header">
            <h3 className="chart-title">Oxigênio Dissolvido</h3>
            <span className="chart-unit">%</span>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="index" 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                  domain={[0, 100]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ fontSize: '12px' }}
                  iconType="line"
                />
                <Area
                  type="monotone"
                  dataKey="dissolved_oxygen"
                  stroke="#06b6d4"
                  fill="#06b6d4"
                  fillOpacity={0.3}
                  name="Oxigênio Dissolvido"
                  isAnimationActive={true}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-info">
            <p className="info-text">Range: 0 - 100%</p>
          </div>
        </div>

        {/* Pressure Chart */}
        <div className="chart-card" data-testid="pressure-chart">
          <div className="chart-header">
            <h3 className="chart-title">Pressão</h3>
            <span className="chart-unit">bar</span>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="index" 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                  domain={[0, 10]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ fontSize: '12px' }}
                  iconType="line"
                />
                <Line
                  type="monotone"
                  dataKey="pressure"
                  stroke="#f59e0b"
                  strokeWidth={2}
                  dot={{ fill: '#f59e0b', r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Pressão"
                  isAnimationActive={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-info">
            <p className="info-text">Range: 0 - 10 bar</p>
          </div>
        </div>

        {/* Agitator Speed Chart */}
        <div className="chart-card" data-testid="agitator-speed-chart">
          <div className="chart-header">
            <h3 className="chart-title">Velocidade do Agitador</h3>
            <span className="chart-unit">RPM</span>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="index" 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  style={{ fontSize: '12px' }}
                  domain={[0, 500]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ fontSize: '12px' }}
                  iconType="line"
                />
                <Area
                  type="monotone"
                  dataKey="agitator_speed"
                  stroke="#10b981"
                  fill="#10b981"
                  fillOpacity={0.3}
                  name="Velocidade do Agitador"
                  isAnimationActive={true}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-info">
            <p className="info-text">Range: 0 - 500 RPM</p>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="charts-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ef4444' }}></span>
          <span className="legend-label">Temperatura (°C)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#8b5cf6' }}></span>
          <span className="legend-label">pH</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#06b6d4' }}></span>
          <span className="legend-label">Oxigênio Dissolvido (%)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#f59e0b' }}></span>
          <span className="legend-label">Pressão (bar)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#10b981' }}></span>
          <span className="legend-label">Velocidade do Agitador (RPM)</span>
        </div>
      </div>
    </div>
  )
}

export default SensorCharts
