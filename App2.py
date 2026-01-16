import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="UK Heart Health: Level 1", layout="wide")

@st.cache_data
def load_data():
    # Load the CSVs you created from your Level 1 Excel files
    l1 = pd.read_excel("Level_1.xlsx")
    lk = pd.read_excel("lookups.xlsx")
    return pd.merge(l1, lk, on='small_area')

df = load_data()

# 1. Sidebar Filters
st.sidebar.header("Geography Filters")
selected_nation = st.sidebar.selectbox("Select Nation", df['nation'].unique())
councils = df[df['nation'] == selected_nation]['local_authority'].unique()
selected_council = st.sidebar.selectbox("Select Local Authority", councils)

# 2. Filter for the specific council
region_df = df[df['local_authority'] == selected_council]

# 3. Main Dashboard UI
st.title(f" Net Zero Health Benefits: {selected_council}")

# Total benefit is the 'sum' column from your image
total_val = region_df['sum'].sum()
st.metric("Total Cumulative Economic Benefit", f"£{total_val:,.2f}M")

# 4. Prepare data for the Chart (The "Melting" step)
# We list the columns from your screenshot that are health benefits
benefit_columns = [
    'air_quality', 'congestion', 'dampness', 'diet_change', 
    'excess_cold', 'excess_heat', 'hassle_costs', 'noise', 
    'physical_activity', 'road_repairs', 'road_safety'
]

# Transform columns into a 'co_benefit_type' format for the chart
chart_data = region_df.melt(
    value_vars=benefit_columns, 
    var_name='co-benefit_type', 
    value_name='Benefit_Value'
)

# 5. Create the Visualization
fig = px.bar(
    chart_data, 
    x='co-benefit_type', 
    y='Benefit_Value',
    color='co-benefit_type',
    title=f"Health Pathway Breakdown for {selected_council}",
    labels={'Benefit_Value': 'Value (£ Million)', 'co-benefit_type': 'Pathway'}
)

st.plotly_chart(fig, use_container_width=True)
