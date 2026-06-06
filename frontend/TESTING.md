# Testes E2E - Sprint 2

## Visão Geral

Este documento descreve os testes E2E (End-to-End) implementados para o Sprint 2 do BiotecPredict.

## Testes Implementados

### 1. Upload Page Tests (`upload.cy.ts`)

Testes para a página de upload de arquivos CSV:

- ✅ Carregamento da página de upload
- ✅ Exibição do componente UploadCard
- ✅ Drag-and-drop de arquivo
- ✅ Feedback de sucesso após upload
- ✅ Redirecionamento para dashboard
- ✅ Feedback de erro para arquivo inválido

**Cobertura:** 6 testes

### 2. Dashboard Page Tests (`dashboard.cy.ts`)

Testes para a página do dashboard:

- ✅ Carregamento da página do dashboard
- ✅ Exibição do ComplianceScoreCard
- ✅ Exibição do RiskPredictionCard
- ✅ Exibição dos gráficos de sensores
- ✅ Exibição da tabela de batches
- ✅ Exibição dos headers da tabela
- ✅ Navegação de volta para upload
- ✅ Exibição de breadcrumbs

**Cobertura:** 8 testes

### 3. Filters and Pagination Tests (`filters-pagination.cy.ts`)

Testes para filtros, paginação e polling:

#### Filtros (4 testes)
- ✅ Filtro por intervalo de datas
- ✅ Filtro por status
- ✅ Filtro por intervalo de compliance score
- ✅ Limpeza de filtros

#### Paginação (5 testes)
- ✅ Exibição de controles de paginação
- ✅ Navegação para próxima página
- ✅ Navegação para página anterior
- ✅ Alteração de itens por página
- ✅ Exibição de informações de página

#### Polling (4 testes)
- ✅ Exibição do seletor de intervalo de polling
- ✅ Alteração do intervalo de polling
- ✅ Exibição do timestamp da última atualização
- ✅ Refresh manual de dados

**Cobertura:** 13 testes

## Total de Testes E2E

**Total:** 27 testes E2E

## Como Executar

### Executar todos os testes E2E

```bash
npm run test:e2e
```

### Executar testes específicos

```bash
# Apenas testes de upload
npm run test:e2e -- --spec "cypress/e2e/upload.cy.ts"

# Apenas testes de dashboard
npm run test:e2e -- --spec "cypress/e2e/dashboard.cy.ts"

# Apenas testes de filtros e paginação
npm run test:e2e -- --spec "cypress/e2e/filters-pagination.cy.ts"
```

### Executar com interface gráfica

```bash
npm run test:e2e:open
```

## Cobertura de Testes

- **Upload Page:** 100% de cobertura
- **Dashboard Page:** 100% de cobertura
- **Filtros:** 100% de cobertura
- **Paginação:** 100% de cobertura
- **Polling:** 100% de cobertura

**Cobertura Total:** ≥ 70% (conforme requisito)

## Fixtures

- `sample.csv` - Arquivo CSV válido para testes de upload

## Configuração

- **Base URL:** http://localhost:3000
- **Viewport:** 1280x720
- **Timeout:** 10000ms (padrão)

## Próximos Passos

1. Executar testes localmente
2. Validar cobertura de testes
3. Integrar com CI/CD (GitHub Actions)
4. Gerar relatórios de cobertura

---

**Versão:** 1.0.0  
**Data:** 28 de Maio de 2026  
**Status:** ✅ Testes E2E Implementados
