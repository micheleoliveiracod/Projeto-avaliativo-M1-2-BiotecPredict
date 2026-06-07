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
feature/geracao-codigo-ia
feature/refatoracao-ia
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

## Fluxo de Pull Request (PR)

### Fluxo Esperado (ATUALIZADO)

O fluxo de PR segue o padrão GitFlow com validação automática via CI/CD assim que a PR é aberta (não espera aprovação — feedback chega antes da revisão):

```
1. Criar branch de trabalho
   ↓
   feature/*, bugfix/*, hotfix/*
   ↓
2. Fazer commits e push
   ↓
   ❌ CI NÃO dispara no push da branch de trabalho
   ↓
3. Abrir PR para develop
   ↓
   ✅ CI dispara: Lint + Testes (ao abrir e a cada novo commit na PR)
   ↓
4. Code review + aprovação (mínimo 1)
   ↓
   CI já validou a PR — revisor vê o status antes de aprovar
   ↓
5. Testes devem passar ANTES do merge
   ↓
6. Merge em develop (squash merge)
   ↓
   ✅ CI dispara novamente: Lint + Testes (push em develop, valida o estado integrado)
   ↓
   Automação: Issue movida para "Done"
   ↓
7. Sincronizar develop com main
   ↓
   PR de develop → main
   ↓
   ❌ CI NÃO dispara (workflow ci.yml mira apenas develop)
   ↓
8. Merge em main (merge commit)
   ↓
   CD dispara: Deploy em produção
```

### Passo a Passo Prático

#### 1. Criar Branch de Trabalho

```bash
# Atualizar develop
git checkout develop
git pull origin develop

# Criar branch de trabalho
git checkout -b feature/nome-da-funcionalidade
```

#### 2. Desenvolver e Fazer Commits

```bash
# Fazer alterações
# ...

# Fazer commit com Conventional Commits
git add .
git commit -m "feat(backend): implementa modelos SQLAlchemy"
```

#### 3. Push para Remote

```bash
# Push da branch
git push -u origin feature/nome-da-funcionalidade

# ⚠️ CI NÃO dispara aqui! (dispara ao abrir a PR para develop)
```

#### 4. Abrir Pull Request

```bash
# Via GitHub CLI
gh pr create --base develop --title "feat(backend): implementa modelos SQLAlchemy"

# Via GitHub Web
# 1. Acesse o repositório
# 2. Clique em "Pull requests"
# 3. Clique em "New pull request"
# 4. Selecione: base=develop, compare=feature/nome-da-funcionalidade
# 5. Preencha o template de PR
```

#### 5. Preencher Template de PR

O template em `.github/pull_request_template.md` contém:

- **Contexto** - Por que a mudança é necessária
- **O que foi feito** - Descrição das alterações
- **Como testar** - Passos para validação
- **Dependências** - Issues relacionadas (Closes #N)
- **Referências** - Links para documentação
- **Checklist** - Itens de verificação

#### 6. Code Review

- CI já disparou ao abrir a PR — verificar se Lint + Testes passaram antes de pedir revisão
- Aguardar aprovação de pelo menos 1 revisor
- Resolver comentários de review
- Fazer commits adicionais se necessário (CI roda novamente a cada novo commit na PR)

#### 7. Merge em Develop

```bash
# Via GitHub CLI (squash merge)
gh pr merge <PR_NUMBER> --squash --delete-branch

# Via GitHub Web
# 1. Clique em "Squash and merge"
# 2. Confirme o merge
# 3. Clique em "Delete branch"

# ⚠️ Automação dispara: Issue movida para "Done"
```

#### 8. Sincronizar Main

```bash
# Atualizar develop
git checkout develop
git pull origin develop

# Criar PR de develop → main
gh pr create --base main --title "chore: merge develop para main"

# ⚠️ CI NÃO dispara (código já foi testado)
```

#### 9. Merge em Main

```bash
# Via GitHub CLI (merge commit)
gh pr merge <PR_NUMBER> --merge --delete-branch

# Via GitHub Web
# 1. Clique em "Merge pull request"
# 2. Confirme o merge
# 3. Clique em "Delete branch"

# ⚠️ CD dispara: Deploy em produção
```

### Merge Strategy

| Tipo de branch | Destino | Estratégia | Justificativa |
|---|---|---|---|
| `feature/*`, `bugfix/*`, `chore/*`, `docs/*` | `develop` | Squash merge | Consolida commits em um único commit limpo |
| `hotfix/*` | `main` e `develop` | Merge commit | Preserva contexto da correção urgente |
| `release/*` | `main` | Merge commit | Mantém rastreabilidade da release |

**Regras:**
- Squash merge: consolida todos os commits da branch em um único commit
- Merge commit: preserva histórico de commits da branch
- Sempre deletar branch após merge

---

## Política de CI/CD por Tipo de Branch

O workflow `ci.yml` é direcionado à branch `develop` — ele dispara em **PRs com destino `develop`** (de qualquer branch de trabalho) e em **push direto em `develop`** (após o merge). Branches de trabalho (`feature/*`, `bugfix/*`, `hotfix/*`) não disparam CI sozinhas — o CI roda quando elas abrem PR para `develop`.

### ✅ Cobertas pelo Pipeline Completo (Lint + Unit + Integration)

- `feature/*`, `bugfix/*`, `hotfix/*` — via PR aberta para `develop`
- `develop` — via push direto (após merge, valida o estado integrado)

**Quando dispara:**
- Ao abrir ou atualizar uma PR com destino `develop` (`opened`, `synchronize`, `reopened`) — não espera aprovação, feedback chega antes da revisão
- Ao dar push em `develop` (após o merge da PR)
- Testes devem passar ANTES do merge ser permitido (branch protection)

### ❌ Sem CI/CD de Testes

- `main` - Produção (workflow `ci.yml` mira apenas `develop`; recebe só código já validado)
- `chore/*`, `docs/*` - Gerenciamento/configuração e documentação pura
- `release/*` - Apenas lint (workflow `release-lint.yml`, sem testes)
- Push direto em `feature/*`, `bugfix/*`, `hotfix/*` (sem PR aberta)

**Justificativa:**
- Feedback rápido: o autor vê o resultado do CI assim que abre/atualiza a PR, antes mesmo da revisão
- Sem ruído: push isolado na branch de trabalho não dispara (evita rodar CI a cada commit local)
- Validação dupla em `develop`: a PR garante antes do merge, o push confirma o estado integrado
- Sprint 0: sem testes (apenas setup)

### Matriz de Triggers (ATUALIZADA)

| Trigger | Ação | Status |
|---------|------|--------|
| Push em `feature/*`, `bugfix/*`, `hotfix/*` | Nenhum | ❌ Não dispara |
| PR aberta/atualizada → `develop` (de qualquer branch) | Lint + Testes | ✅ Dispara |
| Push em `develop` | Lint + Testes | ✅ Dispara |
| PR `develop` → `main` | Nenhum (workflow mira só `develop`) | ❌ Não dispara |
| Push em `main` | Deploy (CD) | ✅ Dispara |
| Push em `release/*` | Lint only (`release-lint.yml`) | ⚠️ Dispara (sem testes) |
| Push em `chore/*`, `docs/*` | Nenhum | ❌ Não dispara |
| Tags `v*` | Deploy | ✅ Dispara |
| Workflow_run (CI sucesso) | Deploy | ✅ Dispara |

---

## Automações do GitHub

### 1. CI - Lint & Tests (`.github/workflows/ci.yml`)

**Objetivo:** Validar qualidade de código e testes

**Triggers (ATUALIZADO):**
- `pull_request` com destino `develop` — dispara em `opened`, `synchronize`, `reopened` (ao abrir e a cada novo commit na PR; não espera aprovação)
- `push` em `develop` — dispara após o merge, validando o estado integrado
- **Exclusões (paths-ignore) em ambos os gatilhos:**
  - `docs/**` - Documentação pura
  - `.specs/**` - Especificações e contexto do projeto
  - `.github/issue_template/**` - Templates de issues
  - `*.md` - Arquivos markdown

**Jobs:**
- `backend-lint` - Lint com flake8, black, isort
- `backend-tests` - Testes unitários com pytest + cobertura
- `frontend-lint` - Lint com ESLint
- `frontend-tests` - Testes com Vitest + cobertura
- `api-integration-tests` - Testes de integração com Postman/Newman
- `build-status` - Verificação final de status

**Tempo estimado:** 5-10 minutos

**Nota Importante:**
- ✅ Testes disparam ao abrir/atualizar a PR para `develop` — feedback chega antes da revisão
- ✅ Testes disparam novamente após o merge (push em `develop`)
- ✅ Testes devem passar ANTES do merge ser permitido
- ❌ Testes NÃO disparam em push direto nas branches de trabalho (`feature/*`, `bugfix/*`, `hotfix/*`)
- ❌ Testes NÃO disparam em `main`, `release/*`, `chore/*`, `docs/*` (workflow mira apenas `develop`)

### 2. CD - Deploy (`.github/workflows/cd.yml`)

**Objetivo:** Deploy automático em produção

**Triggers:**
- Push em `main`
- Tags `v*`
- Workflow_run (CI sucesso)

**Jobs:**
- Build Docker images
- Run health checks
- Create deployment summary

**Tempo estimado:** 2-3 minutos

### 3. Project Automation (`.github/workflows/project-automation.yml`)

**Objetivo:** Manter board do projeto atualizado

**Triggers:**
- Issues: opened, reopened, closed
- Pull requests: opened, reopened, closed, converted_to_draft, ready_for_review

**Ações:**
- Adiciona issues/PRs ao projeto automaticamente
- Move issues conforme status (Todo → Sprint In Progress → In Review → Done)
- Sincroniza milestones com projeto

**Tempo estimado:** < 1 minuto

---

## Branch Protection Rules (Recomendado)

### Para branch `develop`

```
✅ Require pull request reviews before merging
   - Require 1 approval
   - Dismiss stale pull request approvals when new commits are pushed

✅ Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Status checks required:
     - backend-lint
     - backend-tests
     - frontend-lint
     - frontend-tests
     - api-integration-tests
     - build-status

✅ Require branches to be up to date before merging

✅ Require conversation resolution before merging
```

### Para branch `main`

```
✅ Require pull request reviews before merging
   - Require 2 approvals (mais rigoroso para produção)
   - Dismiss stale pull request approvals when new commits are pushed

✅ Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Status checks required:
     - backend-lint
     - backend-tests
     - frontend-lint
     - frontend-tests
     - api-integration-tests
     - build-status

✅ Require branches to be up to date before merging

✅ Require conversation resolution before merging

✅ Require signed commits (recomendado para produção)

✅ Restrict who can push to matching branches (apenas admin)
```

---

## Checklist de PR (ATUALIZADO)

Antes de abrir um PR, verifique:

- [ ] Branch criada a partir de `develop` atualizada
- [ ] Código testado localmente
- [ ] Testes unitários adicionados (quando aplicável)
- [ ] Documentação atualizada (quando aplicável)
- [ ] Commits seguem Conventional Commits
- [ ] Sem conflitos com `develop`
- [ ] Template de PR preenchido completamente
- [ ] Pelo menos 1 revisor atribuído

**Após aprovação do PR:**
- [ ] CI passou com sucesso (Lint + Testes)
- [ ] Nenhum warning ou erro no CI
- [ ] Pronto para merge

---

## Troubleshooting

### CI Falhou

**Problema:** CI falhou no push

**Solução:**
1. Verificar logs no GitHub Actions
2. Executar testes localmente
3. Corrigir erros
4. Fazer novo commit e push
5. CI dispara novamente

### Conflito com Develop

**Problema:** PR tem conflitos com `develop`

**Solução:**
```bash
# Atualizar develop
git fetch origin
git rebase origin/develop

# Resolver conflitos
# ...

# Fazer push com force (cuidado!)
git push -f origin feature/nome-da-feature
```

### PR Não Pode Ser Mergeada

**Problema:** Botão de merge está desabilitado

**Possíveis causas:**
- CI não passou
- Conflitos com branch de destino
- Falta de aprovação
- Branch protection rules

**Solução:**
1. Verificar CI status
2. Resolver conflitos
3. Solicitar aprovação
4. Aguardar branch protection rules

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

| Tipo de branch | Destino | Estratégia | CI/CD | Validação |
|---|---|---|---|---|
| `feature/especificacao-arquitetura` (Sprint 0) | `develop` | Squash merge | ⚠️ Lint/setup | ✅ PR valida |
| `feature/*`, `bugfix/*` | `develop` | Squash merge | ✅ Completo | ✅ PR valida |
| `hotfix/*` | `main` e `develop` | Merge commit | ✅ Completo | ✅ PR valida |
| `release/*` | `main` | Merge commit | ⚠️ Lint only | ✅ PR valida |

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

Organização das 30 issues existentes em 6 sprints (+ milestone de Entrega Final), cada sprint concentrado em **uma única branch de desenvolvimento**, com nomes alinhados às exigências do projeto avaliativo (especificação/arquitetura, geração de código, refatoração com IA, testes automatizados, pipeline CI/CD e documentação).

---

## 📋 Índice Rápido de Branches

| Sprint / Milestone | Branch de Desenvolvimento | Issues | Total |
|---|---|---|---|
| **Sprint 0** — Especificação e arquitetura | `feature/especificacao-arquitetura` | #227, #228, #229, #230, #231 | 5 |
| **Sprint 1** — Geração de Código + ML training | `feature/geracao-codigo-ia` | #202–#211, #213, #214, #215 | 13 |
| **Sprint 2** — Refatoração IA | `feature/refatoracao-ia` | #212, #216 | 2 |
| **Sprint 3** — Testes automatizados | `feature/testes-automatizados` | #217, #218, #219, #220, #221 | 5 |
| **Sprint 4** — Pipeline CI/CD | `feature/pipeline-ci-cd` | #226 | 1 |
| **Sprint 5** — Docs + Prompts | `docs/prompts-readme` | #222, #223, #225 | 3 |
| **Entrega Final** | _(PR final `develop` → `main` + tag)_ | #234 | 1 |
| **TOTAL** | **6 branches de desenvolvimento** | | **30** |

---

## Sprint 0 — Especificação e arquitetura

### Macro Escopo
Concentrar a documentação de especificação e arquitetura do projeto: arquivos `.specs/`, README, licença, `.gitignore`, estrutura de diretórios, steering docs, templates de issues/PR e configuração inicial dos workflows do GitHub Actions. **Sem código de aplicação e sem testes de CI/CD** (a branch dispara apenas lint/setup).

### Branch de Desenvolvimento
- **Branch**: `feature/especificacao-arquitetura`
- **Milestone**: Sprint 0 - Especificação e arquitetura
- **Houses**: Architecture/spec docs (`.specs/`, `README.md`, `.gitignore`, license — documents architecture decisions)
- **Merge em `develop`**: squash merge

### Issues (5 total)

| Issue | Título | Labels |
|---|---|---|
| #231 | chore: criar estrutura de diretórios base | documentation, chore, sprint-0, setup |
| #230 | chore: criar documentação estratégica em .kiro/steering/ | documentation, sprint-0, setup |
| #229 | chore: configurar workflows GitHub Actions | documentation, sprint-0, setup, ci |
| #228 | chore: criar templates de issues e PRs | documentation, sprint-0, setup |
| #227 | chore: criar scripts de automação| documentation, sprint-0, setup |

### Fluxo de Merge

```
1. Commits em feature/especificacao-arquitetura
2. PR -> develop (squash merge — sem CI de testes, apenas lint/setup)
3. Issues movidas para "Done" automaticamente
4. Deletar branch após o merge
```

---

## Sprint 1 — Geração de Código + ML training

### Macro Escopo
Geração assistida por IA do código principal do backend (modelos, schemas, endpoints, services), do frontend (páginas e integração com API) e do pipeline de Machine Learning (treinamento do RandomForest com o dataset do Kaggle). **Maior sprint do projeto — concentra a geração de código de produção**.

### Branch de Desenvolvimento
- **Branch**: `feature/geracao-codigo-ia`
- **Milestone**: Sprint 1 - Geração de Código +  ML training
- **Houses**: Backend + frontend — remaining ML feature code (training script, ML Analytics page)
- **Documentação de prompts**: [`docs/prompts/02-geracao-codigo.md`](../docs/prompts/02-geracao-codigo.md)
- **Merge em `develop`**: squash merge

### Issues (13 total)

| Issue | Título | Labels |
|---|---|---|
| #202 | feat(backend): implementar modelos SQLAlchemy | backend, database, feat, sprint-1 |
| #203 | feat(backend): criar schemas Pydantic | backend, api, feat, sprint-1 |
| #204 | feat(api): criar endpoint POST /upload | backend, api, feat, sprint-1 |
| #205 | feat(api): criar endpoints GET de consulta | backend, api, feat, sprint-1 |
| #206 | test(backend): implementar testes unitários | backend, testing, sprint-1 |
| #207 | feat(frontend): criar página Home com upload | feat, sprint-1 |
| #208 | feat(frontend): criar Dashboard com KPIs | feat, sprint-1 |
| #209 | feat(frontend): criar tabela de batches | feat, sprint-1 |
| #210 | feat(frontend): integração com API backend | api, feat, sprint-1 |
| #211 | test(frontend): implementar testes E2E | testing, sprint-1 |
| #213 | feat(ml): criar ML Pipeline com RandomForest | backend, feat, sprint-1, business-logic |
| #214 | feat(ml): treinar modelo com dataset Kaggle | backend, feat, sprint-1, business-logic |
| #215 | feat(frontend): criar página ML Analytics | frontend, feat, sprint-1 |

### Fluxo de Merge

```
1. Commits em feature/geracao-codigo-ia
2. CI completo (lint + testes) a cada push
3. PR -> develop (squash merge)
4. Issues movidas para "Done" automaticamente
5. Deletar branch após o merge
```

---

## Sprint 2 — Refatoração IA

### Macro Escopo
Refatorar trechos do código gerado na Sprint 1 aplicando princípios SOLID com apoio de IA, cobrindo a refatoração com testes próprios. A refatoração documentada (Open/Closed Principle) transforma `BatchService.calculate_compliance` em um `ComplianceService` orientado a `ComplianceRule` (Protocol), com regras como `TemperatureRule` e `PhRule` — ver [`docs/prompts/03-refatoracao.md`](../docs/prompts/03-refatoracao.md).

### Branch de Desenvolvimento
- **Branch**: `feature/refatoracao-ia`
- **Milestone**: Sprint 2 - Refatoração IA
- **Houses**: Documented AI-assisted refactor of `ml_service.py` + its test coverage (pairs with the existing `docs/prompts/03-refatoracao.md`)
- **Documentação de prompts**: [`docs/prompts/03-refatoracao.md`](../docs/prompts/03-refatoracao.md)
- **Merge em `develop`**: squash merge

### Issues (2 total)

| Issue | Título | Labels |
|---|---|---|
| #212 | feat(ml): implementar Compliance Score Engine | backend, feat, sprint-2, business-logic |
| #216 | test(ml): implementar testes de ML | backend, testing, sprint-2 |

### Fluxo de Merge

```
1. Commits em feature/refatoracao-ia
2. CI completo (lint + testes) a cada push
3. PR -> develop (squash merge)
4. Issues movidas para "Done" automaticamente
5. Deletar branch após o merge
```

---

## Sprint 3 — Testes automatizados

### Macro Escopo
Concentrar a cobertura de testes automatizados de ponta a ponta: testes unitários de backend (pytest) e frontend (Vitest), testes de integração de API (Postman/Newman), testes E2E (Cypress) e validação/relatórios de cobertura.

### Branch de Desenvolvimento
- **Branch**: `feature/testes-automatizados`
- **Milestone**: Sprint 3 - Testes automatizado
- **Houses**: Coverage validation suite (testes unitários backend/frontend, integração Postman, E2E Cypress, validação e relatórios de cobertura)
- **Documentação de prompts**: [`docs/prompts/04-testes.md`](../docs/prompts/04-testes.md)
- **Merge em `develop`**: squash merge

### Issues (5 total)

| Issue | Título | Labels |
|---|---|---|
| #217 | test(backend): testes unitários com pytest | backend, testing, sprint-3 |
| #218 | test(frontend): testes unitários com Vitest | frontend, testing, sprint-3 |
| #219 | test(api): testes de integração com Postman | backend, api, testing, sprint-3 |
| #220 | test(e2e): testes E2E com Cypress | frontend, testing, sprint-3 |
| #221 | test(coverage): validação de cobertura e relatórios | testing, sprint-3 |

### Fluxo de Merge

```
1. Commits em feature/testes-automatizados
2. CI completo (lint + testes + cobertura) a cada push
3. PR -> develop (squash merge)
4. Issues movidas para "Done" automaticamente
5. Deletar branch após o merge
```

---

## Sprint 4 — Pipeline CI/CD

### Macro Escopo
Consolidar o pipeline de CI/CD do projeto e fechar o ciclo com o merge final de `develop` para `main`, incluindo a tag de release.

### Branch de Desenvolvimento
- **Branch**: `feature/pipeline-ci-cd`
- **Milestone**: Sprint 4 - Pipeline CI/CD
- **Houses**: CI/CD pipeline fixes (`project-automation.yml`, `ci.yml`) + release
- **Documentação de prompts**: [`docs/prompts/05-pipeline-cicd.md`](../docs/prompts/05-pipeline-cicd.md)
- **Merge em `develop`**: squash merge

### Issues (1 total)

| Issue | Título | Labels |
|---|---|---|
| #226 | chore: merge final develop → main e tag release v1.0.0 | chore, sprint-4, ci |

### Fluxo de Merge

```
1. Commits em feature/pipeline-ci-cd (ajustes finais de workflows)
2. CI completo (lint + testes) a cada push
3. PR -> develop (squash merge)
4. PR final develop -> main + tag de release (v1.0.0)
5. Issue movida para "Done" automaticamente
```

---

## Sprint 5 — Docs + Prompts

### Macro Escopo
Consolidar a documentação técnica do projeto: documentação de API (Swagger), guias de desenvolvimento e organização dos registros de prompts de IA por etapa em `docs/prompts/`, conectando cada sprint à evidência documental do uso de IA no desenvolvimento.

### Branch de Desenvolvimento
- **Branch**: `docs/prompts-readme`
- **Milestone**: Sprint 5 - Docs + Prompts
- **Houses**: Docs — Swagger, dev guides, organização de prompts, `DIAGRAMAS.md`, `PRD.md` (+ Deploy)
- **Documentação de prompts**: [`docs/prompts/06-documentacao.md`](../docs/prompts/06-documentacao.md)
- **Merge em `develop`**: squash merge

### Issues (3 total)

| Issue | Título | Labels |
|---|---|---|
| #222 | docs: documentação de API com Swagger | documentation, backend, sprint-5 |
| #223 | docs: guias de desenvolvimento | documentation, sprint-5 |
| #225 | docs: organizar prompts em docs/prompts/ por etapa de desenvolvimento | backend, feat, sprint-5, validation |

### Fluxo de Merge

```
1. Commits em docs/prompts-readme
2. CI (lint de documentação) a cada push
3. PR -> develop (squash merge)
4. Issues movidas para "Done" automaticamente
5. Deletar branch após o merge
```

---

## Entrega Final

### Macro Escopo
Fechar o ciclo do projeto avaliativo: revisão final do código e da documentação, merge consolidado de `develop` para `main`, criação da tag de release e apresentação do projeto.

### Issues (1 total)

| Issue | Título | Labels |
|---|---|---|
| #234 | chore: entrega final e apresentação do projeto | documentation, chore, entrega-final |

### Milestone
- **Milestone**: Entrega Final
- **Fluxo**: PR final `develop` → `main` (merge commit) + tag de release `v1.0.0`, seguido da apresentação do projeto

---

## Padrão de Branches

**Total**: 8 branches (`main`, `develop` + 6 branches de desenvolvimento — uma por sprint)

| Sprint | Branch de Desenvolvimento |
|---|---|
| Sprint 0 | `feature/especificacao-arquitetura` |
| Sprint 1 | `feature/geracao-codigo-ia` |
| Sprint 2 | `feature/refatoracao-ia` |
| Sprint 3 | `feature/testes-automatizados` |
| Sprint 4 | `feature/pipeline-ci-cd` |
| Sprint 5 | `docs/prompts-readme` |

**Convenção de Nomes**:
- `feature/<nome-descritivo>` - Geração, refatoração e novas funcionalidades de código
- `docs/<nome-descritivo>` - Documentação e organização de prompts
- `chore/<nome-descritivo>` - Tarefas de manutenção e setup
- `release/v<versão>` - Preparação de release

**Regras**:
- Nomes em minúsculas com hífens
- Sem espaços ou caracteres especiais
- Descritivos e concisos
- Relacionados ao escopo da sprint/issue

**Fluxo de Branches**:
1. Criar a branch de desenvolvimento da sprint a partir de `develop`
2. Concentrar todos os commits da sprint nessa única branch (commits atômicos seguindo Conventional Commits)
3. Fazer push para o remote
4. Abrir PR para `develop` referenciando as issues da sprint ("Closes #X")
5. Após o merge (squash merge), deletar a branch local e remote
6. Ao final da Sprint 4/5, abrir o PR final de `develop` para `main` + tag de release

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

### Sprint 0 - CI/CD mínimo

A Sprint 0 (Especificação e arquitetura) roda apenas lint/setup na branch `feature/especificacao-arquitetura` — sem suíte de testes, já que ainda não há código de aplicação. O pipeline completo (lint + testes + cobertura) passa a rodar a partir da Sprint 1, quando o código de produção é gerado.

### Configurações de Workflows

#### Backend (Python)

- **Lint**: flake8, black, isort
- **Testes**: pytest com coverage
- **Cobertura mínima**: 70%
- **Python**: 3.11+
- **Banco de dados**: SQLite (arquivo local)

#### Frontend (React/TypeScript)

- **Lint**: ESLint
- **Testes**: Vitest com coverage
- **Cobertura mínima**: 70%
- **Node.js**: 20+

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

Labels efetivamente em uso no repositório (22 no total), organizados por categoria:

### Área de Desenvolvimento

| Label | Hex | Uso |
|---|---|---|
| `backend` | #0052CC | Alterações no backend Python/FastAPI |
| `frontend` | #d876e3 | Alterações no frontend React |
| `ml` | #6F42C1 | Alterações em machine learning |
| `database` | #fd7e14 | Alterações no banco de dados |
| `api` | #0052cc | Alterações na API REST |

### Tipo de Trabalho

| Label | Hex | Uso |
|---|---|---|
| `testing` | #FFD700 | Testes e cobertura |
| `documentation` | #808080 | Documentação |
| `bug` | #dc3545 | Correção de bugs |
| `feat` | #17a2b8 | Novas funcionalidades |
| `chore` | #e2e3e5 | Tarefas de manutenção |
| `business-logic` | #f9d0c4 | Regras de negócio (compliance, scoring, ML) |
| `validation` | #c5def5 | Validação de dados e qualidade |
| `logging` | #20C997 | Logs, rastreabilidade e auditoria |

### Sprints

| Label | Hex | Uso |
|---|---|---|
| `sprint-0` | #008672 | Issues da Sprint 0 — Especificação e arquitetura |
| `sprint-1` | #1F77B4 | Issues da Sprint 1 — Geração de Código + ML training |
| `sprint-2` | #FF7F0E | Issues da Sprint 2 — Refatoração IA |
| `sprint-3` | #2CA02C | Issues da Sprint 3 — Testes automatizados |
| `sprint-4` | #D62728 | Issues da Sprint 4 — Pipeline CI/CD |
| `sprint-5` | #9467BD | Issues da Sprint 5 — Docs + Prompts |

### Adicionais

| Label | Hex | Uso |
|---|---|---|
| `setup` | #E83E8C | Setup e configuração inicial |
| `ci` | #17A2B8 | CI/CD e automação |
| `entrega-final` | #8B008B | Requisitos de entrega final do projeto |

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
- [ ] Prompts documentados de forma curada por tema/sprint em `docs/prompts/`
- [ ] Cobertura das etapas: arquitetura, geração de código, refatoração, testes, pipeline CI/CD, documentação, análise crítica
- [ ] Arquivos `docs/prompts/01-arquitetura.md` … `07-analise-critica.md`
- [ ] Rastreabilidade completa do uso de IA ao longo do projeto

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
| 1 | Apresentação clara e objetiva | 10% | ⬜ **PENDENTE** | Vídeo não gravado — única pendência crítica |
| 2 | Uso correto do GitHub Board | 10% | ✅ | Board configurado; `project-automation.yml` move cards automaticamente |
| 3 | Organização do repositório | 10% | ✅ | GitFlow + Conventional Commits + PR/Issue templates + 264+ PRs mergeados |
| 4 | Funcionalidades implementadas | 15% | ✅ | Upload CSV, Compliance Score, ML (RandomForest), Dashboard, ETL — todos funcionando |
| 5 | Arquitetura e design | 10% | ✅ | Clean Architecture + ETL distribuído (Extract→Transform→Load→Validate) |
| 6 | Testes automatizados | 15% | ✅ | 63 testes de integração (pytest) + Postman collection + Vitest frontend |
| 7 | Documentação técnica | 10% | ✅ | README + Swagger (`/docs`) + `docs/prompts/` (7 arquivos) + PRD + DIAGRAMAS + analise-resultados |
| 8 | Pipeline CI/CD | 10% | ✅ | 4 workflows: `ci.yml`, `cd.yml`, `project-automation.yml`, `release-lint.yml` — todos funcionando |
| 9 | Uso de IA no desenvolvimento | 5% | ✅ | Claude AI (Claude Code) usado em geração de código, refatoração, testes e documentação |
| 10 | Análise crítica de IA | 5% | ✅ | `docs/prompts/03-refatoracao.md` (3 refatorações com análise crítica de Michele) + `docs/prompts/07-analise-critica.md` |
| 11 | Rastreabilidade e qualidade | 10% | ✅ | 7 arquivos `docs/prompts/01–07`, 13 fixtures CSV, scripts de validação, `docs/analise-resultados.md` |

> **Última atualização:** Junho de 2026 — Score estimado: **90/100** (apenas critério 1 pendente)

### ⚠️ Pendências para Entrega Final

| Item | Ação necessária | Prazo |
|------|----------------|-------|
| **Vídeo de apresentação** (10%) | Gravar vídeo de até 10 minutos demonstrando o sistema em funcionamento, explicando a arquitetura e o uso de IA; hospedar no YouTube/Vimeo e adicionar link no README | Antes da entrega |
| **Tag de release v1.0.0** | Criar PR `develop → main` e tag `v1.0.0` após gravar o vídeo | Após o vídeo |
| **Fechar issue #234** | Chore de entrega final — fechar com link para o vídeo e tag | Após o merge |

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
4. Labels: `documentation`, `chore`, `entrega-final`
5. Milestone: `Entrega Final`
6. Assignee: Todos os colaboradores
7. Adicione ao projeto "BiotecPredict Roadmap" (coluna "Backlog")
8. Deixe aberta até o final do projeto

---

## Automação do GitHub Projects

O projeto utiliza GitHub Projects com automação para manter o board sincronizado: issues e PRs são adicionados e movidos entre colunas automaticamente conforme seu status.

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

| Milestone (título exato no GitHub) | Tema | Branch de Desenvolvimento |
|---|---|---|
| `Sprint 0 - Especificação e arquitetura` | Especificação, arquitetura e setup do projeto | `feature/especificacao-arquitetura` |
| `Sprint 1 - Geração de Código +  ML training` | Geração de código com IA (backend, frontend, ML) | `feature/geracao-codigo-ia` |
| `Sprint 2 - Refatoração IA` | Refatoração com IA (princípios SOLID / Open-Closed) | `feature/refatoracao-ia` |
| `Sprint 3 - Testes automatizado` | Testes automatizados (unitários, integração, E2E, cobertura) | `feature/testes-automatizados` |
| `Sprint 4 - Pipeline CI/CD` | Consolidação do pipeline CI/CD e merge final para `main` | `feature/pipeline-ci-cd` |
| `Sprint 5 - Docs + Prompts` | Documentação técnica e organização de prompts de IA | `docs/prompts-readme` |
| `Entrega Final` | Apresentação e entrega do projeto | _(PR final `develop` → `main` + tag)_ |

### Configuração do Workflow project-automation.yml

**Localização**: `.github/workflows/project-automation.yml`

**Variáveis de Ambiente**:
```yaml
PROJECT_OWNER: micheleoliveiracod
PROJECT_NUMBER: 7
PROJECT_URL: https://github.com/users/micheleoliveiracod/projects/7
STATUS_FIELD: Status
```

**Triggers**:
- Issues: opened, reopened, closed
- Pull Requests: opened, reopened, closed, converted_to_draft, ready_for_review

**Ações** (jobs `add-to-project` e `move-card`):
- Adiciona issues/PRs recém-abertas ao projeto automaticamente (autenticado com o secret `ADD_TO_PROJECT_PAT`)
- Move o card para a coluna de status correspondente ao evento (Todo → Sprint In Progress → In Review → Done)

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