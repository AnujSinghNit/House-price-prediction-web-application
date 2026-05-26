# House Price Prediction LLM Benchmark

This repository contains a complete benchmark package for evaluating LLM-generated code on a realistic PropTech machine learning backend task.

## Project Overview

The task is to build a Flask API that predicts residential property prices from structured inputs. The benchmark solution generates synthetic housing data, trains a scikit-learn Gradient Boosting model, stores prediction history in SQLite, and exposes REST endpoints for prediction, history, and health checks.

The repository is designed for side-by-side evaluation of two model responses using a clear prompt, a reusable justification framework, and an executable golden reference implementation.

## Repository Structure

```text
.
+-- prompt.md              # Original domain-specific coding prompt
+-- justification.md       # Side-by-side evaluation framework
+-- golden_response/       # Production-quality reference implementation
|   +-- golden_response.py
|   +-- requirements.txt
|   +-- house_price_model.joblib
+-- README.md              # Setup, running, and evaluation notes
```

The submitted GitHub repository should contain the prompt, justification, README, and one `golden_response/` folder with the executable code.

## Requirements

Python 3.9 or newer is recommended.

Install dependencies:

```bash
pip install flask flask-cors scikit-learn pandas numpy joblib
```

On this machine, Python was installed at:

```text
C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe
```

## Run the Golden Response

From the repository root:

```bash
cd golden_response
python golden_response.py
```

The app starts on:

```text
http://localhost:5000
```

On first run, the script will:

1. Generate a synthetic housing dataset.
2. Train the model.
3. Print MAE, RMSE, and R2 metrics.
4. Save the model as `house_price_model.joblib`.
5. Create a SQLite database named `predictions.db`.
6. Start the Flask API.

## API Endpoints

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Predict

```bash
curl -X POST http://localhost:5000/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"square_footage\":2400,\"bedrooms\":4,\"bathrooms\":3,\"location\":\"Suburban\",\"year_built\":2015,\"garage\":true}"
```

Example response shape:

```json
{
  "success": true,
  "data": {
    "predicted_price": 589123.45,
    "formatted_price": "$589,123.45",
    "input": {
      "square_footage": 2400.0,
      "bedrooms": 4,
      "bathrooms": 3,
      "location": "Suburban",
      "year_built": 2015,
      "garage": true
    },
    "timestamp": "2026-05-25T12:00:00+00:00"
  },
  "error": null
}
```

### History

```bash
curl "http://localhost:5000/api/history?limit=10&offset=0"
```

## Testing the Code

Basic runtime checks:

```bash
cd golden_response
python -m py_compile golden_response.py
python golden_response.py
```

Manual API checks:

1. Start the server.
2. Call `/api/health`.
3. Call `/api/predict` with valid input.
4. Call `/api/predict` with missing or invalid fields and confirm HTTP 400.
5. Call `/api/history`.

## Evaluation Methodology

Use `justification.md` to compare two LLM responses against the prompt. The evaluation emphasizes:

- Prompt compliance.
- Runtime correctness.
- Machine learning pipeline quality.
- API design.
- Validation and error handling.
- SQLite persistence.
- Maintainability.
- Documentation quality.

The file `golden_response/golden_response.py` acts as the benchmark reference. A submitted response does not need to be identical to it, but it should meet the same explicit constraints and comparable production-quality expectations.

## GitHub Submission

The required final submission should be a GitHub repository containing:

- `prompt.md`
- `justification.md`
- `golden_response/`
- `README.md`

After pushing the repository, submit the GitHub repository URL.
