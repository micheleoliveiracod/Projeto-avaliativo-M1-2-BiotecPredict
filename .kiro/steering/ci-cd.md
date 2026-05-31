# CI/CD - GitHub Actions

Documentação completa dos workflows de CI/CD implementados no BiotecPredict.

---

## 🎯 Objetivo

Automatizar testes, lint, documentação e deploy através de GitHub Actions, garantindo qualidade de código e rastreabilidade completa.

---

## ⚠️ IMPORTANTE: Política de Workflows (ATUALIZADA)

### Sprint 0 - Sem CI/CD
- ❌ **Sprint 0 (chore/sprint-0-setup-gerenciamento-projeto) NÃO dispara nenhum workflow de testes**
- ✅ Apenas estrutura, documentação e automação
- ✅ Sem código de backend/frontend
- ✅ Sem testes CI/CD ou E2E

### Workflows de CI/CD (Lint + Testes) - Sprint 1+
- ✅ Executam APENAS em: `feature/*`, `bugfix/*` (branches de código e lógica de negócio)
- ❌ NÃO executam em: `chore/*`, `docs/*`, `release/*`, `hotfix/*`, `main`, `develop`
- 🔧 Path filters excluem: `docs/**`, `.kiro/steering/**`, `.github/issue_template/**`, `*.md`
- **Acionamento**: Testes disparam APÓS aprovação do PR (pull_request_review event)
- **Validação**: Testes devem passar ANTES do merge ser permitido
- **Nota**: Sprint 0 (chore/*) NÃO dispara este workflow

### Workflows de Automação de Projeto (Project Board, Issues, PRs)
- ✅ Executam em TODAS as branches (feature/*, bugfix/*, hotfix/*, chore/*, docs/*, release/*, main, develop)
- ✅ Mantêm automação de: Adicionar issues/PRs ao board, Mover status, Sincronizar milestones
- ✅ Não são afetados por path filters

### Workflows de Relatórios (Progress, Velocity, Metrics)
- ✅ Executam em TODAS as branches
- ✅ Agendados (cron) ou disparados por eventos

---

## 📋 Workflows Implementados

### 1. CI - Lint & Tests

**Arquivo:** `.github/workflows/ci.yml`

**Trigger:**
- Pull request review (após aprovação) em branches: `feature/*`, `bugfix/*` (APENAS)
- **Exclusões (paths-ignore):**
  - `docs/**` - Documentação pura
  - `.kiro/steering/**` - Steering files
  - `.github/issue_template/**` - Templates de issues
  - `*.md` - Arquivos markdown

**Nota Importante:** 
- ✅ Testes disparam APENAS APÓS aprovação do PR em branches de código (`feature/*`, `bugfix/*`)
- ✅ Testes devem passar ANTES do merge ser permitido
- ❌ Testes NÃO disparam em push (apenas após PR review)
- ❌ Testes NÃO disparam em `develop`, `main`, `hotfix/*`, `release/*`, `chore/*`, `docs/*`
- ❌ Sem redundância: testes feitos uma vez nas branches de trabalho
- **Sprint 0 (chore/sprint-0-setup-gerenciamento-projeto) NÃO dispara testes CI/CD**
- Testes CI/CD começam em Sprint 1 com branches `feature/*` e `bugfix/*`
- **hotfix/* NÃO dispara testes (removido da política)**

**Jobs:**

#### backend-lint
- Lint com flake8 (erros críticos)
- Formatação com black
- Ordenação de imports com isort
- Python 3.11+

#### backend-tests
- Testes unitários com pytest
- Cobertura com pytest-cov
- PostgreSQL 15-alpine como serviço
- Upload de cobertura para Codecov

#### frontend-lint
- Lint com ESLint
- Node.js 18+
- Cache de npm

#### frontend-tests
- Testes com Vitest
- Cobertura com Vitest
- Upload de cobertura para Codecov

#### api-integration-tests
- Testes de integração com Postman/Newman
- FastAPI server iniciado
- PostgreSQL como serviço
- Relatórios JSON

#### build-status
- Verificação final de status
- Falha se algum job falhar

**Saída:**
- Relatórios de cobertura no Codecov
- Status de build no GitHub
- Logs detalhados

---

### 1.5. Release - Lint Only

**Arquivo:** `.github/workflows/release-lint.yml`

**Objetivo:** Validar apenas lint em branches de release (sem testes unitários/integração/E2E)

**Trigger:**
- Push em branches: release/*
- Pull requests para main

**Jobs:**

#### backend-lint
- Lint com flake8 (erros críticos)
- Formatação com black
- Ordenação de imports com isort
- Python 3.11+

#### frontend-lint
- Lint com ESLint
- Node.js 18+
- Cache de npm

#### lint-status
- Verificação final de status
- Falha se algum job falhar

**Saída:**
- Status de lint no GitHub
- Logs detalhados

**Nota:** Este workflow NÃO executa testes unitários, integração ou E2E. Apenas valida formatação e qualidade de código.

---

### 2. CD - Deploy

**Arquivo:** `.github/workflows/cd.yml`

**Trigger:**
- Tags `v*` (releases)
- Workflow_run do CI (sucesso em main)
- **Exclusões (paths-ignore):**
  - `docs/**` - Documentação pura
  - `.kiro/steering/**` - Steering files
  - `*.md` - Arquivos markdown

**Nota Importante:**
- ✅ Deploy dispara APENAS via tags ou workflow_run
- ❌ Deploy NÃO dispara em push direto em main
- ❌ Deploy NÃO dispara em push em outras branches

---

### 3. Docs Generation

**Arquivo:** `.github/workflows/docs-generation.yml`

**Trigger:**
- Push em develop/main com mudanças em código

**Funcionalidades:**
- Geração de API docs
- Análise de docstrings
- Commit automático

**Saída:**
- Documentação atualizada
- Relatórios de cobertura

---

### 4. AI Test Generation

**Arquivo:** `.github/workflows/ai-test-generation.yml`

**Trigger:**
- Post-commit
- Análise de código novo

**Funcionalidades:**
- Análise de código alterado
- Geração de testes com IA
- Validação de cobertura

**Saída:**
- Testes gerados
- Relatórios de cobertura

---

## 🔧 Configurações

### Backend (Python)

**Arquivo:** `backend/pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests/pytest"]
addopts = "--cov=. --cov-report=html --cov-report=xml"

[tool.coverage.run]
omit = ["*/tests/*", "*/venv/*"]

[tool.black]
line-length = 88

[tool.isort]
profile = "black"
```

**Arquivo:** `backend/.flake8`

```ini
[flake8]
max-line-length = 127
exclude = .git,__pycache__,venv
```

### Frontend (React/TypeScript)

**Arquivo:** `frontend/.eslintrc.cjs`

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: ['eslint:recommended', 'plugin:react/recommended'],
  rules: { /* ... */ }
}
```

**Arquivo:** `frontend/vitest.config.ts`

```typescript
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: { provider: 'v8' }
  }
})
```

---

## 📊 Métricas e Monitoramento

### Cobertura de Testes

- **Mínimo**: 70% (backend + frontend)
- **Alvo**: 80%+
- **Ferramenta**: Codecov

### Lint

- **Backend**: flake8 (erros críticos), black, isort
- **Frontend**: ESLint
- **Ação**: Falha se erros críticos

### Performance

- **Tempo de CI**: ~5-10 minutos
- **Tempo de CD**: ~2-3 minutos
- **Tempo de E2E**: ~10-15 minutos

---

## 🚀 Como Usar

### Visualizar Status

1. Acesse [GitHub Actions](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/actions)
2. Selecione o workflow desejado
3. Verifique status e logs

### Executar Testes Localmente

**Backend:**
```bash
cd backend
pytest tests/pytest/ --cov=. --cov-report=html
```

**Frontend:**
```bash
cd frontend
npm run test:coverage
```

**E2E:**
```bash
cd frontend
npm run test:e2e
```

### Adicionar Novo Workflow

1. Criar arquivo em `.github/workflows/`
2. Definir trigger e jobs
3. Testar localmente com act (opcional)
4. Fazer commit e push

---

## 🔍 Troubleshooting

### Workflow Falhando

1. Verificar logs no GitHub Actions
2. Executar testes localmente
3. Verificar dependências
4. Consultar documentação

### Cobertura Baixa

1. Executar `pytest --cov` localmente
2. Adicionar testes para código novo
3. Verificar relatórios no Codecov

### Build Lento

1. Verificar cache de dependências
2. Otimizar testes
3. Considerar paralelização

---

## 📚 Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Codecov Documentation](https://docs.codecov.io/)

---

## Contexto para o Agente Kiro

Ao trabalhar com CI/CD:

1. **Sempre testar localmente** antes de fazer push
2. **Manter cobertura acima de 70%** em todas as mudanças
3. **Documentar novos workflows** em ci-cd.md
4. **Não commitar secrets** - usar variáveis de ambiente
5. **Monitorar status dos workflows** após push
6. **Resolver falhas rapidamente** - não deixar builds vermelhos

---

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ CI/CD Documentado
