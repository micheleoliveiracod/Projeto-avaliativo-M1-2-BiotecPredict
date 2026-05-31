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
| **PostgreSQL** | Banco de dados relacional | 15+ |
| **pandas** | Manipulação e processamento de dados | 2.0+ |
| **scikit-learn** | Machine learning (RandomForestClassifier) | 1.3+ |
| **pytest** | Framework de testes unitários | 7.0+ |
| **Postman** | Testes de integração da API REST | 11.0+ |

---

## Frontend

| Tecnologia | Papel | Versão |
|---|---|---|
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
| **PostgreSQL** | Banco de dados em container | 15-alpine |

---

## Fluxo de Dados Completo

```
CSV Upload (Kaggle Dataset)
        ↓
backend/processors/csv_processor.py  → Leitura e validação
        ↓
backend/processors/data_validator.py → Validação de ranges
        ↓
Banco de dados (PostgreSQL)          → Persistência
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
- Armazenamento em PostgreSQL
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
- Os arquivos em `.kiro/steering/` fornecem contexto permanente ao agente

---

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ Stack Definida e Implementada
