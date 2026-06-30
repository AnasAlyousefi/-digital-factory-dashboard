
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import apply_custom_style
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cost Impact", layout="wide")
apply_custom_style()
st.title("Cost Impact & ROI Calculator")
st.markdown("---")

st.markdown("Calculate the financial impact of downtime and the ROI of predictive maintenance investments.")

@st.cache_data
def load_data():
    DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    
    oee_df = pd.read_csv(os.path.join(DATA_DIR, 'oee_data.csv'))
    maintenance_df = pd.read_csv(os.path.join(DATA_DIR, 'ai4i2020.csv'))
    return oee_df, maintenance_df

oee_df, maintenance_df = load_data()

# ===== SECTION 1: Downtime Cost Calculator =====
st.subheader("Downtime Cost Calculator")

col1, col2, col3 = st.columns(3)
with col1:
    hourly_cost = st.number_input("Cost per hour of downtime ($)", 
                                    min_value=100, max_value=50000, value=5000, step=500)
with col2:
    total_downtime_hours = (oee_df['downtime'].sum() / 60)
    st.metric("Total Downtime in Dataset", f"{total_downtime_hours:.0f} hours")
with col3:
    total_cost = total_downtime_hours * hourly_cost
    st.metric("Total Downtime Cost", f"${total_cost:,.0f}")

st.markdown("---")

# ===== SECTION 2: Predictive Maintenance Savings =====
st.subheader("Predictive Maintenance ROI")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Without Predictive Maintenance**")
    failure_count = maintenance_df['Machine failure'].sum()
    unplanned_cost_per_failure = st.number_input(
        "Cost per unplanned failure ($)", min_value=1000, max_value=100000, 
        value=15000, step=1000)
    total_unplanned_cost = failure_count * unplanned_cost_per_failure
    st.metric("Total Unplanned Failure Cost", f"${total_unplanned_cost:,.0f}")
    st.caption(f"Based on {failure_count} failures in dataset")

with col_b:
    st.markdown("**With Predictive Maintenance (68% caught early)**")
    recall_rate = 0.68
    prevented_failures = int(failure_count * recall_rate)
    planned_cost_per_failure = st.number_input(
        "Cost per planned maintenance ($)", min_value=500, max_value=20000,
        value=3000, step=500)

    cost_prevented = prevented_failures * unplanned_cost_per_failure
    cost_of_planned = prevented_failures * planned_cost_per_failure
    net_savings = cost_prevented - cost_of_planned

    st.metric("Failures Prevented", f"{prevented_failures}")
    st.metric("Net Savings", f"${net_savings:,.0f}")

st.markdown("---")

# ===== SECTION 3: Summary Visualization =====
st.subheader("Cost Comparison Summary")

comparison_data = pd.DataFrame({
    'Scenario': ['Without Predictive Maintenance', 'With Predictive Maintenance'],
    'Cost': [total_unplanned_cost, total_unplanned_cost - net_savings]
})

fig = px.bar(comparison_data, x='Scenario', y='Cost',
             color='Scenario',
             color_discrete_map={
                 'Without Predictive Maintenance': '#e74c3c',
                 'With Predictive Maintenance': '#27ae60'
             },
             title='Total Maintenance Cost Comparison',
             text='Cost')
fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.success(f"By implementing predictive maintenance, this factory could save approximately ${net_savings:,.0f} by preventing {prevented_failures} unplanned failures.")

st.markdown("---")

# ===== SECTION 4: ROI Summary Box =====
st.subheader("Executive Summary")

roi_percentage = (net_savings / cost_of_planned * 100) if cost_of_planned > 0 else 0

col_x, col_y, col_z = st.columns(3)
col_x.metric("Investment Required", f"${cost_of_planned:,.0f}")
col_y.metric("Expected Savings", f"${net_savings:,.0f}")
col_z.metric("ROI", f"{roi_percentage:.0f}%")

st.info("""
**Business Case Summary:**
This analysis demonstrates that investing in predictive maintenance technology
generates positive ROI by catching equipment failures before they cause
expensive unplanned downtime. The combination of OEE monitoring, ML-based
failure prediction, and proactive maintenance scheduling creates measurable
financial value for manufacturing operations.
""")
