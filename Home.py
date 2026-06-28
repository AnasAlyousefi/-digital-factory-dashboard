
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import apply_custom_style
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Digital Factory Dashboard",
    page_icon="🏭",
    layout="wide"
)
apply_custom_style()

st.title("Digital Factory Dashboard")
st.markdown("### Integrated Manufacturing Intelligence System")
st.markdown("---")

# Load all 3 datasets
@st.cache_data
def load_oee_data():
    df = pd.read_csv('oee_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_data
def load_maintenance_data():
    df = pd.read_csv('ai4i2020.csv')
    return df

@st.cache_data
def load_supply_chain_data():
    df = pd.read_csv('supply_chain_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

oee_df = load_oee_data()
maintenance_df = load_maintenance_data()
supply_df = load_supply_chain_data()

# ===== FACTORY HEALTH SCORE =====
st.subheader("Factory Health Score")

# Calculate health components
avg_oee = oee_df['oee'].mean() * 100
failure_rate = maintenance_df['Machine failure'].mean() * 100
avg_fulfillment = supply_df['fulfillment_rate'].mean() * 100

# Health score formula (weighted average)
oee_score = min(avg_oee / 85 * 100, 100)  # 85% is world class target
reliability_score = max(0, 100 - (failure_rate * 5))  # penalize failure rate
supply_score = avg_fulfillment

health_score = (oee_score * 0.4 + reliability_score * 0.3 + supply_score * 0.3)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Factory Health Score", f"{health_score:.0f}/100")
col2.metric("OEE Performance", f"{avg_oee:.1f}%")
col3.metric("Equipment Reliability", f"{100-failure_rate:.1f}%")
col4.metric("Supply Chain Fulfillment", f"{avg_fulfillment:.1f}%")

# Health status message
if health_score >= 80:
    st.success(f"FACTORY STATUS: HEALTHY - Overall score {health_score:.0f}/100. Operations running well across all systems.")
elif health_score >= 60:
    st.warning(f"FACTORY STATUS: NEEDS ATTENTION - Overall score {health_score:.0f}/100. Some systems require improvement.")
else:
    st.error(f"FACTORY STATUS: CRITICAL - Overall score {health_score:.0f}/100. Immediate action required.")

st.markdown("---")

# ===== CROSS-SYSTEM ALERTS =====
st.subheader("Cross-System Alerts")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**OEE System**")
    machine_oee = oee_df.groupby('machine')['oee'].mean() * 100
    critical_machines = machine_oee[machine_oee < 65].index.tolist()
    if critical_machines:
        st.error(f"Critical OEE: {', '.join(critical_machines)}")
    else:
        st.success("No critical OEE issues")

with col_b:
    st.markdown("**Maintenance System**")
    high_risk_count = maintenance_df['Machine failure'].sum()
    st.warning(f"{high_risk_count} machines flagged for failure risk in dataset")

with col_c:
    st.markdown("**Supply Chain System**")
    low_fulfillment = supply_df[supply_df['fulfillment_rate'] < 0.90]
    if len(low_fulfillment) > 0:
        st.warning(f"{len(low_fulfillment)} records with fulfillment below 90%")
    else:
        st.success("Fulfillment rates healthy")

st.markdown("---")

# ===== NAVIGATION GUIDE =====
st.subheader("Navigate to Detailed Dashboards")
st.markdown("""
Use the sidebar to navigate to detailed dashboards:

- **OEE Monitoring** - Machine efficiency, availability, performance, quality tracking
- **Predictive Maintenance** - ML-powered failure prediction and risk assessment  
- **Supply Chain** - Demand forecasting and inventory optimization
- **Cost Impact** - Financial analysis and ROI calculator

This overview combines insights from all systems into a single Factory Health Score,
giving management instant visibility into overall manufacturing performance.
""")

st.markdown("---")
st.caption("Digital Factory Dashboard | Built by Anas Al-Yousefi | Python, Streamlit, Scikit-learn, Prophet")
