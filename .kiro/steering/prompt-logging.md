# Prompt Logging - BiotecPredict

## 🎯 Propósito

Contexto permanente para o agente Kiro sobre o sistema de logging de prompts. Este arquivo fornece instruções sobre como o sistema funciona, como manter a rastreabilidade e boas práticas para trabalhar com prompt logging durante o desenvolvimento do BiotecPredict.

---

## 📋 Visão Geral

O BiotecPredict implementa um sistema automático de logging de prompts executados no Kiro, organizado por branch Git. O objetivo é manter rastreabilidade completa das interações com o agente durante o desenvolvimento, facilitando auditoria, reprodutibilidade e análise de qualidade.

### Por que é Importante?

- **Auditoria e Conformidade**: Registro documentado de todas as decisões e instruções ao agente
- **Reprodutibilidade**: Entender o contexto e decisões que levaram a uma implementação
- **Análise de Qualidade**: Avaliar efetividade das instruções e padrões de uso
- **Documentação Viva**: Histórico executável que complementa documentação técnica
- **Aprendizado Contínuo**: Analisar prompts bem-sucedidos para melhorar futuras interações

---

## 🏗️ Arquitetura

```
Desenvolvedor submete prompt no Kiro
        ↓
Hook "promptSubmit" é disparado
        ↓
Script Python coleta metadados (usuário, branch, timestamp)
        ↓
Prompt é registrado em arquivo .md por branch
        ↓
Arquivo é versionado no Git automaticamente
```

### Componentes

| Componente | Localização | Função |
|---|---|---|
| **Hook** | `.kiro/hooks/prompt-logger.json` | Intercepta evento `promptSubmit` |
| **Script** | `.kiro/scripts/log_prompt.py` | Coleta metadados e persiste logs |
| **Logs** | `.kiro/prompt-logs/<branch>.md` | Arquivos de log organizados por branch |

---

## 📁 Estrutura de Logs

Cada branch Git tem seu próprio arquivo de log:

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-compliance.md      # Logs de feature branches
├── bugfix-validation.md       # Logs de bugfix branches
├── release-v1.0.0.md         # Logs de release branches
└── chore-setup.md            # Logs de chore branches
```

### Formato de Entrada

```markdown
## Prompt: <título extraído do prompt>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```

---
```

---

## 🔧 Convenções

### Nomes de Arquivo

- Branches com `/` são convertidas para `-`
- Exemplo: `feature/compliance-score` → `feature-compliance-score.md`
- Sempre em minúsculas
- Sem espaços ou caracteres especiais

### Timezone

- **Sempre**: Horário de Brasília (America/Sao_Paulo - UTC-3)
- **Formato**: `YYYY-MM-DD HH:mm:ss`
- **Exemplo**: `2026-05-27 14:35:22`

### Versionamento

- Logs são versionados no Git por padrão
- Facilita rastreabilidade em code reviews
- Preserva histórico de decisões
- Fazer commit dos logs junto com o código

---

## 📋 Convenções de Logging

### Nomes de Arquivos de Log

**Padrão**: `<tipo-branch>-<nome-descritivo>.md`

| Tipo de Branch | Exemplo | Arquivo |
|---|---|---|
| `feature/` | `feature/compliance-score` | `feature-compliance-score.md` |
| `bugfix/` | `bugfix/validation-error` | `bugfix-validation-error.md` |
| `hotfix/` | `hotfix/api-crash` | `hotfix-api-crash.md` |
| `release/` | `release/v1.0.0` | `release-v1.0.0.md` |
| `chore/` | `chore/update-deps` | `chore-update-deps.md` |
| `docs/` | `docs/api-guide` | `docs-api-guide.md` |
| `main` | - | `main.md` |
| `develop` | - | `develop.md` |

**Regras:**
- Converter `/` em `-` (exemplo: `feature/auth-v2` → `feature-auth-v2.md`)
- Sempre em minúsculas
- Sem espaços ou caracteres especiais
- Sem acentuação (usar equivalentes ASCII)

### Formato de Timestamp

**Padrão**: `YYYY-MM-DD HH:mm:ss` (Brasília - UTC-3)

**Exemplos válidos:**
- `2026-05-27 14:35:22` ✅
- `2026-05-27 09:15:00` ✅
- `2026-05-27 23:59:59` ✅

**Exemplos inválidos:**
- `27/05/2026 14:35:22` ❌ (formato brasileiro)
- `2026-05-27T14:35:22Z` ❌ (ISO com Z)
- `14:35:22` ❌ (sem data)

**Timezone obrigatório**: America/Sao_Paulo (UTC-3)
- Não usar UTC ou outros timezones
- Não usar horário de verão (sempre UTC-3)

### Formato de Metadados

**Estrutura obrigatória:**

```markdown
## Prompt: <título extraído do prompt>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```
```

**Campos obrigatórios:**
- `Prompt`: Título descritivo (máx 80 caracteres)
- `Responsável`: Nome do usuário Git (usar `git config user.name`)
- `Branch`: Nome exato da branch (usar `git rev-parse --abbrev-ref HEAD`)
- `Data/hora`: Timestamp em formato padrão com timezone
- `Prompt original`: Conteúdo completo entre triple backticks

### Filtragem de Prompts

**Prompts que NÃO devem ser registrados:**

| Tipo | Exemplo | Motivo |
|---|---|---|
| Confirmações simples | "sim", "ok", "entendido" | Ruído nos logs |
| Respostas muito curtas | "próximo", "continue" | Sem valor informativo |
| Comandos de navegação | "voltar", "ir para", "sair" | Não são prompts reais |
| Respostas vazias | "" | Sem conteúdo |
| Duplicatas | Mesmo prompt repetido | Evitar redundância |

**Prompts que DEVEM ser registrados:**

| Tipo | Exemplo | Motivo |
|---|---|---|
| Instruções de implementação | "Implementar endpoint de upload" | Decisão técnica |
| Pedidos de análise | "Analisar este código" | Análise de qualidade |
| Correções de bugs | "Corrigir erro de validação" | Rastreabilidade de fixes |
| Refatorações | "Refatorar este módulo" | Melhorias de código |
| Documentação | "Documentar esta função" | Documentação viva |

**Critério de mínimo:**
- Prompts com menos de 10 caracteres são automaticamente filtrados
- Prompts sem conteúdo são automaticamente filtrados
- Confirmações simples são automaticamente filtradas

### Metadata Format

**Campos adicionais opcionais:**

```markdown
## Prompt: <título>
- Responsável: <nome>
- Branch: <branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)
- Categoria: [implementação|análise|correção|refatoração|documentação]
- Prioridade: [alta|média|baixa]
- Relacionado a: [#issue-number ou feature-name]

### Prompt original
```
<conteúdo>
```

### Resultado
<resumo do resultado ou link para commit>
```

**Campos opcionais:**
- `Categoria`: Tipo de prompt (para análise futura)
- `Prioridade`: Importância relativa
- `Relacionado a`: Rastreabilidade com issues ou features
- `Resultado`: Resumo do que foi gerado

### Best Practices para Consistência

1. **Usar template padrão** - Copiar formato de entradas anteriores
2. **Manter indentação** - Usar 2 espaços para subitens
3. **Separar seções** - Usar `---` entre prompts
4. **Documentar contexto** - Incluir informações relevantes
5. **Revisar antes de commitar** - Verificar formatação
6. **Fazer commits atômicos** - Um commit por feature/bugfix
7. **Referenciar em PRs** - Mencionar logs em descrição de PR
8. **Manter histórico limpo** - Não editar entradas antigas

---

## 📖 Como Usar

### Submeter Prompts (Automático)

Nenhuma ação manual é necessária. Prompts são registrados automaticamente quando submetidos ao Kiro:

```
1. Abrir Kiro
2. Digitar prompt
3. Pressionar Enter/Submit
   ↓ (Automático)
4. Hook dispara
5. Script coleta metadados
6. Prompt é registrado em .kiro/prompt-logs/<branch-atual>.md
```

### Consultar Logs

**Ver logs da branch atual:**
```bash
# Mac/Linux
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Windows PowerShell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Ver logs de branch específica:**
```bash
# Mac/Linux
cat .kiro/prompt-logs/feature-compliance-score.md

# Windows
type .kiro\prompt-logs\feature-compliance-score.md
```

**Últimas entradas:**
```bash
# Mac/Linux
tail -n 50 .kiro/prompt-logs/<branch>.md

# Windows PowerShell
Get-Content ".kiro\prompt-logs\<branch>.md" -Tail 50
```

**Buscar por palavra-chave:**
```bash
# Mac/Linux
grep -i "compliance" .kiro/prompt-logs/*.md

# Windows PowerShell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

---

## 🎯 Boas Práticas para o Agente Kiro

Ao trabalhar com prompt logging, seguir estas práticas:

### 1. **Não Modificar Formato de Log**
- Manter consistência para parsing futuro
- Sempre usar o formato padrão
- Não editar manualmente arquivos de log

### 2. **Tratar Erros Graciosamente**
- Nunca bloquear execução do Kiro
- Se logging falhar, continuar com a tarefa
- Registrar erros em logs do Kiro, não interromper

### 3. **Preservar Histórico**
- Sempre usar append, nunca sobrescrever
- Manter histórico completo de todas as interações
- Não deletar ou limpar logs

### 4. **Sanitizar Nomes de Branch**
- Converter `/` em `-`
- Converter caracteres especiais em `-`
- Exemplo: `feature/auth-v2` → `feature-auth-v2.md`

### 5. **Documentar Limitações**
- Ser transparente sobre o que não é capturado
- Se conteúdo não for capturado, registrar metadados
- Não gerar entradas vazias

### 6. **Filtrar Prompts Triviais**
- Não registrar confirmações simples (sim, não, ok)
- Não registrar respostas muito curtas (< 10 caracteres)
- Não registrar comandos de navegação (next, back, continue)
- Justificativa: Manter logs focados em interações significativas

### 7. **Fazer Commits Regulares**
- Versionar logs junto com o código
- Exemplo: `git add .kiro/prompt-logs/`
- Commit: `docs: adiciona prompts de implementação`

### 8. **Referenciar Logs em Commits**
- Quando código é gerado por IA, referenciar o log
- Exemplo: `feat(ml): implementa RandomForest (prompts em .kiro/prompt-logs/feature-ml.md)`

---

## ⚠️ Limitações Conhecidas

### 1. Captura de Conteúdo
- Kiro pode não expor conteúdo completo via hooks
- Prompts sem conteúdo são automaticamente filtrados
- Metadados ainda são registrados mesmo sem conteúdo

### 2. Filtragem Automática
- Confirmações simples não são registradas
- Respostas muito curtas são filtradas
- Comandos de navegação são ignorados

### 3. Sem Captura de Resultados (MVP)
- Apenas prompts são capturados, não respostas do agente
- Planejado para fase futura (hook `agentStop`)

### 4. Crescimento de Arquivos
- Arquivos de log crescem indefinidamente
- Estratégia de rotação planejada para fase futura
- Considerar arquivamento manual se necessário

---

## 🔍 Troubleshooting

### Logs não estão sendo criados

**Verificar:**
1. Hook existe: `.kiro/hooks/prompt-logger.json`
2. Script existe: `.kiro/scripts/log_prompt.py`
3. Permissões de execução do script
4. Logs de erro do Kiro

**Solução:**
```bash
# Testar manualmente
python .kiro/scripts/log_prompt.py --test

# Verificar se arquivo foi criado
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

### Conteúdo não é capturado

- Limitação conhecida do Kiro
- Metadados ainda são registrados
- Considerar captura manual se necessário

### Arquivo de log está vazio

- Submeter um prompt no Kiro para criar entrada
- Hook deve capturar automaticamente
- Se ainda vazio, verificar instalação

---

## 🔧 Instruções para Manutenção

### Manutenção do Sistema de Logging

O sistema de prompt logging requer manutenção periódica para garantir funcionamento correto e qualidade dos dados.

### Procedimentos de Backup

**Backup manual dos logs:**

```bash
# Mac/Linux
mkdir -p backups
cp -r .kiro/prompt-logs backups/prompt-logs-$(date +%Y%m%d-%H%M%S)

# Windows PowerShell
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item -Path ".kiro\prompt-logs" -Destination "backups\prompt-logs-$timestamp" -Recurse
```

**Backup automático (recomendado):**
- Adicionar ao `.github/workflows/backup.yml` (planejado para Fase 7)
- Executar diariamente às 00:00 (Brasília)
- Armazenar em GitHub Releases ou artifact storage
- Retenção: 30 dias

**Restaurar backup:**

```bash
# Mac/Linux
cp -r backups/prompt-logs-YYYYMMDD-HHMMSS/* .kiro/prompt-logs/

# Windows PowerShell
Copy-Item -Path "backups\prompt-logs-YYYYMMDD-HHMMSS\*" -Destination ".kiro\prompt-logs" -Recurse -Force
```

### Procedimentos de Limpeza

**Remover entradas duplicadas:**

```bash
# Mac/Linux
# Verificar duplicatas
grep -n "## Prompt:" .kiro/prompt-logs/feature-*.md | sort | uniq -d

# Remover manualmente (editar arquivo)
```

**Remover prompts triviais não capturados:**

```bash
# Mac/Linux
# Buscar linhas vazias ou muito curtas
grep -E "^$|^.{1,5}$" .kiro/prompt-logs/*.md

# Remover manualmente
```

**Arquivar logs antigos (Fase 4):**

```bash
# Mac/Linux
# Mover logs com mais de 3 meses para arquivo
find .kiro/prompt-logs -name "*.md" -mtime +90 -exec mv {} .kiro/prompt-logs/archive/ \;

# Comprimir
tar -czf .kiro/prompt-logs/archive-$(date +%Y%m).tar.gz .kiro/prompt-logs/archive/
```

**Política de retenção:**
- Logs ativos: 3 meses em `.kiro/prompt-logs/`
- Logs arquivados: 1 ano em `.kiro/prompt-logs/archive/`
- Logs deletados: Após 1 ano (manter backup)

### Procedimentos de Troubleshooting Avançado

**Problema: Hook não está disparando**

**Diagnóstico:**
```bash
# Verificar se hook existe
ls -la .kiro/hooks/prompt-logger.json

# Verificar se script existe
ls -la .kiro/scripts/log_prompt.py

# Verificar permissões
chmod +x .kiro/scripts/log_prompt.py

# Testar manualmente
python .kiro/scripts/log_prompt.py --test
```

**Solução:**
1. Verificar instalação do hook no Kiro
2. Reiniciar Kiro
3. Submeter novo prompt para testar
4. Verificar logs de erro do Kiro

**Problema: Arquivo de log corrompido**

**Diagnóstico:**
```bash
# Verificar sintaxe markdown
python -m markdown .kiro/prompt-logs/feature-*.md

# Verificar encoding
file .kiro/prompt-logs/*.md
```

**Solução:**
1. Restaurar backup anterior
2. Recriar entradas manualmente se necessário
3. Verificar encoding (deve ser UTF-8)

**Problema: Logs crescendo muito rápido**

**Diagnóstico:**
```bash
# Verificar tamanho dos arquivos
du -sh .kiro/prompt-logs/*

# Contar entradas por arquivo
grep -c "## Prompt:" .kiro/prompt-logs/*.md
```

**Solução:**
1. Implementar rotação de logs (Fase 4)
2. Arquivar logs antigos
3. Considerar compressão
4. Revisar política de filtragem

### Quando Atualizar o Sistema

**Atualizar quando:**

| Situação | Ação | Frequência |
|----------|------|-----------|
| Novo tipo de branch | Adicionar padrão em "Nomes de Arquivo" | Conforme necessário |
| Mudança de timezone | Atualizar formato em "Formato de Timestamp" | Raramente |
| Novo campo obrigatório | Atualizar "Formato de Metadados" | Conforme necessário |
| Mudança de política de filtragem | Atualizar "Filtragem de Prompts" | Conforme necessário |
| Implementação de Fase 2-4 | Atualizar seções correspondentes | Conforme roadmap |

**Processo de atualização:**

1. Criar issue: `chore: atualizar sistema de prompt logging`
2. Criar branch: `chore/update-prompt-logging`
3. Atualizar `.kiro/steering/prompt-logging.md`
4. Atualizar `.kiro/scripts/log_prompt.py` se necessário
5. Atualizar `.kiro/hooks/prompt-logger.json` se necessário
6. Testar manualmente
7. Fazer commit: `chore: atualiza sistema de prompt logging`
8. Fazer PR e merge

### Monitoramento e Métricas

**Métricas a acompanhar:**

| Métrica | Ferramenta | Frequência |
|---------|-----------|-----------|
| Número de prompts por branch | `grep -c "## Prompt:" .kiro/prompt-logs/*.md` | Semanal |
| Tamanho total dos logs | `du -sh .kiro/prompt-logs/` | Semanal |
| Taxa de crescimento | Comparar com semana anterior | Semanal |
| Prompts por desenvolvedor | `grep "Responsável:" .kiro/prompt-logs/*.md \| sort \| uniq -c` | Mensal |
| Categorias mais usadas | `grep "Categoria:" .kiro/prompt-logs/*.md \| sort \| uniq -c` | Mensal |

**Relatório mensal:**

```bash
# Gerar relatório
cat > .kiro/reports/prompt-logging-$(date +%Y%m).md << 'EOF'
# Relatório de Prompt Logging - $(date +%B/%Y)

## Estatísticas Gerais
- Total de prompts: $(grep -c "## Prompt:" .kiro/prompt-logs/*.md)
- Tamanho total: $(du -sh .kiro/prompt-logs/ | cut -f1)
- Branches ativas: $(ls .kiro/prompt-logs/*.md | wc -l)

## Prompts por Branch
$(for file in .kiro/prompt-logs/*.md; do echo "- $(basename $file): $(grep -c "## Prompt:" $file)"; done)

## Prompts por Desenvolvedor
$(grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq -c)

## Observações
- [Adicionar observações relevantes]
- [Problemas encontrados]
- [Melhorias sugeridas]
EOF
```

### Documentação de Manutenção

**Manter documentação atualizada:**

1. **Este arquivo** (`.kiro/steering/prompt-logging.md`)
   - Atualizar quando houver mudanças no sistema
   - Versionar no Git
   - Referenciar em PRs

2. **Documentação técnica** (`docs/prompt-logging.md`)
   - Guia detalhado para usuários
   - Exemplos práticos
   - Troubleshooting expandido

3. **Spec técnica** (`.kiro/specs/prompt-logging/`)
   - Especificação completa do sistema
   - Requisitos funcionais
   - Testes de aceitação

4. **Changelog** (`.kiro/prompt-logs/CHANGELOG.md`)
   - Histórico de mudanças no sistema
   - Versões do hook e script
   - Datas de atualizações

### Checklist de Manutenção Mensal

- [ ] Verificar tamanho dos logs (< 100MB)
- [ ] Verificar número de entradas (< 1000 por branch)
- [ ] Testar backup e restauração
- [ ] Revisar logs para duplicatas
- [ ] Verificar permissões de arquivos
- [ ] Atualizar métricas e relatórios
- [ ] Revisar issues de logging
- [ ] Documentar problemas encontrados
- [ ] Planejar melhorias para próximo mês
- [ ] Fazer commit de manutenção: `chore: manutenção mensal de prompt logging`

### Contato e Suporte

**Para problemas com prompt logging:**

1. Verificar seção "Troubleshooting" deste arquivo
2. Consultar `docs/prompt-logging.md` para mais detalhes
3. Abrir issue: `bug: problema com prompt logging`
4. Referenciar este arquivo na issue
5. Incluir logs de erro e passos para reproduzir

---

## 📚 Referências

| Referência | Localização | Conteúdo |
|---|---|---|
| **Documentação Completa** | `docs/prompt-logging.md` | Guia detalhado com exemplos |
| **Spec Completa** | `.kiro/specs/prompt-logging/` | Especificação técnica |
| **Git Flow** | `.kiro/steering/gitflow.md` | Convenções de branches e commits |
| **Localização** | `.kiro/steering/localizacao.md` | Timezone e formato de datas |

---

## 🚀 Evolução Futura

### Fase 2: Captura de Resultados
- Hook `agentStop` para capturar fim da execução
- Resumo automático da resposta do agente
- Associação prompt → resultado

### Fase 3: Interface de Consulta
- CLI para buscar logs
- Filtros por data, branch, usuário
- Exportação para outros formatos

### Fase 4: Rotação e Arquivamento
- Arquivamento automático de logs antigos
- Compressão de arquivos grandes
- Política de retenção configurável

---

## 💡 Contexto para Desenvolvimento

Quando trabalhar em tarefas do BiotecPredict:

1. **Submeter prompts normalmente** - Sistema captura automaticamente
2. **Consultar logs de features anteriores** - Reutilizar padrões bem-sucedidos
3. **Referenciar logs em PRs** - Facilitar code reviews
4. **Manter logs versionados** - Fazer commit junto com código
5. **Usar logs para documentação** - Complementar documentação técnica

---

**Versão**: 0.3.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Convenções de Logging e Manutenção Documentadas
