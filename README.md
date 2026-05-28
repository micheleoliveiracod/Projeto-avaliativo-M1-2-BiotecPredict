# BiotecPredict

**Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia**

**Desenvolvido por:** [Michele Oliveira](https://github.com/micheleoliveiracod)
**Organização:** Programa SCTEC e SENAI (https://github.com/IA-para-DEVs-SCTEC-T2)
**Curso:** IA para DEVs
**Objetivo:** Desenvolvimento de um mini projeto E2E com IA em todas as etapas, como entrega final do módulo 1.

---

## 🎯 Visão Geral

BiotecPredict é uma plataforma SaaS end-to-end que monitora processos de manufatura biofarmacêutica utilizando dados industriais de sensores e machine learning. O sistema calcula um **Manufacturing Compliance Score** baseado em regras determinísticas e prevê **riscos de desvios de processo** utilizando modelos de machine learning.

**Fonte de dados:** [Big Data – Biopharmaceutical Manufacturing (Kaggle)](https://www.kaggle.com/datasets/stephengoldie/big-databiopharmaceutical-manufacturing)

---

## 🚀 Funcionalidades Principais

### 📤 Upload de Dados CSV
- Upload de arquivos CSV com dados de batches industriais
- Validação automática de formato e estrutura
- Processamento em lote
- Histórico de uploads

### 📊 Manufacturing Compliance Score
- Cálculo baseado em regras determinísticas
- Score 0-100 com classificações:
  - **ACCEPTABLE** (80-100): Processo conforme
  - **WARNING** (60-79): Atenção necessária
  - **CRITICAL** (0-59): Intervenção imediata

### 🤖 Predição de Risco com ML
- Modelo RandomForestClassifier treinado
- Classificações: LOW RISK, MEDIUM RISK, HIGH RISK
- Acurácia mínima: 80%
- Latência < 1 segundo

### 📈 Dashboard Analítico
- Visualização de KPIs de qualidade
- Gráficos de variáveis de sensores
- Exibição de compliance score
- Exibição de predição de risco
- Histórico de análises

### 🔌 REST API
- Endpoints para upload, consulta e predição
- Documentação automática (Swagger/ReDoc)
- Respostas estruturadas em JSON

---

## 📋 Variáveis Monitoradas

| Variável | Unidade | Descrição |
|---|---|---|
| **Temperature** | °C | Temperatura do biorreator |
| **pH** | - | Potencial hidrogeniônico |
| **Dissolved Oxygen** | % | Oxigênio dissolvido |
| **Pressure** | bar | Pressão do sistema |
| **Agitator Speed** | RPM | Velocidade do agitador |

---

## 🛠️ Stack Tecnológica

### Backend
| Tecnologia | Versão | Papel |
|---|---|---|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.100+ | Framework web |
| **SQLAlchemy** | 2.0+ | ORM |
| **Pydantic** | 2.0+ | Validação de dados |
| **PostgreSQL** | 15+ | Banco de dados |
| **pandas** | 2.0+ | Processamento de dados |
| **scikit-learn** | 1.3+ | Machine Learning |
| **pytest** | 7.0+ | Testes unitários |
| **Postman** | 11.0+ | Testes de integração |

### Frontend
| Tecnologia | Versão | Papel |
|---|---|---|
| **React** | 18+ | Framework principal |
| **TypeScript** | 5.0+ | Tipagem estática |
| **Vite** | 5.0+ | Build tool |
| **TailwindCSS** | 3.0+ | Styling |
| **Recharts** | 2.10+ | Gráficos |
| **Axios** | 1.6+ | Cliente HTTP |
| **Vitest** | 1.0+ | Testes |

### DevOps
| Tecnologia | Versão | Papel |
|---|---|---|
| **Docker** | 24.0+ | Containerização |
| **Docker Compose** | 2.20+ | Orquestração |
| **GitHub Actions** | - | CI/CD |

---

## 📁 Estrutura do Projeto

```
BiotecPredict/
├── backend/
│   ├── api/                         # API REST endpoints
│   │   ├── routes/
│   │   │   ├── batch.py             # POST /upload, GET /batches
│   │   │   ├── prediction.py        # GET /prediction/{batch_id}
│   │   │   └── compliance.py        # GET /compliance/{batch_id}
│   │   └── main.py                  # Entry point
│   │
│   ├── processors/                  # Processamento de dados
│   │   ├── csv_processor.py         # Leitura e parsing
│   │   ├── data_validator.py        # Validação de ranges
│   │   └── data_cleaner.py          # Limpeza de dados
│   │
│   ├── services/                    # Lógica de negócio
│   │   ├── batch_service.py         # Gerenciamento de batches
│   │   ├── compliance_service.py    # Cálculo de compliance
│   │   ├── ml_service.py            # Predição com ML
│   │   └── data_service.py          # Acesso a dados
│   │
│   ├── models/                      # Modelos SQLAlchemy
│   │   ├── batch.py
│   │   ├── sensor_reading.py
│   │   └── prediction.py
│   │
│   ├── schemas/                     # Schemas Pydantic
│   │   ├── batch.py
│   │   ├── prediction.py
│   │   └── compliance.py
│   │
│   ├── db/                          # Banco de dados
│   │   ├── database.py
│   │   └── repository.py
│   │
│   ├── ml/                          # Machine Learning
│   │   ├── model.py
│   │   ├── trainer.py
│   │   └── predictor.py
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
│   │   └── postman/
│   │
│   ├── requirements.txt
│   └── main.py
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
│   │   │   ├── api.ts
│   │   │   ├── batchService.ts
│   │   │   └── predictionService.ts
│   │   │
│   │   ├── hooks/                   # Custom hooks
│   │   ├── utils/                   # Funções auxiliares
│   │   ├── styles/                  # Estilos globais
│   │   └── App.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                            # Documentação
│   ├── diagrams/
│   │   ├── c4/                      # Diagramas C4
│   │   └── uml/                     # Diagramas UML
│   ├── mockups.md
│   ├── PRD.md
│   └── user_stories.md
│
├── deploy/                          # Configuração de deploy
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── start.bat
│   ├── start.sh
│   └── .env.example
│
├── .kiro/                           # Configurações Kiro
│   ├── hooks/
│   ├── scripts/
│   ├── specs/
│   └── steering/                    # Contexto permanente
│
├── .github/
│   ├── issue_template/
│   ├── workflows/
│   └── pull_request_template.md
│
├── .env.example
├── README.md
└── LICENSE
```

---

## 🚀 Início Rápido

### Pré-requisitos

- Docker Desktop (Windows/Mac) ou Docker + Docker Compose (Linux)
- Mínimo 4GB RAM disponível
- Portas 80, 8000, 5432 disponíveis

### Instalação e Execução

#### 1. Clone o repositório

```bash
git clone https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict.git
cd Projeto-avaliativo-M1-2-BiotecPredict
```

#### 2. Configure variáveis de ambiente

```bash
cp deploy/.env.example deploy/.env
```

#### 3. Inicie o sistema

**Windows:**
```cmd
cd deploy
start.bat start
```

**Mac/Linux:**
```bash
cd deploy
chmod +x start.sh
./start.sh start
```

#### 4. Acesse a aplicação

- **Frontend:** http://localhost
- **API:** http://localhost:8000/api
- **Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📦 Instalação de Dependências

### Backend (Python)

O backend utiliza Python 3.11+ com as dependências especificadas em `backend/requirements.txt`.

#### Instalação via pip

```bash
# Navegue até o diretório backend
cd backend

# Instale as dependências
pip install -r requirements.txt
```

#### Dependências Principais

| Dependência | Versão | Propósito |
|---|---|---|
| **fastapi** | 0.104.1 | Framework web |
| **sqlalchemy** | 2.0.23 | ORM para banco de dados |
| **pandas** | 2.1.3 | Processamento de dados |
| **scikit-learn** | 1.3.2 | Machine Learning |
| **pydantic** | 2.5.0 | Validação de dados |
| **pytz** | 2024.1 | Timezone (Prompt Logging) |
| **pytest** | 7.4.3 | Testes unitários |

#### Dependência Especial: pytz

A dependência **pytz** é utilizada pelo sistema de **Prompt Logging** para registrar timestamps em horário de Brasília (America/Sao_Paulo). Ela é automaticamente instalada com o comando acima.

**Uso:**
```python
import pytz
from datetime import datetime

# Obter timestamp em horário de Brasília
brasilia_tz = pytz.timezone('America/Sao_Paulo')
timestamp = datetime.now(brasilia_tz).strftime('%Y-%m-%d %H:%M:%S')
```

### Frontend (Node.js)

O frontend utiliza Node.js 18+ com as dependências especificadas em `frontend/package.json`.

#### Instalação via npm

```bash
# Navegue até o diretório frontend
cd frontend

# Instale as dependências
npm install
```

#### Dependências Principais

| Dependência | Versão | Propósito |
|---|---|---|
| **react** | 18+ | Framework principal |
| **typescript** | 5.0+ | Tipagem estática |
| **vite** | 5.0+ | Build tool |
| **tailwindcss** | 3.0+ | Styling |
| **recharts** | 2.10+ | Gráficos |
| **axios** | 1.6+ | Cliente HTTP |
| **vitest** | 1.0+ | Testes |

### Verificação de Instalação

#### Backend

```bash
# Verificar Python
python --version  # Deve ser 3.11+

# Verificar pip
pip --version

# Verificar instalação de dependências
pip list | grep pytz  # Deve mostrar pytz 2024.1
```

#### Frontend

```bash
# Verificar Node.js
node --version  # Deve ser 18+

# Verificar npm
npm --version

# Verificar instalação de dependências
npm list react  # Deve mostrar react 18+
```

---

## 📡 Endpoints da API

### Upload de Dados

```http
POST /api/v1/upload
Content-Type: multipart/form-data

Response:
{
  "batch_id": "uuid",
  "status": "processing",
  "message": "Batch received and queued for processing"
}
```

### Listar Batches

```http
GET /api/v1/batches

Response:
{
  "batches": [
    {
      "id": "uuid",
      "batch_name": "Batch-001",
      "upload_date": "2026-05-24T10:30:00Z",
      "compliance_score": 85,
      "status": "completed"
    }
  ]
}
```

### Detalhes do Batch

```http
GET /api/v1/batch/{batch_id}

Response:
{
  "id": "uuid",
  "batch_name": "Batch-001",
  "sensor_readings": [
    {
      "temperature": 37.5,
      "ph": 7.2,
      "dissolved_oxygen": 85.3,
      "pressure": 2.1,
      "agitator_speed": 250
    }
  ],
  "compliance_score": 85,
  "status": "completed"
}
```

### Predição de Risco

```http
GET /api/v1/prediction/{batch_id}

Response:
{
  "batch_id": "uuid",
  "risk_level": "LOW RISK",
  "confidence": 0.92,
  "model_version": "1.0.0",
  "prediction_timestamp": "2026-05-24T10:35:00Z"
}
```

### Score de Conformidade

```http
GET /api/v1/compliance/{batch_id}

Response:
{
  "batch_id": "uuid",
  "compliance_score": 85,
  "classification": "ACCEPTABLE",
  "details": {
    "temperature_score": 90,
    "ph_score": 85,
    "dissolved_oxygen_score": 80,
    "pressure_score": 85,
    "agitator_speed_score": 85
  }
}
```

---

## 🧪 Testes

### Backend (pytest)

```bash
cd backend
pip install -r requirements.txt
pytest tests/pytest/
```

### Backend (Postman)

Testes de integração da API REST:

```bash
# Importar collection no Postman
# Arquivo: backend/tests/postman/BiotecPredict.postman_collection.json

# Ou executar via CLI
npm install -g newman
newman run backend/tests/postman/BiotecPredict.postman_collection.json
```

**Endpoints testados:**
- POST /api/v1/upload - Upload de CSV
- GET /api/v1/batches - Listar batches
- GET /api/v1/batch/{id} - Detalhes do batch
- GET /api/v1/prediction/{batch_id} - Predição de risco
- GET /api/v1/compliance/{batch_id} - Score de conformidade

### Frontend (Vitest)

```bash
cd frontend
npm install
npm run test
```

### Cobertura de Testes

Objetivo: **≥ 70%** de cobertura

```bash
# Backend
pytest --cov=backend tests/pytest/

# Frontend
npm run test:coverage
```

---

## 🔄 CI/CD e Automação

### Pipeline CI/CD com GitHub Actions

O projeto utiliza **GitHub Actions** para automação completa de testes, lint, documentação e deploy.

#### Workflows Implementados

| Workflow | Trigger | Funcionalidades |
|----------|---------|-----------------|
| **CI - Lint & Tests** | Push/PR em branches | Lint (flake8, ESLint), Testes (pytest, Vitest), Cobertura (codecov), Testes de Integração (Postman) |
| **CD - Deploy** | Push em main | Build Docker, Health checks, Deploy automático |
| **Docs Generation** | Push em develop/main | Geração automática de API docs, análise de docstrings |
| **AI Test Generation** | Post-commit | Geração de testes com IA, análise de cobertura |

#### Configurações

- **Backend**: `.flake8`, `pyproject.toml` (pytest, coverage, black, isort)
- **Frontend**: `.eslintrc.cjs`, `vitest.config.ts`
- **Cobertura mínima**: 70% (backend + frontend)
- **Lint**: Automático com correções sugeridas

#### Como Usar

**Visualizar status dos workflows:**
1. Acesse [GitHub Actions](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/actions)
2. Selecione o workflow desejado
3. Verifique status e logs

**Executar testes localmente:**
```bash
# Backend
cd backend
pytest tests/pytest/ --cov=. --cov-report=html

# Frontend
cd frontend
npm run test:coverage
```

---

### Sistema de Prompt Logging

O projeto implementa um sistema automático de logging de prompts executados no Kiro, com rastreabilidade completa.

#### Funcionalidades

- ✅ Captura automática de prompts via hook `promptSubmit`
- ✅ Metadados: branch Git, usuário, timestamp (Brasília)
- ✅ Organização de logs por branch
- ✅ Formatação em Markdown
- ✅ Tratamento gracioso de erros
- ✅ Filtragem de prompts triviais

#### Localização dos Logs

```
.kiro/prompt-logs/
├── main.md
├── develop.md
├── feature-upload-csv.md
└── bugfix-validation-error.md
```

#### Consulta de Logs

```bash
# Ver logs de uma branch
cat .kiro/prompt-logs/<branch-name>.md

# Últimas entradas
tail -n 50 .kiro/prompt-logs/<branch-name>.md

# Buscar por palavra-chave
grep -A 10 "palavra-chave" .kiro/prompt-logs/<branch-name>.md
```

**Documentação completa:** [Prompt Logging](.kiro/steering/prompt-logging.md)

---

## 📝 Prompt Logging - Rastreabilidade de Prompts

O projeto implementa um sistema automático de logging de prompts executados no Kiro, com rastreabilidade completa de todas as interações com o agente de IA durante o desenvolvimento.

### O que é Prompt Logging?

**Prompt Logging** é um mecanismo automático que captura e registra todos os prompts submetidos ao Kiro, organizando-os por branch Git. O sistema funciona de forma transparente, sem interferir no fluxo de trabalho, e mantém rastreabilidade completa para auditoria, reprodutibilidade e análise de qualidade.

### Funcionalidades Principais

- ✅ **Captura Automática** - Nenhuma ação manual necessária
- ✅ **Organização por Branch** - Cada branch tem seu próprio arquivo de log
- ✅ **Metadados Completos** - Usuário, branch, timestamp (Brasília), conteúdo
- ✅ **Rastreabilidade Versionada** - Logs são versionados no Git
- ✅ **Filtros Inteligentes** - Prompts triviais são automaticamente filtrados

### Localização dos Logs

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-compliance.md      # Logs de feature branches
├── bugfix-validation.md       # Logs de bugfix branches
└── release-v1.0.0.md         # Logs de release branches
```

### Consulta de Logs

**Ver logs da branch atual:**
```bash
# Mac/Linux
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Windows PowerShell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Buscar por palavra-chave:**
```bash
# Mac/Linux
grep -i "compliance" .kiro/prompt-logs/*.md

# Windows PowerShell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

### Integração em Code Reviews

Ao revisar uma PR, consulte o arquivo de log da branch para entender o contexto:

```bash
# Revisor consultando logs da branch em revisão
cat .kiro/prompt-logs/feature-ml-prediction.md
```

Isso permite:
- Entender a intenção original
- Validar que requisitos foram atendidos
- Identificar decisões arquiteturais
- Facilitar discussões em code reviews

### Dependência: pytz

O sistema de Prompt Logging utiliza a biblioteca **pytz** para registrar timestamps em horário de Brasília (America/Sao_Paulo - UTC-3).

**Instalação:**
```bash
pip install pytz
```

**Versão:** 2024.1 (incluída em `backend/requirements.txt`)

**Uso:**
```python
import pytz
from datetime import datetime

# Obter timestamp em horário de Brasília
brasilia_tz = pytz.timezone('America/Sao_Paulo')
timestamp = datetime.now(brasilia_tz).strftime('%Y-%m-%d %H:%M:%S')
```

### Documentação Detalhada

Para instruções completas sobre instalação, uso e troubleshooting:

- **Documentação Completa:** [docs/prompt-logging.md](docs/prompt-logging.md)
- **Steering File:** [.kiro/steering/prompt-logging.md](.kiro/steering/prompt-logging.md)
- **Instruções de Instalação:** [docs/prompt-logging.md#instruções-de-instalação](docs/prompt-logging.md#instruções-de-instalação)

### Decisão: Logs Versionados no Git

**Decisão:** ✅ Logs DEVEM ser versionados (version controlled)

**Reasoning:**
- **Rastreabilidade:** Histórico completo de todas as interações com IA
- **Auditoria:** Conformidade regulatória e análise crítica de IA
- **Reprodutibilidade:** Entender contexto de implementações anteriores
- **Documentação Viva:** Complementar documentação técnica com histórico executável

**Configuração:**
- Logs são armazenados em `.kiro/prompt-logs/`
- Nada é adicionado ao `.gitignore` para logs
- Fazer commit dos logs junto com o código: `git add .kiro/prompt-logs/`
- Exemplo de commit: `docs: adiciona prompts de implementação da feature`

### Boas Práticas

1. **Fazer commits regulares dos logs** - Versionar junto com o código
2. **Referenciar logs em commits** - Mencionar arquivo de log na mensagem
3. **Consultar logs antes de iniciar feature** - Reutilizar padrões bem-sucedidos
4. **Usar logs em code reviews** - Entender contexto e validar implementação
5. **Manter logs limpos** - Não editar manualmente, deixar sistema gerenciar

### Exemplo de Fluxo Completo

```bash
# 1. Criar branch
git checkout -b feature/compliance-score

# 2. Submeter prompts no Kiro (automático: logs são capturados)
# Prompt 1: "Implementar cálculo de compliance score"
# Prompt 2: "Adicionar testes unitários"

# 3. Verificar logs capturados
cat .kiro/prompt-logs/feature-compliance-score.md

# 4. Fazer commits
git add .
git commit -m "feat(services): implementa compliance score"
git add .kiro/prompt-logs/
git commit -m "docs: adiciona prompts de implementação"

# 5. Fazer push
git push -u origin feature/compliance-score

# 6. Revisor consulta logs para entender contexto
# Logs permanecem versionados para referência futura
```

---

### GitHub Projects - Automação e Rastreamento

O projeto utiliza **GitHub Projects** com automação completa para rastreamento de progresso, velocidade e métricas.

#### Workflows de Automação

| Workflow | Trigger | Funcionalidade |
|----------|---------|-----------------|
| **project-automation.yml** | Issue/PR events | Adiciona ao projeto, move conforme status, sincroniza milestones |
| **progress-report.yml** | Seg 9h UTC | Gera relatório semanal de progresso |
| **velocity-analysis.yml** | Seg 10h UTC | Analisa velocidade do time (últimas 4 semanas) |
| **metrics-dashboard.yml** | Seg 11h UTC | Gera dashboard completo de métricas |

#### Relatórios Gerados

Todos os relatórios são salvos em `.kiro/reports/`:

- **progress-YYYY-MM-DD.md** - Progresso semanal (issues, PRs, taxa de conclusão)
- **velocity-YYYY-MM-DD.md** - Análise de velocidade (média, tendência, projeções)
- **metrics-YYYY-MM-DD.md** - Dashboard de métricas (saúde do projeto, indicadores)

#### Board do GitHub Projects

**Colunas:**
- **Backlog** - Issues não planejadas
- **Sprint Ready** - Issues prontas para iniciar
- **In Progress** - Issues sendo desenvolvidas
- **Review** - Issues em revisão (PR aberta)
- **Done** - Issues concluídas

#### Como Usar

**Visualizar projeto:**
1. Acesse [GitHub Projects](https://github.com/users/micheleoliveiracod/projects/7)
2. Selecione "BiotecPredict Roadmap"
3. Visualize o board com issues/PRs organizadas por status

**Visualizar relatórios:**
```bash
# Progresso
cat .kiro/reports/progress-YYYY-MM-DD.md

# Velocidade
cat .kiro/reports/velocity-YYYY-MM-DD.md

# Métricas
cat .kiro/reports/metrics-YYYY-MM-DD.md
```

**Documentação completa:** [GitHub Projects](.kiro/steering/github-projects.md)

---

## 📝 Prompt Logging - Rastreabilidade Completa de Prompts

O projeto implementa um **sistema automático de logging de prompts** que captura e registra todos os prompts executados no Kiro durante o desenvolvimento, com rastreabilidade completa para auditoria, reprodutibilidade e análise de qualidade.

### O que é Prompt Logging?

**Prompt Logging** é um mecanismo automático que:

- ✅ Captura todos os prompts submetidos ao Kiro
- ✅ Organiza logs por branch Git
- ✅ Registra metadados (usuário, timestamp em Brasília, conteúdo)
- ✅ Funciona de forma transparente (sem ação manual)
- ✅ Mantém rastreabilidade versionada no Git

### Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| **Captura Automática** | Nenhuma ação manual necessária; funciona transparentemente |
| **Organização por Branch** | Cada branch Git tem seu próprio arquivo de log |
| **Metadados Completos** | Usuário Git, branch, timestamp (Brasília - UTC-3), conteúdo |
| **Rastreabilidade Versionada** | Logs são versionados no Git para auditoria completa |
| **Filtros Inteligentes** | Prompts triviais são automaticamente filtrados |
| **Integração em Code Reviews** | Consultáveis durante revisão de PRs para entender contexto |

### Localização dos Logs

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-compliance.md      # Logs de feature branches
├── bugfix-validation.md       # Logs de bugfix branches
└── release-v1.0.0.md         # Logs de release branches
```

### Como Usar

#### 1. Submeter Prompts (Automático)

Nenhuma ação manual é necessária. Prompts são capturados automaticamente:

```
1. Abrir Kiro
2. Digitar seu prompt
3. Pressionar Enter/Submit
   ↓ (Automático)
4. Hook dispara
5. Prompt é registrado em .kiro/prompt-logs/<branch-atual>.md
```

#### 2. Consultar Logs

**Ver logs da branch atual:**
```bash
# Mac/Linux
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Windows PowerShell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Buscar por palavra-chave:**
```bash
# Mac/Linux
grep -i "compliance" .kiro/prompt-logs/*.md

# Windows PowerShell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

#### 3. Integrar em Code Reviews

Ao revisar uma PR, consulte o arquivo de log da branch para entender o contexto:

```bash
# Revisor consultando logs da branch em revisão
cat .kiro/prompt-logs/feature-ml-prediction.md
```

Isso permite:
- Entender a intenção original
- Validar que requisitos foram atendidos
- Identificar decisões arquiteturais
- Facilitar discussões em code reviews

### Dependência: pytz

O sistema de Prompt Logging utiliza a biblioteca **pytz** para registrar timestamps em horário de Brasília (America/Sao_Paulo - UTC-3).

**Instalação:**
```bash
pip install pytz
```

**Versão:** 2024.1 (incluída em `backend/requirements.txt`)

**Uso:**
```python
import pytz
from datetime import datetime

# Obter timestamp em horário de Brasília
brasilia_tz = pytz.timezone('America/Sao_Paulo')
timestamp = datetime.now(brasilia_tz).strftime('%Y-%m-%d %H:%M:%S')
```

### Decisão: Logs Versionados no Git

**Decisão:** ✅ Logs DEVEM ser versionados (version controlled)

**Reasoning:**
- **Rastreabilidade:** Histórico completo de todas as interações com IA
- **Auditoria:** Conformidade regulatória e análise crítica de IA
- **Reprodutibilidade:** Entender contexto de implementações anteriores
- **Documentação Viva:** Complementar documentação técnica com histórico executável

**Configuração:**
- Logs são armazenados em `.kiro/prompt-logs/`
- Nada é adicionado ao `.gitignore` para logs
- Fazer commit dos logs junto com o código: `git add .kiro/prompt-logs/`
- Exemplo de commit: `docs: adiciona prompts de implementação da feature`

### Boas Práticas

1. **Fazer commits regulares dos logs** - Versionar junto com o código
2. **Referenciar logs em commits** - Mencionar arquivo de log na mensagem
3. **Consultar logs antes de iniciar feature** - Reutilizar padrões bem-sucedidos
4. **Usar logs em code reviews** - Entender contexto e validar implementação
5. **Manter logs limpos** - Não editar manualmente, deixar sistema gerenciar

### Documentação Detalhada

Para instruções completas sobre instalação, uso, troubleshooting e limitações:

- **Documentação Completa:** [docs/prompt-logging.md](docs/prompt-logging.md)
- **Steering File (Contexto para Kiro):** [.kiro/steering/prompt-logging.md](.kiro/steering/prompt-logging.md)
- **Instruções de Instalação:** [docs/prompt-logging.md#instruções-de-instalação](docs/prompt-logging.md#instruções-de-instalação)
- **Instruções de Uso:** [docs/prompt-logging.md#instruções-de-uso](docs/prompt-logging.md#instruções-de-uso)
- **Troubleshooting:** [docs/prompt-logging.md#troubleshooting](docs/prompt-logging.md#troubleshooting)
- **Limitações Conhecidas:** [docs/prompt-logging.md#limitações-conhecidas](docs/prompt-logging.md#limitações-conhecidas)

---

### Validação e Qualidade de Dados

O projeto inclui scripts de validação para garantir qualidade dos dados e precisão dos cálculos.

#### Scripts Disponíveis

```bash
# Validar qualidade dos dados imputados
python backend/scripts/validate_data.py --batch-id <batch_id>

# Validar cálculos de compliance score
python backend/scripts/validate_compliance.py --batch-id <batch_id>

# Análise completa de qualidade (perspectiva de cientista de dados)
python backend/scripts/data_quality_checker.py --batch-id <batch_id>
```

#### Relatórios Gerados

Todos os scripts geram relatórios versionados em `backend/reports/`:

- **data_quality_reports/** - Histórico de relatórios de qualidade
- **validation_logs.db** - Banco de dados com versionamento de relatórios

**Rastreabilidade:**
- Data e hora de cada validação
- Identificação de problemas com dados imputados
- Histórico completo para auditoria
- Integração com banco de dados para consultas históricas

**Documentação completa:** [Compliance e Governança](.kiro/steering/compliance.md)

---

### Scripts de Validação

Backend inclui scripts de validação para garantir qualidade dos dados e precisão dos cálculos:

```bash
# Validar qualidade dos dados imputados
python backend/scripts/validate_data.py --batch-id <batch_id>

# Validar cálculos de compliance score
python backend/scripts/validate_compliance.py --batch-id <batch_id>
```

### Relatórios de Validação

Todos os scripts geram relatórios versionados em `backend/reports/`:

- **data_quality_reports/** - Histórico de relatórios de qualidade
- **validation_logs.db** - Banco de dados com versionamento de relatórios

**Rastreabilidade:**
- Data e hora de cada validação
- Identificação de problemas com dados imputados
- Histórico completo para auditoria

---

## 🔄 Fluxo de Dados

```
CSV Upload
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

## 📊 Requisitos Funcionais

| ID | Requisito | Status |
|---|---|---|
| FR-001 | Upload de Arquivo CSV | ✅ |
| FR-002 | Processamento de Batch | ✅ |
| FR-003 | Persistência de Dados | ✅ |
| FR-004 | Manufacturing Compliance Score | ✅ |
| FR-005 | Validação de Especificações | ✅ |
| FR-006 | Predição de Risco com ML | ✅ |
| FR-007 | Inferência em Tempo de Processamento | ✅ |
| FR-008 | Dashboard Analítico | ✅ |
| FR-009 | Tabela de Batches | ✅ |
| FR-010 | Endpoints de Upload | ✅ |
| FR-011 | Endpoints de Consulta | ✅ |
| FR-012 | Testes Automatizados | ✅ |

---

## 📋 Requisitos Não-Funcionais

| ID | Requisito | Alvo |
|---|---|---|
| NFR-001 | Tempo de Resposta | < 5 segundos |
| NFR-002 | Escalabilidade | 100 usuários simultâneos |
| NFR-003 | Disponibilidade | 99% uptime |
| NFR-004 | Criptografia de Dados | HTTPS + bcrypt |
| NFR-005 | Validação de Entrada | Rigorosa |
| NFR-006 | Controle de Acesso | Rate limiting 100 req/min |
| NFR-007 | Clean Architecture | Separação de responsabilidades |
| NFR-008 | Documentação | Completa |

---

## 🔐 Segurança

- ✅ HTTPS em produção
- ✅ Validação rigorosa de tipos (Pydantic)
- ✅ Proteção contra SQL Injection (SQLAlchemy)
- ✅ Sanitização de entrada
- ✅ Rate limiting (100 req/min por IP)
- ✅ Logs de acesso
- ✅ Variáveis de ambiente para secrets

---

## 📚 Documentação

- [Visão Geral do Projeto](docs/PRD.md)
- [Stack Tecnológica](.kiro/steering/tech.md)
- [Estrutura do Projeto](.kiro/steering/structure.md)
- [Requisitos](.kiro/steering/requirements.md)
- [GitFlow](.kiro/steering/gitflow.md)
- [Deploy](.kiro/steering/deploy.md)
- [Compliance](.kiro/steering/compliance.md)

---

## 🔄 GitFlow

O projeto segue o padrão GitFlow com as seguintes branches:

- **main** - Código estável em produção
- **develop** - Branch de integração
- **feature/** - Novas funcionalidades
- **bugfix/** - Correções de bugs
- **hotfix/** - Correções urgentes
- **release/** - Preparação de versão

### Convenção de Commits

Seguir [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona novo endpoint
fix: corrige validação de CSV
docs: atualiza README
chore: atualiza dependências
refactor: melhora compliance score
test: adiciona testes de upload
```

---

## 📈 Roadmap

### Fase 0 — Setup de Documentação (PRÉ-SPRINT) 🚀
- Subir documentação de escopo e requisitos
- Subir estrutura de branches e GitFlow
- Subir steering files e documentação estratégica
- Subir estrutura de diretórios
- Subir requirements.txt e .gitignore
- Subir templates de issues e PRs

### Sprint 1 — Setup Inicial ✅
- Estrutura base do repositório
- Configuração de GitFlow
- Backend FastAPI
- Frontend React/Vite
- PostgreSQL
- GitHub Actions

### Sprint 2 — Upload e Persistência ✅
- Home Page
- Upload CSV
- Parser CSV
- Persistência no banco
- Histórico de uploads

### Sprint 3 — Dashboards e Compliance Score ✅
- Compliance Score Engine
- Dashboard Analítico
- Gráficos Industriais
- Analytics API
- Histórico de Análises

### Sprint 4 — Machine Learning ✅
- Pipeline ML
- RandomForestClassifier
- Endpoint Prediction
- ML Analytics
- Histórico de Predições

---

## 🤝 Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git commit -m 'feat: descrição da feature'`
3. Push para a branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

Consulte [GitFlow](.kiro/steering/gitflow.md) para mais detalhes.

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

- **Desenvolvedor Principal** - BiotecPredict Team

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Consulte a [Documentação](.kiro/steering/)
2. Abra uma [Issue](https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues)
3. Verifique o [Roadmap](.kiro/steering/gitflow.md)

---

## 🎯 Status do Projeto

```
DESENVOLVIMENTO: MVP COMPLETO

Backend:        ✅ 95% (Endpoints, Services, ML, Validação)
Frontend:       ✅ 85% (Pages, Components, Integration, E2E)
Deploy:         ✅ 100% (Docker Compose)
Testes:         ✅ 85% (Unit + Integration + E2E)
Documentação:   ✅ 100% (Completa + Automática)
CI/CD:          ✅ 100% (GitHub Actions + IA)
Validação:      ✅ 100% (Qualidade de Dados + Auditoria)
Prompt Logging: ✅ 100% (Rastreabilidade de Prompts)

Progresso Total: ✅ MVP Completo
Status: 🚀 Pronto para produção
```

---

**Versão:** 0.1.0  
**Data:** 23 de Maio de 2026  
**Status:** 🚀 MVP em Desenvolvimento
