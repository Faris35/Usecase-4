# Import all relevant libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import zscore
from ydata_profiling import ProfileReport
from ipyvizzu import Chart, Data, Config, Style
import altair as alt

# Title of the app
st.title('Navigating the Car Market: Where to Sell Your Vehicle in Saudi Arabia')

st.write('Do you want to sell your old car and buy a new one? Avoid the hassles of selling with the Sayara platform. Sayara saves you time and effort by inspecting and evaluating your car, offering you a competitiveprice—all from the comfort of your home.') 

# Read the data from CSV files
df = pd.read_excel('df_non_negotiable.xlsx')

# Prepare the data for the chart
region_price_df = df[['Price', 'Region']].head(20)

# Questions to answer:

#Q1 Most used car buying areas
st.header('Syarah Sales Spotlight: Which Cities Are Leading the Used Car Market in Saudi Arabia?')
st.write("Saudi Arabia's used car market has been growing rapidly. If you're planning to sell a car, targeting cities with the highest purchasing power can increase your chances of a quick sale.")
most_used_car_areas = df['Region'].value_counts().head(10)
st.write("Most used car buying areas:")
st.bar_chart(most_used_car_areas)
st.write("Using a sample of over 3,000 sold used cars, the data shows that purchasing power is strongest in the largest cities.")

#Q2 Best selling brands by region
best_selling_brands_by_region = df.groupby('Region')['Make'].value_counts().groupby(level=0).nlargest(1).reset_index(level=0, drop=True).reset_index()

# Display the best-selling brands by region
st.header("Best selling brands by region:")

# Create a horizontal bar chart for regions and their best-selling brands
chart = alt.Chart(best_selling_brands_by_region).mark_bar().encode(
    y=alt.Y('Region:N', sort=None),  # Region on y-axis
    x=alt.X('Make:N', aggregate='count'),  # Count of best-selling brand on x-axis
    color='Make:N',  # Color by brand (Make)
    tooltip=['Region', 'Make']  # Tooltip to display Region and Make
).properties(
    title="Best-Selling Brands by Region",
)

# Display the chart
st.altair_chart(chart)


#Q3 Pricing used cars according to the most influential factors

# Create dropdowns for the user to select the make and year of their car
make_selected = st.selectbox('Select the Make:', df['Make'].unique())

# Filter the DataFrame to get the available years for the selected make
available_years = df[df['Make'] == make_selected]['Year'].unique()
year_selected = st.selectbox('Select the Year:', available_years)

# Filter the DataFrame based on the selected make and year to get the available mileage options
filtered_mileage_df = df[(df['Make'] == make_selected) & 
                         (df['Year'] == year_selected)]

# Update the mileage slider to show only the available mileage range for the selected make and year
if not filtered_mileage_df.empty:
    available_mileage = filtered_mileage_df['Mileage'].unique()
    mileage_selected = st.selectbox('Select the Mileage:', available_mileage)
else:
    st.write("No data available for the selected Make and Year.")

# Filter the DataFrame based on the selected make, year, and mileage
filtered_df = df[(df['Make'] == make_selected) & 
                 (df['Year'] == year_selected) & 
                 (df['Mileage'] == mileage_selected)]

# Show the price range for the selected criteria
st.write(f"The estimated price is: {filtered_df['Price'].mean()}")