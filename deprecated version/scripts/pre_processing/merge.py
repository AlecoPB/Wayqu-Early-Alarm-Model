import os
import pandas as pd
import pd_tools as pdt

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

# Directory containing filtered departments
processed_data_dir = f'{_PATH_}optimized_data/departments'

# Initialize an empty list to store DataFrames
dataframes = []

# Iterate through all files in the directory
for file in os.listdir(processed_data_dir):
    if file.startswith('processed_dep_') and file.endswith('.csv'):  # Match processed department files
        filepath = os.path.join(processed_data_dir, file)
        print(f"Loading {filepath}")
        df = pdt.from_file(filepath, ';')
        df.columns = df.columns.str.strip().str.lower()  # Standardize column names
        
        # Convert 5-digit commune codes to 2-digit department codes
        df['code_dept'] = df['code_commune'].astype(str).str[:2].str.zfill(2)
        dataframes.append(df)

# Combine all DataFrames into one
if dataframes:  # Ensure there's at least one file
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Load and process catnat data
    processed_catnat = pdt.from_file(os.path.join(f'{_PATH_}optimized_data/data/processed_catnat.csv'), ';')
    processed_catnat.columns = processed_catnat.columns.str.strip().str.lower()
    
    # Convert catnat commune codes to 2-digit department codes
    processed_catnat['code_dept'] = processed_catnat['code_commune'].astype(str).str[:2].str.zfill(2)
    
    # Verify datetime format in both datasets
    combined_df['datetime'] = pd.to_datetime(combined_df['datetime'])
    processed_catnat['datetime'] = pd.to_datetime(processed_catnat['datetime'])
    
    print("\nPre-merge counts:")
    print(f"Weather data: {len(combined_df)} rows")
    print(f"Catnat data: {len(processed_catnat)} rows")

    # Perform an inner merge on department code and datetime
    final_merged_data = combined_df.merge(
        processed_catnat,
        on=['code_dept', 'datetime'],
        how='left'
    )
    
    print("\nPost-merge counts:")
    print(f"Merged data: {len(final_merged_data)} rows")
    print(f"Merge efficiency: {len(final_merged_data)/min(len(combined_df), len(processed_catnat)):.1%}")

    # Save the final result
    output_path = os.path.join(f'{_PATH_}optimized_data/data/catnat_meteo_merged.csv')
    final_merged_data.to_csv(output_path, index=False, sep=';')
    print(f"\nFinal merged data saved to {output_path}")
    
    # Optional: Show sample of merged data
    print("\nSample of merged data:")
    print(final_merged_data[['code_dept', 'datetime', 'rr', 'lib_risque_jo']].head())
else:
    print("No processed department files found to merge.")