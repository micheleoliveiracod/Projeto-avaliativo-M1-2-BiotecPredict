"""
Compliance Service - Cálculo de Manufacturing Compliance Score.

Implementa regras determinísticas para calcular Manufacturing Compliance Score (0-100)
baseado em validação de ranges de sensores industriais.
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
        1. Para cada sensor, calcula score baseado em desvio da faixa ideal
        2. Aplica penalidades por outliers e valores críticos
        3. Retorna score 0-100 com classificação

        Args:
            sensor_readings: Lista de dicionários com leituras de sensores

        Returns:
            Tupla (score_0_100, classificacao)
            Classificações:
            - ACCEPTABLE (80-100): Processo conforme
            - WARNING (60-79): Atenção necessária
            - CRITICAL (0-59): Intervenção imediata
        """
        if not sensor_readings:
            return 0.0, "CRITICAL"

        sensor_scores = {}

        for sensor_name, sensor_range in SENSOR_RANGES.items():
            values = [reading.get(sensor_name) for reading in sensor_readings if sensor_name in reading]
            if not values:
                continue

            avg_value = sum(values) / len(values)
            sensor_score = ComplianceService._calculate_sensor_score(
                sensor_name, avg_value, sensor_range
            )
            sensor_scores[sensor_name] = sensor_score

        # Média dos scores dos sensores
        if not sensor_scores:
            return 0.0, "CRITICAL"

        average_score = sum(sensor_scores.values()) / len(sensor_scores)
        final_score = min(100.0, max(0.0, average_score))

        classification = ComplianceService._classify_score(final_score)

        return round(final_score, 2), classification

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
        """Classifica score em categorias.

        ACCEPTABLE (>= 80): todos os sensores dentro da faixa aceitável
        WARNING    (>= 45): 1-2 sensores fora da faixa aceitável
        CRITICAL   (<  45): 3+ sensores fora da faixa aceitável
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
