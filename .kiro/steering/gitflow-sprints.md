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

**Versão**: 1.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ 30 Issues + 30 Branches Organizadas em 6 Sprints
