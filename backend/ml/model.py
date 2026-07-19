"""
ML Model - RandomForestClassifier para predição de risco de processo.

Modelo treinado com dados históricos de bioprocessos para prever risco de desvio.

Nota conceitual: este modelo mede DESVIO DO LIMITE ACEITÁVEL — quantos sensores (0, 1-2 ou
3+) romperam a faixa aceitável do processo (ver ACCEPTABLE_RANGES abaixo), sinalizando se o
lote deve ser descartado/investigado. Não mede qualidade/proximidade do ideal — isso é papel
do ComplianceService (backend/services/compliance_service.py), que pontua o quão bem
centrado o processo está mesmo dentro da faixa aceitável. As duas métricas respondem
perguntas diferentes e podem legitimamente divergir no mesmo lote — ver
backend/tests/fixtures/csv/README.md para exemplos reais.
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

        # Gerar dados de treinamento sintéticos.
        # 500 amostras deixava as combinacoes de "exatamente 1" ou "exatamente 3"
        # sensores fora da faixa com poucas dezenas de exemplos cada (5 sensores x
        # 2 direcoes de desvio), insuficiente para o classificador aprender a
        # fronteira: o modelo chegava a prever LOW_RISK/MEDIUM_RISK para entradas
        # que a propria funcao de rotulo (_generate_synthetic_labels) classificaria
        # como MEDIUM_RISK/HIGH_RISK. 15000 amostras (custo de treino ~1s) da
        # densidade suficiente por combinacao e elimina essa inconsistencia
        # (validado com os fixtures em backend/tests/fixtures/csv/bugs/).
        X_synthetic = self._generate_synthetic_data(15000)
        y_synthetic = self._generate_synthetic_labels(X_synthetic)

        # Treinar modelo
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_synthetic)

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=14,
            random_state=42,
            n_jobs=-1,
            min_samples_split=4,
            min_samples_leaf=1,
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
        n_low    = int(n_samples * 0.50)  # todos dentro da faixa aceitável
        n_medium = int(n_samples * 0.30)  # 1-2 sensores fora da faixa
        n_high   = n_samples - n_low - n_medium  # 3-5 sensores fora

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
            # Ranges fora de spec: cobre tanto valores abaixo quanto acima do limite,
            # incluindo valores extremos observados nos CSVs de teste.
            out_ranges = [
                (-5.0, 19.9),    # temperature abaixo
                (30.1, 45.0),    # temperature acima (estendido até 45°C)
                (5.0,  6.4),     # ph abaixo
                (7.6,  9.5),     # ph acima (estendido até 9.5)
                (0.0,  69.9),    # dissolved_oxygen abaixo
                (0.0,  4.4),     # pressure abaixo
                (6.1,  8.0),     # pressure acima
                (50,   199),     # agitator_speed abaixo
                (301,  450),     # agitator_speed acima
            ]
            col_filter = {
                0: lambda r: r[1] < 20 or r[0] > 30,     # temperature
                1: lambda r: r[1] < 6.5 or r[0] > 7.5,  # ph
                2: lambda r: r[1] < 70,                   # dissolved_oxygen
                3: lambda r: r[1] < 4.5 or r[0] > 6.0,  # pressure
                4: lambda r: r[1] < 200 or r[0] > 300,  # agitator_speed
            }
            for row in range(n):
                cols = np.random.choice(5, size=n_out, replace=False)
                for col in cols:
                    candidates = [r for r in out_ranges if col_filter[col](r)]
                    if candidates:
                        lo, hi = candidates[np.random.randint(len(candidates))]
                        base[row, col] = np.random.uniform(lo, hi)
            return base

        X_low = _sample_acceptable(n_low)

        # Médio: metade com 1 sensor fora, metade com 2 — sem gap no treino
        n_med1 = n_medium // 2
        n_med2 = n_medium - n_med1
        X_medium = np.vstack([
            _sample_out_of_range(n_med1, 1),
            _sample_out_of_range(n_med2, 2),
        ])

        # Alto: distribuído entre 3, 4 e 5 sensores fora
        n_high3 = n_high // 3
        n_high4 = n_high // 3
        n_high5 = n_high - n_high3 - n_high4
        X_high = np.vstack([
            _sample_out_of_range(n_high3, 3),
            _sample_out_of_range(n_high4, 4),
            _sample_out_of_range(n_high5, 5),
        ])

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
