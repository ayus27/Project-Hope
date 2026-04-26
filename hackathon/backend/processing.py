import pandas as pd
from pathlib import Path


def load_census_data(csv_path: str | Path) -> pd.DataFrame:
    """Load aggregated census CSV data into a pandas DataFrame."""
    df = pd.read_csv(csv_path)
    df["year"] = df["year"].astype(int)
    df = df.sort_values(["region_id", "year"]).reset_index(drop=True)
    return df


def prepare_community_features(df: pd.DataFrame) -> pd.DataFrame:
    """Construct engineered features for each community-year record."""
    feature_df = df.copy()
    feature_df["age_risk_index"] = (
        (feature_df["age_0_14"] / feature_df["total_population"]) * 0.4 + (feature_df["age_60_plus"] / feature_df["total_population"]) * 0.6
    )
    feature_df["density_risk_index"] = feature_df["total_population"] / feature_df["area_sq_km"]
    feature_df["population_per_health_worker"] = (
        feature_df["population_total"] / feature_df["healthcare_workers"].replace(0, 1)
    )
    return feature_df


def latest_community_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Return the most recent census snapshot for each community."""
    return df.sort_values(["community_id", "year"]).groupby("community_id").tail(1).reset_index(drop=True)
