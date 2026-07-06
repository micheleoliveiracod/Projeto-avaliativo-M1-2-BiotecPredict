# Diagramas — BiotecPredict

Diagramas técnicos do projeto BiotecPredict em formato Mermaid (renderizáveis no GitHub e VSCode).

---

## 1. Arquitetura Geral do Sistema

```mermaid
graph TB
    subgraph Client ["Cliente (Browser)"]
        UI_UP[Página de Upload]
        UI_DB[Dashboard]
    end

    subgraph FE ["Frontend — React + TypeScript + Vite (:3000)"]
        ROUTER[React Router]
        LAYOUT[Layout / Navbar]
        SVC_API[api.ts — Axios]
        PROXY[Vite Proxy /api → :8001]
    end

    subgraph BE ["Backend — FastAPI + Python (:8001)"]
        MW[Middleware CORS]
        subgraph ROUTES ["Rotas"]
            R_BATCH["/batch"]
            R_COMP["/compliance"]
            R_PRED["/prediction"]
        end
        subgraph SERVICES ["Serviços"]
            S_BATCH[BatchService]
            S_COMP[ComplianceService]
            S_ML[MLService]
        end
        subgraph PROC ["Processadores"]
            P_CSV[csv_processor]
            P_VAL[data_validator]
            P_CLEAN[data_cleaner]
        end
        subgraph REPOS ["Repositórios"]
            RP_BATCH[BatchRepository]
            RP_SENSOR[SensorReadingRepository]
        end
    end

    subgraph STORAGE ["Persistência"]
        DB[(SQLite\nbiotecpredict.db)]
        PKL1[(risk_predictor.pkl)]
        PKL2[(scaler.pkl)]
    end

    Client --> FE
    FE --> PROXY
    PROXY --> MW
    MW --> ROUTES
    ROUTES --> SERVICES
    SERVICES --> PROC
    SERVICES --> REPOS
    S_ML --> PKL1
    S_ML --> PKL2
    REPOS --> DB
```

---

## 2. Diagrama de Entidade-Relacionamento (ER)

```mermaid
erDiagram
    BATCH {
        int       id               PK
        string    filename
        string    status
        datetime  upload_date
        int       total_records
        float     compliance_score
        string    compliance_status
        string    risk_prediction
        float     risk_confidence
    }

    SENSOR_READING {
        int       id               PK
        int       batch_id         FK
        datetime  recorded_at
        float     temperature
        float     ph
        float     dissolved_oxygen
        float     pressure
        float     agitator_speed
    }

    BATCH ||--o{ SENSOR_READING : "1 batch → N leituras"
```

---

## 3. Fluxo de Upload de CSV (Sequência)

```mermaid
sequenceDiagram
    actor Op as Operador
    participant FE as Frontend (React)
    participant API as FastAPI
    participant PROC as csv_processor
    participant VAL as data_validator
    participant COMP as ComplianceService
    participant ML as MLService
    participant DB as SQLite

    Op->>FE: Seleciona arquivo CSV
    FE->>API: POST /api/v1/upload

    API->>PROC: parse_csv(file)
    PROC-->>API: DataFrame

    API->>VAL: validate_ranges(df)
    VAL-->>API: df limpo

    API->>DB: INSERT INTO batches (status=PROCESSING)
    DB-->>API: batch_id

    loop Para cada linha do CSV
        API->>DB: INSERT INTO sensor_readings
    end

    API->>COMP: calculate_compliance(batch_id)
    COMP->>DB: SELECT AVG(temperature, pH, ...) FROM sensor_readings
    COMP-->>API: score=87.4, status=ACCEPTABLE

    API->>ML: predict_risk(avg_features)
    ML-->>API: risk=LOW_RISK, confidence=0.92

    API->>DB: UPDATE batches SET status=COMPLETED, score=87.4, risk=LOW_RISK
    API-->>FE: { batch_id, compliance_score, risk_prediction }
    FE-->>Op: Exibe resultado
```

---

## 4. Fluxo de Cálculo do Compliance Score

```mermaid
flowchart TD
    START([Compliance Score Engine]) --> FETCH[Buscar leituras\ndo batch no DB]
    FETCH --> AGG[Calcular média\nde cada variável]

    AGG --> TEMP[Temperatura\n24–26°C ideal]
    AGG --> PH[pH\n6.8–7.2 ideal]
    AGG --> DO[Dissolved Oxygen\n80–95% ideal]
    AGG --> PRESS[Pressão\n4.8–5.5 bar ideal]
    AGG --> RPM[Agitator Speed\n240–280 RPM ideal]

    TEMP --> SCORE_T[Score parcial\n0–100]
    PH --> SCORE_P[Score parcial\n0–100]
    DO --> SCORE_D[Score parcial\n0–100]
    PRESS --> SCORE_PR[Score parcial\n0–100]
    RPM --> SCORE_R[Score parcial\n0–100]

    SCORE_T & SCORE_P & SCORE_D & SCORE_PR & SCORE_R --> AVG_SCORE[Média ponderada\n20% cada]

    AVG_SCORE --> CLASS{Score?}
    CLASS -- "≥ 80" --> ACC[ACCEPTABLE]
    CLASS -- "60–79" --> WARN[WARNING]
    CLASS -- "< 60" --> CRIT[CRITICAL]
```

---

## 5. Pipeline de Machine Learning

```mermaid
flowchart LR
    subgraph TRAIN ["Treino (offline)"]
        DS[(Dataset Kaggle)] --> FE[Feature Engineering]
        FE --> SC_FIT[StandardScaler.fit]
        SC_FIT --> RF_FIT[RandomForest.fit\nn_estimators=100]
        RF_FIT --> EVAL{Acurácia ≥ 80%?}
        EVAL -- Não --> RF_FIT
        EVAL -- Sim --> SAVE_SC[scaler.pkl]
        EVAL -- Sim --> SAVE_RF[risk_predictor.pkl]
    end

    subgraph INFER ["Inferência (online)"]
        BATCH[(Batch Readings)] --> AGGR[Calcular médias]
        AGGR --> LOAD_SC[Carregar scaler.pkl]
        LOAD_SC --> TRANSFORM[scaler.transform]
        TRANSFORM --> LOAD_RF[Carregar risk_predictor.pkl]
        LOAD_RF --> PRED[predict + predict_proba]
        PRED --> OUT([LOW_RISK\nMEDIUM_RISK\nHIGH_RISK\n+ confidence])
    end

    SAVE_SC -.->|deploy| LOAD_SC
    SAVE_RF -.->|deploy| LOAD_RF
```

---

## 6. Diagrama de Componentes — Frontend

```mermaid
graph TD
    APP[App.tsx] --> ROUTER[BrowserRouter]
    ROUTER --> LAYOUT[Layout.tsx\nNavbar + main container]

    LAYOUT --> UP_PAGE[Upload Page\nsrc/pages/Upload/]
    LAYOUT --> DB_PAGE[Dashboard Page\nsrc/pages/Dashboard/]

    UP_PAGE --> UPLOAD_CARD[UploadCard\ndrag-and-drop]

    DB_PAGE --> BATCH_LIST[Tabela de Batches\npaginação + filtros]
    DB_PAGE --> DETAIL_CARD[Cards de KPI\ncompliance + risco]
    DB_PAGE --> CHARTS[Gráficos Recharts\nséries temporais]

    UPLOAD_CARD --> API[api.ts\nAxios instance]
    BATCH_LIST --> API
    DETAIL_CARD --> API
    CHARTS --> API

    API -- "baseURL: /api/v1" --> VITE_PROXY[Vite Proxy]
    VITE_PROXY --> FASTAPI[FastAPI :8001]
```

---

## 7. Diagrama de Camadas — Backend (Clean Architecture)

```mermaid
graph TB
    EXT([HTTP Request]) --> A

    subgraph A ["Camada de API (Rotas)"]
        A1[batch.py]
        A2[compliance.py]
        A3[prediction.py]
    end

    A --> B

    subgraph B ["Camada de Serviços (Business Logic)"]
        B1[BatchService]
        B2[ComplianceService]
        B3[MLService]
    end

    B --> C
    B --> D

    subgraph C ["Camada de Processamento"]
        C1[csv_processor.py]
        C2[data_validator.py]
        C3[data_cleaner.py]
    end

    subgraph D ["Camada de Repositórios (Data Access)"]
        D1[BatchRepository]
        D2[SensorReadingRepository]
    end

    D --> E

    subgraph E ["Camada de Modelos (ORM)"]
        E1[Batch]
        E2[SensorReading]
    end

    E --> F[(SQLite\nbiotecpredict.db)]
```

---

## 8. Pipeline de CI/CD (GitHub Actions)

```mermaid
flowchart TD
    PUSH[git push] --> GH[GitHub]
    GH --> CI_TRIGGER{Trigger}

    CI_TRIGGER --> CI[ci.yml]
    CI_TRIGGER --> E2E[e2e-tests.yml]

    subgraph CI ["ci.yml"]
        LINT[Ruff + Black\nlinting e formatação]
        LINT --> BE_TEST[pytest\nbacked unit tests]
        BE_TEST --> FE_TEST[Vitest\nfrontend unit tests]
        FE_TEST --> INT_TEST[Integration Tests\nuvicorn + HTTP requests]
    end

    subgraph E2E ["e2e-tests.yml"]
        E2E_RUN[Playwright\ne2e tests]
    end

    CI --> STATUS{Passou?}
    E2E --> STATUS

    STATUS -- Sim + branch main --> DOCKER[Docker Build]
    DOCKER --> PUSH_IMG[Push image]
    STATUS -- Não --> FAIL[❌ Pipeline falhou\nnotifica dev]
```

---

## 9. Estados de um Batch

```mermaid
stateDiagram-v2
    [*] --> PROCESSING : POST /upload\narquivo CSV recebido

    PROCESSING --> COMPLETED : Dados processados\nCompliance + ML calculados

    PROCESSING --> FAILED : Arquivo inválido\nou erro de processamento

    COMPLETED --> [*] : Dados disponíveis\nno dashboard

    FAILED --> [*] : Erro registrado\noperador notificado

    note right of COMPLETED
        compliance_score calculado
        risk_prediction definido
        SensorReadings persistidos
    end note
```

---