"""
Compliance Service - Cálculo de Manufacturing Compliance Score.

Implementa regras determinísticas para calcular Manufacturing Compliance Score (0-100)
baseado em validação de ranges de sensores industriais.

Nota conceitual: este score mede QUALIDADE — o quão próximo cada sensor está do centro
da faixa ideal do processo (penaliza afastamento do ideal mesmo dentro da faixa aceitável).
Não conta quantos sensores romperam a faixa aceitável — isso é papel do MLModel/MLService
(backend/ml/model.py), que mede desvio do limite aceitável para sinalizar descarte do lote.
As duas métricas respondem perguntas diferentes ("quão boa está a produção" vs. "quantos
parâmetros de fato romperam o limite de aceite") e podem legitimamente divergir no mesmo
lote — ver backend/tests/fixtures/csv/README.md para exemplos reais.
"""

from typing import Dict, Tuple, List
from dataclasses import dataclass


@dataclass
class SensorRange:
    """Define range esperado para cada sensor."""
    min_value: float
    max_value: float
    ideal_min: float
    ideal_max: float


# Ranges esperados para cada sensor (baseado em dados de processo)
SENSOR_RANGES = {
    "temperature": SensorRange(min_value=20.0, max_value=30.0, ideal_min=24.0, ideal_max=26.0),
    "ph": SensorRange(min_value=6.5, max_value=7.5, ideal_min=6.8, ideal_max=7.2),
    "dissolved_oxygen": SensorRange(min_value=70.0, max_value=100.0, ideal_min=80.0, ideal_max=95.0),
    "pressure": SensorRange(min_value=4.5, max_value=6.0, ideal_min=4.8, ideal_max=5.5),
    "agitator_speed": SensorRange(min_value=200, max_value=300, ideal_min=240, ideal_max=280),
}


class ComplianceService:
    """Serviço para cálculo de Manufacturing Compliance Score."""

    @staticmethod
    def calculate_compliance_score(sensor_readings: List[Dict]) -> Tuple[float, str]:
        """
        Calcula Manufacturing Compliance Score baseado em sensor readings.

        Algoritmo:
        1. Para cada leitura individual, calcula o score de cada sensor (0-100)
        2. Para cada sensor, calcula a média dos scores de todas as leituras do lote
        3. Calcula a média entre sensores e retorna score 0-100 com classificação

        Nota: o score é calculado por leitura e só então agregado (média de scores),
        nunca pela média dos valores brutos antes de pontuar. Isso garante que uma
        leitura isolada com violação crítica (ex: 1 pico de temperatura fora da faixa
        ideal em um lote de leituras boas) sempre puxe o score do lote para baixo,
        em vez de ser diluída/invisível na média dos valores brutos.

        Args:
            sensor_readings: Lista de dicionários com leituras de sensores

        Returns:
            Tupla (score_0_100, classificacao)
            Classificações:
            - ACCEPTABLE (80-100): Processo conforme
            - WARNING (45-79): Atenção necessária
            - CRITICAL (0-44): Intervenção imediata
        """
        if not sensor_readings:
            return 0.0, "CRITICAL"

        sensor_scores = {}

        for sensor_name, sensor_range in SENSOR_RANGES.items():
            reading_scores = [
                ComplianceService._calculate_sensor_score(sensor_name, reading[sensor_name], sensor_range)
                for reading in sensor_readings
                if sensor_name in reading
            ]
            if not reading_scores:
                continue

            sensor_scores[sensor_name] = sum(reading_scores) / len(reading_scores)

        # Média dos scores dos sensores
        if not sensor_scores:
            return 0.0, "CRITICAL"

        average_score = sum(sensor_scores.values()) / len(sensor_scores)
        final_score = round(min(100.0, max(0.0, average_score)), 2)

        # Classifica o valor ja arredondado — evita que o score exibido (ex: "45.0")
        # divirja da classificacao por causa de casas decimais escondidas.
        classification = ComplianceService._classify_score(final_score)

        return final_score, classification

    @staticmethod
    def _calculate_sensor_score(sensor_name: str, value: float, sensor_range: SensorRange) -> float:
        """
        Calcula score para um sensor individual (0-100).

        Faixa ideal      → 90-100 (pequena penalidade por distância do centro)
        Faixa aceitável  → 60-90  (proporcional ao desvio do ideal)
        Fora da faixa    → 0      (violação crítica)
        """
        if sensor_range.ideal_min <= value <= sensor_range.ideal_max:
            distance_from_center = abs(value - (sensor_range.ideal_min + sensor_range.ideal_max) / 2)
            range_width = sensor_range.ideal_max - sensor_range.ideal_min
            deviation_ratio = distance_from_center / (range_width / 2) if range_width > 0 else 0
            score = 100 - (deviation_ratio * 10)
        elif sensor_range.min_value <= value <= sensor_range.max_value:
            if value < sensor_range.ideal_min:
                distance = sensor_range.ideal_min - value
                band = sensor_range.ideal_min - sensor_range.min_value
            else:
                distance = value - sensor_range.ideal_max
                band = sensor_range.max_value - sensor_range.ideal_max
            deviation_ratio = distance / band if band > 0 else 1.0
            score = 60 + (30 * (1 - min(1.0, deviation_ratio)))
        else:
            score = 0.0

        return max(0.0, score)

    @staticmethod
    def _classify_score(score: float) -> str:
        """Classifica score em categorias de qualidade do processo.

        O score é uma média contínua de proximidade do ideal por sensor (ver
        _calculate_sensor_score) — não uma contagem de sensores fora da faixa aceitável.
        Por isso um lote pode cair em CRITICAL com poucos sensores realmente fora (se os
        demais estiverem mal centrados dentro do aceitável), ou em WARNING sem nenhum
        sensor fora (se todos estiverem afastados do ideal). Para saber quantos sensores
        romperam a faixa aceitável — o sinal usado para decidir descarte do lote — use
        MLModel/MLService (backend/ml/model.py), não este método.

        ACCEPTABLE (>= 80): processo bem centrado no ideal
        WARNING    (>= 45): processo afastado do ideal, ainda operável
        CRITICAL   (<  45): qualidade do processo seriamente comprometida
        """
        if score >= 80:
            return "ACCEPTABLE"
        elif score >= 45:
            return "WARNING"
        else:
            return "CRITICAL"

    @staticmethod
    def get_sensor_metrics(sensor_readings: List[Dict]) -> Dict[str, Dict]:
        """
        Retorna métricas detalhadas por sensor.

        Útil para dashboard e análise.
        """
        metrics = {}

        for sensor_name, sensor_range in SENSOR_RANGES.items():
            values = [reading.get(sensor_name) for reading in sensor_readings if sensor_name in reading]
            if not values:
                continue

            metrics[sensor_name] = {
                "average": round(sum(values) / len(values), 2),
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "ideal_min": sensor_range.ideal_min,
                "ideal_max": sensor_range.ideal_max,
                "acceptable_min": sensor_range.min_value,
                "acceptable_max": sensor_range.max_value,
                "count": len(values),
            }

        return metrics

    @staticmethod
    def detect_anomalous_readings(sensor_readings: List[Dict]) -> Dict:
        """
        Detecta leituras individuais que romperam a faixa aceitável de algum sensor.

        Puramente informativo — não altera score nem classificação. Uma leitura fora
        da faixa aceitável pode ser um evento real do processo ou uma falha isolada
        do equipamento/sensor (não necessariamente do produto); cabe à investigação
        de causa raiz (ex: Root-Spector) distinguir as duas coisas a partir deste sinal,
        em vez do compliance score forçar essa decisão sozinho.

        Por que este método existe em vez de usar mediana no calculate_compliance_score:
        avaliamos usar a MEDIANA das notas por leitura (em vez da média) para o score,
        pensando em blindar o cálculo contra outliers. Na prática, é o oposto do que
        queremos aqui: a mediana tem breakdown point de ~50% (só se move quando mais da
        metade das leituras muda), então ela IGNORA completamente uma leitura catastrófica
        isolada — o mesmo mascaramento do bug original, só que pior (a média pelo menos dá
        peso proporcional 1/n ao outlier; a mediana dá peso zero). Testado com o fixture
        backend/tests/fixtures/csv/bugs/outlier_masked_by_average.csv (9 leituras ideais +
        1 catastrófica): a média das notas por leitura dá score 95.48, a mediana dá 97.48 —
        pior, não melhor. Por isso o score continua usando média (robusta o suficiente para
        não deixar 1 evento dominar sozinho, mas sensível o bastante para registrá-lo), e a
        detecção de outlier vira este sinal informativo separado, sem estatística nenhuma
        escondendo ou super-reagindo ao evento.

        Returns:
            {
                "total_readings": int,
                "readings_with_anomaly": int,
                "by_sensor": {sensor_name: quantidade_de_leituras_fora_do_aceitavel, ...}
            }
        """
        by_sensor = {name: 0 for name in SENSOR_RANGES}
        readings_with_anomaly = 0

        for reading in sensor_readings:
            reading_has_anomaly = False
            for sensor_name, sensor_range in SENSOR_RANGES.items():
                if sensor_name not in reading:
                    continue
                value = reading[sensor_name]
                if not (sensor_range.min_value <= value <= sensor_range.max_value):
                    by_sensor[sensor_name] += 1
                    reading_has_anomaly = True
            if reading_has_anomaly:
                readings_with_anomaly += 1

        return {
            "total_readings": len(sensor_readings),
            "readings_with_anomaly": readings_with_anomaly,
            "by_sensor": {name: count for name, count in by_sensor.items() if count > 0},
        }
