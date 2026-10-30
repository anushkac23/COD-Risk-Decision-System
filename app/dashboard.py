import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "orders_sample.csv"

sys.path.append(str(Path(__file__).resolve().parent))

from services.prediction_service import predict_rto_probability
from services.decision_engine import evaluate_order
from services.whatsapp_service import (
    generate_confirmation_message,
    generate_prepaid_message,
    process_customer_response,
    check_response_timeout
)

# Page configuration
st.set_page_config(
    page_title="COD Risk Management",
    page_icon="📦",
    layout="wide"
)


st.title("📦 COD Risk Management Dashboard")
st.write(
    "AI-powered Cash on Delivery risk analysis "
    "and decision support system."
)


# Load dataset and predictions
@st.cache_data
def load_dashboard_data():

    df = pd.read_csv(DATA_PATH)

    df["final_status"] = (
        df["final_status"].astype(str).str.strip().str.upper()
    )

    df = df[
        df["final_status"].isin(["DELIVERED", "RTO"])
    ].copy()

    df = df.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    df["order_datetime"] = pd.to_datetime(
        df["order_datetime"],
        errors="coerce"
    )

    results = []

    for order in df.to_dict("records"):

        probability = predict_rto_probability(order)

        decision = evaluate_order(order, probability)

        results.append(decision)

    results_df = pd.DataFrame(results)

    df = df.reset_index(drop=True)

    return pd.concat(
        [df, results_df.drop(columns=["order_id"])],
        axis=1
    )


with st.spinner("Analysing COD orders using the AI model..."):
    try:
        data = load_dashboard_data()
    except Exception as error:
        st.error(f"Unable to load dashboard: {error}")
        st.stop()


# Sidebar filters
st.sidebar.header("Dashboard Filters")

cities = ["All"] + sorted(
    data["city"].dropna().astype(str).unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)

actions = ["All"] + sorted(
    data["recommended_action"].unique().tolist()
)

selected_action = st.sidebar.selectbox(
    "Select Recommended Action",
    actions
)


filtered_data = data.copy()

if selected_city != "All":
    filtered_data = filtered_data[
        filtered_data["city"].astype(str) == selected_city
    ]

if selected_action != "All":
    filtered_data = filtered_data[
        filtered_data["recommended_action"] == selected_action
    ]

# Recommended Action Summary
st.subheader("Recommended Action Summary")

action_summary = (
    filtered_data["recommended_action"]
    .value_counts()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Ship As-Is",
    action_summary.get("SHIP_AS_IS", 0)
)

col2.metric(
    "WhatsApp Confirmation",
    action_summary.get("WHATSAPP_CONFIRMATION", 0)
)

col3.metric(
    "Prepaid Nudge",
    action_summary.get("PREPAID_NUDGE", 0)
)

col4.metric(
    "Hold for Review",
    action_summary.get("HOLD_FOR_REVIEW", 0)
)
# Key metrics
st.subheader("Business Overview")

total_orders = len(filtered_data)

rto_orders = (
    filtered_data["final_status"] == "RTO"
).sum()

rto_rate = (
    rto_orders / total_orders * 100
    if total_orders else 0
)

average_order_value = (
    filtered_data["order_value"].mean()
    if total_orders else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total COD Orders", f"{total_orders:,}")

col2.metric("Actual RTO Rate", f"{rto_rate:.2f}%")

col3.metric(
    "Average Order Value",
    f"₹{average_order_value:,.2f}"
)

col4.metric("Actual RTO Orders", f"{rto_orders:,}")


# Risk distribution
st.subheader("AI Risk Distribution")

risk_counts = (
    filtered_data["risk_level"]
    .value_counts()
    .reindex(["LOW", "MEDIUM", "HIGH", "VERY HIGH"], fill_value=0)
    .reset_index()
)

risk_counts.columns = ["Risk Level", "Orders"]

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        risk_counts,
        x="Risk Level",
        y="Orders",
        title="Orders by Risk Category",
        text="Orders"
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    action_counts = (
        filtered_data["recommended_action"]
        .value_counts()
        .reset_index()
    )

    action_counts.columns = ["Recommended Action", "Orders"]

    fig = px.pie(
        action_counts,
        names="Recommended Action",
        values="Orders",
        title="Recommended Business Actions"
    )

    st.plotly_chart(fig, use_container_width=True)

# Daily Action Buckets
st.subheader("Daily Order Action Buckets")

daily_actions = (
    filtered_data
    .groupby([
        filtered_data["order_datetime"].dt.date,
        "recommended_action"
    ])
    .size()
    .reset_index(name="Orders")
)

daily_actions.columns = [
    "Date",
    "Recommended Action",
    "Orders"
]

fig = px.bar(
    daily_actions,
    x="Date",
    y="Orders",
    color="Recommended Action",
    barmode="stack",
    title="Daily Orders by Recommended Action"
)

st.plotly_chart(fig, use_container_width=True)
# Daily order trends
st.subheader("Daily COD Order Trends")

daily_orders = (
    filtered_data.dropna(subset=["order_datetime"])
    .groupby(filtered_data["order_datetime"].dt.date)
    .size()
    .reset_index(name="Orders")
)

daily_orders.columns = ["Date", "Orders"]

fig = px.line(
    daily_orders,
    x="Date",
    y="Orders",
    markers=True,
    title="Daily Order Volume"
)

st.plotly_chart(fig, use_container_width=True)


# Order table
st.subheader("Order-Level Risk Analysis")

display_columns = [
    "order_id",
    "customer_name",
    "city",
    "order_value",
    "risk_probability",
    "risk_level",
    "recommended_action",
    "final_status"
]

st.dataframe(
    filtered_data[display_columns],
    use_container_width=True,
    hide_index=True
)

# Download Decision Log
st.subheader("Decision Log")

decision_log_columns = [
    "order_id",
    "customer_name",
    "order_datetime",
    "risk_probability",
    "risk_level",
    "recommended_action",
    "reasons",
    "final_status"
]

decision_log = filtered_data[decision_log_columns].copy()

csv_data = decision_log.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Decision Log (CSV)",
    data=csv_data,
    file_name="cod_decision_log.csv",
    mime="text/csv"
)
# WhatsApp simulator
st.subheader("WhatsApp Automation Simulator")

if len(filtered_data) > 0:

    selected_order_id = st.selectbox(
        "Choose an order",
        filtered_data["order_id"].tolist()
    )

    selected_order = filtered_data[
        filtered_data["order_id"] == selected_order_id
    ].iloc[0].to_dict()

    action = selected_order["recommended_action"]

    st.write("Recommended Action:", action)

    if action == "WHATSAPP_CONFIRMATION":

        st.info(
            generate_confirmation_message(selected_order)
        )

    elif action == "PREPAID_NUDGE":

        st.info(
            generate_prepaid_message(selected_order)
        )

    elif action == "SHIP_AS_IS":

        st.success("This order can proceed without additional confirmation.")

    else:

        st.warning(
            "This order requires manual review before fulfilment."
        )

    customer_response = st.selectbox(
        "Simulate Customer Response",
        ["No response", "YES", "NO", "PREPAID", "Random message"]
    )
    
    elapsed_hours = st.slider(
        "Hours since WhatsApp message was sent",
        min_value=0,
        max_value=48,
        value=0
    )

    if st.button("Process Customer Response"):

     if customer_response == "No response":

        sent_time = datetime.now() - timedelta(hours=elapsed_hours)

        timeout_result = check_response_timeout(sent_time)

        if timeout_result["status"] == "TIMEOUT":
          st.error(timeout_result["message"])
        else:
          st.warning(timeout_result["message"])

    else:

            result = process_customer_response(
                customer_response
            )

            st.write("Customer Status:", result["status"])

            st.success(result["message"])

# Financial impact scenario
st.subheader("Potential Financial Impact")

st.caption(
    "Illustrative business scenario based on model predictions. "
    "Intervention effectiveness and conversion rates are assumptions, "
    "not measured results."
)

# Business assumptions
rto_cost = 169.40
acquisition_cost = 300
discount_percent = 5

# User-controlled assumptions
col1, col2 = st.columns(2)

with col1:
    intervention_rate = st.slider(
        "Assumed intervention success rate (%)",
        min_value=0,
        max_value=100,
        value=20
    )

with col2:
    prepaid_conversion_rate = st.slider(
        "Assumed prepaid conversion rate (%)",
        min_value=0,
        max_value=100,
        value=30
    )

# Orders receiving interventions
intervention_orders = filtered_data[
    filtered_data["recommended_action"].isin([
        "WHATSAPP_CONFIRMATION",
        "PREPAID_NUDGE",
        "HOLD_FOR_REVIEW"
    ])
]

# Estimated RTOs prevented
estimated_prevented_rtos = (
    intervention_orders["risk_probability"].sum()
    / 100
    * intervention_rate / 100
)

# Estimated savings from prevented RTOs
estimated_savings = (
    estimated_prevented_rtos * rto_cost
)

# Estimate prepaid discount expense
prepaid_orders = filtered_data[
    filtered_data["recommended_action"] == "PREPAID_NUDGE"
]

expected_prepaid_conversions = (
    len(prepaid_orders) * prepaid_conversion_rate / 100
)

average_prepaid_order_value = (
    prepaid_orders["order_value"].mean()
    if len(prepaid_orders) > 0
    else 0
)

discount_per_order = (
    average_prepaid_order_value * discount_percent / 100
)

estimated_discount_cost = (
    expected_prepaid_conversions * discount_per_order
)

# Potential false positives among held orders
hold_orders = filtered_data[
    filtered_data["recommended_action"] == "HOLD_FOR_REVIEW"
]

delivered_flagged_for_hold = (
    hold_orders["final_status"] == "DELIVERED"
).sum()

potential_acquisition_exposure = (
    delivered_flagged_for_hold * acquisition_cost
)

# Estimated net benefit before acquisition exposure
estimated_net_benefit = (
    estimated_savings - estimated_discount_cost
)

# Display financial metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Estimated RTO Savings",
    f"₹{estimated_savings:,.2f}"
)

col2.metric(
    "Estimated Discount Cost",
    f"₹{estimated_discount_cost:,.2f}"
)

col3.metric(
    "Estimated Net Benefit",
    f"₹{estimated_net_benefit:,.2f}"
)

st.divider()

st.subheader("Potential Customer Impact")

col1, col2 = st.columns(2)

col1.metric(
    "Delivered Orders Flagged for Hold",
    f"{delivered_flagged_for_hold:,}"
)

col2.metric(
    "Potential Acquisition Cost Exposure",
    f"₹{potential_acquisition_exposure:,.2f}"
)

st.caption(
    "Financial assumptions: ₹169.40 expected cost per RTO, "
    "5% prepaid discount and ₹300 customer acquisition cost. "
    "Delivered orders flagged for hold are potential false positives, "
    "not confirmed lost customers. The net benefit excludes acquisition "
    "exposure because a held order is not necessarily cancelled. "
    "These estimates are illustrative, not proven savings."
)

st.success("COD Risk Dashboard Loaded Successfully!")