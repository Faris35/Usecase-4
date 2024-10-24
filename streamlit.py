# Import all relevant libraries
import streamlit as st
import pandas as pd
import altair as alt

# Title of the app
st.title('Navigating the Car Market: Where to Sell Your Vehicle in Saudi Arabia')

st.write('Do you want to sell your old car and buy a new one? Avoid the hassles of selling with the Sayara platform. Sayara saves you time and effort by inspecting and evaluating your car, offering you a competitive price—all from the comfort of your home.') 

# Read the data from CSV files
df = pd.read_csv('df_non_negotiable.csv')

# Prepare the data for the chart
region_price_df = df[['Price', 'Region']].head(20)

# Questions to answer:

#Q1 Most used car buying areas
st.header('Syarah Sales Spotlight: Which Cities Are Leading the Used Car Market in Saudi Arabia?')
st.write("Saudi Arabia's used car market has been growing rapidly. If you're planning to sell a car, targeting cities with the highest purchasing power can increase your chances of a quick sale.")
most_used_car_areas = df['Region'].value_counts().head(10)
st.write("Exploring saudi demand for used cars:")
st.bar_chart(most_used_car_areas)
st.write("Using a sample of over 3,000 sold used cars, the data shows that purchasing power is strongest in the largest cities.")
st.write("That leads us to a new question: what are the best-selling brands?")
#Q2 Best selling brands by region
best_selling_brands_by_region = df.groupby('Region')['Make'].value_counts().groupby(level=0).nlargest(1).reset_index(level=0, drop=True).reset_index()

# Display the best-selling brands by region
st.header("Best selling brands by region")
st.write("Lest’s dive deeper into the Saudi market, we need to show the preferred brands:")

# Create a horizontal bar chart for regions and their best-selling brands
chart = alt.Chart(best_selling_brands_by_region).mark_bar().encode(
    y=alt.Y('Region:N', sort=None),  # Region on y-axis
    x=alt.X('Make:N', aggregate='count'),  # Count of best-selling brand on x-axis
    color='Make:N',  # Color by brand (Make)
    tooltip=['Region', 'Make']  # Tooltip to display Region and Make
).properties(
    # title="Best-Selling Brands by Region",
)

# Display the chart
st.altair_chart(chart)
st.write("This graphic reflects the right brand for each region and it can be noted that Toyota is the most common in most of Saudi regions.")

#Q3 Pricing used cars according to the most influential factors
# Create dropdowns for the user to select the make, type, and year of their car
st.header('Unlock Your Car’s Value: Instant Estimates on Sayara!')
st.write("Enter your car's information to get an instant price estimate and see where you stand in the market!")
make_selected = st.selectbox('Select the Make:', df['Make'].unique())

# Filter the DataFrame to get the available types for the selected make
available_types = df[df['Make'] == make_selected]['Type'].unique()
type_selected = st.selectbox('Select the Type:', available_types)

# Filter the DataFrame to get the available years for the selected make and type
available_years = df[(df['Make'] == make_selected) & 
                     (df['Type'] == type_selected)]['Year'].unique()
year_selected = st.selectbox('Select the Year:', available_years)

# Filter the DataFrame based on the selected make, type, and year to get the available mileage options
filtered_mileage_df = df[(df['Make'] == make_selected) & 
                         (df['Type'] == type_selected) & 
                         (df['Year'] == year_selected)]

# Update the mileage slider to show only the available mileage range for the selected make, type, and year
if not filtered_mileage_df.empty:
    available_mileage = filtered_mileage_df['Mileage'].unique()
    mileage_selected = st.selectbox('Select the Mileage:', available_mileage)
else:
    st.write("No data available for the selected Make, Type, and Year.")

# Filter the DataFrame based on the selected make, type, year, and mileage
filtered_df = df[(df['Make'] == make_selected) & 
                 (df['Type'] == type_selected) & 
                 (df['Year'] == year_selected) & 
                 (df['Mileage'] == mileage_selected)]

# Show the price range for the selected criteria
st.write(f"The estimated price is: {filtered_df['Price'].mean()}")

st.header('With Syyarh, selling your car has become more reliable, better and faster.')