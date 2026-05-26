# Full-Stack House Price Prediction Web Application

## Project Overview

Build a full-stack House Price Prediction Web Application for a real estate analytics workflow.

The project should include:

- Clean modern UI
- Machine learning price prediction
- REST API backend
- Prediction dashboard
- Prediction history storage
- Model training and persistence
- Input validation and error handling

## Tech Stack

- Python
- Flask
- HTML
- CSS
- Vanilla JavaScript
- scikit-learn
- pandas
- numpy
- joblib
- SQLite
- REST APIs

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
 
