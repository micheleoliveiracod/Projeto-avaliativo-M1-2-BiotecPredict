"""
Batch Service - Lógica de negócio para processamento de batches.

Responsabilidades:
- Orquestrar processamento de CSV
- Persistir dados no banco
- Gerenciar status de batch
"""

from sqlalchemy.orm import Session
from backend.models import Batch, SensorReading
from backend.db.repository import BatchRepository, SensorReadingRepository
from backend.processors import CSVProcessor, DataValidator, DataCleaner
from backend.services.compliance_service import ComplianceService
from backend.services.ml_service import MLService
from datetime import datetime
from typing import Tuple, List, Dict, Any


class BatchService:
    """Serviço para gerenciamento de batches."""

    @staticmethod
    def process_csv_upload(db: Session, file_content: str) -> Tuple[Batch, List[str]]:
        """
        Processar upload de arquivo CSV.

        Pipeline:
        1. Parse CSV
        2. Validar ranges
        3. Limpar dados
        4. Persistir batch e sensor readings

        Args:
            db: Sessão do banco de dados
            file_content: Conteúdo do arquivo CSV

        Returns:
            Tupla (batch_criado, lista_de_avisos)

        Raises:
            ValueError: Se processamento falhar
        """
        warnings = []

        try:
            # 1. Parse CSV
            rows = CSVProcessor.process(file_content)
            warnings.append(f"CSV processado: {len(rows)} linhas lidas")

            # 2. Validar ranges
            valid_rows, validation_errors = DataValidator.validate_batch(rows)
            if validation_errors:
                warnings.extend(validation_errors)

            if not valid_rows:
                raise ValueError("Nenhuma linha válida após validação")

            # 3. Limpar dados
            cleaned_rows, clean_warnings = DataCleaner.clean(valid_rows)
            warnings.extend(clean_warnings)

            if not cleaned_rows:
                raise ValueError("Nenhuma linha após limpeza de dados")

            # 4. Criar batch
            batch = Batch(status="PROCESSING", upload_date=datetime.utcnow())
            batch = BatchRepository.create(db, batch)

            # 5. Persistir sensor readings
            for row in cleaned_rows:
                sensor_reading = SensorReading(
                    batch_id=batch.id,
                    temperature=row["temperature"],
                    ph=row["ph"],
                    dissolved_oxygen=row["dissolved_oxygen"],
                    pressure=row["pressure"],
                    agitator_speed=row["agitator_speed"],
                )
                SensorReadingRepository.create(db, sensor_reading)

            # 6. Calcular compliance score
            score, classification = ComplianceService.calculate_compliance_score(cleaned_rows)
            warnings.append(f"Compliance Score: {score} ({classification})")

            # 7. Predição de risco com ML
            try:
                risk_class, confidence = MLService.predict_risk(cleaned_rows)
                warnings.append(f"Risk Prediction: {risk_class} (confiança: {confidence:.2f})")
            except Exception:
                risk_class = None

            # 8. Atualizar batch com resultados finais
            batch = BatchRepository.update(
                db,
                batch.id,
                status="COMPLETED",
                compliance_score=score,
                risk_prediction=risk_class,
            )

            warnings.append(f"Batch {batch.id} processado com sucesso")
            return batch, warnings

        except Exception as e:
            raise ValueError(f"Erro ao processar batch: {str(e)}")

    @staticmethod
    def get_batch(db: Session, batch_id: int) -> Batch:
        """Obter batch por ID."""
        batch = BatchRepository.get_by_id(db, batch_id)
        if not batch:
            raise ValueError(f"Batch {batch_id} não encontrado")
        return batch

    @staticmethod
    def list_batches(db: Session, skip: int = 0, limit: int = 100) -> List[Batch]:
        """Listar batches com paginação."""
        return BatchRepository.get_all(db, skip, limit)
