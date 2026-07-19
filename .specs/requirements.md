# Requisitos - BiotecPredict

## 📋 Resumo Executivo

Este documento especifica os requisitos funcionais e não-funcionais para a Plataforma de Manufatura Preditiva BiotecPredict.

---

## 🎯 Requisitos Funcionais

### Upload e Processamento de Dados (3 requisitos)

1. **Upload de Arquivo CSV** ✅
   - Usuários podem fazer upload de arquivos CSV com dados de batches
   - Validação de formato e estrutura
   - Feedback de erro em caso de arquivo inválido
   - Suporte a múltiplos uploads simultâneos

2. **Processamento de Batch** ✅
   - Backend processa dados do CSV
   - Validação de ranges de valores
   - Limpeza de dados (nulos, outliers)
   - Persistência em SQLite

3. **Persistência de Dados** ✅
   - Armazenamento de batches em SQLite
   - Histórico completo de dados
   - Rastreabilidade de origem dos dados

---

### Cálculo de Compliance Score (2 requisitos)

4. **Manufacturing Compliance Score** ✅
   - Cálculo baseado em regras determinísticas
   - Score 0-100
   - Classificação: ACCEPTABLE (≥80), WARNING (45–79), CRITICAL (<45)
   - Regras configuráveis por variável
   - Nota: threshold de WARNING ajustado de 60 para 45 após correção de penalidade dupla no cálculo original (ver `docs/prompts/03-refatoracao.md` — Refatoração 3)

5. **Validação de Especificações** ✅
   - Verificação de ranges esperados
   - Detecção de desvios
   - Relatório de conformidade

---

### Machine Learning e Predição (2 requisitos)

6. **Predição de Risco com ML** ✅
   - Modelo RandomForestClassifier treinado com dados sintéticos
   - Features: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed (médias do batch)
   - Output: LOW_RISK (0 params fora da faixa aceitável), MEDIUM_RISK (1-2), HIGH_RISK (3+)
   - Fronteira de classificação alinhada com as faixas aceitáveis do ComplianceService

7. **Inferência em Tempo de Processamento** ✅
   - Predição automática ao processar batch (dentro do BatchService)
   - Latência < 1 segundo
   - Resultado persistido no campo `risk_prediction` da tabela `batch`

---

### Dashboard e Visualização (2 requisitos)

8. **Dashboard Analítico** ✅
   - Visualização de KPIs de qualidade
   - Gráficos de variáveis de sensores
   - Exibição de compliance score
   - Exibição de predição de risco

9. **Tabela de Batches** ✅
   - Listagem de todos os batches processados
   - Filtros por data, status, score
   - Detalhes do batch ao clicar
   - Histórico de processamento

---

### API REST (2 requisitos)

10. **Endpoints de Upload** ✅
    - POST /api/v1/upload - Upload de arquivo CSV
    - Validação de arquivo
    - Retorno de ID do batch

11. **Endpoints de Consulta** ✅
    - GET /api/v1/batches - Listar todos os batches (retorna `List[BatchResponse]`)
    - GET /api/v1/batch/{id} - Detalhes do batch (id é INTEGER)
    - GET /api/v1/batch/{id}/sensors - Leituras de sensores do batch
    - GET /api/v1/compliance/{batch_id} - Score de conformidade (0-100 + classification)
    - GET /api/v1/prediction/{batch_id} - Predição de risco (risk_prediction + confidence_score)
    - POST /api/v1/predict - Predição direta de risco sem batch
    - GET /api/v1/model/info - Informações do modelo RandomForest
    - GET /health - Health check da API

---

### Testes Automatizados (1 requisito)

12. **Testes Automatizados** ✅
    - **63 testes de integração** com pytest (`test_api_integration.py`) — todos passando
    - Testes cobrem: Health (3), Upload (12), Batches (7), Compliance (11), Prediction (9), ML (4), E2E Flow (3)
    - Fixtures CSV compartilhadas em `backend/tests/fixtures/csv/`, organizadas por propósito: `control/` (comportamento correto), `bugs/` (reproduz divergências conhecidas entre Compliance e ML), `rejected/` (HTTP 400 esperado), `performance/` (teste de carga) — ver `tests/fixtures/csv/README.md`
    - Testes unitários com pytest — `unit/`, `repositories/`, `database/`, `health/`
    - Coleção Postman em `docs/postman/BiotecPredict.postman_collection.json` (testes automatizados em cada request)
    - Testes unitários frontend com Vitest
    - Cobertura mínima: 70%

---

### CSVProcessor com Mapeamento de Colunas (1 requisito)

13. **Flexibilidade de Formato CSV** ✅
    - `CSVProcessor` aceita variações de nomes de coluna (maiúsculas, espaços, underscores, aliases)
    - Mapeamento automático: `"Dissolved Oxygen"` → `dissolved_oxygen`, `"Agitator Speed"` → `agitator_speed`, etc.
    - Erro claro com lista de colunas encontradas quando o mapeamento falha

---

## 📋 Requisitos Não-Funcionais

### Performance (3 requisitos)

13. **Tempo de Resposta** ✅
    - Upload e processamento: < 5 segundos
    - Consulta de batch: < 500ms
    - Predição: < 1 segundo
    - Dashboard: < 2 segundos

14. **Escalabilidade** ✅
    - Suporte a 100 usuários simultâneos (MVP)
    - Suporte a 1000+ batches no banco
    - Database escalável horizontalmente
    - API stateless

15. **Disponibilidade** ✅
    - Uptime: 99% (máximo 7.2h downtime/mês)
    - Backup automático diário
    - Recuperação de falhas

---

### Segurança (3 requisitos)

16. **Criptografia de Dados** ✅
    - HTTPS em produção
    - Senhas com bcrypt
    - Dados sensíveis criptografados

17. **Validação de Entrada** ✅
    - Validação rigorosa de tipos
    - Proteção contra SQL Injection
    - Sanitização de entrada

18. **Controle de Acesso** ✅
    - Autenticação básica (MVP)
    - Rate limiting (100 req/min por IP)
    - Logs de acesso

---

### Manutenibilidade (2 requisitos)

19. **Clean Architecture** ✅
    - Separação de responsabilidades
    - Modularidade
    - Código testável

20. **Documentação** ✅
    - Docstrings em todas as funções
    - README completo
    - API documentada (Swagger)
    - Guias de desenvolvimento

---

## ✅ Critérios de Aceitação

### Por Área

**Upload e Processamento**
- ✅ Upload de CSV funciona
- ✅ Validação de dados funciona
- ✅ Dados persistem no banco

**Compliance Score**
- ✅ Score calculado corretamente
- ✅ Classificação correta (ACCEPTABLE/WARNING/CRITICAL)
- ✅ Regras aplicadas corretamente

**Machine Learning**
- ✅ Modelo treinado com acurácia ≥ 80%
- ✅ Predição funciona em tempo real
- ✅ Features corretas utilizadas

**Dashboard**
- ✅ Visualização de KPIs
- ✅ Gráficos renderizam corretamente
- ✅ Filtros funcionam

**API**
- ✅ Todos os endpoints funcionam
- ✅ Respostas em JSON válido
- ✅ Tratamento de erros correto

**Testes**
- ✅ 63 testes de integração passando (pytest)
- ✅ Cobertura ≥ 70%
- ✅ Coleção Postman com testes para todos os endpoints
- ✅ Fixtures CSV cobrindo casos válidos, warning, critical e inválidos

**CSVProcessor**
- ✅ Aceita variações de nomes de coluna
- ✅ Erro claro quando colunas obrigatórias não são encontradas

---

**Versão**: 0.3.0  
**Data**: Junho de 2026  
**Status**: 13 Requisitos Especificados — Implementados e Testados
