import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import SensorCharts from './SensorCharts'

describe('SensorCharts', () => {
  const mockData = [
    { index: 0, temperature: 25, ph: 7.0, dissolved_oxygen: 50, pressure: 2.5, agitator_speed: 100 },
    { index: 1, temperature: 26, ph: 7.1, dissolved_oxygen: 52, pressure: 2.6, agitator_speed: 105 },
    { index: 2, temperature: 27, ph: 7.2, dissolved_oxygen: 54, pressure: 2.7, agitator_speed: 110 },
    { index: 3, temperature: 28, ph: 7.1, dissolved_oxygen: 56, pressure: 2.8, agitator_speed: 115 },
    { index: 4, temperature: 29, ph: 7.0, dissolved_oxygen: 58, pressure: 2.9, agitator_speed: 120 },
  ]

  describe('Rendering', () => {
    it('should render the component with title', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Variáveis de Sensores')).toBeInTheDocument()
    })

    it('should render the subtitle', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Monitoramento em tempo real dos 5 sensores principais')).toBeInTheDocument()
    })

    it('should render all 5 chart cards', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByTestId('temperature-chart')).toBeInTheDocument()
      expect(screen.getByTestId('ph-chart')).toBeInTheDocument()
      expect(screen.getByTestId('dissolved-oxygen-chart')).toBeInTheDocument()
      expect(screen.getByTestId('pressure-chart')).toBeInTheDocument()
      expect(screen.getByTestId('agitator-speed-chart')).toBeInTheDocument()
    })
  })

  describe('Temperature Chart', () => {
    it('should render temperature chart title', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Temperatura')).toBeInTheDocument()
    })

    it('should render temperature unit', () => {
      render(<SensorCharts data={mockData} />)
      const temperatureCard = screen.getByTestId('temperature-chart')
      expect(temperatureCard).toHaveTextContent('°C')
    })

    it('should display temperature range', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Range: 20 - 45°C')).toBeInTheDocument()
    })
  })

  describe('pH Chart', () => {
    it('should render pH chart title', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('pH')).toBeInTheDocument()
    })

    it('should display pH range', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Range: 4.0 - 9.0')).toBeInTheDocument()
    })
  })

  describe('Dissolved Oxygen Chart', () => {
    it('should render dissolved oxygen chart title', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Oxigênio Dissolvido')).toBeInTheDocument()
    })

    it('should render dissolved oxygen unit', () => {
      render(<SensorCharts data={mockData} />)
      const doCard = screen.getByTestId('dissolved-oxygen-chart')
      expect(doCard).toHaveTextContent('%')
    })

    it('should display dissolved oxygen range', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Range: 0 - 100%')).toBeInTheDocument()
    })
  })

  describe('Pressure Chart', () => {
    it('should render pressure chart title', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Pressão')).toBeInTheDocument()
    })

    it('should render pressure unit', () => {
      render(<SensorCharts data={mockData} />)
      const pressureCard = screen.getByTestId('pressure-chart')
      expect(pressureCard).toHaveTextContent('bar')
    })

    it('should display pressure range', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Range: 0 - 10 bar')).toBeInTheDocument()
    })
  })

  describe('Agitator Speed Chart', () => {
    it('should render agitator speed chart title', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Velocidade do Agitador')).toBeInTheDocument()
    })

    it('should render agitator speed unit', () => {
      render(<SensorCharts data={mockData} />)
      const agitatorCard = screen.getByTestId('agitator-speed-chart')
      expect(agitatorCard).toHaveTextContent('RPM')
    })

    it('should display agitator speed range', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Range: 0 - 500 RPM')).toBeInTheDocument()
    })
  })

  describe('Legend', () => {
    it('should render legend section', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      expect(container.querySelector('.charts-legend')).toBeInTheDocument()
    })

    it('should display all 5 legend items', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Temperatura (°C)')).toBeInTheDocument()
      expect(screen.getByText('pH')).toBeInTheDocument()
      expect(screen.getByText('Oxigênio Dissolvido (%)')).toBeInTheDocument()
      expect(screen.getByText('Pressão (bar)')).toBeInTheDocument()
      expect(screen.getByText('Velocidade do Agitador (RPM)')).toBeInTheDocument()
    })
  })

  describe('Data Handling', () => {
    it('should render with provided data', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByTestId('temperature-chart')).toBeInTheDocument()
    })

    it('should render with empty data array', () => {
      render(<SensorCharts data={[]} />)
      expect(screen.getByText('Variáveis de Sensores')).toBeInTheDocument()
    })

    it('should render with default data when no data provided', () => {
      render(<SensorCharts data={[]} />)
      expect(screen.getByTestId('temperature-chart')).toBeInTheDocument()
    })

    it('should handle single data point', () => {
      const singleData = [
        { index: 0, temperature: 25, ph: 7.0, dissolved_oxygen: 50, pressure: 2.5, agitator_speed: 100 }
      ]
      render(<SensorCharts data={singleData} />)
      expect(screen.getByTestId('temperature-chart')).toBeInTheDocument()
    })

    it('should handle large dataset', () => {
      const largeData = Array.from({ length: 100 }, (_, i) => ({
        index: i,
        temperature: 25 + Math.random() * 5,
        ph: 7.0 + Math.random() * 0.5,
        dissolved_oxygen: 50 + Math.random() * 10,
        pressure: 2.5 + Math.random() * 0.5,
        agitator_speed: 100 + Math.random() * 20
      }))
      render(<SensorCharts data={largeData} />)
      expect(screen.getByTestId('temperature-chart')).toBeInTheDocument()
    })
  })

  describe('Props', () => {
    it('should accept custom className', () => {
      const { container } = render(
        <SensorCharts data={mockData} className="custom-class" />
      )
      expect(container.querySelector('.sensor-charts-container')).toHaveClass('custom-class')
    })

    it('should render with default className when not provided', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      expect(container.querySelector('.sensor-charts-container')).toBeInTheDocument()
    })
  })

  describe('Visual Elements', () => {
    it('should render chart containers', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const chartContainers = container.querySelectorAll('.chart-container')
      expect(chartContainers.length).toBeGreaterThan(0)
    })

    it('should render chart info sections', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const chartInfos = container.querySelectorAll('.chart-info')
      expect(chartInfos.length).toBeGreaterThan(0)
    })

    it('should render legend color indicators', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendColors = container.querySelectorAll('.legend-color')
      expect(legendColors.length).toBe(5)
    })
  })

  describe('Accessibility', () => {
    it('should have proper heading hierarchy', () => {
      render(<SensorCharts data={mockData} />)
      const title = screen.getByText('Variáveis de Sensores')
      expect(title.tagName).toBe('H2')
    })

    it('should have descriptive chart titles', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Temperatura')).toBeInTheDocument()
      expect(screen.getByText('pH')).toBeInTheDocument()
      expect(screen.getByText('Oxigênio Dissolvido')).toBeInTheDocument()
      expect(screen.getByText('Pressão')).toBeInTheDocument()
      expect(screen.getByText('Velocidade do Agitador')).toBeInTheDocument()
    })

    it('should display range information for each sensor', () => {
      render(<SensorCharts data={mockData} />)
      expect(screen.getByText('Range: 20 - 45°C')).toBeInTheDocument()
      expect(screen.getByText('Range: 4.0 - 9.0')).toBeInTheDocument()
      expect(screen.getByText('Range: 0 - 100%')).toBeInTheDocument()
      expect(screen.getByText('Range: 0 - 10 bar')).toBeInTheDocument()
      expect(screen.getByText('Range: 0 - 500 RPM')).toBeInTheDocument()
    })
  })

  describe('Responsive Design', () => {
    it('should render charts grid', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      expect(container.querySelector('.charts-grid')).toBeInTheDocument()
    })

    it('should render all chart cards in grid', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const chartCards = container.querySelectorAll('.chart-card')
      expect(chartCards.length).toBe(5)
    })

    it('should have responsive grid layout', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const grid = container.querySelector('.charts-grid')
      expect(grid).toHaveClass('charts-grid')
    })
  })

  describe('Color Coding', () => {
    it('should have distinct colors for each sensor', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendColors = container.querySelectorAll('.legend-color')
      
      // Check that colors are set
      legendColors.forEach(color => {
        expect(color).toHaveStyle({ backgroundColor: expect.any(String) })
      })
    })

    it('should use red for temperature', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendItems = container.querySelectorAll('.legend-item')
      const tempItem = Array.from(legendItems).find(item => 
        item.textContent?.includes('Temperatura')
      )
      expect(tempItem?.querySelector('.legend-color')).toHaveStyle({ backgroundColor: '#ef4444' })
    })

    it('should use purple for pH', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendItems = container.querySelectorAll('.legend-item')
      const phItem = Array.from(legendItems).find(item => 
        item.textContent?.includes('pH')
      )
      expect(phItem?.querySelector('.legend-color')).toHaveStyle({ backgroundColor: '#8b5cf6' })
    })

    it('should use cyan for dissolved oxygen', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendItems = container.querySelectorAll('.legend-item')
      const doItem = Array.from(legendItems).find(item => 
        item.textContent?.includes('Oxigênio Dissolvido')
      )
      expect(doItem?.querySelector('.legend-color')).toHaveStyle({ backgroundColor: '#06b6d4' })
    })

    it('should use amber for pressure', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendItems = container.querySelectorAll('.legend-item')
      const pressureItem = Array.from(legendItems).find(item => 
        item.textContent?.includes('Pressão')
      )
      expect(pressureItem?.querySelector('.legend-color')).toHaveStyle({ backgroundColor: '#f59e0b' })
    })

    it('should use green for agitator speed', () => {
      const { container } = render(<SensorCharts data={mockData} />)
      const legendItems = container.querySelectorAll('.legend-item')
      const agitatorItem = Array.from(legendItems).find(item => 
        item.textContent?.includes('Velocidade do Agitador')
      )
      expect(agitatorItem?.querySelector('.legend-color')).toHaveStyle({ backgroundColor: '#10b981' })
    })
  })
})
