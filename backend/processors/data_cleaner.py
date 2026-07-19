"""
Data Cleaner - Limpeza de dados (nulos) e detecção de outliers (sem remover).

Responsabilidades:
- Remover valores nulos (dado ausente não pode ser pontuado)
- Detectar outliers estatísticos (z-score) — apenas para fins informativos, sem excluir a leitura

Nota: outliers NÃO são removidos do lote. Uma leitura estatisticamente destoante pode ser um
evento real de processo (ex: pico de temperatura por falha de equipamento) que precisa aparecer
no score e no histórico, não desaparecer silenciosamente antes de ser salva no banco. Quem precisa
saber "isso pode ser ruído de sensor" usa ComplianceService.detect_anomalous_readings() (baseado
em faixa aceitável, não em z-score) sobre os dados já persistidos — ver
backend/tests/fixtures/csv/README.md, seção "Bugs de Cálculo — Corrigidos".
"""

from typing import List, Dict, Any
import statistics


class DataCleaner:
    """Limpa dados de sensores removendo nulos e outliers."""

    @staticmethod
    def remove_nulls(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remover linhas com valores nulos.

        Args:
            rows: Lista de dicionários

        Returns:
            Lista sem linhas com nulos
        """
        return [row for row in rows if all(v is not None for v in row.values())]

    @staticmethod
    def detect_outliers(
        rows: List[Dict[str, Any]], threshold: float = 2.0
    ) -> tuple[List[Dict[str, Any]], List[int]]:
        """
        Detecta (sem remover) leituras estatisticamente destoantes por desvio padrão (z-score).

        Args:
            rows: Lista de dicionários
            threshold: Número de desvios padrão (padrão: 2.0)

        Returns:
            Tupla (rows, indices_outliers) — rows é retornado inalterado; quem chama decide
            o que fazer com os índices (aqui, apenas registrar em warnings).
        """
        if len(rows) < 2:
            return rows, []

        outlier_indices = []
        numeric_fields = ["temperature", "ph", "dissolved_oxygen", "pressure", "agitator_speed"]

        for field in numeric_fields:
            values = [row[field] for row in rows if field in row]
            if len(values) < 2:
                continue

            mean = statistics.mean(values)
            stdev = statistics.stdev(values)

            for idx, row in enumerate(rows):
                if field in row:
                    z_score = abs((row[field] - mean) / stdev) if stdev > 0 else 0
                    if z_score > threshold:
                        outlier_indices.append(idx)

        outlier_indices = sorted(set(outlier_indices))

        return rows, outlier_indices

    @staticmethod
    def clean(rows: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[str]]:
        """
        Executar limpeza: remove nulos, apenas reporta outliers (não remove).

        Args:
            rows: Lista de dicionários

        Returns:
            Tupla (rows_limpos, lista_de_avisos)
        """
        warnings = []

        # Remover nulos — dado ausente não pode ser pontuado, essa remoção é legítima
        rows_no_nulls = DataCleaner.remove_nulls(rows)
        if len(rows_no_nulls) < len(rows):
            warnings.append(f"Removidas {len(rows) - len(rows_no_nulls)} linhas com valores nulos")

        # Detectar outliers estatísticos — apenas para aviso, NÃO remove a leitura.
        # Um outlier pode ser um evento real de processo (ex: falha de equipamento) e precisa
        # continuar no lote para aparecer no score, no banco e em detect_anomalous_readings().
        _, outlier_indices = DataCleaner.detect_outliers(rows_no_nulls)
        if outlier_indices:
            warnings.append(
                f"Detectadas {len(outlier_indices)} leituras estatisticamente destoantes "
                f"(z-score > 2.0) — mantidas no lote, não removidas"
            )

        return rows_no_nulls, warnings
