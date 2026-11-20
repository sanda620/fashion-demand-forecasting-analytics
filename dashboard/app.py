from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fashion Intelligence | Demand Analytics",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. DESIGN SYSTEM
# ============================================================

NAVY = "#172536"
NAVY_LIGHT = "#243D59"
GOLD = "#B69A68"
GOLD_LIGHT = "#E9DFC9"
TEAL = "#5D8A9B"
GREEN = "#789B83"
BG = "#F5F4F0"
WHITE = "#FFFFFF"
TEXT = "#263445"
MUTED = "#89919A"
BORDER = "#E8E6E0"
GRID = "#EEECE7"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global */
.stApp {
    background-color: #F5F4F0;
    color: #263445;
    font-family: 'Inter', Arial, sans-serif;
}
.block-container {
    max-width: 1550px;
    padding: 1.6rem 3rem 3rem 3rem;
}
header[data-testid="stHeader"] { background: transparent; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172536 0%, #1d3048 100%);
    border-right: 1px solid #304154;
}
[data-testid="stSidebar"] * { color: #F5F4F0; }
[data-testid="stSidebar"] hr { border-color: #405064; }
[data-testid="stSidebar"] label {
    color: #D5DCE4 !important;
    font-size: 13px;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #B69A68 !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] * { color: #172536 !important; }

/* Headings */
h1, h2, h3, h4 { color: #172536 !important; }
h4 { font-size: 1rem !important; font-weight: 650 !important; }

/* Hero banner */
.hero {
    background: linear-gradient(120deg, #172536 0%, #243D59 60%, #3a5a7c 100%);
    border-radius: 18px;
    padding: 34px 40px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(23, 37, 54, 0.18);
}
.hero::after {
    content: "";
    position: absolute;
    right: -60px; top: -80px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(182,154,104,0.35), transparent 70%);
}
.hero-eyebrow {
    color: #B69A68; font-size: 11px; font-weight: 700;
    letter-spacing: 3px; margin-bottom: 10px;
}
.hero-title {
    color: #FFFFFF; font-size: 34px; font-weight: 700;
    letter-spacing: -1px; margin-bottom: 8px;
}
.hero-sub { color: #C3CDD8; font-size: 14px; max-width: 640px; }
.hero-pill {
    display: inline-block; margin: 16px 8px 0 0;
    padding: 5px 13px; border-radius: 20px; font-size: 11px;
    background: rgba(255,255,255,0.10); color: #E9DFC9;
    border: 1px solid rgba(233,223,201,0.25);
}

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    padding: 22px 22px 20px 22px;
    border-radius: 14px;
    border: 1px solid #E8E6E0;
    border-top: 3px solid #B69A68;
    box-shadow: 0 4px 15px rgba(23, 37, 54, 0.035);
    min-height: 125px;
    transition: transform .2s ease, box-shadow .2s ease;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 26px rgba(23, 37, 54, 0.10);
}
.kpi-label {
    color: #89919A; font-size: 11px; font-weight: 700;
    letter-spacing: 1.2px; margin-bottom: 12px;
}
.kpi-value { color: #172536; font-size: 27px; font-weight: 700; margin-bottom: 5px; }
.kpi-note { color: #89919A; font-size: 11px; }

/* Insight box */
.insight {
    background: #FFFFFF; border: 1px solid #E8E6E0;
    border-left: 4px solid #B69A68; border-radius: 10px;
    padding: 14px 18px; font-size: 13px; color: #263445;
    margin: 6px 0 18px 0;
}

/* Section labels */
.eyebrow {
    color: #B69A68; font-size: 10px; font-weight: 700;
    letter-spacing: 2px; margin-bottom: 5px;
}
.section-title { color: #172536; font-size: 22px; font-weight: 700; margin-bottom: 5px; }
.section-description { color: #89919A; font-size: 13px; margin-bottom: 18px; }

/* Chart containers */
[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E8E6E0;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 4px 15px rgba(23, 37, 54, 0.03);
}

/* Native metrics styled as cards */
[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E8E6E0;
    border-radius: 12px; padding: 16px 20px;
}
[data-testid="stMetricLabel"] p {
    color: #89919A; font-size: 12px; font-weight: 600; letter-spacing: .5px;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    background: #FFFFFF; border-radius: 12px; border: 1px solid #E8E6E0;
}

/* Select boxes */
[data-baseweb="select"] > div { border-radius: 7px; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: #243D59; color: white; border: none; border-radius: 7px;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #B69A68; color: white;
}

/* Dividers */
hr { border-color: #E8E6E0; }

/* Tabs as pills */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: #EAE8E2; padding: 5px; border-radius: 12px;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    color: #77818D; font-weight: 600; border-radius: 9px;
    padding: 8px 22px; height: auto;
}
.stTabs [aria-selected="true"] {
    color: #172536 !important; background: #FFFFFF;
    box-shadow: 0 2px 8px rgba(23,37,54,0.10);
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Footer */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. HELPERS
# ============================================================

def section(eyebrow, title, description=""):
    """Renders the eyebrow + title + description block used above each section."""
    st.markdown(f"""
    <div class="eyebrow">{eyebrow}</div>
    <div class="section-title">{title}</div>
    <div class="section-description">{description}</div>
    """, unsafe_allow_html=True)


def kpi_card(label, value, note, accent):
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color:{accent};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def style_fig(fig, height=380, legend_top=True):
    """Applies one consistent look to every Plotly chart."""
    fig.update_layout(
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        margin=dict(l=30, r=30, t=55, b=30),
        font=dict(family="Inter, Arial", color=TEXT, size=12),
        title=dict(font=dict(size=15, color=NAVY)),
        hoverlabel=dict(bgcolor=NAVY, font_color=WHITE, bordercolor=NAVY),
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    if legend_top:
        fig.update_layout(legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1
        ))
    return fig


# ============================================================
# 4. LOAD DATA
# ============================================================

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
    st.error(f"Required dashboard data file is missing: {error}")
    st.stop()

WEEKS = list(range(2, 12))
ACTUAL_COLS = [f"actual_week_{w}" for w in WEEKS]
PRED_COLS = [f"predicted_week_{w}" for w in WEEKS]


# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 0 25px 0;">
        <div style="color:#B69A68;font-size:11px;font-weight:700;letter-spacing:3px;">
            FASHION INTELLIGENCE
        </div>
        <div style="color:#FFFFFF;font-size:23px;font-weight:700;margin-top:9px;">
            Retail Analytics
        </div>
        <div style="color:#AEB9C5;font-size:12px;margin-top:6px;">
            Demand forecasting platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### DATA FILTERS")

    categories = sorted(
        forecast_data["category"].dropna().unique().tolist()
    )

    seasons = sorted(
        forecast_data["season"].dropna().unique().tolist()
    )

    retail_shops = sorted(
        forecast_data["retail"].dropna().unique().tolist()
    )

    selected_categories = st.multiselect(
        "Product Category",
        categories,
        default=categories
    )

    selected_seasons = st.multiselect(
        "Season",
        seasons,
        default=seasons
    )

    selected_retail = st.multiselect(
        "Retail Shop",
        retail_shops,
        default=retail_shops
    )

    st.divider()

    st.markdown("""
    <div style="padding:10px 0;color:#AEB9C5;font-size:11px;">
        <div style="color:#B69A68;font-weight:700;letter-spacing:1.5px;margin-bottom:8px;">
            PROJECT INFORMATION
        </div>
        Dataset: VISUELLE 2.0<br>
        Forecast horizon: 10 weeks<br>
        Selected model: Random Forest
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 6. FILTER DATA
# ============================================================

filtered_data = forecast_data[
    forecast_data["category"].isin(selected_categories)
    & forecast_data["season"].isin(selected_seasons)
    & forecast_data["retail"].isin(selected_retail)
].copy()

# Per-record totals over the 10 forecast weeks (used by several charts)
filtered_data["actual_total"] = filtered_data[ACTUAL_COLS].sum(axis=1)
filtered_data["predicted_total"] = filtered_data[PRED_COLS].sum(axis=1)

# Sidebar record counter (placed after filtering so it is live)
with st.sidebar:
    st.markdown(
        f"""<div style="font-size:12px;color:#AEB9C5;margin-top:-6px;">
        Showing <b style="color:#B69A68;">{len(filtered_data):,}</b>
        of {len(forecast_data):,} records</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# 7. HERO HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">RETAIL INTELLIGENCE / VISUELLE 2.0</div>
    <div class="hero-title">Fashion Demand Analytics</div>
    <div class="hero-sub">
        Understand demand patterns, evaluate forecasts and explore
        product-level sales predictions.
    </div>
    <span class="hero-pill">10-week horizon</span>
    <span class="hero-pill">Random Forest</span>
    <span class="hero-pill">VISUELLE 2.0</span>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 8. KPI CARDS
# ============================================================

best_model = model_comparison.loc[
    model_comparison["MAE"].idxmin()
]

kpi_values = [
    ("TOTAL PRODUCTS", "5,355", "Products in the full dataset", GOLD),
    ("RETAIL SHOPS", "110", "Retail locations in the dataset", TEAL),
    ("BEST MODEL", str(best_model["Model"]),
     "Lowest MAE among evaluated models", GREEN),
    ("FORECAST WAPE", f'{best_model["WAPE (%)"]:.2f}%',
     "Best model evaluation result", GOLD),
]

for column, item in zip(st.columns(4), kpi_values):
    with column:
        kpi_card(*item)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 9. TABS
# ============================================================

tab_overview, tab_models, tab_explorer = st.tabs(
    ["Overview", "Model Performance", "Product Explorer"]
)


# ------------------------------------------------------------
# TAB 1: OVERVIEW
# ------------------------------------------------------------

with tab_overview:

    section(
        "FORECAST PERFORMANCE",
        "Demand Trend Analysis",
        "Actual demand compared with Random Forest predictions "
        "across the product lifecycle."
    )

    fig_weekly = go.Figure()

    fig_weekly.add_trace(go.Scatter(
        x=weekly_comparison["Week"],
        y=weekly_comparison["Actual_Average"],
        name="Actual Demand",
        mode="lines+markers",
        line=dict(color=NAVY_LIGHT, width=3),
        marker=dict(size=8),
        hovertemplate="%{x}<br>Actual: %{y:.3f}<extra></extra>"
    ))

    fig_weekly.add_trace(go.Scatter(
        x=weekly_comparison["Week"],
        y=weekly_comparison["Predicted_Average"],
        name="Random Forest",
        mode="lines+markers",
        line=dict(color=GOLD, width=3, dash="dot"),
        marker=dict(size=8),
        hovertemplate="%{x}<br>Predicted: %{y:.3f}<extra></extra>"
    ))

    style_fig(fig_weekly, height=390)
    fig_weekly.update_layout(
        xaxis_title="Product Lifecycle Week",
        yaxis_title="Average Sales",
        hovermode="x unified"
    )
    st.plotly_chart(fig_weekly, use_container_width=True)

    st.divider()

    section(
        "SEGMENT ANALYSIS",
        "Your Selection in Detail",
        "These charts react to the sidebar filters."
    )

    if filtered_data.empty:
        st.warning("No records match the selected filters.")

    else:
        a_sum = filtered_data["actual_total"].sum()
        p_sum = filtered_data["predicted_total"].sum()
        seg_wape = (
            (filtered_data["actual_total"]
             - filtered_data["predicted_total"]).abs().sum() / a_sum * 100
            if a_sum else 0
        )

        # Segment KPIs
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Records in view", f"{len(filtered_data):,}")
        s2.metric("Actual sales (10 wks)", f"{a_sum:,.1f}")
        s3.metric(
            "Predicted sales (10 wks)", f"{p_sum:,.1f}",
            delta=f"{(p_sum - a_sum) / a_sum * 100:+.1f}% vs actual"
            if a_sum else None
        )
        s4.metric("Segment WAPE", f"{seg_wape:.2f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # Filtered weekly trend
        seg_actual = filtered_data[ACTUAL_COLS].mean().values
        seg_pred = filtered_data[PRED_COLS].mean().values

        fig_seg = go.Figure()
        fig_seg.add_trace(go.Scatter(
            x=WEEKS, y=seg_actual, name="Actual",
            mode="lines", line=dict(color=NAVY_LIGHT, width=3),
            fill="tozeroy", fillcolor="rgba(36,61,89,0.08)"
        ))
        fig_seg.add_trace(go.Scatter(
            x=WEEKS, y=seg_pred, name="Predicted",
            mode="lines+markers",
            line=dict(color=GOLD, width=3, dash="dot"),
            marker=dict(size=7)
        ))
        style_fig(fig_seg, height=340)
        fig_seg.update_layout(
            title="Average weekly sales: selected segment",
            xaxis=dict(title="Lifecycle Week", tickmode="linear", dtick=1),
            yaxis_title="Average Sales",
            hovermode="x unified"
        )
        st.plotly_chart(fig_seg, use_container_width=True)

        # Category + season breakdown
        c1, c2 = st.columns(2)

        def grouped_bar(col, title):
            g = (filtered_data.groupby(col)[["actual_total", "predicted_total"]]
                 .sum().reset_index())
            g[col] = g[col].astype(str)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=g[col], y=g["actual_total"], name="Actual",
                marker_color=NAVY_LIGHT))
            fig.add_trace(go.Bar(
                x=g[col], y=g["predicted_total"], name="Predicted",
                marker_color=GOLD))
            style_fig(fig, height=340)
            fig.update_layout(title=title, barmode="group", yaxis_title="Total Sales")
            return fig

        with c1:
            st.plotly_chart(
                grouped_bar("category", "Total sales by category"),
                use_container_width=True
            )
        with c2:
            st.plotly_chart(
                grouped_bar("season", "Total sales by season"),
                use_container_width=True
            )

        # Top shops + actual vs predicted scatter
        c3, c4 = st.columns(2)

        with c3:
            top_shops = (filtered_data.groupby("retail")["actual_total"]
                         .sum().nlargest(10).sort_values().reset_index())
            top_shops["retail"] = "Shop " + top_shops["retail"].astype(str)
            fig_shops = go.Figure(go.Bar(
                x=top_shops["actual_total"], y=top_shops["retail"],
                orientation="h", marker_color=TEAL,
                text=top_shops["actual_total"].round(1),
                textposition="outside"
            ))
            style_fig(fig_shops, height=380, legend_top=False)
            fig_shops.update_layout(title="Top 10 shops by actual sales")
            fig_shops.update_xaxes(showgrid=True, gridcolor=GRID)
            st.plotly_chart(fig_shops, use_container_width=True)

        with c4:
            sample = filtered_data.sample(
                min(len(filtered_data), 3000), random_state=42
            )
            max_val = float(max(sample["actual_total"].max(),
                                sample["predicted_total"].max()))
            fig_sc = go.Figure()
            fig_sc.add_trace(go.Scatter(
                x=sample["actual_total"], y=sample["predicted_total"],
                mode="markers", name="Records",
                marker=dict(color=NAVY_LIGHT, size=5, opacity=0.4)
            ))
            fig_sc.add_trace(go.Scatter(
                x=[0, max_val], y=[0, max_val], mode="lines",
                name="Perfect forecast",
                line=dict(color=GOLD, width=2, dash="dash")
            ))
            style_fig(fig_sc, height=380)
            fig_sc.update_layout(
                title="Actual vs predicted (10-week total)",
                xaxis_title="Actual", yaxis_title="Predicted"
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        st.download_button(
            "Download filtered data (CSV)",
            data=filtered_data.to_csv(index=False).encode("utf-8"),
            file_name="filtered_forecast_data.csv",
            mime="text/csv"
        )


# ------------------------------------------------------------
# TAB 2: MODEL PERFORMANCE
# ------------------------------------------------------------

with tab_models:

    section(
        "MACHINE LEARNING EVALUATION",
        "Model Performance",
        "Comparison of forecasting models using MAE, RMSE and WAPE. "
        "Lower values indicate better performance. "
        "The best model in each metric is highlighted in gold."
    )

    st.markdown(
        f"""<div class="insight">
        <b>{best_model["Model"]}</b> achieves the lowest MAE
        ({best_model["MAE"]:.3f}) with a WAPE of
        {best_model["WAPE (%)"]:.2f}%.</div>""",
        unsafe_allow_html=True
    )

    def model_bar(metric, title, fmt):
        best_idx = model_comparison[metric].idxmin()
        colors = [
            GOLD if i == best_idx else "#C9CED4"
            for i in model_comparison.index
        ]
        fig = go.Figure(go.Bar(
            x=model_comparison["Model"],
            y=model_comparison[metric],
            marker_color=colors,
            text=model_comparison[metric],
            texttemplate=fmt,
            textposition="outside"
        ))
        style_fig(fig, height=340, legend_top=False)
        fig.update_layout(title=title, yaxis_title=metric)
        return fig

    m1, m2, m3 = st.columns(3)
    with m1:
        st.plotly_chart(
            model_bar("MAE", "Mean Absolute Error", "%{text:.3f}"),
            use_container_width=True
        )
    with m2:
        st.plotly_chart(
            model_bar("RMSE", "Root Mean Squared Error", "%{text:.3f}"),
            use_container_width=True
        )
    with m3:
        st.plotly_chart(
            model_bar("WAPE (%)", "Weighted Absolute Percentage Error", "%{text:.2f}"),
            use_container_width=True
        )

    st.markdown("#### Detailed Model Comparison")

    metric_cols = [c for c in ["MAE", "RMSE", "WAPE (%)"]
                   if c in model_comparison.columns]
    st.dataframe(
        model_comparison.round(4).style.highlight_min(
            subset=metric_cols, color=GOLD_LIGHT
        ),
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# TAB 3: PRODUCT EXPLORER
# ------------------------------------------------------------

with tab_explorer:

    section(
        "PRODUCT INTELLIGENCE",
        "Product Forecast Explorer",
        "Explore actual and predicted demand for individual "
        "product-retail records."
    )

    if filtered_data.empty:

        st.warning("No records match the selected filters.")

    else:

        explorer_col1, explorer_col2, explorer_col3 = st.columns([2, 2, 1.4])

        with explorer_col1:

            product_options = sorted(
                filtered_data["external_code"].dropna().unique().tolist(),
                key=str
            )

            selected_product = st.selectbox(
                "Select Product",
                product_options
            )

        product_data = filtered_data[
            filtered_data["external_code"] == selected_product
        ]

        with explorer_col2:

            selected_record = st.selectbox(
                "Select Retail Record",
                product_data.index.tolist(),
                format_func=lambda index: (
                    f"Shop {product_data.loc[index, 'retail']} | "
                    f"Season {product_data.loc[index, 'season']}"
                )
            )

        with explorer_col3:
            view_mode = st.radio(
                "View", ["Weekly", "Cumulative"], horizontal=True
            )

        record = product_data.loc[selected_record]

        weeks = WEEKS

        actual_values = [
            record[f"actual_week_{week}"]
            for week in weeks
        ]

        predicted_values = [
            record[f"predicted_week_{week}"]
            for week in weeks
        ]

        fig_product = go.Figure()

        if view_mode == "Weekly":
            fig_product.add_trace(go.Bar(
                x=weeks, y=actual_values, name="Actual Sales",
                marker_color=NAVY_LIGHT, opacity=0.9
            ))
            fig_product.add_trace(go.Scatter(
                x=weeks, y=predicted_values, name="Predicted Sales",
                mode="lines+markers",
                line=dict(color=GOLD, width=3), marker=dict(size=8)
            ))
        else:
            cum_a = pd.Series(actual_values).cumsum()
            cum_p = pd.Series(predicted_values).cumsum()
            fig_product.add_trace(go.Scatter(
                x=weeks, y=cum_a, name="Actual (cumulative)",
                mode="lines", line=dict(color=NAVY_LIGHT, width=3),
                fill="tozeroy", fillcolor="rgba(36,61,89,0.10)"
            ))
            fig_product.add_trace(go.Scatter(
                x=weeks, y=cum_p, name="Predicted (cumulative)",
                mode="lines+markers",
                line=dict(color=GOLD, width=3, dash="dot"),
                marker=dict(size=7)
            ))

        style_fig(fig_product, height=400)
        fig_product.update_layout(
            title=f"Demand Forecast | Product {selected_product}",
            xaxis=dict(title="Product Lifecycle Week", tickmode="linear",
                       dtick=1, showgrid=False),
            yaxis_title="Sales",
            barmode="group",
            hovermode="x unified"
        )

        st.plotly_chart(fig_product, use_container_width=True)

        actual_total = sum(actual_values)
        predicted_total = sum(predicted_values)

        forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

        forecast_col1.metric(
            "Actual Future Sales",
            f"{actual_total:.2f}"
        )

        forecast_col2.metric(
            "Predicted Future Sales",
            f"{predicted_total:.2f}"
        )

        forecast_col3.metric(
            "Forecast Difference",
            f"{predicted_total - actual_total:+.2f}"
        )

        with st.expander("View selected product details"):

            st.write({
                "Product": str(selected_product),
                "Category": str(record["category"]),
                "Color": str(record["color"]),
                "Fabric": str(record["fabric"]),
                "Retail Shop": str(record["retail"]),
                "Season": str(record["season"])
            })


# ============================================================
# 10. FOOTER
# ============================================================

st.divider()

footer_col1, footer_col2 = st.columns(2)

with footer_col1:

    st.markdown("""
    <div style="color:#172536;font-size:12px;font-weight:700;">
        FASHION DEMAND FORECASTING & RETAIL ANALYTICS
    </div>
    <div style="color:#89919A;font-size:11px;margin-top:5px;">
        Machine Learning · Retail Intelligence · VISUELLE 2.0
    </div>
    """, unsafe_allow_html=True)

with footer_col2:

    st.markdown("""
    <div style="text-align:right;color:#89919A;font-size:11px;">
        Built with Python, Scikit-learn, Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)