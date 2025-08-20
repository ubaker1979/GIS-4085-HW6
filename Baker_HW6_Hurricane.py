#GIS 4085 Homework 6 Hurricane
import arcpy
import pandas as pd
import geopandas as gpd
import os

arcpy.env.overwriteOutput = True
gdb_path = arcpy.env.workspace = r'C:\GIS_4085_Python_Programming_II\Week_6\Week6_Data\Week6_Data\GIS4085_Week6.gdb'
arcpy.env.workspace = gdb_path

#Step 1: Create geodataframe from hurricane feature class
hurricane_fc = "hurricane"
full_feature_class_path = os.path.join(gdb_path, hurricane_fc)

try:
    print(f"Reading feature class from: {full_feature_class_path}")
    hurricane_gdf = gpd.read_file(full_feature_class_path)
    print("\nSuccessfully created GeoDataFrame.")
except FileNotFoundError:
    print(f"Error: The feature class '{full_feature_class_path}' was not found.")
    print("Please check the 'gdb_path' and 'feature_class_name' variables and try again.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Outputs
output_folder = r"C:\GIS_4085_Python_Programming_II\Week_6\Week6_HWdata"
cat4_select = "cat4_2000_selection.shp"
cat4_200_fc = "cat4_200"

full_output_shp_path = os.path.join(output_folder, cat4_select)
full_output_fc_path = os.path.join(gdb_path, cat4_200_fc)

#Error Handling
try:
    hurricane_gdf = gpd.read_file(full_feature_class_path)
    print("GeoDataFrame created successfully.\n")

    #Step 2: Select for Category 4 hurricanes
    print("Filtering for Category 4 hurricanes (wind speed 130-156)")
    cat4_2000_gdf = hurricane_gdf[
        (hurricane_gdf['USA_WIND'] >= 130) &
        (hurricane_gdf['USA_WIND'] <= 156) &
        (hurricane_gdf['year'] == 2000)
    ]
    print(f"Selection complete. Found {len(cat4_2000_gdf)} features matching the criteria.\n")

#Step 3: Use .describe() on the wind speed column 
    if 'USA_WIND' in cat4_2000_gdf.columns:
        print(cat4_2000_gdf['USA_WIND'].describe().to_string())
    else:
        print("Warning: 'USA_WIND' column not found in the selection.\n")
    print("\n")

#Step 4: Use .columns to print attribute names
    print("Printing attribute names")
    print("Attribute names in the selected GeoDataFrame:")
    print(list(cat4_2000_gdf.columns))
    print("\n")

#Step 5: Export the selection to a shapefile
    print("Step 5: Exporting selection to a shapefile")

    #gdf.to_file() will create the shapefile.
    cat4_2000_gdf.to_file(full_output_shp_path)
    print(f"Selection exported successfully to: {full_output_shp_path}\n")

#Step 6: Use arcpy to add a field and calculate its value
    print("Step 6: Using arcpy to add 'CAT' field and calculate value")

    #Check if the output feature class already exists and delete it if it does.
    if arcpy.Exists(full_output_fc_path):
        print(f"Deleting existing feature class: {full_output_fc_path}")
        arcpy.management.Delete(full_output_fc_path)

    arcpy.management.CopyFeatures(full_output_shp_path, full_output_fc_path)
    print(f"Copied data to new feature class: {full_output_fc_path}")

    arcpy.management.AddField(full_output_fc_path, "CAT", "SHORT")
    print("Added new field 'CAT'.")

    arcpy.management.CalculateField(
        in_table=full_output_fc_path,
        field="CAT",
        expression="4",
        expression_type="PYTHON3"
    )
    print("Calculated 'CAT' field value to 4.")
    print("\nScript completed successfully!")

except FileNotFoundError:
    print("\nError: The specified file paths were not found.")
    print("Please check the 'gdb_path', 'feature_class_name', and 'output_folder' variables.")
except Exception as e:
    print(f"\nAn error occurred during script execution: {e}")
