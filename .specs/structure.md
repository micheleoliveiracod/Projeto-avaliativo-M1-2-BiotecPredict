# Estrutura do Projeto - BiotecPredict

Organização de diretórios: backend Python (processamento, ML e API) e frontend React (dashboard e visualizações).

---

## Estrutura de Diretórios

```
/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── batch.py             # POST /upload · GET /batches · GET /batch/{id} · GET /batch/{id}/sensors
│   │       ├── compliance.py        # GET /compliance/{batch_id}
│   │       └── prediction.py        # GET /prediction/{batch_id} · POST /predict · GET /model/info
│   │
│   ├── db/
│   │   ├── database.py              # Engine SQLite · SessionLocal · get_db() · init_db()
│   │   └── repository.py            # BatchRepository · SensorReadingRepository
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── model.py                 # RandomForestClassifier: treino sintético + inferência + save/load .pkl
│   │   └── models/
│   │       ├── risk_predictor.pkl   # Modelo serializado (gerado em runtime se ausente)
│   │       └── scaler.pkl           # StandardScaler serializado
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── batch.py                 # Modelo ORM Batch (id INTEGER PK)
│   │   └── sensor_reading.py        # Modelo ORM SensorReading (campo: recorded_at)
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── csv_processor.py         # Leitura e parsing de CSV com mapeamento de aliases de colunas
│   │   ├── data_validator.py        # Validação de ranges físicos (temp 20-45 · pH 4-9 · DO 0-100 · pressão 0-10 · RPM 0-500)
│   │   └── data_cleaner.py          # Limpeza de dados (nulos, outliers)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── batch.py                 # BatchCreate · BatchResponse · BatchUpdate
│   │
│   ├── scripts/
│   │   ├── generate_api_docs.py     # Geração de documentação da API
│   │   └── generate_docstrings.py   # Geração de docstrings
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── batch_service.py         # Orquestração do pipeline CSV → DB → compliance → ML → COMPLETED
│   │   ├── compliance_service.py    # Cálculo do Manufacturing Compliance Score
│   │   └── ml_service.py            # Predição de risco com RandomForest
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── fixtures/                # Dados de teste compartilhados (pytest · Postman · E2E)
│   │   │   └── csv/
│   │   │       ├── README.md                    # Documentação dos cenários de teste
│   │   │       ├── control/                     # Comportamento correto (golden path + fronteiras)
│   │   │       │   ├── valid_ideal.csv              # Valores nos ranges ideais → ACCEPTABLE
│   │   │       │   ├── valid_acceptable.csv         # Valores aceitáveis mas não ideais
│   │   │       │   ├── valid_boundary.csv           # Limites do DataValidator
│   │   │       │   ├── batch_sensor_low/medium/high_risk.csv  # Lotes grandes (100 linhas) por classe
│   │   │       │   ├── boundary_acceptable_warning_*.csv      # Fronteira exata 80 (ACCEPTABLE/WARNING)
│   │   │       │   ├── boundary_warning_critical_*.csv        # Fronteira exata 45 (WARNING/CRITICAL)
│   │   │       │   └── single/two/four/five_sensors_out.csv   # 1, 2, 4 e 5 sensores fora do aceitável
│   │   │       ├── bugs/                        # Regressão dos bugs de cálculo corrigidos
│   │   │       │   ├── warning_zone.csv             # WARNING + LOW_RISK (esperado por design)
│   │   │       │   ├── critical_zone.csv            # Regressão: ML deveria prever HIGH_RISK
│   │   │       │   ├── single_sensor_out_temperature.csv    # Regressão: ML deveria prever MEDIUM_RISK
│   │   │       │   ├── three_sensors_out.csv        # Regressão: ML deveria prever HIGH_RISK
│   │   │       │   ├── outlier_masked_by_average.csv        # Regressão: outlier isolado mascarado pela média
│   │   │       │   └── rounding_boundary_inconsistency.csv  # Regressão: score "45.0" com classificação inconsistente
│   │   │       ├── performance/
│   │   │       │   └── valid_large_500rows.csv      # 500 linhas para performance (SLA < 5s)
│   │   │       └── rejected/                    # Upload deve dar HTTP 400
│   │   │           ├── invalid_empty.csv            # Arquivo vazio
│   │   │           ├── invalid_missing_columns.csv  # Colunas ausentes
│   │   │           ├── invalid_wrong_types.csv       # Tipos errados
│   │   │           └── invalid_out_of_range.csv      # Fora do range do DataValidator
│   │   └── pytest/
│   │       ├── __init__.py
│   │       ├── conftest.py          # Fixtures: test_engine (StaticPool) · db_session · client
│   │       ├── fixtures/            # Fixtures Python auxiliares
│   │       │   └── __init__.py
│   │       ├── unit/
│   │       │   ├── __init__.py
│   │       │   ├── test_models.py
│   │       │   ├── test_schemas.py
│   │       │   ├── test_processors.py
│   │       │   ├── test_services.py
│   │       │   └── test_validators.py
│   │       ├── integration/
│   │       │   ├── __init__.py
│   │       │   ├── test_api_integration.py   # 63 testes — Health · Upload · Batches · Compliance · Prediction · ML
│   │       │   ├── test_routes.py
│   │       │   ├── test_batch_service.py
│   │       │   ├── test_compliance_service.py
│   │       │   └── test_ml_service.py
│   │       ├── repositories/
│   │       │   ├── __init__.py
│   │       │   ├── test_batch_repository.py
│   │       │   └── test_sensor_reading_repository.py
│   │       ├── database/
│   │       │   ├── __init__.py
│   │       │   └── test_database.py
│   │       ├── health/
│   │       │   ├── __init__.py
│   │       │   └── test_health.py
│   │       └── test_services/
│   │           ├── __init__.py
│   │           ├── test_compliance_service.py
│   │           └── test_ml_service.py
│   │
│   ├── main.py                      # Entry point FastAPI · CORS · routers · health check · /
│   ├── setup_db.py                  # Script de inicialização e seed do banco
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Layout.tsx
│   │   │   │   └── Layout.module.css
│   │   │   ├── UploadCard/
│   │   │   │   ├── UploadCard.tsx
│   │   │   │   └── UploadCard.css
│   │   │   └── Dashboard/
│   │   │       ├── Dashboard.tsx
│   │   │       └── Dashboard.css
│   │   │
│   │   ├── pages/
│   │   │   ├── Upload/
│   │   │   │   └── Upload.tsx
│   │   │   └── Dashboard/
│   │   │       └── Dashboard.tsx
│   │   │
│   │   ├── services/
│   │   │   └── api.ts               # Axios · baseURL: /api/v1 (Vite proxy → :8001)
│   │   │
│   │   └── App.tsx                  # BrowserRouter · Layout · Routes (/ e /dashboard)
│   │
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts               # port 3000 · proxy /api → http://localhost:8001
│
├── docs/
│   ├── PRD.md                           # Product Requirements Document completo
│   ├── DIAGRAMAS.md                     # 9 diagramas Mermaid (Arquitetura · ER · Sequência · ML · CI/CD · estados)
│   ├── check-list-requisitos.md         # Checklist de entrega do projeto avaliativo
│   ├── analise-resultados.md            # Guia de interpretação de resultados (indicadores, faixas, cenários)
│   ├── cenarios-de-uso.md               # 2 cenários de uso com comandos curl e respostas esperadas
│   ├── ciclos-geracao-refinamento-codigo.md
│   ├── design-system.md
│   ├── postman/
│   │   └── BiotecPredict.postman_collection.json  # Coleção com testes para todos os endpoints
│   └── prompts/
│       ├── 01-arquitetura.md
│       ├── 02-geracao-codigo.md
│       ├── 03-refatoracao.md
│       ├── 04-testes.md
│       ├── 05-pipeline-cicd.md
│       ├── 06-documentacao.md
│       └── 07-analise-critica.md
│
├── deploy/
│   ├── docker-compose.yml       # Orquestra backend + frontend + volumes persistentes
│   ├── Dockerfile.backend       # Python 3.13-slim + uvicorn
│   ├── Dockerfile.frontend      # Node 18 build → nginx Alpine serve
│   ├── nginx.conf               # Proxy /api e /health para backend; SPA fallback
│   ├── start.bat                # start / stop / restart / logs / status / clean (Windows)
│   ├── start.sh                 # Mesmo para Mac/Linux
│   └── .gitignore
│
├── scripts/
│   └── project-planning/
│       ├── create_all_issues.py
│       ├── create_sprint0_issues.py
│       └── README.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml                   # Lint · pytest · Vitest · API integration
│       └── e2e-tests.yml            # Playwright end-to-end
│
├── .specs/                          # Contexto permanente do agente (specs, arquitetura, processos)
│   ├── product.md
│   ├── tech.md
│   ├── structure.md
│   ├── requirements.md
│   ├── compliance.md
│   ├── deploy.md
│   ├── ci-cd.md
│   ├── gitflow.md
│   └── localizacao.md
│
├── .env.example
├── pytest.ini                       # Configuração global do pytest
├── README.md
└── LICENSE
```

---

## Responsabilidades por Camada

### `backend/api/routes/`

Endpoints REST da API.

| Arquivo | Endpoints |
|---|---|
| `batch.py` | POST /api/v1/upload · GET /api/v1/batches · GET /api/v1/batch/{id} · GET /api/v1/batch/{id}/sensors |
| `compliance.py` | GET /api/v1/compliance/{batch_id} |
| `prediction.py` | GET /api/v1/prediction/{batch_id} · POST /api/v1/predict · GET /api/v1/model/info |
| `main.py` | GET /health · GET / |

> Todos os routers importam `get_db` de `backend.db.database` (sem redefinição local).

---

### `backend/processors/`

Processamento de dados brutos — camada TRANSFORM do ETL.

| Arquivo | Responsabilidade | Ranges validados |
|---|---|---|
| `csv_processor.py` | Leitura e parsing de CSV | — |
| `data_validator.py` | Validação de ranges físicos | temp 20-45°C · pH 4-9 · DO 0-100% · pressão 0-10 bar · RPM 0-500 |
| `data_cleaner.py` | Limpeza de nulos e outliers | — |

---

### `backend/services/`

Lógica de negócio — orquestração e cálculos.

| Arquivo | Responsabilidade |
|---|---|
| `batch_service.py` | Pipeline completo: CSV → validação → limpeza → DB → compliance → ML → COMPLETED |
| `compliance_service.py` | Score 0-100 por regras determinísticas; faixas aceitável e ideal por sensor |
| `ml_service.py` | RandomForestClassifier: LOW_RISK / MEDIUM_RISK / HIGH_RISK + confidence |

**Ranges do ComplianceService** (diferentes do DataValidator — mais restritivos):

| Sensor | Aceitável | Ideal |
|---|---|---|
| temperature | 20–30°C | 24–26°C |
| ph | 6.5–7.5 | 6.8–7.2 |
| dissolved_oxygen | 70–100% | 80–95% |
| pressure | 4.5–6.0 bar | 4.8–5.5 bar |
| agitator_speed | 200–300 RPM | 240–280 RPM |

---

### `backend/db/`

Persistência de dados.

| Arquivo | Responsabilidade |
|---|---|
| `database.py` | Engine SQLite · `get_db()` · `SessionLocal` · `Base` |
| `repository.py` | `BatchRepository` · `SensorReadingRepository` (pattern Repository) |

> `get_db()` é a única definição usada — importada por todos os routers via `from backend.db.database import get_db`.

**Banco de dados — local único, sem duplicação:**

| Ambiente | Arquivo/URL | Como é definido |
|---|---|---|
| Oficial (dev local, sem Docker) | `backend/data/biotecpredict.db` | Default de `database.py`, ancorado em `__file__` (não no cwd de quem roda o processo — evita gerar cópias em lugares diferentes conforme o comando usado para subir o backend) |
| Oficial (Docker) | `/app/data/biotecpredict.db`, persistido no volume nomeado `biotecpredict_data` | `DATABASE_URL` definida em `deploy/docker-compose.yml` |
| Teste (pytest) | SQLite **in-memory** (`sqlite:///:memory:`), um por função de teste | `tests/pytest/conftest.py` (`test_engine` fixture) — nunca toca disco, isolado por teste |

`DATABASE_TEST_URL` não existe mais como variável lida pelo código — a suíte de testes nunca usa
arquivo em disco, então não há um segundo `.db` de teste para manter sincronizado.

---

### `backend/ml/models/`

Artefatos do modelo de ML.

| Arquivo | Conteúdo |
|---|---|
| `risk_predictor.pkl` | RandomForestClassifier serializado |
| `scaler.pkl` | StandardScaler serializado |

> Paths carregados via `os.path.dirname(os.path.abspath(__file__))` para evitar problemas com diretório de trabalho.

---

### `backend/tests/`

Suíte de testes organizada em duas camadas:

| Diretório | Propósito |
|---|---|
| `tests/fixtures/csv/` | CSVs compartilhados por pytest, Postman e E2E, organizados por propósito: `control/` (comportamento correto), `bugs/` (reproduz divergências Compliance × ML conhecidas), `rejected/` (upload deve dar HTTP 400), `performance/` (teste de carga) — ver `tests/fixtures/csv/README.md` |
| `tests/pytest/conftest.py` | `test_engine` (SQLite in-memory + StaticPool) · `db_session` · `client` (override get_db) |
| `tests/pytest/integration/test_api_integration.py` | 63 testes de integração — todos os endpoints verificados |
| `tests/pytest/unit/` | Testes unitários de modelos, schemas, processors, services |

---

### `frontend/components/`

Componentes reutilizáveis da interface.

| Componente | Responsabilidade |
|---|---|
| `Layout` | Navbar + container principal das páginas |
| `UploadCard` | Interface de drag-and-drop para upload de CSV |
| `Dashboard` | Tabela de batches com filtros + cards de KPI (compliance score, risk, sensor data) |

---

### `frontend/pages/`

Páginas da aplicação (rotas).

| Página | Rota | Responsabilidade |
|---|---|---|
| `Upload` | `/` | Interface principal de upload de CSV |
| `Dashboard` | `/dashboard` | Visualização de batches, KPIs e gráficos |

---

### `docs/`

Documentação do projeto.

| Arquivo/Pasta | Conteúdo |
|---|---|
| `PRD.md` | Product Requirements Document (requisitos, modelo de dados, stack, user stories, diagramas) |
| `DIAGRAMAS.md` | 9 diagramas Mermaid: arquitetura, ER, sequência, compliance, ML, frontend, backend, CI/CD, estados |
| `postman/BiotecPredict.postman_collection.json` | Coleção Postman com testes para todos os endpoints (variável `{{base_url}}`) |
| `check-list-requisitos.md` | Checklist de entrega |
| `design-system.md` | Paleta de cores, tipografia, componentes, grid, acessibilidade |
| `prompts/` | 7 arquivos com prompts organizados por etapa de desenvolvimento |

---

## Convenções

- Nomes de arquivos e pastas em `snake_case` no backend (Python)
- Nomes de componentes em `PascalCase` no frontend (React/TypeScript)
- Arquivos de serviço frontend em `camelCase`
- Cada módulo tem responsabilidade única e bem definida
- Lógica de negócio fica em `services/`, nunca em `api/routes/`
- Processamento de dados fica em `processors/`, nunca em `services/`
- Imports sempre usam caminho absoluto a partir de `backend.*` (ex: `from backend.db.database import get_db`)

---

## Pipeline ETL Distribuído

O BiotecPredict implementa um **pipeline ETL distribuído** seguindo o padrão de **Clean Architecture**:

| Etapa | Componente | Responsabilidade | Localização |
|---|---|---|---|
| **EXTRACT** | API REST | Recebe arquivo CSV | `api/routes/batch.py` — POST /upload |
| **TRANSFORM** | Processors | Parsing · validação de ranges · limpeza | `processors/csv_processor.py` · `data_validator.py` · `data_cleaner.py` |
| **LOAD** | Services + DB | Persistência em SQLite | `services/batch_service.py` + `db/repository.py` |
| **ANALYZE** | Services | Score de compliance + predição ML | `services/compliance_service.py` · `ml_service.py` |
| **SERVE** | API REST | Exposição dos resultados | `api/routes/compliance.py` · `prediction.py` |
| **VISUALIZE** | Frontend | Dashboard interativo | `frontend/src/pages/` · `components/` |

### Fluxo Completo

```
CSV Upload (EXTRACT)
    ↓
backend/api/routes/batch.py          → recebe multipart/form-data
    ↓
backend/processors/csv_processor.py  → parsing em lista de dicts
    ↓
backend/processors/data_validator.py → validação de ranges físicos
    ↓
backend/processors/data_cleaner.py   → limpeza de nulos/outliers
    ↓
backend/services/batch_service.py    → cria Batch + SensorReadings no SQLite
    ↓
backend/db/repository.py             → BatchRepository · SensorReadingRepository
    ↓
SQLite (biotecpredict.db)            → persistência
    ↓
GET /compliance/{id}                 → backend/services/compliance_service.py
    ↓
GET /prediction/{id}                 → backend/services/ml_service.py
    ↓
frontend/pages/Dashboard             → visualização de KPIs e gráficos
```

---

**Versão**: 0.2.0
**Data**: Junho de 2026
**Status**: ✅ Estrutura Implementada e Testada
