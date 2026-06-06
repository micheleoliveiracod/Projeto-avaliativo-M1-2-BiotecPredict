# Prompts — Etapa 4: Geração de Testes com IA

Prompts utilizados para gerar a suíte de testes (unitários, integração, E2E) com suporte de IA.

---

## Prompt 4.1 — Testes unitários backend (pytest)

**Padrão aplicado:** Few-shot  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/testes-automatizados`  
**Data:** 2026-05-27

### Prompt original

```
Como engenheiro de QA especialista em pytest e FastAPI,
Quero que você gere testes unitários para os processors do BiotecPredict,
Para garantir que a lógica de validação e limpeza de dados está correta.

Módulos a testar:
- CSVProcessor.process() — deve retornar lista de dicts com colunas corretas
- DataValidator.validate_batch() — deve separar linhas válidas e inválidas
- DataCleaner.clean() — deve remover outliers e retornar warnings

Exemplo de estrutura esperada:
def test_csv_processor_valid_file():
    content = "temperature,ph,...\n36.5,7.2,..."
    result = CSVProcessor.process(content)
    assert len(result) == 1
    assert result[0]['temperature'] == 36.5

Cenários obrigatórios por módulo (mínimo 3 cada):
- happy path (dados válidos)
- edge case (valores nos limites)
- error case (dados inválidos/ausentes)

Restrições:
- Use pytest fixtures para dados de teste
- Sem mocks desnecessários (testar lógica real)
- Cada test function com nome descritivo
```

### Resultado obtido

Suite gerada em `backend/tests/pytest/unit/` cobrindo processors, models, schemas e services. Fixtures centralizadas em `conftest.py`.

### Ajuste aplicado

A IA gerou testes que dependiam de banco de dados para testar os processors — **corrigido**: processors testados com dados em memória, sem dependência de DB.

---

## Prompt 4.2 — Testes de integração (API endpoints)

**Padrão aplicado:** Role-based + Chain of Thought  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-28

### Prompt original

```
Como engenheiro de QA especialista em testes de API REST,
Quero que você gere testes de integração para os endpoints do BiotecPredict,
Para validar o fluxo completo de upload → compliance → predição.

Endpoints a testar:
- POST /api/v1/upload — deve aceitar CSV válido e retornar BatchResponse
- GET /api/v1/batches — deve listar batches com paginação
- GET /api/v1/compliance/{batch_id} — deve retornar score e classificação
- GET /api/v1/prediction/{batch_id} — deve retornar risk_level

Pense passo a passo:
1. Configure TestClient do FastAPI com banco de dados SQLite em memória
2. Para cada endpoint, teste: status code, estrutura do response, casos de erro (404, 400)
3. Garanta que os testes são independentes (cada um cria seus próprios dados)

Restrições:
- Use pytest-asyncio para endpoints async
- Banco de dados de teste separado do de desenvolvimento
- Fixtures para criar dados de teste reutilizáveis
```

### Resultado obtido

Testes de integração em `backend/tests/pytest/integration/` com TestClient configurado e banco SQLite em memória para isolamento.

---

## Prompt 4.3 — Testes E2E com Cypress

**Padrão aplicado:** Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/cypress-e2e-tests`  
**Data:** 2026-05-29

### Prompt original

```
Como engenheiro de QA especialista em Cypress e React,
Quero que você gere testes E2E para os dois cenários principais do BiotecPredict,
Para validar que o fluxo completo do usuário funciona no browser.

Cenário 1 — Upload de CSV:
1. Usuário acessa a página inicial
2. Clica em "Selecionar arquivo"
3. Seleciona um CSV válido
4. Clica em "Enviar"
5. Deve ver mensagem de sucesso e ser redirecionado ao Dashboard

Cenário 2 — Visualização do Dashboard:
1. Usuário acessa /dashboard
2. Deve ver a lista de batches processados
3. Deve ver KPIs de compliance e risco
4. Pode filtrar por data

Restrições:
- Use fixtures do Cypress para o arquivo CSV de teste
- Intercepte chamadas de API com cy.intercept()
- Testes independentes (sem dependência de ordem)
```

### Resultado obtido

Testes E2E em `frontend/cypress/e2e/` cobrindo upload e dashboard. Fixture `sample.csv` criada com dados representativos.
