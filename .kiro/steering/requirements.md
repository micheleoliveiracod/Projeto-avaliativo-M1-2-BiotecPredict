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
   - Persistência em PostgreSQL

3. **Persistência de Dados** ✅
   - Armazenamento de batches em PostgreSQL
   - Histórico completo de dados
   - Rastreabilidade de origem dos dados

---

### Cálculo de Compliance Score (2 requisitos)

4. **Manufacturing Compliance Score** ✅
   - Cálculo baseado em regras determinísticas
   - Score 0-100
   - Classificação: ACCEPTABLE (80-100), WARNING (60-79), CRITICAL (0-59)
   - Regras configuráveis por variável

5. **Validação de Especificações** ✅
   - Verificação de ranges esperados
   - Detecção de desvios
   - Relatório de conformidade

---

### Machine Learning e Predição (2 requisitos)

6. **Predição de Risco com ML** ✅
   - Modelo RandomForestClassifier treinado
   - Features: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed
   - Output: LOW RISK, MEDIUM RISK, HIGH RISK
   - Acurácia mínima: 80%

7. **Inferência em Tempo de Processamento** ✅
   - Predição automática ao processar batch
   - Latência < 1 segundo
   - Armazenamento de predições

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
    - GET /api/v1/batches - Listar todos os batches
    - GET /api/v1/batch/{id} - Detalhes do batch
    - GET /api/v1/prediction/{batch_id} - Predição de risco
    - GET /api/v1/compliance/{batch_id} - Score de conformidade

---

### Testes Automatizados (1 requisito)

12. **Testes Automatizados** ✅
    - Testes unitários com pytest (backend)
    - Testes unitários com Vitest (frontend)
    - Testes de integração com Postman (API)
    - Cobertura mínima: 70%

---

### Validação e Qualidade de Dados (2 requisitos - NOVO)

13. **Validação de Qualidade de Dados** ✅
    - Script `validate_data.py` para validação de ranges, outliers e qualidade
    - Verificação de ranges esperados
    - Detecção de anomalias e outliers
    - Análise de qualidade com perspectiva de cientista de dados
    - Relatórios detalhados de validação

14. **Rastreabilidade de Validações** ✅
    - Script `validate_compliance.py` para validação de compliance score
    - Versionamento de relatórios de validação
    - Histórico com data e hora de cada validação
    - Banco de dados para consultas históricas
    - Identificação de problemas com dados imputados

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
- ✅ Cobertura ≥ 70%
- ✅ Testes passam
- ✅ Sem warnings

**Validação de Dados**
- ✅ Scripts de validação funcionam
- ✅ Relatórios gerados corretamente
- ✅ Histórico de validações rastreável
- ✅ Problemas com dados identificados

---

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: 14 Requisitos Especificados
