# Demo Instructions

## Live Demo Setup

### Prerequisites

- Python 3.8+
- All dependencies installed (`pip install -r requirements.txt`)
- Sample data in `sample_data/` directory

### Running the Demo

1. **Start the Application**:

   ```bash
   python run.py
   ```

2. **Access Points**:
   - **Dashboard**: http://localhost:8502
   - **API Documentation**: http://localhost:8000/docs
   - **API Health Check**: http://localhost:8000/health

### Demo Script

#### 1. Dashboard Overview (30 seconds)

- Navigate to the Streamlit dashboard
- Show main interface with controls
- Demonstrate language selection (English/Nepali)

#### 2. Population Forecasting (1 minute)

- Select forecast horizon (5 years)
- Choose a region (Kathmandu Valley)
- Show population growth chart
- Display forecast data table
- Explain model choices (Linear Regression vs ARIMA)

#### 3. Risk Analysis (1 minute)

- Switch to Risk Analysis tab
- Show demographic risk clusters
- Explain risk categories (High Elderly Care, Maternal & Child Health, Urban Growth)
- Display cluster characteristics

#### 4. Healthcare Demand (1 minute)

- Navigate to Healthcare Demand tab
- Show projected needs for hospitals, clinics, workers
- Explain how forecasts drive healthcare planning

#### 5. AI Insights (30 seconds)

- Show AI-generated policy insights
- Demonstrate explainable recommendations

### API Demo (Optional)

If demonstrating API capabilities:

```bash
# Health check
curl http://localhost:8000/health

# Population forecast
curl "http://localhost:8000/population-forecast?years=5"

# Risk clusters
curl http://localhost:8000/risk-clusters

# Healthcare demand
curl "http://localhost:8000/healthcare-demand?years=5"

# AI insights
curl "http://localhost:8000/insights?years=5"
```

### Key Demo Points

- **Policy Focus**: Emphasize this is for government planning, not clinical decisions
- **Data Sources**: Mention census data aggregation
- **Model Transparency**: Explain simple, interpretable models chosen for policy use
- **Responsible AI**: Highlight bias considerations and limitations
- **Scalability**: Show how platform can handle multiple regions

### Troubleshooting

- If ports 8000/8502 are busy, modify `run.py` to use different ports
- Ensure sample data files exist in `sample_data/` directory
- Check Python version compatibility

### Recording Tips

- Use screen recording software
- Narrate clearly, explaining each feature
- Keep under 3 minutes total
- Include both dashboard interaction and API calls if possible
