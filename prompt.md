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
├── golden_response/
│   ├── golden_response.py
│   ├── requirements.txt
│   └── house_price_model.joblib
└── README.md
```

## FEATURES REQUIRED

### 1. MACHINE LEARNING MODEL

The application should:

- Generate a synthetic housing dataset if no trained model exists — allows the app to train a realistic model even when external data is unavailable.
- Use at least `10,000` samples — provides enough variety for a stable regression model.
- Train a `GradientBoostingRegressor` — delivers strong predictive performance for structured housing data.
- Use a scikit-learn `Pipeline` — keeps preprocessing and modeling bundled together for reliability.
- Use a `ColumnTransformer` — applies different preprocessing steps to numeric and categorical features cleanly.
- Apply `StandardScaler` to numeric features — normalizes scale so numeric variables contribute fairly to the model.
- Apply `OneHotEncoder` to categorical location data — converts location values into numeric features the model can use.
- Save the trained model using `joblib` — persists the model artifact for reuse without retraining.
- Load the model once when the application starts — improves response time by avoiding repeated model loading.
- Print model metrics during startup — verifies training success and helps diagnose model quality.
- Achieve an `R2` score of at least `0.85` on a held-out test set — sets a measurable quality threshold for predictions.

### 2. BACKEND API

Create a Flask REST API with these endpoints:

- `GET /api/health` — returns service status and model health metadata.
- `POST /api/predict` — accepts house details and returns a predicted price.
- `GET /api/history` — returns stored prediction history in paginated form.

The backend should:

- Return structured JSON responses — ensures frontend clients can parse success and error payloads consistently.
- Validate all user input — avoids invalid predictions and protects the model from bad data.
- Store prediction history — enables later review and auditing of past estimates.
- Handle malformed JSON — returns a clear error instead of crashing when requests are invalid.
- Handle unknown routes — keeps the API predictable and user-friendly.
- Handle unexpected server errors — responds safely to failures without leaking internal details.
- Include basic rate limiting for prediction requests — prevents abuse and protects service stability.

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

- Square footage input — collects the primary size feature used for price estimation.
- Bedrooms input — captures home size and market demand information.
- Bathrooms input — reflects layout and value-related house features.
- Location dropdown — constrains input to supported categorical location zones.
- Year built input — measures home age as a predictive feature.
- Garage checkbox or toggle — indicates whether the property includes parking.
- Predict price button — submits the form to the backend prediction API.
- Loading state — shows users the request is in progress.
- Error messages — surface input or backend validation problems clearly.
- Predicted price result card — displays the final estimate in a polished format.

### 4. INPUT VALIDATION

Validate all required fields and return HTTP `400` with a descriptive message for invalid input.

Required ranges:

- `square_footage`: `500` to `10000` — ensures size values are realistic for residential homes.
- `bedrooms`: `1` to `10` — keeps bedroom counts within typical house limits.
- `bathrooms`: `1` to `6` — represents reasonable bathroom configurations.
- `year_built`: `1900` to `2026` — prevents invalid or future construction dates.

Allowed locations:

- `Downtown` — central urban market area.
- `Suburban` — medium-density suburban region.
- `Rural` — low-density countryside market.
- `Urban` — general city neighborhoods.
- `Waterfront` — premium properties near water.

### 5. DASHBOARD WEBSITE

Create a modern dashboard interface with:

- Sidebar navigation — lets users switch between dashboard views easily.
- Dashboard home — provides a central landing page for key stats and controls.
- Price prediction form — lets users submit house details directly from the dashboard.
- Prediction result section — displays the estimate without leaving the page.
- Total predictions stat — summarizes usage volume for quick insights.
- Average predicted price stat — gives a snapshot of predicted market value.
- Recent predictions — surfaces the latest prediction activity.
- Location/category insights — helps users compare results across market segments.
- Model health section — shows whether the predictive system is functioning properly.
- Search prediction history — enables finding past estimates quickly.
- Settings page — offers environment and display configuration options.
- Help/About page — provides project context and user guidance.
- Responsive design — makes the dashboard usable on mobile and desktop.
- Dark/light theme toggle — offers a personalized visual experience.
- Smooth animations — improves perceived polish and usability.

### 6. PREDICTION MANAGEMENT

Users should be able to:

- Submit house details — create new prediction requests from the dashboard.
- View predicted price — see the numeric output of the model immediately.
- View formatted price — understand the result in a user-friendly currency format.
- View original input used for prediction — verify the parameters that generated the estimate.
- View prediction timestamp — know when each estimate was created.
- Browse prediction history — review past predictions in one place.
- Search history — find prior estimates by keywords or location.
- Filter history by location — narrow results to a specific market zone.
- Sort predictions by date or price — compare values in a meaningful order.
- Clear or manage local UI state — reset the interface without losing backend history.

### 7. DATA STORAGE

Store prediction history in SQLite.

The database should:

- Create tables automatically — initialize persistence without manual setup.
- Store each prediction with input values — retain the full request context for audits.
- Store predicted price — save model results for later review.
- Store timestamp — track when each prediction occurred.
- Use parameterized SQL queries — prevent SQL injection and keep data safe.
- Return history from newest to oldest — show the most recent activity first.
- Support pagination with `limit` and `offset` — avoid loading too much history at once.
- Enforce a maximum history limit of `100` — keep storage bounded and performant.

### 8. FRONTEND API INTEGRATION

The frontend should:

- Call the Flask backend using `fetch` — perform AJAX requests from the browser to the REST API.
- Show loading spinners while requests are running — give the user feedback that the app is working.
- Show toast notifications for success and errors — surface immediate status messages without interrupting workflow.
- Refresh prediction history after each successful prediction — keep the dashboard data current.
- Validate form values before sending requests — catch simple mistakes early and reduce invalid API calls.
- Display backend validation errors clearly — translate server responses into helpful UI messages.
- Use a configurable backend API URL — support different deployment environments easily.

### 9. MODERN UI REQUIREMENTS

UI should look modern and professional:

- Rounded corners — soften the overall visual design for a contemporary feel.
- Smooth hover effects — improve interactivity and polish.
- Soft shadows — add subtle depth to cards and panels.
- Clean typography — make the interface easier to scan and read.
- Responsive layout — ensure the app works well on desktop and mobile.
- Dashboard cards — structure information into digestible visual blocks.
- Clear form spacing — prevent the UI from feeling cramped.
- Elegant result display — make prediction output feel important and easy to understand.
- Helpful empty states — guide users when no data is available.
- Polished error and loading states — maintain trust when the app is busy or fails.
- Dark/light theme support — offer a modern, customizable experience.

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

- `success` — indicates whether the request succeeded.
- `data.predicted_price` — the numeric model prediction.
- `data.formatted_price` — a human-readable price string.
- `data.input` — the original validated input used for prediction.
- `data.timestamp` — the ISO timestamp when the prediction was created.
- `error` — provides meaningful failure details when the request fails.

### 11. HEALTH CHECK REQUIREMENTS

`GET /api/health` should report:

- Service status — whether the API is running normally.
- Model load status — confirms the ML model is ready to serve predictions.
- Uptime — indicates how long the service has been running.
- Model metrics — provides health signals from training or evaluation.
- Current timestamp — offers a reference time for diagnostics.

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
├── golden_response/
│   ├── golden_response.py
│   ├── requirements.txt
│   └── house_price_model.joblib
└── README.md
```

### 13. SECURITY AND RELIABILITY

The application should include:

- Input validation — protects the service from invalid or harmful data.
- Basic input sanitization — avoids injection risks and malformed payloads.
- Parameterized SQLite queries — prevents SQL injection attacks.
- CORS setup — controls which frontend origins can access the API.
- Structured error handling — keeps responses consistent and debuggable.
- Basic rate limiting — reduces the chance of overload from repeated requests.
- Safe model loading — avoids crashes or stale model states at startup.
- No retraining per request — keeps the API responsive and predictable.
- No raw stack traces in API responses — prevents leaking internal implementation details.

### 14. EXTRA FEATURES

Add useful optional features:

- Export prediction history — lets users download their stored predictions for offline review.
- Clear history button — provides a way to reset local UI state or remove old entries.
- Model metrics visualization — helps users understand model performance at a glance.
- Prediction trend chart — shows how estimates change over time.
- Location-based average prices — highlights geographic pricing patterns.
- Recent activity feed — surfaces the most recent prediction actions.
- Copy prediction result — makes it easy to reuse the estimate elsewhere.
- Print or download estimate — supports sharing or documentation of results.
- Mobile responsive dashboard — ensures the feature set works on phones and tablets.

### 15. UI DIFFERENCE

The house price prediction app should feel like a modern PropTech analytics tool:

- Use a polished real estate dashboard style — communicate professionalism and trust.
- Use a different color palette from generic templates — make the app stand out visually.
- Use better spacing and typography — improve readability and user focus.
- Make the prediction result visually prominent — highlight the most important output.
- Keep charts and stats easy to scan — ensure data is accessible at a glance.
- Make the form simple for real estate agents to use quickly — reduce friction in data entry.

### 16. CODE REQUIREMENTS

Write clean, beginner-friendly, modular code:

- Use clear function names — make the code readable and self-explanatory.
- Add helpful comments — clarify intent and business logic.
- Use type hints for public helper functions — improve developer confidence and editor support.
- Add docstrings to public functions — document usage and expected behavior.
- Keep configuration values near the top — make environment settings easy to find.
- Separate API, validation, model, and database logic where possible — improve maintainability and testability.
- Use async frontend request handling where appropriate — keep the UI responsive during network calls.
- Keep the code easy for another engineer to run locally — reduce onboarding friction for future developers.

### 17. FINAL OUTPUT REQUIRED

Provide:

- Complete project code — full source files for the backend, frontend, and supporting scripts.
- Folder structure — a clear directory layout for the complete application.
- Setup instructions — how to install dependencies and prepare the project.
- Backend run instructions — commands to start the Flask API.
- Frontend run instructions — commands to launch or serve the UI.
- SQLite/database explanation — details on how prediction history is stored and accessed.
- Model training explanation — how the ML model is generated, evaluated, and persisted.
- API endpoint documentation — request/response shapes for each backend route.
- Example request and response bodies — sample JSON payloads for integration testing.
- Evaluation methodology — how the model and application success are measured.
- Deployment notes — guidance for running the application in production.

## DEVELOPMENT FLOW

Build the project step-by-step starting from:

1. Backend setup — establish the Flask app and project dependencies.
2. Dataset generation — create or load the housing data used for training.
3. Machine learning pipeline — build preprocessing and regression model logic.
4. Model persistence — save the trained model artifact for reuse.
5. SQLite prediction history — set up persistence for past predictions.
6. Prediction API — add the endpoint that returns model estimates.
7. Health API — expose service and model health information.
8. History API — provide paginated access to stored prediction records.
9. Frontend prediction form — build the user interface for submitting predictions.
10. Dashboard interface — create the analytics and history view.
11. Frontend and backend integration — wire UI requests to the Flask API.
12. Error handling and validation — ensure robustness for bad data and failures.
13. Final polishing and testing — refine UX and verify the complete experience.

## FINAL GOAL

The final project should work as a complete production-ready house price prediction web application with:

- Machine learning price prediction — deliver actual numeric home-value estimates.
- Flask REST API — provide the backend service layer for prediction and history.
- Modern responsive dashboard — present results in a polished, mobile-friendly UI.
- Prediction history — preserve past estimates for review and auditing.
- SQLite persistence — store history reliably in a lightweight local database.
- Model metrics — surface model quality and health information.
- Strong validation — protect the app from invalid inputs and misuse.
- Structured JSON responses — ensure consistent API output across endpoints.
- Clear setup documentation — make it easy for others to install and run the app.
- Clean maintainable code — keep the codebase readable and easy to extend.
 
