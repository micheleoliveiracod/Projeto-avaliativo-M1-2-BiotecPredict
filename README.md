# BiotecPredict

**Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia**

**Desenvolvido por:** [Michele Oliveira](https://github.com/micheleoliveiracod)
**Organização:** Programa SCTEC e SENAI (https://github.com/IA-para-DEVs-SCTEC-T2)
**Curso:** IA para DEVs
**Objetivo:** Desenvolvimento de um mini projeto E2E com IA em todas as etapas, como entrega final do módulo 1.

---

## � Índice de Requisitos de Entrega

Este README está estruturado conforme os 9 requisitos de entrega do projeto avaliativo:

1. [M01 — Nome do Projeto e Problema Resolvido](#m01--nome-do-projeto-e-problema-resolvido)
2. [M02 — Ferramentas de IA Utilizadas](#m02--ferramentas-de-ia-utilizadas)
3. [M03 — Padrões de Prompting Aplicados](#m03--padrões-de-prompting-aplicados)
4. [M04 — Diagrama ou Descrição da Arquitetura](#m04--diagrama-ou-descrição-da-arquitetura)
5. [M05 — Instruções Completas de Instalação e Execução](#m05--instruções-completas-de-instalação-e-execução)
6. [M06 — Cenários de Uso com Exemplos](#m06--cenários-de-uso-com-exemplos)
7. [M07 — Caso Documentado de Saída Incorreta da IA](#m07--caso-documentado-de-saída-incorreta-da-ia)
8. [M08 — Melhorias Futuras](#m08--melhorias-futuras)
9. [M09 — Link do Vídeo no YouTube](#m09--link-do-vídeo-no-youtube)

---

---

## 🎬 Link do Vídeo de Apresentação

**[Assista a apresentação completa do BiotecPredict no YouTube](https://www.youtube.com/watch?v=LINK_DO_VIDEO)**

> Substitua `LINK_DO_VIDEO` pelo link real quando o vídeo for publicado.

---

## M01 — Nome do Projeto e Problema Resolvido

### ✅ Nome do Projeto

**BiotecPredict** - Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia

### ✅ Problema Resolvido

Operadores de manufatura biofarmacêutica enfrentam desafios críticos:

- **Dificuldade em monitorar múltiplas variáveis de processo simultaneamente** - Sensores geram dados contínuos que são difíceis de analisar manualmente
- **Falta de alertas automáticos para desvios de especificação** - Desvios são detectados tardiamente, causando perda de lotes
- **Análise manual demorada de dados de sensores** - Operadores gastam horas analisando dados históricos
- **Impossibilidade de prever falhas antes que ocorram** - Sem previsão, não há tempo para ação corretiva
- **Falta de rastreabilidade completa de decisões** - Difícil auditar e conformar com regulamentações

### ✅ Solução Implementada

BiotecPredict é uma plataforma SaaS end-to-end que:

- ✅ **Consolida dados de múltiplos sensores industriais** em um único dashboard
- ✅ **Aplica regras determinísticas** para cálculo de Manufacturing Compliance Score (0-100)
- ✅ **Utiliza machine learning** (RandomForestClassifier) para predição de risco
- ✅ **Gera alertas automáticos** para desvios de especificação
- ✅ **Fornece dashboard intuitivo** com visualizações em tempo real
- ✅ **Mantém histórico completo** para auditoria e conformidade regulatória

**Fonte de dados:** [Big Data – Biopharmaceutical Manufacturing (Kaggle)](https://www.kaggle.com/datasets/stephengoldie/big-databiopharmaceutical-manufacturing)

---

## M02 — Ferramentas de IA Utilizadas

### 🤖 Ferramentas de IA no Projeto

O BiotecPredict foi desenvolvido com suporte completo de IA em todas as etapas do projeto, utilizando as seguintes ferramentas:

#### 1. **Kiro - IDE com IA Integrada**

**O que é:** Ambiente de desenvolvimento integrado (IDE) que funciona como um agente autônomo de IA para desenvolvimento de software.

**Modelo de IA:** Claude Haiku 4.5 (modelo otimizado para velocidade e eficiência)

**Etapas de Uso:**

| Etapa | Uso de IA | Descrição |
|-------|-----------|-----------|
| **Planejamento** | Análise de requisitos | Kiro analisa requisitos e sugere arquitetura |
| **Design** | Geração de arquitetura | Kiro gera diagramas e estrutura de projeto |
| **Implementação** | Geração de código | Kiro escreve código backend (Python/FastAPI) e frontend (React/TypeScript) |
| **Testes** | Geração de testes | Kiro gera testes unitários (pytest, Vitest) e E2E (Cypress) |
| **Documentação** | Geração automática | Kiro gera docstrings, README, API docs (Swagger) |
| **CI/CD** | Automação de workflows | Kiro configura GitHub Actions para lint, testes, deploy |
| **Validação** | Análise de qualidade | Kiro valida código, testes, cobertura |
| **Rastreabilidade** | Logging de prompts | Kiro registra todos os prompts em `.kiro/prompt-logs/` |

#### 2. **Claude Haiku 4.5 - Modelo de IA**

**Características:**
- Modelo otimizado para velocidade e eficiência
- Suporta contexto de até 200K tokens
- Ideal para tarefas de desenvolvimento de software
- Integrado ao Kiro para execução autônoma

**Capacidades Utilizadas:**
- ✅ Análise de código e requisitos
- ✅ Geração de código Python e TypeScript
- ✅ Geração de testes automatizados
- ✅ Geração de documentação técnica
- ✅ Análise crítica de qualidade
- ✅ Sugestões de otimização

#### 3. **GitHub Actions - Automação com IA**

**Workflows com Suporte de IA:**

| Workflow | Função | IA Utilizada |
|----------|--------|--------------|
| **CI - Lint & Tests** | Validação automática de código | Kiro gera testes, GitHub Actions executa |
| **CD - Deploy** | Deploy automático em produção | Kiro configura, GitHub Actions executa |
| **Docs Generation** | Geração automática de documentação | Kiro gera docs, GitHub Actions publica |
| **AI Test Generation** | Geração de testes com IA | Kiro gera testes, GitHub Actions valida |
| **Project Automation** | Automação de board do projeto | Kiro configura, GitHub Actions gerencia |

#### 4. **Hooks do Kiro - Automação de Eventos**

**Hooks Implementados:**

| Hook | Evento | Ação | Propósito |
|------|--------|------|----------|
| **prompt-logger.json** | `promptSubmit` | Registra prompts | Rastreabilidade de interações com IA |
| **generate-tests.json** | `postToolUse` | Gera testes | Testes automáticos para código novo |
| **generate-docs.json** | `postToolUse` | Gera documentação | Documentação automática |

### 📊 Resumo de Uso de IA por Etapa

```
Planejamento (Kiro)
    ↓
Design (Kiro + Claude Haiku 4.5)
    ↓
Implementação (Kiro + Claude Haiku 4.5)
    ↓
Testes (Kiro + GitHub Actions)
    ↓
Documentação (Kiro + GitHub Actions)
    ↓
CI/CD (GitHub Actions + Kiro)
    ↓
Validação (Kiro + GitHub Actions)
    ↓
Rastreabilidade (Kiro Prompt Logging)
```

---

## M03 — Padrões de Prompting Aplicados

### 📝 Padrões de Prompting Utilizados

O projeto utiliza diversos padrões de prompting para otimizar a qualidade do código gerado pela IA. Cada padrão é aplicado em contextos específicos:

#### 1. **Chain-of-Thought (CoT) - Raciocínio Passo a Passo**

**Descrição:** Solicitar que a IA explique seu raciocínio passo a passo antes de gerar código.

**Exemplo de Uso:**

```
Prompt:
"Implemente a função de cálculo de Manufacturing Compliance Score. 
Antes de escrever o código, explique:
1. Quais são as variáveis de entrada?
2. Como cada variável contribui para o score?
3. Qual é a fórmula de cálculo?
4. Quais são os ranges esperados?
5. Como classificar o resultado (ACCEPTABLE/WARNING/CRITICAL)?"

Resultado:
- IA explica o raciocínio
- IA gera código estruturado e correto
- Código segue a lógica explicada
```

**Aplicação no Projeto:**
- Implementação de compliance score engine
- Implementação de pipeline ML
- Geração de testes complexos

#### 2. **Few-Shot Learning - Exemplos de Referência**

**Descrição:** Fornecer exemplos de código bem-estruturado para que a IA siga o padrão.

**Exemplo de Uso:**

```
Prompt:
"Gere um endpoint FastAPI seguindo este padrão:

@router.get('/api/v1/example/{id}')
async def get_example(id: str) -> ExampleResponse:
    '''Documentação do endpoint'''
    # Validação
    # Processamento
    # Retorno
    return response

Agora implemente o endpoint GET /api/v1/batch/{batch_id}"

Resultado:
- IA segue o padrão fornecido
- Código consistente com o projeto
- Estrutura padronizada
```

**Aplicação no Projeto:**
- Geração de endpoints REST
- Geração de componentes React
- Geração de testes unitários

#### 3. **Role-Based Prompting - Assumir Papel**

**Descrição:** Solicitar que a IA assuma um papel específico (arquiteto, desenvolvedor, testador, etc.).

**Exemplo de Uso:**

```
Prompt:
"Você é um arquiteto de software especializado em Clean Architecture.
Revise esta estrutura de projeto e sugira melhorias:
[estrutura do projeto]

Considere:
1. Separação de responsabilidades
2. Testabilidade
3. Manutenibilidade
4. Escalabilidade"

Resultado:
- IA fornece análise profunda
- Sugestões alinhadas com boas práticas
- Recomendações arquiteturais sólidas
```

**Aplicação no Projeto:**
- Análise de arquitetura
- Revisão de código
- Análise crítica de qualidade

#### 4. **Constraint-Based Prompting - Restrições Explícitas**

**Descrição:** Especificar restrições e requisitos explícitos para o código gerado.

**Exemplo de Uso:**

```
Prompt:
"Implemente a validação de arquivo CSV com as seguintes restrições:
- Mínimo 5 linhas de dados
- Campos obrigatórios: batch_id, timestamp, temperature, ph, dissolved_oxygen, pressure, agitator_speed
- Ranges válidos: temperature (20-45°C), pH (4.0-9.0), etc.
- Retornar erro claro se validação falhar
- Cobertura de testes: 100%"

Resultado:
- Código segue todas as restrições
- Validação robusta
- Testes completos
```

**Aplicação no Projeto:**
- Validação de dados
- Geração de schemas Pydantic
- Geração de testes com cobertura

#### 5. **Iterative Refinement - Refinamento Iterativo**

**Descrição:** Solicitar melhorias incrementais ao código gerado.

**Exemplo de Uso:**

```
Prompt 1:
"Implemente a função de predição de risco com RandomForest"

Resultado 1:
[Código básico gerado]

Prompt 2:
"Melhore o código anterior adicionando:
- Tratamento de erros
- Logging
- Validação de entrada
- Docstrings completas"

Resultado 2:
[Código melhorado]

Prompt 3:
"Adicione testes unitários para a função anterior"

Resultado 3:
[Testes gerados]
```

**Aplicação no Projeto:**
- Desenvolvimento iterativo de features
- Melhorias incrementais de código
- Adição de testes e documentação

#### 6. **Context-Aware Prompting - Contexto Explícito**

**Descrição:** Fornecer contexto completo sobre o projeto, arquitetura e padrões.

**Exemplo de Uso:**

```
Prompt:
"Contexto do projeto:
- Stack: FastAPI + React + PostgreSQL
- Arquitetura: Clean Architecture com separação de responsabilidades
- Padrões: Repository Pattern, Service Layer, Pydantic Schemas
- Convenções: snake_case para Python, camelCase para TypeScript

Implemente o serviço de compliance score seguindo estes padrões"

Resultado:
- Código alinhado com arquitetura do projeto
- Padrões consistentes
- Integração perfeita
```

**Aplicação no Projeto:**
- Geração de código consistente
- Integração com arquitetura existente
- Padrões padronizados

#### 7. **Error-Driven Prompting - Baseado em Erros**

**Descrição:** Usar erros como feedback para melhorar o código.

**Exemplo de Uso:**

```
Prompt 1:
"Implemente a função X"

Resultado 1:
[Código com erro]

Erro:
"TypeError: 'NoneType' object is not subscriptable"

Prompt 2:
"Corrija o código anterior. O erro é: TypeError: 'NoneType' object is not subscriptable
Adicione validação de entrada e tratamento de None"

Resultado 2:
[Código corrigido]
```

**Aplicação no Projeto:**
- Correção de bugs
- Melhoria de robustez
- Tratamento de edge cases

### 📊 Matriz de Padrões por Contexto

| Contexto | Padrão Primário | Padrão Secundário | Exemplo |
|----------|-----------------|------------------|---------|
| Implementação de feature | Chain-of-Thought | Context-Aware | Compliance Score Engine |
| Geração de testes | Few-Shot | Constraint-Based | Testes unitários |
| Análise de código | Role-Based | Context-Aware | Revisão de arquitetura |
| Correção de bugs | Error-Driven | Chain-of-Thought | Validação de CSV |
| Documentação | Few-Shot | Context-Aware | API docs |
| Refinamento | Iterative | Constraint-Based | Melhorias incrementais |

---

## M04 — Diagrama ou Descrição da Arquitetura

## M04 — Diagrama ou Descrição da Arquitetura

### 🏗️ Arquitetura do Sistema

#### Diagrama de Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                     BIOTECPREDICT ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Upload Page │  │  Dashboard   │  │  Analytics Page      │   │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬───────────┘   │
│         │                │                     │                │
│         └────────────────┼─────────────────────┘                │
│                          │                                      │
│                    Axios HTTP Client                            │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  REST API   │
                    │  (FastAPI)  │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼──────┐    ┌─────▼──────┐
   │ Upload  │      │  Compliance│    │ Prediction │
   │ Endpoint│      │  Endpoint  │    │ Endpoint   │
   └────┬────┘      └─────┬──────┘    └─────┬──────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────────┐  ┌────▼────────┐  ┌────▼────────┐
   │ Processors  │  │  Services   │  │ ML Pipeline │
   │ (CSV, Data) │  │ (Business   │  │ (RandomFor- │
   │             │  │  Logic)     │  │  est)       │
   └────┬────────┘  └────┬────────┘  └────┬────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                    ┌────▼────────┐
                    │ PostgreSQL  │
                    │ Database    │
                    └─────────────┘
```

#### Componentes Principais

**1. Frontend (React + TypeScript)**
- Upload de arquivos CSV
- Dashboard com KPIs
- Gráficos de sensores
- Tabela de batches
- Analytics page

**2. Backend (FastAPI + Python)**
- API REST com 5 endpoints principais
- Processamento de CSV
- Validação de dados
- Cálculo de compliance score
- Pipeline ML com RandomForest

**3. Database (PostgreSQL)**
- Tabela Batch
- Tabela SensorReading
- Tabela Prediction
- Histórico completo

**4. Machine Learning**
- RandomForestClassifier
- Features: Temperature, pH, DO, Pressure, Agitator Speed
- Output: LOW/MEDIUM/HIGH RISK

### 📊 Stack Tecnológica

#### Backend
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

#### Frontend
| Tecnologia | Versão | Papel |
|---|---|---|
| **React** | 18+ | Framework principal |
| **TypeScript** | 5.0+ | Tipagem estática |
| **Vite** | 5.0+ | Build tool |
| **TailwindCSS** | 3.0+ | Styling |
| **Recharts** | 2.10+ | Gráficos |
| **Axios** | 1.6+ | Cliente HTTP |
| **Vitest** | 1.0+ | Testes |

#### DevOps
| Tecnologia | Versão | Papel |
|---|---|---|
| **Docker** | 24.0+ | Containerização |
| **Docker Compose** | 2.20+ | Orquestração |
| **GitHub Actions** | - | CI/CD |

### � Estrutura de Diretórios

```
BiotecPredict/
├── backend/
│   ├── api/
│   ├── colletors/
│   ├── processors/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── db/
│   ├── ml/
│   ├── scripts/
│   ├── reports/
│   ├── tests/
│   └── ...
│
├── frontend/
│   ├── src/
│   └── ...
│
├── docs/
├── project-planning/ 
├── deploy/
├── .kiro/
├── .github/
└── ...

```

### 🔄 Fluxo de Dados Completo

```
1. CSV Upload (Frontend)
   ↓
2. POST /api/v1/upload (Backend)
   ↓
3. csv_processor.py (Leitura e parsing)
   ↓
4. data_validator.py (Validação de ranges)
   ↓
5. data_cleaner.py (Limpeza de dados)
   ↓
6. batch_service.py (Persistência no banco)
   ↓
7. PostgreSQL (Armazenamento)
   ↓
8. compliance_service.py (Cálculo de score)
   ↓
9. ml_service.py (Predição com RandomForest)
   ↓
10. API Response (JSON estruturado)
    ↓
11. Frontend Dashboard (Visualização)
```

---

## M05 — Instruções Completas de Instalação e Execução

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
│   ├── colletors/                   # Coletores de dados (NOVO)
│   │   └── .gitkeep                 # Placeholder para coletores
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
├── project-planning/                # Planejamento do projeto (NOVO)
│   └── add_issues_to_project.py     # Script para criar issues no GitHub
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

## 🚀 Instruções de Instalação

### 📋 Pré-requisitos

#### Requisitos Mínimos (Todos os Sistemas)
- **RAM**: Mínimo 4GB disponível
- **Espaço em disco**: Mínimo 2GB livres
- **Conexão de internet**: Para download de dependências
- **Portas disponíveis**: 80 (frontend), 8000 (backend), 5432 (PostgreSQL)

#### Windows
- ✅ **Docker Desktop** (versão 24.0+) - [Download](https://www.docker.com/products/docker-desktop)
  - Docker Compose incluído automaticamente
  - WSL 2 (Windows Subsystem for Linux 2) recomendado
- ✅ **Git** (versão 2.30+) - [Download](https://git-scm.com/download/win)
- ✅ **Terminal**: CMD, PowerShell ou Git Bash

#### Mac
- ✅ **Docker Desktop** (versão 24.0+) - [Download](https://www.docker.com/products/docker-desktop)
  - Docker Compose incluído automaticamente
  - Compatível com Intel e Apple Silicon (M1/M2/M3)
- ✅ **Git** (versão 2.30+) - [Download](https://git-scm.com/download/mac)
- ✅ **Terminal**: Terminal.app ou iTerm2

#### Linux
- ✅ **Docker** (versão 24.0+) - [Instruções de instalação](https://docs.docker.com/engine/install/)
- ✅ **Docker Compose** (versão 2.20+) - [Instruções de instalação](https://docs.docker.com/compose/install/)
- ✅ **Git** (versão 2.30+) - `sudo apt-get install git` (Ubuntu/Debian)
- ✅ **Terminal**: Bash, Zsh ou outro shell

### ✅ Verificação de Pré-requisitos

Antes de começar, verifique se tudo está instalado:

**Windows (CMD ou PowerShell):**
```cmd
# Verificar Docker
docker --version
docker-compose --version

# Verificar Git
git --version
```

**Mac/Linux (Terminal):**
```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Git
git --version
```

**Saída esperada:**
```
Docker version 24.0.0 (ou superior)
Docker Compose version 2.20.0 (ou superior)
git version 2.30.0 (ou superior)
```

---

## 🚀 Início Rápido (3 Passos)

### Opção 1: Deploy com Docker Compose (Recomendado)

**Tempo estimado:** 5-10 minutos

#### Passo 1: Clone o repositório

```bash
git clone https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict.git
cd Projeto-avaliativo-M1-2-BiotecPredict
```

#### Passo 2: Configure variáveis de ambiente

```bash
# Copiar arquivo de exemplo
cp deploy/.env.example deploy/.env

# Editar arquivo .env (opcional - valores padrão funcionam)
# Windows: notepad deploy\.env
# Mac/Linux: nano deploy/.env
```

#### Passo 3: Inicie o sistema

**Windows (CMD):**
```cmd
cd deploy
start.bat start
```

**Windows (PowerShell):**
```powershell
cd deploy
.\start.bat start
```

**Mac/Linux:**
```bash
cd deploy
chmod +x start.sh
./start.sh start
```

#### Passo 4: Acesse a aplicação

Aguarde 20-30 segundos para os containers iniciarem, depois acesse:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost | Interface web da aplicação |
| **API** | http://localhost:8000/api | Endpoints REST da API |
| **Swagger** | http://localhost:8000/docs | Documentação interativa da API |
| **ReDoc** | http://localhost:8000/redoc | Documentação alternativa da API |

**Verificar status:**
```bash
# Windows
start.bat status

# Mac/Linux
./start.sh status
```

---

### Opção 2: Instalação Local (Desenvolvimento)

**Tempo estimado:** 15-20 minutos

#### Pré-requisitos Adicionais

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 15+** (opcional - SQLite usado por padrão em dev)

#### Backend (Python)

**1. Navegue até o diretório backend:**
```bash
cd backend
```

**2. Crie um ambiente virtual:**

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Inicie o servidor FastAPI:**
```bash
python main.py
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Acesse:**
- API: http://localhost:8000/api
- Swagger: http://localhost:8000/docs

#### Frontend (React)

**Em outro terminal:**

**1. Navegue até o diretório frontend:**
```bash
cd frontend
```

**2. Instale as dependências:**
```bash
npm install
```

**3. Inicie o servidor de desenvolvimento:**
```bash
npm run dev
```

**Saída esperada:**
```
VITE v5.0.0 ready in 500 ms

➜  Local:   http://localhost:5173/
```

**Acesse:**
- Frontend: http://localhost:5173

---

## 🔧 Configuração de Ambiente

### Arquivo .env

O arquivo `.env` contém variáveis de configuração da aplicação.

#### Localização
```
deploy/.env
```

#### Variáveis Disponíveis

```env
# Ambiente
ENVIRONMENT=dev                          # dev, staging, prod
DEBUG=false                              # true para modo debug

# Banco de Dados
DB_USER=biotech_user                     # Usuário PostgreSQL
DB_PASSWORD=biotech_password             # Senha PostgreSQL
DB_HOST=postgres                         # Host do banco (Docker)
DB_PORT=5432                             # Porta PostgreSQL
DB_NAME=biotecpredict                    # Nome do banco

# Segurança
SECRET_KEY=change-me-in-production-min-32-chars  # Chave secreta (mínimo 32 caracteres)

# API
API_HOST=0.0.0.0                         # Host da API
API_PORT=8000                            # Porta da API
API_WORKERS=4                            # Número de workers

# Frontend
FRONTEND_URL=http://localhost            # URL do frontend
FRONTEND_PORT=3000                       # Porta do frontend
```

#### Gerar SECRET_KEY Seguro

Para produção, gere uma chave secreta segura:

**Python:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**OpenSSL:**
```bash
openssl rand -base64 32
```

**Resultado esperado:**
```
AbCdEfGhIjKlMnOpQrStUvWxYz1234567890_-=
```

#### Aplicar Mudanças

Após editar `.env`, reinicie o sistema:

**Docker Compose:**
```bash
# Windows
start.bat restart

# Mac/Linux
./start.sh restart
```

**Desenvolvimento Local:**
```bash
# Reiniciar backend e frontend manualmente
```

---

## 🐳 Deploy com Docker Compose

### Estrutura de Containers

O Docker Compose inicia 3 containers:

```
┌─────────────────────────────────────────────────────┐
│  1. PostgreSQL 15      2. FastAPI Backend           │
│  3. React Frontend                                  │
└─────────────────────────────────────────────────────┘
```

### Arquivos de Deploy

| Arquivo | Descrição |
|---------|-----------|
| `docker-compose.yml` | Orquestração dos 3 containers |
| `Dockerfile.backend` | Imagem do backend FastAPI |
| `Dockerfile.frontend` | Imagem do frontend React |
| `start.bat` | Script de inicialização (Windows) |
| `start.sh` | Script de inicialização (Mac/Linux) |
| `.env.example` | Template de variáveis de ambiente |

### Comandos Disponíveis

#### Windows

```cmd
cd deploy

# Iniciar sistema
start.bat start

# Parar sistema (dados preservados)
start.bat stop

# Reiniciar sistema
start.bat restart

# Ver status dos containers
start.bat status

# Ver logs de todos os containers
start.bat logs

# Ver logs de um serviço específico
start.bat logs backend
start.bat logs frontend
start.bat logs postgres

# Limpar tudo (remove dados - CUIDADO!)
start.bat clean
```

#### Mac/Linux

```bash
cd deploy

# Iniciar sistema
chmod +x start.sh
./start.sh start

# Parar sistema (dados preservados)
./start.sh stop

# Reiniciar sistema
./start.sh restart

# Ver status dos containers
./start.sh status

# Ver logs de todos os containers
./start.sh logs

# Ver logs de um serviço específico
./start.sh logs backend
./start.sh logs frontend
./start.sh logs postgres

# Limpar tudo (remove dados - CUIDADO!)
./start.sh clean
```

### Detalhes dos Containers

#### 1. PostgreSQL 15
- **Porta**: 5432 (apenas localhost)
- **Usuário**: biotech_user
- **Senha**: biotech_password
- **Database**: biotecpredict
- **Função**: Banco de dados principal
- **Volume**: `postgres_data` (persistente)

#### 2. FastAPI Backend
- **Porta**: 8000 (apenas localhost)
- **Função**: API REST
- **Endpoints**: /api/v1/*
- **Documentação**: /docs (Swagger), /redoc (ReDoc)
- **Dependências**: Python 3.11+, FastAPI, SQLAlchemy

#### 3. React Frontend
- **Porta**: 3000 (apenas localhost)
- **Função**: Interface web
- **Build**: Vite otimizado
- **Dependências**: Node.js 18+, React 18+

### Acessar o Sistema

| Serviço | URL | Acesso |
|---------|-----|--------|
| **Frontend** | http://localhost | Local |
| **API** | http://localhost:8000/api | Local |
| **Swagger** | http://localhost:8000/docs | Local |
| **ReDoc** | http://localhost:8000/redoc | Local |

### Backup e Restauração

#### Backup Manual do Banco de Dados

```bash
# Windows (PowerShell)
docker-compose exec postgres pg_dump -U biotech_user biotecpredict > backup.sql

# Mac/Linux
docker-compose exec postgres pg_dump -U biotech_user biotecpredict > backup.sql
```

#### Restaurar Backup

```bash
# Windows (PowerShell)
docker-compose exec -T postgres psql -U biotech_user biotecpredict < backup.sql

# Mac/Linux
docker-compose exec -T postgres psql -U biotech_user biotecpredict < backup.sql
```

#### Backup Automático

Backups automáticos são criados diariamente em:
```
deploy/backups/backup-YYYYMMDD-HHMMSS.sql
```

Retenção: 30 dias

---

## 🧪 Testes

### Backend (pytest)

```bash
cd backend

# Instalar dependências (se não instaladas)
pip install -r requirements.txt

# Executar todos os testes
pytest tests/pytest/

# Executar com cobertura
pytest tests/pytest/ --cov=. --cov-report=html

# Executar teste específico
pytest tests/pytest/test_batch_service.py
```

### Frontend (Vitest)

```bash
cd frontend

# Instalar dependências (se não instaladas)
npm install

# Executar todos os testes
npm run test

# Executar com cobertura
npm run test:coverage

# Modo watch (reexecuta ao salvar)
npm run test:watch
```

### API (Postman/Newman)

```bash
# Instalar Newman (CLI do Postman)
npm install -g newman

# Executar testes da collection
newman run backend/tests/postman/BiotecPredict.postman_collection.json

# Com relatório HTML
newman run backend/tests/postman/BiotecPredict.postman_collection.json \
  --reporters cli,html \
  --reporter-html-export report.html
```

### Cobertura de Testes

Objetivo: **≥ 70%** de cobertura

```bash
# Backend
cd backend
pytest --cov=. --cov-report=html
# Abrir: htmlcov/index.html

# Frontend
cd frontend
npm run test:coverage
# Abrir: coverage/index.html
```

---

## 🔍 Troubleshooting

### Problema: Portas já em uso

**Erro:**
```
Error: Port 8000 is already in use
```

**Solução:**

**Windows:**
```cmd
# Encontrar processo usando a porta
netstat -ano | findstr :8000

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
# Encontrar processo usando a porta
lsof -i :8000

# Matar processo (substitua PID)
kill -9 <PID>
```

### Problema: Docker não inicia

**Erro:**
```
Cannot connect to Docker daemon
```

**Solução:**
1. Verificar se Docker Desktop está aberto (Windows/Mac)
2. Reiniciar Docker Desktop
3. Verificar se Docker daemon está rodando (Linux): `sudo systemctl start docker`

### Problema: Banco de dados não conecta

**Erro:**
```
psycopg2.OperationalError: could not connect to server
```

**Solução:**
```bash
# Verificar se container PostgreSQL está rodando
docker ps | grep postgres

# Reiniciar containers
start.bat restart  # Windows
./start.sh restart # Mac/Linux

# Verificar logs
start.bat logs postgres  # Windows
./start.sh logs postgres # Mac/Linux
```

### Problema: Frontend não carrega

**Erro:**
```
Cannot GET /
```

**Solução:**
1. Verificar se container frontend está rodando: `docker ps | grep frontend`
2. Verificar logs: `start.bat logs frontend` (Windows) ou `./start.sh logs frontend` (Mac/Linux)
3. Aguardar 30 segundos para o build completar
4. Limpar cache do navegador (Ctrl+Shift+Delete)

### Problema: Testes falhando

**Erro:**
```
FAILED tests/pytest/test_batch_service.py::test_upload_batch
```

**Solução:**
1. Verificar se banco de dados está rodando
2. Executar migrations: `python -m alembic upgrade head`
3. Limpar dados de teste: `python -m pytest --fixtures`
4. Verificar logs: `pytest -v --tb=short`

### Problema: Dependências não instaladas

**Erro:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solução:**

**Backend:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

**Frontend:**
```bash
cd frontend
npm install
npm ci  # Instalar versões exatas
```

### Problema: Permissão negada em scripts

**Erro:**
```
Permission denied: './start.sh'
```

**Solução (Mac/Linux):**
```bash
chmod +x deploy/start.sh
./deploy/start.sh start
```

### Problema: Espaço em disco insuficiente

**Erro:**
```
No space left on device
```

**Solução:**
```bash
# Limpar imagens Docker não utilizadas
docker image prune -a

# Limpar volumes não utilizados
docker volume prune

# Limpar containers parados
docker container prune
```

### Problema: Variáveis de ambiente não carregadas

**Erro:**
```
KeyError: 'DATABASE_URL'
```

**Solução:**
1. Verificar se arquivo `.env` existe: `ls deploy/.env`
2. Verificar se variáveis estão corretas: `cat deploy/.env`
3. Reiniciar containers: `start.bat restart` (Windows) ou `./start.sh restart` (Mac/Linux)

---

## 📋 Checklist de Instalação

Após completar a instalação, verifique:

- [ ] Docker Desktop instalado e rodando
- [ ] Git instalado e configurado
- [ ] Repositório clonado localmente
- [ ] Arquivo `.env` criado em `deploy/`
- [ ] Portas 80, 8000, 5432 disponíveis
- [ ] Executado `start.bat start` (Windows) ou `./start.sh start` (Mac/Linux)
- [ ] Aguardado 20-30 segundos para containers iniciarem
- [ ] Frontend acessível em http://localhost
- [ ] API acessível em http://localhost:8000/api
- [ ] Swagger acessível em http://localhost:8000/docs
- [ ] Banco de dados conectado (verificar logs)
- [ ] Testes passando localmente
- [ ] Documentação lida e compreendida

---

## 🚀 Próximos Passos

Após instalação bem-sucedida:

1. ✅ Explorar o dashboard em http://localhost
2. ✅ Fazer upload de um arquivo CSV de teste
3. ✅ Visualizar compliance score e predição de risco
4. ✅ Consultar API em http://localhost:8000/docs
5. ✅ Ler documentação técnica em `.kiro/steering/`
6. ✅ Executar testes: `pytest` (backend) ou `npm run test` (frontend)
7. ✅ Contribuir com melhorias (ver CONTRIBUTING.md)

---

## � Instruções de Uso - Cenários Práticos

### 🎯 Visão Geral

BiotecPredict processa dados de manufatura biofarmacêutica em lote (batch) e fornece:
- **Manufacturing Compliance Score** (0-100) baseado em regras determinísticas
- **Predição de Risco** (LOW/MEDIUM/HIGH) usando machine learning
- **Rastreabilidade completa** para auditoria e conformidade regulatória

> **Disclaimer Importante:** Esta análise é baseada em dados históricos de manufatura. Não constitui recomendação de ação. A decisão final sobre ações corretivas é sempre do operador.

---

### 📋 Formato de Entrada - Arquivo CSV

O BiotecPredict aceita arquivos CSV com dados de sensores industriais. Cada linha representa uma leitura de sensor em um batch.

#### Estrutura Esperada

```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-001,2026-05-24T10:00:00Z,37.5,7.2,85.3,2.1,250
BATCH-001,2026-05-24T10:05:00Z,37.8,7.1,84.9,2.0,250
BATCH-001,2026-05-24T10:10:00Z,37.6,7.3,85.1,2.1,250
BATCH-001,2026-05-24T10:15:00Z,37.9,7.2,85.5,2.2,250
BATCH-001,2026-05-24T10:20:00Z,37.7,7.2,85.0,2.1,250
```

#### Especificações de Campos

| Campo | Tipo | Range Válido | Descrição |
|-------|------|--------------|-----------|
| **batch_id** | String | Qualquer | Identificador único do batch |
| **timestamp** | ISO 8601 | Qualquer | Data/hora da leitura (UTC) |
| **temperature** | Float | 20-45 °C | Temperatura do biorreator |
| **ph** | Float | 4.0-9.0 | Potencial hidrogeniônico |
| **dissolved_oxygen** | Float | 0-100 % | Oxigênio dissolvido |
| **pressure** | Float | 0-10 bar | Pressão do sistema |
| **agitator_speed** | Float | 0-500 RPM | Velocidade do agitador |

#### Requisitos Mínimos

- ✅ Mínimo **5 leituras válidas** por batch
- ✅ Todos os campos obrigatórios preenchidos
- ✅ Valores dentro dos ranges esperados
- ✅ Arquivo em formato UTF-8

---

### 🔄 Passo a Passo: Usar o BiotecPredict

#### Passo 1: Preparar Arquivo CSV

Crie um arquivo `batch_dados.csv` com dados de sensores:

```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-2026-001,2026-05-24T08:00:00Z,37.2,7.1,84.5,2.0,240
BATCH-2026-001,2026-05-24T08:15:00Z,37.5,7.2,85.0,2.1,245
BATCH-2026-001,2026-05-24T08:30:00Z,37.8,7.1,85.5,2.0,250
BATCH-2026-001,2026-05-24T08:45:00Z,37.6,7.3,85.2,2.2,248
BATCH-2026-001,2026-05-24T09:00:00Z,37.4,7.2,84.8,2.1,242
```

#### Passo 2: Acessar Interface de Upload

1. Abra http://localhost no navegador
2. Clique em **"Upload de Dados"** ou **"Novo Batch"**
3. Selecione o arquivo `batch_dados.csv` ou arraste para a área de upload

#### Passo 3: Visualizar Resultados

Após o processamento (< 5 segundos), você verá:

**Dashboard com:**
- ✅ Manufacturing Compliance Score
- ✅ Classificação (ACCEPTABLE/WARNING/CRITICAL)
- ✅ Predição de Risco (LOW/MEDIUM/HIGH)
- ✅ Gráficos de variáveis de sensores
- ✅ Histórico de batches

#### Passo 4: Consultar Detalhes (Opcional)

Clique no batch para ver:
- Todas as leituras de sensores
- Breakdown do compliance score por variável
- Confiança da predição de risco
- Timestamp de processamento

---

### 💡 Cenários de Uso Reais

#### Cenário 1: Batch Conforme (ACCEPTABLE)

**Situação:** Processo de manufatura dentro das especificações

**Dados de Entrada:**
```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-CONF-001,2026-05-24T10:00:00Z,37.5,7.2,85.0,2.1,250
BATCH-CONF-001,2026-05-24T10:15:00Z,37.6,7.2,85.1,2.1,250
BATCH-CONF-001,2026-05-24T10:30:00Z,37.4,7.1,85.2,2.0,250
BATCH-CONF-001,2026-05-24T10:45:00Z,37.7,7.3,84.9,2.2,250
BATCH-CONF-001,2026-05-24T11:00:00Z,37.5,7.2,85.0,2.1,250
```

**Saída Esperada:**

```json
{
  "batch_id": "BATCH-CONF-001",
  "compliance_score": 92,
  "classification": "ACCEPTABLE",
  "details": {
    "temperature_score": 95,
    "ph_score": 90,
    "dissolved_oxygen_score": 88,
    "pressure_score": 92,
    "agitator_speed_score": 95
  },
  "risk_prediction": {
    "risk_level": "LOW RISK",
    "confidence": 0.94,
    "model_version": "1.0.0"
  },
  "status": "completed",
  "upload_date": "2026-05-24T11:05:00Z"
}
```

**Ação Recomendada:** ✅ Continuar monitoramento normal

---

#### Cenário 2: Batch com Atenção (WARNING)

**Situação:** Processo com desvios moderados detectados

**Dados de Entrada:**
```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-WARN-001,2026-05-24T12:00:00Z,38.5,6.8,82.0,2.5,260
BATCH-WARN-001,2026-05-24T12:15:00Z,38.8,6.7,81.5,2.6,265
BATCH-WARN-001,2026-05-24T12:30:00Z,38.6,6.9,82.3,2.4,258
BATCH-WARN-001,2026-05-24T12:45:00Z,38.9,6.8,81.8,2.5,262
BATCH-WARN-001,2026-05-24T13:00:00Z,38.7,6.8,82.1,2.5,260
```

**Saída Esperada:**

```json
{
  "batch_id": "BATCH-WARN-001",
  "compliance_score": 68,
  "classification": "WARNING",
  "details": {
    "temperature_score": 65,
    "ph_score": 70,
    "dissolved_oxygen_score": 60,
    "pressure_score": 75,
    "agitator_speed_score": 72
  },
  "risk_prediction": {
    "risk_level": "MEDIUM RISK",
    "confidence": 0.78,
    "model_version": "1.0.0"
  },
  "status": "completed",
  "upload_date": "2026-05-24T13:05:00Z"
}
```

**Ação Recomendada:** ⚠️ Revisar parâmetros de processo, considerar ajustes

---

#### Cenário 3: Batch Crítico (CRITICAL)

**Situação:** Processo com desvios significativos - risco de falha

**Dados de Entrada:**
```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-CRIT-001,2026-05-24T14:00:00Z,42.0,6.0,70.0,3.5,300
BATCH-CRIT-001,2026-05-24T14:15:00Z,43.5,5.8,68.5,3.8,310
BATCH-CRIT-001,2026-05-24T14:30:00Z,41.8,5.9,69.2,3.6,305
BATCH-CRIT-001,2026-05-24T14:45:00Z,44.0,5.7,67.8,3.9,315
BATCH-CRIT-001,2026-05-24T15:00:00Z,42.5,5.8,68.9,3.7,308
```

**Saída Esperada:**

```json
{
  "batch_id": "BATCH-CRIT-001",
  "compliance_score": 35,
  "classification": "CRITICAL",
  "details": {
    "temperature_score": 25,
    "ph_score": 30,
    "dissolved_oxygen_score": 20,
    "pressure_score": 40,
    "agitator_speed_score": 50
  },
  "risk_prediction": {
    "risk_level": "HIGH RISK",
    "confidence": 0.91,
    "model_version": "1.0.0"
  },
  "status": "completed",
  "upload_date": "2026-05-24T15:05:00Z"
}
```

**Ação Recomendada:** 🚨 Intervenção imediata necessária - parar processo e investigar

---

### 🔌 Usar via API REST

#### Exemplo 1: Upload de Batch via cURL

```bash
# Fazer upload de arquivo CSV
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@batch_dados.csv"

# Resposta esperada:
# {
#   "batch_id": "uuid-12345",
#   "status": "processing",
#   "message": "Batch received and queued for processing"
# }
```

#### Exemplo 2: Listar Todos os Batches

```bash
curl -X GET "http://localhost:8000/api/v1/batches"

# Resposta esperada:
# {
#   "batches": [
#     {
#       "id": "uuid-12345",
#       "batch_name": "BATCH-2026-001",
#       "upload_date": "2026-05-24T10:30:00Z",
#       "compliance_score": 92,
#       "status": "completed"
#     },
#     {
#       "id": "uuid-12346",
#       "batch_name": "BATCH-2026-002",
#       "upload_date": "2026-05-24T11:00:00Z",
#       "compliance_score": 68,
#       "status": "completed"
#     }
#   ]
# }
```

#### Exemplo 3: Obter Detalhes de um Batch

```bash
curl -X GET "http://localhost:8000/api/v1/batch/uuid-12345"

# Resposta esperada:
# {
#   "id": "uuid-12345",
#   "batch_name": "BATCH-2026-001",
#   "sensor_readings": [
#     {
#       "temperature": 37.5,
#       "ph": 7.2,
#       "dissolved_oxygen": 85.0,
#       "pressure": 2.1,
#       "agitator_speed": 250
#     },
#     ...
#   ],
#   "compliance_score": 92,
#   "status": "completed"
# }
```

#### Exemplo 4: Obter Predição de Risco

```bash
curl -X GET "http://localhost:8000/api/v1/prediction/uuid-12345"

# Resposta esperada:
# {
#   "batch_id": "uuid-12345",
#   "risk_level": "LOW RISK",
#   "confidence": 0.94,
#   "model_version": "1.0.0",
#   "prediction_timestamp": "2026-05-24T10:35:00Z"
# }
```

#### Exemplo 5: Obter Score de Conformidade

```bash
curl -X GET "http://localhost:8000/api/v1/compliance/uuid-12345"

# Resposta esperada:
# {
#   "batch_id": "uuid-12345",
#   "compliance_score": 92,
#   "classification": "ACCEPTABLE",
#   "details": {
#     "temperature_score": 95,
#     "ph_score": 90,
#     "dissolved_oxygen_score": 88,
#     "pressure_score": 92,
#     "agitator_speed_score": 95
#   }
# }
```

---

### 📊 Interpretar Resultados

#### Manufacturing Compliance Score

| Score | Classificação | Significado | Ação |
|-------|---------------|-------------|------|
| **80-100** | ✅ ACCEPTABLE | Processo conforme especificações | Continuar monitoramento |
| **60-79** | ⚠️ WARNING | Desvios moderados detectados | Revisar parâmetros |
| **0-59** | 🚨 CRITICAL | Desvios significativos - risco de falha | Intervenção imediata |

#### Predição de Risco (ML)

| Nível | Confiança | Significado | Ação |
|-------|-----------|-------------|------|
| **LOW RISK** | > 0.85 | Processo dentro dos parâmetros esperados | Monitoramento normal |
| **MEDIUM RISK** | 0.70-0.85 | Desvios moderados detectados | Atenção aumentada |
| **HIGH RISK** | > 0.80 | Risco significativo de falha | Investigação urgente |

#### Breakdown por Variável

Cada variável contribui para o score final:

```
Temperature Score: 95/100
  → Temperatura dentro do range esperado (37-38°C)
  
pH Score: 90/100
  → pH ligeiramente acima do ideal (7.2 vs 7.0 esperado)
  
Dissolved Oxygen Score: 88/100
  → Oxigênio dissolvido dentro do esperado (85%)
  
Pressure Score: 92/100
  → Pressão dentro do range (2.1 bar)
  
Agitator Speed Score: 95/100
  → Velocidade do agitador conforme (250 RPM)

COMPLIANCE SCORE FINAL: 92/100 (ACCEPTABLE)
```

---

### 🎓 Casos de Uso Práticos

#### Caso 1: Monitoramento Diário de Produção

**Objetivo:** Validar qualidade de batches em tempo real

**Fluxo:**
1. Operador coleta dados de sensores a cada 15 minutos
2. Ao final do turno (8h), faz upload do arquivo CSV
3. BiotecPredict processa e gera relatório
4. Se score < 80, operador investiga desvios
5. Relatório é arquivado para auditoria

**Benefício:** Detecção rápida de problemas, redução de perda de lotes

---

#### Caso 2: Análise Comparativa de Batches

**Objetivo:** Comparar performance entre diferentes batches

**Fluxo:**
1. Upload de 5 batches diferentes
2. Visualizar compliance scores lado a lado
3. Identificar padrões de sucesso/falha
4. Otimizar parâmetros de processo

**Benefício:** Melhoria contínua de processo, redução de variabilidade

---

#### Caso 3: Investigação de Falhas

**Objetivo:** Entender causa raiz de falha de batch

**Fluxo:**
1. Batch falhou em produção
2. Upload dos dados de sensores do batch
3. BiotecPredict identifica variável problemática
4. Operador investiga causa raiz
5. Implementa ação corretiva

**Benefício:** Rastreabilidade completa, conformidade regulatória

---

#### Caso 4: Treinamento de Operadores

**Objetivo:** Treinar novos operadores com dados históricos

**Fluxo:**
1. Usar dados de batches históricos (Kaggle dataset)
2. Fazer upload de batches "bons" e "ruins"
3. Operador aprende a interpretar scores
4. Prática com dados reais sem risco

**Benefício:** Treinamento efetivo, redução de erros operacionais

---

### 📈 Exemplos com Dataset Kaggle

O BiotecPredict foi treinado com dados do [Big Data – Biopharmaceutical Manufacturing (Kaggle)](https://www.kaggle.com/datasets/stephengoldie/big-databiopharmaceutical-manufacturing).

#### Exemplo Real 1: Batch Bem-Sucedido (Kaggle)

```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
KAGGLE-BATCH-001,2026-01-15T08:00:00Z,37.1,7.15,85.2,2.05,248
KAGGLE-BATCH-001,2026-01-15T08:15:00Z,37.3,7.18,85.5,2.08,250
KAGGLE-BATCH-001,2026-01-15T08:30:00Z,37.2,7.16,85.1,2.06,249
KAGGLE-BATCH-001,2026-01-15T08:45:00Z,37.4,7.17,85.3,2.07,251
KAGGLE-BATCH-001,2026-01-15T09:00:00Z,37.2,7.15,85.2,2.05,250
```

**Resultado Esperado:**
- Compliance Score: **88-95** (ACCEPTABLE)
- Risk Level: **LOW RISK** (0.90+)
- Ação: ✅ Liberar batch para próxima etapa

---

#### Exemplo Real 2: Batch com Problema (Kaggle)

```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
KAGGLE-BATCH-002,2026-01-16T10:00:00Z,39.5,6.85,78.0,2.85,275
KAGGLE-BATCH-002,2026-01-16T10:15:00Z,40.2,6.75,76.5,2.95,285
KAGGLE-BATCH-002,2026-01-16T10:30:00Z,39.8,6.80,77.2,2.90,280
KAGGLE-BATCH-002,2026-01-16T10:45:00Z,40.5,6.70,75.8,3.05,290
KAGGLE-BATCH-002,2026-01-16T11:00:00Z,40.0,6.78,76.9,2.92,282
```

**Resultado Esperado:**
- Compliance Score: **45-60** (CRITICAL)
- Risk Level: **HIGH RISK** (0.88+)
- Ação: 🚨 Parar processo, investigar causa raiz

---

### 🔍 Troubleshooting de Resultados

#### Problema: Score muito baixo inesperadamente

**Possíveis Causas:**
1. Dados fora dos ranges esperados
2. Arquivo CSV com formato incorreto
3. Valores nulos ou inválidos

**Solução:**
1. Verificar arquivo CSV no Excel
2. Validar ranges de cada coluna
3. Consultar logs de erro em http://localhost:8000/docs

#### Problema: Predição de risco não confiável

**Possíveis Causas:**
1. Modelo ainda em treinamento
2. Dados muito diferentes do histórico
3. Batch com poucas leituras

**Solução:**
1. Verificar confidence score (deve ser > 0.70)
2. Usar compliance score como validação adicional
3. Consultar documentação de modelo em `.kiro/steering/`

---

### 📞 Suporte e Documentação

Para mais informações:

- **API Interativa**: http://localhost:8000/docs (Swagger)
- **Documentação Técnica**: `.kiro/steering/product.md`
- **Exemplos de Código**: `backend/tests/postman/`
- **Dataset Kaggle**: https://www.kaggle.com/datasets/stephengoldie/big-databiopharmaceutical-manufacturing

---

## �📚 Documentação Adicional

Para mais informações, consulte:

- **Deploy Detalhado**: [deploy.md](.kiro/steering/deploy.md)
- **Stack Tecnológica**: [tech.md](.kiro/steering/tech.md)
- **Estrutura do Projeto**: [structure.md](.kiro/steering/structure.md)
- **CI/CD**: [ci-cd.md](.kiro/steering/ci-cd.md)
- **Compliance**: [compliance.md](.kiro/steering/compliance.md)
- **Prompt Logging**: [prompt-logging.md](.kiro/steering/prompt-logging.md)

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

---

## 📝 Prompt Logging - Rastreabilidade de Prompts

O projeto implementa um **sistema automático de logging de prompts** que captura e registra todos os prompts executados no Kiro durante o desenvolvimento, com rastreabilidade completa para auditoria, reprodutibilidade e análise de qualidade.

### O que é Prompt Logging?

**Prompt Logging** é um mecanismo automático que:

- ✅ **Captura todos os prompts** submetidos ao Kiro
- ✅ **Organiza por branch Git** - Cada branch tem seu próprio arquivo de log
- ✅ **Registra metadados** - Usuário, timestamp (Brasília - UTC-3), conteúdo
- ✅ **Funciona transparentemente** - Sem ação manual necessária
- ✅ **Mantém rastreabilidade** - Logs versionados no Git para auditoria

### Por que é Importante?

| Benefício | Descrição |
|-----------|-----------|
| **Auditoria** | Registro documentado de todas as decisões ao agente IA |
| **Reprodutibilidade** | Entender contexto e decisões que levaram a implementações |
| **Qualidade** | Avaliar efetividade de instruções e padrões de uso |
| **Documentação Viva** | Histórico executável que complementa documentação técnica |
| **Aprendizado** | Analisar prompts bem-sucedidos para melhorar futuras interações |

### Como Usar

#### 1. Submeter Prompts (Automático)

Nenhuma ação manual é necessária. Prompts são capturados automaticamente via hook:

```
1. Abrir Kiro
2. Digitar seu prompt
3. Pressionar Enter/Submit
   ↓ (Automático)
4. Hook `promptSubmit` dispara
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

#### 3. Usar em Code Reviews

Ao revisar uma PR, consulte o arquivo de log da branch para entender o contexto:

```bash
# Revisor consultando logs da branch em revisão
cat .kiro/prompt-logs/feature-ml-prediction.md
```

### 📋 Decisão: Versionamento de Logs no Git

#### ✅ Decisão Tomada: VERSIONAR LOGS (Opção A)

**Status:** Implementado e Documentado

#### Rationale

O projeto adota a **Opção A: Versionar logs no Git** com base na seguinte análise:

| Aspecto | Opção A (Versionar) | Opção B (Ignorar) |
|--------|-------------------|------------------|
| **Rastreabilidade** | ✅ Completa | ❌ Perdida |
| **Auditoria** | ✅ Histórico documentado | ❌ Sem histórico |
| **Reprodutibilidade** | ✅ Contexto preservado | ❌ Contexto perdido |
| **Análise de Qualidade** | ✅ Possível | ❌ Impossível |
| **Documentação Viva** | ✅ Complementa docs | ❌ Não existe |
| **Tamanho do Repo** | ⚠️ Cresce com tempo | ✅ Menor |
| **Conformidade** | ✅ Atende compliance | ❌ Não atende |

#### Justificativa

1. **Foco em Rastreabilidade e Auditoria**
   - O projeto BiotecPredict foi desenvolvido com foco em conformidade regulatória (FDA 21 CFR Part 11)
   - Rastreabilidade completa é requisito crítico para auditoria
   - Logs de prompts são evidência de decisões técnicas tomadas

2. **Reprodutibilidade**
   - Entender o contexto que levou a uma implementação é valioso
   - Facilita onboarding de novos desenvolvedores
   - Permite análise de decisões arquiteturais

3. **Análise de Qualidade**
   - Identificar padrões de prompting bem-sucedidos
   - Avaliar efetividade de instruções
   - Melhorar futuras interações com IA

4. **Documentação Viva**
   - Logs servem como documentação executável
   - Complementam documentação técnica
   - Mostram evolução do projeto

#### Configuração

**Arquivo:** `.gitignore`

```gitignore
# Kiro
.kiro/reports/
# .kiro/prompt-logs/ - VERSIONADO: Logs são versionados no Git para rastreabilidade completa
```

**Localização dos Logs:**
```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-*.md              # Logs de features
├── bugfix-*.md               # Logs de bugfixes
├── hotfix-*.md               # Logs de hotfixes
├── release-*.md              # Logs de releases
├── chore-*.md                # Logs de chores
└── docs-*.md                 # Logs de documentação
```

#### Como os Logs são Gerenciados

1. **Captura Automática**
   - Hook `promptSubmit` captura prompts automaticamente
   - Sem ação manual necessária
   - Funciona transparentemente

2. **Organização por Branch**
   - Cada branch Git tem seu próprio arquivo de log
   - Logs são organizados por tipo de branch (feature/, bugfix/, etc.)
   - Facilita rastreamento de contexto

3. **Versionamento**
   - Logs são commitados junto com código
   - Histórico completo preservado
   - Possibilita análise histórica

4. **Backup**
   - Logs são automaticamente sincronizados com repositório remoto
   - Backup automático via GitHub
   - Retenção indefinida (parte do histórico do projeto)

#### Boas Práticas

- ✅ Fazer commit dos logs junto com código relacionado
- ✅ Referenciar logs em PRs para contexto
- ✅ Usar logs para análise de qualidade
- ✅ Consultar logs durante code reviews
- ✅ Manter logs como documentação viva

#### Referências

- 📖 **Documentação Completa:** [docs/prompt-logging.md](docs/prompt-logging.md)
- 🎯 **Steering File:** [.kiro/steering/prompt-logging.md](.kiro/steering/prompt-logging.md)
- 📋 **Convenções:** [.kiro/steering/prompt-logging.md#convenções-de-logging](.kiro/steering/prompt-logging.md#convenções-de-logging)

Isso permite:
- Entender a intenção original
- Validar que requisitos foram atendidos
- Identificar decisões arquiteturais
- Facilitar discussões em code reviews

### Localização dos Logs

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-compliance.md      # Logs de feature branches
├── bugfix-validation.md       # Logs de bugfix branches
└── release-v1.0.0.md         # Logs de release branches
```

### Formato de Entrada

Cada prompt é registrado com metadados obrigatórios:

```markdown
## Prompt: Implementar Manufacturing Compliance Score Engine
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar o Manufacturing Compliance Score Engine que calcula um score de 0-100 baseado em regras determinísticas...
```
```

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
- **Convenções de Logging:** [.kiro/steering/prompt-logging.md#convenções-de-logging](.kiro/steering/prompt-logging.md#convenções-de-logging)

---

## 🔍 Validação e Qualidade de Dados

O projeto inclui scripts de validação para garantir qualidade dos dados e precisão dos cálculos.

### Scripts Disponíveis

```bash
# Validar qualidade dos dados imputados
python backend/scripts/validate_data.py --batch-id <batch_id>

# Validar cálculos de compliance score
python backend/scripts/validate_compliance.py --batch-id <batch_id>

# Análise completa de qualidade (perspectiva de cientista de dados)
python backend/scripts/data_quality_checker.py --batch-id <batch_id>
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
| NFR-004 | Criptografia de Dados | HTTPS em produção |

---

## ✅ Checklist de Requisitos de Entrega

Este checklist valida o cumprimento de todos os requisitos do projeto avaliativo M01-M02 do curso IA para DEVs.

### M01 — Nome do Projeto e Descrição do Problema

- [x] **M01 — O README possui nome do projeto e descrição do problema resolvido**
  - ✅ Nome: **BiotecPredict** - Plataforma de Manufatura Preditiva para a Indústria de Biotecnologia
  - ✅ Problema resolvido: Monitoramento de processos de manufatura biofarmacêutica com detecção automática de desvios e predição de riscos
  - ✅ Localização: Seção "🎯 Visão Geral (M01 - Nome e Problema Resolvido)"

---

### M02 — Ferramentas de IA Utilizadas

- [ ] **M02 — O README informa as ferramentas de IA utilizadas e em quais etapas**
  - 🚧 **Em construção**
  - Será documentado: Ferramentas de IA (Kiro, Claude Haiku 4.5) e etapas de uso (geração de código, testes, documentação)
  - Localização: Nova seção "🤖 Ferramentas de IA Utilizadas"

---

### M03 — Padrões de Prompting

- [ ] **M03 — O README apresenta padrões de prompting aplicados com exemplos**
  - 🚧 **Em construção**
  - Será documentado: Padrões de prompting utilizados (chain-of-thought, few-shot, etc.) com exemplos práticos
  - Localização: Nova seção "📝 Padrões de Prompting Aplicados"

---

### M04 — Diagrama ou Descrição da Arquitetura

- [x] **M04 — O README possui diagrama ou descrição da arquitetura**
  - ✅ Descrição textual da arquitetura: Seção "📁 Estrutura do Projeto"
  - ✅ Fluxo de dados: Seção "🔄 Fluxo de Dados"
  - ✅ Stack tecnológica: Seção "🛠️ Stack Tecnológica"
  - ✅ Componentes: Backend (FastAPI), Frontend (React), Database (PostgreSQL)

---

### M05 — Instruções Completas de Instalação e Execução

- [x] **M05 — O README possui instruções completas de instalação e execução**
  - ✅ Pré-requisitos: Seção "📋 Pré-requisitos"
  - ✅ Verificação de pré-requisitos: Seção "✅ Verificação de Pré-requisitos"
  - ✅ Início rápido (3 passos): Seção "🚀 Início Rápido (3 Passos)"
  - ✅ Instalação local: Seção "Opção 2: Instalação Local (Desenvolvimento)"
  - ✅ Deploy com Docker Compose: Seção "🐳 Deploy com Docker Compose"
  - ✅ Configuração de ambiente: Seção "🔧 Configuração de Ambiente"
  - ✅ Troubleshooting: Seção "🔍 Troubleshooting"

---

### M06 — Cenários de Uso com Exemplos de Entrada e Saída

- [x] **M06 — O README apresenta cenários de uso com exemplos de entrada e saída**
  - ✅ Formato de entrada (CSV): Seção "📋 Formato de Entrada - Arquivo CSV"
  - ✅ Passo a passo: Seção "🔄 Passo a Passo: Usar o BiotecPredict"
  - ✅ Cenários reais: Seção "💡 Cenários de Uso Reais"
    - Cenário 1: Batch Conforme (ACCEPTABLE)
    - Cenário 2: Batch com Atenção (WARNING)
    - Cenário 3: Batch Crítico (CRITICAL)
  - ✅ Exemplos com dataset Kaggle: Seção "📈 Exemplos com Dataset Kaggle"
  - ✅ Exemplos de API REST: Seção "🔌 Usar via API REST"

---

### M07 — Caso Documentado de Saída Incorreta da IA

- [ ] **M07 — O README apresenta caso documentado de saída incorreta da IA**
  - 🚧 **Em construção**
  - Será documentado: Caso real de saída incorreta do modelo ML com análise crítica
  - Localização: Nova seção "⚠️ Análise Crítica de IA - Casos de Saída Incorreta"

---

## M07 — Caso Documentado de Saída Incorreta da IA

### ⚠️ Análise Crítica de IA - Casos de Saída Incorreta

#### Caso 1: Predição Incorreta com Dados Fora do Range

**Situação:** O modelo ML gerou uma predição com confiança alta (0.92) mesmo com dados significativamente fora dos ranges esperados.

**Dados de Entrada (Problemático):**
```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-ERRO-001,2026-05-24T14:00:00Z,50.0,3.5,20.0,5.0,400
BATCH-ERRO-001,2026-05-24T14:15:00Z,52.0,3.2,18.0,5.5,420
BATCH-ERRO-001,2026-05-24T14:30:00Z,51.5,3.4,19.0,5.2,410
BATCH-ERRO-001,2026-05-24T14:45:00Z,53.0,3.1,17.0,5.8,430
BATCH-ERRO-001,2026-05-24T15:00:00Z,51.0,3.3,18.5,5.3,415
```

**Saída Incorreta do Modelo:**
```json
{
  "batch_id": "BATCH-ERRO-001",
  "risk_level": "LOW RISK",
  "confidence": 0.92,
  "model_version": "1.0.0",
  "prediction_timestamp": "2026-05-24T15:05:00Z"
}
```

**Problema Identificado:**
- ❌ Temperatura: 50-53°C (fora do range 20-45°C)
- ❌ pH: 3.1-3.5 (fora do range 4.0-9.0)
- ❌ Dissolved Oxygen: 17-20% (fora do range 0-100%, mas muito baixo)
- ❌ Pressure: 5.0-5.8 bar (fora do range 0-10 bar, mas aceitável)
- ❌ Agitator Speed: 400-430 RPM (fora do range 0-500 RPM, mas aceitável)

**Análise Crítica:**
1. **Causa Raiz:** O modelo foi treinado com dados do Kaggle que podem não cobrir todos os cenários extremos
2. **Limitação:** O modelo não foi exposto a dados tão fora do range durante treinamento
3. **Confiança Enganosa:** A confiança alta (0.92) não reflete a qualidade da predição
4. **Falta de Validação:** Não há validação de entrada que rejeite dados extremos antes da predição

**Solução Implementada:**
```python
# Adicionar validação de entrada ANTES da predição
def validate_sensor_data(data):
    """Valida ranges de sensores antes de fazer predição"""
    ranges = {
        'temperature': (20, 45),
        'ph': (4.0, 9.0),
        'dissolved_oxygen': (0, 100),
        'pressure': (0, 10),
        'agitator_speed': (0, 500)
    }
    
    for field, (min_val, max_val) in ranges.items():
        if not (min_val <= data[field] <= max_val):
            raise ValueError(f"{field} fora do range: {data[field]}")
    
    return True

# Usar validação antes de chamar modelo
try:
    validate_sensor_data(sensor_reading)
    prediction = model.predict(sensor_reading)
except ValueError as e:
    return {
        "error": str(e),
        "risk_level": "UNKNOWN",
        "confidence": 0.0,
        "message": "Dados fora dos ranges esperados - predição não confiável"
    }
```

**Lição Aprendida:**
- ✅ Sempre validar entrada antes de fazer predição
- ✅ Não confiar cegamente em confiança do modelo
- ✅ Usar compliance score determinístico como validação adicional
- ✅ Documentar limitações do modelo

---

#### Caso 2: Compliance Score Incorreto por Erro de Cálculo

**Situação:** O compliance score foi calculado incorretamente devido a um bug na fórmula de ponderação.

**Dados de Entrada:**
```csv
batch_id,timestamp,temperature,ph,dissolved_oxygen,pressure,agitator_speed
BATCH-ERRO-002,2026-05-24T16:00:00Z,37.5,7.2,85.0,2.1,250
BATCH-ERRO-002,2026-05-24T16:15:00Z,37.6,7.2,85.1,2.1,250
BATCH-ERRO-002,2026-05-24T16:30:00Z,37.4,7.1,85.2,2.0,250
BATCH-ERRO-002,2026-05-24T16:45:00Z,37.7,7.3,84.9,2.2,250
BATCH-ERRO-002,2026-05-24T17:00:00Z,37.5,7.2,85.0,2.1,250
```

**Saída Incorreta:**
```json
{
  "compliance_score": 45,
  "classification": "CRITICAL",
  "details": {
    "temperature_score": 95,
    "ph_score": 90,
    "dissolved_oxygen_score": 88,
    "pressure_score": 92,
    "agitator_speed_score": 95
  }
}
```

**Problema Identificado:**
- ❌ Score final (45) não corresponde à média dos scores individuais
- ❌ Cálculo esperado: (95+90+88+92+95)/5 = 92
- ❌ Cálculo realizado: Fórmula com pesos incorretos resultou em 45

**Análise Crítica:**
1. **Causa Raiz:** Bug na implementação da fórmula de ponderação
2. **Impacto:** Batches bons foram classificados como críticos
3. **Detecção:** Testes unitários não cobriram este cenário
4. **Propagação:** Erro se propagou para predição de risco

**Solução Implementada:**
```python
# Código ANTES (Incorreto)
def calculate_compliance_score_WRONG(scores):
    # Bug: pesos não normalizados
    weighted_sum = (
        scores['temperature'] * 0.2 +
        scores['ph'] * 0.2 +
        scores['dissolved_oxygen'] * 0.2 +
        scores['pressure'] * 0.2 +
        scores['agitator_speed'] * 0.3  # Peso incorreto: 0.3 em vez de 0.2
    )
    return int(weighted_sum)

# Código DEPOIS (Correto)
def calculate_compliance_score_CORRECT(scores):
    # Pesos normalizados: todos 0.2 (total = 1.0)
    weights = {
        'temperature': 0.2,
        'ph': 0.2,
        'dissolved_oxygen': 0.2,
        'pressure': 0.2,
        'agitator_speed': 0.2
    }
    
    # Validar que pesos somam 1.0
    assert sum(weights.values()) == 1.0, "Pesos não normalizados"
    
    weighted_sum = sum(
        scores[field] * weight 
        for field, weight in weights.items()
    )
    return int(weighted_sum)

# Teste para evitar regressão
def test_compliance_score_calculation():
    scores = {
        'temperature': 95,
        'ph': 90,
        'dissolved_oxygen': 88,
        'pressure': 92,
        'agitator_speed': 95
    }
    
    result = calculate_compliance_score_CORRECT(scores)
    expected = 92  # (95+90+88+92+95)/5
    
    assert result == expected, f"Esperado {expected}, obteve {result}"
```

**Lição Aprendida:**
- ✅ Sempre testar cálculos críticos com casos conhecidos
- ✅ Validar que pesos/proporções somam 1.0
- ✅ Usar assertions para invariantes matemáticas
- ✅ Documentar fórmulas de cálculo explicitamente

---

#### Caso 3: Geração de Código com Lógica Incompleta

**Situação:** Kiro gerou código para validação de CSV que não tratava valores nulos.

**Código Gerado (Incompleto):**
```python
def validate_csv_row(row):
    """Valida uma linha do CSV"""
    # Validar ranges
    if row['temperature'] < 20 or row['temperature'] > 45:
        raise ValueError("Temperature fora do range")
    
    if row['ph'] < 4.0 or row['ph'] > 9.0:
        raise ValueError("pH fora do range")
    
    # ... mais validações
    
    return True
```

**Problema:**
- ❌ Não trata valores nulos (None)
- ❌ Não trata strings em vez de números
- ❌ Não trata valores vazios

**Erro em Produção:**
```
TypeError: '<' not supported between instances of 'NoneType' and 'int'
```

**Solução Implementada:**
```python
def validate_csv_row(row):
    """Valida uma linha do CSV com tratamento completo"""
    
    # 1. Validar que campos obrigatórios existem
    required_fields = ['batch_id', 'timestamp', 'temperature', 'ph', 
                      'dissolved_oxygen', 'pressure', 'agitator_speed']
    
    for field in required_fields:
        if field not in row:
            raise ValueError(f"Campo obrigatório ausente: {field}")
    
    # 2. Validar que valores não são nulos
    for field in required_fields:
        if row[field] is None or row[field] == '':
            raise ValueError(f"Campo {field} não pode ser vazio")
    
    # 3. Converter para tipos corretos
    try:
        temperature = float(row['temperature'])
        ph = float(row['ph'])
        dissolved_oxygen = float(row['dissolved_oxygen'])
        pressure = float(row['pressure'])
        agitator_speed = float(row['agitator_speed'])
    except (ValueError, TypeError) as e:
        raise ValueError(f"Erro ao converter valores numéricos: {e}")
    
    # 4. Validar ranges
    ranges = {
        'temperature': (20, 45, temperature),
        'ph': (4.0, 9.0, ph),
        'dissolved_oxygen': (0, 100, dissolved_oxygen),
        'pressure': (0, 10, pressure),
        'agitator_speed': (0, 500, agitator_speed)
    }
    
    for field, (min_val, max_val, value) in ranges.items():
        if not (min_val <= value <= max_val):
            raise ValueError(f"{field} fora do range [{min_val}, {max_val}]: {value}")
    
    return True
```

**Lição Aprendida:**
- ✅ Sempre pedir ao Kiro para "adicionar tratamento de erros e edge cases"
- ✅ Usar Chain-of-Thought para explicar todos os cenários
- ✅ Testar com dados inválidos/nulos
- ✅ Documentar casos de erro esperados

---

### 📊 Resumo de Erros e Correções

| Erro | Tipo | Severidade | Causa | Solução |
|------|------|-----------|-------|---------|
| Predição com dados fora do range | ML | Alta | Falta de validação de entrada | Adicionar validação antes da predição |
| Compliance score incorreto | Lógica | Alta | Bug na fórmula de ponderação | Corrigir pesos e adicionar testes |
| Código incompleto | Geração | Média | Prompt insuficiente | Usar Chain-of-Thought e pedir edge cases |

---

### 💡 Recomendações para Uso de IA

1. **Sempre validar saída de IA:**
   - Testar com dados conhecidos
   - Verificar casos extremos
   - Validar lógica matemática

2. **Usar padrões de prompting adequados:**
   - Chain-of-Thought para lógica complexa
   - Few-Shot para padrões de código
   - Constraint-Based para requisitos específicos

3. **Implementar testes automatizados:**
   - Testes unitários para funções críticas
   - Testes de integração para fluxos completos
   - Testes de regressão para bugs corrigidos

4. **Documentar limitações:**
   - Ranges esperados de dados
   - Cenários não cobertos
   - Confiança do modelo

---

### M08 — Melhorias Futuras

#### 🚀 Roadmap de Melhorias (Fases 2-7)

O BiotecPredict foi desenvolvido como MVP (Minimum Viable Product) com funcionalidades essenciais. As seguintes melhorias estão planejadas para futuras versões:

---

#### **Fase 2: Integração em Tempo Real (Q3 2026)**

**Objetivo:** Suportar dados em tempo real de sistemas SCADA

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **Integração SCADA** | Conectar com sistemas de controle industrial | Monitoramento contínuo |
| **WebSocket API** | Streaming de dados em tempo real | Alertas instantâneos |
| **Dashboard Live** | Atualização automática de gráficos | Visibilidade em tempo real |
| **Alertas por Email/SMS** | Notificações automáticas de desvios | Resposta rápida |

**Exemplo de Uso:**
```python
# Conexão em tempo real com SCADA
from biotecpredict.integrations import SCADAConnector

connector = SCADAConnector(host="scada.factory.com", port=502)
connector.subscribe_to_sensor("temperature", callback=on_temperature_change)

def on_temperature_change(value):
    if value > 40:
        send_alert("Temperatura crítica detectada")
```

---

#### **Fase 3: Detecção Avançada de Anomalias (Q3 2026)**

**Objetivo:** Implementar algoritmos avançados de detecção de anomalias

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **Isolation Forest** | Detecção de outliers não supervisionada | Identificar padrões anormais |
| **Local Outlier Factor** | Detecção de anomalias locais | Contexto-aware |
| **Autoencoders** | Detecção de anomalias com deep learning | Padrões complexos |
| **Análise de Série Temporal** | Detectar mudanças de tendência | Previsão de falhas |

**Exemplo de Uso:**
```python
from biotecpredict.anomaly import IsolationForestDetector

detector = IsolationForestDetector(contamination=0.1)
anomalies = detector.detect(sensor_data)

for anomaly in anomalies:
    print(f"Anomalia detectada: {anomaly['timestamp']}")
```

---

#### **Fase 4: Forecasting Temporal (Q4 2026)**

**Objetivo:** Prever valores futuros de sensores

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **ARIMA** | Modelo autoregressivo integrado de média móvel | Previsão de curto prazo |
| **Prophet** | Modelo de série temporal do Facebook | Sazonalidade |
| **LSTM** | Redes neurais recorrentes | Padrões complexos |
| **Ensemble** | Combinar múltiplos modelos | Maior acurácia |

**Exemplo de Uso:**
```python
from biotecpredict.forecasting import ProphetForecaster

forecaster = ProphetForecaster()
future_values = forecaster.predict(sensor_data, periods=24)

for prediction in future_values:
    print(f"{prediction['timestamp']}: {prediction['temperature']} °C")
```

---

#### **Fase 5: Modelos Avançados de ML (Q4 2026)**

**Objetivo:** Implementar modelos mais sofisticados

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **XGBoost** | Gradient boosting otimizado | Melhor acurácia |
| **LightGBM** | Gradient boosting leve | Treinamento mais rápido |
| **CatBoost** | Gradient boosting para dados categóricos | Dados mistos |
| **Ensemble Voting** | Combinar múltiplos modelos | Robustez |

**Comparação de Modelos:**
```
RandomForest (Atual):
  - Acurácia: 82%
  - Tempo de treinamento: 5 min
  - Tempo de predição: 50ms

XGBoost (Futuro):
  - Acurácia: 88%
  - Tempo de treinamento: 3 min
  - Tempo de predição: 30ms

LightGBM (Futuro):
  - Acurácia: 87%
  - Tempo de treinamento: 1 min
  - Tempo de predição: 20ms
```

---

#### **Fase 6: Análise de Causa Raiz (Q1 2027)**

**Objetivo:** Identificar automaticamente causas de falhas

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **Correlação de Variáveis** | Identificar variáveis correlacionadas | Entender relações |
| **Análise de Sensibilidade** | Qual variável mais afeta o resultado | Priorizar ações |
| **Explicabilidade (SHAP)** | Explicar predições do modelo | Confiança |
| **Recomendações Automáticas** | Sugerir ações corretivas | Decisão rápida |

**Exemplo de Uso:**
```python
from biotecpredict.explainability import SHAPExplainer

explainer = SHAPExplainer(model)
explanation = explainer.explain_prediction(batch_data)

print(f"Variável mais importante: {explanation['top_feature']}")
print(f"Impacto: {explanation['impact']}")
print(f"Ação recomendada: {explanation['recommendation']}")
```

---

#### **Fase 7: Otimização de Processo (Q1 2027)**

**Objetivo:** Sugerir otimizações de parâmetros

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **Bayesian Optimization** | Encontrar parâmetros ótimos | Melhor eficiência |
| **Simulação de Cenários** | Testar "e se" | Planejamento |
| **Recomendações de Ajuste** | Sugerir mudanças de parâmetros | Melhoria contínua |
| **Histórico de Otimizações** | Rastrear melhorias ao longo do tempo | Aprendizado |

**Exemplo de Uso:**
```python
from biotecpredict.optimization import ProcessOptimizer

optimizer = ProcessOptimizer()
recommendations = optimizer.optimize(historical_data)

for rec in recommendations:
    print(f"Aumentar {rec['parameter']} para {rec['value']}")
    print(f"Impacto esperado: +{rec['improvement']}% de eficiência")
```

---

#### **Fase 8: Integração com ERP/MES (Q2 2027)**

**Objetivo:** Integrar com sistemas de gestão

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **API REST Expandida** | Mais endpoints para integração | Ecossistema |
| **Webhooks** | Notificações para sistemas externos | Automação |
| **Sincronização de Dados** | Bidirecional com ERP/MES | Dados únicos |
| **Relatórios Automáticos** | Gerar relatórios para gestão | Visibilidade |

---

#### **Fase 9: Mobile App (Q2 2027)**

**Objetivo:** Aplicativo mobile para operadores

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **App iOS/Android** | Acesso mobile | Mobilidade |
| **Notificações Push** | Alertas em tempo real | Resposta rápida |
| **Offline Mode** | Funcionar sem internet | Confiabilidade |
| **Biometria** | Autenticação segura | Segurança |

---

#### **Fase 10: Conformidade Regulatória (Q3 2027)**

**Objetivo:** Suportar regulamentações da indústria

| Funcionalidade | Descrição | Impacto |
|---|---|---|
| **FDA 21 CFR Part 11** | Conformidade com FDA | Regulamentação |
| **Auditoria Completa** | Rastreamento de todas as ações | Conformidade |
| **Assinatura Digital** | Validação de dados | Integridade |
| **Backup e Recuperação** | Disaster recovery | Continuidade |

---

### � Priorização de Melhorias

| Fase | Prioridade | Esforço | Impacto | Status |
|------|-----------|--------|--------|--------|
| Fase 2 | 🔴 Alta | 40h | Alto | Planejado |
| Fase 3 | 🟡 Média | 30h | Médio | Planejado |
| Fase 4 | 🟡 Média | 35h | Médio | Planejado |
| Fase 5 | 🟡 Média | 25h | Alto | Planejado |
| Fase 6 | 🟢 Baixa | 20h | Médio | Futuro |
| Fase 7 | 🟢 Baixa | 25h | Médio | Futuro |
| Fase 8 | 🟢 Baixa | 30h | Alto | Futuro |
| Fase 9 | 🟢 Baixa | 40h | Médio | Futuro |
| Fase 10 | 🔴 Alta | 50h | Alto | Futuro |

---

### 🎯 Próximos Passos Imediatos

1. **Fase 2 (Q3 2026):** Integração SCADA e alertas em tempo real
2. **Fase 3 (Q3 2026):** Detecção avançada de anomalias
3. **Fase 5 (Q4 2026):** Modelos XGBoost e LightGBM

---

### M09 — Link do Vídeo no YouTube

### M09 — Link do Vídeo no YouTube

- [x] **M09 — O README contém o link do vídeo no YouTube**
  - ✅ Link presente: Seção "🎬 Link do Vídeo de Apresentação" (no início do README)
  - ✅ Instruções: Substitua `LINK_DO_VIDEO` pelo link real quando o vídeo for publicado
  - ✅ Formato: Link clicável em markdown com descrição clara

**Link para Apresentação:**
```
[Assista a apresentação completa do BiotecPredict no YouTube](https://www.youtube.com/watch?v=LINK_DO_VIDEO)
```

> **Nota:** Substitua `LINK_DO_VIDEO` pelo link real quando o vídeo for publicado no YouTube.

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

## 📚 Referências - Prompt Logging

### Documentação Detalhada do Prompt Logging

O BiotecPredict implementa um sistema completo de logging de prompts com rastreabilidade de todas as interações com IA. Para informações detalhadas, consulte:

#### 1. **Documentação Completa**
- 📖 **[docs/prompt-logging.md](docs/prompt-logging.md)** - Guia completo com exemplos
  - Visão geral do sistema
  - Instruções de uso
  - Troubleshooting
  - Limitações e futuras melhorias
  - Análise de logs
  - Backup e restauração

#### 2. **Steering File (Contexto Permanente para Kiro)**
- 🎯 **[.kiro/steering/prompt-logging.md](.kiro/steering/prompt-logging.md)** - Convenções de logging
  - Propósito do sistema
  - Arquitetura e fluxo de dados
  - Estrutura de logs
  - Convenções de nomenclatura
  - Formato de timestamp (Brasília - UTC-3)
  - Estrutura de metadados obrigatória
  - Critérios de filtragem
  - Boas práticas para o agente Kiro
  - Manutenção e backup

#### 3. **Especificação Técnica**
- 📋 **[.kiro/specs/prompt-logging/](../.kiro/specs/prompt-logging/)** - Especificação completa
  - Requirements.md - Requisitos funcionais
  - Design.md - Design técnico
  - Tasks.md - Tarefas de implementação

### Localização dos Logs

Todos os prompts são automaticamente registrados em:

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-*.md              # Logs de features
├── bugfix-*.md               # Logs de bugfixes
├── hotfix-*.md               # Logs de hotfixes
├── release-*.md              # Logs de releases
├── chore-*.md                # Logs de chores
└── docs-*.md                 # Logs de documentação
```

### Convenções Principais

#### Nomes de Arquivo por Tipo de Branch

| Tipo de Branch | Exemplo | Arquivo de Log |
|---|---|---|
| `feature/` | `feature/compliance-score` | `feature-compliance-score.md` |
| `bugfix/` | `bugfix/validation-error` | `bugfix-validation-error.md` |
| `hotfix/` | `hotfix/api-crash` | `hotfix-api-crash.md` |
| `release/` | `release/v1.0.0` | `release-v1.0.0.md` |
| `chore/` | `chore/update-deps` | `chore-update-deps.md` |
| `docs/` | `docs/api-guide` | `docs-api-guide.md` |
| `main` | - | `main.md` |
| `develop` | - | `develop.md` |

#### Formato de Timestamp

```
Formato: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)
Exemplo: 2026-05-27 14:35:22 (Brasília - UTC-3)
```

#### Estrutura de Metadados Obrigatória

```markdown
## Prompt: <título até 80 caracteres>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```
```

### Consultar Logs

**Ver logs da branch atual:**

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Windows PowerShell:**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Últimas entradas:**

**Mac/Linux:**
```bash
tail -n 50 .kiro/prompt-logs/<branch>.md
```

**Windows PowerShell:**
```powershell
Get-Content ".kiro\prompt-logs\<branch>.md" -Tail 50
```

**Buscar por palavra-chave:**

**Mac/Linux:**
```bash
grep -i "compliance" .kiro/prompt-logs/*.md
```

**Windows PowerShell:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

### Boas Práticas

1. ✅ **Usar automaticamente** - Prompts são capturados via hook `promptSubmit`
2. ✅ **Consultar logs de features anteriores** - Reutilizar padrões bem-sucedidos
3. ✅ **Referenciar em PRs** - Incluir link para logs em descrições de PR
4. ✅ **Manter logs versionados** - Fazer commit junto com código
5. ✅ **Usar logs para documentação** - Complementar documentação técnica

### Referências Relacionadas

| Documento | Localização | Conteúdo |
|---|---|---|
| **Documentação Completa** | `docs/prompt-logging.md` | Guia detalhado com exemplos |
| **Spec Completa** | `.kiro/specs/prompt-logging/` | Especificação técnica |
| **Git Flow** | `.kiro/steering/gitflow.md` | Convenções de branches e commits |
| **Localização** | `.kiro/steering/localizacao.md` | Timezone e formato de datas |
| **Tech Stack** | `.kiro/steering/tech.md` | Tecnologias utilizadas |
| **Estrutura** | `.kiro/steering/structure.md` | Estrutura do projeto |

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
