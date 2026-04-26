from pydantic import BaseModel


class PopulationForecast(BaseModel):
    community_id: int
    community_name: str
    year: int
    predicted_population: int


class RiskCluster(BaseModel):
    cluster_id: int
    community_count: int
    average_age_risk: float
    average_density_risk: float
    average_population_per_health_worker: float


class HealthcareDemandForecast(BaseModel):
    community_id: int
    community_name: str
    year: int
    predicted_population: int
    forecast_hospitals: int
    forecast_clinics: int
    forecast_healthcare_workers: int
    forecast_vaccine_doses: int
