# Convenções de Logging - Contexto Permanente para o Agente Kiro

## 🎯 Propósito

Este arquivo fornece contexto permanente e abrangente para o agente Kiro sobre as convenções de logging de prompts do BiotecPredict. Ele documenta:

- **Propósito do sistema**: Por que registramos prompts
- **Como funciona**: Arquitetura e fluxo de dados
- **Estrutura de logs**: Organização e formato
- **Convenções de nomenclatura**: Padrões por tipo de branch
- **Formato de timestamp**: Timezone e padrão de data/hora
- **Estrutura de metadados**: Campos obrigatórios
- **Critérios de filtragem**: Prompts triviais vs significativos
- **Boas práticas**: Como trabalhar com prompt logging
- **Integração com Kiro**: Como o sistema se integra com a IDE
- **Manutenção**: Procedimentos de backup e limpeza

---

## 📋 Visão Geral do Sistema

### O que é Prompt Logging?

O **Prompt Logging** é um sistema automático que registra todos os prompts executados no Kiro, organizados por branch Git. Cada prompt é capturado com metadados (usuário, branch, timestamp) e armazenado em arquivos markdown estruturados.

### Por que é Importante?

- **Auditoria e Conformidade**: Registro documentado de todas as decisões e instruções ao agente
- **Reprodutibilidade**: Entender o contexto e decisões que levaram a uma implementação
- **Análise de Qualidade**: Avaliar efetividade das instruções e padrões de uso
- **Documentação Viva**: Histórico executável que complementa documentação técnica
- **Aprendizado Contínuo**: Analisar prompts bem-sucedidos para melhorar futuras interações
- **Rastreabilidade**: Vincular código gerado aos prompts que o originaram

### Benefícios para o Desenvolvimento

| Benefício | Descrição | Exemplo |
|-----------|-----------|---------|
| **Code Review** | Revisor entende contexto das decisões | "Por que essa função foi implementada assim?" → Ver prompts |
| **Documentação** | Histórico executável do desenvolvimento | Prompts servem como documentação viva |
| **Qualidade** | Identificar padrões de sucesso | Analisar prompts que geraram código de qualidade |
| **Treinamento** | Aprender com prompts bem-sucedidos | Reutilizar padrões de prompting efetivos |
| **Conformidade** | Rastreabilidade para auditorias | Provar que código foi gerado com IA |

---

## 🏗️ Arquitetura do Sistema

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    PROMPT LOGGING SYSTEM                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      KIRO IDE                                │
│  (Desenvolvedor submete prompt)                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   HOOK: promptSubmit                          │
│  (.kiro/hooks/prompt-logger.json)                            │
│  Intercepta evento de submissão de prompt                    │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              SCRIPT: log_prompt.py                            │
│  (.kiro/scripts/log_prompt.py)                               │
│  - Coleta metadados (usuário, branch, timestamp)             │
│  - Extrai conteúdo do prompt                                 │
│  - Formata entrada markdown                                  │
│  - Persiste em arquivo de log                                │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              ARQUIVO DE LOG: <branch>.md                      │
│  (.kiro/prompt-logs/<branch>.md)                             │
│  - Organizado por branch Git                                 │
│  - Formato markdown estruturado                              │
│  - Versionado no Git                                         │
└──────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados

```
1. Desenvolvedor abre Kiro
   ↓
2. Digita prompt e pressiona Enter/Submit
   ↓
3. Hook "promptSubmit" é disparado
   ↓
4. Script log_prompt.py é executado
   ↓
5. Coleta metadados:
   - Nome do usuário Git (git config user.name)
   - Branch atual (git rev-parse --abbrev-ref HEAD)
   - Timestamp em Brasília (America/Sao_Paulo - UTC-3)
   ↓
6. Extrai conteúdo do prompt
   ↓
7. Formata entrada markdown
   ↓
8. Persiste em .kiro/prompt-logs/<branch>.md
   ↓
9. Arquivo é versionado no Git
```

---

## 📁 Estrutura de Logs

### Localização

Cada branch Git tem seu próprio arquivo de log:

```
.kiro/prompt-logs/
├── main.md                           # Logs da branch main
├── develop.md                        # Logs da branch develop
├── feature-compliance-score.md       # Logs de feature/compliance-score
├── feature-ml-prediction.md          # Logs de feature/ml-prediction
├── bugfix-validation-error.md        # Logs de bugfix/validation-error
├── hotfix-api-crash.md              # Logs de hotfix/api-crash
├── release-v1.0.0.md                # Logs de release/v1.0.0
├── chore-update-deps.md             # Logs de chore/update-deps
└── docs-api-guide.md                # Logs de docs/api-guide
```

### Formato de Arquivo

Cada arquivo de log segue este padrão:

```markdown
# Prompt Logs: <branch-name>

Histórico de prompts executados no Kiro nesta branch.

---

## Prompt: <título extraído do prompt>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```

---

## Prompt: <próximo prompt>
...
```

### Exemplo Real

```markdown
# Prompt Logs: feature-compliance-score

Histórico de prompts executados no Kiro nesta branch.

---

## Prompt: Implementar Manufacturing Compliance Score Engine
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar o Manufacturing Compliance Score Engine que calcula um score de 0-100 baseado em regras determinísticas. O score deve classificar em ACCEPTABLE (80-100), WARNING (60-79) ou CRITICAL (0-59). Usar as variáveis: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed.
```

---

## Prompt: Criar testes unitários para compliance score
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 15:12:45 (Brasília - UTC-3)

### Prompt original
```
Criar testes unitários com pytest para validar o cálculo do compliance score. Incluir testes para:
1. Score calculado corretamente
2. Classificação correta (ACCEPTABLE/WARNING/CRITICAL)
3. Tratamento de valores fora do range
4. Edge cases (valores nulos, zeros, máximos)
```

---
```

---

## 🔧 Convenções de Logging

### Nomes de Arquivo por Tipo de Branch

**Padrão geral:** `<tipo-branch>-<nome-descritivo>.md`

#### Branches de Feature

| Tipo | Exemplo de Branch | Arquivo de Log | Descrição |
|---|---|---|---|
| `feature/` | `feature/compliance-score` | `feature-compliance-score.md` | Novas funcionalidades |
| `feature/` | `feature/ml-prediction` | `feature-ml-prediction.md` | Modelos de ML |
| `feature/` | `feature/upload-endpoint` | `feature-upload-endpoint.md` | Endpoints da API |

**Regra:** Converter `/` em `-`, manter minúsculas, sem espaços ou caracteres especiais

#### Branches de Correção

| Tipo | Exemplo de Branch | Arquivo de Log | Descrição |
|---|---|---|---|
| `bugfix/` | `bugfix/validation-error` | `bugfix-validation-error.md` | Correção de bugs |
| `bugfix/` | `bugfix/csv-parsing` | `bugfix-csv-parsing.md` | Correção de parsing |
| `hotfix/` | `hotfix/api-crash` | `hotfix-api-crash.md` | Correção urgente |

**Regra:** Converter `/` em `-`, descrever o problema de forma concisa

#### Branches de Manutenção

| Tipo | Exemplo de Branch | Arquivo de Log | Descrição |
|---|---|---|---|
| `chore/` | `chore/update-deps` | `chore-update-deps.md` | Atualização de dependências |
| `chore/` | `chore/setup-ci` | `chore-setup-ci.md` | Configuração de CI/CD |
| `docs/` | `docs/api-guide` | `docs-api-guide.md` | Documentação |
| `release/` | `release/v1.0.0` | `release-v1.0.0.md` | Preparação de release |

**Regra:** Converter `/` em `-`, manter versão exata para releases

#### Branches Principais

| Tipo | Arquivo de Log | Descrição |
|---|---|---|
| `main` | `main.md` | Código em produção |
| `develop` | `develop.md` | Integração de features |

**Regra:** Sem conversão, apenas o nome da branch

### Regras de Nomenclatura

1. **Converter `/` em `-`**
   - `feature/auth-v2` → `feature-auth-v2.md`
   - `bugfix/login-error` → `bugfix-login-error.md`
   - `release/v1.0.0` → `release-v1.0.0.md`

2. **Sempre em minúsculas**
   - ✅ `feature-compliance-score.md`
   - ❌ `Feature-Compliance-Score.md`
   - ❌ `FEATURE-COMPLIANCE-SCORE.md`

3. **Sem espaços ou caracteres especiais**
   - ✅ `feature-ml-prediction.md`
   - ❌ `feature ml prediction.md`
   - ❌ `feature@ml#prediction.md`

4. **Sem acentuação**
   - ✅ `feature-autenticacao.md`
   - ❌ `feature-autenticação.md`

5. **Descritivo e conciso**
   - ✅ `feature-compliance-score-engine.md` (claro e específico)
   - ❌ `feature-x.md` (muito vago)
   - ❌ `feature-implementar-compliance-score-engine-com-validacao-de-ranges.md` (muito longo)

### Formato de Timestamp

**Padrão obrigatório:** `YYYY-MM-DD HH:mm:ss` (Brasília - UTC-3)

#### Exemplos Válidos

```
2026-05-27 14:35:22 (Brasília - UTC-3)  ✅
2026-05-27 09:15:00 (Brasília - UTC-3)  ✅
2026-05-27 23:59:59 (Brasília - UTC-3)  ✅
2026-05-27 00:00:00 (Brasília - UTC-3)  ✅
```

#### Exemplos Inválidos

```
27/05/2026 14:35:22 (Brasília - UTC-3)  ❌ (formato brasileiro)
2026-05-27T14:35:22Z (UTC)              ❌ (ISO com Z, timezone errado)
14:35:22 (Brasília - UTC-3)             ❌ (sem data)
2026-05-27 14:35:22 (UTC-3)             ❌ (sem "Brasília")
2026-05-27 14:35:22                     ❌ (sem timezone)
```

#### Timezone Obrigatório

- **Timezone padrão**: America/Sao_Paulo (UTC-3)
- **Nunca usar**: UTC, UTC-0, UTC+0, ou outros timezones
- **Nunca usar**: Horário de verão (sempre UTC-3, mesmo em períodos de verão)
- **Sempre incluir**: "(Brasília - UTC-3)" após o timestamp

#### Implementação em Python

```python
import pytz
from datetime import datetime

def get_brasilia_timestamp() -> str:
    """Gera timestamp em horário de Brasília (UTC-3)."""
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S (Brasília - UTC-3)")

# Uso
timestamp = get_brasilia_timestamp()
# Resultado: "2026-05-27 14:35:22 (Brasília - UTC-3)"
```

### Estrutura de Metadados Obrigatória

**Formato padrão:**

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

| Campo | Descrição | Exemplo | Regras |
|---|---|---|---|
| **Prompt** | Título descritivo | "Implementar Manufacturing Compliance Score Engine" | Máx 80 caracteres, imperativo |
| **Responsável** | Nome do usuário Git | "Michele Oliveira" | Usar `git config user.name` |
| **Branch** | Nome exato da branch | "feature-compliance-score" | Usar `git rev-parse --abbrev-ref HEAD` |
| **Data/hora** | Timestamp em Brasília | "2026-05-27 14:35:22 (Brasília - UTC-3)" | Formato YYYY-MM-DD HH:mm:ss |
| **Prompt original** | Conteúdo completo | Texto entre triple backticks | Preservar formatação original |

**Exemplo completo:**

```markdown
## Prompt: Implementar Manufacturing Compliance Score Engine
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar o Manufacturing Compliance Score Engine que calcula um score de 0-100 baseado em regras determinísticas. O score deve classificar em ACCEPTABLE (80-100), WARNING (60-79) ou CRITICAL (0-59). Usar as variáveis: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed.
```
```

### Critérios de Filtragem de Prompts

#### Prompts que NÃO devem ser registrados

| Tipo | Exemplo | Motivo | Ação |
|---|---|---|---|
| Confirmações simples | "sim", "ok", "entendido" | Ruído nos logs | Filtrar automaticamente |
| Respostas muito curtas | "próximo", "continue" | Sem valor informativo | Filtrar automaticamente |
| Comandos de navegação | "voltar", "ir para", "sair" | Não são prompts reais | Filtrar automaticamente |
| Respostas vazias | "" | Sem conteúdo | Filtrar automaticamente |
| Duplicatas | Mesmo prompt repetido | Evitar redundância | Filtrar manualmente |

**Critério de mínimo:**
- Prompts com **menos de 10 caracteres** são automaticamente filtrados
- Prompts **sem conteúdo** são automaticamente filtrados
- **Confirmações simples** são automaticamente filtradas

#### Prompts que DEVEM ser registrados

| Tipo | Exemplo | Motivo | Prioridade |
|---|---|---|---|
| Instruções de implementação | "Implementar endpoint de upload" | Decisão técnica | Alta |
| Pedidos de análise | "Analisar este código" | Análise de qualidade | Alta |
| Correções de bugs | "Corrigir erro de validação" | Rastreabilidade de fixes | Alta |
| Refatorações | "Refatorar este módulo" | Melhorias de código | Média |
| Documentação | "Documentar esta função" | Documentação viva | Média |
| Perguntas técnicas | "Como implementar JWT?" | Decisões arquiteturais | Média |
| Testes | "Criar testes para esta função" | Cobertura de testes | Média |

**Critério de significância:**
- Prompts com **10+ caracteres** são considerados significativos
- Prompts com **conteúdo técnico** são sempre registrados
- Prompts que **geram código ou documentação** são sempre registrados

### Exemplo de Arquivo de Log Completo

```markdown
# Prompt Logs: feature-compliance-score

Histórico de prompts executados no Kiro nesta branch.

---

## Prompt: Implementar Manufacturing Compliance Score Engine
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar o Manufacturing Compliance Score Engine que calcula um score de 0-100 baseado em regras determinísticas. O score deve classificar em ACCEPTABLE (80-100), WARNING (60-79) ou CRITICAL (0-59). Usar as variáveis: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed.
```

---

## Prompt: Criar testes unitários para compliance score
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 15:12:45 (Brasília - UTC-3)

### Prompt original
```
Criar testes unitários com pytest para validar o cálculo do compliance score. Incluir testes para:
1. Score calculado corretamente
2. Classificação correta (ACCEPTABLE/WARNING/CRITICAL)
3. Tratamento de valores fora do range
4. Edge cases (valores nulos, zeros, máximos)
```

---

## Prompt: Adicionar validação de ranges de sensores
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 16:45:30 (Brasília - UTC-3)

### Prompt original
```
Adicionar validação de ranges para cada sensor:
- Temperature: 20-45°C
- pH: 4.0-9.0
- Dissolved Oxygen: 0-100%
- Pressure: 0-10 bar
- Agitator Speed: 0-500 RPM

Rejeitar batches que não atendem aos ranges.
```

---
```

---

## 📋 Referência Rápida - Convenções de Logging

### Checklist de Conformidade

Ao criar um novo log, verificar:

- [ ] **Nome do arquivo**: `<tipo>-<nome>.md` (minúsculas, sem espaços)
- [ ] **Tipo de branch**: feature/, bugfix/, hotfix/, release/, chore/, docs/, main, develop
- [ ] **Conversão de `/`**: Convertido para `-` (ex: `feature/auth` → `feature-auth.md`)
- [ ] **Título do prompt**: Máx 80 caracteres, descritivo
- [ ] **Responsável**: Nome do usuário Git (usar `git config user.name`)
- [ ] **Branch**: Nome exato (usar `git rev-parse --abbrev-ref HEAD`)
- [ ] **Data/hora**: `YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)`
- [ ] **Prompt original**: Conteúdo completo entre triple backticks
- [ ] **Filtro trivial**: Prompt tem 10+ caracteres e é significativo
- [ ] **Sem dados sensíveis**: Nenhuma senha, token ou chave no log

### Matriz de Tipos de Branch

| Tipo | Padrão | Exemplo | Arquivo |
|---|---|---|---|
| Feature | `feature/<nome>` | `feature/compliance-score` | `feature-compliance-score.md` |
| Bugfix | `bugfix/<nome>` | `bugfix/validation-error` | `bugfix-validation-error.md` |
| Hotfix | `hotfix/<nome>` | `hotfix/api-crash` | `hotfix-api-crash.md` |
| Release | `release/v<versão>` | `release/v1.0.0` | `release-v1.0.0.md` |
| Chore | `chore/<nome>` | `chore/update-deps` | `chore-update-deps.md` |
| Docs | `docs/<nome>` | `docs/api-guide` | `docs-api-guide.md` |
| Main | `main` | - | `main.md` |
| Develop | `develop` | - | `develop.md` |

### Formato de Timestamp - Referência

```
Correto:   2026-05-27 14:35:22 (Brasília - UTC-3)
Errado:    2026-05-27 14:35:22 (UTC)
Errado:    27/05/2026 14:35:22
Errado:    2026-05-27T14:35:22Z
```

### Estrutura de Metadados - Template

```markdown
## Prompt: <título em até 80 caracteres>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```
```

### Critérios de Filtragem - Decisão Rápida

| Pergunta | Sim | Não |
|---|---|---|
| Tem 10+ caracteres? | ✅ Registrar | ❌ Filtrar |
| É uma confirmação simples? | ❌ Filtrar | ✅ Registrar |
| Tem conteúdo técnico? | ✅ Registrar | ❌ Filtrar |
| Gera código/docs? | ✅ Registrar | ❌ Filtrar |
| É um comando de navegação? | ❌ Filtrar | ✅ Registrar |

---

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

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Windows PowerShell:**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Ver logs de branch específica:**

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/feature-compliance-score.md
```

**Windows:**
```cmd
type .kiro\prompt-logs\feature-compliance-score.md
```

**Últimas entradas:**

**Mac/Linux:**
```bash
tail -n 50 .kiro/prompt-logs/<branch>.md
```

**Windows PowerShell:**
```powershell
Get-Content ".kiro\prompt-logs\<branch>.md" -Tail 50
```

**Buscar por palavra-chave:**

**Mac/Linux:**
```bash
grep -i "compliance" .kiro/prompt-logs/*.md
```

**Windows PowerShell:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

---

## 🎯 Boas Práticas para o Agente Kiro

Ao trabalhar com prompt logging, seguir estas práticas:

### 1. **Não Modificar Formato de Log**
- Manter consistência para parsing futuro
- Sempre usar o formato padrão
- Não editar manualmente arquivos de log
- Preservar estrutura de metadados

### 2. **Tratar Erros Graciosamente**
- Nunca bloquear execução do Kiro
- Se logging falhar, continuar com a tarefa
- Registrar erros em logs do Kiro, não interromper
- Falhas de logging não devem impedir desenvolvimento

### 3. **Preservar Histórico**
- Sempre usar append, nunca sobrescrever
- Manter histórico completo de todas as interações
- Não deletar ou limpar logs
- Versionar logs junto com código

### 4. **Sanitizar Nomes de Branch**
- Converter `/` em `-`
- Converter caracteres especiais em `-`
- Exemplo: `feature/auth-v2` → `feature-auth-v2.md`
- Sempre em minúsculas

### 5. **Documentar Limitações**
- Ser transparente sobre o que não é capturado
- Se conteúdo não for capturado, registrar metadados
- Não gerar entradas vazias
- Indicar quando há limitações de captura

### 6. **Filtrar Prompts Triviais**
- Não registrar confirmações simples (sim, não, ok)
- Não registrar respostas muito curtas (< 10 caracteres)
- Não registrar comandos de navegação (next, back, continue)
- Justificativa: Manter logs focados em interações significativas

### 7. **Fazer Commits Regulares**
- Versionar logs junto com o código
- Exemplo: `git add .kiro/prompt-logs/`
- Commit: `docs: adiciona prompts de implementação`
- Incluir referência ao log em mensagens de commit

### 8. **Referenciar Logs em Commits**
- Quando código é gerado por IA, referenciar o log
- Exemplo: `feat(ml): implementa RandomForest (prompts em .kiro/prompt-logs/feature-ml.md)`
- Facilita rastreabilidade e code reviews
- Documenta decisões técnicas

### 9. **Usar Timestamp Correto**
- Sempre usar timezone de Brasília (UTC-3)
- Formato: `YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)`
- Nunca usar UTC ou outros timezones
- Verificar se timestamp está correto antes de registrar

### 10. **Manter Metadados Consistentes**
- Sempre incluir todos os 5 campos obrigatórios
- Usar nomes de usuário consistentes
- Usar nomes de branch exatos
- Não abreviar ou modificar metadados

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

## 🔧 Manutenção do Sistema

### Backup Automático

Banco de dados é automaticamente feito backup diariamente em:

```
.kiro/prompt-logs/backups/backup-YYYYMMDD-HHMMSS.md
```

Retenção: 30 dias

### Backup Manual

**Mac/Linux:**
```bash
mkdir -p backups
cp -r .kiro/prompt-logs backups/prompt-logs-$(date +%Y%m%d-%H%M%S)
```

**Windows PowerShell:**
```powershell
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item -Path ".kiro\prompt-logs" -Destination "backups\prompt-logs-$timestamp" -Recurse
```

### Restaurar Backup

**Mac/Linux:**
```bash
cp -r backups/prompt-logs-YYYYMMDD-HHMMSS/* .kiro/prompt-logs/
```

**Windows PowerShell:**
```powershell
Copy-Item -Path "backups\prompt-logs-YYYYMMDD-HHMMSS\*" -Destination ".kiro\prompt-logs" -Recurse -Force
```

### Limpeza de Logs Antigos

**Remover entradas duplicadas:**

**Mac/Linux:**
```bash
# Verificar duplicatas
grep -n "## Prompt:" .kiro/prompt-logs/feature-*.md | sort | uniq -d

# Remover manualmente (editar arquivo)
```

**Remover prompts triviais não capturados:**

**Mac/Linux:**
```bash
# Buscar linhas vazias ou muito curtas
grep -E "^$|^.{1,5}$" .kiro/prompt-logs/*.md

# Remover manualmente
```

---

## 📊 Análise de Logs

### Contar Prompts por Branch

**Mac/Linux:**
```bash
for file in .kiro/prompt-logs/*.md; do
  echo "$(basename $file): $(grep -c "## Prompt:" $file)"
done
```

**Windows PowerShell:**
```powershell
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $count = (Select-String -Path $_.FullName -Pattern "## Prompt:" | Measure-Object).Count
  Write-Host "$($_.Name): $count"
}
```

### Contar Prompts por Desenvolvedor

**Mac/Linux:**
```bash
grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq -c | sort -rn
```

**Windows PowerShell:**
```powershell
$users = @{}
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: (.+)" | 
  ForEach-Object { 
    $user = $_.Matches.Groups[1].Value
    if ($users.ContainsKey($user)) { $users[$user]++ } 
    else { $users[$user] = 1 }
  }
$users.GetEnumerator() | Sort-Object Value -Descending | 
  ForEach-Object { Write-Host "$($_.Key): $($_.Value)" }
```

### Gerar Relatório de Atividade

**Mac/Linux:**
```bash
cat > activity-report.sh << 'EOF'
#!/bin/bash
echo "# Relatório de Atividade - Prompt Logging"
echo ""
echo "## Resumo Geral"
echo "- Total de prompts: $(grep -c "## Prompt:" .kiro/prompt-logs/*.md)"
echo "- Branches ativas: $(ls -1 .kiro/prompt-logs/*.md | wc -l)"
echo "- Período: $(date)"
echo ""

echo "## Prompts por Desenvolvedor"
grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq -c | sort -rn

echo ""
echo "## Prompts por Branch"
for file in .kiro/prompt-logs/*.md; do
  count=$(grep -c "## Prompt:" "$file" 2>/dev/null || echo 0)
  branch=$(basename "$file" .md)
  echo "- $branch: $count prompts"
done | sort -t: -k2 -rn
EOF
chmod +x activity-report.sh
./activity-report.sh > activity-report.md
```

---

## 💡 Contexto para Desenvolvimento

Quando trabalhar em tarefas do BiotecPredict:

1. **Submeter prompts normalmente** - Sistema captura automaticamente
2. **Consultar logs de features anteriores** - Reutilizar padrões bem-sucedidos
3. **Referenciar logs em PRs** - Facilitar code reviews
4. **Manter logs versionados** - Fazer commit junto com código
5. **Usar logs para documentação** - Complementar documentação técnica

---

## 📚 Referências

| Referência | Localização | Conteúdo |
|---|---|---|
| **Documentação Completa** | `docs/prompt-logging.md` | Guia detalhado com exemplos |
| **Spec Completa** | `.kiro/specs/prompt-logging/` | Especificação técnica |
| **Git Flow** | `.kiro/steering/gitflow.md` | Convenções de branches e commits |
| **Localização** | `.kiro/steering/localizacao.md` | Timezone e formato de datas |
| **Tech Stack** | `.kiro/steering/tech.md` | Tecnologias utilizadas |
| **Estrutura** | `.kiro/steering/structure.md` | Estrutura do projeto |

---

## 🚀 Próximos Passos

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

**Versão**: 0.4.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Convenções de Logging Documentadas  
**Timezone**: America/Sao_Paulo (UTC-3)  
**Idioma**: Português Brasileiro (pt-BR)

---

## 📌 Resumo Executivo - Convenções de Logging

### O que é Prompt Logging?

Sistema automático que registra todos os prompts executados no Kiro, organizados por branch Git, com metadados completos (usuário, branch, timestamp) para rastreabilidade, auditoria e documentação viva.

### Por que é Importante?

- **Auditoria**: Registro documentado de todas as decisões ao agente
- **Reprodutibilidade**: Entender contexto e decisões que levaram a implementações
- **Qualidade**: Avaliar efetividade de instruções e padrões de uso
- **Documentação Viva**: Histórico executável que complementa documentação técnica
- **Aprendizado**: Analisar prompts bem-sucedidos para melhorar futuras interações

### Convenções Principais

#### 1. Nomes de Arquivo por Tipo de Branch

```
feature/compliance-score      → feature-compliance-score.md
bugfix/validation-error       → bugfix-validation-error.md
hotfix/api-crash             → hotfix-api-crash.md
release/v1.0.0               → release-v1.0.0.md
chore/update-deps            → chore-update-deps.md
docs/api-guide               → docs-api-guide.md
main                         → main.md
develop                      → develop.md
```

**Regra**: Converter `/` em `-`, sempre minúsculas, sem espaços

#### 2. Timestamp em Brasília (UTC-3)

```
Formato: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)
Exemplo: 2026-05-27 14:35:22 (Brasília - UTC-3)
```

**Regra**: Sempre incluir timezone, nunca usar UTC ou outros timezones

#### 3. Estrutura de Metadados Obrigatória

```markdown
## Prompt: <título até 80 caracteres>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo>
```
```

**Regra**: Todos os 5 campos são obrigatórios

#### 4. Filtragem de Prompts Triviais

**Não registrar:**
- Confirmações simples (sim, ok, entendido)
- Respostas muito curtas (< 10 caracteres)
- Comandos de navegação (próximo, voltar, sair)
- Respostas vazias

**Registrar:**
- Instruções de implementação
- Pedidos de análise
- Correções de bugs
- Refatorações
- Documentação

**Regra**: Prompts com 10+ caracteres e conteúdo técnico são significativos

### Boas Práticas Essenciais

1. ✅ Usar formato padrão sempre
2. ✅ Preservar histórico completo
3. ✅ Sanitizar nomes de branch
4. ✅ Usar timestamp correto
5. ✅ Manter metadados consistentes
6. ✅ Filtrar prompts triviais
7. ✅ Fazer commits regulares
8. ✅ Referenciar logs em PRs
9. ✅ Tratar erros graciosamente
10. ✅ Documentar limitações

### Localização dos Logs

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-*.md              # Logs de features
├── bugfix-*.md               # Logs de bugfixes
├── hotfix-*.md               # Logs de hotfixes
├── release-*.md              # Logs de releases
├── chore-*.md                # Logs de chores
└── docs-*.md                 # Logs de documentação
```

### Próximos Passos

1. **Usar automaticamente**: Prompts são capturados via hook `promptSubmit`
2. **Consultar logs**: Ver histórico de prompts por branch
3. **Referenciar em PRs**: Incluir link para logs em descrições de PR
4. **Analisar padrões**: Identificar prompts bem-sucedidos
5. **Documentar decisões**: Usar logs como documentação viva

---

## 📚 Referências Relacionadas

| Documento | Localização | Conteúdo |
|---|---|---|
| **Documentação Completa** | `docs/prompt-logging.md` | Guia detalhado com exemplos |
| **Spec Completa** | `.kiro/specs/prompt-logging/` | Especificação técnica |
| **Git Flow** | `.kiro/steering/gitflow.md` | Convenções de branches e commits |
| **Localização** | `.kiro/steering/localizacao.md` | Timezone e formato de datas |
| **Tech Stack** | `.kiro/steering/tech.md` | Tecnologias utilizadas |
| **Estrutura** | `.kiro/steering/structure.md` | Estrutura do projeto |

---

**Versão**: 0.4.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Convenções de Logging Documentadas  
**Timezone**: America/Sao_Paulo (UTC-3)  
**Idioma**: Português Brasileiro (pt-BR)
