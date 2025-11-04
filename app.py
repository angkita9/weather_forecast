# =====================================================
# 🌤️ Streamlit Weather Dashboard – Europe 5 Cities
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Page setup ---
st.set_page_config(page_title="European Weather Dashboard", layout="wide")

st.title("🌦️ European Cities Weather Dashboard")
st.markdown("Visualize and explore 30-day weather trends for Paris, Vienna, Prague, Rome, and Lisbon.")

# --- Auto-detect data folder ---
current_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(current_dir, "data")

st.write("📁 Data folder path:", data_folder)

if not os.path.exists(data_folder):
    st.error("The 'data' folder was not found. Please create it beside app.py and add your CSV file(s).")
    st.stop()

# --- Load CSV files ---
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
if not csv_files:
    st.error("No CSV files found in the 'data' folder. Please add your downloaded weather CSV.")
    st.stop()

selected_file = st.selectbox("Select Weather CSV File", csv_files)
df = pd.read_csv(os.path.join(data_folder, selected_file))

# --- Clean data ---
df["date_time"] = pd.to_datetime(df["date_time"], errors='coerce')

# --- Sidebar filters ---
st.sidebar.header("🔍 Filters")

cities = st.sidebar.multiselect(
    "Select City", options=sorted(df["city"].dropna().unique()),
    default=list(df["city"].dropna().unique())
)

metrics = st.sidebar.multiselect(
    "Select Weather Metrics",
    options=["temperature", "humidity", "pressure", "wind_speed",
             "precipitation", "snowfall", "visibility"],
    default=["temperature", "humidity"]
)

# Date filter
min_date = df["date_time"].min()
max_date = df["date_time"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# --- Apply filters ---
filtered_df = df[
    (df["city"].isin(cities)) &
    (df["date_time"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# --- Display data table ---
st.subheader("📊 Filtered Weather Data (First 10 Rows)")
st.dataframe(filtered_df.head(10))

# --- Visualizations ---
st.subheader("🌡️ Weather Trends Over Time")
for metric in metrics:
    fig = px.line(
        filtered_df,
        x="date_time", y=metric,
        color="city",
        title=f"{metric.replace('_', ' ').title()} Over Time",
        markers=True
    )
    fig.update_layout(legend_title_text="City")
    st.plotly_chart(fig, use_container_width=True)

# --- Summary statistics ---
st.subheader("📈 Summary Statistics")
st.dataframe(filtered_df.groupby("city")[metrics].mean().round(2))
