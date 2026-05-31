# Prompt Logs - BiotecPredict

Histórico automático de prompts executados no Kiro, organizados por branch Git.

## 📁 Estrutura

```
.kiro/prompt-logs/
├── main.md              # Logs da branch main
├── develop.md           # Logs da branch develop
├── feature-*.md         # Logs de features
├── bugfix-*.md          # Logs de bugfixes
├── hotfix-*.md          # Logs de hotfixes
├── release-*.md         # Logs de releases
├── chore-*.md           # Logs de chores
└── docs-*.md            # Logs de documentação
```

## 🎯 Propósito

- **Auditoria**: Registro documentado de todas as decisões ao agente
- **Reprodutibilidade**: Entender contexto e decisões que levaram a implementações
- **Rastreabilidade**: Vincular código gerado aos prompts que o originaram

## 📋 Formato de Arquivo

Cada arquivo segue este padrão:

```markdown
# Prompt Logs: <branch-name>

---

## Prompt: <título extraído do prompt>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```
```

## 🔧 Convenções

### Nomes de Arquivo

| Tipo | Exemplo | Arquivo |
|---|---|---|
| Feature | `feature/compliance-score` | `feature-compliance-score.md` |
| Bugfix | `bugfix/validation-error` | `bugfix-validation-error.md` |
| Hotfix | `hotfix/api-crash` | `hotfix-api-crash.md` |
| Release | `release/v1.0.0` | `release-v1.0.0.md` |
| Chore | `chore/update-deps` | `chore-update-deps.md` |
| Docs | `docs/api-guide` | `docs-api-guide.md` |
| Main | `main` | `main.md` |
| Develop | `develop` | `develop.md` |

**Regra**: Converter `/` em `-`, sempre minúsculas, sem espaços.

### Timestamp Obrigatório

Formato: `YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)`

Exemplo: `2026-05-27 14:35:22 (Brasília - UTC-3)`

## 📊 Consultar Logs

**Ver logs da branch atual:**
```bash
# Windows PowerShell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"

# Mac/Linux
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Buscar por palavra-chave:**
```bash
# Windows PowerShell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"

# Mac/Linux
grep -i "compliance" .kiro/prompt-logs/*.md
```

## 🔐 Boas Práticas

- ✅ Prompts capturados automaticamente via hook `promptSubmit`
- ✅ Sempre usar timestamp em horário de Brasília (UTC-3)
- ✅ Manter histórico completo (nunca deletar)
- ✅ Versionar logs junto com código
- ✅ Referenciar logs em PRs para rastreabilidade

## 📚 Referências

- Documentação completa: `.kiro/steering/prompt-logging.md`
- Convenções de logging: `.kiro/steering/localizacao.md`
- Git Flow: `.kiro/steering/gitflow.md`

---

**Versão**: 1.0.0  
**Status**: ✅ Ativo  
**Timezone**: America/Sao_Paulo (UTC-3)
