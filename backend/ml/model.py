"""
ML Model - RandomForestClassifier para predição de risco de processo.

Modelo treinado com dados históricos de bioprocessos para prever risco de desvio.
"""

import pickle
import os
from typing import Tuple, List, Dict
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class MLModel:
    """Modelo de predição de risco usando RandomForestClassifier."""

    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(_BASE_DIR, "models", "risk_predictor.pkl")
    SCALER_PATH = os.path.join(_BASE_DIR, "models", "scaler.pkl")

    # Features esperadas (mesma ordem usada no treinamento)
    FEATURES = ["temperature", "ph", "dissolved_oxygen", "pressure", "agitator_speed"]

    # Labels
    RISK_CLASSES = {0: "LOW_RISK", 1: "MEDIUM_RISK", 2: "HIGH_RISK"}
    CLASS_LABELS = {"LOW_RISK": 0, "MEDIUM_RISK": 1, "HIGH_RISK": 2}

    def __init__(self):
        """Inicializa modelo e scaler."""
        self.model = None
        self.scaler = None
        self._ensure_model_exists()

    def _ensure_model_exists(self):
        """Garante que modelo e scaler existem."""
        if os.path.exists(self.MODEL_PATH) and os.path.exists(self.SCALER_PATH):
            self.load()
        else:
            self._create_default_model()

    def _create_default_model(self):
        """Cria modelo default treinado com dados sintéticos."""
        np.random.seed(42)

        # Gerar dados de treinamento sintéticos
        X_synthetic = self._generate_synthetic_data(500)
        y_synthetic = self._generate_synthetic_labels(X_synthetic)

        # Treinar modelo
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_synthetic)

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            min_samples_split=5,
            min_samples_leaf=2,
        )
        self.model.fit(X_scaled, y_synthetic)

        # Salvar modelo
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
        self.save()

    # Ranges aceitáveis — mesmos do ComplianceService
    ACCEPTABLE_RANGES = {
        "temperature":    (20.0, 30.0),
        "ph":             (6.5,  7.5),
        "dissolved_oxygen": (70.0, 100.0),
        "pressure":       (4.5,  6.0),
        "agitator_speed": (200,  300),
    }

    def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
        """Gera dados sintéticos cobrindo zonas ideal, aceitável e fora de spec."""
        n_low    = int(n_samples * 0.60)  # dentro da faixa aceitável
        n_medium = int(n_samples * 0.25)  # 1-2 sensores fora da faixa
        n_high   = n_samples - n_low - n_medium  # 3+ sensores fora

        def _sample_acceptable(n):
            return np.column_stack([
                np.random.uniform(20.0, 30.0, n),
                np.random.uniform(6.5,  7.5,  n),
                np.random.uniform(70.0, 100.0, n),
                np.random.uniform(4.5,  6.0,  n),
                np.random.uniform(200,  300,  n),
            ])

        def _sample_out_of_range(n, n_out):
            """n_out sensores fora da faixa aceitável para cada amostra."""
            base = _sample_acceptable(n)
            out_ranges = [
                (-5.0, 19.9),   # temperature abaixo
                (30.1, 40.0),   # temperature acima
                (5.0, 6.4),     # ph abaixo
                (7.6, 9.0),     # ph acima
                (0.0, 69.9),    # dissolved_oxygen abaixo
                (0.0, 4.4),     # pressure abaixo
                (50,  199),     # agitator_speed abaixo
            ]
            for row in range(n):
                cols = np.random.choice(5, size=n_out, replace=False)
                for col in cols:
                    col_ranges = [r for r in out_ranges if
                                  (col == 0 and r[1] < 20) or
                                  (col == 0 and r[0] > 30) or
                                  (col == 1 and r[1] < 6.5) or
                                  (col == 1 and r[0] > 7.5) or
                                  (col == 2 and r[1] < 70) or
                                  (col == 3 and r[1] < 4.5) or
                                  (col == 4 and r[1] < 200)]
                    if col_ranges:
                        lo, hi = col_ranges[np.random.randint(len(col_ranges))]
                        base[row, col] = np.random.uniform(lo, hi)
            return base

        X_low    = _sample_acceptable(n_low)
        X_medium = _sample_out_of_range(n_medium, 1)
        X_high   = _sample_out_of_range(n_high, 3)

        return np.vstack([X_low, X_medium, X_high])

    def _generate_synthetic_labels(self, X: np.ndarray) -> np.ndarray:
        """
        Gera labels alinhados com o ComplianceService:
        - LOW_RISK   : todos os sensores dentro da faixa aceitável
        - MEDIUM_RISK: 1-2 sensores fora da faixa aceitável
        - HIGH_RISK  : 3+ sensores fora da faixa aceitável
        """
        labels = np.zeros(len(X), dtype=int)
        ranges = list(self.ACCEPTABLE_RANGES.values())

        for i, sample in enumerate(X):
            out_of_range = sum(
                1 for val, (lo, hi) in zip(sample, ranges)
                if not (lo <= val <= hi)
            )
            if out_of_range >= 3:
                labels[i] = 2  # HIGH_RISK
            elif out_of_range >= 1:
                labels[i] = 1  # MEDIUM_RISK
            else:
                labels[i] = 0  # LOW_RISK

        return labels

    def predict(self, sensor_readings: List[Dict]) -> Tuple[str, float]:
        """
        Prediz risco baseado em sensor readings.

        Args:
            sensor_readings: Lista de dicionários com leituras de sensores

        Returns:
            Tupla (risco_classificacao, confidence_0_1)
        """
        if not self.model or not self.scaler:
            return "MEDIUM_RISK", 0.5

        # Extrair features
        X = self._extract_features(sensor_readings)
        if X is None or len(X) == 0:
            return "MEDIUM_RISK", 0.5

        # Normalizar
        X_scaled = self.scaler.transform([X])

        # Prever
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        confidence = max(probabilities)

        risk_class = self.RISK_CLASSES.get(prediction, "MEDIUM_RISK")
        return risk_class, round(float(confidence), 3)

    def _extract_features(self, sensor_readings: List[Dict]) -> np.ndarray:
        """Extrai features na ordem correta."""
        features = []

        for feature_name in self.FEATURES:
            values = [reading.get(feature_name) for reading in sensor_readings if feature_name in reading]
            if not values:
                return None
            average = sum(values) / len(values)
            features.append(average)

        return np.array(features, dtype=float)

    def save(self):
        """Salva modelo e scaler."""
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
        with open(self.MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)
        with open(self.SCALER_PATH, "wb") as f:
            pickle.dump(self.scaler, f)

    def load(self):
        """Carrega modelo e scaler."""
        if os.path.exists(self.MODEL_PATH):
            with open(self.MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
        if os.path.exists(self.SCALER_PATH):
            with open(self.SCALER_PATH, "rb") as f:
                self.scaler = pickle.load(f)

    def get_feature_importance(self) -> Dict[str, float]:
        """Retorna importância das features."""
        if not self.model:
            return {}

        importance = self.model.feature_importances_
        return {
            feature: round(float(imp), 4)
            for feature, imp in zip(self.FEATURES, importance)
        }
