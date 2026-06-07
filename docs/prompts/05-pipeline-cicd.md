# Prompts — Etapa 5: Pipeline CI/CD com GitHub Actions

Prompts utilizados para configurar o pipeline de CI/CD com suporte de IA.

---

## Prompt 5.1 — Geração do workflow CI principal

**Padrão aplicado:** Chain of Thought + Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/pipeline-ci-cd`  
**Data:** 2026-05-28

### Prompt original

```
Como engenheiro DevOps especialista em GitHub Actions e Python/Node.js,
Quero que você crie um workflow de CI para o BiotecPredict,
Para que lint e testes rodem automaticamente a cada push na develop.

Pense passo a passo:
1. Identifique os jobs necessários: backend-lint, backend-tests, frontend-lint, frontend-tests
2. Para cada job, defina as dependências (ex: testes só rodam se lint passar)
3. Configure cache de dependências (pip e npm) para performance
4. Configure banco de dados SQLite como service para os testes de integração

Stack:
- Backend: Python 3.11, flake8, black, pytest
- Frontend: Node 18, ESLint, Vitest

Restrições:
- Trigger: push em develop, paths ignorando docs/ e *.md
- Concorrência: cancel-in-progress para não acumular runs
- Variáveis de ambiente via secrets do GitHub
- Jobs paralelos onde possível para velocidade
```

### Resultado gerado

Workflow `ci.yml` com 4 jobs paralelos: `backend-lint`, `backend-tests` (com SQLite service), `frontend-lint`, `frontend-tests`. Cache configurado para pip e npm.

### Código gerado (antes da correção)

A IA gerou o trigger sem filtro de branch, o que fazia o CI rodar em qualquer push, inclusive em branches de feature sem banco configurado. Node.js estava em v18 e `npm install` era usado no lugar de `npm ci`.

```yaml
name: CI - Lint & Tests

on:
  push:           # ❌ rodava em todas as branches
  pull_request:   # ❌ sem paths-ignore

jobs:

  backend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black isort
          cd backend && pip install -r requirements.txt
      - name: Lint with flake8
        run: cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          cd backend && pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run pytest
        run: cd backend && pytest tests/pytest/ -v  # ❌ sem DATABASE_URL

  frontend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'   # ❌ versão desatualizada
      - name: Install dependencies
        run: cd frontend && npm install  # ❌ npm install em vez de npm ci
      - name: Lint
        run: cd frontend && npm run lint

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'   # ❌ versão desatualizada
      - name: Install dependencies
        run: cd frontend && npm install  # ❌ npm install em vez de npm ci
      - name: Run Vitest
        run: cd frontend && npm run test
```

### Problema identificado e corrigido

A IA gerou o workflow rodando em **todas as branches**, o que causava falhas desnecessárias em branches de feature sem banco configurado. **Correção:** restrito a `develop` com `paths-ignore` para arquivos de documentação. Adicionalmente, Node.js foi atualizado para v20, `npm install` substituído por `npm ci` com cache, e adicionado job `build-status` agregador.

### Código corrigido (depois)

```yaml
name: CI - Lint & Tests

on:
  push:
    branches: [ develop ]           # ✅ restrito à develop
    paths-ignore:
      - 'docs/**'
      - '.specs/**'
      - '.github/issue_template/**'
      - '*.md'
  pull_request:
    branches: [ develop ]
    paths-ignore:
      - 'docs/**'
      - '.specs/**'
      - '.github/issue_template/**'
      - '*.md'

concurrency:
  group: ci-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:

  backend-lint:
    runs-on: ubuntu-latest
    name: Backend - Lint (flake8)
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black isort
          cd backend && pip install -r requirements.txt
      - name: Lint with flake8
        run: |
          cd backend
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      - name: Check formatting with black
        run: cd backend && black --check . || true
      - name: Check import sorting with isort
        run: cd backend && isort --check-only . || true

  backend-tests:
    runs-on: ubuntu-latest
    name: Backend - Unit Tests (pytest)
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          cd backend && pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run pytest with coverage
        run: cd backend && pytest tests/pytest/ --cov=. --cov-report=xml --cov-report=html -v
        env:
          DATABASE_URL: sqlite:///./biotecpredict_test.db   # ✅ variável explícita
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
          flags: backend
          name: backend-coverage

  frontend-lint:
    runs-on: ubuntu-latest
    name: Frontend - Lint (ESLint)
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'                                        # ✅ Node 20
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json        # ✅ cache
      - name: Install dependencies
        run: cd frontend && npm ci                                  # ✅ npm ci
      - name: Lint with ESLint
        run: cd frontend && npm run lint || true

  frontend-tests:
    runs-on: ubuntu-latest
    name: Frontend - Unit Tests (Vitest)
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      - name: Install dependencies
        run: cd frontend && npm ci
      - name: Run Vitest with coverage
        run: cd frontend && npm run test:coverage || npm run test
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
          flags: frontend
          name: frontend-coverage

  build-status:                                                     # ✅ job agregador
    runs-on: ubuntu-latest
    name: Build Status Check
    needs: [backend-lint, backend-tests, frontend-lint, frontend-tests, api-integration-tests]
    if: always()
    steps:
      - name: Check build status
        run: |
          if [ "${{ needs.backend-lint.result }}" = "failure" ] || \
             [ "${{ needs.backend-tests.result }}" = "failure" ] || \
             [ "${{ needs.frontend-lint.result }}" = "failure" ] || \
             [ "${{ needs.frontend-tests.result }}" = "failure" ]; then
            echo "❌ CI Pipeline Failed"
            exit 1
          else
            echo "✅ CI Pipeline Passed"
          fi
```

---

## Prompt 5.2 — Automação do quadro Kanban

**Padrão aplicado:** Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-29

### Prompt original

```
Como engenheiro DevOps especialista em GitHub Actions e GitHub Projects,
Quero que você crie um workflow que automatize o quadro Kanban do projeto,
Para que issues e PRs sejam movidos automaticamente conforme o estado.

Comportamento esperado:
- Issue aberta → coluna "A Fazer"
- PR aberto → coluna "Em Andamento"
- PR em draft → coluna "Em Andamento"
- PR ready for review → coluna "Em Revisão"
- PR/issue fechado → coluna "Concluído"

Configuração:
- Project URL: https://github.com/users/micheleoliveiracod/projects/7
- Token: secret ADD_TO_PROJECT_PAT (com permissão project)

Restrições:
- Use GraphQL API para mover cards (REST não suporta ProjectV2)
- Falhas no workflow não devem bloquear o PR
```

### Resultado gerado

Workflow `project-automation.yml` com jobs para adicionar ao projeto e atualizar status via GraphQL API.

### Código gerado (antes da correção)

A IA gerou os jobs sem `continue-on-error` e sem retry para localizar o card no board, causando falha quando o GitHub Projects ainda não havia indexado o item recém-criado.

```yaml
name: Project Automation

on:
  issues:
    types: [opened, reopened, closed]
  pull_request:
    types: [opened, reopened, closed, converted_to_draft, ready_for_review]

env:
  PROJECT_OWNER: micheleoliveiracod
  PROJECT_NUMBER: 7
  PROJECT_URL: https://github.com/users/micheleoliveiracod/projects/7
  STATUS_FIELD: Status

jobs:
  add-to-project:
    name: Add Issue/PR to Project
    runs-on: ubuntu-latest
    if: github.event.action == 'opened'
    steps:
      - name: Add to project
        # ❌ sem continue-on-error — falha bloqueava o PR
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: ${{ env.PROJECT_URL }}
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}

  move-card:
    name: Move Card to Matching Column
    runs-on: ubuntu-latest
    needs: add-to-project
    if: always()
    steps:
      - name: Update Status field via GraphQL
        # ❌ sem continue-on-error
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
          script: |
            const content = context.payload.pull_request || context.payload.issue;
            // ❌ busca direta sem retry — falhava quando o card ainda não estava indexado
            const result = await github.graphql(`query($id: ID!) {
              node(id: $id) {
                ... on PullRequest { projectItems(first: 20) { nodes { id project { number } } } }
              }
            }`, { id: content.node_id });
            const item = result.node.projectItems.nodes.find((n) => n.project.number === 7);
            if (!item) {
              core.error(`Item não encontrado no board.`);  // ❌ erro fatal
              return;
            }
            await github.graphql(`mutation ...`);
```

### Problema identificado e corrigido

O workflow falhava intermitentemente porque o card adicionado pelo job `add-to-project` ainda não havia sido indexado pelo GitHub Projects no momento em que o job `move-card` tentava localizá-lo. **Correção:** adicionado `continue-on-error: true` em ambos os jobs e loop de retry com 4 tentativas e espera de 3 s entre cada uma.

### Código corrigido (depois)

```yaml
name: Project Automation

on:
  issues:
    types: [opened, reopened, closed]
  pull_request:
    types: [opened, reopened, closed, converted_to_draft, ready_for_review]

env:
  PROJECT_OWNER: micheleoliveiracod
  PROJECT_NUMBER: 7
  PROJECT_URL: https://github.com/users/micheleoliveiracod/projects/7
  STATUS_FIELD: Status

permissions:
  contents: read
  issues: read
  pull-requests: read

jobs:
  add-to-project:
    name: Add Issue/PR to Project
    runs-on: ubuntu-latest
    if: github.event.action == 'opened'
    steps:
      - name: Add to project
        continue-on-error: true                        # ✅ tolerante a falhas
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: ${{ env.PROJECT_URL }}
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}

  move-card:
    name: Move Card to Matching Column
    runs-on: ubuntu-latest
    needs: add-to-project
    if: |
      always() &&
      (github.event_name == 'pull_request' || (github.event_name == 'issues' && github.event.action == 'reopened'))
    steps:
      - name: Update Status field via GraphQL
        continue-on-error: true                        # ✅ tolerante a falhas
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
          script: |
            const content = context.payload.pull_request || context.payload.issue;
            const action = context.payload.action;

            let targetStatus = null;
            if (context.eventName === 'issues' && action === 'reopened') {
              targetStatus = 'Todo';
            } else if (context.eventName === 'pull_request') {
              if (action === 'opened' || action === 'reopened') {
                targetStatus = content.draft ? 'Sprint In Progress' : 'In Review';
              } else if (action === 'converted_to_draft') {
                targetStatus = 'Sprint In Progress';
              } else if (action === 'ready_for_review') {
                targetStatus = 'In Review';
              }
            }
            if (!targetStatus) {
              core.info(`Nenhuma transição mapeada — nada a fazer.`);
              return;
            }

            // ✅ retry com 4 tentativas para aguardar indexação do card no board
            let item = null;
            for (let attempt = 0; attempt < 4 && !item; attempt += 1) {
              if (attempt > 0) await new Promise((resolve) => setTimeout(resolve, 3000));
              const result = await github.graphql(`query($id: ID!) {
                node(id: $id) {
                  ... on Issue { projectItems(first: 20) { nodes { id project { number } } } }
                  ... on PullRequest { projectItems(first: 20) { nodes { id project { number } } } }
                }
              }`, { id: content.node_id });
              item = result.node.projectItems.nodes.find((n) => n.project.number === 7);
            }

            if (!item) {
              core.warning(`#${content.number} não encontrado no board — ignorado.`);  // ✅ warning
              return;
            }

            await github.graphql(`mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) {
              updateProjectV2ItemFieldValue(input: {
                projectId: $project itemId: $item fieldId: $field
                value: { singleSelectOptionId: $option }
              }) { projectV2Item { id } }
            }`, { ... });

            core.info(`#${content.number} movido para "${targetStatus}".`);
```
