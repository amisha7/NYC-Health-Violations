#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 22:08:26 2023

Name: Amisha Patel

@author: patel
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


# Read data from csv file
df = pd.read_csv("https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?date=20231111&accessType=DOWNLOAD") 

# Filter to only Indian cuisine
indian_df = df[df["CUISINE DESCRIPTION"] == "Indian"]


'''
-----------------  1. Analyze the closures in your cuisine category  -----------------------
'''

# Get closed indian restaurant and count them
closed_indian = indian_df[indian_df['ACTION'].str.contains('Closed ', case=False)]

# # Get the most common violation code
top_violation = closed_indian["VIOLATION CODE"].mode()[0]

print("\n1]. Analyze the closures in your cuisine category:")
print("\t A. Number of closed Indian cuisine restaurants:", len(closed_indian))
print("\t B. Most common violation code for closed Indian cuisine restaurants:", top_violation)


'''
-----------------  2. Analyze the violations that relate to mice and cockroaches -----------------------
'''

# Search violation description for 'mice'
mice_violations = indian_df[indian_df['VIOLATION DESCRIPTION'].str.contains('mice', case=False, na=False)]
num_mice = len(mice_violations)

# Search violation description for 'roach' 
roach_violations = indian_df[indian_df['VIOLATION DESCRIPTION'].str.contains('roach', case=False, na=False)]
num_roach = len(roach_violations)

# Calculate ratio
ratio_dec = num_mice / num_roach
ratio_int = num_mice // num_roach

print("\n2]. Analyze the violations that relate to mice and cockroaches:")
print("\t A. Number of mice violations: ", num_mice) 
print("\t B. Number of roach violations: ", num_roach)
print(f"\t C. There were {ratio_dec:.2f} mice per roach or {ratio_int} mice per roach.")


'''
-----------------  3. Analyze the frequent violaters  -----------------------
'''

# Filtering for your cuisine and counting violations by borough
violations_by_borough = indian_df["BORO"].value_counts()

# Getting the borough with the most violations
most_violations_borough = violations_by_borough.idxmax()

# Filtering for your cuisine and finding the restaurant with the most violations
restaurant_with_most_violations = indian_df.groupby("CAMIS").size().idxmax()

# Extracting information about the restaurant with the most violations
restaurant_info = indian_df[indian_df["CAMIS"] == restaurant_with_most_violations].iloc[0]

# Checking how many times the restaurant closed 
closed_count = len(indian_df[(indian_df["CAMIS"] == restaurant_with_most_violations) & indian_df['ACTION'].str.contains('Closed', case=False)])

# Checking how many times the restaurant reopen 
reopened_count = len(indian_df[(indian_df["CAMIS"] == restaurant_with_most_violations) & indian_df['ACTION'].str.contains('Re-opened', case=False)])


print("\n3]. Analyze the frequent violaters:")
print("\t A. Borough with the most violations for Indian cuisine:", most_violations_borough)
print("\t B. Restaurant with the most violations:")
print("\t\tName:", restaurant_info["DBA"])
print("\t\tAddress:", restaurant_info["BUILDING"], restaurant_info["STREET"], ",", restaurant_info["BORO"], ",", int(restaurant_info["ZIPCODE"]))
print("\t\tBorough:", restaurant_info["BORO"])
print("\t C. Number of times the restaurant closed:", closed_count, "and re-opended:",reopened_count)


'''
-----------------------   Extra Point  --------------------------
'''

print("\n4]. Extra Credit - Plots")

# Filtering for 'rat' violations in the "Indian" cuisine category
rat_violations = indian_df[indian_df["VIOLATION DESCRIPTION"].str.contains('rats', case=False, na=False)]

# Counting 'rat' violations by borough
rat_violations_by_borough = rat_violations["BORO"].value_counts()

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(rat_violations_by_borough, labels=rat_violations_by_borough.index, autopct='%1.1f%%', startangle=140)
plt.title('Rat Violations by Borough in Indian Cuisine')
plt.show()



# Load the NYC map data (shapefile)
nyc_map = gpd.read_file("https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile")

# Clean Data 
indian_df_cleaned = indian_df.query('(Latitude != 0) & (Longitude != 0)').dropna(subset=['Latitude', 'Longitude'])

# Assuming 'Latitude' and 'Longitude' are columns in your dataset and make geometry from longitude and latitude
geometry = [Point(xy) for xy in zip(indian_df_cleaned['Longitude'], indian_df_cleaned['Latitude'])]
indian_geo_df = gpd.GeoDataFrame(indian_df_cleaned, geometry=geometry)

# Create a plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the NYC map
nyc_map.plot(ax=ax, color='lightgrey', edgecolor='black')

# Plot the violations for Indian cuisine on top of the map
indian_geo_df.plot(ax=ax, color='red', alpha=0.5, legend=True)

# Customize the plot
plt.title('Violations for Indian Cuisine in NYC')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

