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
├── control/       ← comportamento correto, sem bugs conhecidos (golden path + variações)
├── bugs/          ← reproduzem divergências reais entre ComplianceService e MLModel
├── rejected/      ← upload deve ser rejeitado (HTTP 400) — nunca sobem para o banco
└── performance/   ← só para medir tempo de upload, não para validar score/classificação
```

| Pasta | Quando usar |
|---|---|
| `control/` | Popular o banco com histórico "saudável", validar que o cálculo funciona no caso normal |
| `bugs/` | Reproduzir/registrar os problemas de cálculo já encontrados (ver seção própria abaixo) — suba só se quiser o histórico documentando os casos suspeitos |
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

---

## Arquivos Disponíveis

Todos os valores de "Resultado Esperado" abaixo foram **recalculados executando o código real**
(`ComplianceService.calculate_compliance_score` + `MLModel.predict`), não são estimativas. Se o
código mudar, rode o script de verificação (seção "Como Validar os Fixtures" abaixo) e atualize esta
tabela — caso contrário a tabela mente sobre o comportamento real do sistema.

### ✅ `control/` — Válidos, comportamento correto (Upload HTTP 200)

| Arquivo | Linhas | Score | Classificação | Risco ML (confiança) | Uso |
|---|---|---|---|---|---|
| `valid_ideal.csv` | 10 | 98.65 | ACCEPTABLE | LOW_RISK (0.985) | Caso feliz (golden path) |
| `valid_acceptable.csv` | 8 | 88.06 | ACCEPTABLE | LOW_RISK (0.995) | Aceitável mas não ideal |
| `valid_boundary.csv` | 4 | 50.14 | WARNING | MEDIUM_RISK (0.933) | Valores nos limites do DataValidator (20/45, 4.0/9.0 etc.) |
| `single_sensor_out_ph.csv` | 8 | 79.87 | WARNING | MEDIUM_RISK (0.886) | 1 sensor fora (pH), resto ideal |
| `two_sensors_out.csv` | 8 | 59.92 | WARNING | MEDIUM_RISK (0.825) | 2 sensores fora do aceitável |
| `four_sensors_out.csv` | 8 | 20.0 | CRITICAL | HIGH_RISK (0.842) | 4 sensores fora |
| `five_sensors_out.csv` | 8 | 0.0 | CRITICAL | HIGH_RISK (0.862) | 5 sensores fora |
| `boundary_acceptable_warning_high.csv` | 6 | 81.0 | ACCEPTABLE | LOW_RISK (0.993) | Fronteira ACCEPTABLE/WARNING, lado ≥80 |
| `boundary_acceptable_warning_low.csv` | 6 | 79.19 | WARNING | LOW_RISK (0.993) | Fronteira ACCEPTABLE/WARNING, lado <80 |
| `boundary_warning_critical_high.csv` | 6 | 45.17 | WARNING | MEDIUM_RISK (0.518) | Fronteira WARNING/CRITICAL, lado ≥45 |
| `boundary_warning_critical_low.csv` | 6 | 44.81 | CRITICAL | MEDIUM_RISK (0.512) | Fronteira WARNING/CRITICAL, lado <45 |
| `batch_sensor_low_risk.csv` | 100 | 94.25 | ACCEPTABLE | LOW_RISK (0.975) | Lote grande consistente (baixo risco) |
| `batch_sensor_medium_risk.csv` | 100 | 58.08 | WARNING | MEDIUM_RISK (0.807) | Lote grande consistente (risco médio) |
| `batch_sensor_high_risk.csv` | 100 | 0.0 | CRITICAL | HIGH_RISK (0.841) | Lote grande consistente (alto risco) |

### ⚠️ `bugs/` — Reproduzem divergências reais de cálculo (Upload HTTP 200, resultado suspeito)

| Arquivo | Linhas | Score | Classificação | Risco ML (confiança) | Bug reproduzido |
|---|---|---|---|---|---|
| `warning_zone.csv` | 5 | 69.48 | WARNING | LOW_RISK (0.98) | Bug #2 — WARNING + LOW_RISK no mesmo lote |
| `critical_zone.csv` | 5 | 0.0 | CRITICAL | MEDIUM_RISK (0.592) | Bug #1 — ML deveria prever HIGH_RISK |
| `single_sensor_out_temperature.csv` | 8 | 79.72 | WARNING | LOW_RISK (0.775) | Bug #1 — ML deveria prever MEDIUM_RISK |
| `three_sensors_out.csv` | 8 | 39.93 | CRITICAL | MEDIUM_RISK (0.67) | Bug #3 — ML deveria prever HIGH_RISK |
| `outlier_masked_by_average.csv` | 10 | 94.13 | ACCEPTABLE | LOW_RISK (0.995) | Bug #4 (o mais grave) — 1 leitura catastrófica mascarada pela média do lote |
| `rounding_boundary_inconsistency.csv` | 6 | 45.0 | **CRITICAL** | MEDIUM_RISK (0.512) | Bug #5 — score exibido "45.0" mas classificado CRITICAL |

### 🚀 `performance/` — Teste de carga

| Arquivo | Linhas | Resultado Esperado | Uso |
|---|---|---|---|
| `valid_large_500rows.csv` | 500 | Upload OK em < 5s | Teste de performance (SLA) |

### ❌ `rejected/` — Upload rejeitado (HTTP 400)

| Arquivo | Motivo da Rejeição |
|---|---|
| `invalid_empty.csv` | Arquivo sem conteúdo (0 bytes) |
| `invalid_missing_columns.csv` | Colunas `dissolved_oxygen`, `pressure`, `agitator_speed` ausentes |
| `invalid_wrong_types.csv` | Valores não numéricos nos campos de sensor |
| `invalid_out_of_range.csv` | Valores fora do range do DataValidator (temp=50, pH=12, etc.) |

---

## ⚠️ Bugs de Cálculo Encontrados (validados com o código real, 2026-07-19)

Os fixtures em `bugs/` reproduzem divergências reais entre o score determinístico
(`ComplianceService`) e a predição de ML (`MLModel`/`MLService`), e uma inconsistência de
arredondamento dentro do próprio `ComplianceService`. Todos foram confirmados rodando o código —
não são hipóteses.

1. **`single_sensor_out_temperature.csv` / `critical_zone.csv` — ML subestima o risco.**
   Um lote com 1 sensor fora da faixa aceitável (temperatura) dá WARNING no Compliance, mas o
   `MLModel` prevê **LOW_RISK** (confiança 0.775), contradizendo a própria regra de treino do
   modelo (`_generate_synthetic_labels`: 1 sensor fora ⇒ MEDIUM_RISK). Em `critical_zone.csv`
   (3-4 sensores fora, score 0.0 CRITICAL) o ML prevê **MEDIUM_RISK**, não HIGH_RISK.

2. **`warning_zone.csv` — mesma divergência, direção oposta.** Todos os sensores estão dentro
   da faixa *aceitável* mas fora da faixa *ideal* → Compliance classifica WARNING, mas nenhum
   sensor está "fora de faixa" pela definição do `MLModel` (`ACCEPTABLE_RANGES`), então o ML
   prevê corretamente **LOW_RISK** pela sua própria regra — só que isso produz a combinação
   confusa WARNING + LOW_RISK no mesmo lote. As duas classificações usam limites diferentes
   (ideal vs. aceitável) sem estarem alinhadas.

3. **`three_sensors_out.csv` — limite de 3+ sensores não é respeitado pelo ML.** Score 39.93
   CRITICAL (correto), mas o `MLModel` prevê MEDIUM_RISK com confiança baixa (0.67), quando
   deveria prever HIGH_RISK pela própria regra de rótulo do treino sintético.

4. **`outlier_masked_by_average.csv` — o bug mais grave.** `ComplianceService.calculate_compliance_score`
   faz a **média de todas as leituras do lote antes de pontuar** (linha `avg_value = sum(values) / len(values)`
   em `compliance_service.py`). Um lote com 9 leituras ideais e **1 leitura catastrófica**
   (temperatura 44°C — quase o dobro do limite ideal, mas ainda dentro do range aceito no
   upload pelo `DataValidator`, 20–45°C) é diluído para **score 94.13 · ACCEPTABLE · LOW_RISK
   (99.5% de confiança)**. A leitura perigosa desaparece completamente do resultado. Isso é
   exatamente o risco de "calcular o lote errado": um evento pontual de falha de processo pode
   ficar invisível na análise agregada.

5. **`rounding_boundary_inconsistency.csv` — score exibido não bate com a classificação.**
   `_classify_score` é chamado com o valor **não arredondado**, mas o score retornado ao
   chamador é `round(final_score, 2)`. Em `boundary_warning_critical_*` a fronteira normal
   funciona (45.17→WARNING, 44.81→CRITICAL), mas exatamente no fio da navalha (valor real
   ≈44.997, que arredonda para "45.0") o resultado é **score exibido "45.0" com classificação
   CRITICAL** — mesmo "45.0" que noutro lote classificaria WARNING (`score >= 45`). Como o
   score é o dado que alimenta o banco/projeto seguinte, dois lotes podem aparecer com o
   mesmo score "45.0" e classificações opostas.

**Recomendação**: antes de usar o banco de análises gerado como entrada de outro projeto, decidir
e corrigir: (a) se o `MLModel` deve ser re-treinado/ajustado para respeitar sua própria regra de
contagem de sensores fora de faixa, (b) se `ComplianceService` deve pontuar por pior leitura
além da média (ou registrar ambos), e (c) aplicar o arredondamento **antes** de classificar em
`_classify_score`, não depois.

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
print(score, classification, risk, confidence)
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
| Alerta de qualidade | `bugs/warning_zone.csv` | upload → compliance | 200 + WARNING |
| Falha crítica | `bugs/critical_zone.csv` | upload → compliance | 200 + CRITICAL |
| Performance (SLA < 5s) | `performance/valid_large_500rows.csv` | upload | 200 em < 5s |
| Rejeição — vazio | `rejected/invalid_empty.csv` | upload | 400 |
| Rejeição — schema | `rejected/invalid_missing_columns.csv` | upload | 400 |
| Rejeição — tipos | `rejected/invalid_wrong_types.csv` | upload | 400 |
| Rejeição — range | `rejected/invalid_out_of_range.csv` | upload | 400 |
| Fronteira ACCEPTABLE/WARNING | `control/boundary_acceptable_warning_high.csv` + `_low.csv` | compliance | 81.0 ACCEPTABLE vs 79.19 WARNING |
| Fronteira WARNING/CRITICAL | `control/boundary_warning_critical_high.csv` + `_low.csv` | compliance | 45.17 WARNING vs 44.81 CRITICAL |
| Divergência Compliance × ML | `bugs/single_sensor_out_temperature.csv`, `bugs/three_sensors_out.csv` | compliance + prediction | ver seção "Bugs de Cálculo Encontrados" |
| Outlier mascarado pela média do lote | `bugs/outlier_masked_by_average.csv` | compliance | ver "Bug #4" — não pode dar ACCEPTABLE |
| Inconsistência de arredondamento | `bugs/rounding_boundary_inconsistency.csv` | compliance | ver "Bug #5" — score "45.0" não pode ser CRITICAL |
