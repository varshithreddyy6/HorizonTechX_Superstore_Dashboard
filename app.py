import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
df = pd.read_csv("data/Superstore.csv", encoding="latin1")

# DATE CONVERSION
df["Order Date"] = pd.to_datetime(df["Order Date"])

# SIDEBAR FILTERS
st.sidebar.title("Dashboard Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

state = st.sidebar.multiselect(
    "Select State",
    options=df["State"].unique(),
    default=df["State"].unique()
)

# FILTER DATA
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["State"].isin(state))
]

# TITLE
st.title("Superstore Sales Dashboard")
st.markdown("Interactive Data Visualization Dashboard")

st.divider()

# KPI CARDS
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
profit_margin = (total_profit / total_sales) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")

with col3:
    st.metric("Total Orders", total_orders)

with col4:
    st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# CHARTS ROW 1
col1, col2 = st.columns(2)

with col1:
    sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()

    fig = px.bar(
        sales_region,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    st.plotly_chart(fig, width="stretch")

with col2:
    profit_category = filtered_df.groupby("Category")["Profit"].sum().reset_index()

    fig = px.pie(
        profit_category,
        names="Category",
        values="Profit",
        title="Profit by Category"
    )

    st.plotly_chart(fig, width="stretch")

# CHARTS ROW 2
col1, col2 = st.columns(2)

with col1:
    monthly_sales = filtered_df.groupby(
        filtered_df["Order Date"].dt.strftime("%Y-%m")
    )["Sales"].sum().reset_index()

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, width="stretch")

with col2:
    segment_sales = filtered_df.groupby("Segment")["Sales"].sum().reset_index()

    fig = px.bar(
        segment_sales,
        x="Segment",
        y="Sales",
        color="Segment",
        title="Sales by Segment"
    )

    st.plotly_chart(fig, width="stretch")

# TOP PRODUCTS
top_products = filtered_df.groupby("Product Name")["Sales"].sum().reset_index()

top_products = top_products.sort_values(
    by="Sales",
    ascending=False
).head(10)

fig = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# ADVANCED ANALYTICS
st.subheader("Advanced Analytics")

col1, col2, col3 = st.columns(3)

# BEST STATE
best_state = filtered_df.groupby("State")["Sales"].sum().idxmax()

# WORST CATEGORY
worst_category = filtered_df.groupby("Category")["Profit"].sum().idxmin()

# BEST MONTH
best_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax(),
    "Order Date"
]

with col1:
    st.success(f"Best Performing State: {best_state}")

with col2:
    st.error(f"Worst Performing Category: {worst_category}")

with col3:
    st.info(f"Highest Sales Month: {best_month}")

st.divider()

# DATASET PREVIEW
st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_df)

# DOWNLOAD BUTTON
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_superstore_data.csv",
    mime="text/csv"
)