import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Science & Technology Dashboard 🇱🇰", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("science_and_tech_sl.csv")
    return df

df = load_data()

# Apply custom font style and theme globally using HTML
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fb;
            color: #333;
        }
        h1, h2, h3, h4 {
            font-family: 'Roboto', sans-serif;
            color: #2c3e50;
        }
        .italic {
            font-style: italic;
        }
        .stMetricValue {
            font-family: 'Roboto', sans-serif;
            font-size: 1.2em;
            color: #34495e;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #16a085;
        }
        .stRadio>div>label,
        .stSelectbox>div>label,
        .stTextInput>label {
            font-family: 'Arial', sans-serif;
            color: #34495e;
        }
        .stSidebar .sidebar-content {
            background-color: #ecf0f1;
        }
        .stDataFrame {
            background-color: #ffffff;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            border-radius: 5px;
        }
        .stPlotlyChart {
            margin-bottom: 20px;
        }
        .stMarkdown {
            font-family: 'Arial', sans-serif;
            color: #34495e;
        }
        /* Hover effect for sidebar items */
        .stSidebarMenu li:hover {
            background-color: #1abc9c;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
selected_indicators = st.sidebar.multiselect("Select Indicators", sorted(df["Indicator.Name"].unique()))

# Apply filters
filtered_df = df[df["Indicator.Name"].isin(selected_indicators)]

# Title
st.title("📊 Sri Lankan Science & Technology Indicators Dashboard")
st.markdown("<p class='italic'>Explore key science and technological indicators in Sri Lanka.</p>", unsafe_allow_html=True)

# Display selected filters
if selected_indicators:
    st.markdown("### Selected Indicators:")
    for indicator in selected_indicators:
        st.markdown(f"- {indicator}")

# Display KPIs
st.markdown("### Key Performance Indicators (KPIs)")
kpi_col1, kpi_col2 = st.columns(2)

for indicator in selected_indicators:
    indicator_data = filtered_df[filtered_df["Indicator.Name"] == indicator]
    
    # Calculate the most recent value and percentage change
    latest_value = indicator_data.iloc[-1]["Value"]
    first_value = indicator_data.iloc[0]["Value"]
    percentage_change = ((latest_value - first_value) / first_value) * 100 if first_value != 0 else 0
    
    kpi_col1.metric(f"{indicator} (Latest)", f"{latest_value:,.2f}")
    kpi_col2.metric(f"{indicator} (Change)", f"{percentage_change:,.2f}%")

# Plotting the selected indicators (Three chart types)
st.markdown("### Indicator Visualizations")

for indicator in selected_indicators:
    indicator_data = filtered_df[filtered_df["Indicator.Name"] == indicator]
    
    # Line Chart
    line_fig = px.line(indicator_data, x='Year', y='Value', title=f"{indicator} Over Time (Line Chart)", markers=True)
    st.plotly_chart(line_fig, use_container_width=True)
    
    # Bar Chart
    bar_fig = px.bar(indicator_data, x='Year', y='Value', title=f"{indicator} Over Time (Bar Chart)")
    st.plotly_chart(bar_fig, use_container_width=True)
    
    # Scatter Plot
    scatter_fig = px.scatter(indicator_data, x='Year', y='Value', title=f"{indicator} Over Time (Scatter Plot)", trendline="ols")
    st.plotly_chart(scatter_fig, use_container_width=True)

# Additional information for each indicator
st.subheader("📊 Indicator Breakdown")

# Generate a dictionary with unique indicator names and their descriptions
indicator_info = {}

# List of unique indicator names from the dataset
unique_indicators = df["Indicator.Name"].unique()

# Iterate through the unique indicators and dynamically generate descriptions
for indicator in unique_indicators:
    if indicator == "Trade in services (% of GDP)":
        indicator_info[indicator] = "Shows the proportion of GDP derived from trade in services."
    elif indicator == "Insurance and financial services (% of service imports, BoP)":
        indicator_info[indicator] = "Percentage of service imports for insurance and financial services."
    elif indicator == "Ease of doing business score":
        indicator_info[indicator] = "Global ranking for ease of doing business (0 = lowest, 100 = highest)."
    elif indicator == "Cost to export, border compliance (US$)":
        indicator_info[indicator] = "The cost of complying with border export regulations in US dollars."
    elif indicator == "Time required to start a business (days)":
        indicator_info[indicator] = "Average number of days required to start a business."
    else:
        indicator_info[indicator] = "Data description not available for this indicator."

# Display descriptions for each selected indicator
for indicator in selected_indicators:
    st.markdown(f"**{indicator}**: {indicator_info.get(indicator, 'Data description not available for this indicator.')}")

# Data Table with Sorting
st.subheader("📋 Data Overview")
sort_column = st.selectbox("Sort by Column", filtered_df.columns, index=0)
ascending = st.radio("Sort Order", ['Ascending', 'Descending']) == 'Ascending'
st.dataframe(filtered_df.sort_values(by=sort_column, ascending=ascending), use_container_width=True)

# Footer
st.markdown("---")
st.caption("📌 Data Source: science_and_tech_sl.csv | Created with ❤️ using Streamlit")


import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv(r"C:\Users\shazneen\Desktop\University\Degree\Year 02\Semester - 02\Data Science Proj. Lifecycle\ICW\science_and_tech_sl.csv")  # Path should be updated to match the location

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
