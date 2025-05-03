import streamlit as st
import pandas as pd

# Load data and convert to date
rain_data = pd.read_csv('../data-prep/clean-data/rain-data-processed.csv')
rain_data['Date'] = pd.to_datetime(rain_data['Date']).dt.date

#st.logo(image, *, size="medium", link=None, icon_image=None)
st.set_page_config(
    page_title="The Daily Drip",
    page_icon="☔️",
    layout="wide",
)

st.markdown("<h1 style='text-align: center;'>The Daily Drip ☔️</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.markdown("<h3 style='text-align: center;'>Charts 📈</h3>", unsafe_allow_html=True)

#Controls
col3.markdown("<h3 style='text-align: center;'>Controls 🎮</h3>", unsafe_allow_html=True)

# Location selection
col3.write("##### Location")
location = col3.selectbox("Select a location:", options='Belém', index=0)

# Date range selection
col3.write("##### Date Range Selection")
start_date = col3.date_input("From:", value='2025-01-01', min_value=rain_data['Date'].min(), max_value=rain_data['Date'].max())
end_date = col3.date_input("To:", value=rain_data['Date'].max(), min_value=rain_data['Date'].min(), max_value=rain_data['Date'].max())

# Validate interval
if start_date > end_date:
    st.error("Start date must be before end date.")
else:
    # Filter data
    mask = (rain_data['Date'] >= start_date) & (rain_data['Date'] <= end_date)
    filtered_data = rain_data.loc[mask]
    
    # Display chart
    chart_data = filtered_data.copy()
    chart_data['Date'] = chart_data['Date'].astype(str) 
    col1.bar_chart(chart_data.set_index('Date')['Precipitation (mm)'], color='#921581',height=396)


    # Clean display of table
    with col1.expander("Show data"):
        st.dataframe(filtered_data.reset_index(drop=True))

col2.markdown("<h3 style='text-align: center;'>Stats #️⃣</h3>", unsafe_allow_html=True)
# Display total rainfall
total_rainfall = filtered_data['Precipitation (mm)'].sum()
col2.metric(label="Total Rainfall", value=f"{total_rainfall:.2f} mm", border=True)
# Display average rainfall
average_rainfall = filtered_data['Precipitation (mm)'].mean()
col2.metric(label="Average Rainfall", value=f"{average_rainfall:.2f} mm",border=True)
# Display maximum rainfall
max_rainfall = filtered_data['Precipitation (mm)'].max()
col2.metric(label="Maximum Rainfall in a Single Day", value=f"{max_rainfall:.2f} mm",border=True)
# Total days in range
total_days = (end_date - start_date).days + 1
# Count of rainy days
rainy_days = filtered_data[filtered_data['Precipitation (mm)'] > 0].shape[0]
# Display as a combined message
col2.metric(label="Rain Frequency", value=f"{rainy_days} out of {total_days} days",  help="Number of days with rain vs total selected days", border=True)