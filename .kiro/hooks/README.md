# Hooks - BiotecPredict

Automação de tarefas através de hooks do Kiro. Disparados por eventos do IDE.

## 📋 Hooks Implementados

### 1. Prompt Logger ✅
**Arquivo**: `prompt-logger.json`  
**Evento**: `promptSubmit`  
**Ação**: `runCommand`  
**Script**: `python3 .kiro/scripts/log_prompt.py`

**Propósito**: Registra automaticamente prompts executados no Kiro  
**Saída**: `.kiro/prompt-logs/<branch>.md`

**Funcionalidades**:
- Captura automática de prompts
- Organização por branch Git
- Timestamp em horário Brasília
- Filtragem de prompts triviais
- Rastreabilidade completa

---

### 2. Generate Tests with AI ✅
**Arquivo**: `generate-tests.json`  
**Evento**: `postToolUse`  
**Tipo de Ferramenta**: `write`  
**Ação**: `askAgent`

**Propósito**: Gera automaticamente testes com IA para código novo  
**Frameworks**: pytest (backend), Vitest (frontend)

**Funcionalidades**:
- Testes unitários automáticos
- Testes de edge cases
- Testes de integração
- Testes E2E para fluxos
- Cobertura mínima: 70%

---

### 3. Generate Documentation ✅
**Arquivo**: `generate-docs.json`  
**Evento**: `postToolUse`  
**Tipo de Ferramenta**: `write`  
**Ação**: `askAgent`

**Propósito**: Gera automaticamente documentação com IA  
**Saídas**: Docstrings, API docs, README, diagramas

**Funcionalidades**:
- Docstrings em todas as funções
- Atualização de README
- Documentação de API (Swagger)
- Diagramas de arquitetura
- Padrão português brasileiro

---

### 4. Validate Data Quality ✅
**Arquivo**: `debug-prompt.json` (renomeado)  
**Evento**: `preToolUse`  
**Tipo de Ferramenta**: `.*sql.*|.*database.*`  
**Ação**: `askAgent`

**Propósito**: Valida qualidade de dados antes de persistência  
**Ranges Validados**:
- Temperature: 20-45°C
- pH: 4.0-9.0
- Dissolved Oxygen: 0-100%
- Pressure: 0-10 bar
- Agitator Speed: 0-500 RPM

**Funcionalidades**:
- Validação de ranges
- Detecção de outliers
- Verificação de mínimo de leituras (≥5)
- Rejeição de dados inválidos
- Logs de auditoria

---

### 5. Code Quality Check ✅
**Arquivo**: `code-quality-check.json`  
**Evento**: `preToolUse`  
**Tipo de Ferramenta**: `write`  
**Ação**: `askAgent`

**Propósito**: Verifica qualidade de código antes de commit  
**Validações**:
- Lint (flake8 backend, ESLint frontend)
- Type hints em Python
- Docstrings em todas as funções
- Sem secrets ou dados sensíveis

**Funcionalidades**:
- Verificação de padrões de código
- Clean Architecture
- Separação de responsabilidades
- Rejeição de código de baixa qualidade

---

### 6. Validate Compliance Score ✅
**Arquivo**: `validate-compliance.json`  
**Evento**: `postToolUse`  
**Tipo de Ferramenta**: `.*compliance.*|.*score.*`  
**Ação**: `askAgent`

**Propósito**: Valida cálculos de compliance score  
**Classificações**:
- ACCEPTABLE: 80-100
- WARNING: 60-79
- CRITICAL: 0-59

**Funcionalidades**:
- Validação de range (0-100)
- Verificação de classificação
- Rastreamento de cálculos
- Validação de regras
- Logs de auditoria

---

### 7. Generate Quality Reports ✅
**Arquivo**: `generate-reports.json`  
**Evento**: `agentStop`  
**Ação**: `askAgent`

**Propósito**: Gera automaticamente relatórios de qualidade  
**Relatórios**:
- Validação de dados
- Compliance score
- Rastreabilidade completa

**Funcionalidades**:
- Relatórios em Markdown
- Timestamp Brasília
- Versionamento automático
- Salvo em `backend/reports/`

---

## 🔧 Configuração

### Estrutura de Hook
```json
{
  "name": "Hook Name",
  "version": "1.0.0",
  "description": "Descrição do hook",
  "when": {
    "type": "promptSubmit|postToolUse|preToolUse|agentStop|...",
    "toolTypes": "write|read|*|regex",
    "patterns": ["*.ts", "*.py"]
  },
  "then": {
    "type": "askAgent|runCommand",
    "prompt": "Instruções para o agente",
    "command": "Comando a executar"
  }
}
```

### Tipos de Evento
- `promptSubmit` - Quando prompt é submetido
- `preToolUse` - Antes de ferramenta ser executada
- `postToolUse` - Depois de ferramenta ser executada
- `agentStop` - Quando agente para execução
- `fileEdited` - Quando arquivo é editado
- `fileCreated` - Quando arquivo é criado

### Tipos de Ação
- `askAgent` - Envia mensagem ao agente
- `runCommand` - Executa comando shell

---

## 🚀 Como Usar

### Ativar Hook
1. Criar arquivo JSON em `.kiro/hooks/`
2. Seguir schema de configuração
3. Reiniciar Kiro
4. Hook será disparado automaticamente

### Desativar Hook
1. Renomear arquivo (ex: `hook.json.bak`)
2. Ou deletar arquivo
3. Reiniciar Kiro

### Testar Hook
1. Executar ação que dispara o hook
2. Verificar logs do Kiro
3. Validar saída esperada

---

## 📊 Fluxo de Execução

```
Evento do Kiro
    ↓
Hook detecta evento
    ↓
Verifica condições (when)
    ↓
Executa ação (then)
    ├─ askAgent: Envia prompt ao agente
    └─ runCommand: Executa script
    ↓
Resultado registrado
```

---

## ⚠️ Boas Práticas

1. **Não bloquear execução** - Hooks devem ser rápidos
2. **Tratamento de erros** - Sempre implementar fallback
3. **Documentação** - Documentar propósito de cada hook
4. **Versionamento** - Manter versão atualizada
5. **Testes** - Testar em diferentes cenários
6. **Logs** - Registrar execução para debugging

---

## 🔍 Troubleshooting

### Hook não dispara
- Verificar se arquivo JSON está válido
- Verificar se evento está correto
- Reiniciar Kiro
- Verificar logs do Kiro

### Hook dispara mas não executa
- Verificar se script/comando existe
- Verificar permissões de execução
- Verificar se dependências estão instaladas
- Verificar logs de erro

### Circular dependency
- Evitar hooks que disparam outros hooks infinitamente
- Exemplo: preToolUse → askAgent → Tool → preToolUse (loop)
- Solução: Usar diferentes tipos de ferramenta

---

## 📚 Referências

- **Steering**: `.kiro/steering/prompt-logging.md`
- **Scripts**: `.kiro/scripts/`
- **Specs**: `.kiro/specs/`
- **Logs**: `.kiro/prompt-logs/`

---

## 📈 Roadmap de Hooks

| Hook | Status | Sprint | Propósito |
|------|--------|--------|----------|
| Prompt Logger | ✅ | 0 | Logging de prompts |
| Generate Tests | ✅ | 1 | Testes com IA |
| Generate Docs | ✅ | 1 | Documentação com IA |
| Validate Data | ✅ | 1 | Validação de dados |
| Code Quality | ✅ | 1 | Qualidade de código |
| Validate Compliance | ✅ | 3 | Validação de compliance |
| Generate Reports | ✅ | 5 | Relatórios automáticos |

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ 7 Hooks Implementados
