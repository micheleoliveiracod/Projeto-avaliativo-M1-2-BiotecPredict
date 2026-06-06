# CI/CD - GitHub Actions

Documentação completa dos workflows de CI/CD implementados no BiotecPredict.

---

## 🎯 Objetivo

Automatizar testes, lint, documentação e deploy através de GitHub Actions, garantindo qualidade de código e rastreabilidade completa.

---

## ⚠️ IMPORTANTE: Política de Workflows (ATUALIZADA)

### Sprint 0 - CI/CD mínimo
- A branch de Sprint 0 (`feature/especificacao-arquitetura`) roda apenas lint/setup — sem suíte de testes, já que ainda não há código de aplicação
- O pipeline completo (lint + testes + cobertura) passa a rodar a partir da Sprint 1, quando o código de produção é gerado

### Workflows de CI/CD (Lint + Testes)
- ✅ Disparam em **push** e **pull request** direcionados à branch `develop`
- 🔧 Path filters (`paths-ignore`) excluem: `docs/**`, `.specs/**`, `.github/issue_template/**`, `*.md`
- **Concorrência**: apenas uma execução ativa por branch/PR — execuções redundantes são canceladas automaticamente

### Workflow de Lint para Release
- ✅ Dispara em `push` para `release/*` e em `pull_request` para `main`
- 🎯 Valida apenas formatação/qualidade — sem testes unitários, integração ou E2E

### Workflow de Automação de Projeto (Project Board)
- ✅ Dispara em eventos de `issues` e `pull_request` (abertura, reabertura, fechamento etc.), em qualquer branch
- ✅ Adiciona issues/PRs ao Project Board e move os cards conforme o status

### CD - Deploy
- ✅ Dispara via push de tag `v*` ou após o workflow "CI - Lint & Tests" concluir com sucesso na branch `main`
- ❌ Não dispara em push direto a outras branches

---

## 📋 Workflows Implementados

### 1. CI - Lint & Tests

**Arquivo:** `.github/workflows/ci.yml`

**Trigger:**
- Push em branches: `develop`
- Pull request direcionado a: `develop`
- **Exclusões (paths-ignore), em ambos os eventos:**
  - `docs/**` - Documentação pura
  - `.specs/**` - Especificações e contexto do projeto
  - `.github/issue_template/**` - Templates de issues
  - `*.md` - Arquivos markdown

**Nota Importante:**
- ✅ Testes disparam a cada push em `develop` ou abertura/atualização de PR contra `develop`
- ✅ Concorrência: apenas uma execução ativa por branch/PR — execuções anteriores são canceladas (`cancel-in-progress`)
- ✅ Testes devem passar para o job `build-status` final ficar verde
- ❌ Mudanças isoladas em documentação/especificação não disparam o workflow (path filters)
- A Sprint 0 (`feature/especificacao-arquitetura`) ainda não possui código de aplicação, então o pipeline roda apenas a etapa de lint/setup; a suíte completa de testes passa a validar mudanças reais a partir da Sprint 1

**Jobs:**

#### backend-lint
- Lint com flake8 (erros críticos)
- Formatação com black
- Ordenação de imports com isort
- Python 3.11+

#### backend-tests
- Testes unitários com pytest
- Cobertura com pytest-cov
- SQLite (sem serviço externo necessário)
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
- SQLite (sem serviço externo necessário)
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
- Push de tags `v*` (releases)
- Conclusão (com sucesso) do workflow "CI - Lint & Tests" na branch `main`

**Nota Importante:**
- ✅ Deploy dispara APENAS via tag `v*` ou via `workflow_run` do CI em `main`
- ❌ Deploy NÃO dispara em push direto em `main`
- ❌ Deploy NÃO dispara em push em outras branches
- Sem `paths-ignore`: qualquer tag `v*` ou execução do CI em `main` aciona o job

---

### 3. E2E Tests - Cypress

**Arquivo:** `.github/workflows/e2e-tests.yml`

**Trigger:**
- Manual (`workflow_dispatch`)
- Agendado (`schedule`, cron configurado para nunca executar na prática — placeholder até a suíte E2E estar pronta)

**Status:** Desabilitado para execução automática nesta fase do projeto. Será ativado quando a suíte de testes E2E (Cypress) estiver consolidada (Sprints de frontend/testes automatizados).

**Jobs:**

#### e2e-tests
- Sobe backend (Python/FastAPI) e frontend (Node.js)
- Executa a suíte Cypress contra a aplicação completa

---

### 4. Project Automation

**Arquivo:** `.github/workflows/project-automation.yml`

**Trigger:**
- Eventos de `issues`: opened, reopened, closed
- Eventos de `pull_request`: opened, reopened, closed, converted_to_draft, ready_for_review
- Roda em qualquer branch — não é afetado por path filters

**Funcionalidades:**
- `add-to-project`: adiciona a issue/PR recém-aberta ao Project Board (via `actions/add-to-project`, autenticado com o secret `ADD_TO_PROJECT_PAT`)
- `move-card`: move o card no board para a coluna de status correspondente ao evento (ex.: Done ao fechar)

**Saída:**
- Issues e PRs sincronizados automaticamente com o Project Board

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
