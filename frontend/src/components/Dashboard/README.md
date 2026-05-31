# Dashboard Component

## Descrição

Componente React principal que consolida todos os elementos do dashboard unificado em uma única tela. Exibe indicadores de qualidade (Compliance Score), predição de risco (ML), gráficos de 5 sensores e tabela de histórico de batches com filtros e paginação.

## Características

- ✅ **Compliance Score Card** - Score 0-100 com classificação (ACCEPTABLE/WARNING/CRITICAL)
- ✅ **Risk Prediction Card** - Predição de risco (LOW/MEDIUM/HIGH) com confidence score
- ✅ **Sensor Charts** - Visualização de 5 variáveis de sensores:
  - Temperature (°C)
  - pH
  - Dissolved Oxygen (%)
  - Pressure (bar)
  - Agitator Speed (RPM)
- ✅ **Batch History Table** - Tabela com histórico de batches processados
- ✅ **Filtros** - Filtrar por status, score range e período
- ✅ **Paginação** - Navegação entre páginas (10 itens por página)
- ✅ **Layout Responsivo** - Mobile, tablet e desktop
- ✅ **TypeScript** - Tipagem completa
- ✅ **Real-time Updates** - Atualização automática de dados (30s por padrão)
- ✅ **Disclaimer** - Aviso obrigatório sobre análises

## Props

```typescript
interface DashboardProps {
  refreshInterval?: number // Intervalo de atualização em ms (padrão: 30000)
}
```

## Uso

```tsx
import { Dashboard } from '@/components/Dashboard'

export default function App() {
  return <Dashboard refreshInterval={30000} />
}
```

## Estrutura de Dados

### Batch
```typescript
interface Batch {
  id: string
  upload_date: string
  compliance_score: number
  risk_prediction: string
  confidence_score: number
  status: string
}
```

### Sensor Data
```typescript
interface SensorData {
  temperature: number
  ph: number
  dissolved_oxygen: number
  pressure: number
  agitator_speed: number
}
```

## API Endpoints Utilizados

- `GET /api/v1/batches` - Lista todos os batches
- `GET /api/v1/compliance/{batch_id}` - Compliance score do batch
- `GET /api/v1/prediction/{batch_id}` - Predição de risco do batch

## Estilos

O componente utiliza **TailwindCSS** através de CSS Modules (`Dashboard.module.css`).

### Breakpoints Responsivos

- **Mobile**: < 768px (1 coluna)
- **Tablet**: 768px - 1023px (2 colunas)
- **Desktop**: ≥ 1024px (5 colunas para sensores)

## Funcionalidades

### Compliance Score
- Score 0-100 com cor indicativa
- Classificação automática:
  - 80-100: ACCEPTABLE (verde)
  - 60-79: WARNING (amarelo)
  - 0-59: CRITICAL (vermelho)

### Risk Prediction
- Predição: LOW RISK, MEDIUM RISK, HIGH RISK
- Confidence score em percentual
- Cores indicativas por nível de risco

### Sensor Charts
- Visualização de 5 sensores com ranges esperados
- Barra de progresso com cor indicativa
- Validação automática de ranges

### Batch Table
- Listagem de batches com paginação
- Filtros por status, score range e período
- Formatação de datas em pt-BR
- Badges coloridas para status e predição

### Filtros
- **Status**: Todos, Concluído, Processando, Falha
- **Score Range**: Todos, Aceitável, Aviso, Crítico
- **Período**: Todos, Hoje, Última Semana, Último Mês

### Paginação
- 10 itens por página
- Botões Anterior/Próxima
- Indicador de página atual

## Tratamento de Erros

- Mensagem de erro com botão "Tentar Novamente"
- Loading state durante carregamento
- Empty state quando nenhum batch encontrado
- Timeout de 30s para requisições

## Acessibilidade

- Labels associados aos inputs
- Atributos ARIA apropriados
- Navegação por teclado
- Contraste de cores adequado

## Performance

- Atualização automática configurável
- Paginação para evitar renderização de muitos itens
- Memoização de componentes (quando necessário)
- CSS otimizado com media queries

## Conformidade

- ✅ Disclaimer obrigatório incluído
- ✅ Sem dados sensíveis expostos
- ✅ Rastreabilidade de origem dos dados
- ✅ Validação de ranges de sensores

## Próximas Melhorias

- [ ] Integração com Recharts para gráficos avançados
- [ ] Exportação de dados em CSV
- [ ] Alertas em tempo real
- [ ] Análise de tendências
- [ ] Comparação entre batches
