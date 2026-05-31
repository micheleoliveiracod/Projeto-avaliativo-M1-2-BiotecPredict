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
from typing import List, Dict, Any
from backend.schemas import SensorReadingSchema


class CSVProcessor:
    """Processa arquivos CSV com dados de sensores."""

    REQUIRED_COLUMNS = [
        "temperature",
        "ph",
        "dissolved_oxygen",
        "pressure",
        "agitator_speed",
    ]

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

            # Validar colunas obrigatórias
            missing_columns = set(CSVProcessor.REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"Colunas obrigatórias faltando: {missing_columns}")

            rows = []
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Converter valores para float
                    processed_row = {
                        "temperature": float(row["temperature"]),
                        "ph": float(row["ph"]),
                        "dissolved_oxygen": float(row["dissolved_oxygen"]),
                        "pressure": float(row["pressure"]),
                        "agitator_speed": float(row["agitator_speed"]),
                    }
                    rows.append(processed_row)
                except ValueError as e:
                    raise ValueError(f"Erro ao converter valores na linha {row_num}: {str(e)}")

            if not rows:
                raise ValueError("Nenhuma linha de dados encontrada no CSV")

            return rows

        except Exception as e:
            raise ValueError(f"Erro ao processar CSV: {str(e)}")
