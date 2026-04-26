import pandas as pd


# Configurable ratios for healthcare demand calculation
HEALTHCARE_RATIOS = {
    'hospital_beds_per_1000': 2.5,  # WHO guideline
    'clinics_per_10000': 1.0,       # Approximate ratio
    'doctors_per_1000': 1.5,        # WHO minimum
    'nurses_per_1000': 3.0,         # WHO minimum
    'vaccines_child_per_year': 0.15,  # Coverage rate for routine vaccines
    'vaccines_elderly_per_year': 0.20  # Coverage rate for elderly vaccines
}


def forecast_hospital_beds(population: int) -> int:
    """Estimate hospital beds needed based on population."""
    return int((population / 1000) * HEALTHCARE_RATIOS['hospital_beds_per_1000'])


def forecast_clinics(population: int) -> int:
    """Estimate clinics needed based on population."""
    return max(1, int((population / 10000) * HEALTHCARE_RATIOS['clinics_per_10000']))


def forecast_doctors(population: int) -> int:
    """Estimate doctors needed based on population."""
    return int((population / 1000) * HEALTHCARE_RATIOS['doctors_per_1000'])


def forecast_nurses(population: int) -> int:
    """Estimate nurses needed based on population."""
    return int((population / 1000) * HEALTHCARE_RATIOS['nurses_per_1000'])


def forecast_vaccine_demand_children(child_population: int) -> int:
    """Estimate annual vaccine doses needed for children."""
    return int(child_population * HEALTHCARE_RATIOS['vaccines_child_per_year'])


def forecast_vaccine_demand_elderly(elderly_population: int) -> int:
    """Estimate annual vaccine doses needed for elderly."""
    return int(elderly_population * HEALTHCARE_RATIOS['vaccines_elderly_per_year'])


def forecast_healthcare_demand(df: pd.DataFrame, forecast_years: int = 5) -> list[dict]:
    """
    Generate healthcare demand forecasts for all regions.
    Uses population projections and age distribution to estimate needs.
    """
    from forecasting.population_forecast import forecast_all_regions

    # Get population forecasts
    pop_forecasts = forecast_all_regions(df, forecast_years)

    if pop_forecasts.empty:
        return []

    # Get latest age distribution for each region
    latest_data = df.sort_values(['region_id', 'year']).groupby('region_id').tail(1)

    demands = []

    for _, forecast_row in pop_forecasts.iterrows():
        region_id = forecast_row['region_id']
        year = forecast_row['year']
        population = forecast_row['predicted_population']

        # Get age distribution from latest data
        region_latest = latest_data[latest_data['region_id'] == region_id].iloc[0]
        child_pop = int(population * (region_latest['age_0_14'] / region_latest['total_population']))
        elderly_pop = int(population * (region_latest['age_60_plus'] / region_latest['total_population']))

        demand = {
            'region_id': int(region_id),
            'region_name': forecast_row['region_name'],
            'year': int(year),
            'predicted_population': int(population),
            'hospital_beds_needed': forecast_hospital_beds(population),
            'clinics_needed': forecast_clinics(population),
            'doctors_needed': forecast_doctors(population),
            'nurses_needed': forecast_nurses(population),
            'vaccine_doses_children': forecast_vaccine_demand_children(child_pop),
            'vaccine_doses_elderly': forecast_vaccine_demand_elderly(elderly_pop)
        }

        demands.append(demand)

    return demands