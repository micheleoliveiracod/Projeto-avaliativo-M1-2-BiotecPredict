# Estrutura do Projeto - BiotecPredict

Organização de diretórios: backend Python (processamento, ML e API) e frontend React (dashboard e visualizações).

---

## Estrutura de Diretórios

```
/
├── backend/
│   ├── api/                         # API REST endpoints
│   │   ├── routes/
│   │   │   ├── batch.py             # POST /upload, GET /batches, GET /batch/{id}
│   │   │   ├── prediction.py        # GET /prediction/{batch_id}
│   │   │   └── compliance.py        # GET /compliance/{batch_id}
│   │   └── main.py                  # Entry point da API
│   │
│   ├── colletors/                   # Coletores de dados (NOVO)
│   │   └── .gitkeep                 # Placeholder para coletores de dados
│   │
│   ├── processors/                  # Processamento de dados
│   │   ├── csv_processor.py         # Leitura e parsing de CSV
│   │   ├── data_validator.py        # Validação de ranges
│   │   └── data_cleaner.py          # Limpeza de dados (nulos, outliers)
│   │
│   ├── services/                    # Lógica de negócio
│   │   ├── batch_service.py         # Gerenciamento de batches
│   │   ├── compliance_service.py    # Cálculo de compliance score
│   │   ├── ml_service.py            # Predição com RandomForest
│   │   └── data_service.py          # Acesso a dados
│   │
│   ├── models/                      # Modelos SQLAlchemy
│   │   ├── batch.py                 # Modelo Batch
│   │   ├── sensor_reading.py        # Modelo SensorReading
│   │   └── prediction.py            # Modelo Prediction
│   │
│   ├── schemas/                     # Schemas Pydantic
│   │   ├── batch.py                 # Schemas de batch
│   │   ├── prediction.py            # Schemas de predição
│   │   └── compliance.py            # Schemas de compliance
│   │
│   ├── db/                          # Banco de dados
│   │   ├── database.py              # Configuração PostgreSQL
│   │   └── repository.py            # Repository pattern
│   │
│   ├── ml/                          # Machine Learning
│   │   ├── model.py                 # RandomForestClassifier
│   │   ├── trainer.py               # Treinamento do modelo
│   │   └── predictor.py             # Predição
│   │
│   ├── scripts/                     # Scripts de validação (NOVO)
│   │   ├── validate_data.py         # Validação de qualidade de dados
│   │   └── validate_compliance.py   # Validação de cálculos de score
│   │
│   ├── reports/                     # Relatórios de validação (NOVO)
│   │   ├── data_quality_reports/    # Histórico de relatórios
│   │   └── validation_logs.db       # Versionamento de relatórios
│   │
│   ├── tests/
│   │   ├── pytest/
│   │   │   ├── test_batch_service.py
│   │   │   ├── test_compliance_service.py
│   │   │   └── test_ml_service.py
│   │   └── postman/
│   │       └── BiotecPredict.postman_collection.json
│   │
│   ├── requirements.txt
│   └── main.py                      # Entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/              # Componentes reutilizáveis
│   │   │   ├── UploadCard/
│   │   │   ├── ComplianceScoreCard/
│   │   │   ├── RiskPredictionCard/
│   │   │   ├── SensorChart/
│   │   │   └── BatchTable/
│   │   │
│   │   ├── pages/                   # Páginas da aplicação
│   │   │   ├── Dashboard/
│   │   │   ├── Upload/
│   │   │   ├── BatchDetails/
│   │   │   ├── Results/
│   │   │   └── Analytics/
│   │   │
│   │   ├── services/                # Serviços de API
│   │   │   ├── api.ts               # Cliente HTTP
│   │   │   ├── batchService.ts      # Operações de batch
│   │   │   └── predictionService.ts # Consulta de predições
│   │   │
│   │   ├── hooks/                   # Custom hooks React
│   │   ├── utils/                   # Funções auxiliares
│   │   ├── styles/                  # Estilos globais
│   │   └── App.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                            # Documentação do projeto
│   ├── diagrams/
│   │   ├── c4/                      # Diagramas C4
│   │   └── uml/                     # Diagramas UML
│   ├── mockups.md
│   ├── PRD.md
│   └── user_stories.md
│
├── project-planning/                # Planejamento do projeto (NOVO)
│   └── add_issues_to_project.py     # Script para criar issues no GitHub
│
├── deploy/                          # Configuração de deploy
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── .env.example
│
├── .kiro/                           # Configurações Kiro
│   ├── hooks/
│   ├── scripts/
│   ├── specs/
│   └── steering/                    # Contexto permanente
│
├── .env.example
├── README.md
└── LICENSE
```

---

## Responsabilidades por Camada

### `backend/colletors/`

Coletores de dados de diferentes fontes.

| Arquivo | Responsabilidade |
|---|---|
| (Placeholder para coletores futuros) | Integração com APIs externas, sensores, sistemas SCADA |

### `backend/processors/`

Processamento de dados brutos.

| Arquivo | Responsabilidade |
|---|---|
| `csv_processor.py` | Leitura e parsing de arquivos CSV |
| `data_validator.py` | Validação de ranges de valores |
| `data_cleaner.py` | Limpeza de dados (nulos, outliers) |

### `backend/services/`

Lógica de negócio e orquestração.

| Arquivo | Responsabilidade |
|---|---|
| `batch_service.py` | Gerenciamento de batches (CRUD) |
| `compliance_service.py` | Cálculo de Manufacturing Compliance Score |
| `ml_service.py` | Predição de risco com RandomForest |
| `data_service.py` | Acesso a dados do banco |

### `backend/scripts/`

Scripts de validação e qualidade de dados.

| Arquivo | Responsabilidade |
|---|---|
| `validate_data.py` | Validação de qualidade dos dados imputados (ranges, outliers, anomalias) |
| `validate_compliance.py` | Validação de cálculos de compliance score |

### `backend/reports/`

Relatórios versionados de validação e qualidade.

| Diretório/Arquivo | Responsabilidade |
|---|---|
| `data_quality_reports/` | Histórico de relatórios de qualidade |
| `validation_logs.db` | Banco de dados com versionamento de relatórios |

**Rastreabilidade:**
- Data e hora de cada validação
- Identificação de problemas com dados imputados
- Histórico completo para auditoria
- Integração com banco de dados para consultas históricas

---

Endpoints REST.

| Arquivo | Responsabilidade |
|---|---|
| `batch.py` | POST /upload, GET /batches, GET /batch/{id} |
| `prediction.py` | GET /prediction/{batch_id} |
| `compliance.py` | GET /compliance/{batch_id} |

### `frontend/components/`

Componentes reutilizáveis.

| Componente | Responsabilidade |
|---|---|
| `UploadCard` | Interface de upload de CSV |
| `ComplianceScoreCard` | Exibição do score de conformidade |
| `RiskPredictionCard` | Exibição da predição de risco |
| `SensorChart` | Gráficos de variáveis de sensores |
| `BatchTable` | Tabela de batches processados |

### `frontend/pages/`

Páginas da aplicação.

| Página | Responsabilidade |
|---|---|
| `Dashboard` | Visão geral com KPIs |
| `Upload` | Interface de upload |
| `BatchDetails` | Detalhes do batch |
| `Results` | Visualização de resultados |
| `Analytics` | Gráficos e análises |

---

## Convenções

- Nomes de arquivos e pastas em `snake_case` no backend (Python)
- Nomes de componentes em `PascalCase` no frontend (React)
- Nomes de arquivos de serviço em `camelCase` no frontend
- Cada módulo tem responsabilidade única e bem definida
- Lógica de negócio fica em `services/`, nunca em `api/`
- Processamento de dados fica em `processors/`, nunca em `services/`

---

## Pipeline ETL Distribuído

O BiotecPredict implementa um **pipeline ETL distribuído** em vez de um módulo centralizado, seguindo o padrão de **Clean Architecture** com separação clara de responsabilidades:

### Etapas do ETL

| Etapa | Componente | Responsabilidade | Localização |
|-------|-----------|------------------|-------------|
| **EXTRACT** | API REST | Recebe arquivo CSV do usuário | `api/routes/batch.py` (POST /upload) |
| **TRANSFORM** | Processors | Limpeza, validação e transformação de dados | `processors/csv_processor.py`, `data_validator.py`, `data_cleaner.py` |
| **LOAD** | Services | Persistência de dados no banco | `services/batch_service.py` |
| **VALIDATE** | Scripts | Validação de qualidade pós-processamento | `scripts/validate_data.py`, `validate_compliance.py` |

### Fluxo Completo

```
CSV Upload (EXTRACT)
    ↓
backend/api/routes/batch.py
    ↓
backend/processors/csv_processor.py (TRANSFORM - parsing)
    ↓
backend/processors/data_validator.py (TRANSFORM - validação de ranges)
    ↓
backend/processors/data_cleaner.py (TRANSFORM - limpeza de nulos/outliers)
    ↓
backend/services/batch_service.py (LOAD - persistência)
    ↓
PostgreSQL (armazenamento)
    ↓
backend/services/compliance_service.py (cálculo de score)
    ↓
backend/services/ml_service.py (predição com ML)
    ↓
backend/scripts/validate_data.py (VALIDATE - validação de qualidade)
    ↓
backend/scripts/validate_compliance.py (VALIDATE - validação de compliance)
    ↓
backend/reports/ (rastreabilidade e auditoria)
    ↓
backend/api/routes/ (REST - exposição de dados)
    ↓
frontend/pages/ (visualização)
```

### Benefícios da Arquitetura Distribuída

- **Separação de Responsabilidades**: Cada camada tem função bem definida
- **Testabilidade**: Cada etapa pode ser testada independentemente
- **Manutenibilidade**: Fácil localizar e modificar lógica específica
- **Escalabilidade**: Possibilidade de paralelizar etapas
- **Rastreabilidade**: Cada etapa registra metadados para auditoria

---

## Fluxo de Dados

```
CSV Upload
    ↓
backend/processors/csv_processor.py
    ↓
backend/processors/data_validator.py
    ↓
backend/services/batch_service.py (persistência)
    ↓
backend/services/compliance_service.py (cálculo)
    ↓
backend/services/ml_service.py (predição)
    ↓
backend/api/routes/ (REST)
    ↓
frontend/pages/ (visualização)
```

---

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ Estrutura Definida
