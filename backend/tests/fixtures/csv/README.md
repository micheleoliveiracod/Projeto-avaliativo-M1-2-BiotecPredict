# Fixtures CSV — BiotecPredict

Arquivos CSV para uso nos testes **pytest**, **Postman** e **E2E** do projeto.

**Localização**: `backend/tests/fixtures/csv/`  
**Base URL para Postman/E2E**: `http://localhost:8001/api/v1/upload`

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

### ✅ Válidos — Upload aceito (HTTP 200)

| Arquivo | Linhas | Resultado Esperado | Uso |
|---|---|---|---|
| `valid_ideal.csv` | 10 | Upload OK · ACCEPTABLE · LOW_RISK | Caso feliz (golden path) |
| `valid_acceptable.csv` | 8 | Upload OK · ACCEPTABLE (score ~75-85) | Cenário aceitável mas não ideal |
| `valid_boundary.csv` | 4 | Upload OK · Compliance baixo | Valores nos limites do DataValidator |
| `warning_zone.csv` | 5 | Upload OK · **WARNING** · MEDIUM_RISK | Valores aceitos mas fora do range ideal do Compliance |
| `critical_zone.csv` | 5 | Upload OK · **CRITICAL** · HIGH_RISK | Valores aceitos mas fora do range aceitável do Compliance |
| `valid_large_500rows.csv` | 500 | Upload OK em < 5s | Teste de performance |

### ❌ Inválidos — Upload rejeitado (HTTP 400)

| Arquivo | Motivo da Rejeição |
|---|---|
| `invalid_empty.csv` | Arquivo sem conteúdo (0 bytes) |
| `invalid_missing_columns.csv` | Colunas `dissolved_oxygen`, `pressure`, `agitator_speed` ausentes |
| `invalid_wrong_types.csv` | Valores não numéricos nos campos de sensor |
| `invalid_out_of_range.csv` | Valores fora do range do DataValidator (temp=50, pH=12, etc.) |

---

## Como Usar

### pytest
```python
from pathlib import Path

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "csv"

def test_upload_ideal(client):
    csv_path = FIXTURES / "valid_ideal.csv"
    files = {"file": ("valid_ideal.csv", open(csv_path, "rb"), "text/csv")}
    r = client.post("/api/v1/upload", files=files)
    assert r.status_code == 200
```

### Postman
1. No request `Upload CSV Válido`, selecione o arquivo em **Body → form-data → file**
2. Use `valid_ideal.csv` para o fluxo principal
3. Use `invalid_empty.csv` para testar a resposta 400

### E2E (Playwright)
```typescript
await page.setInputFiles('input[type="file"]', 'backend/tests/fixtures/csv/valid_ideal.csv');
await page.click('button[type="submit"]');
await expect(page.locator('.compliance-score')).toBeVisible();
```

---

## Cenários de Teste Recomendados

| Cenário | Arquivo | Endpoint | Expectativa |
|---|---|---|---|
| Golden path completo | `valid_ideal.csv` | upload → compliance → prediction | 200 + ACCEPTABLE + LOW_RISK |
| Alerta de qualidade | `warning_zone.csv` | upload → compliance | 200 + WARNING |
| Falha crítica | `critical_zone.csv` | upload → compliance | 200 + CRITICAL |
| Performance (SLA < 5s) | `valid_large_500rows.csv` | upload | 200 em < 5s |
| Rejeição — vazio | `invalid_empty.csv` | upload | 400 |
| Rejeição — schema | `invalid_missing_columns.csv` | upload | 400 |
| Rejeição — tipos | `invalid_wrong_types.csv` | upload | 400 |
| Rejeição — range | `invalid_out_of_range.csv` | upload | 400 |
