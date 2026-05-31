"""
Data Validator - Validação de ranges de sensores.

Responsabilidades:
- Validar ranges esperados
- Detectar valores fora do range
- Retornar status de validação
"""

from typing import List, Dict, Any, Tuple


class DataValidator:
    """Valida dados de sensores contra ranges esperados."""

    RANGES = {
        "temperature": (20, 45),  # °C
        "ph": (4.0, 9.0),  # pH
        "dissolved_oxygen": (0, 100),  # %
        "pressure": (0, 10),  # bar
        "agitator_speed": (0, 500),  # RPM
    }

    @staticmethod
    def validate_row(row: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validar uma linha de dados.

        Args:
            row: Dicionário com dados de sensores

        Returns:
            Tupla (is_valid, list_of_errors)
        """
        errors = []

        for field, (min_val, max_val) in DataValidator.RANGES.items():
            if field not in row:
                errors.append(f"Campo obrigatório faltando: {field}")
                continue

            value = row[field]
            if not isinstance(value, (int, float)):
                errors.append(f"{field}: valor deve ser numérico")
                continue

            if value < min_val or value > max_val:
                errors.append(
                    f"{field}: valor {value} fora do range [{min_val}, {max_val}]"
                )

        return len(errors) == 0, errors

    @staticmethod
    def validate_batch(rows: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Validar lote de dados.

        Args:
            rows: Lista de dicionários com dados de sensores

        Returns:
            Tupla (valid_rows, list_of_errors)
        """
        valid_rows = []
        errors = []

        for idx, row in enumerate(rows):
            is_valid, row_errors = DataValidator.validate_row(row)
            if is_valid:
                valid_rows.append(row)
            else:
                errors.append(f"Linha {idx + 1}: {'; '.join(row_errors)}")

        return valid_rows, errors
