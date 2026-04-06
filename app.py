import pandas as pd
import streamlit as st
import plotly.express as px

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="AI Geo Dashboard", layout="wide")

st.title("🌍 AI Smart Geo Dashboard")
st.write("Upload CSV → Map + AI Insights + Charts 🚀")

# ==============================
# FILE UPLOAD
# ==============================
file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if file:

    # ==============================
    # LOAD DATA
    # ==============================
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        st.success("✅ File Loaded Successfully")
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

    # ==============================
    # BASIC INFO
    # ==============================
    st.subheader("📄 Data Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.dataframe(df.head())

    # ==============================
    # COLUMN TYPES
    # ==============================
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    # ==============================
    # SIDEBAR FILTERS
    # ==============================
    st.sidebar.header("🎯 Filters")

    filtered_df = df.copy()

    for col in cat_cols:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) < 50:
            selected = st.sidebar.multiselect(col, unique_vals, default=unique_vals)
            if selected:
                filtered_df = filtered_df[filtered_df[col].isin(selected)]

    # ==============================
    # KPIs
    # ==============================
    st.subheader("📊 Key Metrics")

    if num_cols:
        cols = st.columns(min(4, len(num_cols)))
        for i, col in enumerate(num_cols[:4]):
            try:
                cols[i].metric(col, f"{filtered_df[col].mean():.2f}")
            except:
                cols[i].metric(col, "N/A")

    # ==============================
    # 🌍 MAP DETECTION
    # ==============================
    st.subheader("🌍 Smart Map")

    lat_col = None
    lon_col = None
    location_col = None

    for col in df.columns:
        if col.lower() in ["lat", "latitude"]:
            lat_col = col
        elif col.lower() in ["lon", "longitude"]:
            lon_col = col
        elif col.lower() in ["country", "state", "city", "region"]:
            location_col = col

    # ==============================
    # 📍 MAP CLUSTERING (BEST)
    # ==============================
    if lat_col and lon_col:
        st.success("📍 Using Map Clustering (Lat/Lon detected)")

        size_col = num_cols[0] if num_cols else None

        fig = px.scatter_mapbox(
            filtered_df,
            lat=lat_col,
            lon=lon_col,
            size=size_col,
            color=size_col,
            hover_name=location_col if location_col else None,
            zoom=3,
            height=500
        )

        fig.update_layout(mapbox_style="open-street-map")

        st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # 🌎 COUNTRY MAP
    # ==============================
    elif location_col:
        st.success(f"🌎 Choropleth Map using {location_col}")

        try:
            agg_col = num_cols[0] if num_cols else None

            map_data = filtered_df.groupby(location_col)[agg_col].sum().reset_index()

            fig = px.choropleth(
                map_data,
                locations=location_col,
                locationmode="country names",
                color=agg_col,
                title=f"{agg_col} by {location_col}"
            )

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.warning("⚠️ Could not generate map")

    else:
        st.warning("⚠️ No geo columns found (need Lat/Lon or Country)")

    # ==============================
    # 📈 CHART BUILDER
    # ==============================
    st.subheader("📈 Custom Chart")

    chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter"])

    x_col = st.selectbox("X-axis", df.columns)
    y_col = st.selectbox("Y-axis", num_cols) if num_cols else None

    try:
        if chart_type == "Bar":
            fig = px.bar(filtered_df, x=x_col, y=y_col)
        elif chart_type == "Line":
            fig = px.line(filtered_df, x=x_col, y=y_col)
        else:
            fig = px.scatter(filtered_df, x=x_col, y=y_col)

        st.plotly_chart(fig, use_container_width=True)

    except:
        st.warning("⚠️ Chart error")

    # ==============================
    # 🤖 AI INSIGHTS
    # ==============================
    st.subheader("🤖 AI Insights")

    try:
        insights = []

        if num_cols:
            best = filtered_df[num_cols].mean().idxmax()
            worst = filtered_df[num_cols].mean().idxmin()

            insights.append(f"📈 Best performing metric: {best}")
            insights.append(f"📉 Lowest performing metric: {worst}")

        if cat_cols:
            valid_cat = [c for c in cat_cols if not filtered_df[c].dropna().empty]
            if valid_cat:
                top_val = filtered_df[valid_cat[0]].value_counts().idxmax()
                insights.append(f"🏆 Most common in {valid_cat[0]}: {top_val}")

        # Display insights
        for ins in insights:
            st.write(ins)

        if not insights:
            st.info("Not enough data for insights")

    except:
        st.warning("⚠️ Could not generate insights")

    # ==============================
    # DOWNLOAD
    # ==============================
    st.download_button(
        "📥 Download Filtered Data",
        filtered_df.to_csv(index=False),
        file_name="filtered_data.csv"
    )

else:
    st.info("👆 Upload a CSV file to begin")