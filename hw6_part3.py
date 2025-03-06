#IMF, UN, World Bank reported numbers streamlit app

#load packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import streamlit as st
from IPython.display import IFrame

#load website content and parse page
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'  # Example URL
page = requests.get(url)
bs4page = BeautifulSoup(page.text, 'lxml')

#find table, read into pd df
table = bs4page.find('table', {'class': 'wikitable'})
GDP = pd.read_html(str(table))[0]

#check columns, need flattening? 
print("Columns in the DataFrame:")
print(GDP.columns)
GDP.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in GDP.columns]
print("Flattened columns in the DataFrame:")
print(GDP.columns)

# identify column names for renaming
print("Columns in the DataFrame before renaming:")
print(GDP.columns)
GDP = GDP.rename(columns={
    'Country/Territory': 'Country',
    'IMF[1][12] Forecast': 'GDP (IMF$Forecast)'
})

# Inspect the columns of the DataFrame after renaming
print("Columns in the DataFrame after renaming:")
print(GDP.columns)

# Replace non-numeric values with NaN and then drop them
GDP['GDP (IMF$Forecast)'] = GDP['GDP (IMF$Forecast)'].replace('—', pd.NA)
GDP['GDP (UN$Estimate)'] = GDP['GDP (UN$Estimate)'].replace('—', pd.NA)
GDP['GDP (WorldBank$Estimate)'] = GDP['GDP (WorldBank$Estimate)'].replace('—', pd.NA)
GDP = GDP.dropna(subset=['GDP (IMF$Forecast)'])

# Convert GDP column to float
GDP['GDP (IMF$Forecast)'] = GDP['GDP (IMF$Forecast)'].astype(str).str.replace(',', '').astype(float)
GDP['GDP (UN$Estimate)'] = GDP['GDP (UN$Estimate)'].astype(str).str.replace(',', '').astype(float)
GDP['GDP (WorldBank$Estimate)'] = GDP['GDP (WorldBank$Estimate)'].astype(str).str.replace(',', '').astype(float)

#load wikipedia page for countries list (missing from updated IMF table page)
url2 = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_the_United_Nations_geoscheme"
page2 = requests.get(url2)
bs4page2 = BeautifulSoup(page2.text, 'lxml')
table = bs4page2.find('table', {'class': 'wikitable'})
UNregion = pd.read_html(str(table))[0]

#check columns and rename
print("columns in dataframe:")
print(UNregion.columns)
UNregion = UNregion.rename(columns={
    'Country or Area': 'Country',
    'Geographical subregion': 'Region'
})
print("columns in dataframe:")
print(UNregion.columns)

# Merge GDP and UNregion dataframes on the 'Country' column
merged_df = pd.merge(GDP, UNregion, on='Country')

# Streamlit app
st.title("GDP by Country and Region")

# Dropdown menu for selecting data source
data_source = st.selectbox("Select data source:", ["IMF Forecast", "UN Estimate", "World Bank Estimate"])

# Map data source to column name
data_source_map = {
    "IMF Forecast": "GDP (IMF$Forecast)",
    "UN Estimate": "GDP (UN$Estimate)",
    "World Bank Estimate": "GDP (WorldBank$Estimate)"
}
selected_column = data_source_map[data_source]

# Create an interactive stacked bar plot grouped by region
fig = px.bar(merged_df, x='Region', y=selected_column, color='Country', title=f'GDP by Country and Region ({data_source})', barmode='stack')

# Display the plot in the Streamlit app
st.plotly_chart(fig)