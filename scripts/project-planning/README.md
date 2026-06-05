# Scripts de Automação - BiotecPredict

Automação de criação de issues, branches, labels e gerenciamento do GitHub Project Board para o projeto avaliativo BiotecPredict.

**Projeto**: Plataforma de Manufatura Preditiva com Machine Learning  
**Stack**: Python (FastAPI) + React (TypeScript) + PostgreSQL  
**Período**: 24/05/2026 - 31/05/2026 (8 dias)  
**Total de Issues**: 34 (30 Sprints + 4 Fases Adicionais)  
**Total de Branches**: 30 (5 por sprint)  
**Total de Milestones**: 10 (6 Sprints + 4 Fases)

---

## 📋 Scripts Disponíveis

### 1. `create_all_issues.py` ⭐ **PRINCIPAL**

**Propósito**: Criar automaticamente **19 labels + 10 milestones + 34 issues** no GitHub

**Uso**:
```bash
python3 create_all_issues.py
```

**O que faz**:
- ✅ Cria 19 labels (backend, frontend, ml, database, api, testing, documentation, etc.)
- ✅ Cria 10 milestones (Sprint 0-5 + 4 Fases Adicionais)
- ✅ Cria 34 issues (5 por sprint + 4 fases) com:
  - Títulos em Conventional Commits
  - Labels apropriadas
  - Milestones associados
  - Descrições completas com escopo e critérios de aceite
  - Referências de branches GitFlow

**Estrutura de Issues**:
- **Sprint 0** (Issues 1-5): Setup e gerenciamento
- **Sprint 1** (Issues 6-10): Backend + API + Modelos
- **Sprint 2** (Issues 11-15): Frontend + Dashboard
- **Sprint 3** (Issues 16-20): ML + Compliance + Predição
- **Sprint 4** (Issues 21-25): Testes + Cobertura
- **Sprint 5** (Issues 26-30): Documentação + Validação + Deploy
- **Fase 6** (Issue 31): Entrega Final e Apresentação
- **Fase 7** (Issue 32): Validação de Dados
- **Fase 8** (Issue 33): Prompt Logging
- **Fase 9** (Issue 34): CI/CD com IA

---

### 2. `create_branches.py` ⭐ **PRINCIPAL**

**Propósito**: Criar automaticamente **30 branches** no GitHub (5 por sprint)

**Uso**:
```bash
python3 create_branches.py
```

**O que faz**:
- ✅ Verifica se Git está instalado
- ✅ Verifica se repositório local existe
- ✅ Cria 30 branches localmente a partir de `develop`
- ✅ Faz push de cada branch para repositório remoto
- ✅ Volta para `develop` após conclusão
- ✅ Fornece resumo detalhado de sucesso/falha

**Estrutura de Branches**:

#### Sprint 0 - Setup e Gerenciamento
```
feature/project-structure
feature/database-setup
feature/fastapi-setup
feature/react-setup
chore/create-issues-milestones
```

#### Sprint 1 - Backend + API + Modelos
```
feature/sqlalchemy-models
feature/pydantic-schemas
feature/upload-endpoint
feature/query-endpoints
feature/backend-unit-tests
```

#### Sprint 2 - Frontend + Dashboard
```
feature/home-upload-page
feature/dashboard-kpis
feature/batch-table
feature/api-integration
feature/frontend-e2e-tests
```

#### Sprint 3 - ML + Compliance + Predição
```
feature/compliance-score-engine
feature/ml-pipeline-randomforest
feature/model-training
feature/ml-analytics-page
feature/ml-tests
```

#### Sprint 4 - Testes + Cobertura
```
feature/backend-pytest-coverage
feature/frontend-vitest-coverage
feature/postman-integration-tests
feature/cypress-e2e-tests
feature/coverage-validation
```

#### Sprint 5 - Documentação + Validação + Deploy
```
feature/swagger-documentation
feature/dev-guides
feature/data-validation-scripts
feature/compliance-validation-scripts
release/v1.0.0
```

---

### 3. `add_issues_to_project.py`

**Propósito**: Adicionar issues ao GitHub Project Board automaticamente

**Uso**:
```bash
python3 add_issues_to_project.py
```

**O que faz**:
- ✅ Conecta ao GitHub Project "BiotecPredict Roadmap"
- ✅ Adiciona todas as 34 issues ao projeto
- ✅ Posiciona issues na coluna "Backlog"
- ✅ Sincroniza milestones com projeto

---

### 4. `manage_project.py`

**Propósito**: Gerenciar automação do GitHub Project Board (mover issues conforme status)

**Uso**:
```bash
python3 manage_project.py
```

**O que faz**:
- ✅ Monitora mudanças de status de issues
- ✅ Move issues automaticamente entre colunas:
  - Backlog → Sprint In Progress (quando PR é aberta)
  - Sprint In Progress → In Review (quando PR está em review)
  - In Review → Done (quando issue é fechada)
- ✅ Sincroniza milestones com projeto

---

### 5. `create_sprint0_issues.py`

**Propósito**: Criar apenas as 5 issues do Sprint 0 (setup e gerenciamento)

**Uso**:
```bash
python3 create_sprint0_issues.py
```

**O que faz**:
- ✅ Cria 5 issues específicas do Sprint 0
- ✅ Cria milestone "Sprint 0 - Setup"
- ✅ Útil para iniciar o projeto incrementalmente

---

### 6. `create_missing.py`

**Propósito**: Criar apenas issues/branches/milestones que estão faltando

**Uso**:
```bash
python3 create_missing.py
```

**O que faz**:
- ✅ Verifica quais issues já existem no GitHub
- ✅ Cria apenas as que estão faltando
- ✅ Evita duplicação
- ✅ Útil para recuperação após falhas

---

### 7. `configure_automation.py` ⭐ **NOVO**

**Propósito**: Configurar automação completa entre Issues, Branches, Milestones e GitHub Project Board

**Uso**:
```bash
python3 configure_automation.py
```

**O que faz**:
- ✅ Relaciona automaticamente cada issue com sua branch correspondente
- ✅ Atualiza milestones de todas as issues
- ✅ Cria branches localmente (se não existirem)
- ✅ Faz push de branches para remote
- ✅ Adiciona issues ao GitHub Project Board
- ✅ Verifica configuração final
- ✅ Mostra status das branches locais
- ✅ Exibe status do GitHub Project

**Menu Interativo**:
1. Configurar automação para TODAS as issues
2. Verificar configuração atual
3. Ver status das branches locais
4. Ver status do GitHub Project
5. Abrir projeto no navegador

**Mapeamento Automático**:
- Issue #1 → `feature/project-structure` → Sprint 0 - Setup
- Issue #2 → `feature/database-setup` → Sprint 0 - Setup
- ... (30 issues mapeadas)
- Issue #30 → `release/v1.0.0` → Sprint 5 - Documentação

**Exemplo de Uso**:
```bash
# Executar script
python3 configure_automation.py

# Selecionar opção 1 para configurar todas as issues
# Confirmar com 's'
# Aguardar conclusão (~2-3 minutos)
# Verificar com opção 2
```

---

### 8. `sync_board_status.py` ⭐ **NOVO**

**Propósito**: Sincronizar status das issues com o GitHub Project Board automaticamente

**Uso**:
```bash
python3 sync_board_status.py
```

**O que faz**:
- ✅ Determina status de cada issue baseado em seu estado e PRs
- ✅ Move issues automaticamente entre colunas do board:
  - **Todo**: Issues não iniciadas (sem PR)
  - **Sprint In Progress**: Issues em desenvolvimento (PR aberta)
  - **In Review**: Issues em revisão (PR em review)
  - **Done**: Issues completadas (fechadas)
- ✅ Gera relatório de progresso do projeto
- ✅ Mostra distribuição de issues por status
- ✅ Exibe progresso por sprint

**Menu Interativo**:
1. Sincronizar status de TODAS as issues
2. Ver status atual do board
3. Gerar relatório de progresso
4. Abrir projeto no navegador

**Relatório de Progresso**:
- Estatísticas gerais (total, abertas, fechadas, taxa de conclusão)
- Progresso por sprint (com barra visual)
- Distribuição de issues por status
- Detalhes por sprint

**Exemplo de Uso**:
```bash
# Executar script
python3 sync_board_status.py

# Selecionar opção 2 para ver status atual
# Visualizar distribuição de issues
# Selecionar opção 3 para gerar relatório
```

---

## 🔧 Pré-requisitos

### Obrigatório
- **GitHub CLI (`gh`)** instalado e autenticado
- **Python 3.8+**
- **Git** instalado
- **Variáveis de ambiente** configuradas

### Instalação do GitHub CLI

**Windows (PowerShell)**:
```powershell
choco install gh
# ou
winget install GitHub.cli
```

**macOS**:
```bash
brew install gh
```

**Linux (Debian/Ubuntu)**:
```bash
sudo apt install gh
```

### Autenticação

```bash
gh auth login
# Selecionar: GitHub.com
# Selecionar: HTTPS
# Autenticar com navegador
```

### Variáveis de Ambiente

Criar arquivo `.env` na pasta `project-planning/`:

```env
GITHUB_TOKEN=seu_token_aqui
GITHUB_REPO=micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
GITHUB_PROJECT_ID=7
```

**Gerar GitHub Token**:
1. Acesse https://github.com/settings/tokens
2. Clique em "Generate new token"
3. Selecione escopos: `repo`, `project`
4. Copie o token e adicione ao `.env`

---

## 🚀 Fluxo de Execução Recomendado

### Opção 1: Execução Completa (Recomendado) ⭐

```bash
# Passo 1: Criar issues e milestones
python3 create_all_issues.py

# Passo 2: Criar branches
python3 create_branches.py

# Passo 3: Configurar automação (NOVO)
python3 configure_automation.py
# Selecionar opção 1 para configurar todas as issues

# Passo 4: Sincronizar status do board (NOVO)
python3 sync_board_status.py
# Selecionar opção 2 para ver status atual
# Selecionar opção 3 para gerar relatório
```

**Tempo total**: ~5-10 minutos

**Resultado**:
- ✅ 34 issues criadas e relacionadas com branches
- ✅ 30 branches criadas localmente e no remote
- ✅ Todos os milestones configurados
- ✅ Todas as issues adicionadas ao project board
- ✅ Automação de status do board funcionando
- ✅ Relatório de progresso gerado

### Opção 2: Execução Incremental (Para Testes)

```bash
# Passo 1: Criar apenas Sprint 0
python3 create_sprint0_issues.py

# Passo 2: Testar e validar
# ... fazer testes ...

# Passo 3: Criar issues faltantes
python3 create_missing.py

# Passo 4: Criar branches
python3 create_branches.py

# Passo 5: Configurar automação
python3 configure_automation.py

# Passo 6: Sincronizar status
python3 sync_board_status.py
```

### Opção 3: Recuperação (Se Algo Falhar)

```bash
# Criar apenas o que está faltando
python3 create_missing.py

# Recriar branches
python3 create_branches.py

# Configurar automação
python3 configure_automation.py

# Sincronizar status
python3 sync_board_status.py
```

### Opção 4: Apenas Automação (Se Issues e Branches Já Existem)

```bash
# Configurar automação para issues existentes
python3 configure_automation.py
# Selecionar opção 1

# Sincronizar status do board
python3 sync_board_status.py
# Selecionar opção 1
```

---

## 📊 Convenções Seguidas

### GitFlow
- ✅ `feature/<nome>` - Novas funcionalidades
- ✅ `chore/<nome>` - Tarefas de manutenção
- ✅ `release/v<versão>` - Preparação de release
- ✅ `bugfix/<nome>` - Correção de bugs
- ✅ `hotfix/<nome>` - Correção urgente

### Labels (19 Total)
**Área de Desenvolvimento**:
- `backend` - Alterações no backend Python/FastAPI
- `frontend` - Alterações no frontend React
- `ml` - Alterações em machine learning
- `database` - Alterações no banco de dados
- `api` - Alterações na API REST

**Tipo de Trabalho**:
- `testing` - Testes e cobertura
- `documentation` - Documentação
- `bug` - Correção de bugs
- `feat` - Novas funcionalidades
- `chore` - Tarefas de manutenção
- `refactor` - Refatoração de código
- `style` - Formatação e estilo
- `perf` - Melhoria de performance

**Sprints**:
- `sprint-1`, `sprint-2`, `sprint-3`, `sprint-4`, `sprint-5`

**Adicionais**:
- `setup` - Setup e configuração
- `ci` - CI/CD e automação
- `entrega-final` - Requisitos de entrega final
- `rastreamento` - Rastreamento de progresso

### Issues
- ✅ Título em Conventional Commits
- ✅ Labels apropriadas por sprint e tipo
- ✅ Milestones associados
- ✅ Descrição com contexto, escopo e critérios de aceite
- ✅ Referência de branch GitFlow

### Commits
- ✅ Formato: `<tipo>(<escopo>): <descrição>`
- ✅ Tipos: feat, fix, docs, chore, refactor, test, style, perf, ci
- ✅ Descrição no imperativo e em minúsculas
- ✅ Sem ponto final

---

## 📈 Estrutura de Sprints

| Sprint | Período | Foco | Issues | Status |
|--------|---------|------|--------|--------|
| **Sprint 0** | 24-26/05 | Setup e Gerenciamento | 5 | ✅ Documentado |
| **Sprint 1** | 27/05 | Backend + API + Modelos | 5 | ✅ Documentado |
| **Sprint 2** | 28/05 | Frontend + Dashboard | 5 | ✅ Documentado |
| **Sprint 3** | 29/05 | ML + Compliance + Predição | 5 | ✅ Documentado |
| **Sprint 4** | 30/05 | Testes + Cobertura | 5 | ✅ Documentado |
| **Sprint 5** | 31/05 | Documentação + Validação + Deploy | 5 | ✅ Documentado |
| **Fase 6** | 01/06 | Entrega Final | 1 | ✅ NOVO |
| **Fase 7** | Paralelo | Validação de Dados | 1 | ✅ NOVO |
| **Fase 8** | Paralelo | Prompt Logging | 1 | ✅ NOVO |
| **Fase 9** | Paralelo | CI/CD com IA | 1 | ✅ NOVO |

---

## 🎯 Requisitos de Entrega (9 Critérios)

O projeto deve atender aos seguintes critérios de avaliação:

1. **Apresentação** (10%) - Vídeo de apresentação (máx 10 min)
2. **GitHub Board** (10%) - Kanban com automação completa
3. **Repositório** (10%) - GitFlow + Conventional Commits
4. **Desenvolvimento** (15%) - Funcionalidades implementadas
5. **Testes** (15%) - Cobertura ≥ 70%
6. **Documentação** (10%) - README + API docs + Steering
7. **CI/CD** (10%) - GitHub Actions workflows
8. **Uso de IA** (5%) - Kiro + hooks
9. **Análise Crítica** (5%) - Documento de análise de IA

---

## 📚 Referências

### Documentação do Projeto
- `.kiro/steering/gitflow.md` - Convenções de GitFlow
- `.kiro/steering/gitflow-sprints.md` - Organização de sprints e branches
- `.kiro/steering/structure.md` - Estrutura do projeto
- `.kiro/steering/tech.md` - Stack tecnológica
- `.kiro/steering/requirements.md` - Requisitos funcionais
- `.kiro/steering/product.md` - Visão do produto
- `.kiro/steering/ci-cd.md` - Workflows GitHub Actions
- `.kiro/steering/deploy.md` - Deploy com Docker Compose
- `.kiro/steering/compliance.md` - Compliance e rastreabilidade
- `.kiro/steering/localizacao.md` - Timezone e idioma

### Documentação Externa
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitFlow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

---

## ✅ Checklist de Execução

### Pré-requisitos
- [ ] GitHub CLI instalado e autenticado
- [ ] Python 3.8+ instalado
- [ ] Git instalado
- [ ] Repositório local clonado
- [ ] Arquivo `.env` criado com GitHub token

### Execução Completa (Recomendado)
- [ ] Executar `python3 create_all_issues.py`
- [ ] Verificar 34 issues criadas no GitHub
- [ ] Verificar 10 milestones criados
- [ ] Verificar 19 labels criados
- [ ] Executar `python3 create_branches.py`
- [ ] Verificar 30 branches criadas no GitHub
- [ ] Executar `python3 configure_automation.py` (NOVO)
- [ ] Selecionar opção 1 para configurar todas as issues
- [ ] Verificar relacionamento issue-branch-milestone
- [ ] Executar `python3 sync_board_status.py` (NOVO)
- [ ] Selecionar opção 2 para ver status do board
- [ ] Selecionar opção 3 para gerar relatório

### Validação
- [ ] Todas as 34 issues visíveis no GitHub
- [ ] Todas as 30 branches visíveis no GitHub
- [ ] Todas as issues com milestone correto
- [ ] Todas as issues com branch correspondente
- [ ] Project board "BiotecPredict Roadmap" com 6 colunas
- [ ] Automação de movimento de issues funcionando
- [ ] Milestones sincronizados com sprints
- [ ] Labels aplicadas corretamente
- [ ] Relatório de progresso gerado

### Início do Projeto
- [ ] Sprint 0 iniciado
- [ ] Primeira issue atribuída
- [ ] Primeira branch criada localmente
- [ ] Primeiro commit feito
- [ ] Primeira PR aberta

---

## 🔍 Troubleshooting

### GitHub CLI não encontrado
```bash
# Verificar instalação
gh --version

# Se não estiver instalado, instalar:
# Windows: choco install gh
# macOS: brew install gh
# Linux: sudo apt install gh
```

### Erro de autenticação
```bash
# Fazer login novamente
gh auth login

# Verificar token
gh auth status
```

### Erro ao criar issues
```bash
# Verificar se repositório está correto
gh repo view

# Verificar se projeto existe
gh project list
```

### Branches não aparecem no GitHub
```bash
# Verificar se push foi bem-sucedido
git branch -a

# Fazer push manual se necessário
git push -u origin <branch-name>
```

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verificar logs dos scripts
2. Consultar documentação em `.kiro/steering/`
3. Verificar status do GitHub Actions
4. Consultar issues abertas no repositório

---

**Versão**: 3.0.0  
**Projeto**: BiotecPredict - Plataforma de Manufatura Preditiva  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Atualizado com 34 Issues + 10 Milestones + 30 Branches  
**Período**: 24/05/2026 - 31/05/2026 (8 dias)  
**Stack**: Python (FastAPI) + React (TypeScript) + PostgreSQL  
**Avaliação**: 9 Critérios de Entrega
