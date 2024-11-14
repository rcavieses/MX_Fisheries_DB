import os
import pandas as pd

# Set the directory where the files are located
directory = 'data/vessel_monitor_system'

# Create an empty list to store the DataFrames
dfs = []

# Loop through the files and read them into DataFrames
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        dfs.append(df)

# Concatenate the DataFrames into a single DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Save the merged DataFrame to a new file
merged_df.to_csv('vms_2018_2023.csv', index=False)