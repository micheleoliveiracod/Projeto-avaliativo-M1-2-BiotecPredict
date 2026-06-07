# Dashboard Component - Usage Examples

## Basic Usage

```tsx
import { Dashboard } from '@/components/Dashboard'

export default function DashboardPage() {
  return <Dashboard />
}
```

## With Custom Refresh Interval

```tsx
import { Dashboard } from '@/components/Dashboard'

export default function DashboardPage() {
  // Atualizar a cada 60 segundos
  return <Dashboard refreshInterval={60000} />
}
```

## In a Layout

```tsx
import { Dashboard } from '@/components/Dashboard'
import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'

export default function DashboardLayout() {
  return (
    <div className="app-layout">
      <Header />
      <div className="main-content">
        <Sidebar />
        <main className="content">
          <Dashboard refreshInterval={30000} />
        </main>
      </div>
    </div>
  )
}
```

## With Error Boundary

```tsx
import { Dashboard } from '@/components/Dashboard'
import ErrorBoundary from '@/components/ErrorBoundary'

export default function DashboardPage() {
  return (
    <ErrorBoundary>
      <Dashboard />
    </ErrorBoundary>
  )
}
```

## With Loading Skeleton

```tsx
import { Dashboard } from '@/components/Dashboard'
import { Suspense } from 'react'
import DashboardSkeleton from '@/components/DashboardSkeleton'

export default function DashboardPage() {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <Dashboard />
    </Suspense>
  )
}
```

## Integration with React Router

```tsx
import { Dashboard } from '@/components/Dashboard'
import { useParams } from 'react-router-dom'

export default function DashboardPage() {
  const { batchId } = useParams()

  return (
    <div>
      <h1>Dashboard - Batch {batchId}</h1>
      <Dashboard refreshInterval={30000} />
    </div>
  )
}
```

## With State Management (Redux/Zustand)

```tsx
import { Dashboard } from '@/components/Dashboard'
import { useAppStore } from '@/store'

export default function DashboardPage() {
  const refreshInterval = useAppStore(state => state.dashboardRefreshInterval)

  return <Dashboard refreshInterval={refreshInterval} />
}
```

## Responsive Container

```tsx
import { Dashboard } from '@/components/Dashboard'

export default function DashboardPage() {
  return (
    <div className="dashboard-page">
      <style>{`
        .dashboard-page {
          width: 100%;
          max-width: 1400px;
          margin: 0 auto;
          padding: 1rem;
        }

        @media (max-width: 768px) {
          .dashboard-page {
            padding: 0.5rem;
          }
        }
      `}</style>
      <Dashboard />
    </div>
  )
}
```

## With Custom Styling

```tsx
import { Dashboard } from '@/components/Dashboard'
import styles from './DashboardPage.module.css'

export default function DashboardPage() {
  return (
    <div className={styles.container}>
      <Dashboard />
    </div>
  )
}
```

```css
/* DashboardPage.module.css */
.container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 2rem;
}

.container :global(.dashboard-container) {
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
```

## With Data Refresh Button

```tsx
import { Dashboard } from '@/components/Dashboard'
import { useRef } from 'react'

export default function DashboardPage() {
  const dashboardRef = useRef<HTMLDivElement>(null)

  const handleRefresh = () => {
    // Trigger refresh by remounting component
    window.location.reload()
  }

  return (
    <div>
      <div className="dashboard-controls">
        <button onClick={handleRefresh}>
          🔄 Atualizar Agora
        </button>
      </div>
      <div ref={dashboardRef}>
        <Dashboard refreshInterval={30000} />
      </div>
    </div>
  )
}
```

## With Notifications

```tsx
import { Dashboard } from '@/components/Dashboard'
import { useNotification } from '@/hooks/useNotification'

export default function DashboardPage() {
  const { notify } = useNotification()

  const handleDashboardLoad = () => {
    notify({
      type: 'success',
      message: 'Dashboard carregado com sucesso'
    })
  }

  return (
    <div onLoad={handleDashboardLoad}>
      <Dashboard />
    </div>
  )
}
```

## Full Page Example

```tsx
import { Dashboard } from '@/components/Dashboard'
import { useState } from 'react'

export default function DashboardPage() {
  const [refreshInterval, setRefreshInterval] = useState(30000)

  return (
    <div className="dashboard-page">
      <header className="page-header">
        <h1>Dashboard Unificado</h1>
        <div className="header-controls">
          <label>
            Intervalo de Atualização:
            <select 
              value={refreshInterval} 
              onChange={(e) => setRefreshInterval(Number(e.target.value))}
            >
              <option value={10000}>10 segundos</option>
              <option value={30000}>30 segundos</option>
              <option value={60000}>1 minuto</option>
              <option value={300000}>5 minutos</option>
            </select>
          </label>
        </div>
      </header>

      <main className="page-content">
        <Dashboard refreshInterval={refreshInterval} />
      </main>

      <footer className="page-footer">
        <p>© 2026 BiotecPredict - Plataforma de Manufatura Preditiva</p>
      </footer>
    </div>
  )
}
```

## TypeScript Usage

```tsx
import { Dashboard } from '@/components/Dashboard'
import type { FC } from 'react'

interface DashboardPageProps {
  refreshInterval?: number
  onError?: (error: Error) => void
}

const DashboardPage: FC<DashboardPageProps> = ({ 
  refreshInterval = 30000,
  onError 
}) => {
  return (
    <div>
      <Dashboard refreshInterval={refreshInterval} />
    </div>
  )
}

export default DashboardPage
```

## Testing Usage

```tsx
import { render, screen, waitFor } from '@testing-library/react'
import { Dashboard } from '@/components/Dashboard'

describe('Dashboard Integration', () => {
  it('should render dashboard in page', async () => {
    render(<Dashboard />)

    await waitFor(() => {
      expect(screen.getByText('Dashboard Unificado')).toBeInTheDocument()
    })
  })

  it('should accept custom refresh interval', async () => {
    render(<Dashboard refreshInterval={60000} />)

    await waitFor(() => {
      expect(screen.getByText('Dashboard Unificado')).toBeInTheDocument()
    })
  })
})
```

## Notes

- O componente gerencia seu próprio estado de dados
- Atualização automática configurável via `refreshInterval`
- Sem dependências externas (apenas React)
- Totalmente responsivo
- TypeScript completo
- Acessível (WCAG)
- Pronto para produção
