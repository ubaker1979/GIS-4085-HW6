# GIS-4085-HW6
Week 6 Homework Assignment

1. The first task will be to explore and update hurricane data using geopandas and arcpy.  You might find it easier to work in the Python window of ArcGIS Pro than an IDE as the code can take a few minutes to run. If you receive error messages around 'activate' and 'conda' in your IDE, you can disregard these. If you use Pro, remember to activate your gis4085 environment. Write a script that performs the following steps:
create a geodataframe from the hurricane feature class
select for wind speeds >= 130  and <= 156 - this is the range for Category 4 hurricanes, and the year 2000
use the .describe() method on the wind speed column to print summary statistics 
use the .columns property to print the attribute names 
export the selection to a shapefile - gdf.to_file()
use arcpy to add a field: "CAT", data type SHORT and calculate the value of the field to 4, export to a new feature class, cat4_2000
2. The second task will use Census data, starting with the raw data you would download. The data require pre-processing to join the tabular data to spatial data (blocks, block groups, tracts, counties, states). Typically, I perform these steps in a mix of Excel and Pro. This task will use pandas to perform the pre-processing steps to create an unique ID for the join and convert the population data to a numeric data type.
