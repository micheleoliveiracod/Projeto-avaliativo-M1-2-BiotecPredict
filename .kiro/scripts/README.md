# Scripts - BiotecPredict

Utilitários e scripts de automação para o projeto BiotecPredict.

## 📋 Scripts Disponíveis

### 1. Prompt Logging
**Arquivo**: `log_prompt.py`  
**Propósito**: Registra automaticamente prompts executados no Kiro  
**Trigger**: Hook `promptSubmit`  
**Saída**: `.kiro/prompt-logs/<branch>.md`

```bash
python .kiro/scripts/log_prompt.py
```

**Funcionalidades**:
- Captura automática de prompts
- Detecção de branch Git
- Timestamp em horário Brasília (UTC-3)
- Filtragem de prompts triviais
- Rastreabilidade completa

---

### 2. Data Validation
**Arquivo**: `validate_data.py`  
**Propósito**: Valida qualidade de dados imputados  
**Ranges**:
- Temperature: 20-45°C
- pH: 4.0-9.0
- Dissolved Oxygen: 0-100%
- Pressure: 0-10 bar
- Agitator Speed: 0-500 RPM

```bash
python .kiro/scripts/validate_data.py
```

**Funcionalidades**:
- Validação de ranges
- Detecção de outliers (desvio padrão)
- Verificação de mínimo de leituras (≥5)
- Relatórios JSON com rastreabilidade
- Salva em `backend/reports/validation_*.json`

---

### 3. Compliance Score Validation
**Arquivo**: `validate_compliance.py`  
**Propósito**: Valida cálculos de compliance score  
**Classificações**:
- ACCEPTABLE: 80-100
- WARNING: 60-79
- CRITICAL: 0-59

```bash
python .kiro/scripts/validate_compliance.py
```

**Funcionalidades**:
- Validação de range (0-100)
- Verificação de classificação
- Rastreamento de cálculos
- Validação de regras aplicadas
- Relatórios JSON com auditoria

---

### 4. Spec Validation
**Arquivo**: `validate_spec.py`  
**Propósito**: Valida formato e completude de specs  
**Uso**:

```bash
python .kiro/scripts/validate_spec.py <spec-name>
python .kiro/scripts/validate_spec.py prompt-logging
```

**Valida**:
- Existência de arquivos (requirements.md, design.md, tasks.md)
- Presença de seções obrigatórias
- Formato Markdown
- Completude de documentação

---

## 🔧 Configuração

### Dependências Python
```bash
pip install pytz  # Para timezone handling
```

### Variáveis de Ambiente
```bash
KIRO_PROMPT=<prompt-content>  # Captura de prompt (opcional)
```

---

## 📊 Saídas Geradas

### Logs de Prompts
**Localização**: `.kiro/prompt-logs/<branch>.md`  
**Formato**: Markdown com metadados  
**Conteúdo**: Prompts com timestamp, usuário, branch

### Relatórios de Validação
**Localização**: `backend/reports/`  
**Formato**: JSON com versionamento  
**Nomes**:
- `validation_YYYYMMDD_HHMMSS.json` - Validação de dados
- `compliance_YYYYMMDD_HHMMSS.json` - Validação de compliance

---

## 🚀 Integração com Hooks

Os scripts são automaticamente disparados por hooks do Kiro:

| Hook | Script | Evento |
|------|--------|--------|
| `prompt-logger.json` | `log_prompt.py` | promptSubmit |
| `validate-data.json` | `validate_data.py` | preToolUse (database) |
| `validate-compliance.json` | `validate_compliance.py` | postToolUse (compliance) |

---

## 🧪 Testes

### Testar Logging de Prompts
```bash
python .kiro/scripts/log_prompt.py
# Verifica: Branch, usuário, timestamp, arquivo criado
```

### Testar Validação de Dados
```bash
python .kiro/scripts/validate_data.py
# Gera relatório de teste em backend/reports/
```

### Testar Validação de Compliance
```bash
python .kiro/scripts/validate_compliance.py
# Gera relatório de teste em backend/reports/
```

### Testar Validação de Specs
```bash
python .kiro/scripts/validate_spec.py prompt-logging
# Valida estrutura da spec
```

---

## 📝 Boas Práticas

1. **Executar scripts localmente** antes de fazer commit
2. **Verificar saídas** em `.kiro/prompt-logs/` e `backend/reports/`
3. **Manter scripts simples** - sem dependências externas pesadas
4. **Documentar mudanças** em README.md
5. **Versionar scripts** com comentários de data/versão

---

## 🔍 Troubleshooting

### Script não encontra pytz
```bash
pip install pytz>=2024.1
```

### Permissão negada ao executar
```bash
chmod +x .kiro/scripts/*.py
```

### Relatórios não são salvos
- Verificar se `backend/reports/` existe
- Verificar permissões de escrita
- Verificar espaço em disco

---

## 📚 Referências

- **Steering**: `.kiro/steering/prompt-logging.md`
- **Hooks**: `.kiro/hooks/`
- **Specs**: `.kiro/specs/`
- **Logs**: `.kiro/prompt-logs/`

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Scripts Documentados
