from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

from backend.processing import prepare_community_features, latest_community_snapshot


def explain_linear_model(model: LinearRegression, feature_names: list[str]) -> dict[str, float]:
    """Return model coefficients for explainable interpretation."""
    return {name: float(coef) for name, coef in zip(feature_names, model.coef_)}


def predict_population_growth(df: pd.DataFrame, forecast_years: int = 5) -> tuple[pd.DataFrame, dict[str, dict[str, float]]]:
    """Train a simple linear regression per community and forecast population growth."""
    forecasts = []
    explainers: dict[str, dict[str, float]] = {}

    for community_id, group in df.groupby("region_id"):
        history = group.sort_values("year")
        X = history[["year"]].values
        y = history["total_population"].values
        if len(history) < 2:
            continue

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.array([history["year"].max() + i for i in range(1, forecast_years + 1)]).reshape(-1, 1)
        population_forecast = model.predict(future_years)

        for year, pop in zip(future_years.flatten(), population_forecast):
            forecasts.append(
                {
                    "region_id": int(community_id),
                    "region_name": history.iloc[0]["region_name"],
                    "year": int(year),
                    "predicted_population": int(round(pop)),
                }
            )

        explainers[str(int(community_id))] = explain_linear_model(model, ["year"])

    return pd.DataFrame(forecasts), explainers


def identify_risk_patterns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """Cluster communities by demographic risk and return cluster labels."""
    snapshot = latest_community_snapshot(df)
    features = prepare_community_features(snapshot)

    risk_columns = ["age_risk_index", "density_risk_index", "population_per_health_worker"]
    X = features[risk_columns].fillna(0).values

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    cluster_details = []
    for cluster_id in range(3):
        cluster_slice = features.iloc[labels == cluster_id]
        cluster_details.append(
            {
                "cluster_id": int(cluster_id),
                "community_count": int(len(cluster_slice)),
                "average_age_risk": float(cluster_slice["age_risk_index"].mean()),
                "average_density_risk": float(cluster_slice["density_risk_index"].mean()),
                "average_population_per_health_worker": float(cluster_slice["population_per_health_worker"].mean()),
            }
        )

    community_labels = {
        str(int(row["community_id"])): f"cluster_{int(label)}"
        for row, label in zip(features.to_dict(orient="records"), labels)
    }

    return pd.DataFrame(cluster_details), community_labels


def forecast_healthcare_demand(df: pd.DataFrame, forecast_years: int = 5) -> pd.DataFrame:
    """Forecast healthcare demand using simplified ratio models and population projections."""
    snapshot = latest_community_snapshot(df)
    forecast_df, _ = predict_population_growth(df, forecast_years=forecast_years)

    demand_rows = []
    for row in forecast_df.to_dict(orient="records"):
        community_id = row["community_id"]
        baseline = snapshot[snapshot["community_id"] == community_id].iloc[0]
        population_ratio = row["predicted_population"] / max(baseline["population_total"], 1)

        demand_rows.append(
            {
                "community_id": community_id,
                "community_name": row["community_name"],
                "year": row["year"],
                "predicted_population": row["predicted_population"],
                "forecast_hospitals": int(round(baseline["hospitals"] * population_ratio)),
                "forecast_clinics": int(round(baseline["clinics"] * population_ratio)),
                "forecast_healthcare_workers": int(round(baseline["healthcare_workers"] * population_ratio)),
                "forecast_vaccine_doses": int(round(baseline["vaccine_doses_administered"] * population_ratio)),
            }
        )

    return pd.DataFrame(demand_rows)
