#GIS 4085 Homework 6 Population Census
import arcpy 
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import numpy as np
arcpy.env.overwriteOutput = True
gdb_path = arcpy.env.workspace = r'C:\GIS_4085_Python_Programming_II\Week_6\Week6_Data\Week6_Data\GIS4085_Week6.gdb'
arcpy.env.workspace = gdb_path
pop_csv = r'C:\GIS_4085_Python_Programming_II\Week_6\Week6_HWdata\Census2020_P1\P12020.csv'

pop_all_df = pd.read.csv('C:\GIS_4085_Python_Programming_II\Week_6\Week6_HWdata\Census2020_P1\DECENNIALPL2020.P1-Data.csv')

#remove rows 2 and 3 in csv
pop_df = pop_all_df.drop(index = [0,1])

#Create new field called GEOID so you can perform a join
pop_df['GEOID'] = pop_df['GEO_ID'].str[-4:]

pop_df['POPALL'] = pop_df['P1_001N'].astype('long')

print(pop_df['POPALL'].dtype)
print(pop_df)

#Export to new csv
pop_df.to_csv('C:\GIS_4085_Python_Programming_II\Week_6\Week6_HWdata\Census2020_P1\P12020.csv')

#Use describe to get summary stats of population column
print(pop_df['POPALL'].describe())
print('min val: ' + str(pop_df['POPALL'].min()))
print('max val: ' + str(pop_df['POPALL'].max()))

#Query for counties with pop > 500,000
pop500kdf = pop_df.query('POPALL >= 500000')
print(pop500kdf)

#Top 5 counties by population
top5sort_df = pop500kdf.sort_values(by=['POPALL'])
top5pop_df = top5sort_df.nlargest(5, 'POPALL')
print(top5pop_df)

fig, ax = plt.subplots()
bar_container = ax.bar(top5pop_df['NAME'], top5pop_df['POPALL'])
ax.set(xlabel = "County", ylabel = "Population", title = "Top 5 Colorado Counties by Population")
ax.bar_label(bar_container, fmt='{:,.0f}')
plt.show()

# #join P1 .csv to County fc
try:
    ctyPop = arcpy.management.AddJoin('County', 'GEOID_lng', pop_csv, 'GEOID')
    arcpy.management.CopyFeatures(ctyPop, 'CountyPop')
except arcpy.ExecuteError as e:
    print(e)

pop_gdf = geopandas.read.file(gdb_path, layer='CountyPop')
print(pop_gdf)
