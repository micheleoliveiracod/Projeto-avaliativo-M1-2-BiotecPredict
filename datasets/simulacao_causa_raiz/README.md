# Dataset de Simulação — Causa-Raiz

Este dataset **não é** um fixture de teste do BiotecPredict. Ele existe para alimentar um
**agente de IA de análise de causa-raiz** (consumidor externo, referido no repositório como
*Root-Spector* — ver `backend/tests/fixtures/csv/README.md`) com lotes simulados que sejam
**factíveis de investigar**: cada lote de desvio tem uma causa física única e coerente, em vez de
vários parâmetros descontrolados ao mesmo tempo.

---

## ⚠️ Isto NÃO é a pasta de treino/validação

| Pasta | Propósito | Quem usa |
|---|---|---|
| [`backend/tests/fixtures/csv/`](../../backend/tests/fixtures/csv/) (14 arquivos em `control/`, mais `bugs/`, `rejected/`, `performance/`) | **Treino e validação dos métodos de cálculo** do próprio BiotecPredict — testar `ComplianceService`, `MLModel` e a API (pytest, Postman, E2E). Valores de score/classificação **travados e documentados** no README daquela pasta; alterar esses arquivos quebra CI. | Suite de testes do BiotecPredict |
| **`datasets/simulacao_causa_raiz/`** (esta pasta) | **Simulação de lotes de produção** com causa-raiz fisicamente plausível, para um agente externo de IA praticar diagnóstico de causa-raiz sobre a saída do BiotecPredict (score, classificação, risco). Não é fixture de teste e não trava nenhum comportamento do backend. | Agente de causa-raiz (projeto externo) |

Se você está mexendo no cálculo do BiotecPredict (`ComplianceService`, `MLModel`), a fonte da
verdade é `backend/tests/fixtures/csv/`, **não** esta pasta.

---

## Por que este dataset existe

Os fixtures de `control/` foram desenhados para testar a regra de classificação de risco do
BiotecPredict (quantos sensores rompem a faixa aceitável: 0 → LOW, 1–2 → MEDIUM, 3+ → HIGH) — por
isso arquivos como `four_sensors_out.csv` e `five_sensors_out.csv` colocam **todos os sensores
fora ao mesmo tempo**, e os lotes grandes (`batch_sensor_medium/high_risk.csv`) fazem os 5
parâmetros derivarem juntos e gradualmente. Isso é ótimo para testar o classificador, mas **não
reflete como um desvio real de bioprocesso acontece**: numa planta real, uma causa-raiz costuma
afetar 1, no máximo 2 ou 3 parâmetros — nunca os 5 ao mesmo tempo, e sempre respeitando as
correlações fisiológicas entre eles.

## Referências usadas para calibrar as correlações entre sensores

- [Aula 7 – Biorreatores: Tipos, Projeto e Operação](https://brasilead.com/wp-content/uploads/2026/01/Aula-7-Biorreatores-Tipos-Projeto-e-Operacao.pdf)
- [Biorreator Fermentador: A Revolução na Produção de Biocombustíveis e Produtos Sustentáveis](https://www.mecflu.com.br/blog/biorreator-fermentador-a-revolucao-na-producao-de-biocombustiveis-e-produtos-sustentaveis)

Padrão real confirmado nas referências e usado para desenhar os desvios:

- **Contaminação microbiana / meio de cultura ruim** → pH cai (ácidos do metabolismo do
  contaminante), temperatura sobe (calor extra do metabolismo) e OD cai (consumo extra de
  oxigênio) — os três **andam juntos** porque têm a mesma causa física. É o único cenário deste
  dataset com 3 sensores correlacionados.
- **Falha/configuração errada do agitador** → normalmente isolada (erro de operador no RPM);
  quando o RPM fica muito baixo, correlaciona com queda de OD (menos transferência de oxigênio -
  KLa), formando um par.
- **Falha de pH sozinha** → bomba de ácido/base com defeito ou setpoint errado.
- **Falha de temperatura sozinha** → jaqueta de aquecimento/resfriamento ou deriva de sensor.
- **Pressão** → geralmente ligada à válvula de contrapressão ou vedação, raramente correlacionada
  com os demais sensores.

## Como os dados foram gerados

Script: [`gerar_dataset.py`](gerar_dataset.py). Cada lote é uma série de leituras
(`temperature, ph, dissolved_oxygen, pressure, agitator_speed`, mesmo schema aceito pelo
`CSVProcessor` do BiotecPredict) que opera normal por um período, então o(s) sensor(es) da causa-
raiz fazem uma transição rápida até um valor de desvio e **persistem** nele até o fim do lote —
como uma falha real de equipamento que não se autocorrige sozinha. Isso é necessário porque o
`MLModel.predict()` real usa a **média do lote inteiro** por sensor como feature (não linha a
linha); um desvio que só aparece no fim do lote fica diluído na média e não é detectado — nada a
ver com um método de cálculo diferente, é só desenhar o dado bruto de forma realista o bastante
para o cálculo real do BiotecPredict, sem nenhuma alteração, conseguir enxergá-lo.

O script **não implementa nenhum cálculo de score/classificação/risco** — isso é feito
exclusivamente pelo código real e inalterado do BiotecPredict (`ComplianceService` e `MLModel`),
o mesmo usado para validar os fixtures de `backend/tests/fixtures/csv/`.

Para regenerar:

```bash
python datasets/simulacao_causa_raiz/gerar_dataset.py
```

---

## Arquivos gerados

Resultado obtido rodando cada CSV pelo `ComplianceService.calculate_compliance_score` +
`MLModel.predict` reais (mesmo procedimento de validação do
`backend/tests/fixtures/csv/README.md`), em 2026-07-19.

### ✅ Lotes aprovados (5) — sem desvio, só ruído normal de processo

| Arquivo | Linhas | Score | Classificação | Risco ML (confiança) |
|---|---|---|---|---|
| `aprovado_01_lote_ideal_alta_estabilidade.csv` | 60 | 98.91 | ACCEPTABLE | LOW_RISK (0.999) |
| `aprovado_02_lote_ideal_operacao_padrao.csv` | 60 | 98.91 | ACCEPTABLE | LOW_RISK (0.999) |
| `aprovado_03_lote_ideal_ciclo_longo.csv` | 96 | 98.86 | ACCEPTABLE | LOW_RISK (0.999) |
| `aprovado_04_lote_aceitavel_leve_variacao.csv` | 60 | 98.81 | ACCEPTABLE | LOW_RISK (0.999) |
| `aprovado_05_lote_aceitavel_borda_inferior.csv` | 60 | 96.83 | ACCEPTABLE | LOW_RISK (0.999) |

### ⚠️ Lotes com desvio (10) — cada um com UMA causa-raiz física plausível

| Arquivo | Causa-raiz simulada | Sensor(es) afetado(s) | Linhas | Score | Classificação | Risco ML (confiança) |
|---|---|---|---|---|---|---|
| `desvio_01_contaminacao_ph_temp_od.csv` | Contaminação microbiana / meio de cultura ruim | pH + temperatura + OD (cluster correlacionado) | 72 | 48.31 | WARNING | **HIGH_RISK** (0.559) |
| `desvio_02_bomba_dosadora_base_ph_alto.csv` | Falha na bomba dosadora de base (excesso de titulação) | pH (isolado) | 60 | 84.13 | ACCEPTABLE | MEDIUM_RISK (1.000) |
| `desvio_03_bomba_dosadora_acido_ph_baixo.csv` | Falha na bomba dosadora de ácido (excesso de titulação) | pH (isolado) | 60 | 84.53 | ACCEPTABLE | MEDIUM_RISK (0.947) |
| `desvio_04_falha_aquecimento_temp_alta.csv` | Falha no sistema de aquecimento (jaqueta térmica presa ligada) | temperatura (isolado) | 64 | 84.65 | ACCEPTABLE | MEDIUM_RISK (0.971) |
| `desvio_05_drift_sensor_temperatura.csv` | Deriva de calibração do sensor/controlador de temperatura (drift do termopar) | temperatura (isolado, subida lenta e gradual desde o início) | 68 | 83.96 | ACCEPTABLE | MEDIUM_RISK (0.971) |
| `desvio_06_agitador_rpm_baixo_od_baixo.csv` | Agitador configurado com RPM muito baixo | agitador + OD (par correlacionado — menos mistura/aeração) | 70 | 71.32 | WARNING | MEDIUM_RISK (0.946) |
| `desvio_07_agitador_rpm_alto_config_errada.csv` | Erro de configuração do operador (RPM acima do programado) | agitador (isolado) | 58 | 84.36 | ACCEPTABLE | MEDIUM_RISK (0.940) |
| `desvio_08_valvula_contrapressao_pressao_alta.csv` | Válvula de contrapressão travada/mal ajustada | pressão (isolado) | 62 | 84.56 | ACCEPTABLE | MEDIUM_RISK (1.000) |
| `desvio_09_vazamento_pressao_baixa.csv` | Vazamento na linha/vedação do reator | pressão (isolado) | 62 | 84.56 | ACCEPTABLE | MEDIUM_RISK (0.935) |
| `desvio_10_falha_aeracao_od_baixo_isolado.csv` | Falha no suprimento de ar (compressor/fluxo insuficiente na fonte de ar, não na agitação) | OD (isolado — agitador permanece normal) | 66 | 85.04 | ACCEPTABLE | MEDIUM_RISK (0.724) |

**Leitura do resultado:** `desvio_01` é o único cenário com 3 sensores fora — deliberado, é o caso
fisiológico real em que uma única causa (contaminação) move 3 parâmetros pela mesma razão. Pela
regra do BiotecPredict (3+ sensores fora = HIGH_RISK), ele corretamente classifica como HIGH_RISK.
Todos os outros 9 desvios — isolados ou pares fisicamente correlacionados — ficam em MEDIUM_RISK,
coerente com o padrão real: a maioria dos desvios de produção envolve 1 ou 2 parâmetros, não
todos.

## Como revalidar os resultados

```python
import csv, glob, os
from backend.services.compliance_service import ComplianceService
from backend.ml.model import MLModel

model = MLModel()
for fp in sorted(glob.glob("datasets/simulacao_causa_raiz/csv/*.csv")):
    with open(fp) as f:
        rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]
    score, classification = ComplianceService.calculate_compliance_score(rows)
    risk, confidence = model.predict(rows)
    print(os.path.basename(fp), score, classification, risk, confidence)
```
