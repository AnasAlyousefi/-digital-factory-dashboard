
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import apply_custom_style
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="OEE Monitoring", layout="wide")
apply_custom_style()
st.title("OEE Monitoring")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('oee_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
machines = st.sidebar.multiselect("Select Machine", df['machine'].unique(), default=df['machine'].unique())
shifts = st.sidebar.multiselect("Select Shift", df['shift'].unique(), default=df['shift'].unique())

filtered = df[df['machine'].isin(machines) & df['shift'].isin(shifts)]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall OEE",  f"{filtered['oee'].mean()*100:.1f}%")
col2.metric("Availability", f"{filtered['availability'].mean()*100:.1f}%")
col3.metric("Performance",  f"{filtered['performance'].mean()*100:.1f}%")
col4.metric("Quality",      f"{filtered['quality'].mean()*100:.1f}%")

st.markdown("---")

# Machine Alerts
st.subheader("Machine Alerts")
machine_oee = filtered.groupby('machine')['oee'].mean() * 100
critical = machine_oee[machine_oee < 65].index.tolist()
warning = machine_oee[(machine_oee >= 65) & (machine_oee < 70)].index.tolist()
good = machine_oee[machine_oee >= 70].index.tolist()

col_a, col_b, col_c = st.columns(3)
with col_a:
    if critical:
        st.error(f"CRITICAL: {', '.join(critical)}")
    else:
        st.success("No critical machines")
with col_b:
    if warning:
        st.warning(f"WARNING: {', '.join(warning)}")
    else:
        st.success("No warnings")
with col_c:
    if good:
        st.success(f"Good: {', '.join(good)}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    oee_trend = filtered.groupby('date')['oee'].mean().reset_index()
    oee_trend['oee'] = oee_trend['oee'] * 100
    fig1 = px.line(oee_trend, x='date', y='oee', title='Daily OEE Trend')
    fig1.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="Target 85%")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    m_oee = filtered.groupby('machine')['oee'].mean().reset_index()
    m_oee['oee'] = m_oee['oee'] * 100
    fig2 = px.bar(m_oee, x='machine', y='oee', color='oee',
                  color_continuous_scale='RdYlGn', title='OEE by Machine')
    fig2.add_hline(y=85, line_dash="dash", line_color="green")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    components = filtered.groupby('machine')[['availability','performance','quality']].mean()*100
    components = components.reset_index().melt(id_vars='machine',
                 value_vars=['availability','performance','quality'],
                 var_name='Component', value_name='Percentage')
    fig3 = px.bar(components, x='machine', y='Percentage', color='Component',
                  barmode='group', title='OEE Components by Machine')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    defects = filtered.groupby('machine')['defects'].sum().reset_index()
    fig4 = px.bar(defects, x='machine', y='defects', color='defects',
                  color_continuous_scale='Reds', title='Total Defects by Machine')
    st.plotly_chart(fig4, use_container_width=True)
