from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from data_ingestion.loader import load_census_data
from feature_engineering.features import engineer_features
from forecasting.population_forecast import forecast_all_regions
from analytics.risk_clustering import cluster_demographic_risks, assign_risk_categories
from forecasting.healthcare_demand import forecast_healthcare_demand
from analytics.insights import generate_all_insights

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "sample_data" / "census_data.csv"

app = FastAPI(
    title="नेपाल जनसंख्या स्वास्थ्य बुद्धिमत्ता API",
    description="""
    Nepal Population Health Intelligence API

    This platform provides population-level planning insights using aggregated census data from Nepal.
    It does not make individual clinical decisions and does not replace expert judgment by Nepal's Ministry of Health.

    All forecasts and insights are advisory and intended for policy planning purposes only.
    """,
    version="0.1.0",
)

# Load and prepare data on startup
census_df = load_census_data(DATA_PATH)
features_df = engineer_features(census_df)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Population Health Intelligence API is running."}


@app.get("/population-forecast")
def get_population_forecast(years: int = 5):
    """
    Get population growth forecasts for all regions.

    - **years**: Number of years to forecast (default: 5)
    """
    forecasts = forecast_all_regions(census_df, forecast_years=years)
    return JSONResponse(content={
        "forecasts": forecasts.to_dict(orient="records") if not forecasts.empty else []
    })


@app.get("/risk-clusters")
def get_risk_clusters():
    """
    Get demographic risk clusters and categories for all regions.
    """
    clustered_data, cluster_labels = cluster_demographic_risks(features_df)
    risk_categories = assign_risk_categories(cluster_labels)

    return JSONResponse(content={
        "regions": clustered_data[['region_id', 'region_name', 'risk_cluster']].to_dict(orient="records"),
        "categories": risk_categories
    })


@app.get("/healthcare-demand")
def get_healthcare_demand(years: int = 5):
    """
    Get healthcare demand forecasts for all regions.

    - **years**: Number of years to forecast (default: 5)
    """
    demands = forecast_healthcare_demand(census_df, forecast_years=years)
    return JSONResponse(content={"demands": demands})


@app.get("/insights")
def get_insights(years: int = 5):
    """
    Get AI-generated plain-English insights for policymakers.

    - **years**: Number of years for projections (default: 5)
    """
    forecasts = forecast_all_regions(census_df, forecast_years=years)
    _, cluster_labels = cluster_demographic_risks(features_df)
    risk_categories = assign_risk_categories(cluster_labels)
    demands = forecast_healthcare_demand(census_df, forecast_years=years)

    insights = generate_all_insights(census_df, forecasts, risk_categories, demands)

    return JSONResponse(content={"insights": insights})