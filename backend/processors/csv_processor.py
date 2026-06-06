"""
CSV Processor - Leitura e parsing de arquivos CSV.

Responsabilidades:
- Ler arquivo CSV
- Validar estrutura
- Extrair dados de sensores
- Retornar lista de leituras
"""

import csv
from io import StringIO
from typing import List, Dict, Any, Optional


class CSVProcessor:
    """Processa arquivos CSV com dados de sensores."""

    REQUIRED_COLUMNS = [
        "temperature",
        "ph",
        "dissolved_oxygen",
        "pressure",
        "agitator_speed",
    ]

    # Mapeamento de aliases → nomes canônicos (aceita variações do Kaggle e outros datasets)
    COLUMN_ALIASES: Dict[str, str] = {
        # temperature
        "temperature": "temperature",
        "temp": "temperature",
        "temperatura": "temperature",
        "temperature (c)": "temperature",
        "temperature(c)": "temperature",
        "temperature_c": "temperature",
        # ph
        "ph": "ph",
        "ph_value": "ph",
        "ph value": "ph",
        "ph_level": "ph",
        # dissolved_oxygen
        "dissolved_oxygen": "dissolved_oxygen",
        "dissolved oxygen": "dissolved_oxygen",
        "dissolved_o2": "dissolved_oxygen",
        "dissolved o2": "dissolved_oxygen",
        "do": "dissolved_oxygen",
        "do (%)": "dissolved_oxygen",
        "do(%)": "dissolved_oxygen",
        "oxigenio_dissolvido": "dissolved_oxygen",
        "oxygen": "dissolved_oxygen",
        "dissolvedoxygen": "dissolved_oxygen",
        # pressure
        "pressure": "pressure",
        "pressao": "pressure",
        "pressão": "pressure",
        "pressure (bar)": "pressure",
        "pressure(bar)": "pressure",
        "vessel_pressure": "pressure",
        "vessel pressure": "pressure",
        # agitator_speed
        "agitator_speed": "agitator_speed",
        "agitator speed": "agitator_speed",
        "agitator_speed (rpm)": "agitator_speed",
        "agitator_speed(rpm)": "agitator_speed",
        "agitation_speed": "agitator_speed",
        "agitation speed": "agitator_speed",
        "agitation_rate": "agitator_speed",
        "agitation rate": "agitator_speed",
        "rpm": "agitator_speed",
        "stirrer_speed": "agitator_speed",
        "stirrer speed": "agitator_speed",
        "speed": "agitator_speed",
        "agitatorspeed": "agitator_speed",
    }

    @staticmethod
    def _normalize_header(header: str) -> str:
        return header.strip().lower().replace("-", "_")

    @staticmethod
    def _build_column_map(fieldnames: List[str]) -> Dict[str, str]:
        """Constrói mapeamento de nome original → nome canônico."""
        mapping: Dict[str, str] = {}
        for field in fieldnames:
            normalized = CSVProcessor._normalize_header(field)
            canonical = CSVProcessor.COLUMN_ALIASES.get(normalized)
            if canonical and canonical not in mapping.values():
                mapping[field] = canonical
        return mapping

    @staticmethod
    def process(file_content: str) -> List[Dict[str, Any]]:
        """
        Processar conteúdo do CSV.

        Args:
            file_content: Conteúdo do arquivo CSV como string

        Returns:
            Lista de dicionários com dados de sensores

        Raises:
            ValueError: Se estrutura do CSV for inválida
        """
        try:
            reader = csv.DictReader(StringIO(file_content))

            if reader.fieldnames is None:
                raise ValueError("Arquivo CSV vazio")

            fieldnames = list(reader.fieldnames)
            column_map = CSVProcessor._build_column_map(fieldnames)

            # Verificar se todas as colunas obrigatórias foram mapeadas
            mapped_canonical = set(column_map.values())
            missing_columns = set(CSVProcessor.REQUIRED_COLUMNS) - mapped_canonical
            if missing_columns:
                raise ValueError(
                    f"Colunas obrigatórias faltando: {missing_columns}. "
                    f"Colunas encontradas no CSV: {fieldnames}"
                )

            # Inverter mapeamento: canônico → nome original no CSV
            canonical_to_original: Dict[str, str] = {v: k for k, v in column_map.items()}

            rows = []
            for row_num, row in enumerate(reader, start=2):
                try:
                    processed_row = {
                        canonical: float(row[canonical_to_original[canonical]])
                        for canonical in CSVProcessor.REQUIRED_COLUMNS
                    }
                    rows.append(processed_row)
                except ValueError as e:
                    raise ValueError(f"Erro ao converter valores na linha {row_num}: {str(e)}")

            if not rows:
                raise ValueError("Nenhuma linha de dados encontrada no CSV")

            return rows

        except Exception as e:
            raise ValueError(f"Erro ao processar CSV: {str(e)}")
