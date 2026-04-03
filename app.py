import pandas as pd
import streamlit as st
import plotly.express as px

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Elite Sales Dashboard", layout="wide")

# ==============================
# DARK THEME STYLE
# ==============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0f172a;
    color: white;
}
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("sales23_advanced.csv")
    df.columns = df.columns.str.strip()
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    return df

df = load_data()

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.title("🎯 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    df['Region'].dropna().unique(),
    default=df['Region'].dropna().unique()
)

quarters = st.sidebar.multiselect(
    "Select Quarter",
    df['Quarter'].dropna().unique(),
    default=df['Quarter'].dropna().unique()
)

# ==============================
# FILTER DATA
# ==============================
data = df.copy()

if regions:
    data = data[data['Region'].isin(regions)]

if quarters:
    data = data[data['Quarter'].isin(quarters)]

# ==============================
# TITLE
# ==============================
st.title("🚀 Elite Sales Dashboard")

# ==============================
# KPIs
# ==============================
total_sales = data['Sales'].sum()
total_profit = data['Profit'].sum()
avg_margin = data['Profit_Margin_%'].mean()

# Growth %
monthly = data.groupby(data['Order_Date'].dt.to_period('M'))['Sales'].sum()
growth = monthly.pct_change().mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Profit Margin", f"{avg_margin:.2f}%")
col4.metric("🚀 Growth %", f"{growth:.2f}%")

# ==============================
# CHARTS ROW 1
# ==============================
col1, col2 = st.columns(2)

fig1 = px.bar(
    data.groupby('Category')['Sales'].sum().reset_index(),
    x='Category', y='Sales',
    title="Sales by Category",
    color='Category'
)
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(
    data,
    names='Sales_Category',
    values='Sales',
    title="Sales Distribution"
)
col2.plotly_chart(fig2, use_container_width=True)

# ==============================
# CHARTS ROW 2
# ==============================
col3, col4 = st.columns(2)

fig3 = px.line(
    data.groupby('Order_Date')['Sales'].sum().reset_index(),
    x='Order_Date', y='Sales',
    title="Sales Trend"
)
col3.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(
    data.groupby('High_Discount')['Profit'].sum().reset_index(),
    x='High_Discount', y='Profit',
    title="Discount Impact on Profit"
)
col4.plotly_chart(fig4, use_container_width=True)

# ==============================
# INSIGHTS
# ==============================
st.subheader("🧠 Insights")

if not data.empty:
    top_state = data.groupby('State')['Profit'].sum().idxmax()
    worst_state = data.groupby('State')['Profit'].sum().idxmin()

    st.success(f"🏆 Best State (Profit): {top_state}")
    st.error(f"⚠️ Worst State (Profit): {worst_state}")

# ==============================
# DOWNLOAD BUTTON
# ==============================
st.download_button(
    "📥 Download Filtered Data",
    data.to_csv(index=False),
    file_name="filtered_sales.csv"
)