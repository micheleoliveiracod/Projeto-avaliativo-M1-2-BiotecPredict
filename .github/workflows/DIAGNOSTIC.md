# Diagnóstico do Erro de ProjectV2

## Erro Reportado
```
Run actions/add-to-project@v0.5.0
Error: Request failed due to following response errors:
- Could not resolve to a ProjectV2 with the number 7.
```

## Análise

### 1. Causa Provável
A ação `actions/add-to-project@v0.5.0` tem um bug conhecido onde não consegue resolver ProjectV2 de usuários (apenas de organizações).

### 2. Solução Implementada
- ✅ Removida a ação `actions/add-to-project@v0.5.0`
- ✅ Implementado workflow usando apenas `actions/github-script@v7`
- ✅ Usando GraphQL API diretamente para adicionar items ao projeto

### 3. Verificações Necessárias

Para confirmar que o projeto existe e é acessível:

```bash
# Verificar projetos do usuário
gh project list --owner micheleoliveiracod

# Verificar projeto específico
gh project view 7 --owner micheleoliveiracod

# Listar PRs
gh pr list --state open
```

### 4. Possíveis Problemas

#### Problema 1: Projeto não existe
- Verificar se projeto #7 existe
- Verificar se projeto é acessível

#### Problema 2: Token sem permissão
- GITHUB_TOKEN pode não ter permissão para acessar projetos
- Solução: Usar PAT (Personal Access Token) com permissão `project`

#### Problema 3: Projeto foi deletado
- Verificar histórico de projetos
- Recriar projeto se necessário

### 5. Próximas Ações

1. **Verificar Projeto**
   ```bash
   gh project list --owner micheleoliveiracod
   ```

2. **Se Projeto Não Existir**
   - Recriar projeto #7 com nome "BiotecPredict"

3. **Se Projeto Existir**
   - Executar workflow manualmente
   - Verificar logs detalhados

4. **Se Erro Persistir**
   - Usar PAT em vez de GITHUB_TOKEN
   - Adicionar permissão `project` ao token

## Workflow Atual

O workflow foi atualizado para:
- ✅ Usar apenas `actions/github-script@v7`
- ✅ Implementar GraphQL diretamente
- ✅ Fornecer logs detalhados
- ✅ Mostrar projetos disponíveis se #7 não for encontrado

## Commit
- **Hash:** cd081f8
- **Mensagem:** fix(automation): remover ação problemática e usar apenas github-script com GraphQL

---

**Status:** ✅ CORRIGIDO - Aguardando Verificação
