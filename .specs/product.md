# Produto: BiotecPredict - Plataforma de Manufatura Preditiva

## Visão do Produto

Plataforma SaaS end-to-end que monitora processos de manufatura biofarmacêutica utilizando dados industriais de sensores e machine learning. O sistema calcula um Manufacturing Compliance Score baseado em regras determinísticas e prevê riscos de desvios de processo, auxiliando operadores na tomada de decisão.

> ⚠️ O produto **não substitui a supervisão humana**. As análises são informativas e baseadas em dados históricos. A decisão final sobre ações corretivas é sempre do operador.

---

## Problema

Operadores de manufatura biofarmacêutica enfrentam:

- Dificuldade em monitorar múltiplas variáveis de processo simultaneamente
- Falta de alertas automáticos para desvios de especificação
- Análise manual demorada de dados de sensores
- Impossibilidade de prever falhas antes que ocorram
- Falta de rastreabilidade completa de decisões

---

## Solução

Uma plataforma que:

- Consolida dados de múltiplos sensores industriais
- Aplica regras determinísticas para cálculo de compliance score
- Utiliza machine learning para predição de risco
- Gera alertas automáticos para desvios
- Fornece dashboard intuitivo com visualizações
- Mantém histórico completo para auditoria

---

## Público-Alvo

- Operadores de manufatura biofarmacêutica
- Supervisores de qualidade
- Engenheiros de processo
- Cientistas de dados em indústria farmacêutica

---

## Objetivos

- Monitorar processos de manufatura em tempo real
- Detectar desvios de especificação automaticamente
- Prever riscos de falha de processo
- Reduzir tempo de análise de dados
- Melhorar rastreabilidade e conformidade regulatória

---

## Escopo Inicial (MVP)

**Dentro do escopo:**
- Upload de dados CSV com variáveis de processo
- Processamento em lote de batches industriais
- Cálculo de Manufacturing Compliance Score (0-100)
- Predição de risco com RandomForestClassifier
- Dashboard com visualizações de KPIs
- API REST para integração
- Histórico completo de batches e predições
- Scripts de validação de qualidade de dados
- Relatórios versionados com rastreabilidade

**Fora do escopo (por ora):**
- Dados em tempo real (apenas batch)
- Integração com sistemas SCADA
- Alertas por email/SMS
- Análise de anomalias avançada
- Modelos de forecasting temporal

---

## Variáveis Monitoradas

| Variável | Unidade | Descrição |
|---|---|---|
| **Temperature** | °C | Temperatura do biorreator |
| **pH** | - | Potencial hidrogeniônico |
| **Dissolved Oxygen** | % | Oxigênio dissolvido |
| **Pressure** | bar | Pressão do sistema |
| **Agitator Speed** | RPM | Velocidade do agitador |

---

## Manufacturing Compliance Score

O score é calculado com base em regras determinísticas que avaliam cada variável contra especificações esperadas.

| Score | Classificação | Ação |
|---|---|---|
| 80 – 100 | ACCEPTABLE | Processo conforme |
| 45 – 79 | WARNING | Atenção necessária |
| 0 – 44 | CRITICAL | Intervenção imediata |

---

## Predição de Risco (ML)

Modelo RandomForestClassifier treinado com dados históricos para prever risco de desvio de processo.

| Predição | Significado |
|---|---|
| **LOW RISK** | Processo dentro dos parâmetros esperados |
| **MEDIUM RISK** | Desvios moderados detectados |
| **HIGH RISK** | Risco significativo de falha de processo |

---

## Validação e Qualidade de Dados

Sistema inclui scripts de validação para garantir qualidade dos dados e precisão dos cálculos:

- **validate_data.py** - Validação de qualidade dos dados imputados (ranges, outliers, anomalias)
- **validate_compliance.py** - Validação de cálculos de compliance score

Todos os relatórios são versionados em `backend/reports/` com rastreabilidade completa.

---

## Saída Esperada por Batch

Para cada batch processado, o sistema retorna:

- ID do batch e data de upload
- Dados de sensores processados
- Manufacturing Compliance Score (0-100) com classificação
- Predição de risco (LOW/MEDIUM/HIGH) com confiança
- Histórico completo para auditoria
- Relatório de validação de qualidade

---

## Fonte de Dados

**Dataset:** [Big Data – Biopharmaceutical Manufacturing (Kaggle)](https://www.kaggle.com/datasets/stephengoldie/big-databiopharmaceutical-manufacturing)

- Variáveis industriais de processo
- Dados de sensores de biorreatores
- Dados de batches industriais
- Falhas de processo históricos
- Informações temporais (time-series)

---

## Evoluções Futuras (Fora do MVP)

- Integração com sistemas SCADA em tempo real
- Detecção de anomalias com Isolation Forest
- Forecasting temporal com ARIMA/Prophet
- Modelos avançados (XGBoost, Neural Networks)
- Alertas automáticos por email/SMS
- Análise de causa raiz de falhas
- Otimização de parâmetros de processo

---

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ Produto Definido
