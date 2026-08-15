import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Energy Intelligence Platform",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Energy Intelligence Platform")


# =========================================================
# SIDEBAR — FILE UPLOAD
# =========================================================

with st.sidebar:
    st.header("Filters")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )


# =========================================================
# INITIAL SCREEN
# =========================================================

if uploaded_file is None:
    st.info("Upload an energy dataset using the sidebar to begin the analysis.")
    st.stop()


# =========================================================
# READ DATASET
# =========================================================

df = pd.read_csv(uploaded_file)

    

# =========================================================
# SIDEBAR — FILTERS
# =========================================================

with st.sidebar:
    state_options = sorted(df["StateCode"].dropna().unique())

    state1 = st.selectbox(
        "State 1",
        state_options
    )

    state2 = st.selectbox(
        "State 2",
        state_options,
        index=1 if len(state_options) > 1 else 0
    )

    state1_indicators = df.loc[
        df["StateCode"] == state1,
        "MSN"
    ].dropna().unique()

    msn = st.selectbox(
        "Energy Indicator",
        sorted(state1_indicators)
    )



# =========================================================
# CREATE DATAFRAMES FOR BOTH STATES
# =========================================================

chart_df1 = df[
    (df["StateCode"] == state1) &
    (df["MSN"] == msn)
].copy()

chart_df2 = df[
    (df["StateCode"] == state2) &
    (df["MSN"] == msn)
].copy()


# =========================================================
# YEAR RANGE FILTER
# =========================================================

years = sorted(
    set(chart_df1["Year"].dropna().unique()) |
    set(chart_df2["Year"].dropna().unique())
)

if not years:
    st.error("No data is available for the selected states and indicator.")
    st.stop()

with st.sidebar:
    year_range = st.select_slider(
        "Year Range",
        options=years,
        value=(years[0], years[-1])
    )
    map_year = st.selectbox(
    "Map Year",
    options=years,
    index=len(years) - 1
    )


chart_df1 = chart_df1[
    (chart_df1["Year"] >= year_range[0]) &
    (chart_df1["Year"] <= year_range[1])
].sort_values("Year")

ml_df = chart_df1[["Year", "Data"]].dropna().copy()

X = ml_df[["Year"]]
y = ml_df["Data"]

model = LinearRegression()
model.fit(X, y)



last_year = int(ml_df["Year"].max())

future_years = pd.DataFrame({
    "Year": range(last_year + 1, last_year + 6)
})

future_years["Predicted Data"] = model.predict(
    future_years[["Year"]]
)

st.subheader("📈 Experimental 5-Year Trend Projection")

forecast_fig = px.line(
    future_years,
    x="Year",
    y="Predicted Data",
    markers=True,
    title=f"Experimental Trend Projection for {state1} | {msn}"
)

forecast_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Predicted Energy Value",
    template="plotly_dark",
    height=400,
    xaxis=dict(
    tickmode="linear",
    dtick=1
    )
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)


chart_df2 = chart_df2[
    (chart_df2["Year"] >= year_range[0]) &
    (chart_df2["Year"] <= year_range[1])
].sort_values("Year")


if chart_df1.empty:
    st.error(
        f"No data is available for {state1}, indicator {msn}, "
        f"between {year_range[0]} and {year_range[1]}."
    )
    st.stop()


# =========================================================
# US MAP
# =========================================================

map_df = df[
    (df["MSN"] == msn) &
    (df["Year"] == map_year) &
    (df["StateCode"] != "US")
].copy()


top_state = map_df.loc[map_df["Data"].idxmax()]

st.subheader(f"🗺️ US Energy Consumption Map — {map_year}")

fig_map = px.choropleth(
    map_df,
    locations="StateCode",
    locationmode="USA-states",
    color="Data",
    scope="usa",
    color_continuous_scale="Viridis",
    labels={
        "StateCode": "State",
        "Data": "Average Value"
    },
    hover_data={
        "StateCode": True,
        "Data": ":,.2f"
    }
)

fig_map.update_layout(
    height=550,
    margin=dict(l=0, r=0, t=20, b=0),
    coloraxis_colorbar_title="Average"
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


# =========================================================
# COMPARISON DATAFRAME
# =========================================================

state1_comparison = chart_df1.copy()
state1_comparison["State"] = state1

state2_comparison = chart_df2.copy()
state2_comparison["State"] = state2

comparison_df = pd.concat(
    [state1_comparison, state2_comparison],
    ignore_index=True
)


# =========================================================
# COMPARISON CHART
# =========================================================

st.subheader("📊 State Comparison")

fig = px.line(
    comparison_df,
    x="Year",
    y="Data",
    color="State",
    markers=True,
    color_discrete_sequence=["#00B4FF", "#FF8C00"],
    hover_data={
        "Year": True,
        "Data": ":,.2f",
        "State": True
    }
)

fig.update_layout(
    title={
        "text": f"📈 {state1} vs {state2} | {msn}",
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title="Year",
    yaxis_title="Energy Value",
    template="plotly_dark",
    height=420,
    margin=dict(l=20, r=20, t=60, b=20),
    legend_title_text="State"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=6)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CALCULATIONS
# =========================================================

peak_row = chart_df1.loc[chart_df1["Data"].idxmax()]
minimum_row = chart_df1.loc[chart_df1["Data"].idxmin()]

average_state1 = chart_df1["Data"].mean()
average_state2 = (
    chart_df2["Data"].mean()
    if not chart_df2.empty
    else float("nan")
)

difference = average_state1 - average_state2

min_value = chart_df1["Data"].min()
max_value = chart_df1["Data"].max()
mean_value = chart_df1["Data"].mean()


# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

st.subheader("🤖 AI Insights")

if chart_df2.empty:
    comparison_text = (
        f"No comparison data is available for {state2} "
        f"during the selected period."
    )
else:
    comparison_text = (
        f"The average difference between {state1} and "
        f"{state2} is {difference:,.2f}."
    )

st.info(
    f"""
📈 **Peak Consumption:** {peak_row["Data"]:,.2f} in {int(peak_row["Year"])}

📉 **Lowest Consumption:** {minimum_row["Data"]:,.2f} in {int(minimum_row["Year"])}

📊 **Average Consumption ({state1}):** {average_state1:,.2f}

⚖️ **Comparison:** {comparison_text}
"""
)


# =========================================================
# SUMMARY METRICS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Minimum",
        f"{min_value:,.2f}"
    )

with col2:
    st.metric(
        "Average",
        f"{mean_value:,.2f}"
    )

with col3:
    st.metric(
        "Maximum",
        f"{max_value:,.2f}"
    )


# =========================================================
# DATASET PREVIEW
# =========================================================

st.subheader("📋 Dataset Preview")

preview_df = chart_df1.sort_values(
    "Year",
    ascending=False
).head(20)

st.dataframe(
    preview_df,
    use_container_width=True
)