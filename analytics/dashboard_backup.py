import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="ShopMetrics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------
# PROJECT DATA PATH
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# --------------------------------
# LOAD DATA
# --------------------------------

@st.cache_data
def load_data():
    kpis = pd.read_csv(DATA_DIR / "dashboard_kpis.csv")
    categories = pd.read_csv(DATA_DIR / "category_analysis.csv")
    products = pd.read_csv(DATA_DIR / "product_performance.csv")
    funnel = pd.read_csv(DATA_DIR / "funnel_analysis.csv")

    return kpis, categories, products, funnel


try:
    kpis, categories, products, funnel = load_data()

except FileNotFoundError as error:
    st.error(f"Required data file not found: {error.filename}")
    st.info("Please check the files inside data/processed.")
    st.stop()


# --------------------------------
# HELPER FUNCTION
# --------------------------------

def get_kpi(metric_name, default=0):
    result = kpis.loc[kpis["Metric"] == metric_name, "Value"]

    if result.empty:
        return default

    return float(result.iloc[0])


# --------------------------------
# DASHBOARD HEADER
# --------------------------------

st.title("🛒 ShopMetrics")
st.subheader("E-Commerce Funnel and Basket Analytics")

st.write(
    "Analyze store performance, customer conversion, "
    "product revenue, and cart abandonment."
)

st.divider()


# --------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------

total_sessions = get_kpi("Total Sessions")
total_orders = get_kpi("Total Orders")
total_revenue = get_kpi("Total Revenue")
conversion_rate = get_kpi("Conversion Rate (%)")
cart_abandonment = get_kpi("Cart Abandonment Rate (%)")
average_order_value = get_kpi("Average Order Value")

st.header("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sessions", f"{total_sessions:,.0f}")
col2.metric("Total Orders", f"{total_orders:,.0f}")
col3.metric("Total Revenue", f"₹{total_revenue:,.2f}")

col4, col5, col6 = st.columns(3)

col4.metric("Conversion Rate", f"{conversion_rate:.2f}%")
col5.metric("Cart Abandonment", f"{cart_abandonment:.2f}%")
col6.metric("Average Order Value", f"₹{average_order_value:,.2f}")

st.divider()


# --------------------------------
# CATEGORY-WISE REVENUE
# --------------------------------

st.header("Category-wise Revenue Analysis")

if not categories.empty:
    category_chart = px.bar(
        categories,
        x="category",
        y="total_revenue",
        title="Revenue by Product Category",
        labels={
            "category": "Product Category",
            "total_revenue": "Revenue (₹)"
        },
        text_auto=".2s"
    )

    category_chart.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(category_chart, use_container_width=True)

else:
    st.info("No category data available.")


st.divider()


# --------------------------------
# TOP 10 PRODUCTS
# --------------------------------

st.header("Top 10 Products by Revenue")

if not products.empty:
    top_products = products.nlargest(10, "total_revenue")

    product_chart = px.bar(
        top_products.sort_values("total_revenue"),
        x="total_revenue",
        y="product_name",
        orientation="h",
        title="Top 10 Revenue-Generating Products",
        labels={
            "product_name": "Product",
            "total_revenue": "Revenue (₹)"
        },
        text_auto=".2s"
    )

    product_chart.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Product"
    )

    st.plotly_chart(product_chart, use_container_width=True)

else:
    st.info("No product data available.")


st.divider()


# --------------------------------
# E-COMMERCE FUNNEL
# --------------------------------

st.header("E-Commerce Conversion Funnel")

if not funnel.empty:
    funnel_chart = px.funnel(
        funnel,
        x="Sessions",
        y="Stage",
        title="Customer Journey: Page View to Purchase",
        labels={
            "Sessions": "Number of Sessions",
            "Stage": "Funnel Stage"
        }
    )

    st.plotly_chart(funnel_chart, use_container_width=True)

    st.subheader("Funnel Details")
    st.dataframe(funnel, use_container_width=True)

else:
    st.info("No funnel data available.")


st.divider()


# --------------------------------
# CATEGORY DATA TABLE
# --------------------------------

st.header("Category Performance Details")

st.dataframe(
    categories,
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "ShopMetrics | E-Commerce Funnel and Basket Analytics"
)

st.caption(
    "Developed using Python, Pandas, Streamlit, and Plotly."
)