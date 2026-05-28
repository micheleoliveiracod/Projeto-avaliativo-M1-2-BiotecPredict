# Specs - BiotecPredict

Documentação de especificações, requisitos, design e tarefas de implementação do projeto BiotecPredict.

## 📋 Estrutura

```
.kiro/specs/
├── .config.kiro              # Configuração central de specs
├── README.md                 # Este arquivo
├── requirements.md           # Requisitos gerais do projeto
├── design.md                 # Design geral do projeto
├── tasks.md                  # Tarefas de implementação
└── prompt-logging/           # Spec de prompt logging
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

## 🎯 Specs Ativas

### 1. Prompt Logging ✅ (Concluído)
- **Status**: Completed
- **Sprint**: Pre-Sprint (Fase 0)
- **Objetivo**: Sistema automático de logging de prompts com rastreabilidade
- **Arquivos**: `.kiro/specs/prompt-logging/`

### 2. Backend API 🔄 (Em Progresso)
- **Status**: In Progress
- **Sprint**: Sprint 1 (27/05/2026)
- **Objetivo**: API FastAPI com modelos, schemas e endpoints
- **Requisitos**: Upload CSV, processamento de batch, persistência PostgreSQL

### 3. Frontend Dashboard ⏳ (Pendente)
- **Status**: Pending
- **Sprint**: Sprint 2 (28/05/2026)
- **Objetivo**: Dashboard React com visualizações e upload
- **Requisitos**: Upload interface, KPIs, gráficos, tabela de batches

### 4. ML & Compliance Score ⏳ (Pendente)
- **Status**: Pending
- **Sprint**: Sprint 3 (29/05/2026)
- **Objetivo**: Machine Learning e cálculo de compliance score
- **Requisitos**: RandomForest, compliance engine, predição de risco

### 5. Data Validation ⏳ (Pendente)
- **Status**: Pending
- **Sprint**: Sprint 5 (31/05/2026)
- **Objetivo**: Scripts de validação e qualidade de dados
- **Requisitos**: Validação de ranges, detecção de outliers, relatórios

## 🔍 Correctness Properties

O projeto define 5 propriedades de correção que devem ser validadas:

1. **Data Validation** - Dados dentro dos ranges esperados
2. **Compliance Score Range** - Score entre 0-100
3. **Classification Correctness** - Classificação corresponde ao score
4. **Minimum Readings** - Mínimo de 5 leituras por batch
5. **Prediction Consistency** - Predições consistentes com dados

## 📝 Como Usar

### Criar Nova Spec
1. Criar diretório: `.kiro/specs/<feature-name>/`
2. Criar arquivos: `requirements.md`, `design.md`, `tasks.md`
3. Atualizar `.config.kiro` com nova spec
4. Documentar correctness properties

### Atualizar Spec Existente
1. Editar arquivo correspondente (requirements.md, design.md, ou tasks.md)
2. Manter versionamento em `.config.kiro`
3. Fazer commit com mensagem clara

### Validar Spec
```bash
# Verificar formato
python .kiro/scripts/validate_spec.py <spec-name>

# Gerar relatório
python .kiro/scripts/generate_spec_report.py
```

## 🔗 Referências

- **Steering Files**: `.kiro/steering/` - Contexto permanente
- **Hooks**: `.kiro/hooks/` - Automação de tarefas
- **Scripts**: `.kiro/scripts/` - Utilitários
- **Prompt Logs**: `.kiro/prompt-logs/` - Histórico de prompts

## 📊 Status Geral

| Spec | Status | Sprint | Progresso |
|------|--------|--------|-----------|
| Prompt Logging | ✅ Completed | 0 | 100% |
| Backend API | 🔄 In Progress | 1 | 0% |
| Frontend Dashboard | ⏳ Pending | 2 | 0% |
| ML & Compliance | ⏳ Pending | 3 | 0% |
| Data Validation | ⏳ Pending | 5 | 0% |

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Specs Estruturadas
