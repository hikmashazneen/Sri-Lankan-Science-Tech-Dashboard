import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("science_and_tech_sl.csv")

# Convert year to string for dropdown filters
df['Year'] = df['Year'].astype(str)

# Sidebar year filter
selected_years = st.sidebar.multiselect(
    "Select Year(s):", options=sorted(df['Year'].unique()), default=sorted(df['Year'].unique())
)

# Filter dataset based on selected years
filtered_df = df[df['Year'].isin(selected_years)]

# List of unique indicators
indicators = df['Indicator.Name'].unique()

# Main title
st.title("Science & Technology Indicators in Sri Lanka")

# Display Key KPIs at the top (latest year by default)
latest_year = df['Year'].max()
latest_data = df[df['Year'] == latest_year]
st.subheader(f"Key Science & Tech KPIs - {latest_year}")
col1, col2, col3 = st.columns(3)

with col1:
    rd_value = latest_data[latest_data['Indicator.Name'] == 'Research and development expenditure (% of GDP)']['Value'].sum()
    st.metric("R&D Expenditure (% of GDP)", f"{rd_value:.2f}%")

with col2:
    articles = latest_data[latest_data['Indicator.Name'] == 'Scientific and technical journal articles']['Value'].sum()
    st.metric("Sci. Journal Articles", int(articles))

with col3:
    patents = latest_data[latest_data['Indicator.Name'] == 'Patent applications, nonresidents']['Value'].sum()
    st.metric("Nonresident Patents", int(patents))

# Chart generation
for indicator in indicators:
    data = filtered_df[filtered_df['Indicator.Name'] == indicator]

    if data.empty:
        continue

    # Custom chart titles and y-axis labels
    if indicator == 'Research and development expenditure (% of GDP)':
        title = 'R&D Expenditure Over Time'
        yaxis = 'R&D (% of GDP)'
    elif indicator == 'Scientific and technical journal articles':
        title = 'Scientific Journal Articles Over Time'
        yaxis = 'Number of Articles'
    elif indicator == 'Patent applications, nonresidents':
        title = 'Nonresident Patent Applications Over Time'
        yaxis = 'Patent Applications'
    elif indicator == 'Researchers in R&D (per million people)':
        title = 'R&D Researchers Per Million People'
        yaxis = 'Researchers / Million People'
    elif indicator == 'Technicians in R&D (per million people)':
        title = 'R&D Technicians Per Million People'
        yaxis = 'Technicians / Million People'
    elif indicator == 'High-technology exports (% of manufactured exports)':
        title = 'High-Tech Exports (% of Manufactured Exports)'
        yaxis = 'High-Tech Exports (%)'
    elif indicator == 'Charges for the use of intellectual property, payments (BoP, current US$)':
        title = 'IP Usage Payments'
        yaxis = 'Payments (USD)'
    elif indicator == 'Charges for the use of intellectual property, receipts (BoP, current US$)':
        title = 'IP Usage Receipts'
        yaxis = 'Receipts (USD)'
    else:
        title = indicator
        yaxis = 'Value'

    # Plot
    fig = px.line(
        data,
        x="Year",
        y="Value",
        title=title,
        labels={"Value": yaxis, "Year": "Year"},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
