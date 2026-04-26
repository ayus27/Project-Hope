import pandas as pd


def calculate_population_density(df: pd.DataFrame) -> pd.Series:
    """
    Calculate population density as total_population / area_sq_km.
    Higher density indicates urban areas with potentially higher service demands.
    """
    return df['total_population'] / df['area_sq_km']


def calculate_elderly_ratio(df: pd.DataFrame) -> pd.Series:
    """
    Calculate elderly ratio as age_60_plus / total_population.
    Indicates proportion of population likely needing chronic care services.
    """
    return df['age_60_plus'] / df['total_population']


def calculate_child_ratio(df: pd.DataFrame) -> pd.Series:
    """
    Calculate child ratio as age_0_14 / total_population.
    Indicates proportion of population needing maternal and child health services.
    """
    return df['age_0_14'] / df['total_population']


def calculate_working_age_ratio(df: pd.DataFrame) -> pd.Series:
    """
    Calculate working age ratio as age_15_59 / total_population.
    Indicates proportion of population in productive age groups.
    """
    return df['age_15_59'] / df['total_population']


def calculate_population_growth_rate(df: pd.DataFrame) -> pd.Series:
    """
    Calculate year-over-year population growth rate.
    Positive values indicate growing regions, negative indicate declining.
    """
    df_sorted = df.sort_values(['region_id', 'year'])
    growth_rate = df_sorted.groupby('region_id')['total_population'].pct_change()
    return growth_rate


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all engineered features to the DataFrame.
    """
    df = df.copy()
    df['population_density'] = calculate_population_density(df)
    df['elderly_ratio'] = calculate_elderly_ratio(df)
    df['child_ratio'] = calculate_child_ratio(df)
    df['working_age_ratio'] = calculate_working_age_ratio(df)
    df['population_growth_rate'] = calculate_population_growth_rate(df)
    return df