from pathlib import Path

import pandas as pd
import streamlit as st
import altair as alt

from data_ingestion.loader import load_census_data
from feature_engineering.features import engineer_features
from forecasting.population_forecast import forecast_all_regions
from analytics.risk_clustering import cluster_demographic_risks, assign_risk_categories, get_cluster_summary
from forecasting.healthcare_demand import forecast_healthcare_demand
from analytics.insights import generate_all_insights

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "sample_data" / "census_data.csv"

# ── Translation dictionaries

LANG = {
    "en": {
        "page_title": "Population Health Intelligence Dashboard",
        "main_title": "🏥 Nepal Population Health Intelligence",
        "main_desc": (
            "**Nepal Population Health Intelligence Platform**\n\n"
            "This platform provides insights using integrated census data for Nepal's population planning.\n\n"
            "**It does not make individual clinical decisions and does not replace expert judgment.**"
        ),
        "controls": "Controls",
        "forecast_horizon": "Forecast Horizon (Years)",
        "select_region": "Select Region",
        "tab_population": "Population Trends",
        "tab_risk": "Risk Analysis",
        "tab_healthcare": "Healthcare Demand",
        "tab_insights": "AI Insights",
        "pop_forecast_header": "📈 Population Growth Forecast",
        "growth_chart": "Growth Chart",
        "forecast_data": "Forecast Data",
        "all_regions_summary": "All Regions Summary",
        "risk_header": "🎯 Demographic Risk Analysis",
        "risk_categories": "Risk Categories by Region",
        "cluster_chars": "Cluster Characteristics",
        "risk_distribution": "Risk Distribution",
        "region_col": "Region",
        "risk_cat_col": "Risk Category",
        "healthcare_header": "🏥 Healthcare Demand Forecast",
        "healthcare_needs": "Healthcare Needs",
        "hospital_beds": "Hospital Beds",
        "clinics": "Clinics",
        "doctors": "Doctors",
        "nurses": "Nurses",
        "vaccine_demand": "Vaccine Demand",
        "child_vaccines": "Child Vaccines/Year",
        "elderly_vaccines": "Elderly Vaccines/Year",
        "all_regions_healthcare": "All Regions Healthcare Summary",
        "insights_header": "🧠 AI Insights",
        "insight_label": "Insight",
        "no_insights": "No insights generated. Check data and parameters.",
        "disclaimer": (
            "**Disclaimer:** This platform provides population-level planning insights using aggregated data.\n\n"
            "It does not make individual clinical decisions and does not replace expert judgment.\n\n"
            "All estimates are based on historical trends and must be verified by Nepal government domain experts."
        ),
        "language_label": "Language / भाषा",
        "year": "Year",
        "predicted_population": "Predicted Population",
    },
    "ne": {
        "page_title": "जनसंख्या स्वास्थ्य बुद्धिमत्ता ड्यासबोर्ड",
        "main_title": "🏥 नेपाल जनसंख्या स्वास्थ्य बुद्धिमत्ता",
        "main_desc": (
            "**नेपाल जनसंख्या स्वास्थ्य बुद्धिमत्ता मंच**\n\n"
            "यह मंच नेपालकी जनसंख्या योजनाको लागि एकीकृत जनगणना डेटा प्रयोग गरेर अन्तर्दृष्टि प्रदान गर्दछ।\n\n"
            "**यो व्यक्तिगत क्लिनिकल निर्णय गर्दैन र विशेषज्ञ निर्णयको स्थान नलिदैन।**"
        ),
        "controls": "नियन्त्रण",
        "forecast_horizon": "पूर्वानुमान क्षितिज (वर्षहरू)",
        "select_region": "क्षेत्र चयन गर्नुहोस्",
        "tab_population": "जनसंख्या प्रवृत्ति",
        "tab_risk": "जोखिम विश्लेषण",
        "tab_healthcare": "स्वास्थ्य सेवा माग",
        "tab_insights": "कृत्रिम बुद्धिमत्ता अन्तर्दृष्टि",
        "pop_forecast_header": "📈 जनसंख्या वृद्धि पूर्वानुमान",
        "growth_chart": "वृद्धि चार्ट",
        "forecast_data": "पूर्वानुमान डेटा",
        "all_regions_summary": "सबै क्षेत्रको सारांश",
        "risk_header": "🎯 जनसांख्यिकीय जोखिम विश्लेषण",
        "risk_categories": "क्षेत्र अनुसार जोखिम श्रेणीहरू",
        "cluster_chars": "क्लस्टर विशेषताहरू",
        "risk_distribution": "जोखिम वितरण",
        "region_col": "क्षेत्र",
        "risk_cat_col": "जोखिम श्रेणी",
        "healthcare_header": "🏥 स्वास्थ्य सेवा माग पूर्वानुमान",
        "healthcare_needs": "स्वास्थ्य सेवा आवश्यकताहरू",
        "hospital_beds": "अस्पताल शय्या",
        "clinics": "क्लिनिकहरू",
        "doctors": "चिकित्सकहरू",
        "nurses": "नर्सहरू",
        "vaccine_demand": "खोप माग",
        "child_vaccines": "बाल खोप/वर्ष",
        "elderly_vaccines": "वृद्ध खोप/वर्ष",
        "all_regions_healthcare": "सबै क्षेत्र स्वास्थ्य सेवा सारांश",
        "insights_header": "🧠 कृत्रिम बुद्धिमत्ता अन्तर्दृष्टि",
        "insight_label": "अन्तर्दृष्टि",
        "no_insights": "कुनै अन्तर्दृष्टि उत्पन्न भएन। डेटा र प्यारामिटरहरू जाँच गर्नुहोस्।",
        "disclaimer": (
            "**अस्वीकरण:** यह मंच एकीकृत डेटा प्रयोग गरेर जनसंख्या-स्तरीय योजना अन्तर्दृष्टि प्रदान गर्दछ।\n\n"
            "यो व्यक्तिगत क्लिनिकल निर्णय गर्दैन र विशेषज्ञ निर्णयको स्थान नलिदैन।\n\n"
            "सबै अनुमानहरू ऐतिहासिक प्रवृत्तिहरूमा आधारित हुन् र नेपाल सरकारका डोमेन विशेषज्ञहरू द्वारा सत्यापित हुनु पर्दछ।"
        ),
        "language_label": "भाषा / Language",
        "year": "वर्ष",
        "predicted_population": "अनुमानित जनसंख्या",
    },
}


def t(key: str) -> str:
    """Return translated string for current language."""
    lang = st.session_state.get("lang", "en")
    return LANG[lang].get(key, key)


# ── Page config ─────────────

st.set_page_config(page_title="Population Health Intelligence Dashboard", layout="wide")

# ── Language toggle (top of sidebar)

lang_options = {"English": "en", "नेपाली": "ne"}
chosen = st.sidebar.radio(
    "Language / भाषा",
    list(lang_options.keys()),
    index=0,
    horizontal=True,
)
st.session_state["lang"] = lang_options[chosen]

# ── Header

st.title(t("main_title"))
st.markdown(t("main_desc"))

# ── Load data ───────────────

census_df = load_census_data(DATA_PATH)
features_df = engineer_features(census_df)

# ── Sidebar controls ───────

st.sidebar.header(t("controls"))
years = st.sidebar.slider(t("forecast_horizon"), min_value=1, max_value=10, value=5)
selected_region = st.sidebar.selectbox(
    t("select_region"),
    census_df['region_name'].unique(),
)

# ── Tabs

tab1, tab2, tab3, tab4 = st.tabs([
    t("tab_population"), t("tab_risk"), t("tab_healthcare"), t("tab_insights")
])

# ────────── Tab 1: Population Trends

with tab1:
    st.header(t("pop_forecast_header"))

    forecasts = forecast_all_regions(census_df, forecast_years=years)
    if not forecasts.empty:
        region_forecast = forecasts[forecasts['region_name'] == selected_region].copy()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{t('growth_chart')} - {selected_region}")

            # Convert year to string so chart axes don't add commas
            chart_df = region_forecast.copy()
            chart_df["year"] = chart_df["year"].astype(str)

            chart = (
                alt.Chart(chart_df)
                .mark_line(point=True, color="#58A6FF")
                .encode(
                    x=alt.X("year:N", title=t("year"), sort=None),
                    y=alt.Y("predicted_population:Q", title=t("predicted_population")),
                    tooltip=[
                        alt.Tooltip("year:N", title=t("year")),
                        alt.Tooltip("predicted_population:Q", title=t("predicted_population"), format=","),
                    ],
                )
                .properties(height=300)
                .configure_axis(labelFontSize=12, titleFontSize=13)
            )
            st.altair_chart(chart, use_container_width=True)

        with col2:
            st.subheader(t("forecast_data"))
            st.dataframe(region_forecast)

        st.subheader(t("all_regions_summary"))
        summary = forecasts.groupby('region_name').agg({
            'predicted_population': ['min', 'max', 'mean']
        }).round(0)
        st.dataframe(summary)

# ────────── Tab 2: Risk Analysis

with tab2:
    st.header(t("risk_header"))

    clustered_data, cluster_labels = cluster_demographic_risks(features_df)
    risk_categories = assign_risk_categories(cluster_labels)

    cluster_summary = get_cluster_summary(features_df, cluster_labels)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("risk_categories"))
        region_risks = pd.DataFrame({
            t("region_col"): clustered_data['region_name'],
            t("risk_cat_col"): [risk_categories.get(str(rid), "Unknown") for rid in clustered_data['region_id']]
        })
        st.dataframe(region_risks)

    with col2:
        st.subheader(t("cluster_chars"))
        st.dataframe(cluster_summary.round(3))

    st.subheader(t("risk_distribution"))
    risk_counts = pd.Series([cat for cat in risk_categories.values()]).value_counts()
    st.bar_chart(risk_counts)

# ────────── Tab 3: Healthcare Demand

with tab3:
    st.header(t("healthcare_header"))

    demands = forecast_healthcare_demand(census_df, forecast_years=years)

    if demands:
        # Filter for selected region
        region_demands = [d for d in demands if d['region_name'] == selected_region]

        if region_demands:
            latest_demand = region_demands[-1]  # Most future year

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"{t('healthcare_needs')} - {selected_region} ({latest_demand['year']})")
                st.metric(t("hospital_beds"), latest_demand['hospital_beds_needed'])
                st.metric(t("clinics"), latest_demand['clinics_needed'])
                st.metric(t("doctors"), latest_demand['doctors_needed'])
                st.metric(t("nurses"), latest_demand['nurses_needed'])

            with col2:
                st.subheader(t("vaccine_demand"))
                st.metric(t("child_vaccines"), latest_demand['vaccine_doses_children'])
                st.metric(t("elderly_vaccines"), latest_demand['vaccine_doses_elderly'])

        st.subheader(t("all_regions_healthcare"))
        demand_df = pd.DataFrame(demands)
        summary = demand_df.groupby(['region_name', 'year']).agg({
            'hospital_beds_needed': 'sum',
            'clinics_needed': 'sum',
            'doctors_needed': 'sum'
        }).reset_index()
        st.dataframe(summary)

# ────────── Tab 4: AI Insights ─

with tab4:
    st.header(t("insights_header"))

    forecasts = forecast_all_regions(census_df, forecast_years=years)
    _, cluster_labels = cluster_demographic_risks(features_df)
    risk_categories = assign_risk_categories(cluster_labels)
    demands = forecast_healthcare_demand(census_df, forecast_years=years)

    insights = generate_all_insights(features_df, forecasts, risk_categories, demands)

    if insights:
        for i, insight in enumerate(insights, 1):
            st.info(f"**{t('insight_label')} {i}:** {insight}")
    else:
        st.info(t("no_insights"))

# ── Footer

st.markdown("---")
st.caption(t("disclaimer"))
