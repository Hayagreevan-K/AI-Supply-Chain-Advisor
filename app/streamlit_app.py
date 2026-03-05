import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from services.llm_service import ask_supply_chain_ai
from services.preprocessing import preprocess_data
from services.forecasting_service import predict_demand
from services.inventory_service import (
    calculate_inventory_metrics,
    estimate_stockout_days
)

st.title("AI Supply Chain Advisor")

st.write("Upload a supply chain dataset or use the default dataset.")


uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/supply_chain_sales.csv")


st.subheader("Dataset Preview")
st.dataframe(df.head())


# -------------------------
# Warehouse / Product Filter
# -------------------------

warehouse_list = df["warehouse_id"].unique()
product_list = df["product_id"].unique()

selected_warehouse = st.selectbox(
    "Select Warehouse",
    warehouse_list
)

selected_product = st.selectbox(
    "Select Product",
    product_list
)


filtered_df = df[
    (df["warehouse_id"] == selected_warehouse) &
    (df["product_id"] == selected_product)
]


st.subheader("Filtered Dataset")
st.dataframe(filtered_df.head())


# -------------------------
# Preprocessing
# -------------------------

processed_df = preprocess_data(filtered_df)


features = [
    "promotion",
    "holiday",
    "day_of_week",
    "month",
    "week_of_year",
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "rolling_std_7"
]


X = processed_df[features]


predictions = predict_demand(X)

processed_df["predicted_demand"] = predictions


# -------------------------
# Forecast Visualization
# -------------------------

st.subheader("Actual vs Predicted Demand")

fig, ax = plt.subplots()

ax.plot(
    processed_df["date"],
    processed_df["sales"],
    label="Actual Sales"
)

ax.plot(
    processed_df["date"],
    processed_df["predicted_demand"],
    label="Predicted Demand"
)

ax.legend()

st.pyplot(fig)


# -------------------------
# Inventory Optimization
# -------------------------

lead_time = st.slider("Lead Time (days)", 1, 10, 5)

metrics = calculate_inventory_metrics(predictions, lead_time)


st.subheader("Inventory Recommendations")

st.write("Average Demand:", metrics["average_demand"])
st.write("Safety Stock:", metrics["safety_stock"])
st.write("Reorder Point:", metrics["reorder_point"])


# -------------------------
# Stockout Prediction
# -------------------------

inventory = st.number_input("Current Inventory", value=500)

days_left = estimate_stockout_days(
    inventory,
    metrics["average_demand"]
)

st.subheader("Stockout Prediction")

st.write("Estimated days until stockout:", days_left)

st.subheader("AI Supply Chain Assistant")

question = st.text_input(
    "Ask a supply chain question",
    placeholder="Example: When should I reorder inventory?"
)

if question:

    answer = ask_supply_chain_ai(
        question,
        metrics,
        days_left
    )

    st.success(answer)