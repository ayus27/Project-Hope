import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_latest_region_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the most recent data for each region for clustering.
    """
    return df.sort_values(['region_id', 'year']).groupby('region_id').tail(1).reset_index(drop=True)


def cluster_demographic_risks(df: pd.DataFrame, n_clusters: int = 3) -> tuple[pd.DataFrame, pd.Series]:
    """
    Cluster regions based on demographic risk factors using KMeans.
    Features: population_density, elderly_ratio, child_ratio, population_growth_rate
    """
    latest_data = get_latest_region_data(df)

    # Select features for clustering
    features = ['population_density', 'elderly_ratio', 'child_ratio', 'population_growth_rate']
    X = latest_data[features].fillna(0)  # Handle any NaN growth rates

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # Add cluster labels to data
    latest_data = latest_data.copy()
    latest_data['risk_cluster'] = clusters

    return latest_data, pd.Series(clusters, index=latest_data['region_id'])


def assign_risk_categories(cluster_labels: pd.Series) -> dict[str, str]:
    """
    Assign human-readable risk categories based on cluster characteristics.
    This is a simplified mapping - in practice, you'd analyze cluster centroids.
    """
    # For demo purposes, assign categories based on cluster number
    # In a real implementation, analyze the cluster centers to determine categories
    categories = {
        0: "High Elderly Care Demand",
        1: "High Maternal & Child Health Need",
        2: "Rapid Urban Growth Risk"
    }

    return {str(region_id): categories.get(cluster, "Moderate Risk") for region_id, cluster in cluster_labels.items()}


def get_cluster_summary(df: pd.DataFrame, cluster_labels: pd.Series) -> pd.DataFrame:
    """
    Generate summary statistics for each risk cluster.
    """
    latest_data = get_latest_region_data(df)
    latest_data = latest_data.copy()
    latest_data['risk_cluster'] = cluster_labels

    summary = latest_data.groupby('risk_cluster').agg({
        'region_id': 'count',
        'population_density': 'mean',
        'elderly_ratio': 'mean',
        'child_ratio': 'mean',
        'population_growth_rate': 'mean'
    }).rename(columns={'region_id': 'region_count'})

    return summary.reset_index()