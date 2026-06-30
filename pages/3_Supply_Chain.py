
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import apply_custom_style
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from prophet import Prophet

st.set_page_config(page_title="Supply Chain", layout="wide")
apply_custom_style()
st.title("Supply Chain Forecasting")
st.markdown("---")

@st.cache_data
def load_data():
    DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(DATA_DIR, 'supply_chain_data.csv'))
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

@st.cache_data
def run_forecast(product, periods):
    prophet_df = df[df['product'] == product][['date', 'demand']].copy()
    prophet_df.columns = ['ds', 'y']

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return prophet_df, forecast

# Sidebar controls
st.sidebar.header("Forecast Settings")
selected_product = st.sidebar.selectbox("Select Product", df['product'].unique())
forecast_period = st.sidebar.slider("Forecast Period (days)", 30, 365, 180)

# Run forecast
prophet_df, forecast = run_forecast(selected_product, forecast_period)
future_only = forecast[forecast['ds'] > prophet_df['ds'].max()]

filtered_df = df[df['product'] == selected_product]

# KPI Cards
st.subheader("Supply Chain KPIs - " + selected_product)
col1, col2, col3, col4 = st.columns(4)

avg_demand_hist = filtered_df['demand'].mean()
avg_inventory = filtered_df['inventory'].mean()
avg_fulfillment = filtered_df['fulfillment_rate'].mean() * 100
avg_lead_time = filtered_df['lead_time_days'].mean()

col1.metric("Avg Daily Demand", f"{avg_demand_hist:.0f} units")
col2.metric("Avg Inventory", f"{avg_inventory:.0f} units")
col3.metric("Fulfillment Rate", f"{avg_fulfillment:.1f}%")
col4.metric("Avg Lead Time", f"{avg_lead_time:.1f} days")

st.markdown("---")

# Forecast Chart
st.subheader(f"Demand Forecast - Next {forecast_period} Days")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=prophet_df['ds'], y=prophet_df['y'],
    name='Actual Demand', line=dict(color='blue', width=1), opacity=0.7))
fig1.add_trace(go.Scatter(x=future_only['ds'], y=future_only['yhat'],
    name='Forecasted Demand', line=dict(color='red', width=2, dash='dash')))
fig1.add_trace(go.Scatter(x=future_only['ds'], y=future_only['yhat_upper'],
    name='Upper Bound', line=dict(color='orange', width=1)))
fig1.add_trace(go.Scatter(x=future_only['ds'], y=future_only['yhat_lower'],
    name='Lower Bound', line=dict(color='orange', width=1),
    fill='tonexty', fillcolor='rgba(255,165,0,0.2)'))

fig1.update_layout(xaxis_title='Date', yaxis_title='Units Demanded', height=450)
st.plotly_chart(fig1, use_container_width=True)

avg_forecast = future_only['yhat'].mean()
avg_lower = future_only['yhat_lower'].mean()
avg_upper = future_only['yhat_upper'].mean()

st.info(f"RECOMMENDATION: Order between {avg_lower:.0f} and {avg_upper:.0f} units/day. Target: {avg_forecast:.0f} units/day.")

st.markdown("---")

# Comparison
st.subheader("All Products Comparison")
col_a, col_b = st.columns(2)

with col_a:
    monthly_all = df.copy()
    monthly_all['month'] = monthly_all['date'].dt.strftime('%Y-%m')
    monthly_avg = monthly_all.groupby(['month', 'product'])['demand'].mean().reset_index()
    fig2 = px.line(monthly_avg, x='month', y='demand', color='product',
                   title='Monthly Demand Trend - All Products')
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    fulfillment_compare = df.groupby('product')['fulfillment_rate'].mean().reset_index()
    fulfillment_compare['fulfillment_rate'] = fulfillment_compare['fulfillment_rate'] * 100
    fig3 = px.bar(fulfillment_compare, x='product', y='fulfillment_rate',
                  color='fulfillment_rate', color_continuous_scale='RdYlGn',
                  title='Average Fulfillment Rate by Product')
    st.plotly_chart(fig3, use_container_width=True)
