
import streamlit as st

def apply_custom_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@500;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.02em;
    }

    h1 {
        border-bottom: 3px solid #F5A623;
        padding-bottom: 12px;
        display: inline-block;
    }

    /* Metric cards styled like factory gauges */
    div[data-testid="stMetric"] {
        background: #14181D;
        border: 1px solid #232830;
        border-top: 3px solid #F5A623;
        border-radius: 6px;
        padding: 16px 18px;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 12px;
        color: #9AA1AC !important;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        color: #F5A623 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0B0E11;
        border-right: 1px solid #232830;
    }

    /* Alert boxes - sharper corners, industrial feel */
    div[data-testid="stAlert"] {
        border-radius: 4px;
        border-left: 4px solid currentColor;
    }

    /* Dividers */
    hr {
        border-color: #232830 !important;
    }
    </style>
    """, unsafe_allow_html=True)
