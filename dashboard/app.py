
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Fashion Demand Analytics",
    page_icon="👗",
    layout="wide"
)

st.title("Fashion Demand Forecasting & Retail Analytics")
st.caption("VISUELLE 2.0 | Machine Learning Demand Forecasting")


# --------------------------------------------------
# LOAD DASHBOARD DATA
# --------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_data():
    model_comparison = pd.read_csv(
        DATA_DIR / "model_comparison.csv"
    )

    weekly_comparison = pd.read_csv(
        DATA_DIR / "weekly_comparison.csv"
    )

    forecast_data = pd.read_csv(
        DATA_DIR / "forecast_data.csv"
    )

    return model_comparison, weekly_comparison, forecast_data


try:
    model_comparison, weekly_comparison, forecast_data = load_data()
except FileNotFoundError as error:
    st.error(f"Dashboard data file not found: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

categories = sorted(
    forecast_data["category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    categories,
    default=categories
)

seasons = sorted(
    forecast_data["season"].dropna().unique()
)

selected_seasons = st.sidebar.multiselect(
    "Season",
    seasons,
    default=seasons
)

retail_shops = sorted(
    forecast_data["retail"].dropna().unique()
)

selected_retail = st.sidebar.multiselect(
    "Retail Shop",
    retail_shops,
    default=retail_shops
)

filtered_data = forecast_data[
    forecast_data["category"].isin(selected_categories)
    & forecast_data["season"].isin(selected_seasons)
    & forecast_data["retail"].isin(selected_retail)
]


# --------------------------------------------------
# OVERVIEW METRICS
# --------------------------------------------------

st.subheader("Business Overview")

best_model = model_comparison.loc[
    model_comparison["MAE"].idxmin()
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Products",
    "5,355"
)

col2.metric(
    "Retail Shops",
    "110"
)

col3.metric(
    "Best Model",
    best_model["Model"]
)

col4.metric(
    "Best Model WAPE",
    f'{best_model["WAPE (%)"]:.2f}%'
)

st.divider()


# --------------------------------------------------
# WEEKLY DEMAND ANALYSIS
# --------------------------------------------------

st.subheader("Weekly Demand: Actual vs Predicted")

fig_weekly = go.Figure()

fig_weekly.add_trace(
    go.Scatter(
        x=weekly_comparison["Week"],
        y=weekly_comparison["Actual_Average"],
        mode="lines+markers",
        name="Actual Demand"
    )
)

fig_weekly.add_trace(
    go.Scatter(
        x=weekly_comparison["Week"],
        y=weekly_comparison["Predicted_Average"],
        mode="lines+markers",
        name="Random Forest Prediction"
    )
)

fig_weekly.update_layout(
    xaxis_title="Product Lifecycle Week",
    yaxis_title="Average Sales",
    hovermode="x unified",
    legend_title="Demand"
)

st.plotly_chart(fig_weekly, use_container_width=True)


# --------------------------------------------------
# MODEL COMPARISON
# --------------------------------------------------

st.subheader("Model Performance Comparison")

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    fig_mae = px.bar(
        model_comparison,
        x="Model",
        y="MAE",
        title="Mean Absolute Error (MAE)",
        text_auto=".3f"
    )

    st.plotly_chart(fig_mae, use_container_width=True)

with metric_col2:
    fig_rmse = px.bar(
        model_comparison,
        x="Model",
        y="RMSE",
        title="Root Mean Squared Error (RMSE)",
        text_auto=".3f"
    )

    st.plotly_chart(fig_rmse, use_container_width=True)

st.dataframe(
    model_comparison.round(4),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# PRODUCT FORECAST EXPLORER
# --------------------------------------------------

st.divider()

st.subheader("Product-Level Demand Forecast Explorer")

st.write(
    "Explore actual and predicted demand for individual "
    "product-retail records."
)

if filtered_data.empty:
    st.warning("No records match the selected filters.")
else:
    product_options = filtered_data["external_code"].dropna().unique()

    selected_product = st.selectbox(
        "Select Product",
        product_options
    )

    product_data = filtered_data[
        filtered_data["external_code"] == selected_product
    ]

    selected_record = st.selectbox(
        "Select Retail Record",
        product_data.index,
        format_func=lambda index: (
            f"Shop {product_data.loc[index, 'retail']} | "
            f"Season {product_data.loc[index, 'season']}"
        )
    )

    record = product_data.loc[selected_record]

    weeks = list(range(2, 12))

    actual_values = [
        record[f"actual_week_{week}"]
        for week in weeks
    ]

    predicted_values = [
        record[f"predicted_week_{week}"]
        for week in weeks
    ]

    fig_product = go.Figure()

    fig_product.add_trace(
        go.Bar(
            x=weeks,
            y=actual_values,
            name="Actual Demand"
        )
    )

    fig_product.add_trace(
        go.Scatter(
            x=weeks,
            y=predicted_values,
            mode="lines+markers",
            name="Predicted Demand"
        )
    )

    fig_product.update_layout(
        title=f"Demand Forecast for Product {selected_product}",
        xaxis_title="Product Lifecycle Week",
        yaxis_title="Sales",
        xaxis=dict(tickmode="linear", dtick=1)
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

    actual_total = sum(actual_values)
    predicted_total = sum(predicted_values)

    total_col1, total_col2 = st.columns(2)

    total_col1.metric(
        "Actual Future Sales",
        f"{actual_total:.2f}"
    )

    total_col2.metric(
        "Predicted Future Sales",
        f"{predicted_total:.2f}",
        delta=f"{predicted_total - actual_total:.2f}"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Fashion Demand Forecasting & Retail Analytics | "
    "Developed using Python, Scikit-learn, Streamlit and Plotly | "
    "Dataset: VISUELLE 2.0"
)
