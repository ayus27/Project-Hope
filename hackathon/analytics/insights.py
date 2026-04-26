import pandas as pd
from analytics.risk_clustering import get_latest_region_data


def generate_population_insights(df: pd.DataFrame, forecasts: pd.DataFrame) -> list[str]:
    """
    Generate plain-English insights about population trends.
    """
    insights = []

    for region_id in df['region_id'].unique():
        region_data = df[df['region_id'] == region_id]
        region_forecasts = forecasts[forecasts['region_id'] == region_id]

        if region_forecasts.empty:
            continue

        region_name = region_data['region_name'].iloc[0]
        current_pop = region_data['total_population'].max()
        future_pop = region_forecasts['predicted_population'].iloc[-1]
        growth_pct = ((future_pop - current_pop) / current_pop) * 100

        if growth_pct > 10:
            insights.append(
                f"{region_name} is projected to experience significant population growth of {growth_pct:.1f}% "
                f"over the next {len(region_forecasts)} years, which may require expanded infrastructure planning."
            )
        elif growth_pct < -5:
            insights.append(
                f"{region_name} may see population decline of {abs(growth_pct):.1f}% "
                f"over the next {len(region_forecasts)} years, potentially affecting service utilization."
            )

    return insights


def generate_demographic_insights(df: pd.DataFrame, risk_categories: dict) -> list[str]:
    """
    Generate insights about demographic risk patterns.
    Expected: DataFrame with engineered features (elderly_ratio, child_ratio, etc.)
    """
    insights = []
    latest_data = get_latest_region_data(df)

    for _, row in latest_data.iterrows():
        region_name = row['region_name']
        elderly_pct = row['elderly_ratio'] * 100
        child_pct = row['child_ratio'] * 100
        risk_category = risk_categories.get(str(int(row['region_id'])), "Unknown")

        if elderly_pct > 20:
            insights.append(
                f"{region_name}'s elderly population ({elderly_pct:.1f}%) suggests potential "
                f"higher demand for chronic care services in the coming years."
            )

        if child_pct > 25:
            insights.append(
                f"{region_name} has a relatively young population ({child_pct:.1f}% children), "
                f"indicating possible needs for maternal and child health programs."
            )

        if risk_category != "Moderate Risk":
            insights.append(
                f"{region_name} falls into the '{risk_category}' category, "
                f"which may require targeted planning for specific demographic challenges."
            )

    return insights


def generate_healthcare_insights(demand_forecasts: list[dict]) -> list[str]:
    """
    Generate insights about healthcare demand projections.
    """
    insights = []

    # Group by region and get latest year
    region_demands = {}
    for demand in demand_forecasts:
        region_id = demand['region_id']
        if region_id not in region_demands:
            region_demands[region_id] = demand

    for demand in region_demands.values():
        region_name = demand['region_name']
        beds = demand['hospital_beds_needed']
        clinics = demand['clinics_needed']
        doctors = demand['doctors_needed']

        insights.append(
            f"Based on population projections, {region_name} may need approximately "
            f"{beds} hospital beds, {clinics} clinics, and {doctors} doctors "
            f"to serve healthcare demands in {demand['year']}."
        )

    return insights


def generate_all_insights(df: pd.DataFrame, forecasts: pd.DataFrame,
                         risk_categories: dict, demand_forecasts: list[dict]) -> list[str]:
    """
    Combine all types of insights into a comprehensive list.
    """
    all_insights = []

    all_insights.extend(generate_population_insights(df, forecasts))
    all_insights.extend(generate_demographic_insights(df, risk_categories))
    all_insights.extend(generate_healthcare_insights(demand_forecasts))

    return all_insights