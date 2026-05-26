# Full-Stack House Price Prediction Web Application

## Project Overview

Build a full-stack House Price Prediction Web Application for a real estate analytics workflow.

The project should include:

- Clean modern UI — makes the app easy to use and visually appealing for real estate users.
- Machine learning price prediction — delivers automated home-value estimates from input features.
- REST API backend — allows the frontend to request predictions and history from a central service.
- Prediction dashboard — provides a visual workspace for users to review results and trends.
- Prediction history storage — preserves past predictions for auditing and comparison.
- Model training and persistence — creates a reusable trained model that can be loaded without retraining.
- Input validation and error handling — protects the application from invalid data and improves reliability.

## Objective

Define the primary goal of the project, success criteria, and measurable targets.

- Goal: Build a production-ready full-stack house price prediction web application.
- Success Criteria: Working Flask API, trained ML model persisted to disk, responsive frontend, prediction history persisted in SQLite, and reproducible setup steps.
- Measurable Targets: Achieve R2 >= 0.85 on a held-out test set; handle at least 100 concurrent requests with graceful degradation; enforce a max history of 100 entries per the database constraint.

## Input / Output

Input schema (JSON) for prediction requests:

- `square_footage` (int): 500 - 10000
- `bedrooms` (int): 1 - 10
- `bathrooms` (int): 1 - 6
- `location` (str): one of ["Downtown", "Suburban", "Rural", "Urban", "Waterfront"]
- `year_built` (int): 1900 - 2026
- `garage` (bool)

Output envelope (JSON):

```json
{
  "success": true,
  "data": {
    "predicted_price": 123456.78,
    "formatted_price": "$123,456.78",
    "input": { /* original input */ },
    "timestamp": "2026-05-26T12:34:56Z"
  },
  "error": null
}
```

## Input Validation

The backend and frontend must validate each prediction request before processing:

- `square_footage` is required, must be an integer, and must be between `500` and `10000`.
- `bedrooms` is required, must be an integer, and must be between `1` and `10`.
- `bathrooms` is required, must be an integer, and must be between `1` and `6`.
- `location` is required and must be one of: `Downtown`, `Suburban`, `Rural`, `Urban`, `Waterfront`.
- `year_built` is required, must be an integer, and must be between `1900` and `2026`.
- `garage` is required and must be a boolean.
- Requests with missing or invalid fields must return HTTP `400` with a structured `error` payload describing the invalid fields.
- The frontend should show clear inline validation errors before sending API requests.

## Contracts

API contracts and shapes:

- `GET /api/health` -> `{ success, data: { status, model_loaded, uptime, metrics }, error }`
- `POST /api/predict` -> Accepts the input schema above; returns the standard output envelope with `data.predicted_price`, `data.formatted_price`, `data.input`, and `data.timestamp`.
- `GET /api/history?limit=&offset=` -> Returns paginated history: `{ success, data: { items: [...], total, limit, offset }, error }`

All endpoints return `400` for validation errors with `{ success: false, data: null, error: { message, details? } }` and `500` for unexpected server errors.

## Data

- Primary dataset: synthetic housing dataset (generate when no model exists) with at least 10,000 samples.
- Fields: square_footage, bedrooms, bathrooms, location, year_built, garage, sale_price.
- Storage: CSV during development; SQLite for prediction history; `joblib` for model artifacts.

## Data Preprocessing

- Impute or reject missing values according to strict validation rules.
- Clip numeric features to allowed ranges.
- Engineer derived features if beneficial (e.g., `age = current_year - year_built`).
- Use `ColumnTransformer` to apply `StandardScaler` to numeric features and `OneHotEncoder` to `location`.
- Train/test split (e.g., 80/20) with a fixed random seed for reproducibility.

## Performance & Scalability

- Load the trained model once at application startup; avoid retraining on requests.
- Use gunicorn or a WSGI server in production behind a reverse proxy.
- Add caching for frequent identical predictions if necessary.
- SQLite is acceptable for local/small-scale use; for higher scale, migrate to Postgres or another RDBMS.
- Baseline concurrency target: handle 100 simultaneous requests with graceful degradation (queueing, rate limiting).

## Constraints

- Model must achieve R2 >= 0.85 on a held-out test set.
- Minimum dataset size: 10,000 samples when generating synthetic data.
- Prediction input ranges and allowed location values are enforced.
- Prediction history capped at 100 entries; oldest entries are purged when the limit is reached.

## Error Handling

- Validate request JSON; return `400` with structured error details on validation failure.
- Return `422` for semantically invalid requests when appropriate.
- Catch unexpected exceptions and return `500` with a generic error message; never expose raw stack traces.
- Handle database errors gracefully; on transient DB failures, return `503` with retry-friendly messages.

## Output

- Primary output: `data.predicted_price` (float) and `data.formatted_price` (string).
- Include the original sanitized `data.input` in responses for reproducibility.
- Include an ISO 8601 `data.timestamp` for each prediction.


## Tech Stack

- Python — backend language for model training and API development.
- Flask — web framework used to build the prediction and health endpoints.
- HTML — structure the frontend pages and form content.
- CSS — style the dashboard for a modern, responsive experience.
- Vanilla JavaScript — handle form interaction and API requests from the browser.
- scikit-learn — build, train, and evaluate the regression model.
- pandas — load, clean, and prepare the dataset for training and inference.
- numpy — support numeric operations and feature engineering.
- joblib — persist the trained model to disk and load it at startup.
- SQLite — store prediction history locally for fast, lightweight persistence.
- REST APIs — define the communication contract between frontend and backend.

## Project Structure

Create a clear project structure:

```text
project-root/
│
├── backend/       -> Flask API and ML model logic
├── frontend/      -> House price prediction web interface
├── data/          -> Generated dataset or database files
├── models/        -> Saved ML model files
└── docs/          -> Setup and usage documentation
```

For a simplified single-file benchmark version, the backend may be delivered as:

```text
project-root/
│
├── prompt.md
├── justification.md
├── golden_response.py
└── README.md
```

## FEATURES REQUIRED

### 1. MACHINE LEARNING MODEL

The application should:

- Generate a synthetic housing dataset if no trained model exists
- Use at least `10,000` samples
- Train a `GradientBoostingRegressor`
- Use a scikit-learn `Pipeline`
- Use a `ColumnTransformer`
- Apply `StandardScaler` to numeric features
- Apply `OneHotEncoder` to categorical location data
- Save the trained model using `joblib`
- Load the model once when the application starts
- Print model metrics during startup
- Achieve an `R2` score of at least `0.85` on a held-out test set

### 2. BACKEND API

Create a Flask REST API with these endpoints:

- `GET /api/health`
- `POST /api/predict`
- `GET /api/history`

The backend should:

- Return structured JSON responses
- Validate all user input
- Store prediction history
- Handle malformed JSON
- Handle unknown routes
- Handle unexpected server errors
- Include basic rate limiting for prediction requests

### 3. HOUSE PRICE PREDICTION FORM

The prediction form should accept:

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

The form should include:

- Square footage input
- Bedrooms input
- Bathrooms input
- Location dropdown
- Year built input
- Garage checkbox or toggle
- Predict price button
- Loading state
- Error messages
- Predicted price result card

### 4. INPUT VALIDATION

Validate all required fields and return HTTP `400` with a descriptive message for invalid input.

Required ranges:

- `square_footage`: `500` to `10000`
- `bedrooms`: `1` to `10`
- `bathrooms`: `1` to `6`
- `year_built`: `1900` to `2026`

Allowed locations:

- `Downtown`
- `Suburban`
- `Rural`
- `Urban`
- `Waterfront`

### 5. DASHBOARD WEBSITE

Create a modern dashboard interface with:

- Sidebar navigation
- Dashboard home
- Price prediction form
- Prediction result section
- Total predictions stat
- Average predicted price stat
- Recent predictions
- Location/category insights
- Model health section
- Search prediction history
- Settings page
- Help/About page
- Responsive design
- Dark/light theme toggle
- Smooth animations

### 6. PREDICTION MANAGEMENT

Users should be able to:

- Submit house details
- View predicted price
- View formatted price
- View original input used for prediction
- View prediction timestamp
- Browse prediction history
- Search history
- Filter history by location
- Sort predictions by date or price
- Clear or manage local UI state

### 7. DATA STORAGE

Store prediction history in SQLite.

The database should:

- Create tables automatically
- Store each prediction with input values
- Store predicted price
- Store timestamp
- Use parameterized SQL queries
- Return history from newest to oldest
- Support pagination with `limit` and `offset`
- Enforce a maximum history limit of `100`

### 8. FRONTEND API INTEGRATION

The frontend should:

- Call the Flask backend using `fetch`
- Show loading spinners while requests are running
- Show toast notifications for success and errors
- Refresh prediction history after each successful prediction
- Validate form values before sending requests
- Display backend validation errors clearly
- Use a configurable backend API URL

### 9. MODERN UI REQUIREMENTS

UI should look modern and professional:

- Rounded corners
- Smooth hover effects
- Soft shadows
- Clean typography
- Responsive layout
- Dashboard cards
- Clear form spacing
- Elegant result display
- Helpful empty states
- Polished error and loading states
- Dark/light theme support

### 10. API RESPONSE FORMAT

Return all API responses using this JSON envelope:

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

The prediction response must include:

- `success`
- `data.predicted_price`
- `data.formatted_price`
- `data.input`
- `data.timestamp`
- `error`

### 11. HEALTH CHECK REQUIREMENTS

`GET /api/health` should report:

- Service status
- Model load status
- Uptime
- Model metrics
- Current timestamp

### 12. FILES TO CREATE

BACKEND:

```text
backend/
│
├── app.py
├── config.py
├── model.py
├── database.py
├── validation.py
├── requirements.txt
└── README.md
```

FRONTEND:

```text
frontend/
│
├── index.html
├── styles.css
├── app.js
├── dashboard.html
├── settings.html
└── help.html
```

SIMPLIFIED BENCHMARK VERSION:

```text
project-root/
│
├── prompt.md
├── justification.md
├── golden_response.py
└── README.md
```

### 13. SECURITY AND RELIABILITY

The application should include:

- Input validation
- Basic input sanitization
- Parameterized SQLite queries
- CORS setup
- Structured error handling
- Basic rate limiting
- Safe model loading
- No retraining per request
- No raw stack traces in API responses

### 14. EXTRA FEATURES

Add useful optional features:

- Export prediction history
- Clear history button
- Model metrics visualization
- Prediction trend chart
- Location-based average prices
- Recent activity feed
- Copy prediction result
- Print or download estimate
- Mobile responsive dashboard

### 15. UI DIFFERENCE

The house price prediction app should feel like a modern PropTech analytics tool:

- Use a polished real estate dashboard style
- Use a different color palette from generic templates
- Use better spacing and typography
- Make the prediction result visually prominent
- Keep charts and stats easy to scan
- Make the form simple for real estate agents to use quickly

### 16. CODE REQUIREMENTS

Write clean, beginner-friendly, modular code:

- Use clear function names
- Add helpful comments
- Use type hints for public helper functions
- Add docstrings to public functions
- Keep configuration values near the top
- Separate API, validation, model, and database logic where possible
- Use async frontend request handling where appropriate
- Keep the code easy for another engineer to run locally

### 17. FINAL OUTPUT REQUIRED

Provide:

- Complete project code
- Folder structure
- Setup instructions
- Backend run instructions
- Frontend run instructions
- SQLite/database explanation
- Model training explanation
- API endpoint documentation
- Example request and response bodies
- Evaluation methodology
- Deployment notes

## DEVELOPMENT FLOW

Build the project step-by-step starting from:

1. Backend setup
2. Dataset generation
3. Machine learning pipeline
4. Model persistence
5. SQLite prediction history
6. Prediction API
7. Health API
8. History API
9. Frontend prediction form
10. Dashboard interface
11. Frontend and backend integration
12. Error handling and validation
13. Final polishing and testing

## FINAL GOAL

The final project should work as a complete production-ready house price prediction web application with:

- Machine learning price prediction
- Flask REST API
- Modern responsive dashboard
- Prediction history
- SQLite persistence
- Model metrics
- Strong validation
- Structured JSON responses
- Clear setup documentation
- Clean maintainable code
 
