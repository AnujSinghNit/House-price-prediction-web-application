# Domain-Specific Coding Prompt

## Task

Build a production-quality Python backend for a PropTech house price prediction API. The service will be used by a real estate analytics team to estimate residential property prices, store prediction history, and expose health information for monitoring.

The solution must be delivered as executable Python code and should be clear enough for another engineer to run locally.

## Business Context

Real estate agents need fast preliminary valuations before ordering a formal appraisal. The API should accept structured property information, run a trained machine learning model, return a price estimate, and keep an auditable record of each prediction.

## Functional Requirements

1. Create a Flask REST API with these endpoints:
   - `GET /api/health`
   - `POST /api/predict`
   - `GET /api/history`
2. Generate a synthetic housing dataset with at least 10,000 samples if no trained model exists.
3. Train a `GradientBoostingRegressor` inside a scikit-learn `Pipeline`.
4. Use a `ColumnTransformer` with:
   - `StandardScaler` for numeric features.
   - `OneHotEncoder` for categorical location.
5. Persist the trained model using `joblib`.
6. Store prediction history in SQLite.

## Input Fields

`POST /api/predict` must accept JSON with:

```json
{
  "square_footage": 2400,
  "bedrooms": 4,
  "bathrooms": 3,
  "location": "Suburban",
  "year_built": 2015,
  "garage": true
}
```

## Explicit Constraints

1. Validate all required fields and return HTTP `400` with a descriptive message for missing or invalid input.
2. Enforce these ranges:
   - `square_footage`: 500 to 10000
   - `bedrooms`: 1 to 10
   - `bathrooms`: 1 to 6
   - `year_built`: 1900 to 2026
3. `location` must be one of: `Downtown`, `Suburban`, `Rural`, `Urban`, `Waterfront`.
4. Load the ML model once at application startup. Do not retrain or reload it per request.
5. The prediction response must include:
   - `success`
   - `data.predicted_price`
   - `data.formatted_price`
   - `data.input`
   - `data.timestamp`
   - `error`
6. `GET /api/history` must support `limit` and `offset` query parameters with a maximum limit of 100.
7. `GET /api/health` must report model load status, uptime, and model metrics.
8. Include basic rate limiting for the prediction endpoint.
9. Handle malformed JSON, not-found routes, and unexpected server errors with structured JSON.
10. The model must achieve an R2 score of at least 0.85 on a held-out test set.

## Technical Requirements

1. Use only Python standard library plus:
   - Flask
   - flask-cors
   - scikit-learn
   - pandas
   - numpy
   - joblib
2. Use SQLite with parameterized queries.
3. Use type hints for public helper functions.
4. Add docstrings to all public functions.
5. Keep configuration values near the top of the file.

## Formatting Requirements

1. Return all API responses using this JSON envelope:

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

2. Keep the code in a single file named `golden_response.py`.
3. Use clear section comments so reviewers can quickly navigate the code.
4. Print model metrics when the application starts.
5. Include a concise README explaining setup, execution, endpoints, and evaluation methodology.

## Expected Deliverable

Submit a repository containing:

- `prompt.md`
- `justification.md`
- `golden_response.py`
- `README.md`

The repository should allow an evaluator to run:

```bash
pip install flask flask-cors scikit-learn pandas numpy joblib
python golden_response.py
```

Then test the API at `http://localhost:5000`.
