# Componentes React - BiotecPredict

Documentação da estrutura de componentes React seguindo o Design System da aplicação.

---

## 📦 Componentes Implementados

### 1. Layout Estrutural

#### `Layout.tsx`
**Propósito:** Wrapper da aplicação com navegação e estrutura base

**Responsabilidades:**
- Header com logo e título
- Navigation (futuro: menu de navegação)
- Footer (futuro)
- Espaçamento consistente

**Localização:** `src/components/Layout/`

---

#### `Navigation.tsx`
**Propósito:** Navegação entre telas

**Recursos:**
- Links para Tela 1 (Upload) e Tela 2 (Dashboard)
- Indicador de página ativa
- Responsivo em mobile

**Localização:** `src/components/Layout/`

---

### 2. Componentes de Interface (UI)

#### `UploadCard.tsx`
**Propósito:** Card com interface de upload de arquivo CSV

**Características:**
- Drag-and-drop
- Click to browse
- Validação de arquivo (.csv, max 10MB)
- Loading state
- Success/error feedback
- Acessível (ARIA labels)

**Props:**
```tsx
interface UploadCardProps {
  onUploadSuccess?: (batchId: string) => void;
  onUploadError?: (error: string) => void;
}
```

**Arquivo:** `src/components/UploadCard/UploadCard.tsx`

---

#### `ComplianceScoreCard.tsx`
**Propósito:** Exibir Manufacturing Compliance Score (0-100)

**Características:**
- Score em número grande e colorido
- Classificação automática (ACCEPTABLE/WARNING/CRITICAL)
- Cores semânticas (verde/amarelo/vermelho)
- Ícone indicativo
- Responsivo

**Props:**
```tsx
interface ComplianceScoreCardProps {
  score: number;      // 0-100
  batchId: string;
  loading?: boolean;
  error?: string;
}
```

**Localização:** `src/components/ComplianceScoreCard/`

**Design System:**
- Card base (background branco, border, shadow)
- Cores: `#28A745` (verde) / `#FFC107` (amarelo) / `#DC3545` (vermelho)
- Typography: H1 para score (32px, bold), Small para label

---

#### `RiskPredictionCard.tsx`
**Propósito:** Exibir predição de risco ML (LOW/MEDIUM/HIGH)

**Características:**
- Status do risco (LOW RISK / MEDIUM RISK / HIGH RISK)
- Confidence score em percentual
- Cores por nível de risco
- Ícone de perigo/sucesso
- Badge de confiança

**Props:**
```tsx
interface RiskPredictionCardProps {
  prediction: 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK';
  confidence: number;  // 0-1 (percentual)
  batchId: string;
  loading?: boolean;
}
```

**Localização:** `src/components/RiskPredictionCard/`

**Design System:**
- Card base
- Cores: `#28A745` (LOW) / `#FFC107` (MEDIUM) / `#DC3545` (HIGH)
- Confidence em badge com fundo semi-transparente

---

### 3. Visualizações de Dados

#### `SensorCharts.tsx`
**Propósito:** Exibir 5 sensores em gráficos/barras

**Sensores Monitorados:**
1. Temperature (°C)
2. pH
3. Dissolved Oxygen (%)
4. Pressure (bar)
5. Agitator Speed (RPM)

**Características:**
- Barras de progresso coloridas
- Indicador de range esperado
- Cores: verde (dentro), amarelo (margem), vermelho (fora)
- Responsivo (5 colunas desktop, 2 tablet, 1 mobile)
- Valores em unidades corretas

**Props:**
```tsx
interface SensorChartsProps {
  sensors: {
    temperature: number;
    ph: number;
    dissolved_oxygen: number;
    pressure: number;
    agitator_speed: number;
  };
  loading?: boolean;
}
```

**Localização:** `src/components/SensorCharts/`

**Design System:**
- Cards individuais para cada sensor
- Ícones representativos
- Escala de cores: verde (80-100%) → amarelo (60-79%) → vermelho (0-59%)

---

#### `BatchTable.tsx`
**Propósito:** Tabela com histórico de batches processados

**Características:**
- Listagem de todos os batches
- **Filtros:** status, score range, período
- **Paginação:** 10 itens por página
- **Badges:** coloridas por status
- Ordenação (futuro)
- Responsivo (scroll horizontal em mobile)

**Colunas:**
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ID | string | Identificador do batch |
| Upload Date | datetime | Data/hora do upload |
| Compliance Score | number | Score 0-100 |
| Classification | badge | ACCEPTABLE/WARNING/CRITICAL |
| Risk Prediction | badge | LOW/MEDIUM/HIGH |

**Props:**
```tsx
interface BatchTableProps {
  batches: Batch[];
  onBatchSelect?: (batchId: string) => void;
  loading?: boolean;
  filters?: FilterOptions;
}

interface Batch {
  id: string;
  upload_date: string;
  compliance_score: number;
  classification: 'ACCEPTABLE' | 'WARNING' | 'CRITICAL';
  risk_prediction: 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK';
}
```

**Localização:** `src/components/BatchTable/`

**Design System:**
- Table base com borders
- Header com fundo cinza
- Hover effect em linhas
- Badges com cores semânticas
- Responsivo com overflow

---

### 4. Componentes de Layout de Página

#### `Dashboard.tsx` (Componente)
**Propósito:** Tela 2 consolidada - Agrupa as 4 seções de análises

**Estrutura (4 Seções):**

```
┌─────────────────────────────────────────┐
│ 1. INDICADORES DE DADOS                 │
│    ├─ Sensor 1: Temperature             │
│    ├─ Sensor 2: pH                      │
│    ├─ Sensor 3: Dissolved Oxygen        │
│    ├─ Sensor 4: Pressure                │
│    └─ Sensor 5: Agitator Speed          │
├─────────────────────────────────────────┤
│ 2. ANÁLISE DE COMPLIANCE                │
│    └─ ComplianceScoreCard (0-100)       │
│ + 3. ANÁLISE PREDITIVA (ML)             │
│    └─ RiskPredictionCard (LOW/MED/HIGH) │
├─────────────────────────────────────────┤
│ 4. HISTÓRICO DE BATCHES                 │
│    └─ BatchTable com filtros            │
└─────────────────────────────────────────┘
```

**Layout Responsivo:**
- **Desktop (≥1024px):** Grid 2 colunas (Cards) + 5 colunas (Sensores) + Full (Tabela)
- **Tablet (768-1023px):** Grid 2 colunas com wrapping
- **Mobile (<768px):** Flex column, full width

**Características:**
- Auto-refresh a cada 30 segundos
- Disclaimer obrigatório
- Loading states
- Error handling
- API integration

**Props:**
```tsx
interface DashboardProps {
  refreshInterval?: number; // ms, default 30000
}
```

**Localização:** `src/components/Dashboard/`

---

#### `Upload.tsx` (Página)
**Propósito:** Tela 1 - Upload de arquivo CSV

**Estrutura:**
```
┌─────────────────────────────┐
│ H1: Upload de Arquivo CSV   │
│                             │
│ P: Descrição                │
│                             │
│ ┌───────────────────────┐   │
│ │   UploadCard          │   │
│ │ (drag-and-drop area)  │   │
│ └───────────────────────┘   │
└─────────────────────────────┘
```

**Características:**
- Heading descritivo
- Help text
- Componente UploadCard integrado
- Responsivo

**Localização:** `src/pages/Upload/`

---

#### `Dashboard.tsx` (Página)
**Propósito:** Tela 2 - Dashboard com análises

**Estrutura:**
```
┌──────────────────────────┐
│ H1: Dashboard Analítico  │
│                          │
│ ┌────────────────────┐   │
│ │ Dashboard Component │   │
│ └────────────────────┘   │
└──────────────────────────┘
```

**Localização:** `src/pages/Dashboard/`

---

## 🎨 Design System Mapping

### Cores por Componente

| Componente | Cor Primária | Cor Secundária | Cor de Sucesso | Cor de Aviso | Cor de Erro |
|-----------|-------------|----------------|----------------|-------------|-----------|
| Botões | #0052CC | #003a99 | - | - | #DC3545 |
| ComplianceScore | - | - | #28A745 | #FFC107 | #DC3545 |
| RiskPrediction | - | - | #28A745 | #FFC107 | #DC3545 |
| SensorCharts | - | - | #28A745 | #FFC107 | #DC3545 |
| Badges | - | - | #28A745 | #FFC107 | #DC3545 |

### Tipografia por Componente

| Componente | H1 | H2 | H3 | Body | Small |
|-----------|----|----|----|----|--------|
| Dashboard | 32px/700 | 24px/700 | 20px/600 | 16px/400 | 14px/500 |
| Cards | - | - | 20px/600 | 16px/400 | 14px/500 |
| Table | - | - | 14px/600 | 14px/400 | 12px/400 |

### Espaçamento

- **Dentro de componentes:** 16px (space-md)
- **Entre componentes:** 24px (space-lg)
- **Entre seções:** 48px (space-2xl)

---

## 📱 Responsividade por Componente

### UploadCard
- Mobile: Full width, 16px padding
- Tablet: Max 600px width, centered
- Desktop: Max 700px width, centered

### Dashboard
- Mobile: Single column, 16px gap
- Tablet: 2 columns, 24px gap
- Desktop: 5 columns sensores + 2 cols compliance/risk + full width table

### BatchTable
- Mobile: Horizontal scroll
- Tablet: Ajusta font size
- Desktop: Full responsive

---

## ♿ Acessibilidade Implementada

**Todos os componentes incluem:**
- [ ] `htmlFor` em labels
- [ ] `aria-label` ou `aria-labelledby` em ícones
- [ ] `aria-describedby` em inputs
- [ ] `role` apropriado em componentes customizados
- [ ] Navegação por teclado
- [ ] Focus visible states
- [ ] Contrast ratio 4.5:1 para textos
- [ ] Semantic HTML

---

## 🧪 Testes

**Cada componente inclui:**
- `ComponentName.test.tsx` com testes unitários
- Cobertura mínima: 80%
- Testes de:
  - Rendering
  - Props
  - User interactions
  - Loading/error states
  - Accessibility

---

## 📋 Checklist de Novo Componente

Ao criar novo componente, incluir:

- [ ] Arquivo `.tsx` com componente
- [ ] Arquivo `.module.css` com estilos
- [ ] Arquivo `.test.tsx` com testes
- [ ] Arquivo `README.md` documentando:
  - Descrição e propósito
  - Características
  - Props e tipos
  - Exemplos de uso
  - Design System mapping
- [ ] Tipagem TypeScript completa
- [ ] Acessibilidade WCAG AA
- [ ] Responsividade (mobile/tablet/desktop)
- [ ] Estados (normal/hover/active/disabled/loading/error)
- [ ] Documentação em COMPONENTS.md

---

## 🔄 Fluxo de Estado e Props

```
App
├── Upload (Página)
│   └── UploadCard (Componente)
│       └── onUploadSuccess → redireciona para /dashboard
│
└── Dashboard (Página)
    └── Dashboard (Componente)
        ├── SensorCharts
        ├── ComplianceScoreCard
        ├── RiskPredictionCard
        └── BatchTable
            └── onBatchSelect → futura: modal de detalhes
```

---

## 📚 Localizações

```
frontend/src/
├── components/
│   ├── Layout/
│   │   ├── Layout.tsx
│   │   └── Navigation.tsx
│   ├── UploadCard/
│   │   ├── UploadCard.tsx
│   │   ├── UploadCard.module.css
│   │   ├── UploadCard.test.tsx
│   │   └── README.md
│   ├── Dashboard/
│   │   ├── Dashboard.tsx
│   │   ├── Dashboard.module.css
│   │   ├── Dashboard.test.tsx
│   │   └── README.md
│   ├── ComplianceScoreCard/
│   │   ├── ComplianceScoreCard.tsx
│   │   ├── ComplianceScoreCard.module.css
│   │   ├── ComplianceScoreCard.test.tsx
│   │   └── README.md
│   ├── RiskPredictionCard/
│   │   ├── RiskPredictionCard.tsx
│   │   ├── RiskPredictionCard.module.css
│   │   ├── RiskPredictionCard.test.tsx
│   │   └── README.md
│   ├── SensorCharts/
│   │   ├── SensorCharts.tsx
│   │   ├── SensorCharts.module.css
│   │   ├── SensorCharts.test.tsx
│   │   └── README.md
│   └── BatchTable/
│       ├── BatchTable.tsx
│       ├── BatchTable.module.css
│       ├── BatchTable.test.tsx
│       └── README.md
├── pages/
│   ├── Upload/
│   │   ├── Upload.tsx
│   │   └── Upload.module.css
│   └── Dashboard/
│       ├── Dashboard.tsx
│       └── Dashboard.module.css
└── App.tsx
```

---

**Versão:** 1.0.0  
**Data:** 05 de Junho de 2026  
**Status:** ✅ Componentes Documentados
