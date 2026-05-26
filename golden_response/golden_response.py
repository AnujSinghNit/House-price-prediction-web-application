"""
Golden benchmark solution for the PropTech house price prediction prompt.

Run:
    pip install flask flask-cors scikit-learn pandas numpy joblib
    python golden_response.py
"""

from __future__ import annotations

import os
import re
import sqlite3
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Configuration
BASE_DIR = os.path.dirname(__file__)
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "5000"))
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "predictions.db"))
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "house_price_model.joblib"))
RANDOM_SEED = 42
SAMPLE_COUNT = 10_000
RATE_LIMIT_REQUESTS = 20
RATE_LIMIT_SECONDS = 60

LOCATIONS = ["Downtown", "Suburban", "Rural", "Urban", "Waterfront"]
LOCATION_MULTIPLIERS = {
    "Downtown": 1.45,
    "Suburban": 1.00,
    "Rural": 0.72,
    "Urban": 1.20,
    "Waterfront": 1.80,
}

NUMERIC_FEATURES = [
    "square_footage",
    "bedrooms",
    "bathrooms",
    "year_built",
    "garage",
    "age",
    "total_rooms",
]
CATEGORICAL_FEATURES = ["location"]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SERVER_STARTED_AT = time.time()
MODEL: Pipeline | None = None
MODEL_METRICS: dict[str, float] = {}
RATE_LIMIT_BUCKETS: dict[str, deque[float]] = defaultdict(deque)


# Response helpers
def envelope(success: bool, data: Any = None, error: str | None = None, status: int = 200) -> tuple[Any, int]:
    """Return a consistent JSON API envelope."""
    return jsonify({"success": success, "data": data, "error": error}), status


def utc_now() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


# Database
def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row dictionaries enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    """Create the prediction history table if it does not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                square_footage REAL NOT NULL,
                bedrooms INTEGER NOT NULL,
                bathrooms INTEGER NOT NULL,
                location TEXT NOT NULL,
                year_built INTEGER NOT NULL,
                garage INTEGER NOT NULL,
                predicted_price REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )


def save_prediction(input_data: dict[str, Any], predicted_price: float) -> int:
    """Persist one prediction and return its database id."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO predictions (
                square_footage, bedrooms, bathrooms, location,
                year_built, garage, predicted_price, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                input_data["square_footage"],
                input_data["bedrooms"],
                input_data["bathrooms"],
                input_data["location"],
                input_data["year_built"],
                int(input_data["garage"]),
                predicted_price,
                utc_now(),
            ),
        )
        return int(cursor.lastrowid)


def fetch_history(limit: int, offset: int) -> list[dict[str, Any]]:
    """Fetch prediction history ordered from newest to oldest."""
    limit = max(1, min(limit, 100))
    offset = max(0, offset)
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, square_footage, bedrooms, bathrooms, location,
                   year_built, garage, predicted_price, timestamp
            FROM predictions
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
    return [dict(row) | {"garage": bool(row["garage"])} for row in rows]


# ML training and inference
def generate_dataset(samples: int = SAMPLE_COUNT) -> pd.DataFrame:
    """Generate reproducible synthetic house price training data."""
    rng = np.random.default_rng(RANDOM_SEED)
    square_footage = rng.integers(500, 10001, samples)
    bedrooms = rng.integers(1, 11, samples)
    bathrooms = rng.integers(1, 7, samples)
    locations = rng.choice(LOCATIONS, samples)
    year_built = rng.integers(1900, 2027, samples)
    garage = rng.integers(0, 2, samples)

    base_price = 50_000
    price = (
        base_price
        + square_footage * 155
        + bedrooms * 13_000
        + bathrooms * 18_000
        + np.maximum(0, year_built - 1970) * 600
        + garage * 24_000
    ).astype(float)
    price *= np.array([LOCATION_MULTIPLIERS[location] for location in locations])
    price += rng.normal(0, price * 0.04)
    price = np.maximum(price, 25_000)

    df = pd.DataFrame(
        {
            "square_footage": square_footage,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "location": locations,
            "year_built": year_built,
            "garage": garage,
            "price": price,
        }
    )
    return add_features(df)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add deterministic derived features used during training and inference."""
    enriched = df.copy()
    enriched["age"] = 2026 - enriched["year_built"]
    enriched["total_rooms"] = enriched["bedrooms"] + enriched["bathrooms"]
    return enriched


def build_pipeline() -> Pipeline:
    """Build the preprocessing and regression pipeline."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                GradientBoostingRegressor(
                    n_estimators=220,
                    learning_rate=0.08,
                    max_depth=5,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )


def train_or_load_model() -> tuple[Pipeline, dict[str, float]]:
    """Load the cached model if present, otherwise train and persist a model."""
    df = generate_dataset()
    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    x_train, x_test, y_train, y_test = train_test_split(
        df[feature_columns],
        df["price"],
        test_size=0.2,
        random_state=RANDOM_SEED,
    )

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = build_pipeline()
        model.fit(x_train, y_train)
        joblib.dump(model, MODEL_PATH)

    predictions = model.predict(x_test)
    metrics = {
        "r2": round(float(r2_score(y_test, predictions)), 4),
        "mae": round(float(mean_absolute_error(y_test, predictions)), 2),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, predictions))), 2),
    }
    return model, metrics


def predict_price(input_data: dict[str, Any]) -> float:
    """Predict a house price from validated input data."""
    if MODEL is None:
        raise RuntimeError("Model is not loaded")
    features = add_features(pd.DataFrame([input_data]))
    prediction = float(MODEL.predict(features[NUMERIC_FEATURES + CATEGORICAL_FEATURES])[0])
    return round(max(0.0, prediction), 2)


# Validation and rate limiting
def sanitize_text(value: Any) -> str:
    """Strip basic HTML tags and surrounding whitespace from text input."""
    return re.sub(r"<[^>]*>", "", str(value)).strip()


def parse_bool(value: Any) -> bool:
    """Coerce common JSON or form-style boolean values."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def validate_input(payload: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Validate request payload for the prediction endpoint."""
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object"

    required = ["square_footage", "bedrooms", "bathrooms", "location", "year_built"]
    missing = [field for field in required if field not in payload or payload[field] in (None, "")]
    if missing:
        return None, f"Missing required field(s): {', '.join(missing)}"

    try:
        square_footage = float(payload["square_footage"])
        bedrooms = int(payload["bedrooms"])
        bathrooms = int(payload["bathrooms"])
        year_built = int(payload["year_built"])
    except (TypeError, ValueError):
        return None, "Numeric fields must contain valid numbers"

    checks = [
        (500 <= square_footage <= 10000, "square_footage must be between 500 and 10000"),
        (1 <= bedrooms <= 10, "bedrooms must be between 1 and 10"),
        (1 <= bathrooms <= 6, "bathrooms must be between 1 and 6"),
        (1900 <= year_built <= 2026, "year_built must be between 1900 and 2026"),
    ]
    for passed, message in checks:
        if not passed:
            return None, message

    location = sanitize_text(payload["location"])
    if location not in LOCATIONS:
        return None, f"location must be one of: {', '.join(LOCATIONS)}"

    return {
        "square_footage": square_footage,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "location": location,
        "year_built": year_built,
        "garage": parse_bool(payload.get("garage", False)),
    }, None


def rate_limit_key() -> str:
    """Return a client key for simple in-memory rate limiting."""
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()


def is_rate_limited(client_key: str) -> bool:
    """Return True when the client exceeds the configured sliding window."""
    now = time.time()
    bucket = RATE_LIMIT_BUCKETS[client_key]
    while bucket and now - bucket[0] > RATE_LIMIT_SECONDS:
        bucket.popleft()
    if len(bucket) >= RATE_LIMIT_REQUESTS:
        return True
    bucket.append(now)
    return False


# API routes
@app.route("/api/health", methods=["GET"])
def health() -> tuple[Any, int]:
    """Return service health, model status, uptime, and metrics."""
    return envelope(
        True,
        {
            "status": "healthy",
            "model_loaded": MODEL is not None,
            "uptime_seconds": round(time.time() - SERVER_STARTED_AT, 2),
            "model_metrics": MODEL_METRICS,
            "timestamp": utc_now(),
        },
    )


@app.route("/api/predict", methods=["POST"])
def predict() -> tuple[Any, int]:
    """Validate input, run model inference, and store prediction history."""
    client_key = rate_limit_key()
    if is_rate_limited(client_key):
        return envelope(False, None, "Rate limit exceeded. Try again later.", 429)

    payload = request.get_json(silent=True)
    if payload is None:
        return envelope(False, None, "Request body must be valid JSON", 400)

    validated, error = validate_input(payload)
    if error:
        return envelope(False, None, error, 400)

    try:
        predicted_price = predict_price(validated)
        prediction_id = save_prediction(validated, predicted_price)
    except Exception as exc:
        return envelope(False, None, f"Prediction failed: {exc}", 500)

    return envelope(
        True,
        {
            "prediction_id": prediction_id,
            "predicted_price": predicted_price,
            "formatted_price": f"${predicted_price:,.2f}",
            "input": validated,
            "timestamp": utc_now(),
        },
    )


@app.route("/api/history", methods=["GET"])
def history() -> tuple[Any, int]:
    """Return paginated prediction history."""
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    return envelope(
        True,
        {
            "predictions": fetch_history(limit, offset),
            "limit": max(1, min(limit, 100)),
            "offset": max(0, offset),
        },
    )


@app.errorhandler(404)
def not_found(_error: Any) -> tuple[Any, int]:
    """Return a structured response for unknown routes."""
    return envelope(False, None, "Endpoint not found", 404)


@app.errorhandler(500)
def server_error(_error: Any) -> tuple[Any, int]:
    """Return a structured response for unexpected server errors."""
    return envelope(False, None, "Internal server error", 500)


def initialize() -> None:
    """Initialize database and model before serving requests."""
    global MODEL, MODEL_METRICS
    init_database()
    MODEL, MODEL_METRICS = train_or_load_model()
    print("Model metrics:")
    print(f"  R2:   {MODEL_METRICS['r2']:.4f}")
    print(f"  MAE:  ${MODEL_METRICS['mae']:,.2f}")
    print(f"  RMSE: ${MODEL_METRICS['rmse']:,.2f}")
    if MODEL_METRICS["r2"] < 0.85:
        raise RuntimeError("Model failed to meet required R2 >= 0.85")


if __name__ == "__main__":
    initialize()
    app.run(host=APP_HOST, port=APP_PORT, debug=False)
