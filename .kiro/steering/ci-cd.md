# CI/CD Workflow

## Visão Geral
Este documento descreve o fluxo de CI/CD para o projeto BiotecPredict.

## Gatilhos de CI/CD

### Pull Requests
- **Lint**: Executado automaticamente em todos os PRs
- **Testes Unitários**: Executados após aprovação do PR
- **Cobertura de Testes**: Mínimo 80% de cobertura obrigatório

### Branches Protegidas
- `main`: Requer 2 aprovações + testes passando
- `develop`: Requer 1 aprovação + testes passando

## Etapas do Pipeline

1. **Lint** (Python)
   - Verifica PEP 8
   - Valida imports
   - Detecta código morto

2. **Testes Unitários**
   - Executa pytest
   - Gera relatório de cobertura
   - Valida schemas Pydantic

3. **Testes de Integração**
   - Testa endpoints FastAPI
   - Valida banco de dados
   - Verifica migrações

## Aprovação de PRs

PRs são aprovados manualmente após:
- ✅ Todos os testes passarem
- ✅ Cobertura mínima atingida
- ✅ Code review concluído
- ✅ Sem conflitos com develop

Após aprovação, o merge é feito manualmente.
