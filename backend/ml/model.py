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

    MODEL_PATH = "backend/ml/models/risk_predictor.pkl"
    SCALER_PATH = "backend/ml/models/scaler.pkl"

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

    def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
        """Gera dados sintéticos para treinamento inicial."""
        # Ranges normais esperados
        temperature = np.random.normal(25.0, 1.0, n_samples)
        ph = np.random.normal(7.0, 0.3, n_samples)
        dissolved_oxygen = np.random.normal(85.0, 5.0, n_samples)
        pressure = np.random.normal(5.0, 0.3, n_samples)
        agitator_speed = np.random.normal(250, 15, n_samples)

        return np.column_stack([temperature, ph, dissolved_oxygen, pressure, agitator_speed])

    def _generate_synthetic_labels(self, X: np.ndarray) -> np.ndarray:
        """Gera labels baseado em heurísticas."""
        labels = np.zeros(len(X), dtype=int)

        for i, sample in enumerate(X):
            temp, ph, do, pressure, speed = sample

            # Heurística simples: quanto mais desvios, maior o risco
            deviations = 0
            if not (24 <= temp <= 26):
                deviations += 1
            if not (6.8 <= ph <= 7.2):
                deviations += 1
            if not (80 <= do <= 95):
                deviations += 1
            if not (4.8 <= pressure <= 5.5):
                deviations += 1
            if not (240 <= speed <= 280):
                deviations += 1

            if deviations >= 3:
                labels[i] = 2  # HIGH_RISK
            elif deviations == 2:
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
