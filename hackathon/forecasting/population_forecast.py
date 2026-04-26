import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')


def forecast_population_linear(df: pd.DataFrame, region_id: int, forecast_years: int = 5) -> pd.DataFrame:
    """
    Forecast population using linear regression.
    Suitable for policy planning as it's simple, interpretable, and shows clear trends.
    """
    region_data = df[df['region_id'] == region_id].sort_values('year')
    if len(region_data) < 2:
        return pd.DataFrame()

    X = region_data['year'].values.reshape(-1, 1)
    y = region_data['total_population'].values

    model = LinearRegression()
    model.fit(X, y)

    last_year = region_data['year'].max()
    future_years = range(last_year + 1, last_year + forecast_years + 1)
    future_X = [[year] for year in future_years]
    predictions = model.predict(future_X)

    forecast_df = pd.DataFrame({
        'region_id': region_id,
        'region_name': region_data['region_name'].iloc[0],
        'year': future_years,
        'predicted_population': predictions.astype(int),
        'model': 'linear_regression'
    })

    return forecast_df


def forecast_population_arima(df: pd.DataFrame, region_id: int, forecast_years: int = 5) -> pd.DataFrame:
    """
    Forecast population using ARIMA time series model.
    Suitable for policy planning as it captures temporal patterns and seasonality in population changes.
    """
    region_data = df[df['region_id'] == region_id].sort_values('year')
    if len(region_data) < 3:  # Need at least 3 points for ARIMA
        return pd.DataFrame()

    try:
        model = ARIMA(region_data['total_population'], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_years)

        last_year = region_data['year'].max()
        future_years = range(last_year + 1, last_year + forecast_years + 1)

        forecast_df = pd.DataFrame({
            'region_id': region_id,
            'region_name': region_data['region_name'].iloc[0],
            'year': future_years,
            'predicted_population': forecast.astype(int),
            'model': 'arima'
        })

        return forecast_df
    except:
        # Fallback to linear if ARIMA fails
        return forecast_population_linear(df, region_id, forecast_years)


def forecast_all_regions(df: pd.DataFrame, forecast_years: int = 5, use_arima: bool = True) -> pd.DataFrame:
    """
    Generate population forecasts for all regions.
    Uses ARIMA by default for better time series modeling, falls back to linear regression.
    """
    all_forecasts = []

    for region_id in df['region_id'].unique():
        if use_arima:
            forecast = forecast_population_arima(df, region_id, forecast_years)
        else:
            forecast = forecast_population_linear(df, region_id, forecast_years)

        if not forecast.empty:
            all_forecasts.append(forecast)

    if all_forecasts:
        return pd.concat(all_forecasts, ignore_index=True)
    else:
        return pd.DataFrame()