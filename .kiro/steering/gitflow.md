# Git Flow

## Objetivo

Padronizar o fluxo de versionamento Git adotado neste repositório, garantindo um histórico limpo, rastreável e compreensível para todos os colaboradores. As regras aqui definidas se aplicam tanto ao backend (Python) quanto ao frontend (React) do BiotecPredict.

---

## Branches Principais

| Branch | Papel |
|---|---|
| `main` | Código estável e testado — reflete o que está em produção. Nunca recebe commits diretos. |
| `develop` | Branch de integração. Todas as features concluídas são mergeadas aqui antes de ir para `main`. |

> Nenhum commit deve ser feito diretamente em `main` ou `develop`. Toda alteração passa por uma branch dedicada e PR.

---

## Branches de Trabalho

| Tipo | Quando usar |
|---|---|
| `feature/` | Nova funcionalidade (ex: novo coletor, nova página no frontend) |
| `bugfix/` | Correção de bug identificado em `develop` |
| `hotfix/` | Correção urgente de bug em produção — parte de `main`, volta para `main` e `develop` |
| `release/` | Preparação de versão antes de ir para `main` (ajustes finais, bump de versão, changelog) |
| `chore/` | Tarefas de manutenção sem impacto funcional (dependências, configs, CI) |
| `docs/` | Alterações exclusivas de documentação |

---

## Convenção de Nomes de Branches

```
feature/nome-da-funcionalidade
bugfix/descricao-do-ajuste
hotfix/descricao-do-problema
release/v1.2.0
chore/descricao-da-tarefa
docs/descricao-da-documentacao
```

**Regras:**
- Letras minúsculas e hífens — sem espaços, underscores ou caracteres especiais
- Nomes curtos e descritivos
- Usar o idioma do projeto (português, manter consistência)

**Exemplos práticos:**
```
feature/upload-csv
feature/compliance-score-engine
feature/ml-prediction
bugfix/csv-validation-error
hotfix/api-crash-batch-processing
chore/atualiza-dependencias-python
docs/atualiza-readme-stack
release/v0.1.0
```

---

## Convenção de Commits

Adotar o padrão [Conventional Commits](https://www.conventionalcommits.org/).

### Formato

```
<tipo>(<escopo opcional>): <descrição curta no imperativo>
```

### Tipos

| Tipo | Quando usar | Descrição |
|---|---|---|
| `feat` | Nova funcionalidade | Implementa novas características |
| `fix` | Correção de bug | Corrige bugs |
| `docs` | Alteração de documentação | Atualiza documentos e instruções de execução |
| `chore` | Manutenção | Adiciona scripts setup, atualiza dependências, configurações |
| `refactor` | Reorganização de código | Melhora código sem mudar função |
| `test` | Adição ou correção de testes | Testes unitários e integração |
| `style` | Formatação, espaçamento | Sem impacto lógico |
| `perf` | Melhoria de performance | Otimizações |
| `ci` | Alterações em pipelines | CI/CD |

### Exemplos

```
feat(api): adiciona endpoint de upload de CSV
feat(ml): implementa RandomForestClassifier para predição
fix(processors): corrige validação de ranges de sensores
fix(frontend): corrige renderização do dashboard em mobile
docs: atualiza README com fluxo de processamento
chore: atualiza dependências do requirements.txt
refactor(services): separa lógica de compliance score
test(services): adiciona testes unitários para compliance
```

**Regras:**
- Descrição no imperativo e em letras minúsculas
- Sem ponto final
- Máximo de 72 caracteres na primeira linha
- Commits atômicos — uma alteração lógica por commit

---

## Issues

### Templates de Issues

O projeto utiliza **templates estruturados** para padronizar a criação de issues. Ao criar uma nova issue, escolha o template apropriado:

| Template | Quando usar |
|---|---|
| 🚀 **Feature Request** | Propor novas funcionalidades |
| 🐛 **Bug Report** | Reportar bugs ou comportamentos incorretos |
| 📚 **Documentation** | Melhorias ou adições à documentação |
| 🔧 **Chore/Maintenance** | Tarefas de manutenção, configuração ou refatoração |
| 💬 **General Issue** | Issues que não se encaixam nas outras categorias |

**Como usar:**
1. Acesse [Issues > New Issue](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues/new/choose)
2. Selecione o template apropriado
3. Preencha todos os campos obrigatórios
4. Adicione labels relevantes (se não forem adicionadas automaticamente)

---

## Pull Requests

### Template de Pull Request

O projeto utiliza um **template automático** para PRs. Ao abrir uma nova PR, o template será aplicado automaticamente com as seguintes seções:

- **Contexto** — Por que a mudança é necessária
- **O que foi feito** — Descrição das alterações
- **Como testar** — Passos para validação
- **Dependências** — Issues relacionadas (`Closes #123`)
- **Referências** — Links para documentação
- **Checklist** — Itens de verificação
- **Screenshots/Logs** — Evidências visuais (opcional)

### Título
Seguir o mesmo padrão de Conventional Commits:
```
feat(api): adiciona endpoint de upload de CSV
fix(ml): corrige predição de risco
```

### Descrição
O template já inclui as seções obrigatórias. Preencha todas as seções relevantes:

- **Contexto** — Por que essa mudança é necessária? Qual problema ela resolve?
- **O que foi feito** — Descreva as alterações de forma clara e objetiva
- **Como testar** — Passo a passo para validar as alterações localmente
- **Dependências** — Use `Closes #123` para fechar issues automaticamente
- **Referências** — Links para documentação, steering files, ou recursos externos

### Antes de abrir o PR
- [ ] Código testado localmente
- [ ] Testes unitários/integração adicionados (quando aplicável)
- [ ] Documentação atualizada (quando aplicável)
- [ ] Commits seguem Conventional Commits
- [ ] Sem conflitos com a branch de destino (`develop` ou `main`)
- [ ] Template de PR preenchido completamente

### Revisão
- Todo PR deve ter ao menos **1 aprovação** antes do merge
- **Nenhum membro da equipe pode aprovar seu próprio PR**
- Comentários de revisão devem ser resolvidos antes do merge
- O autor do PR é responsável por resolver conflitos

---

## Merge Strategy

### Recomendação padrão: **Squash Merge**

Para branches `feature/`, `bugfix/`, `chore/` e `docs/` mergeando em `develop`:
- Usar **squash merge** — consolida todos os commits da branch em um único commit limpo no histórico de `develop`
- O título do commit resultante deve seguir a convenção de Conventional Commits

Para branches `release/` mergeando em `main`:
- Usar **merge commit** — preserva o contexto da release no histórico

Para branches `hotfix/` mergeando em `main` e `develop`:
- Usar **merge commit** — mantém rastreabilidade da correção urgente

| Tipo de branch | Destino | Estratégia | CI/CD |
|---|---|---|---|
| `feature/`, `bugfix/`, `chore/`, `docs/` | `develop` | Squash merge | ✅ Completo |
| `release/` | `main` | Merge commit | ⚠️ Lint only |
| `hotfix/` | `main` e `develop` | Merge commit | ✅ Completo |

---

## Política de CI/CD por Tipo de Branch

### Branches com CI/CD Completo (Lint + Unit + Integration + E2E)

- `feature/*` - Novas funcionalidades
- `bugfix/*` - Correções de bugs
- `hotfix/*` - Correções urgentes
- `main` - Produção
- `develop` - Integração

### Branches com Lint Only (Sem Testes)

- `release/*` - Preparação de release (apenas lint, sem testes)

### Branches sem CI/CD (Nenhum Teste)

- `chore/*` - Gerenciamento/configuração
- `docs/*` - Documentação pura

**Justificativa:**
- `chore/*` e `docs/*` não contêm código que afeta funcionalidade
- `release/*` já passou por testes completos em `develop`, apenas valida formatação
- Evita falsos positivos e desperdício de recursos

---

## Merge Strategy

---

## Releases

Adotar **versionamento semântico** ([SemVer](https://semver.org/)): `MAJOR.MINOR.PATCH`

| Incremento | Quando usar |
|---|---|
| `MAJOR` | Mudança incompatível com versão anterior |
| `MINOR` | Nova funcionalidade compatível com versão anterior |
| `PATCH` | Correção de bug compatível com versão anterior |

### Fluxo de release

1. Criar branch `release/vX.Y.Z` a partir de `develop`
2. Realizar ajustes finais (bump de versão, atualização de changelog)
3. Abrir PR de `release/vX.Y.Z` → `main`
4. Após merge em `main`, criar **tag** com a versão:
   ```
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
5. Mergear `main` de volta em `develop` para sincronizar

### Changelog
Manter um arquivo `CHANGELOG.md` na raiz do projeto, atualizado a cada release com as alterações agrupadas por tipo (`feat`, `fix`, etc.).

---

## Boas Práticas

- **Branches de curta duração** — feature branches devem ser mergeadas e deletadas assim que concluídas; evitar branches abertas por mais de uma semana sem atividade
- **Commits frequentes e atômicos** — commitar uma alteração lógica por vez, não acumular dias de trabalho em um único commit
- **Nunca fazer force push em `main` ou `develop`** — apenas em branches pessoais de trabalho, e com cautela
- **Deletar branches após o merge** — manter o repositório limpo
- **Sincronizar com `develop` regularmente** — fazer rebase ou merge de `develop` na feature branch para evitar conflitos grandes no final
- **Não commitar segredos** — chaves de API (ex: `ANTHROPIC_API_KEY`), senhas ou tokens nunca devem ir para o repositório; usar `.env` com `.gitignore` configurado

---

# Sprints - BiotecPredict

Organização detalhada dos 6 sprints com 5 issues cada (total de 30 issues) e 30 branches correspondentes (5 por sprint).

---

## 📋 Índice Rápido de Branches

| Sprint | Branches | Total |
|--------|----------|-------|
| **Sprint 0** | `feature/project-structure`, `feature/database-setup`, `feature/fastapi-setup`, `feature/react-setup`, `chore/create-issues-milestones` | 5 |
| **Sprint 1** | `feature/sqlalchemy-models`, `feature/pydantic-schemas`, `feature/upload-endpoint`, `feature/query-endpoints`, `feature/backend-unit-tests` | 5 |
| **Sprint 2** | `feature/home-upload-page`, `feature/dashboard-kpis`, `feature/batch-table`, `feature/api-integration`, `feature/frontend-e2e-tests` | 5 |
| **Sprint 3** | `feature/compliance-score-engine`, `feature/ml-pipeline-randomforest`, `feature/model-training`, `feature/ml-analytics-page`, `feature/ml-tests` | 5 |
| **Sprint 4** | `feature/backend-pytest-coverage`, `feature/frontend-vitest-coverage`, `feature/postman-integration-tests`, `feature/cypress-e2e-tests`, `feature/coverage-validation` | 5 |
| **Sprint 5** | `feature/swagger-documentation`, `feature/dev-guides`, `feature/data-validation-scripts`, `feature/compliance-validation-scripts`, `release/v1.0.0` | 5 |
| **TOTAL** | | **30** |

---

## Sprint 0 — Setup e Gerenciamento (5 Issues)

### Macro Escopo
Estabelecer a base de gerenciamento do projeto com estrutura, documentação e configurações de automação.

### Período
24/05/2026 (sexta) até 26/05/2026 (domingo) — 3 dias

### Issues (5 total)

#### #1 - setup: estruturar repositório e diretórios base
- **Branch**: `feature/project-structure`
- **Labels**: setup, backend, frontend, sprint-0
- **Milestone**: Sprint 0 - Setup
- **Descrição**: Criar estrutura de diretórios conforme `.kiro/steering/structure.md`
- **Checklist de Atividades**:
  - [ ] Criar diretórios backend (api/, processors/, services/, models/, schemas/, db/, ml/, scripts/, reports/, tests/)
  - [ ] Criar diretórios frontend (src/components/, src/pages/, src/services/, src/hooks/, src/utils/)
  - [ ] Criar arquivos README.md em diretórios principais
  - [ ] Configurar .gitignore para Python e React
  - [ ] Criar arquivos iniciais (requirements.txt, package.json)
- **Critérios de Aceitação**:
  - [ ] Estrutura de diretórios criada conforme especificação
  - [ ] Projeto pode ser inicializado localmente
  - [ ] Todos os .gitignore configurados corretamente

#### #2 - setup: configurar banco de dados PostgreSQL e ORM
- **Branch**: `feature/database-setup`
- **Labels**: setup, database, backend, sprint-0
- **Milestone**: Sprint 0 - Setup
- **Descrição**: Configurar SQLAlchemy e conexão com PostgreSQL
- **Checklist de Atividades**:
  - [ ] Criar modelos SQLAlchemy (Batch, SensorReading, Prediction)
  - [ ] Implementar repository pattern
  - [ ] Configurar conexão com SQLite (dev) e PostgreSQL (prod)
  - [ ] Criar migrations iniciais
  - [ ] Implementar funções CRUD básicas
- **Critérios de Aceitação**:
  - [ ] Modelos SQLAlchemy funcionando
  - [ ] Conexão com banco de dados testada
  - [ ] Migrations executadas com sucesso

#### #3 - setup: configurar FastAPI e endpoints base
- **Branch**: `feature/fastapi-setup`
- **Labels**: setup, backend, api, sprint-0
- **Milestone**: Sprint 0 - Setup
- **Descrição**: Configurar FastAPI com estrutura base
- **Checklist de Atividades**:
  - [ ] Criar main.py com FastAPI app
  - [ ] Configurar CORS e middleware
  - [ ] Criar estrutura de rotas (api/routes/)
  - [ ] Implementar health check endpoint
  - [ ] Configurar documentação Swagger
- **Critérios de Aceitação**:
  - [ ] FastAPI rodando localmente
  - [ ] Swagger acessível em /docs
  - [ ] Health check respondendo

#### #4 - setup: configurar React e estrutura de componentes
- **Branch**: `feature/react-setup`
- **Labels**: setup, frontend, ui, sprint-0
- **Milestone**: Sprint 0 - Setup
- **Descrição**: Configurar React com Vite e estrutura base
- **Checklist de Atividades**:
  - [ ] Criar projeto React com Vite
  - [ ] Configurar TailwindCSS
  - [ ] Criar estrutura de componentes base
  - [ ] Configurar roteamento (React Router)
  - [ ] Criar serviço de API (Axios)
- **Critérios de Aceitação**:
  - [ ] React rodando localmente
  - [ ] Componentes base criados
  - [ ] Roteamento funcionando

#### #5 - setup: criar issues e milestones do projeto
- **Branch**: `chore/create-issues-milestones`
- **Labels**: setup, chore, sprint-0
- **Milestone**: Sprint 0 - Setup
- **Descrição**: Criar todas as 30 issues e 6 milestones no GitHub
- **Checklist de Atividades**:
  - [ ] Criar 6 milestones (Sprint 0-5)
  - [ ] Criar 30 issues (5 por sprint)
  - [ ] Adicionar labels apropriadas
  - [ ] Configurar GitHub Project Board
  - [ ] Adicionar issues ao board
- **Critérios de Aceitação**:
  - [ ] Todas as 30 issues criadas
  - [ ] Milestones configurados
  - [ ] Board Kanban funcional

### Branches (5 total)

```
feature/project-structure
feature/database-setup
feature/fastapi-setup
feature/react-setup
chore/create-issues-milestones
```

---

## Sprint 1 — Backend + API + Modelos (5 Issues)

### Macro Escopo
Implementar backend FastAPI com modelos de dados, schemas de validação e endpoints REST para processamento de batches.

### Período
27/05/2026 (segunda) — 1 dia

### Issues (5 total)

#### #6 - feat(backend): implementar modelos SQLAlchemy
- **Branch**: `feature/sqlalchemy-models`
- **Labels**: backend, database, feat, sprint-1
- **Milestone**: Sprint 1 - Backend
- **Descrição**: Criar modelos SQLAlchemy para Batch, SensorReading e Prediction
- **Checklist de Atividades**:
  - [ ] Criar modelo Batch com campos: id, upload_date, status, compliance_score, risk_prediction
  - [ ] Criar modelo SensorReading com campos: temperature, ph, dissolved_oxygen, pressure, agitator_speed
  - [ ] Criar modelo Prediction com campos: model_version, prediction_timestamp, confidence_score
  - [ ] Implementar relacionamentos entre modelos
  - [ ] Adicionar validações e constraints
- **Critérios de Aceitação**:
  - [ ] Modelos criados e testados
  - [ ] Relacionamentos funcionando
  - [ ] Migrations executadas

#### #7 - feat(backend): criar schemas Pydantic
- **Branch**: `feature/pydantic-schemas`
- **Labels**: backend, api, feat, sprint-1
- **Milestone**: Sprint 1 - Backend
- **Descrição**: Criar schemas Pydantic para validação de entrada/saída
- **Checklist de Atividades**:
  - [ ] Criar schema BatchCreate para upload
  - [ ] Criar schema BatchResponse para retorno
  - [ ] Criar schema SensorReadingSchema
  - [ ] Criar schema PredictionSchema
  - [ ] Adicionar validações customizadas
- **Critérios de Aceitação**:
  - [ ] Schemas validando corretamente
  - [ ] Documentação Swagger atualizada
  - [ ] Testes de validação passando

#### #8 - feat(api): criar endpoint POST /upload
- **Branch**: `feature/upload-endpoint`
- **Labels**: backend, api, feat, sprint-1
- **Milestone**: Sprint 1 - Backend
- **Descrição**: Implementar endpoint para upload de arquivo CSV
- **Checklist de Atividades**:
  - [ ] Criar rota POST /api/v1/upload
  - [ ] Implementar validação de arquivo CSV
  - [ ] Processar dados do CSV
  - [ ] Persistir batch no banco
  - [ ] Retornar ID do batch criado
- **Critérios de Aceitação**:
  - [ ] Endpoint respondendo corretamente
  - [ ] Arquivo CSV processado
  - [ ] Batch persistido no banco

#### #9 - feat(api): criar endpoints GET de consulta
- **Branch**: `feature/query-endpoints`
- **Labels**: backend, api, feat, sprint-1
- **Milestone**: Sprint 1 - Backend
- **Descrição**: Implementar endpoints para consultar batches e resultados
- **Checklist de Atividades**:
  - [ ] Criar rota GET /api/v1/batches (listar todos)
  - [ ] Criar rota GET /api/v1/batch/{id} (detalhes)
  - [ ] Criar rota GET /api/v1/prediction/{batch_id}
  - [ ] Criar rota GET /api/v1/compliance/{batch_id}
  - [ ] Implementar filtros e paginação
- **Critérios de Aceitação**:
  - [ ] Todos os endpoints respondendo
  - [ ] Dados retornados corretamente
  - [ ] Filtros funcionando

#### #10 - test(backend): implementar testes unitários
- **Branch**: `feature/backend-unit-tests`
- **Labels**: backend, testing, test, sprint-1
- **Milestone**: Sprint 1 - Backend
- **Descrição**: Criar testes unitários com pytest
- **Checklist de Atividades**:
  - [ ] Criar testes para modelos
  - [ ] Criar testes para schemas
  - [ ] Criar testes para endpoints
  - [ ] Criar testes para services
  - [ ] Atingir cobertura mínima de 70%
- **Critérios de Aceitação**:
  - [ ] Testes passando
  - [ ] Cobertura ≥ 70%
  - [ ] Sem warnings

### Branches (5 total)

```
feature/sqlalchemy-models
feature/pydantic-schemas
feature/upload-endpoint
feature/query-endpoints
feature/backend-unit-tests
```

---

## Sprint 2 — Frontend + Dashboard (5 Issues)

### Macro Escopo
Implementar frontend React com interface de upload, dashboard analítico e integração com API backend.

### Período
28/05/2026 (terça) — 1 dia

### Issues (5 total)

#### #11 - feat(frontend): criar página Home com upload
- **Branch**: `feature/home-upload-page`
- **Labels**: frontend, ui, feat, sprint-2
- **Milestone**: Sprint 2 - Frontend
- **Descrição**: Implementar página inicial com interface de upload de CSV
- **Checklist de Atividades**:
  - [ ] Criar componente UploadCard
  - [ ] Implementar drag-and-drop
  - [ ] Validar arquivo CSV
  - [ ] Chamar API de upload
  - [ ] Exibir feedback de sucesso/erro
- **Critérios de Aceitação**:
  - [ ] Upload funcionando
  - [ ] Validação de arquivo
  - [ ] Feedback ao usuário

#### #12 - feat(frontend): criar Dashboard com KPIs
- **Branch**: `feature/dashboard-kpis`
- **Labels**: frontend, ui, components, feat, sprint-2
- **Milestone**: Sprint 2 - Frontend
- **Descrição**: Implementar dashboard com visualização de KPIs
- **Checklist de Atividades**:
  - [ ] Criar componente Dashboard
  - [ ] Exibir compliance score
  - [ ] Exibir predição de risco
  - [ ] Criar gráficos com Recharts
  - [ ] Implementar atualização em tempo real
- **Critérios de Aceitação**:
  - [ ] Dashboard renderizando
  - [ ] Gráficos exibindo dados
  - [ ] Dados atualizando

#### #13 - feat(frontend): criar tabela de batches
- **Branch**: `feature/batch-table`
- **Labels**: frontend, ui, components, feat, sprint-2
- **Milestone**: Sprint 2 - Frontend
- **Descrição**: Implementar tabela com histórico de batches
- **Checklist de Atividades**:
  - [ ] Criar componente BatchTable
  - [ ] Listar todos os batches
  - [ ] Implementar filtros (data, status, score)
  - [ ] Implementar paginação
  - [ ] Adicionar link para detalhes
- **Critérios de Aceitação**:
  - [ ] Tabela exibindo batches
  - [ ] Filtros funcionando
  - [ ] Paginação implementada

#### #14 - feat(frontend): integração com API backend
- **Branch**: `feature/api-integration`
- **Labels**: frontend, api, feat, sprint-2
- **Milestone**: Sprint 2 - Frontend
- **Descrição**: Integrar frontend com endpoints da API
- **Checklist de Atividades**:
  - [ ] Criar serviço de API (Axios)
  - [ ] Implementar chamadas para todos os endpoints
  - [ ] Adicionar tratamento de erros
  - [ ] Implementar loading states
  - [ ] Adicionar cache de dados
- **Critérios de Aceitação**:
  - [ ] Todas as chamadas funcionando
  - [ ] Erros tratados
  - [ ] Loading states visíveis

#### #15 - test(frontend): implementar testes E2E
- **Branch**: `feature/frontend-e2e-tests`
- **Labels**: frontend, testing, test, sprint-2
- **Milestone**: Sprint 2 - Frontend
- **Descrição**: Criar testes E2E com Cypress
- **Checklist de Atividades**:
  - [ ] Criar testes de upload
  - [ ] Criar testes de dashboard
  - [ ] Criar testes de tabela
  - [ ] Criar testes de filtros
  - [ ] Atingir cobertura mínima de 70%
- **Critérios de Aceitação**:
  - [ ] Testes passando
  - [ ] Cobertura ≥ 70%
  - [ ] Sem warnings

### Branches (5 total)

```
feature/home-upload-page
feature/dashboard-kpis
feature/batch-table
feature/api-integration
feature/frontend-e2e-tests
```

---

## Sprint 3 — ML + Compliance + Predição (5 Issues)

### Macro Escopo
Implementar machine learning com RandomForestClassifier e cálculo de Manufacturing Compliance Score baseado em regras determinísticas.

### Período
29/05/2026 (quarta) — 1 dia

### Issues (5 total)

#### #16 - feat(ml): implementar Compliance Score Engine
- **Branch**: `feature/compliance-score-engine`
- **Labels**: backend, business-logic, feat, sprint-3
- **Milestone**: Sprint 3 - ML
- **Descrição**: Criar engine para cálculo de compliance score
- **Checklist de Atividades**:
  - [ ] Implementar regras de validação por sensor
  - [ ] Calcular score 0-100
  - [ ] Classificar em ACCEPTABLE/WARNING/CRITICAL
  - [ ] Adicionar rastreabilidade de cálculos
  - [ ] Criar testes de validação
- **Critérios de Aceitação**:
  - [ ] Score calculado corretamente
  - [ ] Classificação correta
  - [ ] Rastreabilidade implementada

#### #17 - feat(ml): criar ML Pipeline com RandomForest
- **Branch**: `feature/ml-pipeline-randomforest`
- **Labels**: backend, business-logic, feat, sprint-3
- **Milestone**: Sprint 3 - ML
- **Descrição**: Implementar pipeline de ML com RandomForestClassifier
- **Checklist de Atividades**:
  - [ ] Criar pipeline de preprocessamento
  - [ ] Implementar RandomForestClassifier
  - [ ] Configurar features (Temperature, pH, DO, Pressure, Agitator Speed)
  - [ ] Implementar predição
  - [ ] Adicionar confidence score
- **Critérios de Aceitação**:
  - [ ] Pipeline funcionando
  - [ ] Predições geradas
  - [ ] Confidence score calculado

#### #18 - feat(ml): treinar modelo com dataset Kaggle
- **Branch**: `feature/model-training`
- **Labels**: backend, business-logic, feat, sprint-3
- **Milestone**: Sprint 3 - ML
- **Descrição**: Treinar modelo com dataset Kaggle
- **Checklist de Atividades**:
  - [ ] Carregar dataset Kaggle
  - [ ] Preparar dados (train/test split)
  - [ ] Treinar RandomForestClassifier
  - [ ] Validar acurácia (≥ 80%)
  - [ ] Salvar modelo treinado
- **Critérios de Aceitação**:
  - [ ] Modelo treinado
  - [ ] Acurácia ≥ 80%
  - [ ] Modelo persistido

#### #19 - feat(frontend): criar página ML Analytics
- **Branch**: `feature/ml-analytics-page`
- **Labels**: frontend, ui, feat, sprint-3
- **Milestone**: Sprint 3 - ML
- **Descrição**: Criar página com análises de ML
- **Checklist de Atividades**:
  - [ ] Criar componente MLAnalytics
  - [ ] Exibir predição de risco
  - [ ] Exibir confidence score
  - [ ] Criar gráficos de distribuição
  - [ ] Adicionar histórico de predições
- **Critérios de Aceitação**:
  - [ ] Página renderizando
  - [ ] Dados exibindo
  - [ ] Gráficos funcionando

#### #20 - test(ml): implementar testes de ML
- **Branch**: `feature/ml-tests`
- **Labels**: backend, testing, test, sprint-3
- **Milestone**: Sprint 3 - ML
- **Descrição**: Criar testes para compliance score e ML
- **Checklist de Atividades**:
  - [ ] Testes de compliance score
  - [ ] Testes de predição
  - [ ] Testes de confidence score
  - [ ] Testes de edge cases
  - [ ] Atingir cobertura mínima de 70%
- **Critérios de Aceitação**:
  - [ ] Testes passando
  - [ ] Cobertura ≥ 70%
  - [ ] Sem warnings

### Branches (5 total)

```
feature/compliance-score-engine
feature/ml-pipeline-randomforest
feature/model-training
feature/ml-analytics-page
feature/ml-tests
```

---

## Sprint 4 — Testes + Cobertura (5 Issues)

### Macro Escopo
Implementar suite completa de testes com cobertura mínima de 70% em backend e frontend.

### Período
30/05/2026 (quinta) — 1 dia

### Issues (5 total)

#### #21 - test(backend): testes unitários com pytest
- **Branch**: `feature/backend-pytest-coverage`
- **Labels**: backend, testing, test, sprint-4
- **Milestone**: Sprint 4 - Testes
- **Descrição**: Expandir testes unitários backend para 70% cobertura
- **Checklist de Atividades**:
  - [ ] Adicionar testes para todos os services
  - [ ] Adicionar testes para processors
  - [ ] Adicionar testes para validators
  - [ ] Gerar relatório de cobertura
  - [ ] Atingir 70% de cobertura
- **Critérios de Aceitação**:
  - [ ] Cobertura ≥ 70%
  - [ ] Testes passando
  - [ ] Relatório gerado

#### #22 - test(frontend): testes unitários com Vitest
- **Branch**: `feature/frontend-vitest-coverage`
- **Labels**: frontend, testing, test, sprint-4
- **Milestone**: Sprint 4 - Testes
- **Descrição**: Expandir testes unitários frontend para 70% cobertura
- **Checklist de Atividades**:
  - [ ] Adicionar testes para componentes
  - [ ] Adicionar testes para hooks
  - [ ] Adicionar testes para services
  - [ ] Gerar relatório de cobertura
  - [ ] Atingir 70% de cobertura
- **Critérios de Aceitação**:
  - [ ] Cobertura ≥ 70%
  - [ ] Testes passando
  - [ ] Relatório gerado

#### #23 - test(api): testes de integração com Postman
- **Branch**: `feature/postman-integration-tests`
- **Labels**: backend, api, testing, test, sprint-4
- **Milestone**: Sprint 4 - Testes
- **Descrição**: Criar testes de integração com Postman/Newman
- **Checklist de Atividades**:
  - [ ] Criar collection Postman
  - [ ] Adicionar testes para todos os endpoints
  - [ ] Configurar environment variables
  - [ ] Executar testes com Newman
  - [ ] Gerar relatórios
- **Critérios de Aceitação**:
  - [ ] Testes passando
  - [ ] Todos os endpoints testados
  - [ ] Relatórios gerados

#### #24 - test(e2e): testes E2E com Cypress
- **Branch**: `feature/cypress-e2e-tests`
- **Labels**: frontend, testing, test, sprint-4
- **Milestone**: Sprint 4 - Testes
- **Descrição**: Expandir testes E2E com Cypress
- **Checklist de Atividades**:
  - [ ] Criar testes de fluxo completo
  - [ ] Adicionar testes de responsividade
  - [ ] Adicionar testes de performance
  - [ ] Gerar relatórios
  - [ ] Atingir cobertura mínima
- **Critérios de Aceitação**:
  - [ ] Testes passando
  - [ ] Fluxos completos testados
  - [ ] Relatórios gerados

#### #25 - test(coverage): validação de cobertura e relatórios
- **Branch**: `feature/coverage-validation`
- **Labels**: testing, ci, test, sprint-4
- **Milestone**: Sprint 4 - Testes
- **Descrição**: Validar cobertura total e gerar relatórios
- **Checklist de Atividades**:
  - [ ] Consolidar cobertura backend + frontend
  - [ ] Gerar relatório consolidado
  - [ ] Validar cobertura ≥ 70%
  - [ ] Criar dashboard de cobertura
  - [ ] Documentar resultados
- **Critérios de Aceitação**:
  - [ ] Cobertura total ≥ 70%
  - [ ] Relatórios gerados
  - [ ] Dashboard acessível

### Branches (5 total)

```
feature/backend-pytest-coverage
feature/frontend-vitest-coverage
feature/postman-integration-tests
feature/cypress-e2e-tests
feature/coverage-validation
```

---

## Sprint 5 — Documentação + Validação + Deploy (5 Issues)

### Macro Escopo
Documentação técnica completa, scripts de validação de qualidade de dados e deploy final em produção.

### Período
31/05/2026 (sexta) — 1 dia

### Issues (5 total)

#### #26 - docs: documentação de API com Swagger
- **Branch**: `feature/swagger-documentation`
- **Labels**: documentation, backend, docs, sprint-5
- **Milestone**: Sprint 5 - Documentação
- **Descrição**: Criar documentação completa da API com Swagger
- **Checklist de Atividades**:
  - [ ] Documentar todos os endpoints
  - [ ] Adicionar exemplos de requisição/resposta
  - [ ] Documentar schemas
  - [ ] Adicionar autenticação (se aplicável)
  - [ ] Gerar OpenAPI spec
- **Critérios de Aceitação**:
  - [ ] Swagger acessível em /docs
  - [ ] Todos os endpoints documentados
  - [ ] Exemplos funcionando

#### #27 - docs: guias de desenvolvimento
- **Branch**: `feature/dev-guides`
- **Labels**: documentation, docs, sprint-5
- **Milestone**: Sprint 5 - Documentação
- **Descrição**: Criar guias de desenvolvimento
- **Checklist de Atividades**:
  - [ ] Criar guia de setup local
  - [ ] Criar guia de arquitetura
  - [ ] Criar guia de contribuição
  - [ ] Criar guia de deployment
  - [ ] Adicionar troubleshooting
- **Critérios de Aceitação**:
  - [ ] Guias completos
  - [ ] Exemplos funcionando
  - [ ] Fácil de seguir

#### #28 - feat(validation): scripts de validação de dados
- **Branch**: `feature/data-validation-scripts`
- **Labels**: backend, validation, feat, sprint-5
- **Milestone**: Sprint 5 - Documentação
- **Descrição**: Criar scripts para validação de qualidade de dados
- **Checklist de Atividades**:
  - [ ] Criar validate_data.py
  - [ ] Validar ranges de sensores
  - [ ] Detectar outliers
  - [ ] Gerar relatórios
  - [ ] Adicionar logging
- **Critérios de Aceitação**:
  - [ ] Script funcionando
  - [ ] Validações corretas
  - [ ] Relatórios gerados

#### #29 - feat(validation): scripts de validação de compliance
- **Branch**: `feature/compliance-validation-scripts`
- **Labels**: backend, validation, feat, sprint-5
- **Milestone**: Sprint 5 - Documentação
- **Descrição**: Criar scripts para validação de compliance score
- **Checklist de Atividades**:
  - [ ] Criar validate_compliance.py
  - [ ] Validar cálculos de score
  - [ ] Verificar classificações
  - [ ] Gerar relatórios
  - [ ] Adicionar rastreabilidade
- **Critérios de Aceitação**:
  - [ ] Script funcionando
  - [ ] Validações corretas
  - [ ] Relatórios gerados

#### #30 - chore: deploy em produção e entrega final
- **Branch**: `release/v1.0.0`
- **Labels**: chore, ci, sprint-5
- **Milestone**: Sprint 5 - Documentação
- **Descrição**: Deploy final em produção e entrega do projeto
- **Checklist de Atividades**:
  - [ ] Preparar ambiente de produção
  - [ ] Executar migrations
  - [ ] Deploy da aplicação
  - [ ] Testes de smoke
  - [ ] Documentar processo de deploy
- **Critérios de Aceitação**:
  - [ ] Aplicação em produção
  - [ ] Testes passando
  - [ ] Documentação completa

### Branches (5 total)

```
feature/swagger-documentation
feature/dev-guides
feature/data-validation-scripts
feature/compliance-validation-scripts
release/v1.0.0
```

---

## Resumo de Branches por Sprint

### Sprint 0 — Setup e Gerenciamento (5 branches)
```
feature/project-structure
feature/database-setup
feature/fastapi-setup
feature/react-setup
chore/create-issues-milestones
```

### Sprint 1 — Backend + API + Modelos (5 branches)
```
feature/sqlalchemy-models
feature/pydantic-schemas
feature/upload-endpoint
feature/query-endpoints
feature/backend-unit-tests
```

### Sprint 2 — Frontend + Dashboard (5 branches)
```
feature/home-upload-page
feature/dashboard-kpis
feature/batch-table
feature/api-integration
feature/frontend-e2e-tests
```

### Sprint 3 — ML + Compliance + Predição (5 branches)
```
feature/compliance-score-engine
feature/ml-pipeline-randomforest
feature/model-training
feature/ml-analytics-page
feature/ml-tests
```

### Sprint 4 — Testes + Cobertura (5 branches)
```
feature/backend-pytest-coverage
feature/frontend-vitest-coverage
feature/postman-integration-tests
feature/cypress-e2e-tests
feature/coverage-validation
```

### Sprint 5 — Documentação + Validação + Deploy (5 branches)
```
feature/swagger-documentation
feature/dev-guides
feature/data-validation-scripts
feature/compliance-validation-scripts
release/v1.0.0
```

---

## Padrão de Branches

**Total**: 30 branches (5 por sprint)

**Convenção de Nomes**:
- `feature/<nome-descritivo>` - Novas funcionalidades
- `chore/<nome-descritivo>` - Tarefas de manutenção
- `release/v<versão>` - Preparação de release

**Regras**:
- Nomes em minúsculas com hífens
- Sem espaços ou caracteres especiais
- Descritivos e concisos
- Relacionados ao escopo da issue

**Fluxo de Branches**:
1. Criar branch a partir de `develop`
2. Desenvolver e fazer commits atômicos
3. Fazer push para remote
4. Abrir PR para `develop`
5. Após merge, deletar branch local e remote

---

## Hooks e Automação

### Hooks do Kiro

O projeto utiliza hooks do Kiro para automação de tarefas durante o desenvolvimento.

#### Hooks Implementados

| Hook | Evento | Ação | Propósito |
|------|--------|------|----------|
| **prompt-logger.json** | `promptSubmit` | `askAgent` | Registra prompts em logs por branch |
| **generate-tests.json** | `postToolUse` | `runCommand` | Gera testes para código novo |
| **generate-docs.json** | `postToolUse` | `runCommand` | Gera documentação para código novo |

#### Configuração de Hooks

Hooks são armazenados em `.kiro/hooks/` e seguem o schema:

```json
{
  "name": "Hook Name",
  "version": "1.0.0",
  "when": {
    "type": "promptSubmit|postToolUse|preToolUse|fileEdited|...",
    "patterns": ["*.ts", "*.py"],
    "toolTypes": ["write", "read", "*"]
  },
  "then": {
    "type": "askAgent|runCommand",
    "prompt": "Instruções para o agente",
    "command": "Comando a executar"
  }
}
```

#### Boas Práticas

- **Não bloquear execução** - Hooks devem ser rápidos e não impedir o fluxo
- **Tratamento de erros** - Sempre implementar fallback gracioso
- **Documentação** - Documentar propósito e comportamento de cada hook
- **Versionamento** - Manter versão do hook atualizada
- **Testes** - Testar hooks em diferentes cenários

---

## Workflows do GitHub Actions

### Estrutura de Workflows

O projeto utiliza GitHub Actions para CI/CD automático com os seguintes workflows (iniciados a partir do Sprint 1):

#### 1. CI - Lint & Tests (`ci.yml`) - Sprint 1+

**Trigger:** Push/PR em branches (develop, feature/*, bugfix/*, hotfix/*)

**Jobs:**
- `backend-lint` - Lint com flake8, black, isort
- `backend-tests` - Testes unitários com pytest + cobertura
- `frontend-lint` - Lint com ESLint
- `frontend-tests` - Testes com Vitest + cobertura
- `api-integration-tests` - Testes de integração com Postman/Newman
- `build-status` - Verificação final de status

**Saída:**
- Relatórios de cobertura no Codecov
- Status de build no GitHub
- Logs detalhados de cada job

#### 2. CD - Deploy (`cd.yml`) - Sprint 1+

**Trigger:** Push em main, tags v*, workflow_run do CI

**Jobs:**
- `deploy` - Build Docker, health checks, deploy

**Saída:**
- Deployment summary no GitHub
- Status de deploy

#### 3. Docs Generation (`docs-generation.yml`) - Sprint 5+

**Trigger:** Push em develop/main com mudanças em código

**Jobs:**
- Geração de API docs
- Análise de docstrings
- Commit automático de mudanças

**Saída:**
- Documentação atualizada
- Relatórios de cobertura de docs

#### 4. AI Test Generation (`ai-test-generation.yml`) - Sprint 4+

**Trigger:** Post-commit, análise de código novo

**Jobs:**
- Análise de código alterado
- Geração de testes com IA
- Validação de cobertura

**Saída:**
- Testes gerados automaticamente
- Relatórios de cobertura

### Fase 0 - Sem Workflows CI/CD

A Fase 0 (Setup de Gerenciamento) **não inclui workflows CI/CD**. Apenas estrutura e documentação são criadas.

**Workflows iniciados em:**
- **Sprint 1**: CI, CD
- **Sprint 4**: AI Test Generation
- **Sprint 5**: Docs Generation

### Configurações de Workflows

#### Backend (Python)

- **Lint**: flake8, black, isort
- **Testes**: pytest com coverage
- **Cobertura mínima**: 70%
- **Python**: 3.11+
- **Banco de dados**: PostgreSQL 15-alpine

#### Frontend (React/TypeScript)

- **Lint**: ESLint
- **Testes**: Vitest com coverage
- **Cobertura mínima**: 70%
- **Node.js**: 18+

### Monitoramento de Workflows

**Visualizar status:**
1. Acesse [GitHub Actions](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/actions)
2. Selecione o workflow desejado
3. Verifique status e logs

**Badges de status:**
```markdown
![CI](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/workflows/CI%20-%20Lint%20%26%20Tests/badge.svg)
![CD](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/workflows/CD%20-%20Deploy/badge.svg)
```

### Troubleshooting

**Workflow falhando:**
1. Verificar logs no GitHub Actions
2. Executar testes localmente
3. Verificar dependências
4. Consultar documentação de cada workflow

**Cobertura baixa:**
1. Executar `pytest --cov` localmente
2. Adicionar testes para código novo
3. Verificar relatórios no Codecov

---

```
Issue (com Sprint/Milestone)
    ↓
Create branch (feature/nome-da-issue)
    ↓
Develop (commits atômicos)
    ↓
Push para remote
    ↓
Pull Request (com Closes #N)
    ↓
Code Review (mínimo 1 aprovação)
    ↓
Merge into develop (squash merge)
    ↓
Issue fecha automaticamente
    ↓
Board atualiza automaticamente
```

---

## Labels Recomendados

Use os seguintes labels para categorizar issues e PRs:

| Label | Cor | Uso |
|---|---|---|
| `backend` | Azul | Alterações no backend Python/FastAPI |
| `frontend` | Verde | Alterações no frontend React |
| `ml` | Roxo | Alterações em machine learning |
| `database` | Laranja | Alterações no banco de dados |
| `api` | Azul escuro | Alterações na API REST |
| `testing` | Amarelo | Testes e cobertura |
| `documentation` | Cinza | Documentação |
| `bug` | Vermelho | Correção de bugs |
| `feat` | Ciano | Novas funcionalidades |
| `chore` | Cinza claro | Tarefas de manutenção |
| `sprint-1` | Verde | Issues do Sprint 1 |
| `sprint-2` | Azul | Issues do Sprint 2 |
| `sprint-3` | Roxo | Issues do Sprint 3 |
| `sprint-4` | Laranja | Issues do Sprint 4 |

---

## Master Checklist Issue - Entrega Final

### Visão Geral

A **Master Checklist Issue** é uma issue especial que permanece aberta durante todo o projeto e consolida todos os requisitos de entrega do projeto avaliativo. Ela serve como:

- **Rastreador central** de todos os requisitos de entrega
- **Ponto de referência** para verificar progresso geral
- **Documentação viva** do que foi entregue
- **Evidência de conformidade** com critérios de avaliação

### Criação Automática

A master checklist issue é criada automaticamente no início do projeto via GitHub Actions workflow:

**Arquivo**: `.github/workflows/create-delivery-checklist.yml`

**Trigger**: Manual (via workflow_dispatch) ou ao criar milestone "Entrega Final"

**Funcionalidades**:
- ✅ Cria issue com título "📋 Master Checklist - Entrega Final"
- ✅ Adiciona ao projeto "BiotecPredict Roadmap"
- ✅ Coloca na coluna "Backlog" (permanece aberta)
- ✅ Atribui milestone "Entrega Final"
- ✅ Inclui todos os requisitos de avaliação
- ✅ Mapeia requisitos contra implementação atual
- ✅ Identifica gaps (se houver)

### Estrutura da Master Checklist

A issue contém as seguintes seções:

#### 1. Apresentação (Video Delivery) - 10%
- [ ] Vídeo de apresentação gravado (máx 10 min)
- [ ] Demonstração de funcionalidades principais
- [ ] Explicação de arquitetura e decisões técnicas
- [ ] Análise crítica de uso de IA no projeto
- [ ] Vídeo hospedado (YouTube, Vimeo, ou GitHub)

#### 2. Uso do GitHub Board (Kanban) - 10%
- [ ] Board "BiotecPredict Roadmap" criado
- [ ] 6 colunas configuradas: Backlog, Sprint Ready, In Progress, Review, Done, Blocked
- [ ] Issues adicionadas ao board automaticamente
- [ ] Movimento automático de issues conforme status
- [ ] Milestones sincronizados com sprints
- [ ] Relatórios de progresso gerados semanalmente

#### 3. Uso do Repositório GitHub - 10%
- [ ] Branches seguem GitFlow (main, develop, feature/*, bugfix/*, hotfix/*)
- [ ] Commits seguem Conventional Commits
- [ ] Pull requests com templates preenchidos
- [ ] Mínimo 1 aprovação antes de merge
- [ ] Histórico limpo e rastreável
- [ ] Tags de versão criadas (v0.0.1-alpha, v0.1.0, etc)
- [ ] Issue templates criados e utilizados

#### 4. Desenvolvimento da Aplicação - 15%
- [ ] Funcionalidades principais implementadas (upload, compliance, ML)
- [ ] Arquitetura Clean Architecture implementada
- [ ] Separação de responsabilidades (processors, services, api)
- [ ] Pipeline ETL distribuído implementado (Extract→Transform→Load→Validate)
- [ ] Código gerado com suporte de IA (via Kiro)
- [ ] Docstrings em todas as funções
- [ ] README completo com instruções
- [ ] Modelos SQLAlchemy criados
- [ ] Schemas Pydantic criados
- [ ] API REST endpoints implementados

#### 5. Testes Automatizados - 15%
- [ ] Testes unitários (pytest backend, Vitest frontend)
- [ ] Testes de integração (Postman/Newman)
- [ ] Cobertura mínima 70% (backend + frontend)
- [ ] Testes gerados com IA (via Kiro)
- [ ] CI pipeline executando testes automaticamente
- [ ] Relatórios de cobertura no Codecov
- [ ] Testes passando sem warnings

#### 6. Documentação Técnica - 10%
- [ ] README.md completo
- [ ] Documentação de API (Swagger/OpenAPI)
- [ ] Guias de desenvolvimento
- [ ] Docstrings em código
- [ ] Documentação gerada automaticamente com IA
- [ ] Steering files com contexto permanente
- [ ] Diagramas de arquitetura (C4/UML)
- [ ] Documentação de deploy

#### 7. Pipeline CI/CD - 10%
- [ ] GitHub Actions workflows configurados (4 workflows)
- [ ] Lint automático (flake8, ESLint)
- [ ] Testes automáticos (pytest, Vitest)
- [ ] Deploy automático em main
- [ ] Relatórios de cobertura (Codecov)
- [ ] Workflows com suporte de IA (geração de testes, docs)
- [ ] Automação de projeto (project-automation.yml)
- [ ] Relatórios semanais (progress, velocity, metrics)

#### 8. Uso de IA no Desenvolvimento - 5%
- [ ] Kiro configurado como IDE
- [ ] Hooks de IA implementados (5 hooks)
- [ ] Geração de código com IA
- [ ] Geração de testes com IA
- [ ] Geração de documentação com IA

#### 9. Análise Crítica de IA - 5%
- [ ] Documento de análise crítica criado
- [ ] Avaliação de qualidade de código gerado por IA
- [ ] Identificação de limitações e melhorias
- [ ] Comparação: código manual vs gerado por IA
- [ ] Recomendações para uso futuro de IA

#### 10. Rastreabilidade de Prompts - 5%
- [ ] Sistema de prompt logging implementado
- [ ] Prompts capturados automaticamente (hook promptSubmit)
- [ ] Logs organizados por branch Git
- [ ] Timestamp em horário de Brasília
- [ ] Rastreabilidade completa de interações
- [ ] Arquivo `.kiro/prompt-logs/<branch>.md` por branch

#### 11. Validação e Qualidade de Dados - 5%
- [ ] Scripts de validação implementados
- [ ] Verificação de ranges de sensores
- [ ] Detecção de anomalias e outliers
- [ ] Relatórios de qualidade gerados
- [ ] Versionamento de relatórios
- [ ] Rastreabilidade para auditoria

### Critérios de Avaliação (11 Critérios Principais)

A master checklist mapeia os critérios de avaliação do projeto:

| # | Critério | Peso | Status | Evidência |
|---|----------|------|--------|-----------|
| 1 | Apresentação clara e objetiva | 10% | ⬜ | Vídeo no README |
| 2 | Uso correto do GitHub Board | 10% | ⬜ | Board com 6 colunas |
| 3 | Organização do repositório | 10% | ⬜ | GitFlow + Conventional Commits |
| 4 | Funcionalidades implementadas | 15% | ⬜ | Upload, Compliance, ML, ETL |
| 5 | Arquitetura e design | 10% | ⬜ | Clean Architecture + ETL distribuído |
| 6 | Testes automatizados | 15% | ⬜ | Cobertura ≥ 70% |
| 7 | Documentação técnica | 10% | ⬜ | README + API docs + Steering |
| 8 | Pipeline CI/CD | 10% | ⬜ | GitHub Actions workflows |
| 9 | Uso de IA no desenvolvimento | 5% | ⬜ | Kiro + hooks |
| 10 | Análise crítica de IA | 5% | ⬜ | Documento de análise |
| 11 | Rastreabilidade e qualidade | 10% | ⬜ | Prompts + Validação + Compliance |

### Atualização da Master Checklist

A master checklist é atualizada automaticamente:

1. **Ao completar uma issue**: Checkbox correspondente é marcado
2. **Ao fazer merge em main**: Status é atualizado
3. **Semanalmente**: Relatório de progresso é gerado
4. **Ao final do projeto**: Checklist é finalizada com score total

### Integração com Workflow

```
Issue criada (Master Checklist)
    ↓
Adicionada ao board "BiotecPredict Roadmap"
    ↓
Coluna "Backlog" (permanece aberta)
    ↓
Checkboxes marcados conforme progresso
    ↓
Relatórios semanais gerados
    ↓
Ao final: Score total calculado
```

### Criação Manual da Master Checklist

Se a automação não funcionar, criar manualmente:

1. Acesse [Issues > New Issue](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues/new)
2. Título: `📋 Master Checklist - Entrega Final`
3. Descrição: Copie a estrutura acima com todos os checkboxes
4. Labels: `checklist`, `entrega-final`, `rastreamento`
5. Milestone: `Entrega Final`
6. Assignee: Todos os colaboradores
7. Adicione ao projeto "BiotecPredict Roadmap" (coluna "Backlog")
8. Deixe aberta até o final do projeto

---

## Automação do GitHub Projects

O projeto utiliza GitHub Projects com automação completa para rastreamento de progresso, velocidade e métricas.

### Configuração do Board

**Projeto**: BiotecPredict  
**URL**: https://github.com/users/micheleoliveiracod/projects/7  
**Proprietário**: micheleoliveiracod  
**Tipo**: Table/Board

### Colunas do Board

| Coluna | Descrição | Status Automático |
|--------|-----------|------------------|
| **Todo** | Issues não iniciadas | Padrão para issues novas |
| **Sprint In Progress** | Issues em desenvolvimento | Quando PR é aberta |
| **In Review** | Issues em revisão | Quando PR está em review |
| **Done** | Issues completadas | Quando issue é fechada |

### Automação por Status

#### Trigger: Issue Aberta
```
Issue criada → Adicionada ao projeto → Coluna: Todo
```

#### Trigger: PR Aberta
```
PR aberta → Issue movida → Coluna: Sprint In Progress
```

#### Trigger: PR em Review
```
PR marcada como ready_for_review → Issue movida → Coluna: In Review
```

#### Trigger: Issue Fechada
```
Issue fechada → Issue movida → Coluna: Done
```

### Milestones para Sprints

| Milestone | Período | Sprint | Objetivo | Status | Workflows |
|-----------|---------|--------|----------|--------|-----------|
| **Fase 0 - Setup** | 24-27/05 | Pre-Sprint | Setup e documentação | ✅ Concluído | ❌ Nenhum |
| **Sprint 1 - Backend** | 27/05 | Sprint 1 | Backend + API + Modelos | 🔄 Em Progresso | ✅ CI, CD |
| **Sprint 2 - Frontend** | 28/05 | Sprint 2 | Frontend + Dashboard + Upload | ⏳ Próximo | ✅ CI, CD, E2E |
| **Sprint 3 - ML** | 29/05 | Sprint 3 | ML + Compliance + Predição | ⏳ Próximo | ✅ CI, CD, E2E |
| **Sprint 4 - Testes** | 30/05 | Sprint 4 | Testes + E2E + Cobertura | ⏳ Próximo | ✅ CI, CD, E2E, AI Test Gen |
| **Sprint 5 - Docs** | 31/05 | Sprint 5 | Documentação + Validação | ⏳ Próximo | ✅ CI, CD, E2E, Docs Gen, AI Test Gen |
| **Entrega Final** | 31/05 | Final | Apresentação + Deploy | ⏳ Próximo | ✅ CI, CD, E2E |

### Workflows de Automação

| Workflow | Trigger | Função | Status |
|----------|---------|--------|--------|
| **project-automation.yml** | Issue/PR events | Adiciona ao projeto, move conforme status | ✅ Ativo |
| **progress-report.yml** | Semanal (seg 9h UTC) | Gera relatório de progresso | ✅ Ativo |
| **velocity-analysis.yml** | Semanal (seg 10h UTC) | Analisa velocidade do time | ✅ Ativo |
| **metrics-dashboard.yml** | Semanal (seg 11h UTC) | Gera dashboard de métricas | ✅ Ativo |

### Configuração do Workflow project-automation.yml

**Localização**: `.github/workflows/project-automation.yml`

**Variáveis de Ambiente**:
```yaml
PROJECT_ID: 7
PROJECT_URL: https://github.com/users/micheleoliveiracod/projects/7
REPO_OWNER: micheleoliveiracod
REPO_NAME: BiotecPredict
```

**Triggers**:
- Issues: opened, reopened, closed
- Pull Requests: opened, reopened, closed, converted_to_draft, ready_for_review

**Ações**:
- Adiciona issues/PRs ao projeto automaticamente
- Move issues conforme status (Todo → Sprint In Progress → In Review → Done)
- Sincroniza milestones com projeto

### Relatórios Gerados

- `.kiro/reports/progress-YYYY-MM-DD.md` - Progresso semanal
- `.kiro/reports/velocity-YYYY-MM-DD.md` - Análise de velocidade
- `.kiro/reports/metrics-YYYY-MM-DD.md` - Dashboard de métricas

### Como Usar o Board

#### Criar Nova Issue

1. Ir para: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues
2. Clique em "New issue"
3. Selecione template (Feature, Bug, etc)
4. Preencha campos obrigatórios
5. Selecione milestone
6. Clique em "Submit new issue"
7. **Automático**: Issue será adicionada ao projeto na coluna "Todo"

#### Iniciar Desenvolvimento

1. Abra a issue
2. Crie feature branch: `git checkout -b feature/nome-da-issue`
3. Desenvolva
4. Faça commit: `git commit -m "feat: descrição"`
5. Faça push: `git push -u origin feature/nome-da-issue`
6. Abra PR
7. **Automático**: Issue será movida para "Sprint In Progress"

#### Solicitar Review

1. Marque PR como "Ready for review"
2. **Automático**: Issue será movida para "In Review"

#### Completar Issue

1. Aprove PR
2. Faça merge (squash merge)
3. **Automático**: Issue será fechada e movida para "Done"

### Links Importantes

- **Projeto**: https://github.com/users/micheleoliveiracod/projects/7
- **Repositório**: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
- **Issues**: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues
- **Milestones**: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/milestones
- **Workflows**: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/actions

---

**Versão**: 0.4.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ GitFlow + GitHub Projects + Master Checklist Completo

---

## 📌 Resumo Executivo - Fase 0

### Objetivo
Estabelecer a base de gerenciamento do projeto com estrutura, documentação e configurações.

### Escopo
- ✅ Estrutura de diretórios (.github/, .kiro/, scripts/)
- ✅ Templates de issues e PRs
- ✅ Steering files com documentação estratégica
- ✅ Scripts de setup e validação
- ✅ Documentação base (README, LICENSE, .gitattributes, .gitignore)
- ❌ Sem código de aplicação
- ❌ Sem workflows CI/CD ou E2E
- ❌ Sem testes
- ❌ Sem dependências

### Fluxo
1. Branch: `chore/setup-gerenciamento-projeto` (a partir de `main`)
2. Commits atômicos com Conventional Commits
3. Push para remote
4. **Merge manual em main** (sem PR automática)
5. Tag: `v0.0.1-alpha`
6. Sincronizar `develop` com `main`
7. Deletar branch

### Resultado
- Repositório pronto para Sprint 1
- Estrutura de gerenciamento estabelecida
- Documentação estratégica em `.kiro/steering/`
- Workflows CI/CD iniciados a partir do Sprint 1