# Scripts - BiotecPredict

Scripts de automação e utilitários para o projeto Kiro.

## 📁 Estrutura

```
.kiro/scripts/
├── log_prompt.py              # Logging automático de prompts
├── validate_markdown_logs.py  # Validação de logs markdown
└── README.md                  # Este arquivo
```

## 🎯 Scripts Disponíveis

### `log_prompt.py`

**Propósito**: Capturar e registrar prompts executados no Kiro automaticamente.

**Acionamento**: Hook `promptSubmit` em `.kiro/hooks/prompt-logger.json`

**Funcionalidades**:
- Coleta metadados (usuário Git, branch, timestamp)
- Extrai conteúdo do prompt
- Formata entrada markdown
- Persiste em `.kiro/prompt-logs/<branch>.md`
- Filtra prompts triviais (< 10 caracteres)

**Uso Manual**:
```bash
python .kiro/scripts/log_prompt.py --prompt "seu prompt aqui"
```

**Saída**: Arquivo `.kiro/prompt-logs/<branch-atual>.md` atualizado

---

### `validate_markdown_logs.py`

**Propósito**: Validar integridade e formato dos logs markdown.

**Funcionalidades**:
- Verifica estrutura de metadados obrigatória
- Valida timestamps em formato correto
- Detecta duplicatas de prompts
- Gera relatório de validação

**Uso**:
```bash
python .kiro/scripts/validate_markdown_logs.py
```

**Saída**: Relatório de validação no console

---

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Timezone (padrão: America/Sao_Paulo)
export TZ=America/Sao_Paulo

# Diretório de logs (padrão: .kiro/prompt-logs/)
export KIRO_LOGS_DIR=.kiro/prompt-logs
```

### Dependências

```bash
# Instalar dependências
pip install pytz python-dotenv

# Ou via requirements
pip install -r requirements.txt
```

---

## 📋 Convenções

### Timestamp Obrigatório

Formato: `YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)`

Exemplo: `2026-05-27 14:35:22 (Brasília - UTC-3)`

**Regra**: Sempre usar timezone de Brasília (UTC-3), nunca UTC ou outros timezones.

### Metadados Obrigatórios

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

### Filtro de Prompts Triviais

**Não registrar**:
- Confirmações simples (sim, ok, entendido)
- Respostas muito curtas (< 10 caracteres)
- Comandos de navegação (próximo, voltar, sair)
- Respostas vazias

**Registrar**:
- Instruções de implementação
- Pedidos de análise
- Correções de bugs
- Refatorações
- Documentação

---

## 🚀 Boas Práticas

✅ **Fazer**:
- Usar scripts via hooks automáticos
- Manter logs versionados no Git
- Referenciar logs em PRs
- Validar logs regularmente

❌ **Não fazer**:
- Editar logs manualmente
- Deletar histórico de prompts
- Commitar secrets nos logs
- Modificar formato de metadados

---

## 📊 Monitoramento

### Verificar Logs da Branch Atual

```bash
# Windows PowerShell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"

# Mac/Linux
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

### Contar Prompts por Branch

```bash
# Windows PowerShell
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $count = (Select-String -Path $_.FullName -Pattern "## Prompt:" | Measure-Object).Count
  Write-Host "$($_.Name): $count"
}

# Mac/Linux
for file in .kiro/prompt-logs/*.md; do
  echo "$(basename $file): $(grep -c "## Prompt:" $file)"
done
```

### Validar Integridade

```bash
python .kiro/scripts/validate_markdown_logs.py
```

---

## 🔐 Segurança

- ✅ Nunca commitar secrets em logs
- ✅ Usar `.env` para variáveis sensíveis
- ✅ Manter `.env` no `.gitignore`
- ✅ Sanitizar dados sensíveis antes de logar

---

## 📚 Referências

- Documentação de Prompt Logging: `.kiro/steering/prompt-logging.md`
- Convenções de Localização: `.kiro/steering/localizacao.md`
- Git Flow: `.kiro/steering/gitflow.md`

---

**Versão**: 1.0.0  
**Status**: ✅ Ativo  
**Timezone**: America/Sao_Paulo (UTC-3)
