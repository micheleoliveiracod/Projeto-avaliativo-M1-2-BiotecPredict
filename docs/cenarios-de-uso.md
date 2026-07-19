# Cenários de Uso — BiotecPredict

Demonstração de 2 cenários end-to-end da plataforma, cobrindo o fluxo completo: upload de CSV → compliance score → predição de risco.

**Pré-requisito:** backend rodando em `http://localhost:8001`

```bash
# Iniciar o backend
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## Cenário 1 — Processo dentro do padrão (Golden Path)

> **Contexto de negócio:** A equipe de manufatura conclui um batch de biofármaco com todas as variáveis de processo dentro dos ranges ideais. A plataforma confirma conformidade e classifica o risco como baixo.

**Arquivo de entrada:** `backend/tests/fixtures/csv/control/valid_ideal.csv`

```csv
temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,85.0,5.0,260
25.2,7.1,87.0,5.1,255
24.8,6.9,86.0,4.9,258
25.5,7.2,88.0,5.2,262
24.6,7.0,84.0,5.0,250
25.1,7.1,85.5,5.1,265
24.9,7.0,86.5,4.8,252
25.3,6.8,87.5,5.3,270
25.0,7.2,85.0,5.2,260
24.7,7.0,86.0,5.0,255
```

---

### Passo 1 — Upload do CSV

**Request:**

```bash
curl -X POST http://localhost:8001/api/v1/upload \
  -F "file=@backend/tests/fixtures/csv/control/valid_ideal.csv"
```

**Response esperada (HTTP 200):**

```json
{
  "id": 1,
  "upload_date": "2026-06-05T14:32:10.245Z",
  "status": "COMPLETED",
  "compliance_score": 98.65,
  "risk_prediction": "LOW_RISK"
}
```

> O batch é criado, processado e analisado em uma única chamada. `status: COMPLETED` confirma que o pipeline ETL finalizou com sucesso.

---

### Passo 2 — Consultar o Compliance Score

**Request:**

```bash
curl http://localhost:8001/api/v1/compliance/1
```

**Response esperada (HTTP 200):**

```json
{
  "batch_id": 1,
  "compliance_score": 98.65,
  "classification": "ACCEPTABLE",
  "sensor_metrics": {
    "temperature": {
      "average": 25.01,
      "min": 24.6,
      "max": 25.5,
      "ideal_min": 24.0,
      "ideal_max": 26.0,
      "acceptable_min": 20.0,
      "acceptable_max": 30.0,
      "count": 10
    },
    "ph": {
      "average": 7.03,
      "min": 6.8,
      "max": 7.2,
      "ideal_min": 6.8,
      "ideal_max": 7.2,
      "acceptable_min": 6.5,
      "acceptable_max": 7.5,
      "count": 10
    },
    "dissolved_oxygen": {
      "average": 86.05,
      "min": 84.0,
      "max": 88.0,
      "ideal_min": 80.0,
      "ideal_max": 95.0,
      "acceptable_min": 70.0,
      "acceptable_max": 100.0,
      "count": 10
    },
    "pressure": {
      "average": 5.06,
      "min": 4.8,
      "max": 5.3,
      "ideal_min": 4.8,
      "ideal_max": 5.5,
      "acceptable_min": 4.5,
      "acceptable_max": 6.0,
      "count": 10
    },
    "agitator_speed": {
      "average": 258.7,
      "min": 250.0,
      "max": 270.0,
      "ideal_min": 240.0,
      "ideal_max": 280.0,
      "acceptable_min": 200.0,
      "acceptable_max": 300.0,
      "count": 10
    }
  }
}
```

> **Interpretação:** Score 98.65/100 — todas as 5 variáveis dentro dos ranges ideais. Classificação ACCEPTABLE indica que o batch atende plenamente as especificações de qualidade.

---

### Passo 3 — Consultar a Predição de Risco

**Request:**

```bash
curl http://localhost:8001/api/v1/prediction/1
```

**Response esperada (HTTP 200):**

```json
{
  "batch_id": 1,
  "risk_prediction": "LOW_RISK",
  "confidence_score": 0.87,
  "interpretation": "Processo estável com variáveis dentro dos parâmetros ideais. Risco de falha mínimo.",
  "recommendations": [
    "Manter parâmetros atuais de temperatura (24–26°C)",
    "Continuar monitoramento padrão de pH e oxigênio dissolvido",
    "Nenhuma intervenção imediata necessária"
  ]
}
```

> **Interpretação:** O modelo RandomForest classificou o batch como LOW_RISK com 87% de confiança. Nenhuma intervenção é necessária — o processo pode continuar normalmente.

---

### Resultado do Cenário 1

| Variável | Valor médio | Range ideal | Status |
|---|---|---|---|
| Temperatura | 25.01°C | 24–26°C | ✅ Ideal |
| pH | 7.03 | 6.8–7.2 | ✅ Ideal |
| Oxigênio dissolvido | 86.05% | 80–95% | ✅ Ideal |
| Pressão | 5.06 bar | 4.8–5.5 bar | ✅ Ideal |
| Velocidade do agitador | 258.7 RPM | 240–280 RPM | ✅ Ideal |
| **Compliance Score** | **98.65/100** | ≥ 80 = ACCEPTABLE | ✅ ACCEPTABLE |
| **Predição de Risco** | **LOW_RISK** | — | ✅ Aprovado |

---

## Cenário 2 — Processo fora do padrão (Falha Crítica)

> **Contexto de negócio:** Sensores detectam desvios severos em todas as variáveis de processo. A temperatura subiu acima do limite aceitável, o pH está fora de controle e o oxigênio dissolvido caiu abaixo do mínimo. A plataforma identifica o batch como crítico e recomenda intervenção imediata.

**Arquivo de entrada:** `backend/tests/fixtures/csv/bugs/critical_zone.csv`

```csv
temperature,ph,dissolved_oxygen,pressure,agitator_speed
32.0,7.6,65.0,6.2,310
33.0,7.7,63.0,6.5,315
32.5,7.8,64.0,6.3,312
31.5,7.6,62.0,6.4,320
32.0,7.9,65.0,6.2,310
```

---

### Passo 1 — Upload do CSV

**Request:**

```bash
curl -X POST http://localhost:8001/api/v1/upload \
  -F "file=@backend/tests/fixtures/csv/bugs/critical_zone.csv"
```

**Response esperada (HTTP 200):**

```json
{
  "id": 2,
  "upload_date": "2026-06-05T14:35:22.891Z",
  "status": "COMPLETED",
  "compliance_score": 0.0,
  "risk_prediction": "HIGH_RISK"
}
```

> O batch foi processado, mas `compliance_score: 0.0` e `risk_prediction: HIGH_RISK` sinalizam falha crítica imediata.

---

### Passo 2 — Consultar o Compliance Score

**Request:**

```bash
curl http://localhost:8001/api/v1/compliance/2
```

**Response esperada (HTTP 200):**

```json
{
  "batch_id": 2,
  "compliance_score": 0.0,
  "classification": "CRITICAL",
  "sensor_metrics": {
    "temperature": {
      "average": 32.2,
      "min": 31.5,
      "max": 33.0,
      "ideal_min": 24.0,
      "ideal_max": 26.0,
      "acceptable_min": 20.0,
      "acceptable_max": 30.0,
      "count": 5
    },
    "ph": {
      "average": 7.72,
      "min": 7.6,
      "max": 7.9,
      "ideal_min": 6.8,
      "ideal_max": 7.2,
      "acceptable_min": 6.5,
      "acceptable_max": 7.5,
      "count": 5
    },
    "dissolved_oxygen": {
      "average": 63.8,
      "min": 62.0,
      "max": 65.0,
      "ideal_min": 80.0,
      "ideal_max": 95.0,
      "acceptable_min": 70.0,
      "acceptable_max": 100.0,
      "count": 5
    },
    "pressure": {
      "average": 6.32,
      "min": 6.2,
      "max": 6.5,
      "ideal_min": 4.8,
      "ideal_max": 5.5,
      "acceptable_min": 4.5,
      "acceptable_max": 6.0,
      "count": 5
    },
    "agitator_speed": {
      "average": 313.4,
      "min": 310.0,
      "max": 320.0,
      "ideal_min": 240.0,
      "ideal_max": 280.0,
      "acceptable_min": 200.0,
      "acceptable_max": 300.0,
      "count": 5
    }
  }
}
```

> **Interpretação:** Score 0.0/100 — todas as 5 variáveis fora dos limites aceitáveis. Classificação CRITICAL indica violação grave das especificações de processo. O batch deve ser descartado e o processo interrompido para investigação.

---

### Passo 3 — Consultar a Predição de Risco

**Request:**

```bash
curl http://localhost:8001/api/v1/prediction/2
```

**Response esperada (HTTP 200):**

```json
{
  "batch_id": 2,
  "risk_prediction": "HIGH_RISK",
  "confidence_score": 0.93,
  "interpretation": "Processo com desvios críticos em múltiplas variáveis. Alta probabilidade de falha de produto.",
  "recommendations": [
    "Interromper o processo imediatamente",
    "Investigar sistema de controle de temperatura (leituras: 31.5–33.0°C, limite: 30°C)",
    "Verificar sistema de aeração — oxigênio dissolvido abaixo do mínimo (63.8%, limite: 70%)",
    "Realizar manutenção preventiva antes de reiniciar o batch",
    "Acionar equipe de qualidade para avaliação do material produzido"
  ]
}
```

> **Interpretação:** O modelo classifica este batch como HIGH_RISK com 93% de confiança. A intervenção imediata é necessária — o produto deste batch não pode ser aprovado sem investigação completa.

---

### Resultado do Cenário 2

| Variável | Valor médio | Limite aceitável | Desvio | Status |
|---|---|---|---|---|
| Temperatura | 32.2°C | máx. 30°C | +2.2°C | ❌ Crítico |
| pH | 7.72 | máx. 7.5 | +0.22 | ❌ Crítico |
| Oxigênio dissolvido | 63.8% | mín. 70% | -6.2% | ❌ Crítico |
| Pressão | 6.32 bar | máx. 6.0 bar | +0.32 bar | ❌ Crítico |
| Velocidade do agitador | 313.4 RPM | máx. 300 RPM | +13.4 RPM | ❌ Crítico |
| **Compliance Score** | **0.0/100** | ≥ 80 = ACCEPTABLE | — | ❌ CRITICAL |
| **Predição de Risco** | **HIGH_RISK** | — | — | ❌ Reprovado |

---

## Cenário 3 — Processo em desvio parcial (Médio Risco)

> **Contexto de negócio:** Temperatura e pH saem progressivamente da faixa aceitável durante o batch. A plataforma identifica o processo como MEDIUM_RISK e emite alerta — intervenção corretiva pode evitar a perda do produto.

**Arquivo de entrada:** `backend/tests/fixtures/csv/control/batch_sensor_medium_risk.csv`

```csv
temperature,ph,dissolved_oxygen,pressure,agitator_speed
27.9,7.24,83.5,5.1,262
29.4,7.56,81.2,5.0,258
31.2,7.89,80.1,5.2,265
33.1,8.19,79.8,5.1,260
35.0,8.05,78.5,5.3,270
```

> Temperatura sobe progressivamente de 27.9°C (aceitável) até 35°C (fora da faixa). pH passa de 7.24 para 8.19 (limite: 7.5). Os demais sensores permanecem dentro dos limites aceitáveis.

---

### Passo 1 — Upload do CSV

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@backend/tests/fixtures/csv/control/batch_sensor_medium_risk.csv"
```

**Response esperada (HTTP 200):**

```json
{
  "id": 3,
  "upload_date": "2026-06-07T10:15:00.000Z",
  "status": "COMPLETED",
  "compliance_score": 57.6,
  "risk_prediction": "MEDIUM_RISK"
}
```

> `compliance_score: 57.6` → classificação WARNING (faixa 45–79). `risk_prediction: MEDIUM_RISK` — 2 sensores fora da faixa aceitável (temperatura e pH).

---

### Passo 2 — Consultar o Compliance Score

**Request:**

```bash
curl http://localhost:8000/api/v1/compliance/3
```

**Response esperada (HTTP 200):**

```json
{
  "batch_id": 3,
  "compliance_score": 57.6,
  "classification": "WARNING",
  "sensor_metrics": {
    "temperature": {
      "average": 31.32,
      "min": 27.9,
      "max": 35.0,
      "acceptable_min": 20.0,
      "acceptable_max": 30.0
    },
    "ph": {
      "average": 7.79,
      "min": 7.24,
      "max": 8.19,
      "acceptable_min": 6.5,
      "acceptable_max": 7.5
    },
    "dissolved_oxygen": { "average": 80.62, "acceptable_min": 70.0, "acceptable_max": 100.0 },
    "pressure": { "average": 5.14, "acceptable_min": 4.5, "acceptable_max": 6.0 },
    "agitator_speed": { "average": 263.0, "acceptable_min": 200.0, "acceptable_max": 300.0 }
  }
}
```

> **Interpretação:** Score 57.6/100 → WARNING. Temperatura e pH fora da faixa aceitável em parte do batch. Os outros 3 sensores estão normais. O batch está em zona de risco — intervenção corretiva é recomendada antes que os desvios piorem.

---

### Passo 3 — Consultar a Predição de Risco

**Request:**

```bash
curl http://localhost:8000/api/v1/prediction/3
```

**Response esperada (HTTP 200):**

```json
{
  "batch_id": 3,
  "risk_prediction": "MEDIUM_RISK",
  "confidence_score": 0.807,
  "interpretation": "Processo com desvios em variáveis críticas. Risco moderado de falha do produto."
}
```

> **Interpretação:** O modelo classifica como MEDIUM_RISK com 80.7% de confiança — alta certeza da classificação. Lembrar: `confidence_score` mede a certeza do modelo sobre a classe prevista, não a saúde do processo.

---

### Resultado do Cenário 3

| Variável | Valor médio | Limite aceitável | Status |
|---|---|---|---|
| Temperatura | 31.32°C | 20–30°C | ⚠️ Fora da faixa |
| pH | 7.79 | 6.5–7.5 | ⚠️ Fora da faixa |
| Oxigênio dissolvido | 80.62% | 70–100% | ✅ OK |
| Pressão | 5.14 bar | 4.5–6.0 bar | ✅ OK |
| Velocidade do agitador | 263 RPM | 200–300 RPM | ✅ OK |
| **Compliance Score** | **57.6/100** | ≥80 = ACCEPTABLE; ≥45 = WARNING | ⚠️ WARNING |
| **Predição de Risco** | **MEDIUM_RISK** | — | ⚠️ Intervenção recomendada |

---

## Comparativo dos Cenários

| Aspecto | Cenário 1 (Baixo Risco) | Cenário 3 (Médio Risco) | Cenário 2 (Alto Risco) |
|---|---|---|---|
| **Arquivo CSV** | `valid_ideal.csv` | `batch_sensor_medium_risk.csv` | `batch_sensor_high_risk.csv` |
| **Sensores fora da faixa** | 0 | 2 (temp + pH) | 5 (todos) |
| **Compliance Score** | 98.65/100 | 57.6/100 | ~0/100 |
| **Classificação** | ACCEPTABLE | WARNING | CRITICAL |
| **Predição ML** | LOW_RISK (97.5%) | MEDIUM_RISK (80.7%) | HIGH_RISK (84.1%) |
| **Ação recomendada** | Continuar normalmente | Intervir corretivamente | Interromper imediatamente |

> **Nota sobre confiança do modelo:** A confiança (%) indica a certeza do modelo, não a gravidade do problema. HIGH_RISK ter 84.1% (menor que LOW_RISK com 97.5%) reflete maior variabilidade nos padrões de risco alto — veja `docs/analise-resultados.md` seção 7.

---

## Como Executar com Postman

1. Importe `docs/postman/BiotecPredict.postman_collection.json` no Postman
2. Defina a variável `base_url` como `http://localhost:8000` (Docker) ou `http://localhost:8001` (uvicorn direto)
3. Execute os requests na seguinte ordem:
   - **Upload CSV Válido** → selecione `valid_ideal.csv` → batch_id salvo automaticamente
   - **GET Compliance Score** → usa batch_id da variável
   - **GET Predição de Risco** → usa batch_id da variável
4. Repita com `batch_sensor_medium_risk.csv` (Cenário 3) e `batch_sensor_high_risk.csv` (Cenário 2)

---

## Como Executar com pytest

```bash
# A partir da raiz do projeto
pytest backend/tests/pytest/integration/test_api_integration.py -v -k "e2e"
```

Os testes `TestEndToEndFlow` cobrem os cenários de baixo e alto risco automaticamente.

---

## Cenário Bônus — Upload inválido (Rejeição)

> **Contexto:** O usuário tenta enviar um arquivo com dados fora dos ranges físicos possíveis — a plataforma rejeita antes de persistir.

```bash
curl -X POST http://localhost:8001/api/v1/upload \
  -F "file=@backend/tests/fixtures/csv/rejected/invalid_out_of_range.csv"
```

**Response (HTTP 400):**

```json
{
  "detail": "Arquivo CSV inválido: valores fora do range aceitável detectados"
}
```

> **Interpretação:** O pipeline ETL bloqueia dados inconsistentes na etapa de validação — nenhum dado inválido chega ao banco de dados.

---

**Data:** Junho de 2026  
**Arquivo de referência:** `backend/tests/fixtures/csv/README.md`  
**Coleção Postman:** `docs/postman/BiotecPredict.postman_collection.json`
