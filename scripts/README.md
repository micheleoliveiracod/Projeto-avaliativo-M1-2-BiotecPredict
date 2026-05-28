# Scripts de Automação - BiotecPredict

Este diretório contém scripts de automação para gerenciamento de issues e branches do projeto BiotecPredict.

## 📜 Scripts Disponíveis

### `create_all_issues.py` ⭐ **PRINCIPAL**

Script Python para criar automaticamente **30 issues + 6 milestones + 19 labels** no GitHub.

**Uso:**
```bash
python3 scripts/create_all_issues.py
```

**O que faz:**
- ✅ Cria 19 labels BiotecPredict-específicas (backend, frontend, ml, database, api, testing, documentation, etc.)
- ✅ Cria 6 milestones (Sprint 0-5)
- ✅ Cria 30 issues (5 por sprint) com:
  - Títulos em Conventional Commits
  - Labels apropriadas
  - Milestones associados
  - Descrições completas com escopo e critérios de aceite
  - Referências de branches GitFlow

**Estrutura de Issues:**
- **Sprint 0** (Issues 1-5): Setup e gerenciamento
- **Sprint 1** (Issues 6-10): Backend + API + Modelos
- **Sprint 2** (Issues 11-15): Frontend + Dashboard
- **Sprint 3** (Issues 16-20): ML + Compliance + Predição
- **Sprint 4** (Issues 21-25): Testes + Cobertura
- **Sprint 5** (Issues 26-30): Documentação + Validação + Deploy

---

### `create_branches.py` ⭐ **PRINCIPAL**

Script Python para criar automaticamente **30 branches** no GitHub (5 por sprint).

**Uso:**
```bash
python3 scripts/create_branches.py
```

**O que faz:**
- ✅ Verifica se Git está instalado
- ✅ Verifica se repositório local existe
- ✅ Cria 30 branches localmente a partir de `develop`
- ✅ Faz push de cada branch para repositório remoto
- ✅ Volta para `develop` após conclusão
- ✅ Fornece resumo detalhado de sucesso/falha

**Estrutura de Branches:**
- **Sprint 0**: `feature/project-structure`, `feature/database-setup`, `feature/fastapi-setup`, `feature/react-setup`, `chore/create-issues-milestones`
- **Sprint 1**: `feature/sqlalchemy-models`, `feature/pydantic-schemas`, `feature/upload-endpoint`, `feature/query-endpoints`, `feature/backend-unit-tests`
- **Sprint 2**: `feature/home-upload-page`, `feature/dashboard-kpis`, `feature/batch-table`, `feature/api-integration`, `feature/frontend-e2e-tests`
- **Sprint 3**: `feature/compliance-score-engine`, `feature/ml-pipeline-randomforest`, `feature/model-training`, `feature/ml-analytics-page`, `feature/ml-tests`
- **Sprint 4**: `feature/backend-pytest-coverage`, `feature/frontend-vitest-coverage`, `feature/postman-integration-tests`, `feature/cypress-e2e-tests`, `feature/coverage-validation`
- **Sprint 5**: `feature/swagger-documentation`, `feature/dev-guides`, `feature/data-validation-scripts`, `feature/compliance-validation-scripts`, `release/v1.0.0`

---

## 🔧 Pré-requisitos

### Obrigatório
- **GitHub CLI (`gh`)** instalado e autenticado
- **Python 3.8+**
- **Git** instalado

### Instalação do GitHub CLI

**Windows (PowerShell):**
```powershell
choco install gh
# ou
winget install GitHub.cli
```

**macOS:**
```bash
brew install gh
```

**Linux (Debian/Ubuntu):**
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

---

## 🚀 Como Usar

### Passo 1: Criar Issues e Milestones

```bash
cd scripts/
python3 create_all_issues.py
```

**Resultado esperado:**
- 19 labels criadas
- 6 milestones criados
- 30 issues criadas com labels e milestones

### Passo 2: Criar Branches

```bash
cd scripts/
python3 create_branches.py
```

**Resultado esperado:**
- 30 branches criadas localmente
- 30 branches enviadas para repositório remoto
- Volta automática para branch `develop`

---

## 📋 Convenções Seguidas

**GitFlow:**
- ✅ `feature/<nome>` - Novas funcionalidades
- ✅ `chore/<nome>` - Tarefas de manutenção
- ✅ `release/v<versão>` - Preparação de release

**Labels (conforme gitflow.md):**
- ✅ backend, frontend, ml, database, api, testing, documentation
- ✅ bug, feat, chore, setup, business-logic, validation
- ✅ sprint-0, sprint-1, sprint-2, sprint-3, sprint-4, sprint-5

**Issues:**
- ✅ Título em Conventional Commits
- ✅ Labels apropriadas por sprint e tipo
- ✅ Milestones associados
- ✅ Descrição com contexto, escopo e critérios de aceite
- ✅ Referência de branch GitFlow

---

## 📚 Referências

- `.kiro/steering/gitflow.md` - Convenções de GitFlow
- `.kiro/steering/gitflow-sprints.md` - Organização de sprints e branches
- `.kiro/steering/structure.md` - Estrutura do projeto
- `.kiro/steering/tech.md` - Stack tecnológica

---

## ✅ Checklist de Execução

- [ ] GitHub CLI instalado e autenticado
- [ ] Python 3.8+ instalado
- [ ] Git instalado
- [ ] Repositório local clonado
- [ ] Executar `python3 create_all_issues.py`
- [ ] Verificar issues no GitHub
- [ ] Executar `python3 create_branches.py`
- [ ] Verificar branches no GitHub
- [ ] Iniciar Sprint 0

---

**Versão**: 2.0.0  
**Projeto**: BiotecPredict  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Atualizado para BiotecPredict
