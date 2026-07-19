"""
Gerador do dataset de simulacao para analise de causa-raiz.

Diferente de backend/tests/fixtures/csv/control/ (que sao fixtures de
TREINO/VALIDACAO do proprio motor de calculo do BiotecPredict, com scores
travados e documentados no README daquela pasta), os CSVs gerados aqui
simulam lotes de producao plausiveis: cada desvio tem UMA causa-raiz
fisica coerente, afetando apenas o(s) sensor(es) que essa causa afetaria
de verdade — nunca os 5 parametros ao mesmo tempo.

Referencias usadas para calibrar as correlacoes entre sensores:
- "Aula 7 - Biorreatores: Tipos, Projeto e Operacao"
  https://brasilead.com/wp-content/uploads/2026/01/Aula-7-Biorreatores-Tipos-Projeto-e-Operacao.pdf
- "Biorreator Fermentador: A Revolucao na Producao de Biocombustiveis e Produtos Sustentaveis"
  https://www.mecflu.com.br/blog/biorreator-fermentador-a-revolucao-na-producao-de-biocombustiveis-e-produtos-sustentaveis

Colunas geradas (mesmo schema aceito pelo CSVProcessor do BiotecPredict):
temperature, ph, dissolved_oxygen, pressure, agitator_speed

Faixas de referencia (backend/services/compliance_service.py):
  sensor            aceitavel        ideal
  temperature       20.0 - 30.0      24.0 - 26.0
  ph                6.5  - 7.5       6.8  - 7.2
  dissolved_oxygen  70.0 - 100.0     80.0 - 95.0
  pressure          4.5  - 6.0       4.8  - 5.5
  agitator_speed    200  - 300       240  - 280

Faixas do DataValidator (upload so aceita dentro destas — todo desvio
simulado fica DENTRO destes limites para o CSV nao ser rejeitado no
upload, mas FORA da faixa aceitavel do ComplianceService):
  temperature 20-45 | ph 4.0-9.0 | dissolved_oxygen 0-100 |
  pressure 0-10 | agitator_speed 0-500
"""
import csv
import random
from pathlib import Path

OUT_DIR = Path(__file__).parent / "csv"

IDEAL_CENTER = {
    "temperature": 25.0,
    "ph": 7.0,
    "dissolved_oxygen": 87.5,
    "pressure": 5.15,
    "agitator_speed": 260.0,
}

NOISE_STD = {
    "temperature": 0.15,
    "ph": 0.03,
    "dissolved_oxygen": 0.8,
    "pressure": 0.05,
    "agitator_speed": 3.0,
}

DECIMALS = {
    "temperature": 2,
    "ph": 3,
    "dissolved_oxygen": 2,
    "pressure": 3,
    "agitator_speed": 1,
}

COLUMNS = ["temperature", "ph", "dissolved_oxygen", "pressure", "agitator_speed"]


def _row(overrides, rng):
    values = {}
    for col in COLUMNS:
        center = IDEAL_CENTER[col]
        std = NOISE_STD[col]
        values[col] = rng.gauss(center, std)
    for col, target in overrides.items():
        values[col] = target
    return values


def gerar_lote(nome, n_linhas, seed, desvios=None, onset_fraction=0.2,
                ramp_fraction=0.18, descricao=""):
    """
    desvios: dict sensor -> valor_alvo_final. O sensor opera normal ate
    onset_fraction * n_linhas, faz a transicao (rampa linear curta) durante
    ramp_fraction * n_linhas, e entao PERSISTE no valor_alvo (com ruido)
    ate o fim do lote — como uma falha real de equipamento que comeca e
    nao se autocorrige. Isso mantem a media do lote inteiro (a feature que
    o MLModel real usa) deslocada de forma consistente, em vez de diluida
    por uma rampa que so termina desviada na ultima linha.
    Sensores fora de `desvios` permanecem com ruido normal o lote todo —
    isolando o sinal da causa-raiz para quem for analisar depois.
    """
    rng = random.Random(seed)
    onset_row = int(n_linhas * onset_fraction)
    ramp_len = max(1, int(n_linhas * ramp_fraction))
    ramp_end_row = onset_row + ramp_len
    desvios = desvios or {}

    rows = []
    for i in range(n_linhas):
        row = {}
        for col in COLUMNS:
            center = IDEAL_CENTER[col]
            std = NOISE_STD[col]
            if col in desvios and i >= onset_row:
                target = desvios[col]
                if i < ramp_end_row:
                    progress = (i - onset_row) / ramp_len
                    ramped_center = center + (target - center) * progress
                else:
                    ramped_center = target
                value = rng.gauss(ramped_center, std * 1.3)
            else:
                value = rng.gauss(center, std)
            row[col] = round(value, DECIMALS[col])
        rows.append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{nome}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"{nome}.csv ({n_linhas} linhas) - {descricao}")
    return path


def main():
    # ------------------------------------------------------------------
    # 10 DESVIOS — cada um com causa-raiz fisica unica e plausivel
    # ------------------------------------------------------------------
    gerar_lote(
        "desvio_01_contaminacao_ph_temp_od",
        n_linhas=72, seed=101, onset_fraction=0.12, ramp_fraction=0.12,
        desvios={"ph": 5.0, "temperature": 38.0, "dissolved_oxygen": 45.0},
        descricao="Contaminacao microbiana / meio de cultura ruim: metabolismo "
                   "do contaminante libera acidos (pH cai), gera calor extra "
                   "(temperatura sobe) e consome O2 (OD cai) — os 3 sensores "
                   "se movem JUNTOS porque tem a mesma causa fisica.",
    )
    gerar_lote(
        "desvio_02_bomba_dosadora_base_ph_alto",
        n_linhas=60, seed=102,
        desvios={"ph": 8.3},
        descricao="Falha na bomba dosadora de base (excesso de titulacao): "
                   "pH sobe isolado, demais sensores normais.",
    )
    gerar_lote(
        "desvio_03_bomba_dosadora_acido_ph_baixo",
        n_linhas=60, seed=103,
        desvios={"ph": 5.9},
        descricao="Falha na bomba dosadora de acido (excesso de titulacao): "
                   "pH cai isolado, demais sensores normais.",
    )
    gerar_lote(
        "desvio_04_falha_aquecimento_temp_alta",
        n_linhas=64, seed=104,
        desvios={"temperature": 34.0},
        descricao="Falha no sistema de aquecimento (jaqueta termica presa "
                   "ligada): temperatura sobe isolada, demais sensores normais.",
    )
    gerar_lote(
        "desvio_05_drift_sensor_temperatura",
        n_linhas=68, seed=105, onset_fraction=0.1, ramp_fraction=0.35,
        desvios={"temperature": 33.5},
        descricao="Deriva de calibracao do sensor/controlador de temperatura "
                   "(drift do termopar): subida mais lenta e gradual desde o "
                   "inicio do lote, isolada — diferencia falha de INSTRUMENTO "
                   "(este) de falha de ATUADOR (desvio_04).",
    )
    gerar_lote(
        "desvio_06_agitador_rpm_baixo_od_baixo",
        n_linhas=70, seed=106,
        desvios={"agitator_speed": 172.0, "dissolved_oxygen": 60.0},
        descricao="Agitador configurado com RPM muito baixo: reduz a "
                   "transferencia de oxigenio (KLa), entao agitator_speed e "
                   "dissolved_oxygen caem JUNTOS — par correlacionado por "
                   "mistura/aeracao insuficiente.",
    )
    gerar_lote(
        "desvio_07_agitador_rpm_alto_config_errada",
        n_linhas=58, seed=107,
        desvios={"agitator_speed": 340.0},
        descricao="Erro de configuracao do operador (RPM setado acima do "
                   "programado): agitator_speed sobe isolado, demais "
                   "sensores normais.",
    )
    gerar_lote(
        "desvio_08_valvula_contrapressao_pressao_alta",
        n_linhas=62, seed=108,
        desvios={"pressure": 6.8},
        descricao="Valvula de contrapressao travada/mal ajustada: pressao "
                   "sobe isolada, demais sensores normais.",
    )
    gerar_lote(
        "desvio_09_vazamento_pressao_baixa",
        n_linhas=62, seed=109,
        desvios={"pressure": 3.9},
        descricao="Vazamento na linha/vedacao do reator: pressao cai "
                   "isolada, demais sensores normais.",
    )
    gerar_lote(
        "desvio_10_falha_aeracao_od_baixo_isolado",
        n_linhas=66, seed=110,
        desvios={"dissolved_oxygen": 62.0},
        descricao="Falha no suprimento de ar (compressor/fluxo insuficiente "
                   "na fonte de ar, nao na agitacao): OD cai isolado, "
                   "agitator_speed permanece normal — diferencia esta causa "
                   "de desvio_06 (mistura insuficiente).",
    )

    # ------------------------------------------------------------------
    # 5 LOTES APROVADOS — sem desvio, so ruido normal de processo
    # ------------------------------------------------------------------
    gerar_lote(
        "aprovado_01_lote_ideal_alta_estabilidade",
        n_linhas=60, seed=201,
        descricao="Lote ideal, ruido de processo minimo (alta estabilidade).",
    )
    gerar_lote(
        "aprovado_02_lote_ideal_operacao_padrao",
        n_linhas=60, seed=202,
        descricao="Lote ideal, ruido de processo padrao.",
    )
    gerar_lote(
        "aprovado_03_lote_ideal_ciclo_longo",
        n_linhas=96, seed=203,
        descricao="Lote ideal, ciclo mais longo (mais leituras), mesma "
                   "estabilidade dos demais aprovados.",
    )
    gerar_lote(
        "aprovado_04_lote_aceitavel_leve_variacao",
        n_linhas=60, seed=204,
        descricao="Lote aceitavel: leve variacao dentro da faixa ideal, "
                   "sem romper faixa aceitavel em nenhum sensor.",
    )
    gerar_lote(
        "aprovado_05_lote_aceitavel_borda_inferior",
        n_linhas=60, seed=205,
        desvios={"dissolved_oxygen": 82.0, "agitator_speed": 248.0},
        onset_fraction=0.0,
        descricao="Lote aceitavel operando proximo a borda inferior do "
                   "ideal (ainda dentro do aceitavel) em OD e agitacao — "
                   "variacao normal de processo, nao desvio.",
    )


if __name__ == "__main__":
    main()
