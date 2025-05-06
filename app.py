import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sri Lanka Science & Tech Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #006699;'>🇱🇰 Sri Lanka - Science & Technology Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/hikmashazneen/Sri-Lankan-Science-Tech-Dashboard/main/science_and_tech_sl.csv"
    return pd.read_csv(url)

# Load data
with st.spinner("Loading dataset..."):
    df = load_data()

df['Year'] = df['Year'].astype(str)

# Sidebar - Multi-year filter
st.sidebar.header("📅 Select Year(s)")
year_options = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Choose one or more years (default: all):",
    options=year_options,
    default=year_options
)

# Filter data
filtered_df = df[df['Year'].isin(selected_years)]

# Chart configurations
chart_settings = {
    'Research and development expenditure (% of GDP)': {
        'type': 'line',
        'title': 'R&D Expenditure Over Time',
        'unit': '% of GDP',
        'description': 'Annual expenditure on Research & Development as a percentage of GDP in Sri Lanka.'
    },
    'Scientific and technical journal articles': {
        'type': 'bar',
        'title': 'Scientific and Technical Journal Articles',
        'unit': 'Articles',
        'description': 'Total number of scientific and technical journal articles published per year.'
    },
    'Patent applications, nonresidents': {
        'type': 'area',
        'title': 'Nonresident Patent Applications',
        'unit': 'Applications',
        'description': 'Number of patent applications filed in Sri Lanka by nonresidents.'
    },
    'Researchers in R&D (per million people)': {
        'type': 'scatter',
        'title': 'Researchers in R&D',
        'unit': 'Per million people',
        'description': 'Researchers engaged in R&D per million people.'
    },
    'Technicians in R&D (per million people)': {
        'type': 'line',
        'title': 'Technicians in R&D',
        'unit': 'Per million people',
        'description': 'Technicians in R&D per million people.'
    },
    'High-technology exports (% of manufactured exports)': {
        'type': 'line',
        'title': 'High-Tech Exports',
        'unit': '% of manufactured exports',
        'description': 'Share of high-tech exports in total manufactured exports.'
    },
    'Charges for the use of intellectual property, payments (BoP, current US$)': {
        'type': 'bar',
        'title': 'IP Usage Payments',
        'unit': 'USD',
        'description': 'Payments for the use of intellectual property rights (e.g., licensing fees).'
    },
    'Charges for the use of intellectual property, receipts (BoP, current US$)': {
        'type': 'bar',
        'title': 'IP Usage Receipts',
        'unit': 'USD',
        'description': 'Receipts from granting IP rights usage to foreign entities.'
    }
}

# Display all charts
st.markdown("## 📊 Science & Technology Indicators in Sri Lanka")
for indicator, settings in chart_settings.items():
    data = filtered_df[filtered_df['Indicator.Name'] == indicator]
    if data.empty:
        st.warning(f"No data found for {indicator} in the selected year(s).")
        continue

    if settings['type'] == 'line':
        fig = px.line(data, x="Year", y="Value", markers=True, title=settings['title'],
                      labels={"Value": settings['unit'], "Year": "Year"})
    elif settings['type'] == 'bar':
        fig = px.bar(data, x="Year", y="Value", title=settings['title'],
                     labels={"Value": settings['unit'], "Year": "Year"})
    elif settings['type'] == 'area':
        fig = px.area(data, x="Year", y="Value", title=settings['title'],
                      labels={"Value": settings['unit'], "Year": "Year"})
    elif settings['type'] == 'scatter':
        fig = px.scatter(data, x="Year", y="Value", size="Value", title=settings['title'],
                         labels={"Value": settings['unit'], "Year": "Year"})

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"**Description:** {settings['description']}")
    st.markdown("---")
