from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from forecasting.population_forecast import forecast_population_linear, forecast_population_arima
from analytics.risk_clustering import cluster_demographic_risks, assign_risk_categories
from forecasting.healthcare_demand import forecast_healthcare_demand
from analytics.insights import generate_all_insights
from backend.processing import load_census_data

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "sample_data" / "census_data.csv"

app = FastAPI(
    title="Population Health Intelligence API",
    description="Explainable community-level population growth, risk, and healthcare demand forecasts.",
    version="0.1.0",
)

# Load the census dataset once on startup
census_df = load_census_data(DATA_PATH)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Population Health Intelligence API is running."}


@app.get("/population-forecast")
def get_population_forecast(years: int = 5):
    """Return population growth forecasts for all regions."""
    # Use linear regression for all regions
    all_forecasts = []
    for region_id in census_df['region_id'].unique():
        forecast_df = forecast_population_linear(census_df, region_id, forecast_years=years)
        if not forecast_df.empty:
            all_forecasts.append(forecast_df)

    if all_forecasts:
        combined_forecast = pd.concat(all_forecasts, ignore_index=True)
        return JSONResponse(content={"forecast": combined_forecast.to_dict(orient="records")})
    return JSONResponse(content={"forecast": []})


@app.get("/risk-clusters")
def get_risk_clusters():
    """Return demographic risk clusters."""
    latest_data = census_df.sort_values(['region_id', 'year']).groupby('region_id').tail(1).reset_index(drop=True)
    clusters, cluster_labels = cluster_demographic_risks(latest_data)
    categories = assign_risk_categories(cluster_labels)

    # Format response
    cluster_summary = []
    for cluster_id in clusters['risk_cluster'].unique():
        cluster_data = clusters[clusters['risk_cluster'] == cluster_id]
        cluster_summary.append({
            "cluster_id": int(cluster_id),
            "community_count": len(cluster_data),
            "average_age_risk": float(cluster_data['elderly_ratio'].mean()),
            "average_density_risk": float(cluster_data['population_density'].mean()),
            "average_population_per_health_worker": 1000.0  # Placeholder
        })

    return JSONResponse(content={"clusters": cluster_summary})


@app.get("/healthcare-demand")
def get_healthcare_demand(years: int = 5):
    """Return healthcare demand forecasts."""
    demand_forecast = forecast_healthcare_demand(census_df, forecast_years=years)
    return JSONResponse(content={"demand_forecast": demand_forecast.to_dict(orient="records")})


@app.get("/insights")
def get_insights(years: int = 5):
    """Return AI-generated policy insights."""
    # Generate required data
    forecasts_df = pd.DataFrame()
    for region_id in census_df['region_id'].unique():
        forecast_df = forecast_population_linear(census_df, region_id, forecast_years=years)
        if not forecast_df.empty:
            forecasts_df = pd.concat([forecasts_df, forecast_df], ignore_index=True)

    latest_data = census_df.sort_values(['region_id', 'year']).groupby('region_id').tail(1).reset_index(drop=True)
    _, cluster_labels = cluster_demographic_risks(latest_data)
    risk_categories = assign_risk_categories(cluster_labels)

    demand_forecasts = forecast_healthcare_demand(census_df, forecast_years=years)

    insights = generate_all_insights(census_df, forecasts_df, risk_categories, demand_forecasts)
    return JSONResponse(content={"insights": insights})
