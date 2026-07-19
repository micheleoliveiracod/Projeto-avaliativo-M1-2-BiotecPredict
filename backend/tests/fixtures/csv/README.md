# Fixtures CSV — BiotecPredict

Arquivos CSV para uso nos testes **pytest**, **Postman** e **E2E** do projeto.

**Localização**: `backend/tests/fixtures/csv/`
**Base URL para Postman/E2E**: `http://localhost:8001/api/v1/upload`

---

## Estrutura de Pastas

Os fixtures são organizados por **propósito de uso**, não por ordem alfabética. Antes de usar um
arquivo, confira em qual pasta ele está para saber o que esperar dele:

```
backend/tests/fixtures/csv/
├── control/       ← comportamento correto (golden path + variações + fronteiras exatas)
├── bugs/          ← reproduzem os bugs de cálculo já encontrados E CORRIGIDOS (ver seção própria)
├── rejected/      ← upload deve ser rejeitado (HTTP 400) — nunca sobem para o banco
└── performance/   ← só para medir tempo de upload, não para validar score/classificação
```

| Pasta | Quando usar |
|---|---|
| `control/` | Popular o banco com histórico "saudável", validar que o cálculo funciona no caso normal |
| `bugs/` | Regressão — garantir que os bugs corrigidos em 2026-07-19 não voltem a acontecer |
| `rejected/` | Testar que o `DataValidator` rejeita corretamente — **não fazer upload esperando sucesso** |
| `performance/` | Testar SLA de upload (< 5s) — não representa um lote real de processo |

---

## Ranges de Referência

### DataValidator (filtro no upload — rejeita se fora deste range)
| Sensor | Mínimo | Máximo | Unidade |
|---|---|---|---|
| temperature | 20 | 45 | °C |
| ph | 4.0 | 9.0 | — |
| dissolved_oxygen | 0 | 100 | % |
| pressure | 0 | 10 | bar |
| agitator_speed | 0 | 500 | RPM |

### ComplianceService (scoring — usado para calcular o score 0-100)
| Sensor | Aceitável | Ideal | Unidade |
|---|---|---|---|
| temperature | 20–30 | 24–26 | °C |
| ph | 6.5–7.5 | 6.8–7.2 | — |
| dissolved_oxygen | 70–100 | 80–95 | % |
| pressure | 4.5–6.0 | 4.8–5.5 | bar |
| agitator_speed | 200–300 | 240–280 | RPM |

### As duas métricas medem coisas diferentes, por design

- **Compliance Score** mede **qualidade** — o quão próximo cada sensor está do centro da faixa
  *ideal*. Responde "quão boa está a produção?".
- **Predição de Risco (ML)** mede **desvio do limite aceitável** — quantos sensores (0, 1-2 ou 3+)
  romperam a faixa *aceitável*, sinalizando se o lote deve ser descartado/investigado. Responde
  "quantos parâmetros de fato romperam o limite de aceite?".

Ver `docs/analise-resultados.md`, seção 7.3, para o guia completo de leitura conjunta.

---

## Arquivos Disponíveis

Todos os valores de "Resultado Esperado" abaixo foram **recalculados executando o código real**
(`ComplianceService.calculate_compliance_score` + `MLModel.predict`) em 2026-07-19, após as
correções descritas na seção "Bugs de Cálculo — Corrigidos" abaixo. Se o código mudar, rode o
script de verificação (seção "Como Validar os Fixtures") e atualize esta tabela — caso contrário
a tabela mente sobre o comportamento real do sistema.

### ✅ `control/` — Válidos, comportamento correto (Upload HTTP 200)

| Arquivo | Linhas | Score | Classificação | Risco ML (confiança) | Uso |
|---|---|---|---|---|---|
| `valid_ideal.csv` | 10 | 97.0 | ACCEPTABLE | LOW_RISK (0.999) | Caso feliz (golden path) |
| `valid_acceptable.csv` | 8 | 80.31 | ACCEPTABLE | LOW_RISK (0.998) | Aceitável mas não ideal |
| `valid_boundary.csv` | 4 | 12.19 | CRITICAL | MEDIUM_RISK (0.829) | Valores nos limites do DataValidator (20/45, 4.0/9.0 etc.) — a maioria das leituras rompe o aceitável do Compliance |
| `single_sensor_out_ph.csv` | 8 | 79.65 | WARNING | MEDIUM_RISK (1.0) | 1 sensor fora (pH), resto ideal |
| `two_sensors_out.csv` | 8 | 59.76 | WARNING | MEDIUM_RISK (0.961) | 2 sensores fora do aceitável |
| `four_sensors_out.csv` | 8 | 19.91 | CRITICAL | HIGH_RISK (0.992) | 4 sensores fora |
| `five_sensors_out.csv` | 8 | 0.0 | CRITICAL | HIGH_RISK (1.0) | 5 sensores fora |
| `boundary_acceptable_warning_high.csv` | 6 | 81.0 | ACCEPTABLE | LOW_RISK (0.999) | Fronteira ACCEPTABLE/WARNING, lado ≥80 |
| `boundary_acceptable_warning_low.csv` | 6 | 79.19 | WARNING | LOW_RISK (0.999) | Fronteira ACCEPTABLE/WARNING, lado <80 — qualidade caiu mas nenhum sensor rompeu o aceitável (esperado, não é bug) |
| `boundary_warning_critical_high.csv` | 6 | 45.17 | WARNING | MEDIUM_RISK (0.852) | Fronteira WARNING/CRITICAL, lado ≥45 |
| `boundary_warning_critical_low.csv` | 6 | 44.81 | CRITICAL | MEDIUM_RISK (0.857) | Fronteira WARNING/CRITICAL, lado <45 — 2 sensores rompem o aceitável |
| `batch_sensor_low_risk.csv` | 100 | 92.39 | ACCEPTABLE | LOW_RISK (0.998) | Lote grande consistente (baixo risco) |
| `batch_sensor_medium_risk.csv` | 100 | 63.91 | WARNING | MEDIUM_RISK (0.979) | Lote grande consistente (risco médio) |
| `batch_sensor_high_risk.csv` | 100 | 0.0 | CRITICAL | HIGH_RISK (0.993) | Lote grande consistente (alto risco) |

### 🧪 `bugs/` — Testes de regressão dos bugs corrigidos (Upload HTTP 200)

| Arquivo | Linhas | Score | Classificação | Risco ML (confiança) | Bug que este fixture regride |
|---|---|---|---|---|---|
| `warning_zone.csv` | 5 | 69.48 | WARNING | LOW_RISK (0.996) | Não é bug — WARNING (qualidade baixa) + LOW_RISK (nenhum sensor rompeu o aceitável) é o comportamento esperado por design |
| `critical_zone.csv` | 5 | 0.0 | CRITICAL | HIGH_RISK (0.953) | Corrigido — ML previa MEDIUM_RISK, agora prevê HIGH_RISK corretamente |
| `single_sensor_out_temperature.csv` | 8 | 79.6 | WARNING | MEDIUM_RISK (0.971) | Corrigido — ML previa LOW_RISK, agora prevê MEDIUM_RISK corretamente |
| `three_sensors_out.csv` | 8 | 39.84 | CRITICAL | HIGH_RISK (0.739) | Corrigido — ML previa MEDIUM_RISK, agora prevê HIGH_RISK corretamente |
| `outlier_masked_by_average.csv` | 10 | 95.48 | ACCEPTABLE | LOW_RISK (0.999) | Corrigido (parcial, por design) — score sobe de 94.13→95.48 com a pontuação por leitura; a leitura anômala agora aparece explicitamente em `anomalous_readings` (1/10), sem forçar downgrade de classificação (ver nota abaixo) |
| `rounding_boundary_inconsistency.csv` | 6 | 45.0 | WARNING | MEDIUM_RISK (0.857) | Corrigido — score "45.0" agora classifica WARNING de forma consistente (antes dava CRITICAL) |

### 🚀 `performance/` — Teste de carga

| Arquivo | Linhas | Resultado Esperado | Uso |
|---|---|---|---|
| `valid_large_500rows.csv` | 500 | Upload OK em < 5s (score 94.97 · ACCEPTABLE) | Teste de performance (SLA) |

### ❌ `rejected/` — Upload rejeitado (HTTP 400)

| Arquivo | Motivo da Rejeição |
|---|---|
| `invalid_empty.csv` | Arquivo sem conteúdo (0 bytes) |
| `invalid_missing_columns.csv` | Colunas `dissolved_oxygen`, `pressure`, `agitator_speed` ausentes |
| `invalid_wrong_types.csv` | Valores não numéricos nos campos de sensor |
| `invalid_out_of_range.csv` | Valores fora do range do DataValidator (temp=50, pH=12, etc.) |

---

## ✅ Bugs de Cálculo — Corrigidos (2026-07-19)

Os 3 bugs reais encontrados ao validar o código com estes fixtures foram corrigidos. O que era
apenas uma divergência esperada por design (Compliance × ML medindo eixos diferentes) **não** foi
alterado — ver seção "As duas métricas medem coisas diferentes" acima.

### 1. `ComplianceService` pontuava a média dos valores brutos, não a média dos scores

**Antes:** `avg_value = sum(values) / len(values)` calculava a média das leituras *antes* de
pontuar — uma leitura catastrófica isolada (ex: temperatura 44°C num lote de 9 leituras ideais)
virava invisível na média bruta (`outlier_masked_by_average.csv` dava 94.13 · ACCEPTABLE).

**Correção:** cada leitura agora é pontuada individualmente (`_calculate_sensor_score` por linha),
e o score do sensor é a média dessas notas — não a nota da média bruta. Isso deixou o algoritmo
mais honesto em qualquer lote com leituras heterogêneas: `valid_boundary.csv`, por exemplo, que
tinha várias leituras extremas diluídas por uma média moderada, caiu de 50.14 (WARNING) para o
valor real, 12.19 (CRITICAL).

**O que decidimos não fazer:** cogitamos forçar a classificação para no mínimo WARNING sempre que
qualquer leitura individual rompesse totalmente a faixa aceitável de um sensor. Decidimos **não**
fazer isso — um outlier isolado pode ser falha de equipamento/sensor, não do produto, e forçar o
downgrade geraria alarme falso em lotes bons por causa de um soluço de sensor. Em vez disso,
adicionamos `ComplianceService.detect_anomalous_readings()` (exposto em
`GET /api/v1/compliance/{batch_id}` como `anomalous_readings`), que informa quantas leituras e
quais sensores tiveram rompimento, sem alterar score nem classificação — a decisão de investigar
fica com quem consome o dado (ex: Root-Spector), não com uma regra cega no Compliance.

**Por que média e não mediana:** também avaliamos usar a **mediana** das notas por leitura em vez
da média, pensando em blindar o score contra outliers. Testamos com o código real e o resultado é
o oposto do esperado — a mediana **piora** o mascaramento, não resolve. Motivo estatístico: a
mediana tem *breakdown point* de quase 50% (só se move quando mais da metade dos dados muda), ou
seja, ela foi desenhada justamente para **ignorar** uma minoria de valores extremos. Com 1 leitura
catastrófica em 10, a mediana das notas de temperatura em `outlier_masked_by_average.csv` volta a
**100.0** (como se a leitura ruim nunca tivesse existido), e o score do lote **sobe** de 95.48 para
97.48 — pior, não melhor. A média, com *breakdown point* de 0% (qualquer valor entra com peso
proporcional 1/n), é o estimador certo aqui: dá visibilidade parcial ao outlier sem deixá-lo
dominar sozinho o resultado. Por isso o score usa média, e a detecção de outlier fica no sinal
`anomalous_readings`, separado — a estatística certa para "não esconder o evento" (média) e a
estatística certa para "não deixar isso derrubar o produto sozinho" (contagem informativa, não
classificação forçada) são ferramentas diferentes, e usamos cada uma para o que ela resolve bem.

### 2. `_classify_score` classificava o valor não arredondado

**Antes:** o score retornado ao chamador era `round(final_score, 2)`, mas `_classify_score` era
chamado com o valor **não arredondado** — na fronteira exata (ex: valor real ≈44.997, que arredonda
para "45.0"), o resultado podia ser score exibido "45.0" com classificação **CRITICAL**, quando
"45.0" em qualquer outro lote classificaria WARNING.

**Correção:** o arredondamento agora acontece **antes** da classificação — o valor que é exibido
é exatamente o valor usado para decidir a categoria. `rounding_boundary_inconsistency.csv` passou
a dar "45.0" · WARNING de forma consistente.

### 3. `MLModel` era treinado com poucos dados sintéticos (500 amostras) e errava contra a própria regra de rótulo

**Antes:** com apenas 500 amostras sintéticas, as combinações de "exatamente 1" ou "exatamente 3"
sensores fora da faixa aceitável (a regra usada em `_generate_synthetic_labels` para gerar os
próprios rótulos de treino) ficavam com poucas dezenas de exemplos cada (5 sensores × 2 direções
de desvio). O classificador treinado nessa base esparsa **errava contra sua própria definição**:
previa LOW_RISK para lotes com 1 sensor comprovadamente fora (deveria ser MEDIUM_RISK) e
MEDIUM_RISK para lotes com 3+ sensores fora (deveria ser HIGH_RISK).

**Correção:** aumentamos a base sintética de 500 para 15.000 amostras e ajustamos os hiperparâmetros
do `RandomForestClassifier` (`n_estimators` 100→200, `max_depth` 10→14, `min_samples_split` 5→4,
`min_samples_leaf` 2→1). Custo de treino: ~1 segundo (negligenciável, roda só uma vez quando não
há modelo salvo em `backend/ml/models/`). Acurácia em conjunto de teste sintético subiu de ~92%
para ~99.6%, e os 3 casos que antes erravam agora acertam com boa confiança:
- `single_sensor_out_temperature.csv`: LOW_RISK (0.775) → **MEDIUM_RISK (0.971)**
- `critical_zone.csv`: MEDIUM_RISK (0.592) → **HIGH_RISK (0.953)**
- `three_sensors_out.csv`: MEDIUM_RISK (0.67) → **HIGH_RISK (0.739)**

> Se você já tinha um `backend/ml/models/risk_predictor.pkl` / `scaler.pkl` salvo de antes dessa
> correção, apague os dois arquivos para forçar o retreino — o modelo salvo antigo continua sendo
> carregado (`_ensure_model_exists`) mesmo depois do código mudar, até ser apagado.

---

## Como Validar os Fixtures

Rode a partir da raiz do repositório (requer o venv do backend, com `sqlalchemy`/`scikit-learn`
instalados) para recalcular score/classificação/risco de qualquer fixture com o código atual:

```python
import csv
from backend.services.compliance_service import ComplianceService
from backend.ml.model import MLModel

with open("backend/tests/fixtures/csv/<pasta>/<arquivo>.csv") as f:
    rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]

score, classification = ComplianceService.calculate_compliance_score(rows)
risk, confidence = MLModel().predict(rows)
anomalies = ComplianceService.detect_anomalous_readings(rows)
print(score, classification, risk, confidence, anomalies)
```

---

## Como Usar

### pytest
```python
from pathlib import Path

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "csv"

def test_upload_ideal(client):
    csv_path = FIXTURES / "control" / "valid_ideal.csv"
    files = {"file": ("valid_ideal.csv", open(csv_path, "rb"), "text/csv")}
    r = client.post("/api/v1/upload", files=files)
    assert r.status_code == 200
```

### Postman
1. No request `Upload CSV Válido`, selecione o arquivo em **Body → form-data → file**
2. Use `control/valid_ideal.csv` para o fluxo principal
3. Use `rejected/invalid_empty.csv` para testar a resposta 400

### E2E (Playwright)
```typescript
await page.setInputFiles('input[type="file"]', 'backend/tests/fixtures/csv/control/valid_ideal.csv');
await page.click('button[type="submit"]');
await expect(page.locator('.compliance-score')).toBeVisible();
```

---

## Cenários de Teste Recomendados

| Cenário | Arquivo | Endpoint | Expectativa |
|---|---|---|---|
| Golden path completo | `control/valid_ideal.csv` | upload → compliance → prediction | 200 + ACCEPTABLE + LOW_RISK |
| Alerta de qualidade (por design, não é bug) | `bugs/warning_zone.csv` | upload → compliance | 200 + WARNING + LOW_RISK |
| Falha crítica | `bugs/critical_zone.csv` | upload → compliance → prediction | 200 + CRITICAL + HIGH_RISK |
| Performance (SLA < 5s) | `performance/valid_large_500rows.csv` | upload | 200 em < 5s |
| Rejeição — vazio | `rejected/invalid_empty.csv` | upload | 400 |
| Rejeição — schema | `rejected/invalid_missing_columns.csv` | upload | 400 |
| Rejeição — tipos | `rejected/invalid_wrong_types.csv` | upload | 400 |
| Rejeição — range | `rejected/invalid_out_of_range.csv` | upload | 400 |
| Fronteira ACCEPTABLE/WARNING | `control/boundary_acceptable_warning_high.csv` + `_low.csv` | compliance | 81.0 ACCEPTABLE vs 79.19 WARNING |
| Fronteira WARNING/CRITICAL | `control/boundary_warning_critical_high.csv` + `_low.csv` | compliance | 45.17 WARNING vs 44.81 CRITICAL |
| Regressão — ML contra própria regra de treino | `bugs/single_sensor_out_temperature.csv`, `bugs/three_sensors_out.csv` | compliance + prediction | ver "Bugs de Cálculo — Corrigidos", item 3 |
| Regressão — outlier isolado no lote | `bugs/outlier_masked_by_average.csv` | compliance | score sobe com a nova pontuação por leitura; `anomalous_readings` mostra 1/10 leituras anômalas |
| Regressão — arredondamento vs. classificação | `bugs/rounding_boundary_inconsistency.csv` | compliance | score "45.0" deve classificar WARNING de forma consistente |
