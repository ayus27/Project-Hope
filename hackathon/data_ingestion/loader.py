import pandas as pd
from pathlib import Path


def load_census_data(csv_path: str | Path) -> pd.DataFrame:
    """
    Load census CSV data with basic validation.

    Validates:
    - Missing values in critical columns
    - Negative numbers in population/area columns
    - Inconsistent totals (age groups should sum to total_population)

    Returns cleaned DataFrame.
    """
    df = pd.read_csv(csv_path)

    # Basic validation
    required_columns = ['region_id', 'region_name', 'year', 'total_population', 'age_0_14', 'age_15_59', 'age_60_plus', 'area_sq_km']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Check for missing values in critical columns
    critical_cols = ['region_id', 'year', 'total_population', 'area_sq_km']
    for col in critical_cols:
        if df[col].isnull().any():
            raise ValueError(f"Missing values found in critical column: {col}")

    # Check for negative values
    numeric_cols = ['total_population', 'age_0_14', 'age_15_59', 'age_60_plus', 'area_sq_km']
    for col in numeric_cols:
        if (df[col] < 0).any():
            raise ValueError(f"Negative values found in column: {col}")

    # Validate age group totals
    df['calculated_total'] = df['age_0_14'] + df['age_15_59'] + df['age_60_plus']
    tolerance = 0.01 * df['total_population']  # Allow 1% tolerance for rounding
    inconsistent = ~df['calculated_total'].between(df['total_population'] - tolerance, df['total_population'] + tolerance)
    if inconsistent.any():
        bad_rows = df[inconsistent][['region_id', 'year', 'total_population', 'calculated_total']]
        raise ValueError(f"Inconsistent age totals in rows:\n{bad_rows}")

    # Clean up and sort
    df = df.drop(columns=['calculated_total'])
    df['year'] = df['year'].astype(int)
    df = df.sort_values(['region_id', 'year']).reset_index(drop=True)

    return df