# नेपाल जनसंख्या स्वास्थ्य बुद्धिमत्ता मंच

# Nepal Population Health Intelligence Platform

An AI-powered Population Health Intelligence Platform for Nepal government planning.

## Team Members

- [Aayush Aman Shah] (@ayus27)
- [Shoovam Shrestha] (@shuvamshresthadmk-ctrl)
- [Hermit Shrestha] (@hermitstha)
- [Iyus Basnet] (@iyusbasnet)

## Problem Statement

Nepal faces significant challenges in healthcare planning due to rapid urbanization, demographic shifts, and limited resources. The government needs accurate population forecasts and healthcare demand projections to allocate resources effectively across districts and regions. Current planning relies on outdated census data and manual estimates, leading to inefficient resource distribution and potential gaps in healthcare coverage.

Key challenges:

- Inaccurate population growth predictions
- Lack of demographic risk analysis
- Insufficient healthcare workforce planning
- No integrated platform for policy-level insights

## Solution Description

Our AI-powered Population Health Intelligence Platform addresses these challenges by:

1. **Population Forecasting**: Using machine learning models (Linear Regression and ARIMA) to predict population growth at district/regional levels
2. **Demographic Risk Analysis**: Clustering regions based on demographic risk factors (age distribution, population density, growth rates)
3. **Healthcare Demand Forecasting**: Projecting future needs for hospitals, clinics, healthcare workers, and vaccines
4. **Interactive Dashboard**: Streamlit-based interface for policy makers to explore insights and make data-driven decisions
5. **REST API**: FastAPI backend providing programmatic access to all analytics

The platform uses integrated census data to provide explainable, non-clinical policy-level insights for the Nepal Ministry of Health.

## Tech Stack

- **Backend**: Python 3.8+, FastAPI, Uvicorn
- **Frontend/Dashboard**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (Linear Regression, KMeans clustering), Statsmodels (ARIMA)
- **Visualization**: Altair (via Streamlit)
- **Deployment**: Docker-ready for containerization

## Goals

- Predict population growth at district/regional level across Nepal
- Identify demographic risk patterns (age-based, density-based, migration patterns)
- Forecast future healthcare demand for Nepali regions (hospitals, clinics, workforce, vaccines)
- Provide explainable, non-clinical policy-level insights for Nepal Ministry of Health

## Project Structure

- `data_ingestion/` — Load and validate census CSV data with comprehensive checks
- `feature_engineering/` — Calculate demographic features (density, age ratios, growth rates)
- `ml_models/` — Store trained machine learning models and serialization
- `forecasting/` — Population growth and healthcare demand forecasting (linear regression, ARIMA)
- `analytics/` — Demographic risk clustering and AI-generated insights
- `api/` — FastAPI backend with REST endpoints for all analytics
- `dashboard/` — Streamlit interactive dashboard for policy planning
- `sample_data/` — Aggregated census sample data and schema examples
- `requirements.txt` — Python dependencies

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd hackathon
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start both backend and dashboard with a single command:

   ```bash
   python run.py
   ```

   This will start:
   - FastAPI backend on http://localhost:8000
   - Streamlit dashboard on http://localhost:8502

2. Alternatively, run them separately:

   Backend API:

   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

   Dashboard:

   ```bash
   streamlit run dashboard/app.py --server.port 8501
   ```

Screenshots:

- [Dashboard Overview](demo/Dashboard.png)
- [Population Forecast](demo/population-forecast-data.png)
- [Risk Analysis](demo/risk-analysis.png)

## API Endpoints

- `GET /health` — Health check
- `GET /population-forecast?years=5` — Population growth forecasts
- `GET /risk-clusters` — Demographic risk clusters
- `GET /healthcare-demand?years=5` — Healthcare demand projections
- `GET /insights?years=5` — AI-generated policy insights

## Disclaimer

This platform provides population-level planning insights using aggregated data from Nepal census records.
It does not make individual clinical decisions and does not replace expert judgment by Nepal's Ministry of Health or local health authorities.
