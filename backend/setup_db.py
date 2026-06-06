#!/usr/bin/env python3
import sys
import os

# Garante que o root do projeto está no path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    from backend.db.database import Base, engine, SessionLocal
    from backend.models import Batch, SensorReading
    from datetime import datetime

    print("=== CRIANDO BANCO DE DADOS ===")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas")

    db = SessionLocal()

    batch = Batch(
        status="COMPLETED",
        upload_date=datetime.utcnow()
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    batch_id = batch.id
    print(f"✅ Batch criado (ID: {batch_id})")

    readings = [
        SensorReading(batch_id=batch_id, temperature=25.0, ph=7.0, dissolved_oxygen=85.0, pressure=5.0, agitator_speed=250, recorded_at=datetime.utcnow()),
        SensorReading(batch_id=batch_id, temperature=25.2, ph=7.1, dissolved_oxygen=84.5, pressure=5.1, agitator_speed=255, recorded_at=datetime.utcnow()),
        SensorReading(batch_id=batch_id, temperature=25.1, ph=6.9, dissolved_oxygen=86.0, pressure=4.9, agitator_speed=248, recorded_at=datetime.utcnow()),
    ]
    db.add_all(readings)
    db.commit()
    print("✅ 3 leituras de sensores inseridas")

    db.close()
    print("✅ Banco de dados pronto!")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
