# Design System - BiotecPredict

## Visão Geral

Sistema de design documentado para manter consistência visual e funcional em toda a plataforma BiotecPredict. Define padrões para cores, tipografia, componentes, layouts e acessibilidade.

---

## 🎨 Paleta de Cores

### Cores Principais

| Cor | Hex | RGB | Uso |
|-----|-----|-----|-----|
| **Azul Primário** | #0052CC | rgb(0, 82, 204) | Botões, links, destaques |
| **Verde Sucesso** | #28A745 | rgb(40, 167, 69) | Status OK, ACCEPTABLE, LOW RISK |
| **Amarelo Aviso** | #FFC107 | rgb(255, 193, 7) | Status WARNING, MEDIUM RISK |
| **Vermelho Erro** | #DC3545 | rgb(220, 53, 69) | Status CRITICAL, HIGH RISK, erros |
| **Cinza Escuro** | #2C3E50 | rgb(44, 62, 80) | Texto principal, backgrounds |
| **Cinza Claro** | #ECF0F1 | rgb(236, 240, 241) | Backgrounds secundários |
| **Branco** | #FFFFFF | rgb(255, 255, 255) | Backgrounds principais |

### Cores Semânticas

#### Manufacturing Compliance Score
```css
/* Score Bands */
--color-acceptable: #28A745  /* 80-100 - Verde */
--color-warning: #FFC107     /* 60-79 - Amarelo */
--color-critical: #DC3545    /* 0-59 - Vermelho */
```

#### Risk Prediction
```css
--color-low-risk: #28A745    /* LOW RISK - Verde */
--color-medium-risk: #FFC107 /* MEDIUM RISK - Amarelo */
--color-high-risk: #DC3545   /* HIGH RISK - Vermelho */
```

#### Sensor Values
```css
--color-within-spec: #17A2B8    /* Dentro da especificação */
--color-out-of-spec: #FFC107    /* Fora da especificação */
--color-critical-spec: #DC3545  /* Crítico/Fora dos limites */
```

### Gradientes

**Gradiente Primário (Botões CTA):**
```css
background: linear-gradient(135deg, #0052CC 0%, #003a99 100%);
```

**Gradiente de Status:**
```css
/* Success */
background: linear-gradient(135deg, #28A745 0%, #1e7e34 100%);

/* Warning */
background: linear-gradient(135deg, #FFC107 0%, #e0a800 100%);

/* Critical */
background: linear-gradient(135deg, #DC3545 0%, #c82333 100%);
```

---

## 📝 Tipografia

### Famílias de Fontes

**Fonte Principal (UI):**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
             'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
             'Helvetica Neue', sans-serif;
```

**Fonte Monospace (Código/Dados):**
```css
font-family: 'Courier New', 'Courier', 'Monaco', monospace;
```

### Escala Tipográfica

| Uso | Tamanho | Peso | Line Height | Exemplo |
|-----|---------|------|-------------|---------|
| **H1** (Títulos Página) | 32px | 700 | 1.2 | BiotecPredict |
| **H2** (Seções) | 24px | 700 | 1.3 | Análise de Compliance |
| **H3** (Subtítulos) | 20px | 600 | 1.3 | Dados dos Sensores |
| **Body** (Texto Normal) | 16px | 400 | 1.5 | Lorem ipsum... |
| **Small** (Rótulos) | 14px | 500 | 1.4 | Label text |
| **XSmall** (Helpe r Text) | 12px | 400 | 1.4 | Description text |

### Estilos de Texto

**Destaque Primário:**
```css
font-size: 16px;
font-weight: 600;
color: #0052CC;
text-decoration: none;
```

**Texto Desabilitado:**
```css
color: #95A5A6;
opacity: 0.6;
cursor: not-allowed;
```

---

## 📦 Componentes Reutilizáveis

### 1. Card (Cartão de Informação)

**Uso:** Agrupar informações relacionadas

**Propriedades:**
```css
background: #FFFFFF;
border: 1px solid #E8E8E8;
border-radius: 8px;
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
padding: 20px;
```

**Componentes que usam:**
- `ComplianceScoreCard`
- `RiskPredictionCard`
- `SensorCharts`

---

### 2. Botões

**Botão Primário (CTA - Call to Action):**
```css
background: linear-gradient(135deg, #0052CC 0%, #003a99 100%);
color: #FFFFFF;
padding: 12px 24px;
border-radius: 6px;
font-weight: 600;
font-size: 16px;
border: none;
cursor: pointer;
transition: all 0.3s ease;
```

**Botão Secundário:**
```css
background: #F5F5F5;
color: #2C3E50;
padding: 12px 24px;
border-radius: 6px;
border: 1px solid #D0D0D0;
font-weight: 600;
```

**Botão Perigoso (Destructive):**
```css
background: #DC3545;
color: #FFFFFF;
padding: 12px 24px;
border-radius: 6px;
font-weight: 600;
```

---

### 3. Inputs e Forms

**Campo de Entrada (Input):**
```css
border: 1px solid #D0D0D0;
border-radius: 6px;
padding: 10px 12px;
font-size: 16px;
font-family: inherit;
transition: border-color 0.3s ease;
```

**Input Focus:**
```css
border-color: #0052CC;
box-shadow: 0 0 0 3px rgba(0, 82, 204, 0.1);
outline: none;
```

**Input Error:**
```css
border-color: #DC3545;
background: rgba(220, 53, 69, 0.05);
```

---

### 4. Badges (Tags de Status)

**Badge Sucesso:**
```css
background: rgba(40, 167, 69, 0.15);
color: #155724;
padding: 4px 12px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;
```

**Badge Aviso:**
```css
background: rgba(255, 193, 7, 0.15);
color: #856404;
padding: 4px 12px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;
```

**Badge Crítico:**
```css
background: rgba(220, 53, 69, 0.15);
color: #721c24;
padding: 4px 12px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;
```

---

### 5. Tabelas

**Estrutura Base:**
```css
/* Header */
thead {
  background: #F5F5F5;
  font-weight: 600;
  border-bottom: 2px solid #D0D0D0;
}

/* Células */
td {
  padding: 12px;
  border-bottom: 1px solid #E8E8E8;
}

/* Hover (Linhas)*/
tbody tr:hover {
  background: #F9F9F9;
}
```

---

## 🏗️ Grid e Layouts

### Breakpoints (Responsive Design)

```css
/* Mobile First */
$mobile: 0px;          /* Padrão */
$tablet: 768px;        /* md */
$desktop: 1024px;      /* lg */
$wide: 1280px;         /* xl */
$ultra-wide: 1536px;   /* 2xl */
```

### Componente de Grid

**Layout de Tela 2 (Dashboard):**

```
Desktop (≥ 1024px):
┌─────────────────────────────────────────────┐
│  Compliance Score    │  Risk Prediction      │
├──────────────────────────────────────────────┤
│            Sensor Charts (5 colunas)        │
├──────────────────────────────────────────────┤
│        Batch Table (com filtros)            │
└──────────────────────────────────────────────┘

Tablet (768px - 1023px):
┌────────────────────────┐
│ Compliance │ Risk       │
├────────────────────────┤
│ Sensor 1 │ Sensor 2    │
├──────────────────────────┤
│ Sensor 3 │ Sensor 4    │
├────────────────────────┤
│   Sensor 5 (full)      │
├────────────────────────┤
│  Batch Table           │
└────────────────────────┘

Mobile (< 768px):
┌────────────────┐
│ Compliance     │
├────────────────┤
│ Risk Pred.     │
├────────────────┤
│ Sensor Charts  │
│  (empilhados)  │
├────────────────┤
│ Batch Table    │
│ (horizontal)   │
└────────────────┘
```

### Container Max Width

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px; /* Mobile padding */
}

@media (min-width: 768px) {
  .container {
    padding: 0 24px;
  }
}
```

---

## ♿ Acessibilidade

### WCAG 2.1 AA Compliance

**Contraste de Cores:**
- Texto sobre background: mínimo 4.5:1
- Componentes UI: mínimo 3:1
- Todos os textos em verde devem ter apenas 4.5:1 (exceção permitida)

### Uso de Cores

❌ **Não fazer:**
```css
/* Não use APENAS cor para indicar status */
.status { color: #28A745; }
```

✅ **Fazer:**
```css
.status-success {
  color: #28A745;
  display: flex;
  align-items: center;
}

.status-success::before {
  content: '✓';
  margin-right: 8px;
}
```

### Labels e ARIA

**Exemplo Correto:**
```tsx
<label htmlFor="compliance-filter">Filtrar por Status:</label>
<select id="compliance-filter" aria-describedby="filter-help">
  <option value="">Todos</option>
  <option value="acceptable">ACCEPTABLE</option>
  <option value="warning">WARNING</option>
  <option value="critical">CRITICAL</option>
</select>
<p id="filter-help" className="help-text">
  Selecione um status para filtrar o dashboard
</p>
```

### Navegação por Teclado

- Tab: navegar entre elementos
- Shift + Tab: navegar ao contrário
- Enter/Space: ativar botões
- Setas: navegar em menus/seleções

---

## 🎯 Espaçamento (Spacing Scale)

```css
/* Múltiplos de 4px (sistema de 4px) */
$space-xs: 4px;      /* Micro espaçamentos */
$space-sm: 8px;      /* Small gaps */
$space-md: 16px;     /* Normal gaps */
$space-lg: 24px;     /* Large gaps */
$space-xl: 32px;     /* Extra large */
$space-2xl: 48px;    /* Component separation */
$space-3xl: 64px;    /* Section separation */
```

**Regra de Ouro:**
- Espaço dentro de componente: `space-md` (16px)
- Espaço entre componentes: `space-lg` (24px)
- Espaço entre seções: `space-2xl` (48px)

---

## 🔲 Bordas e Raios

```css
/* Borda padrão */
$border-light: 1px solid #E8E8E8;
$border-normal: 1px solid #D0D0D0;
$border-dark: 1px solid #999999;

/* Raios de borda */
$radius-sm: 4px;     /* Inputs, pequenos componentes */
$radius-md: 6px;     /* Cards, botões */
$radius-lg: 8px;     /* Containers maiores */
$radius-full: 9999px; /* Circles, avatars */
```

---

## 🌑 Dark Mode (Futuro)

Preparado para futuro suporte a Dark Mode:

```css
/* CSS Variables para fácil alternância */
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F5F5F5;
  --text-primary: #2C3E50;
  --text-secondary: #666666;
  --border-color: #E8E8E8;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1E1E1E;
    --bg-secondary: #2D2D2D;
    --text-primary: #FFFFFF;
    --text-secondary: #CCCCCC;
    --border-color: #444444;
  }
}
```

---

## 📐 Sombras

```css
/* Elevar componentes sutilmente */
$shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
$shadow-md: 0 4px 8px rgba(0, 0, 0, 0.12);
$shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);
$shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.18);

/* Foco interativo */
$shadow-focus: 0 0 0 3px rgba(0, 82, 204, 0.1);
```

---

## ⏱️ Animações e Transições

**Padrão:**
```css
/* Transições padrão */
transition: all 0.3s ease;

/* Especific transitions */
transition: background-color 0.2s ease,
            border-color 0.2s ease;

/* Durations */
$duration-fast: 0.15s;    /* Hover, focus */
$duration-normal: 0.3s;   /* Modal, transitions */
$duration-slow: 0.5s;     /* Page transitions */
```

**Timing Functions:**
```css
ease-in: cubic-bezier(0.42, 0, 1, 1);
ease-out: cubic-bezier(0, 0, 0.58, 1);
ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);
```

---

## 🎭 Estados de Componentes

### Estados Interativos

```
Normal → Hover → Active → Disabled
```

**Exemplo (Botão):**
```css
/* Normal */
button {
  background: #0052CC;
  color: #FFFFFF;
}

/* Hover */
button:hover {
  background: #003a99;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 82, 204, 0.3);
}

/* Active */
button:active {
  background: #002966;
  transform: translateY(0);
}

/* Disabled */
button:disabled {
  background: #CCCCCC;
  color: #999999;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Focus (Keyboard) */
button:focus-visible {
  outline: 2px solid #0052CC;
  outline-offset: 2px;
}
```

---

## 📱 Responsividade

### Estratégia Mobile-First

```css
/* Base: Mobile (0px) */
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .dashboard {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .dashboard {
    grid-template-columns: repeat(5, 1fr);
  }
}
```

---

## 🔍 Ícones

**Font: Material Icons ou Feather Icons**

```html
<!-- Material Icons -->
<i class="material-icons">upload_file</i>
<i class="material-icons">dashboard</i>
<i class="material-icons">warning</i>
<i class="material-icons">check_circle</i>
<i class="material-icons">error</i>
```

**Tamanhos Padrão:**
- Small: 16px (Labels)
- Normal: 24px (Buttons, list items)
- Large: 32px (Page headings)
- XLarge: 48px (Section icons)

---

## 🧪 Testes de Design

**Checklist ao implementar novo componente:**

- [ ] Contraste de cores WCAG AA compliant
- [ ] Estados (normal, hover, active, disabled, focus)
- [ ] Responsivo (mobile, tablet, desktop)
- [ ] Acessível (labels, ARIA, teclado)
- [ ] Consistente com paleta de cores
- [ ] Espaçamento segue scale (4px)
- [ ] Tipografia segue escala
- [ ] Documentado em README do componente

---

## 📚 Referências

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://material.io/design)
- [Tailwind CSS](https://tailwindcss.com)
- [Web.dev Accessibility](https://web.dev/accessibility/)

---

## 📝 Histórico de Versões

| Versão | Data | Alterações |
|--------|------|-----------|
| 1.0.0 | 05/06/2026 | Design System inicial |

---

**Última atualização:** 05 de Junho de 2026  
**Status:** ✅ Design System Completo
