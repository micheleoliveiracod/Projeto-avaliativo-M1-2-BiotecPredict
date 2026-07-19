# Stack Tecnológica - BiotecPredict

Definição das tecnologias utilizadas no projeto. Onde a tecnologia específica não foi explicitada, a escolha é indicada como inferência.

---

## Backend

| Tecnologia | Papel | Versão |
|---|---|---|
| **Python** | Linguagem principal do backend | 3.11+ |
| **FastAPI** | Framework web leve e rápido | 0.100+ |
| **SQLAlchemy** | ORM para abstração do banco de dados | 2.0+ |
| **Pydantic** | Validação de dados e schemas | 2.0+ |
| **SQLite** | Banco de dados relacional (arquivo local) | 3.x |
| **pandas** | Manipulação e processamento de dados | 2.0+ |
| **scikit-learn** | Machine learning (RandomForestClassifier) | 1.3+ |
| **pytest** | Framework de testes unitários e de integração | 7.0+ |
| **httpx** | Cliente HTTP para TestClient do FastAPI | 0.27+ |
| **Postman** | Testes manuais e automatizados da API REST | 11.0+ |

---

## Frontend

| Tecnologia | Papel | Versão |
|---|---|---|
| **Node.js** | Runtime de build e testes do frontend | **20+** (Dockerfile atualizado de 18→20) |
| **React** | Framework principal do frontend | 18+ |
| **TypeScript** | Tipagem estática | 5.0+ |
| **Vite** | Build tool rápido | 5.0+ |
| **TailwindCSS** | Styling utility-first | 3.0+ |
| **Recharts** | Gráficos e visualizações | 2.10+ |
| **Axios** | Cliente HTTP | 1.6+ |
| **Vitest** | Framework de testes | 1.0+ |

---

## DevOps e Deploy

| Tecnologia | Papel | Versão |
|---|---|---|
| **Docker** | Containerização | 24.0+ |
| **Docker Compose** | Orquestração local | 2.20+ |
| **SQLite** | Banco de dados (arquivo local) | 3.x |
| **GitHub Actions** | CI/CD automatizado | — |

---

## Fluxo de Dados Completo

```
CSV Upload (Kaggle Dataset)
        ↓
backend/processors/csv_processor.py  → Leitura e validação
        ↓
backend/processors/data_validator.py → Validação de ranges
        ↓
Banco de dados (SQLite)              → Persistência
        ↓
backend/services/compliance_service.py → Cálculo de score
        ↓
backend/services/ml_service.py       → Predição com RandomForest
        ↓
backend/api/                         → REST ao frontend
        ↓
frontend/                            → Dashboard e visualizações
```

---

## Dataset

**Fonte**: Big Data – Biopharmaceutical Manufacturing (Kaggle)  
**Link**: https://www.kaggle.com/datasets/stephengoldie/big-databiopharmaceutical-manufacturing

**Conteúdo**:
- Variáveis industriais de processo
- Dados de sensores (Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed)
- Dados de batches industriais
- Falhas de processo
- Informações temporais (time-series)

---

## Arquitetura de Processamento

### Pipeline ETL Distribuído

O BiotecPredict implementa um **pipeline ETL distribuído** seguindo o padrão de **Clean Architecture** com separação clara de responsabilidades:

| Etapa | Componente | Função | Localização |
|-------|-----------|--------|-------------|
| **EXTRACT** | API REST | Recebe arquivo CSV do usuário | `api/routes/batch.py` (POST /upload) |
| **TRANSFORM** | Processors | Limpeza, validação e transformação | `processors/csv_processor.py`, `data_validator.py`, `data_cleaner.py` |
| **LOAD** | Services | Persistência de dados no banco | `services/batch_service.py` |
| **VALIDATE** | Scripts | Validação de qualidade pós-processamento | `scripts/validate_data.py`, `validate_compliance.py` |

### 1. Ingestão de Dados (EXTRACT)
- Upload de arquivo CSV via API REST
- Validação de formato
- Parsing de dados

### 2. Processamento (TRANSFORM)
- Limpeza de dados (valores nulos, outliers)
- Normalização de features
- Validação de ranges

### 3. Cálculo de Compliance Score
- Regras determinísticas baseadas em especificações
- Score 0-100
- Classificação (ACCEPTABLE / WARNING / CRITICAL)

### 4. Predição de Risco
- RandomForestClassifier treinado
- Features: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed
- Output: LOW RISK / MEDIUM RISK / HIGH RISK

### 5. Persistência (LOAD)
- Armazenamento em SQLite
- Histórico de batches
- Rastreabilidade de predições

### 6. Validação e Qualidade (VALIDATE)
- Scripts de validação de dados imputados
- Verificação de ranges e outliers
- Análise de anomalias e qualidade
- Relatórios versionados com rastreabilidade

### 7. Visualização
- Dashboard React
- Gráficos com Recharts
- KPIs de qualidade

---

## Padrões de Testes

### Configuração do Banco de Dados em Testes

O pytest usa SQLite in-memory com `StaticPool` para garantir que todas as sessões compartilhem a mesma conexão:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # crítico: sem StaticPool, create_all() e db_session usam conexões diferentes
)
```

> **Por que StaticPool?** SQLite in-memory cria um banco separado por conexão por padrão. StaticPool faz todas as conexões compartilharem a mesma instância, garantindo que `Base.metadata.create_all()` e a sessão de teste vejam as mesmas tabelas.

### Override de Dependências FastAPI

```python
def override_get_db():
    yield db_session  # mesma sessão do fixture

app.dependency_overrides[get_db] = override_get_db
```

> `get_db` deve ser importada de `backend.db.database` em todos os routers — nunca redefinida localmente — para que o override funcione.

### Coleção Postman

- Localização: `docs/postman/BiotecPredict.postman_collection.json`
- Variáveis de coleção: `base_url` = `http://localhost:8001`, `batch_id` = `1`
- O request de Upload salva o `batch_id` automaticamente via test script
- Fixtures CSV em `backend/tests/fixtures/csv/`, organizadas por propósito em subpastas: `control/` (comportamento correto), `bugs/` (reproduz divergências conhecidas entre `ComplianceService` e `MLModel`), `rejected/` (upload deve dar HTTP 400), `performance/` (teste de carga) — detalhes e valores esperados em `tests/fixtures/csv/README.md`

---

### Benefícios da Arquitetura ETL Distribuída

- **Separação de Responsabilidades**: Cada camada tem função bem definida
- **Testabilidade**: Cada etapa pode ser testada independentemente
- **Manutenibilidade**: Fácil localizar e modificar lógica específica
- **Escalabilidade**: Possibilidade de paralelizar etapas
- **Rastreabilidade**: Cada etapa registra metadados para auditoria
- **Clean Architecture**: Segue princípios de design de software

---

## Restrições e Decisões Técnicas

- **Sem dados em tempo real no MVP** — processamento batch de arquivos CSV
- **Dados públicos apenas** — dataset do Kaggle
- **Análise determinística + ML** — compliance score por regras, risco por modelo
- **Output estruturado** — JSON padronizado para todas as respostas
- **Cobertura de features** — 5 variáveis críticas de processo
- **Modelo inicial simples** — RandomForest para MVP; XGBoost/Isolation Forest em futuro

---

## IDE e Ambiente de Desenvolvimento

Utilizar o **Kiro** como IDE, no modelo **Claude Haiku 4.5**.

- O modo **Auto** permite que o agente execute alterações de forma autônoma
- Os arquivos em `.specs/` fornecem contexto permanente ao agente

---

**Versão**: 0.2.0  
**Data**: Junho de 2026  
**Status**: ✅ Stack Definida, Implementada e Testada
