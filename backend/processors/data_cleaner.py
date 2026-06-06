"""
Data Cleaner - Limpeza de dados (nulos, outliers).

Responsabilidades:
- Remover valores nulos
- Detectar outliers
- Retornar dados limpos
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
        Detectar outliers usando desvio padrão.

        Args:
            rows: Lista de dicionários
            threshold: Número de desvios padrão (padrão: 2.0)

        Returns:
            Tupla (rows_sem_outliers, indices_outliers)
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

        # Remover duplicatas e ordenar
        outlier_indices = sorted(set(outlier_indices), reverse=True)

        # Remover outliers
        cleaned_rows = [row for idx, row in enumerate(rows) if idx not in outlier_indices]

        return cleaned_rows, outlier_indices

    @staticmethod
    def clean(rows: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[str]]:
        """
        Executar limpeza completa.

        Args:
            rows: Lista de dicionários

        Returns:
            Tupla (rows_limpos, lista_de_avisos)
        """
        warnings = []

        # Remover nulos
        rows_no_nulls = DataCleaner.remove_nulls(rows)
        if len(rows_no_nulls) < len(rows):
            warnings.append(f"Removidas {len(rows) - len(rows_no_nulls)} linhas com valores nulos")

        # Detectar outliers
        rows_cleaned, outlier_indices = DataCleaner.detect_outliers(rows_no_nulls)
        if outlier_indices:
            warnings.append(f"Detectados {len(outlier_indices)} outliers removidos")

        return rows_cleaned, warnings
