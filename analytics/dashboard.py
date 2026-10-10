import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="ShopMetrics | Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------
# CUSTOM THEME
# ---------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

st.sidebar.title("⚙️ Dashboard Settings")

theme = st.sidebar.radio(
    "Choose Theme",
    ["Light", "Dark"],
    index=0 if st.session_state.theme == "Light" else 1
)

st.session_state.theme = theme

if theme == "Dark":
    background = "#0E1117"
    text_color = "#FAFAFA"
    card_color = "#1E293B"
    border_color = "#334155"
else:
    background = "#F5F7FB"
    text_color = "#172033"
    card_color = "#FFFFFF"
    border_color = "#DCE3ED"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background};
        color: {text_color};
    }}

    [data-testid="stSidebar"] {{
        background-color: {card_color};
    }}

    [data-testid="stMetric"] {{
        background-color: {card_color};
        border: 1px solid {border_color};
        padding: 18px;
        border-radius: 12px;
    }}

    h1, h2, h3, p, label {{
        color: {text_color};
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {border_color};
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# DATA PATHS
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# ---------------------------------
# LOAD DATA
# ---------------------------------

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
    st.info("Check the files inside data/processed.")
    st.stop()


# ---------------------------------
# HELPER FUNCTION
# ---------------------------------

def get_kpi(metric_name, default=0):
    result = kpis.loc[
        kpis["Metric"] == metric_name,
        "Value"
    ]

    if result.empty:
        return default

    return float(result.iloc[0])


# ---------------------------------
# HEADER
# ---------------------------------

st.title("🛒 ShopMetrics")
st.subheader("E-Commerce Funnel & Basket Analytics")

st.caption(
    "Monitor store performance, discover product trends, "
    "and understand customer conversion."
)

st.divider()


# ---------------------------------
# CATEGORY FILTER
# ---------------------------------

st.sidebar.subheader("📊 Data Filters")

if not categories.empty:
    category_options = ["All Categories"] + sorted(
        categories["category"].dropna().unique().tolist()
    )

    selected_category = st.sidebar.selectbox(
        "Select Product Category",
        category_options
    )
else:
    selected_category = "All Categories"


if selected_category == "All Categories":
    filtered_categories = categories.copy()
    filtered_products = products.copy()
else:
    filtered_categories = categories[
        categories["category"] == selected_category
    ].copy()

    filtered_products = products[
        products["category"] == selected_category
    ].copy()


# ---------------------------------
# KPI CARDS
# ---------------------------------

# ---------------------------------
# KPI CARDS
# ---------------------------------

total_sessions = get_kpi("Total Sessions")
total_orders = get_kpi("Total Orders")
total_revenue = get_kpi("Total Revenue")
conversion_rate = get_kpi("Conversion Rate (%)")
cart_abandonment = get_kpi("Cart Abandonment Rate (%)")
average_order_value = get_kpi("Average Order Value")

st.header("📈 Key Performance Indicators")

if selected_category == "All Categories":
    # Show overall business KPIs
    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Total Sessions", f"{total_sessions:,.0f}")
    col2.metric("🛍️ Total Orders", f"{total_orders:,.0f}")
    col3.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")

    col4, col5, col6 = st.columns(3)

    col4.metric("🎯 Conversion Rate", f"{conversion_rate:.2f}%")
    col5.metric("🛒 Cart Abandonment", f"{cart_abandonment:.2f}%")
    col6.metric("🧾 Average Order Value", f"₹{average_order_value:,.2f}")

else:
    # Show metrics for the selected product category
    category_revenue = filtered_categories["total_revenue"].sum()

    category_units = filtered_categories["units_sold"].sum()

    category_products = filtered_products["product_id"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("📦 Selected Category", selected_category)
    col2.metric("💰 Category Revenue", f"₹{category_revenue:,.2f}")
    col3.metric("🛍️ Units Sold", f"{category_units:,.0f}")

    col4, col5 = st.columns(2)

    col4.metric("🏷️ Products in Category", f"{category_products:,.0f}")

    col5.metric(
        "📊 Share of Total Revenue",
        f"{(category_revenue / total_revenue * 100) if total_revenue else 0:.2f}%"
    )

st.divider()

# ---------------------------------
# REVENUE BY CATEGORY
# ---------------------------------

st.header("📦 Category-wise Revenue Analysis")

if not filtered_categories.empty:
    category_chart = px.bar(
        filtered_categories.sort_values(
            "total_revenue",
            ascending=False
        ),
        x="category",
        y="total_revenue",
        text="total_revenue",
        title="Revenue by Product Category",
        labels={
            "category": "Product Category",
            "total_revenue": "Revenue (₹)"
        },
        color="category",
        template="plotly_dark" if theme == "Dark" else "plotly_white"
    )

    category_chart.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    category_chart.update_layout(
        showlegend=False,
        yaxis_title="Revenue (₹)",
        xaxis_title="Category"
    )

    st.plotly_chart(category_chart, use_container_width=True)
else:
    st.info("No category data available.")

st.divider()


# ---------------------------------
# TOP PRODUCTS
# ---------------------------------

st.header("🏆 Top 10 Products by Revenue")

if not filtered_products.empty:
    top_products = filtered_products.nlargest(
        10,
        "total_revenue"
    ).sort_values("total_revenue")

    product_chart = px.bar(
        top_products,
        x="total_revenue",
        y="product_name",
        orientation="h",
        text="total_revenue",
        title="Best Revenue-Generating Products",
        labels={
            "product_name": "Product",
            "total_revenue": "Revenue (₹)"
        },
        template="plotly_dark" if theme == "Dark" else "plotly_white"
    )

    product_chart.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    product_chart.update_layout(
        yaxis_title="Product",
        xaxis_title="Revenue (₹)"
    )

    st.plotly_chart(product_chart, use_container_width=True)
else:
    st.info("No product data available for this category.")

st.divider()


# ---------------------------------
# CONVERSION FUNNEL
# ---------------------------------

st.header("🔻 E-Commerce Conversion Funnel")

if not funnel.empty:
    funnel_chart = px.funnel(
        funnel,
        x="Sessions",
        y="Stage",
        title="Customer Journey: Page View to Purchase",
        labels={
            "Sessions": "Number of Sessions",
            "Stage": "Funnel Stage"
        },
        template="plotly_dark" if theme == "Dark" else "plotly_white"
    )

    st.plotly_chart(
        funnel_chart,
        use_container_width=True
    )

    st.subheader("Funnel Details")

    st.dataframe(
        funnel.round(2),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No funnel data available.")

st.divider()


# ---------------------------------
# BUSINESS INSIGHTS
# ---------------------------------

st.header("💡 Business Insights")

if not categories.empty:
    best_category = categories.loc[
        categories["total_revenue"].idxmax()
    ]

    insight1, insight2 = st.columns(2)

    with insight1:
        st.metric(
            "🥇 Highest Revenue Category",
            str(best_category["category"]),
            f"₹{best_category['total_revenue']:,.0f}"
        )

    with insight2:
        st.metric(
            "📉 Cart Abandonment Rate",
            f"{cart_abandonment:.2f}%"
        )

    st.info(
        f"The {best_category['category']} category currently "
        "generates the highest revenue in this dataset. "
        "Review its products to identify useful sales patterns."
    )

if not funnel.empty and "Drop-off" in funnel.columns:
    dropoff_stages = funnel[
        funnel["Stage"].str.lower() != "page view"
    ]

    if not dropoff_stages.empty:
        largest_dropoff = dropoff_stages.loc[
            dropoff_stages["Drop-off"].idxmax()
        ]

        st.warning(
            f"Largest recorded funnel drop-off: "
            f"{largest_dropoff['Stage']} — "
            f"{largest_dropoff['Drop-off']:.2f}%."
        )

st.divider()


# ---------------------------------
# CATEGORY PERFORMANCE TABLE
# ---------------------------------

st.header("📋 Category Performance Details")

if not filtered_categories.empty:
    display_categories = filtered_categories.copy()

    if "total_revenue" in display_categories.columns:
        display_categories["total_revenue"] = (
            display_categories["total_revenue"].map(
                lambda value: f"₹{value:,.2f}"
            )
        )

    st.dataframe(
        display_categories,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.caption(
    "ShopMetrics | E-Commerce Funnel and Basket Analytics"
)

st.caption(
    "Built with Python, Pandas, Streamlit, and Plotly."
)

st.caption(
    "Note: This dashboard uses generated sample data for analysis."
)