"""
Testes de integração da API BiotecPredict.

Cobre os endpoints reais da API com banco de dados SQLite in-memory:
- GET  /health
- POST /api/v1/upload
- GET  /api/v1/batches
- GET  /api/v1/batch/{id}
- GET  /api/v1/batch/{id}/sensors
- GET  /api/v1/compliance/{id}
- GET  /api/v1/prediction/{id}
- GET  /api/v1/model/info
- POST /api/v1/predict

Pré-requisitos: conftest.py fornece fixtures client, db_session.
"""

import io
import time
import pytest
from fastapi.testclient import TestClient


# ── Dados auxiliares ──────────────────────────────────────────────────────────

VALID_CSV = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,85.0,5.0,260
25.5,7.1,87.0,5.1,255
24.8,7.0,86.0,4.9,258
25.2,7.2,88.0,5.2,262
"""

MISSING_COLUMNS_CSV = b"""temperature,ph,pressure
25.0,7.0,5.0
"""

WRONG_TYPES_CSV = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
invalid,7.0,85.0,5.0,260
"""

HEADER_ONLY_CSV = b"temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"

LARGE_CSV = (
    b"temperature,ph,dissolved_oxygen,pressure,agitator_speed\n"
    + b"\n".join(
        f"{20 + i % 10},{6.8 + (i % 5) * 0.1},{80 + i % 15},{4.8 + (i % 7) * 0.1},{240 + i % 40}".encode()
        for i in range(500)
    )
)


def _upload(client: TestClient, content: bytes, filename: str = "test.csv") -> dict:
    """Utilitário: faz upload e retorna o JSON da resposta."""
    files = {"file": (filename, io.BytesIO(content), "text/csv")}
    return client.post("/api/v1/upload", files=files)


# ── Health Check ──────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_response_structure(self, client):
        data = client.get("/health").json()
        assert data["status"] == "ok"
        assert data["service"] == "BiotecPredict"
        assert "version" in data

    def test_root_endpoint(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "message" in r.json()


# ── Upload CSV ────────────────────────────────────────────────────────────────

class TestUpload:

    def test_upload_valid_csv_returns_200(self, client):
        r = _upload(client, VALID_CSV)
        assert r.status_code == 200

    def test_upload_response_has_id(self, client):
        data = _upload(client, VALID_CSV).json()
        assert "id" in data
        assert isinstance(data["id"], int)
        assert data["id"] > 0

    def test_upload_response_status_completed(self, client):
        data = _upload(client, VALID_CSV).json()
        assert data["status"] == "COMPLETED"

    def test_upload_response_has_upload_date(self, client):
        data = _upload(client, VALID_CSV).json()
        assert "upload_date" in data
        assert len(data["upload_date"]) > 0

    def test_upload_multiple_files_get_different_ids(self, client):
        id1 = _upload(client, VALID_CSV, "a.csv").json()["id"]
        id2 = _upload(client, VALID_CSV, "b.csv").json()["id"]
        assert id1 != id2

    def test_upload_empty_file_returns_400(self, client):
        r = _upload(client, b"")
        assert r.status_code == 400

    def test_upload_header_only_returns_400(self, client):
        r = _upload(client, HEADER_ONLY_CSV)
        assert r.status_code == 400

    def test_upload_missing_columns_returns_400(self, client):
        r = _upload(client, MISSING_COLUMNS_CSV)
        assert r.status_code == 400

    def test_upload_wrong_types_returns_400(self, client):
        r = _upload(client, WRONG_TYPES_CSV)
        assert r.status_code == 400

    def test_upload_error_response_has_detail(self, client):
        data = _upload(client, b"").json()
        assert "detail" in data

    def test_upload_performance_500_rows_under_5s(self, client):
        start = time.perf_counter()
        r = _upload(client, LARGE_CSV)
        elapsed = time.perf_counter() - start
        assert r.status_code == 200
        assert elapsed < 5.0, f"Upload demorou {elapsed:.2f}s (esperado < 5s)"

    def test_upload_boundary_values_accepted(self, client):
        csv = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
20.0,4.0,0.0,0.0,0.0
45.0,9.0,100.0,10.0,500.0
"""
        r = _upload(client, csv)
        assert r.status_code == 200


# ── Listar Batches ────────────────────────────────────────────────────────────

class TestListBatches:

    def test_list_empty_db_returns_200(self, client):
        r = client.get("/api/v1/batches")
        assert r.status_code == 200

    def test_list_empty_db_returns_list(self, client):
        data = client.get("/api/v1/batches").json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_after_upload_returns_one_batch(self, client):
        _upload(client, VALID_CSV)
        data = client.get("/api/v1/batches").json()
        assert len(data) == 1

    def test_list_batch_has_required_fields(self, client):
        _upload(client, VALID_CSV)
        batch = client.get("/api/v1/batches").json()[0]
        for field in ("id", "status", "upload_date"):
            assert field in batch, f"Campo '{field}' ausente no batch listado"

    def test_list_skip_parameter(self, client):
        _upload(client, VALID_CSV, "a.csv")
        _upload(client, VALID_CSV, "b.csv")
        data = client.get("/api/v1/batches?skip=1&limit=10").json()
        assert len(data) == 1

    def test_list_limit_parameter(self, client):
        for i in range(5):
            _upload(client, VALID_CSV, f"batch{i}.csv")
        data = client.get("/api/v1/batches?limit=3").json()
        assert len(data) == 3

    def test_list_multiple_uploads_ordered(self, client):
        _upload(client, VALID_CSV, "first.csv")
        _upload(client, VALID_CSV, "second.csv")
        data = client.get("/api/v1/batches").json()
        assert len(data) == 2


# ── Detalhe do Batch ──────────────────────────────────────────────────────────

class TestGetBatch:

    def test_get_existing_batch_returns_200(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        r = client.get(f"/api/v1/batch/{batch_id}")
        assert r.status_code == 200

    def test_get_batch_id_matches(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/batch/{batch_id}").json()
        assert data["id"] == batch_id

    def test_get_batch_status_completed(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/batch/{batch_id}").json()
        assert data["status"] == "COMPLETED"

    def test_get_nonexistent_batch_returns_404(self, client):
        r = client.get("/api/v1/batch/99999")
        assert r.status_code == 404

    def test_get_batch_response_fields(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/batch/{batch_id}").json()
        for field in ("id", "status", "upload_date"):
            assert field in data


# ── Sensores do Batch ─────────────────────────────────────────────────────────

class TestBatchSensors:

    def test_get_sensors_returns_200(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        r = client.get(f"/api/v1/batch/{batch_id}/sensors")
        assert r.status_code == 200

    def test_get_sensors_response_structure(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/batch/{batch_id}/sensors").json()
        assert "batch_id" in data
        assert "count" in data
        assert "readings" in data

    def test_get_sensors_count_matches_csv_rows(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/batch/{batch_id}/sensors").json()
        assert data["count"] == 4  # VALID_CSV tem 4 linhas de dados

    def test_get_sensors_reading_has_all_fields(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        reading = client.get(f"/api/v1/batch/{batch_id}/sensors").json()["readings"][0]
        for field in ("temperature", "ph", "dissolved_oxygen", "pressure", "agitator_speed"):
            assert field in reading

    def test_get_sensors_values_match_csv(self, client):
        csv = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,85.0,5.0,260
"""
        batch_id = _upload(client, csv).json()["id"]
        reading = client.get(f"/api/v1/batch/{batch_id}/sensors").json()["readings"][0]
        assert abs(reading["temperature"] - 25.0) < 0.01
        assert abs(reading["ph"] - 7.0) < 0.01

    def test_get_sensors_nonexistent_batch_returns_404(self, client):
        r = client.get("/api/v1/batch/99999/sensors")
        assert r.status_code == 404


# ── Compliance Score ──────────────────────────────────────────────────────────

class TestCompliance:

    def test_get_compliance_returns_200(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        r = client.get(f"/api/v1/compliance/{batch_id}")
        assert r.status_code == 200

    def test_compliance_response_has_required_fields(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/compliance/{batch_id}").json()
        assert "batch_id" in data
        assert "compliance_score" in data
        assert "classification" in data
        assert "sensor_metrics" in data

    def test_compliance_batch_id_matches(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/compliance/{batch_id}").json()
        assert data["batch_id"] == batch_id

    def test_compliance_score_in_valid_range(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        score = client.get(f"/api/v1/compliance/{batch_id}").json()["compliance_score"]
        assert 0 <= score <= 100

    def test_compliance_classification_valid_values(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        classification = client.get(f"/api/v1/compliance/{batch_id}").json()["classification"]
        assert classification in ("ACCEPTABLE", "WARNING", "CRITICAL")

    def test_compliance_ideal_values_acceptable_score(self, client):
        """Valores dentro dos ranges ideais devem resultar em score ACCEPTABLE."""
        csv = b"""temperature,ph,dissolved_oxygen,pressure,agitator_speed
25.0,7.0,85.0,5.0,260
25.0,7.0,85.0,5.0,260
"""
        batch_id = _upload(client, csv).json()["id"]
        data = client.get(f"/api/v1/compliance/{batch_id}").json()
        assert data["compliance_score"] >= 80
        assert data["classification"] == "ACCEPTABLE"

    def test_compliance_sensor_metrics_has_all_sensors(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        metrics = client.get(f"/api/v1/compliance/{batch_id}").json()["sensor_metrics"]
        for sensor in ("temperature", "ph", "dissolved_oxygen", "pressure", "agitator_speed"):
            assert sensor in metrics

    def test_compliance_sensor_metrics_structure(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        metrics = client.get(f"/api/v1/compliance/{batch_id}").json()["sensor_metrics"]
        temp = metrics["temperature"]
        for key in ("average", "min", "max", "ideal_min", "ideal_max"):
            assert key in temp

    def test_compliance_deterministic_same_result_twice(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        score1 = client.get(f"/api/v1/compliance/{batch_id}").json()["compliance_score"]
        score2 = client.get(f"/api/v1/compliance/{batch_id}").json()["compliance_score"]
        assert score1 == score2

    def test_compliance_nonexistent_batch_returns_404(self, client):
        r = client.get("/api/v1/compliance/99999")
        assert r.status_code == 404

    def test_compliance_response_time_under_200ms(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        start = time.perf_counter()
        client.get(f"/api/v1/compliance/{batch_id}")
        elapsed = time.perf_counter() - start
        assert elapsed < 0.2, f"Compliance demorou {elapsed:.3f}s (esperado < 0.2s)"


# ── Predição de Risco ─────────────────────────────────────────────────────────

class TestPrediction:

    def test_get_prediction_returns_200(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        r = client.get(f"/api/v1/prediction/{batch_id}")
        assert r.status_code == 200

    def test_prediction_response_has_required_fields(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/prediction/{batch_id}").json()
        for field in ("batch_id", "risk_prediction", "confidence_score"):
            assert field in data

    def test_prediction_batch_id_matches(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/prediction/{batch_id}").json()
        assert data["batch_id"] == batch_id

    def test_prediction_risk_is_valid_class(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        risk = client.get(f"/api/v1/prediction/{batch_id}").json()["risk_prediction"]
        assert risk in ("LOW_RISK", "MEDIUM_RISK", "HIGH_RISK")

    def test_prediction_confidence_score_range(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        confidence = client.get(f"/api/v1/prediction/{batch_id}").json()["confidence_score"]
        assert 0.0 <= confidence <= 1.0

    def test_prediction_has_interpretation(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/prediction/{batch_id}").json()
        assert "interpretation" in data
        assert len(data["interpretation"]) > 0

    def test_prediction_has_recommendations(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        data = client.get(f"/api/v1/prediction/{batch_id}").json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_prediction_nonexistent_batch_returns_404(self, client):
        r = client.get("/api/v1/prediction/99999")
        assert r.status_code == 404

    def test_prediction_response_time_under_1s(self, client):
        batch_id = _upload(client, VALID_CSV).json()["id"]
        start = time.perf_counter()
        client.get(f"/api/v1/prediction/{batch_id}")
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Predição demorou {elapsed:.3f}s (esperado < 1s)"


# ── ML Direto (POST /predict) ─────────────────────────────────────────────────

class TestPredictEndpoint:

    def test_predict_returns_200(self, client):
        r = client.post("/api/v1/predict", json={
            "temperature": 25.0, "ph": 7.0,
            "dissolved_oxygen": 85.0, "pressure": 5.0, "agitator_speed": 260.0,
        })
        assert r.status_code == 200

    def test_predict_response_has_risk_class(self, client):
        data = client.post("/api/v1/predict", json={
            "temperature": 25.0, "ph": 7.0,
            "dissolved_oxygen": 85.0, "pressure": 5.0, "agitator_speed": 260.0,
        }).json()
        assert "risk_prediction" in data
        assert data["risk_prediction"] in ("LOW_RISK", "MEDIUM_RISK", "HIGH_RISK")

    def test_predict_response_has_confidence(self, client):
        data = client.post("/api/v1/predict", json={
            "temperature": 25.0, "ph": 7.0,
            "dissolved_oxygen": 85.0, "pressure": 5.0, "agitator_speed": 260.0,
        }).json()
        assert "confidence_score" in data
        assert 0.0 <= data["confidence_score"] <= 1.0


# ── Model Info ────────────────────────────────────────────────────────────────

class TestModelInfo:

    def test_model_info_returns_200(self, client):
        r = client.get("/api/v1/model/info")
        assert r.status_code == 200

    def test_model_info_has_model_type(self, client):
        data = client.get("/api/v1/model/info").json()
        assert "model_type" in data

    def test_model_info_has_features(self, client):
        data = client.get("/api/v1/model/info").json()
        assert "features" in data
        assert isinstance(data["features"], list)
        assert len(data["features"]) == 5

    def test_model_info_features_are_correct(self, client):
        features = set(client.get("/api/v1/model/info").json()["features"])
        expected = {"temperature", "ph", "dissolved_oxygen", "pressure", "agitator_speed"}
        assert features == expected


# ── Fluxo End-to-End ──────────────────────────────────────────────────────────

class TestEndToEndFlow:

    def test_full_pipeline_upload_compliance_prediction(self, client):
        """Fluxo completo: upload → compliance → prediction."""
        # 1. Upload
        upload_data = _upload(client, VALID_CSV).json()
        batch_id = upload_data["id"]
        assert upload_data["status"] == "COMPLETED"

        # 2. Compliance
        comp = client.get(f"/api/v1/compliance/{batch_id}").json()
        assert comp["classification"] in ("ACCEPTABLE", "WARNING", "CRITICAL")

        # 3. Prediction
        pred = client.get(f"/api/v1/prediction/{batch_id}").json()
        assert pred["risk_prediction"] in ("LOW_RISK", "MEDIUM_RISK", "HIGH_RISK")

    def test_full_pipeline_sensors_retrievable(self, client):
        """Após upload, sensores devem estar acessíveis."""
        batch_id = _upload(client, VALID_CSV).json()["id"]
        sensors = client.get(f"/api/v1/batch/{batch_id}/sensors").json()
        assert sensors["count"] > 0

    def test_batch_appears_in_list_after_upload(self, client):
        """Batch criado deve aparecer na listagem."""
        batch_id = _upload(client, VALID_CSV).json()["id"]
        ids_in_list = [b["id"] for b in client.get("/api/v1/batches").json()]
        assert batch_id in ids_in_list
