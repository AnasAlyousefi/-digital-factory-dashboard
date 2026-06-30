# Digital Factory Dashboard

An integrated manufacturing intelligence platform that unifies OEE monitoring, predictive maintenance, supply chain forecasting, and cost/ROI analysis into a single multi-page application — built to mirror how a real Process/Data Engineer would consolidate plant-floor data into one decision-support tool.

## Why this project exists

In most manufacturing environments, OEE data, machine sensor logs, demand forecasts, and cost analysis live in separate spreadsheets or disconnected tools. Decision-makers waste time switching between systems, and the financial impact of operational issues (downtime, defects, stockouts) is rarely visible in real time.

This dashboard solves that by combining 3 standalone analytics projects into one platform, plus a 4th page that translates operational metrics into dollar-value business impact — the layer that's usually missing.

## What it does

| Page | Function |
|---|---|
| **Home** | Factory health overview, combining signals across all systems |
| **OEE Monitoring** | Tracks Availability, Performance, and Quality by machine and shift; flags critical/warning machines automatically |
| **Predictive Maintenance** | Random Forest classifier predicts machine failure risk from sensor readings (temperature, torque, rotational speed, tool wear) |
| **Supply Chain Forecasting** | Facebook Prophet model forecasts product demand to support inventory planning |
| **Cost Impact & ROI Calculator** | Converts downtime and maintenance metrics into financial impact, and calculates ROI of predictive maintenance investment |

## Tech Stack

- **Frontend/App:** Streamlit (multi-page architecture)
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn (Random Forest Classifier)
- **Forecasting:** Facebook Prophet
- **Visualization:** Plotly
- **Styling:** Custom dark theme with amber industrial accents (`.streamlit/config.toml`, `style.py`)

## Project Structure

```
digital-factory-dashboard/
├── .streamlit/
│   └── config.toml          # Theme configuration
├── pages/
│   ├── 1_OEE_Monitoring.py
│   ├── 2_Predictive_Maintenance.py
│   ├── 3_Supply_Chain.py
│   └── 4_Cost_Impact.py
├── Home.py                  # Entry point / landing page
├── style.py                 # Shared custom styling
├── requirements.txt
├── oee_data.csv
├── ai4i2020.csv             # Predictive maintenance dataset (AI4I 2020)
└── supply_chain_data.csv
```

## Running Locally

```bash
git clone https://github.com/AnasAlyousefi/-digital-factory-dashboard.git
cd -digital-factory-dashboard
pip install -r requirements.txt
streamlit run Home.py
```

## Live Demo

[Try the live app here](https://jjfdjihezmdwwzjrbtzqi2.streamlit.app/)
## Author

Built by Anas Alyousefi as part of a Data & Process Engineering portfolio, combining Lean Six Sigma / Industrial Engineering domain knowledge with applied data analytics and machine learning.
