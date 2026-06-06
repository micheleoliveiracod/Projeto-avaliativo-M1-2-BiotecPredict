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

### Problema identificado e corrigido

A IA gerou o workflow rodando em **todas as branches**, o que causava falhas desnecessárias em branches de feature sem banco configurado. **Correção:** restrito a `develop` com `paths-ignore` para arquivos de documentação.

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
