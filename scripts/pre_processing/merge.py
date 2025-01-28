import os
import pandas as pd
import pd_tools as pdt

# Directory containing processed files
processed_data_dir = 'processed_data/processed_departments'

# Initialize an empty list to store DataFrames
dataframes = []

# Iterate through all files in the directory
for file in os.listdir(processed_data_dir):
    if file.startswith('processed_dep_') and file.endswith('.csv'):  # Match processed department files
        filepath = os.path.join(processed_data_dir, file)
        print(f"Loading {filepath}")
        df = pdt.from_file(filepath, ';')
        df.columns = df.columns.str.strip().str.lower()  # Standardize column names
        dataframes.append(df)

# Combine all DataFrames into one
if dataframes:  # Ensure there's at least one file
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Optional: Merge with processed_catnat if required
    processed_catnat = pdt.from_file(os.path.join('processed_data/processed_catnat.csv'), ';')
    processed_catnat.columns = processed_catnat.columns.str.strip().str.lower()

    # Perform an inner merge on 'code_commune' and 'datetime'
    final_merged_data = combined_df.merge(processed_catnat, on=['code_commune', 'datetime'], how='inner')

    # Save the final result
    final_merged_data.to_csv(os.path.join('processed_data/processed_result.csv'), index=False, sep=';')
    print("Final merged data saved to processed_data/processed_result.csv")
else:
    print("No processed department files found to merge.")
