import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load data and cache it
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/hikmashazneen/Sri-Lankan-Science-Tech-Dashboard/refs/heads/main/science_and_tech_sl.csv"
    df = pd.read_csv(url)
    return df

# Load the data
df = load_data()

# Impute missing values (fill with mean or median for numeric, mode for categorical)
df.fillna(df.mean(numeric_only=True), inplace=True)  # For numerical columns
df.fillna(df.mode().iloc[0], inplace=True)  # For categorical columns

# Page setup
st.set_page_config(layout="wide")
st.title("Sri Lanka Science & Technology Indicators Dashboard")
st.markdown("""
This interactive dashboard presents key science and technology indicators for Sri Lanka. 
Explore how the country is progressing in R&D investment, research publications, patents, 
and high-tech exports across different years.
""")

# Open the sidebar by default
st.sidebar.markdown("### Select Year Range")
years = sorted(df["Year"].unique())
min_year, max_year = int(min(years)), int(max(years))
selected_year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter data
df_filtered = df[(df["Year"] >= selected_year_range[0]) & (df["Year"] <= selected_year_range[1])]

# Indicator details
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

# Chart types and colors
chart_types = ["line", "bar", "scatter", "area", "line", "bar", "scatter", "area"]
colors = ["#2c7fb8", "#41ab5d", "#1d91c0", "#78c679", "#225ea8", "#31a354", "#0c2c84", "#006d2c"]

# Layout
cols = st.columns(3)

# Loop over indicators
for i, (indicator, meta) in enumerate(indicators.items()):
    data = df_filtered[df_filtered["Indicator.Name"] == indicator].sort_values("Year")
    values = data["Value"]
    unit = meta["unit"]

    min_val = round(values.min())
    max_val = round(values.max())
    avg_val = round(values.mean())

    # Fix for R&D Expenditure showing zeros (check for NaN and proper float conversion)
    if unit == "USD":
        min_str = f"${min_val:,.0f}"
        max_str = f"${max_val:,.0f}"
        avg_str = f"${avg_val:,.0f}"
    else:
        min_str = f"{min_val:,} {unit}"
        max_str = f"{max_val:,} {unit}"
        avg_str = f"{avg_val:,} {unit}"

    # Choose chart type
    chart_type = chart_types[i % len(chart_types)]
    color = colors[i % len(colors)]

    if chart_type == "line":
        fig = go.Figure(go.Scatter(x=data["Year"], y=data["Value"], mode="lines+markers", line=dict(color=color)))
    elif chart_type == "bar":
        fig = go.Figure(go.Bar(x=data["Year"], y=data["Value"], marker_color=color))
    elif chart_type == "scatter":
        fig = go.Figure(go.Scatter(x=data["Year"], y=data["Value"], mode="markers", marker=dict(color=color, size=10)))
    elif chart_type == "area":
        fig = go.Figure(go.Scatter(x=data["Year"], y=data["Value"], fill="tozeroy", mode="lines", line=dict(color=color)))

    fig.update_layout(
        title={'text': indicator, 'x': 0.5, 'xanchor': 'center'},
        margin=dict(l=10, r=10, t=30, b=20),
        height=300
    )

    # Display chart and metrics
    with cols[i % 3]:
        st.markdown(f"#### {indicator}")
        st.caption(meta["desc"])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**Min:** {min_str} | **Max:** {max_str} | **Avg:** {avg_str}")
