# M07 — Caso Documentado de Saída Incorreta da IA

## Contexto

Durante o desenvolvimento do BiotecPredict, a IA (Claude Sonnet 4.6 via Claude Code) gerou código com erros lógicos significativos no módulo de compliance e no pipeline de ML. O caso está documentado no commit `f87c41e` ("fix: corrigir compliance score, treinamento ML e indicadores do frontend").

---

## Caso 1: Penalidade Dupla no Compliance Score

### Prompt original

```
Implemente o compliance score engine para calcular um score de 0-100 baseado nas leituras
dos sensores. Se um sensor estiver fora do range, aplique penalidade proporcional.
```

### O que a IA gerou (código incorreto)

```python
# compliance_service.py — versão com bug
def _calculate_sensor_score(self, value, min_val, max_val):
    if value < min_val or value > max_val:
        deviation = abs(value - min_val) / (max_val - min_val)
        penalty = deviation * 20  # penalidade aplicada aqui
        return max(0, 100 - penalty)
    return 100.0

def calculate_compliance_score(self, readings):
    scores = []
    for reading in readings:
        score = self._calculate_sensor_score(...)
        if score < 60:               # threshold WARNING errado
            score = score * 0.8      # penalidade DUPLA aplicada aqui
        scores.append(score)
    return sum(scores) / len(scores)
```

### Problema identificado

A IA aplicou penalidade **duas vezes** sobre o mesmo desvio:

1. Primeira penalidade em `_calculate_sensor_score` — redução proporcional ao desvio.
2. Segunda penalidade em `calculate_compliance_score` — multiplicação por 0.8 para scores abaixo de 60.

Resultado: batches com leituras levemente fora do range recebiam scores artificialmente baixos (ex: score real 72 → aparecia como 44 após a penalidade dupla), classificando como `CRITICAL` o que deveria ser `WARNING`.

O threshold de `60` para `WARNING` também estava errado — o correto para o domínio biofarmacêutico é `45`.

### Como o erro foi identificado

Ao testar manualmente com o CSV de exemplo (BATCH001, todos os sensores dentro do range), o compliance score retornado foi `38` em vez do esperado `85+`. A discrepância foi investigada adicionando logs intermediários, o que revelou a penalidade dupla.

### Correção aplicada

```python
# compliance_service.py — versão corrigida
def _calculate_sensor_score(self, value, min_val, max_val) -> float:
    if value < min_val or value > max_val:
        deviation = abs(value - min_val) / (max_val - min_val)
        penalty = deviation * 20
        return float(max(0, 100 - penalty))  # penalidade aplicada UMA vez
    return 100.0

def calculate_compliance_score(self, readings):
    scores = []
    for reading in readings:
        score = self._calculate_sensor_score(...)
        scores.append(score)   # sem penalidade adicional
    return sum(scores) / len(scores)
```

Threshold WARNING ajustado de `60` para `45`.

---

## Caso 2: Dados de Treino Desbalanceados no Modelo ML

### Prompt original

```
Treine um RandomForestClassifier com dados sintéticos para classificar risco como
LOW, MEDIUM ou HIGH com base nos sensores.
```

### O que a IA gerou (código incorreto)

```python
# model.py — versão com bug
def _generate_training_data(self):
    # Gerava apenas dados de LOW RISK (80%) e HIGH RISK (20%)
    # Nenhum dado de MEDIUM RISK
    low_risk_samples = self._generate_samples(n=800, risk="LOW")
    high_risk_samples = self._generate_samples(n=200, risk="HIGH")
    return low_risk_samples + high_risk_samples
```

Adicionalmente, os ranges de sensores estavam muito estreitos:
- Temperatura: apenas até 35°C (correto: até 45°C)
- pH: apenas até 8.0 (correto: até 9.5)

### Problema identificado

O modelo nunca previa `MEDIUM RISK` — sempre classificava como `LOW` ou `HIGH`. Para casos de risco médio (1–2 sensores levemente fora do range), o modelo retornava `HIGH RISK` com confiança de 0.51, indicando incerteza total.

Além disso, os ranges estreitos faziam com que leituras normais de temperatura acima de 35°C fossem classificadas erroneamente como `HIGH RISK`.

### Como o erro foi identificado

Ao testar o endpoint `/api/v1/predict` com batches de risco médio, todos retornavam `HIGH RISK`. A verificação da matriz de confusão mostrou que a classe `MEDIUM` tinha zero predições.

### Correção aplicada

```python
# model.py — versão corrigida
def _generate_training_data(self):
    # Proporções balanceadas: 50% LOW / 30% MEDIUM / 20% HIGH
    low_risk = self._generate_samples(n=500, out_of_range=0)
    medium_risk = self._generate_samples(n=300, out_of_range_count=(1, 2))
    high_risk = self._generate_samples(n=200, out_of_range_count=(3, 5))
    return low_risk + medium_risk + high_risk
```

Ranges estendidos: temperatura até 45°C, pH até 9.5, pressão e agitador com margens maiores.

---

## Caso 3: Ranges Errados nos Indicadores Visuais do Frontend

### Prompt original

```
Implemente indicadores visuais no Dashboard que fiquem vermelhos quando os sensores
estiverem fora do range aceitável.
```

### O que a IA gerou (código incorreto)

```typescript
// Dashboard.tsx — versão com bug
const SENSOR_RANGES = {
  temperature: { min: 15, max: 40 },   // range muito amplo
  ph: { min: 6.0, max: 8.5 },          // range incorreto
  dissolved_oxygen: { min: 60, max: 100 },
  pressure: { min: 3.0, max: 8.0 },    // range muito amplo
  agitator_speed: { min: 150, max: 400 }, // range muito amplo
};
```

### Problema identificado

Os ranges do frontend não correspondiam aos ranges de cálculo do backend, criando inconsistência visual: um sensor mostrava verde no dashboard mas contribuía para penalidade no score. Isso confundia o operador sobre o real estado do processo.

### Correção aplicada

```typescript
// Dashboard.tsx — versão corrigida (alinhada ao backend)
const SENSOR_RANGES = {
  temperature: { min: 20, max: 30 },
  ph: { min: 6.5, max: 7.5 },
  dissolved_oxygen: { min: 70, max: 100 },
  pressure: { min: 4.5, max: 6.0 },
  agitator_speed: { min: 200, max: 300 },
};
```

---

## Lições Aprendidas

| # | Lição | Como Aplicar |
|---|-------|-------------|
| 1 | **Testar com valores conhecidos imediatamente** | Após gerar qualquer lógica de cálculo, testar com entrada cujo resultado é previsível antes de avançar |
| 2 | **Revisar lógica de penalidades com atenção** | A IA tende a adicionar penalidades redundantes em múltiplos pontos do código |
| 3 | **Verificar consistência entre camadas** | Ranges e thresholds definidos no backend devem ser explicitamente passados como contexto ao gerar código de frontend |
| 4 | **Dados de treino exigem revisão humana** | A IA não conhece o domínio — proporções e ranges do dataset de treino devem ser validados por quem conhece o processo industrial |
| 5 | **Prompt com contexto de domínio reduz erros** | Ao informar os ranges reais de sensores biofarmacêuticos, a qualidade do código gerado melhorou significativamente |

---

**Arquivos afetados pelo fix:**
- [backend/services/compliance_service.py](../backend/services/compliance_service.py)
- [backend/ml/model.py](../backend/ml/model.py)
- [frontend/src/components/Dashboard/Dashboard.tsx](../frontend/src/components/Dashboard/Dashboard.tsx)

**Commit de correção:** `f87c41e` — fix: corrigir compliance score, treinamento ML e indicadores do frontend
