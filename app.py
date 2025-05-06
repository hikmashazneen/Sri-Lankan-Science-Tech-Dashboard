import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sri Lanka Science & Tech Dashboard", layout="wide")

# Title with formatting
st.markdown("<h1 style='text-align: center; color: #006699;'>🇱🇰 Sri Lanka - Science & Technology Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Cached data loader
@st.cache_data
def load_data():
    return pd.read_csv("science_and_tech_sl.csv")

# Load data
with st.spinner("Loading dataset..."):
    df = load_data()

# Convert year to string for filtering
df['Year'] = df['Year'].astype(str)

# Sidebar - Filtering
st.sidebar.header("🔍 Filter the Data")

# Multi-select for year selection
selected_years = st.sidebar.multiselect(
    "📅 Select Year(s):", sorted(df['Year'].unique()), default=sorted(df['Year'].unique())
)

# Multi-select for indicators
indicators = df['Indicator.Name'].unique()
selected_indicators = st.sidebar.multiselect(
    "📊 Select Indicator(s):", indicators, default=[]
)

if st.sidebar.button("✅ Apply Filters"):
    st.success("Filters applied! See the updated charts below 👇")

# Filter the dataframe based on selected years
filtered_df = df[df['Year'].isin(selected_years)]

# Collapsible KPIs Section
with st.expander("🔎 Key Science & Tech KPIs (Selected Years)", expanded=True):
    selected_data = df[df['Year'].isin(selected_years)]
    st.markdown(f"### 📌 Insights for {', '.join(selected_years)}")

    col1, col2, col3 = st.columns(3)

    with col1:
        rd_value = selected_data[selected_data['Indicator.Name'] == 'Research and development expenditure (% of GDP)']['Value'].sum()
        st.metric("R&D Expenditure (% of GDP)", f"{rd_value:.2f}%")

    with col2:
        articles = selected_data[selected_data['Indicator.Name'] == 'Scientific and technical journal articles']['Value'].sum()
        st.metric("Sci. Journal Articles", int(articles))

    with col3:
        patents = selected_data[selected_data['Indicator.Name'] == 'Patent applications, nonresidents']['Value'].sum()
        st.metric("Nonresident Patents", int(patents))

# Chart mappings
chart_map = {
    'Research and development expenditure (% of GDP)': 'line',
    'Scientific and technical journal articles': 'bar',
    'Patent applications, nonresidents': 'area',
    'Researchers in R&D (per million people)': 'scatter',
    'Technicians in R&D (per million people)': 'pie',
    'High-technology exports (% of manufactured exports)': 'histogram',
    'Charges for the use of intellectual property, payments (BoP, current US$)': 'box',
    'Charges for the use of intellectual property, receipts (BoP, current US$)': 'funnel'
}

label_map = {
    'Research and development expenditure (% of GDP)': ('R&D Expenditure Over Time', 'R&D (% of GDP)'),
    'Scientific and technical journal articles': ('Scientific Journal Articles', 'Articles'),
    'Patent applications, nonresidents': ('Nonresident Patent Applications', 'Applications'),
    'Researchers in R&D (per million people)': ('Researchers per Million', 'Researchers'),
    'Technicians in R&D (per million people)': ('Technicians per Million', 'Technicians'),
    'High-technology exports (% of manufactured exports)': ('High-Tech Exports', 'Export %'),
    'Charges for the use of intellectual property, payments (BoP, current US$)': ('IP Usage Payments', 'Payments (USD)'),
    'Charges for the use of intellectual property, receipts (BoP, current US$)': ('IP Usage Receipts', 'Receipts (USD)')
}

# Chart Display
st.markdown("---")
st.markdown("## 📈 Selected Indicator Visualizations")

if not selected_indicators:
    st.info("Please select at least one indicator from the sidebar to view charts.")
else:
    for indicator in selected_indicators:
        data = filtered_df[filtered_df['Indicator.Name'] == indicator]
        if data.empty:
            st.warning(f"No data found for {indicator} in selected year(s).")
            continue

        chart_type = chart_map.get(indicator, 'line')
        title, yaxis = label_map.get(indicator, (indicator, 'Value'))

        with st.expander(f"📊 {title}"):
            if chart_type == 'line':
                fig = px.line(data, x="Year", y="Value", markers=True, labels={"Value": yaxis, "Year": "Year"})
            elif chart_type == 'bar':
                fig = px.bar(data, x="Year", y="Value", labels={"Value": yaxis, "Year": "Year"})
            elif chart_type == 'area':
                fig = px.area(data, x="Year", y="Value", labels={"Value": yaxis, "Year": "Year"})
            elif chart_type == 'scatter':
                fig = px.scatter(data, x="Year", y="Value", size="Value", labels={"Value": yaxis, "Year": "Year"})
            elif chart_type == 'pie':
                pie_data = data.groupby('Year').sum(numeric_only=True).reset_index()
                fig = px.pie(pie_data, names='Year', values='Value', title=f"{title} - {pie_data['Year'].iloc[0]}")
            elif chart_type == 'histogram':
                fig = px.histogram(data, x="Value", nbins=10, labels={"Value": yaxis})
            elif chart_type == 'box':
                fig = px.box(data, x="Year", y="Value", labels={"Value": yaxis, "Year": "Year"})
            elif chart_type == 'funnel':
                funnel_data = data.groupby('Year').sum(numeric_only=True).reset_index()
                fig = px.funnel(funnel_data, x="Value", y="Year", labels={"Value": yaxis, "Year": "Year"})
            else:
                fig = px.line(data, x="Year", y="Value", markers=True, labels={"Value": yaxis, "Year": "Year"})

            st.plotly_chart(fig, use_container_width=True)
