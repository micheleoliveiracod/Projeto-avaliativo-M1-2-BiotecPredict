# Guia de Interpretação de Resultados — BiotecPredict

Este documento explica como ler e interpretar o Dashboard da plataforma BiotecPredict: o que cada indicador significa, como é calculado, quais são os valores de referência, os três cenários de operação simulados e as observações identificadas durante os testes de validação.

---

## 1. O Dashboard

O Dashboard Analítico é a tela principal da plataforma. Ele consolida, em uma única visão, os resultados do processamento mais recente de leituras de sensores industriais. É atualizado automaticamente a cada 30 segundos e reflete sempre o **batch mais recente** enviado via upload de CSV.

O Dashboard é composto por quatro áreas:

| Área | O que exibe |
|---|---|
| **Compliance Score Card** | Pontuação 0–100 do batch e classificação (ACCEPTABLE / WARNING / CRITICAL) |
| **Predição de Risco Card** | Classificação de risco pelo modelo ML e percentual de confiança |
| **Variáveis de Sensores** | Valor médio de cada um dos 5 sensores, com barra de posição dentro da faixa aceitável e indicação visual (verde = dentro do range, vermelho = fora) |
| **Histórico de Batches** | Tabela com todos os batches já processados, filtráveis por status, score e período |

> **Como usar:** após o upload de um CSV via página de Upload, o Dashboard é atualizado automaticamente. Os dois cards de KPI mostram o diagnóstico imediato; a seção de sensores detalha qual variável específica gerou o desvio.

---

## 2. Sensores Monitorados e Faixas de Referência

O sistema monitora cinco variáveis de processo em cada leitura de sensor. Para cada variável existem duas faixas definidas no backend (`backend/services/compliance_service.py`):

- **Faixa ideal**: condição de operação ótima. Valores nessa faixa recebem pontuação máxima no Compliance Score (90–100 pontos).
- **Faixa aceitável**: condição de operação tolerada. Valores dentro desta faixa mas fora do ideal recebem pontuação parcial (60–90 pontos). Valores **fora** desta faixa recebem 0 pontos e são sinalizados em vermelho no Dashboard.

| Variável | Faixa Aceitável | Faixa Ideal | Unidade |
|---|---|---|---|
| Temperatura | 20 – 30 | 24 – 26 | °C |
| pH | 6,5 – 7,5 | 6,8 – 7,2 | adimensional |
| Oxigênio Dissolvido | 70 – 100 | 80 – 95 | % |
| Pressão | 4,5 – 6,0 | 4,8 – 5,5 | bar |
| Velocidade do Agitador | 200 – 300 | 240 – 280 | RPM |

> **Por que dois limites?** A faixa aceitável delimita os limites físico-químicos dentro dos quais o processo ainda é viável. A faixa ideal representa as condições de máxima eficiência e menor risco de contaminação ou perda de rendimento. Operar na faixa aceitável mas fora do ideal ainda gera pontuação positiva, mas indica que o processo está se afastando das condições ótimas.

### Como os indicadores visuais funcionam

Cada sensor no Dashboard exibe uma barra de posição. O cálculo da largura da barra e a cor de preenchimento são baseados diretamente na **faixa aceitável**:

| Sensor | Barra zerada em | Barra cheia em | Verde se |
|---|---|---|---|
| Temperatura | 20°C | 30°C | 20 ≤ valor ≤ 30 |
| pH | 6,5 | 7,5 | 6,5 ≤ valor ≤ 7,5 |
| O₂ Dissolvido | 70% | 100% | 70 ≤ valor ≤ 100 |
| Pressão | 4,5 bar | 6,0 bar | 4,5 ≤ valor ≤ 6,0 |
| Agitador | 200 RPM | 300 RPM | 200 ≤ valor ≤ 300 |

Um valor fora desse intervalo exibe a barra em **vermelho** — mesmo que o valor exista fisicamente. Por exemplo, temperatura de 33°C é um valor real e mensurável, mas está acima do limite aceitável de 30°C e aparece em vermelho.

> **Implementação:** `frontend/src/components/Dashboard/Dashboard.tsx` — seção "Variáveis de Sensores".

---

## 3. Manufacturing Compliance Score

### O que é

O Compliance Score é um indicador **determinístico** (baseado em regras matemáticas fixas, sem aprendizado) que expressa de forma quantitativa quão próximos os valores médios dos sensores estão das condições ideais de operação. O resultado é um número de **0 a 100**.

Determinístico significa que, dados os mesmos valores de sensor, o score será sempre o mesmo — sem variação aleatória.

### Como é calculado

O cálculo ocorre em duas etapas. A implementação está em `backend/services/compliance_service.py`.

**Etapa 1 — Pontuação individual por sensor**

Para cada sensor, calcula-se a média de todas as leituras do batch. Em seguida, aplica-se a tabela de pontuação:

| Situação do valor médio | Pontuação |
|---|---|
| Dentro da faixa **ideal** | 90 a 100 pontos — quanto mais próximo do centro da faixa, maior |
| Dentro da faixa **aceitável**, fora do ideal | 60 a 90 pontos — proporcional à distância do limite ideal |
| **Fora** da faixa aceitável | 0 pontos |

Fórmulas aplicadas:

```
# Dentro do ideal:
desvio_relativo = distância_do_centro / (largura_ideal / 2)
score = 100 − (desvio_relativo × 10)          → máximo −10 pontos

# Dentro do aceitável, fora do ideal:
desvio_relativo = distância_do_limite_ideal / largura_da_banda
score = 60 + (30 × (1 − desvio_relativo))     → entre 60 e 90 pontos

# Fora do aceitável:
score = 0
```

**Etapa 2 — Score final**

```
Score Final = Média das pontuações individuais dos 5 sensores
```

O valor é limitado entre 0 e 100.

> **Nota sobre o cálculo:** Uma versão anterior do código aplicava uma penalidade adicional de −20 pontos por sensor fora da faixa, sobre os sensores que já recebiam score 0. Isso causava dupla penalização e distorcia o score de cenários de risco médio (2 sensores fora) para CRITICAL. Esse bug foi identificado, documentado e corrigido — ver [`docs/prompts/03-refatoracao.md`](prompts/03-refatoracao.md), Refatoração 2.

### Classificações

| Score | Classificação | Significado operacional |
|---|---|---|
| 80 – 100 | **ACCEPTABLE** | Todos os sensores dentro da faixa aceitável. Processo em condição normal. |
| 45 – 79 | **WARNING** | 1 a 2 sensores fora da faixa aceitável. Atenção e investigação recomendadas. |
| 0 – 44 | **CRITICAL** | 3 ou mais sensores fora da faixa. Intervenção imediata necessária. |

> **Por que o limiar de WARNING é 45 e não 60?** Com 2 dos 5 sensores fora da faixa (score 0 cada um), a média dos 5 sensores chega a aproximadamente 57–60. Um limiar de WARNING em 60 tornaria esse cenário CRITICAL, o que seria semanticamente incorreto para um problema que afeta apenas 2 de 5 variáveis. O limiar 45 garante que cenários com 1–2 sensores fora sejam corretamente classificados como WARNING.

### O que o Score indica na prática

Um Score alto (≥ 80) significa que todos os cinco sensores estão operando próximos às condições ideais. Um Score baixo indica que um ou mais parâmetros estão se desviando — quanto menor o valor, mais grave e abrangente é o desvio. O Score é útil para **rastrear a qualidade histórica** de batches e identificar tendências de degradação ao longo do tempo.

---

## 4. Predição de Risco (Machine Learning)

### O que é

A Predição de Risco é um indicador **probabilístico**, gerado por um modelo de Machine Learning (RandomForestClassifier, implementado em `backend/ml/model.py`). Diferente do Compliance Score, o modelo **aprende padrões** a partir de dados históricos sintéticos e generaliza esse aprendizado para classificar novos batches.

O resultado é uma **classe de risco** (LOW_RISK, MEDIUM_RISK ou HIGH_RISK) acompanhada de um **percentual de confiança** — a probabilidade que o modelo atribui à classe predita.

### Como é calculado

O modelo recebe como entrada a **média de cada sensor** ao longo de todas as leituras do batch (5 valores numéricos no total) e retorna a classe de maior probabilidade segundo o ensemble de 100 árvores de decisão.

```
Entrada: [avg_temperatura, avg_ph, avg_do, avg_pressão, avg_agitador]
Saída:   (classe_de_risco, confiança_0_a_1)
```

O critério aprendido pelo modelo reflete o número de sensores com valores fora da faixa aceitável:

| Sensores fora da faixa | Classe | Confiança típica observada |
|---|---|---|
| 0 | **LOW_RISK** | ~97% |
| 1 a 2 | **MEDIUM_RISK** | ~80% |
| 3 ou mais | **HIGH_RISK** | ~84% |

> **O que significa a confiança?** É a fração de árvores do RandomForest que votaram na classe predita. Confiança de 84% significa que 84 de 100 árvores concordaram com a classificação. Não é uma medida de conformidade do processo — é a certeza do modelo sobre sua própria predição.

### Treinamento do modelo

O modelo é treinado com dados sintéticos gerados na inicialização, quando nenhum modelo salvo é encontrado (`backend/ml/models/`). O conjunto de treino é composto por:

| Classe | Composição | Proporção |
|---|---|---|
| LOW_RISK | Todos os sensores dentro da faixa aceitável | 50% |
| MEDIUM_RISK | Metade com 1 sensor fora, metade com 2 | 30% |
| HIGH_RISK | Distribuído entre 3, 4 e 5 sensores fora | 20% |

> **Por que essa distribuição?** Uma versão anterior do modelo treinava MEDIUM_RISK com apenas 1 sensor fora e HIGH_RISK com exatamente 3, criando um gap no espaço de features para cenários com 2 ou 4–5 sensores fora da faixa. Isso prejudicava a confiança nas predições dos CSVs de teste. O gap foi identificado nos testes de validação e corrigido — ver [`docs/prompts/03-refatoracao.md`](prompts/03-refatoracao.md), Refatoração 2.

### Classificações e ação recomendada

| Classificação | Significado | Ação recomendada |
|---|---|---|
| **LOW_RISK** | Processo dentro dos parâmetros esperados. | Manter monitoramento contínuo. Prosseguir conforme planejado. |
| **MEDIUM_RISK** | 1 a 2 parâmetros fora da faixa aceitável. Desvios moderados. | Aumentar frequência de leituras. Investigar causa dos desvios. Considerar ajuste de parâmetros. |
| **HIGH_RISK** | 3 ou mais parâmetros fora da faixa. Risco significativo de falha. | Intervenção imediata. Revisar todos os parâmetros. Alertar supervisor. Considerar interrupção do batch. |

### Diferença em relação ao Compliance Score

O Compliance Score mede **quão distante** os valores estão do ideal (intensidade do desvio). A Predição de Risco mede **quantos parâmetros** estão fora de controle (abrangência do problema). Os dois indicadores são complementares e devem ser lidos juntos.

---

## 5. Interpretação Combinada dos Indicadores

| Compliance Score | Predição de Risco | Interpretação |
|---|---|---|
| 80 – 100 (ACCEPTABLE) | LOW_RISK | Processo ideal. Todos os parâmetros controlados. |
| 80 – 100 (ACCEPTABLE) | MEDIUM_RISK | Parâmetros na faixa aceitável, mas próximos dos limites. Monitorar. |
| 45 – 79 (WARNING) | MEDIUM_RISK | 1–2 parâmetros com desvio em desenvolvimento. Ação corretiva preventiva. |
| 0 – 44 (CRITICAL) | MEDIUM_RISK | 1–2 parâmetros com desvio severo. Correção necessária. |
| 0 – 44 (CRITICAL) | HIGH_RISK | Falha múltipla. Intervenção imediata. Risco de perda do batch. |

---

## 6. Cenários de Teste Simulados

Os três arquivos CSV abaixo foram criados para validar o comportamento do sistema e demonstrar os três cenários de operação. Eles estão disponíveis em:

```
backend/
└── tests/
    └── fixtures/
        └── csv/
            ├── batch_sensor_low_risk.csv     ← Cenário 1: operação normal
            ├── batch_sensor_medium_risk.csv  ← Cenário 2: alerta de processo
            └── batch_sensor_high_risk.csv    ← Cenário 3: falha crítica
```

Cada arquivo contém 100 linhas de leituras de sensores, com os valores evoluindo progressivamente ao longo do tempo para simular a dinâmica real de um bioprocesso.

---

### Cenário 1 — Operação Normal (`batch_sensor_low_risk.csv`)

Simula um batch estável, com todos os sensores dentro das faixas ideais ou próximos delas. O oxigênio dissolvido começa mais alto e declina levemente ao longo do processo — comportamento normal em fermentações fed-batch, reflexo do consumo metabólico crescente.

| Sensor | Média | Faixa | Situação |
|---|---|---|---|
| Temperatura | ~25,0°C | Ideal: 24–26°C | Dentro do ideal |
| pH | ~7,09 | Ideal: 6,8–7,2 | Dentro do ideal |
| Oxigênio Dissolvido | ~77% | Aceitável: 70–100% | Dentro da faixa aceitável, abaixo do ideal |
| Pressão | ~5,2 bar | Ideal: 4,8–5,5 bar | Dentro do ideal |
| Velocidade do Agitador | ~261 RPM | Ideal: 240–280 RPM | Dentro do ideal |

**Resultado obtido nos testes:**

| Indicador | Valor | Classificação |
|---|---|---|
| Compliance Score | 93,78 | ACCEPTABLE |
| Predição de Risco | LOW_RISK | Confiança: 97,5% |

**Interpretação:** Processo estável. O único sensor fora da faixa ideal é o oxigênio dissolvido (77%, abaixo do ideal de 80–95%), o que é esperado nesse tipo de processo. O Score alto (93,78) confirma que o desvio é leve e não compromete a operação.

---

### Cenário 2 — Alerta de Processo (`batch_sensor_medium_risk.csv`)

Simula falha progressiva no sistema de refrigeração (temperatura subindo de ~28°C para ~35°C ao longo do batch) combinada com esgotamento do buffer de pH (pH derivando de ~7,3 para ~8,2). Os demais sensores permanecem estáveis dentro das faixas ideais.

| Sensor | Média | Faixa | Situação |
|---|---|---|---|
| Temperatura | ~31,5°C | Aceitável: 20–30°C | **Fora da faixa aceitável** (máx. 30°C) |
| pH | ~7,75 | Aceitável: 6,5–7,5 | **Fora da faixa aceitável** (máx. 7,5) |
| Oxigênio Dissolvido | ~83% | Ideal: 80–95% | Dentro do ideal |
| Pressão | ~5,1 bar | Ideal: 4,8–5,5 bar | Dentro do ideal |
| Velocidade do Agitador | ~258 RPM | Ideal: 240–280 RPM | Dentro do ideal |

**Resultado obtido nos testes:**

| Indicador | Valor | Classificação |
|---|---|---|
| Compliance Score | 58,17 | WARNING |
| Predição de Risco | MEDIUM_RISK | Confiança: 80,7% |

**Interpretação:** Dois parâmetros saíram da faixa aceitável, o que classifica o batch como MEDIUM_RISK. O Score 58 (WARNING) reflete que 2 dos 5 sensores falharam, mas os outros 3 estão em condição ideal, o que eleva a média. Ação recomendada: verificar sistema de refrigeração e reposição de tampão de pH. O processo ainda pode ser recuperado sem interrupção do batch se a intervenção for rápida.

> **Nota:** uma versão anterior do código retornava score ~18 (CRITICAL) para este cenário, devido a uma dupla penalização no cálculo do Compliance Score — bug identificado, documentado e corrigido. Ver [`docs/prompts/03-refatoracao.md`](prompts/03-refatoracao.md), Refatoração 2.

---

### Cenário 3 — Falha Crítica (`batch_sensor_high_risk.csv`)

Simula falha múltipla e progressiva: superaquecimento (temperatura chegando a ~42°C), alcalinização crítica (pH chegando a ~8,9), queda severa de oxigênio dissolvido (células em hipóxia, DO caindo a ~35%), pressão abaixo do mínimo operacional e agitação insuficiente para manutenção da homogeneidade do biorreator.

| Sensor | Média | Faixa | Situação |
|---|---|---|---|
| Temperatura | ~37,5°C | Aceitável: 20–30°C | **Fora da faixa aceitável** |
| pH | ~8,50 | Aceitável: 6,5–7,5 | **Fora da faixa aceitável** |
| Oxigênio Dissolvido | ~49,7% | Aceitável: 70–100% | **Fora da faixa aceitável** |
| Pressão | ~3,91 bar | Aceitável: 4,5–6,0 bar | **Fora da faixa aceitável** |
| Velocidade do Agitador | ~157 RPM | Aceitável: 200–300 RPM | **Fora da faixa aceitável** |

**Resultado obtido nos testes:**

| Indicador | Valor | Classificação |
|---|---|---|
| Compliance Score | 0,00 | CRITICAL |
| Predição de Risco | HIGH_RISK | Confiança: 84,1% |

**Interpretação:** Todos os cinco parâmetros estão fora da faixa aceitável. O processo entrou em colapso operacional. Com oxigênio dissolvido em ~50%, as células estão em condição de hipóxia severa, comprometendo rendimento e viabilidade celular. Intervenção imediata e interrupção controlada do batch são recomendadas para evitar contaminação e perda total do lote.

---

## 7. Observações de Validação

As observações abaixo foram identificadas durante os testes de validação com os três CSVs de simulação. Elas descrevem comportamentos do sistema que podem surpreender ou exigir atenção durante o uso.

### 7.1 — Sensor no limite exato da faixa aceitável classifica como WARNING

**Observação:** Quando todos os sensores são enviados exatamente no valor mínimo aceitável (ex: temperatura=20°C, pH=6,5, DO=70%...), o Compliance Score retorna **60** e a classificação é **WARNING**, não ACCEPTABLE.

**Por quê:** O score 60 é o resultado esperado quando um sensor está no limite da faixa aceitável — é o piso da banda "aceitável mas fora do ideal". Como 60 está abaixo do limiar de ACCEPTABLE (80), o resultado é WARNING. Isso é semanticamente correto: operar exatamente no limite mínimo não é uma condição ideal.

**Implicação para o operador:** Um batch com sensores exatamente nos limites vai aparecer como WARNING no dashboard. Isso é intencional — é um sinal para ajustar o processo antes que os valores cruzem para fora da faixa.

---

### 7.2 — A confiança não mede a saúde do processo — mede a certeza do modelo

**Observação:** O modelo retorna confiança de **97,5%** para LOW_RISK e **84,1%** para HIGH_RISK. À primeira leitura, pode parecer estranho: se o processo está em colapso total (todos os 5 sensores fora da faixa), por que a confiança não é 100%? E por que o HIGH_RISK tem confiança menor do que o LOW_RISK?

**A confiança não mede o quão ruim está o processo. Mede o quanto o modelo tem certeza da sua própria resposta.**

O modelo faz uma pergunta internamente: *"qual das três classes melhor descreve este batch?"* As 100 árvores do RandomForest votam. A confiança é o percentual de votos que a classe vencedora recebeu:

```
HIGH RISK CSV → 84 de 100 árvores votaram HIGH_RISK
                → predição: HIGH_RISK, confiança: 84%
```

Isso significa: o modelo tem 84% de certeza de que o batch é HIGH_RISK — não que o processo está 84% bom ou 84% ruim.

**Por que a confiança do HIGH_RISK (84%) é menor que a do LOW_RISK (97%)?**

O LOW_RISK é um cenário homogêneo e muito bem representado no treino (50% das amostras): todos os sensores dentro da faixa, valores próximos do centro. O modelo viu muitos exemplos parecidos, então 97 das 100 árvores concordam sem dificuldade.

O HIGH_RISK cobre uma variedade maior de situações — pode ter 3, 4 ou 5 sensores fora, com diferentes combinações e magnitudes de desvio. O modelo viu menos exemplos dessa classe (20% do treino) e mais diversidade interna, então algumas árvores ficam em dúvida entre HIGH_RISK e MEDIUM_RISK. Por isso 84%, não 97%.

**Como ler os dois números juntos — guia rápido:**

| CSV | Compliance Score | Predição | Confiança | Leitura correta |
|---|---|---|---|---|
| Low Risk | 93,78 | LOW_RISK | 97,5% | Processo saudável. Modelo muito certo disso. |
| Medium Risk | 58,17 | MEDIUM_RISK | 80,7% | Processo com desvios. Modelo bastante certo. |
| High Risk | 0,00 | HIGH_RISK | 84,1% | Processo em colapso. Modelo bastante certo. |

O **Compliance Score** (0 a 100) é que mede a saúde do processo. A **confiança** (%) mede apenas a certeza interna do modelo sobre a classificação que ele escolheu. São métricas independentes — um processo péssimo pode ter confiança alta na predição justamente porque o modelo o reconhece claramente como HIGH_RISK.

---

### 7.3 — Score e Predição contam histórias complementares, não idênticas

**Observação:** É possível ver Compliance Score em **WARNING** com Predição **MEDIUM_RISK** (cenário 2), ou Score **0** com Predição **HIGH_RISK** (cenário 3). Esses resultados não se contradizem — medem dimensões diferentes do mesmo problema.

**Guia rápido de leitura conjunta:**

| O que você vê | O que significa |
|---|---|
| Score ACCEPTABLE + LOW_RISK | Processo saudável. Tudo dentro dos limites. |
| Score WARNING + MEDIUM_RISK | 1–2 sensores fora. Investigar. Processo recuperável. |
| Score CRITICAL + HIGH_RISK | 3+ sensores fora. Intervenção imediata. |
| Score CRITICAL + MEDIUM_RISK | 1–2 sensores muito fora, com desvio severo. Ação corretiva urgente. |

---

### 7.4 — Indicadores visuais dos sensores usam faixas aceitáveis, não faixas de display

**Observação:** Uma versão anterior do frontend exibia os sensores com ranges de visualização muito mais amplos do que as faixas de aceitação do processo (ex: temperatura 0–45°C em vez de 20–30°C). Isso fazia com que **todos os sensores sempre aparecessem em verde**, mesmo para dados de alto risco — tornando os indicadores visuais inúteis como ferramenta de diagnóstico.

**Correção aplicada:** Os ranges visuais foram alinhados às faixas aceitáveis do backend. Agora, um sensor em verde confirma que o valor está dentro da especificação; em vermelho, indica violação — consistente com o que o Compliance Score calcula.

**Referência técnica:** [`docs/prompts/03-refatoracao.md`](prompts/03-refatoracao.md), Refatoração 2 — documentação completa dos bugs identificados e das correções aplicadas com Claude Code.

---

## 8. Limitações dos Indicadores

- **Compliance Score usa médias:** um batch com valores alternando entre extremos pode ter média aceitável mas operação instável. Analisar também os valores mínimo e máximo de cada sensor via endpoint `/api/v1/batch/{id}/sensors`.
- **Predição de Risco é treinado com dados sintéticos:** o modelo representa padrões gerais de bioprocessos e pode ter precisão limitada em cenários muito específicos ou com combinações de sensores não representadas no treino.
- **Ambos os indicadores refletem o momento do upload:** não capturam desvios que ocorram após o envio do arquivo. Para monitoramento contínuo, reenvie o arquivo periodicamente ou integre a API diretamente ao sistema de aquisição de dados.

### 8.1 — Divergências de cálculo confirmadas (2026-07-19), ainda sem correção aplicada

Validando o código real com fixtures dedicadas, foram confirmadas 5 divergências entre
`ComplianceService` e `MLModel`/`MLService` (não hipóteses — reproduzidas rodando o código):
ML previsto abaixo do esperado para lotes com 1 ou 3 sensores fora da faixa aceitável, combinação
WARNING + LOW_RISK no mesmo lote, uma leitura catastrófica mascarada pela média do lote (score
94.13 · ACCEPTABLE mesmo com 1 leitura de temperatura quase o dobro do limite ideal), e uma
inconsistência de arredondamento onde o mesmo score exibido "45.0" pode classificar como WARNING
ou CRITICAL dependendo do valor não arredondado. Detalhes, valores exatos e os CSVs de reprodução
de cada caso: [`backend/tests/fixtures/csv/README.md`](../backend/tests/fixtures/csv/README.md),
seção "Bugs de Cálculo Encontrados".
- **O modelo ML é retreinado do zero a cada inicialização do backend** quando os arquivos `.pkl` não existem: o comportamento pode variar levemente entre deploys. Para resultados reproduzíveis, versione os arquivos `backend/ml/models/risk_predictor.pkl` e `scaler.pkl`.
