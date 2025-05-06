import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/hikmashazneen/Sri-Lankan-Science-Tech-Dashboard/refs/heads/main/science_and_tech_sl.csv"
    df = pd.read_csv(url)
    return df

# Load and prepare data
df = load_data()
df['Value'] = df.groupby("Indicator.Name")['Value'].transform(lambda x: x.interpolate())
df.fillna(df.mode().iloc[0], inplace=True)

# Sidebar - Indicator selection and year range
st.sidebar.title("🔧 Filters")
years = sorted(df["Year"].unique())
min_year, max_year = int(min(years)), int(max(years))
selected_year_range = st.sidebar.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Indicator metadata
indicators = {
    "R&D Expenditure (% GDP)": {"desc": "Percentage of GDP invested in research and development.", "unit": "%"},
    "Science Journal Articles": {"desc": "Number of scientific journal articles published.", "unit": "articles"},
    "Patents - Nonresidents": {"desc": "Patents filed in Sri Lanka by nonresidents.", "unit": "patents"},
    "Patents - Residents": {"desc": "Patents filed by Sri Lankan residents.", "unit": "patents"},
    "Researchers in R&D (/mil)": {"desc": "Researchers involved in R&D per million people.", "unit": "per million"},
    "High-tech Exports (% of Mfg Exports)": {"desc": "Share of high-tech in total manufacturing exports.", "unit": "%"},
    "Technicians in R&D (/mil)": {"desc": "Technicians involved in R&D per million people.", "unit": "per million"},
    "High-tech Exports (US$)": {"desc": "Value of high-tech exports in US dollars.", "unit": "USD"}
}

# By default, show only the "Science Journal Articles"
selected_indicators = st.sidebar.multiselect(
    "Choose Indicators to Display", list(indicators.keys()), default=["Science Journal Articles"]
)

# Filter data by year and selected indicators
df_filtered = df[(df["Year"] >= selected_year_range[0]) & (df["Year"] <= selected_year_range[1]) & df["Indicator.Name"].isin(selected_indicators)]

# Page title
st.title("🇱🇰 Sri Lanka Science & Technology Indicators Dashboard")

# Check interpolation warning
if df['Value'].isna().sum() > 0:
    st.warning("Some missing values were interpolated for consistency in visualizations.")

# Indicator display
chart_types = ["line", "bar", "scatter", "area", "line", "bar", "scatter", "area"]
colors = ["#2c7fb8", "#41ab5d", "#1d91c0", "#78c679", "#225ea8", "#31a354", "#0c2c84", "#006d2c"]
cols = st.columns(3)
summary_data = []

for i, (indicator, meta) in enumerate(indicators.items()):
    if indicator not in selected_indicators:
        continue
    data = df_filtered[df_filtered["Indicator.Name"] == indicator].sort_values("Year")
    if data.empty:
        continue

    data["Year"] = pd.to_datetime(data["Year"], format='%Y')
    values = data["Value"]
    years = data["Year"].dt.year
    unit = meta["unit"]

    min_val, max_val, avg_val = round(values.min()), round(values.max()), round(values.mean())
    latest_val = round(values.iloc[-1])
    latest_year = int(years.iloc[-1])
    delta = round(values.iloc[-1] - values.iloc[-2], 2) if len(values) > 1 else 0

    fmt = (lambda x: f"${x:,.0f}" if unit == "USD" else f"{x:,} {unit}")
    chart_type = chart_types[i % len(chart_types)]
    color = colors[i % len(colors)]

    # Chart
    if chart_type == "line":
        fig = go.Figure(go.Scatter(x=years, y=values, mode="lines+markers", line=dict(color=color)))
    elif chart_type == "bar":
        fig = go.Figure(go.Bar(x=years, y=values, marker_color=color))
    elif chart_type == "scatter":
        fig = go.Figure(go.Scatter(x=years, y=values, mode="markers", marker=dict(color=color, size=10)))
    elif chart_type == "area":
        fig = go.Figure(go.Scatter(x=years, y=values, fill="tozeroy", mode="lines", line=dict(color=color)))

    fig.update_traces(hovertemplate=f"<b>Year</b>: %{{x}}<br><b>Value</b>: %{{y:,.2f}} {unit}<extra></extra>")
    fig.update_layout(title={'text': indicator, 'x': 0.5}, height=350, margin=dict(l=10, r=10, t=30, b=20))

    # Display chart
    col = cols[i % 3]
    with col:
        with st.expander(f"📊 {indicator}", expanded=True):
            st.caption(meta["desc"])
            st.metric(label="Latest Value", value=fmt(latest_val), delta=delta)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"**Min:** {fmt(min_val)} | **Max:** {fmt(max_val)} | **Avg:** {fmt(avg_val)}")

    summary_data.append({
        "Indicator": indicator,
        "Min": fmt(min_val),
        "Max": fmt(max_val),
        "Avg": fmt(avg_val),
        "Latest": f"{fmt(latest_val)} ({latest_year})"
    })

# Show summary table
if st.checkbox("Show Summary Table"):
    st.subheader("📋 Summary of Indicators")
    st.dataframe(pd.DataFrame(summary_data))
