# Prompts — Etapa 3: Refatoração com Suporte de IA

Refatoração documentada com critério técnico, prompt utilizado, estado anterior e resultado obtido.

> **Metodologia de trabalho:** Em todas as refatorações desta etapa, a análise crítica do comportamento do sistema e a identificação do problema foram realizadas pela autora do projeto, **Michele Oliveira**. A IA (Claude Code / Kiro) foi utilizada como ferramenta de apoio para localizar a origem exata do bug no código, propor e aplicar a correção, e executar os testes de validação. O julgamento sobre o que estava errado, por que estava errado e qual o impacto no usuário partiu sempre da análise humana.

---

## Refatoração 1 — Aplicação do Princípio Open/Closed no BatchService

**Critério técnico:** SOLID — Open/Closed Principle  
**Padrão de prompt:** Role-based + Chain of Thought  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/refatoracao-ia`  
**Data:** 2026-05-27

### Análise crítica — Michele Oliveira

Durante a revisão do código de compliance, a autora identificou que toda a lógica de validação de sensores estava concentrada em um único método `calculate_compliance` da classe `BatchService`. Ao tentar adicionar uma nova regra de processo (limite de pressão diferente para um novo tipo de biorreator), percebeu que qualquer mudança exigia modificar diretamente a classe existente — tornando o código frágil, difícil de testar e impossível de estender sem risco de regressão.

O problema identificado: **violação do princípio Open/Closed** — o código estava aberto para modificação quando deveria estar fechado para modificação e aberto para extensão. A solução arquitetural esperada era separar cada regra em sua própria classe, com uma abstração comum que o service pudesse aplicar sem conhecer os detalhes de cada regra.

A IA foi acionada com o problema e o objetivo já definidos pela autora.

---

### Código ANTES da refatoração

```python
# batch_service.py — versão original (violação OCP)
class BatchService:
    @staticmethod
    def calculate_compliance(rows):
        score = 100.0
        for row in rows:
            # lógica de temperatura
            if row['temperature'] < 30 or row['temperature'] > 40:
                score -= 10
            # lógica de pH
            if row['ph'] < 6.8 or row['ph'] > 7.4:
                score -= 10
            # lógica de O2
            if row['dissolved_oxygen'] < 80:
                score -= 15
            # lógica de pressão
            if row['pressure'] < 0.8 or row['pressure'] > 1.2:
                score -= 10
            # lógica de agitação
            if row['agitator_speed'] < 200 or row['agitator_speed'] > 300:
                score -= 5
        return max(0.0, score)
```

**Problema:** Para adicionar uma nova regra de compliance era necessário modificar o `BatchService` — violação do Open/Closed Principle. Além disso, sem separação de responsabilidades, impossível testar cada regra individualmente.

---

### Prompt de refatoração

```
Como engenheiro de software especialista em princípios SOLID,
Quero que você refatore o método calculate_compliance do BatchService,
Para que novas regras de compliance possam ser adicionadas sem modificar a classe existente.

Código atual:
[código acima]

Aplique o princípio Open/Closed:
- Crie uma abstração ComplianceRule com método evaluate(row) → penalty
- Implemente cada regra como classe separada
- O ComplianceService recebe uma lista de regras e as aplica
- Novas regras são adicionadas criando novas classes, sem tocar no service

Restrições:
- Mantenha compatibilidade com a interface atual
- Cada regra deve ter nome descritivo e penalty documentada
- Use dataclasses ou Protocol para a abstração
```

---

### Código DEPOIS da refatoração

```python
# compliance_service.py — versão refatorada (OCP aplicado)
from dataclasses import dataclass
from typing import Protocol, List

class ComplianceRule(Protocol):
    def evaluate(self, row: dict) -> float:
        ...

@dataclass
class TemperatureRule:
    min_val: float = 30.0
    max_val: float = 40.0
    penalty: float = 10.0

    def evaluate(self, row: dict) -> float:
        t = row.get('temperature', 0)
        return self.penalty if not (self.min_val <= t <= self.max_val) else 0.0

@dataclass
class PhRule:
    min_val: float = 6.8
    max_val: float = 7.4
    penalty: float = 10.0

    def evaluate(self, row: dict) -> float:
        ph = row.get('ph', 0)
        return self.penalty if not (self.min_val <= ph <= self.max_val) else 0.0

# ... demais regras

class ComplianceService:
    DEFAULT_RULES: List[ComplianceRule] = [
        TemperatureRule(), PhRule(), OxygenRule(), PressureRule(), AgitatorRule()
    ]

    @classmethod
    def calculate_score(cls, rows: list, rules=None) -> float:
        rules = rules or cls.DEFAULT_RULES
        if not rows:
            return 0.0
        total_penalty = sum(
            rule.evaluate(row) for row in rows for rule in rules
        )
        avg_penalty = total_penalty / len(rows)
        return round(max(0.0, 100.0 - avg_penalty), 2)
```

---

### Avaliação do resultado

✅ Cada regra é testável de forma independente  
✅ Novas regras são adicionadas sem modificar `ComplianceService`  
✅ Configuração de regras injetável (útil para testes)  
⚠️ A IA inicialmente usou herança em vez de Protocol — Michele identificou a incongruência e solicitou correção para composição via Protocol (mais pythônico e flexível)

---

## Refatoração 2 — Correção do cálculo de predição ML (score x predição divergentes)

**Critério técnico:** Correção de bug — coerência semântica entre `risk_prediction` e `confidence_score`  
**Padrão de prompt:** Role-based + Few-shot  
**Ferramenta:** Claude Code (CLI)  
**Branch:** `develop`  
**Data:** 2026-06-06

### Análise crítica — Michele Oliveira

Ao testar o sistema em uso real, a autora percebeu que a resposta da API para um batch com dados claramente fora de especificação retornava `risk_prediction: "HIGH_RISK"` junto com `confidence_score: 0.85` — um score que parecia indicar que o processo estava 85% conforme. A combinação das duas informações era semanticamente contraditória e induzia interpretação errada no frontend.

A autora diagnosticou que havia duas fontes de dados sendo misturadas no mesmo campo de resposta: o modelo ML produzia a predição de risco, mas a confiança estava vindo do `ComplianceService` (sistema completamente independente). A decisão de investigar o código dos dois arquivos e corrigi-los em conjunto foi da autora — a IA foi acionada para localizar o trecho exato, propor a correção e aplicá-la.

---

### Contexto do problema

O endpoint `GET /api/v1/prediction/{batch_id}` retornava campos contraditórios: o `risk_prediction` vinha do modelo ML (`RandomForestClassifier`) enquanto o `confidence_score` estava sendo extraído do `ComplianceService` (score 0-100 normalizado para 0-1). Como os dois sistemas usam lógicas independentes, era comum ver respostas como:

```json
{
  "risk_prediction": "HIGH_RISK",
  "confidence_score": 0.85
}
```

Um score de 0.85 indica que o processo está em boa conformidade (equivalente a 85/100 no compliance), mas a predição diz HIGH_RISK — informação contraditória e que induzia decisões erradas no frontend.

Um segundo bug existia em `model.py`: o índice retornado por `sklearn.predict()` era usado diretamente para buscar a chave no dicionário `RISK_CLASSES`, mas a confiança (`confidence`) era calculada como `probabilities[0]` — sempre a probabilidade da classe `LOW_RISK` — independentemente da classe realmente predita. Isso fazia o score parecer alto mesmo quando o modelo previa risco elevado com baixa probabilidade atribuída à classe correta.

---

### Prompt utilizado

```
Você é um engenheiro de ML experiente em FastAPI e scikit-learn.

Encontrei um bug no BiotecPredict: o campo confidence_score retornado pela API
não corresponde à predição risk_prediction. Exemplo real observado:

  risk_prediction: "HIGH_RISK"
  confidence_score: 0.85  ← vem do ComplianceService, não do modelo ML

O código atual faz o seguinte em ml_service.py:

    risk_class, _ = MLService.predict_risk(sensor_readings)   # ignora confidence do ML
    compliance_score, _ = ComplianceService.calculate_compliance_score(sensor_readings)
    return {
        "risk_prediction": risk_class,
        "confidence_score": round(compliance_score / 100, 3),  # ❌ compliance, não ML
    }

E em model.py o predict() faz:

    prediction = self.model.predict(X_scaled)[0]
    probabilities = self.model.predict_proba(X_scaled)[0]
    confidence = float(probabilities[0])  # ❌ sempre usa prob da classe 0 (LOW_RISK)
    risk_class = self.RISK_CLASSES.get(prediction, "MEDIUM_RISK")
    return risk_class, round(confidence, 3)

Corrija os dois pontos para que:
1. confidence_score reflita a probabilidade real da classe predita pelo modelo ML
2. O cálculo seja feito em model.py com max(probabilities), garantindo que
   o score sempre corresponda à classe vencedora
3. ml_service.py use diretamente o confidence retornado pelo model.predict()
   sem misturar com o ComplianceService

Mostre o before e after de cada arquivo.
```

---

### Código ANTES da correção

**`backend/ml/model.py` — método `predict()`**

```python
def predict(self, sensor_readings: List[Dict]) -> Tuple[str, float]:
    if not self.model or not self.scaler:
        return "MEDIUM_RISK", 0.5

    X = self._extract_features(sensor_readings)
    if X is None or len(X) == 0:
        return "MEDIUM_RISK", 0.5

    X_scaled = self.scaler.transform([X])

    prediction = self.model.predict(X_scaled)[0]
    probabilities = self.model.predict_proba(X_scaled)[0]

    # ❌ Bug: sempre usa a probabilidade do índice 0 (LOW_RISK),
    #    independente da classe realmente predita.
    #    Se o modelo prediz HIGH_RISK com 80% de confiança,
    #    probabilities = [0.05, 0.15, 0.80], mas confidence = 0.05.
    confidence = float(probabilities[0])

    risk_class = self.RISK_CLASSES.get(prediction, "MEDIUM_RISK")
    return risk_class, round(confidence, 3)
```

**`backend/services/ml_service.py` — método `evaluate_batch_risk()`**

```python
@staticmethod
def evaluate_batch_risk(sensor_readings: List[Dict]) -> Dict:
    # ❌ Bug: ignora o confidence retornado pelo modelo ML
    risk_class, _ = MLService.predict_risk(sensor_readings)

    # ❌ Bug: usa o ComplianceService para gerar o score, que é uma
    #    métrica determinística (0-100) sem relação com a probabilidade
    #    do classificador. Os dois sistemas são independentes e podem
    #    facilmente divergir.
    compliance_score, _ = ComplianceService.calculate_compliance_score(sensor_readings)

    return {
        "risk_prediction": risk_class,
        "confidence_score": round(compliance_score / 100, 3),  # ❌ compliance, não ML
        "interpretation": MLService._interpret_risk(risk_class),
        "recommendations": MLService._get_recommendations(risk_class),
    }
```

**Exemplo de resposta bugada:**

```json
{
  "batch_id": 12,
  "risk_prediction": "HIGH_RISK",
  "confidence_score": 0.85,
  "interpretation": "Risco significativo de falha de processo. Intervenção recomendada."
}
```

O compliance score era 85/100 (processo quase conforme), mas o ML indicava HIGH_RISK — resposta semanticamente contraditória.

---

### Código DEPOIS da correção

**`backend/ml/model.py` — método `predict()`**

```python
def predict(self, sensor_readings: List[Dict]) -> Tuple[str, float]:
    if not self.model or not self.scaler:
        return "MEDIUM_RISK", 0.5

    X = self._extract_features(sensor_readings)
    if X is None or len(X) == 0:
        return "MEDIUM_RISK", 0.5

    X_scaled = self.scaler.transform([X])

    prediction = self.model.predict(X_scaled)[0]
    probabilities = self.model.predict_proba(X_scaled)[0]

    # ✅ Corrigido: max(probabilities) é sempre a probabilidade da classe
    #    vencedora (sklearn.predict retorna argmax das probabilidades),
    #    garantindo que confidence_score e risk_prediction sejam coerentes.
    confidence = max(probabilities)

    risk_class = self.RISK_CLASSES.get(prediction, "MEDIUM_RISK")
    return risk_class, round(float(confidence), 3)
```

**`backend/services/ml_service.py` — método `evaluate_batch_risk()`**

```python
@staticmethod
def evaluate_batch_risk(sensor_readings: List[Dict]) -> Dict:
    # ✅ Corrigido: usa o confidence diretamente do modelo ML.
    #    risk_class e confidence provêm da mesma chamada predict(),
    #    garantindo que representem a mesma decisão do classificador.
    risk_class, confidence = MLService.predict_risk(sensor_readings)

    return {
        "risk_prediction": risk_class,
        "confidence_score": confidence,  # ✅ probabilidade real da classe predita
        "interpretation": MLService._interpret_risk(risk_class),
        "recommendations": MLService._get_recommendations(risk_class),
    }
```

**Exemplo de resposta corrigida:**

```json
{
  "batch_id": 12,
  "risk_prediction": "HIGH_RISK",
  "confidence_score": 0.80,
  "interpretation": "Risco significativo de falha de processo. Intervenção recomendada."
}
```

Agora `confidence_score` expressa a probabilidade do modelo para a classe `HIGH_RISK` — 80% de certeza de que o processo está em alto risco. Score e predição são coerentes.

---

### Avaliação do resultado

✅ `confidence_score` e `risk_prediction` derivam da mesma fonte (`model.predict_proba`)  
✅ Eliminada dependência desnecessária do `ComplianceService` dentro do `MLService`  
✅ Comportamento previsível: `max(probabilities)` == probabilidade da classe retornada por `predict()`  
⚠️ Claude Code identificou que o `ComplianceService` e o `MLService` devem ser tratados como fontes independentes de informação no response da API — decisão arquitetural confirmada por Michele

---

## Refatoração 3 — Correção dos indicadores de sensor, cálculo de compliance e dados de treino ML

**Critério técnico:** Correção de múltiplos bugs — consistência entre frontend, regras de compliance e modelo ML  
**Padrão de prompt:** Role-based + Diagnóstico incremental  
**Ferramenta:** Claude Code (CLI)  
**Branch:** `develop`  
**Data:** 2026-06-07

### Análise crítica — Michele Oliveira

Ao testar o sistema com os três CSVs de simulação como usuária final, a autora identificou três comportamentos incorretos que invalidavam o diagnóstico do sistema:

1. **Indicadores visuais de sensor sempre verdes:** ao importar o CSV de alto risco — com temperatura chegando a 42°C, pH a 8,9 e oxigênio dissolvido a 35% — todos os indicadores do dashboard continuavam exibidos em verde, sugerindo que o processo estava normal. Um sistema de monitoramento que não alerta para valores claramente fora de especificação não cumpre sua função.

2. **Score de compliance inconsistente com a classificação de risco:** o CSV de risco médio (2 sensores fora da faixa) retornava um Compliance Score de ~18 com classificação CRITICAL, quando o esperado para um cenário com apenas 2 de 5 sensores comprometidos seria um WARNING. O score CRITICAL estava sendo aplicado incorretamente a um cenário que ainda tinha 3 sensores perfeitos.

3. **Confiança do modelo ML não compatível com os cenários extremos:** ao testar o CSV de alto risco com todos os 5 sensores fora da faixa, a confiança da predição parecia inconsistentemente baixa em relação à clareza do cenário. A autora suspeitou que o modelo não havia sido treinado com exemplos suficientemente variados para cobrir casos com 4 ou 5 sensores fora da faixa simultaneamente.

Com os três problemas identificados e descritos, a autora acionou o Claude Code para localizar as origens no código, propor as correções e executar os testes de validação.

---

### Bug 1 — Ranges dos indicadores de sensor no frontend

**Arquivo:** `frontend/src/components/Dashboard/Dashboard.tsx`

O frontend usava ranges de visualização completamente arbitrários e muito mais amplos do que as faixas aceitáveis do processo, tornando os indicadores inúteis como ferramenta de alerta.

#### Código ANTES

```tsx
{/* Temperatura */}
<p className="range-text">Range: 20 - 45°C</p>  {/* ❌ máximo 45°C — deveria ser 30°C */}
<div
  className="range-fill"
  style={{
    width: `${Math.min(100, (sensorData.temperature / 45) * 100)}%`,
    backgroundColor: sensorData.temperature >= 20 && sensorData.temperature <= 45
      ? '#10b981'   // ❌ verde até 45°C — temperatura de 42°C aparecia VERDE
      : '#ef4444'
  }}
/>

{/* pH */}
<p className="range-text">Range: 4.0 - 9.0</p>  {/* ❌ máximo 9.0 — deveria ser 7.5 */}
<div
  className="range-fill"
  style={{
    width: `${Math.min(100, ((sensorData.ph - 4) / 5) * 100)}%`,
    backgroundColor: sensorData.ph >= 4 && sensorData.ph <= 9
      ? '#10b981'   // ❌ verde até pH 9.0 — pH 8.9 aparecia VERDE
      : '#ef4444'
  }}
/>

{/* Oxigênio Dissolvido */}
<p className="range-text">Range: 0 - 100%</p>   {/* ❌ mínimo 0% — deveria ser 70% */}
<div
  className="range-fill"
  style={{
    width: `${Math.min(100, sensorData.dissolved_oxygen)}%`,
    backgroundColor: sensorData.dissolved_oxygen >= 0 && sensorData.dissolved_oxygen <= 100
      ? '#10b981'   // ❌ verde para qualquer valor — DO 35% aparecia VERDE
      : '#ef4444'
  }}
/>

{/* Pressão */}
<p className="range-text">Range: 0 - 10 bar</p>  {/* ❌ faixa 10x mais larga que o processo */}
{/* Agitador */}
<p className="range-text">Range: 0 - 500 RPM</p> {/* ❌ faixa 5x mais larga que o processo */}
```

**Impacto:** todos os sensores do CSV de alto risco (temperatura 37°C, pH 8,5, DO 49%) apareciam em verde no dashboard, contradizendo o score CRITICAL e a predição HIGH_RISK.

#### Código DEPOIS

```tsx
{/* Temperatura */}
<p className="range-text">Aceitável: 20 – 30°C | Ideal: 24 – 26°C</p>
<div
  className="range-fill"
  style={{
    width: `${Math.min(100, ((sensorData.temperature - 20) / 10) * 100)}%`,
    backgroundColor: sensorData.temperature >= 20 && sensorData.temperature <= 30
      ? '#10b981'   // ✅ verde apenas dentro da faixa aceitável do processo
      : '#ef4444'   // ✅ vermelho para temperatura > 30°C ou < 20°C
  }}
/>

{/* pH */}
<p className="range-text">Aceitável: 6.5 – 7.5 | Ideal: 6.8 – 7.2</p>
<div
  className="range-fill"
  style={{
    width: `${Math.min(100, ((sensorData.ph - 6.5) / 1.0) * 100)}%`,
    backgroundColor: sensorData.ph >= 6.5 && sensorData.ph <= 7.5
      ? '#10b981'   // ✅ vermelho para pH > 7.5
      : '#ef4444'
  }}
/>

{/* Oxigênio Dissolvido */}
<p className="range-text">Aceitável: 70 – 100% | Ideal: 80 – 95%</p>
<div
  className="range-fill"
  style={{
    width: `${Math.min(100, ((sensorData.dissolved_oxygen - 70) / 30) * 100)}%`,
    backgroundColor: sensorData.dissolved_oxygen >= 70 && sensorData.dissolved_oxygen <= 100
      ? '#10b981'   // ✅ vermelho para DO < 70%
      : '#ef4444'
  }}
/>

{/* Pressão: Aceitável 4.5–6.0 bar | Agitador: Aceitável 200–300 RPM */}
```

---

### Bug 2 — Dupla penalização no cálculo do Compliance Score

**Arquivo:** `backend/services/compliance_service.py`

#### Código ANTES

```python
@staticmethod
def calculate_compliance_score(sensor_readings):
    sensor_scores = {}
    total_penalty = 0.0   # ❌ penalidade acumulada separada

    for sensor_name, sensor_range in SENSOR_RANGES.items():
        avg_value = sum(values) / len(values)
        sensor_score, penalty = ComplianceService._calculate_sensor_score(
            sensor_name, avg_value, sensor_range
        )
        sensor_scores[sensor_name] = sensor_score
        total_penalty += penalty  # ❌ acumula 20 pts por sensor fora da faixa

    average_score = sum(sensor_scores.values()) / len(sensor_scores)
    # ❌ dupla penalização: sensor fora da faixa já recebe score=0,
    #    e ainda desconta 20 pts adicionais do score médio.
    #    Com 2 sensores fora: média≈57, menos 40 de penalty = 17 → CRITICAL
    #    quando deveria ser WARNING.
    final_score = max(0.0, average_score - total_penalty)

@staticmethod
def _calculate_sensor_score(sensor_name, value, sensor_range):
    if sensor_range.ideal_min <= value <= sensor_range.ideal_max:
        score = 100 - (deviation_ratio * 10)
    elif sensor_range.min_value <= value <= sensor_range.max_value:
        score = 60 + (40 * (1 - deviation_ratio))
    else:
        score = 0.0   # sensor fora da faixa → já penalizado com 0

    penalty = 0.0
    if value < sensor_range.min_value or value > sensor_range.max_value:
        penalty = 20.0  # ❌ penalidade adicional sobre sensor que já vale 0

    return max(0.0, score), penalty

@staticmethod
def _classify_score(score):
    if score >= 80: return "ACCEPTABLE"
    elif score >= 60: return "WARNING"   # ❌ limiar de 60 tornava 2-sensor-out CRITICAL
    else: return "CRITICAL"
```

**Impacto:** CSV de risco médio (2 sensores fora) retornava score ~17 → CRITICAL. Deveria ser ~58 → WARNING.

#### Código DEPOIS

```python
@staticmethod
def calculate_compliance_score(sensor_readings):
    sensor_scores = {}
    # ✅ sem total_penalty: sensor com score=0 já está penalizado

    for sensor_name, sensor_range in SENSOR_RANGES.items():
        avg_value = sum(values) / len(values)
        sensor_score = ComplianceService._calculate_sensor_score(
            sensor_name, avg_value, sensor_range
        )
        sensor_scores[sensor_name] = sensor_score

    average_score = sum(sensor_scores.values()) / len(sensor_scores)
    # ✅ score final = média pura das pontuações individuais
    final_score = min(100.0, max(0.0, average_score))

@staticmethod
def _calculate_sensor_score(sensor_name, value, sensor_range) -> float:
    """Retorna score 0-100. Fora da faixa → 0. Sem penalidade separada."""
    if sensor_range.ideal_min <= value <= sensor_range.ideal_max:
        score = 100 - (deviation_ratio * 10)      # 90–100
    elif sensor_range.min_value <= value <= sensor_range.max_value:
        score = 60 + (30 * (1 - deviation_ratio)) # 60–90  ✅ banda ajustada
    else:
        score = 0.0  # ✅ penalização única e suficiente

    return max(0.0, score)

@staticmethod
def _classify_score(score):
    if score >= 80: return "ACCEPTABLE"
    elif score >= 45: return "WARNING"   # ✅ limiar ajustado: 2 sensores fora ≈ 58 → WARNING
    else: return "CRITICAL"
```

**Resultado após correção:**

| Cenário | Score antes | Classe antes | Score depois | Classe depois |
|---|---|---|---|---|
| LOW RISK (0 sensores fora) | ~95 | ACCEPTABLE | 93,78 | ACCEPTABLE |
| MEDIUM RISK (2 sensores fora) | ~17 | **CRITICAL** ❌ | 58,17 | **WARNING** ✅ |
| HIGH RISK (5 sensores fora) | 0 | CRITICAL | 0,00 | CRITICAL |

---

### Bug 3 — Gap no conjunto de dados de treino do modelo ML

**Arquivo:** `backend/ml/model.py`

#### Código ANTES

```python
def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
    n_low    = int(n_samples * 0.60)
    n_medium = int(n_samples * 0.25)
    n_high   = n_samples - n_low - n_medium

    # ❌ MEDIUM_RISK treinado apenas com exatamente 1 sensor fora
    #    — sem nenhum exemplo com 2 sensores fora.
    #    O CSV de risco médio tem 2 sensores fora → gap no treino.
    X_medium = _sample_out_of_range(n_medium, 1)

    # ❌ HIGH_RISK treinado apenas com exatamente 3 sensores fora
    #    — sem exemplos com 4 ou 5 sensores fora.
    #    O CSV de alto risco tem TODOS os 5 sensores fora → gap no treino.
    X_high   = _sample_out_of_range(n_high, 3)

    # ❌ range de temperatura out-of-range limitado a 40°C
    #    — CSV de alto risco chega a 42°C, fora da distribuição de treino.
    out_ranges = [
        (30.1, 40.0),   # temperature acima ← limitado
        ...
    ]
```

#### Código DEPOIS

```python
def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
    n_low    = int(n_samples * 0.50)
    n_medium = int(n_samples * 0.30)
    n_high   = n_samples - n_low - n_medium

    # ✅ MEDIUM_RISK: metade com 1 sensor fora, metade com 2 — sem gap
    n_med1 = n_medium // 2
    n_med2 = n_medium - n_med1
    X_medium = np.vstack([
        _sample_out_of_range(n_med1, 1),
        _sample_out_of_range(n_med2, 2),
    ])

    # ✅ HIGH_RISK: distribuído entre 3, 4 e 5 sensores fora
    n_high3 = n_high // 3
    n_high4 = n_high // 3
    n_high5 = n_high - n_high3 - n_high4
    X_high = np.vstack([
        _sample_out_of_range(n_high3, 3),
        _sample_out_of_range(n_high4, 4),
        _sample_out_of_range(n_high5, 5),
    ])

    # ✅ range de temperatura estendido até 45°C para cobrir valores extremos
    out_ranges = [
        (30.1, 45.0),   # temperature acima — estendido
        (7.6,  9.5),    # ph acima — estendido
        (6.1,  8.0),    # pressure acima — novo
        (301,  450),    # agitator acima — novo
        ...
    ]
```

**Resultado após correção (testes com os CSVs reais):**

```
LOW RISK CSV   → LOW_RISK,    confiança 97,5%
MEDIUM RISK CSV → MEDIUM_RISK, confiança 80,7%
HIGH RISK CSV  → HIGH_RISK,   confiança 84,1%
```

---

### Avaliação do resultado — validação end-to-end

Os três bugs foram corrigidos e validados via API com upload real dos CSVs de simulação:

```
POST /api/v1/upload (batch_sensor_low_risk.csv)
→ compliance_score: 93.78  |  risk_prediction: LOW_RISK

POST /api/v1/upload (batch_sensor_medium_risk.csv)
→ compliance_score: 58.17  |  risk_prediction: MEDIUM_RISK

POST /api/v1/upload (batch_sensor_high_risk.csv)
→ compliance_score: 0.00   |  risk_prediction: HIGH_RISK
```

✅ Indicadores de sensor agora mostram vermelho para valores fora da faixa aceitável do processo  
✅ CSV de risco médio classificado como WARNING (não CRITICAL)  
✅ Score de compliance e predição ML consistentes em todos os três cenários  
✅ Modelo retreinado com dados balanceados — arquivos `.pkl` regenerados automaticamente no startup  

### O que significa a confiança da predição — esclarecimento importante

Durante a validação, Michele levantou uma dúvida pertinente: por que o HIGH RISK CSV tem confiança de 84,1% sendo que deveria ser o pior cenário? A resposta é que **a confiança não mede o quão ruim está o processo — mede o quanto o modelo tem certeza da sua própria resposta.**

O modelo faz uma pergunta internamente: *"qual das três classes melhor descreve este batch?"* As 100 árvores do RandomForest votam. A confiança é o percentual de votos que a classe vencedora recebeu:

```
HIGH RISK CSV → 84 de 100 árvores votaram HIGH_RISK
                → predição: HIGH_RISK, confiança: 84%
```

Isso significa: o modelo tem 84% de certeza de que o batch é HIGH_RISK — não que o processo está 84% bom.

A confiança do HIGH_RISK (84%) é menor que a do LOW_RISK (97%) porque o LOW_RISK é um cenário mais homogêneo e bem representado no treino (50% das amostras). O HIGH_RISK cobre combinações mais variadas de falha (3, 4 ou 5 sensores fora, com diferentes magnitudes), o que gera mais divergência entre as árvores. Esse comportamento é esperado e não indica problema na predição.

Como ler os dois números em conjunto:

| CSV | Compliance Score | Predição | Confiança | Leitura correta |
|---|---|---|---|---|
| Low Risk | 93,78 | LOW_RISK | 97,5% | Processo saudável, modelo muito certo disso |
| Medium Risk | 58,17 | MEDIUM_RISK | 80,7% | Processo com desvios, modelo bastante certo |
| High Risk | 0,00 | HIGH_RISK | 84,1% | Processo em colapso, modelo bastante certo |

O **Compliance Score** (0 a 100) mede a saúde do processo. A **confiança** (%) mede a certeza interna do modelo sobre a classificação escolhida. São métricas independentes — um processo péssimo pode ter confiança alta na predição justamente porque o modelo o reconhece claramente como HIGH_RISK.
