import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Energy Intelligence Platform",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Energy Intelligence Platform")

st.write("Upload an energy dataset to begin the analysis.")

with st.sidebar:
    st.header("Filters")

    uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
    )
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    col1, col2 = st.columns(2)

    with col1:
      state1 = st.selectbox(
        "State 1",
        sorted(df["StateCode"].unique())
      )

    filtered_df = df[df["StateCode"] == state1]
    
    msn = st.selectbox(
        "Energy Indicator",
        sorted(filtered_df["MSN"].unique())
    )

    with col2:
      state2 = st.selectbox(
        "State 2",
        sorted(df["StateCode"].unique()),
        index=1
      )
    chart_df1 = df[
     (df["StateCode"] == state1) &
     (df["MSN"] == msn)
   ]

    chart_df2 = df[
     (df["StateCode"] == state2) &
     (df["MSN"] == msn)
    ]

    years = sorted(chart_df1["Year"].unique())

    st.markdown("### 📅 Select Year Range")

    year_range = st.select_slider(
    "Years",
    options=years,
    value=(years[0], years[-1]),
    label_visibility="collapsed"
    )

    chart_df1 = chart_df1[
     (chart_df1["Year"] >= year_range[0]) &
     (chart_df1["Year"] <= year_range[1])
    ]

    chart_df2 = chart_df2[
     (chart_df2["Year"] >= year_range[0]) &
     (chart_df2["Year"] <= year_range[1])
    ]

    min_value = chart_df1["Data"].min()
    max_value = chart_df1["Data"].max()
    mean_value = chart_df1["Data"].mean()

    st.caption("Dataset loaded successfully")

    st.subheader("📊 Dataset Summary")
    
    # metrics

    comparison_df = pd.concat([chart_df1, chart_df2])

    comparison_df["State"] = (
     [state1] * len(chart_df1) +
     [state2] * len(chart_df2)
    )

    fig = px.line(
      comparison_df,
      x="Year",
      y="Data",
      color="State",
      markers=True,
      color_discrete_sequence=["#00B4FF", "#FF8C00"]
  )

    fig.update_layout(
      title={
        "text": f"📈 {state1} vs {state2} | {msn}",
        "x": 0.5,
        "xanchor": "center"
      },
      xaxis_title="Year",
      yaxis_title="Energy Consumption",
      template="plotly_dark",
      height=420,
      margin=dict(l=20, r=20, t=50, b=20),
      showlegend=False
    )

    fig.update_traces(
      line=dict(width=3),
      marker=dict(size=6)
     )

    st.plotly_chart(fig, use_container_width=True)


    col1, col2, col3 = st.columns(3)

    with col1:
      st.metric("Minimum", f"{min_value:,.2f}")

    with col2:
      st.metric("Average", f"{mean_value:,.2f}")

    with col3:
      st.metric("Maximum", f"{max_value:,.2f}")

    st.subheader("📋 Dataset Preview")

    st.dataframe(
      chart_df1.sort_values("Year", ascending=False).head(20)
    )
  
