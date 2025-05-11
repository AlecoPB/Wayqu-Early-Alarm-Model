"""
Final merge to obtain pre-processed data
"""
import pandas as pd

# Load the CSV files into DataFrames
temperature_df = pd.read_csv('OneDrive\Escritorio\Machine_Learning\LockIn\Wayqu\processed_data/processed_temperatures.csv')
wind_df = pd.read_csv('OneDrive\Escritorio\Machine_Learning\LockIn\Wayqu\processed_data/processed_winds.csv')

# Print the columns of each DataFrame for debugging
print("Temperature DataFrame columns:", temperature_df.columns.tolist())
print("Wind DataFrame columns:", wind_df.columns.tolist())

# Check for duplicates in temperature_df and wind_df
temperature_df = temperature_df.drop_duplicates(subset=['code_commune', 'datetime'])
wind_df = wind_df.drop_duplicates(subset=['code_commune', 'datetime'])

# Merge the DataFrames on both 'code_commune' and 'datetime', avoiding column name conflicts
merged_df = pd.merge(
    temperature_df, wind_df, 
    on=['code_commune', 'datetime'], 
    how='inner', 
    suffixes=('_temp', '_wind')
)

# Print the columns of the merged DataFrame
print("Merged DataFrame columns:", merged_df.columns.tolist())

# Select the required columns and create a copy
final_df = merged_df[
    [
        'code_commune', 
        'rain_24_temp', 
        'average_celsius_temp', 
        'average_wind_wind', 
        'datetime', 
        'num_risque_jo_temp', 
        'lib_risque_jo_temp', 
        'duration_days_temp'
    ]
].copy()  # Explicitly create a copy to avoid the warning

# Rename the columns for consistency
final_df.rename(
    columns={
        'rain_24_temp': 'rain_24',
        'average_celsius_temp': 'average_celsius',
        'average_wind_wind': 'average_wind',
        'num_risque_jo_temp': 'num_risque_jo',
        'lib_risque_jo_temp': 'lib_risque_jo',
        'duration_days_temp': 'duration_days',
    },
    inplace=True
)

# Final formatting
final_df.drop(columns=['lib_risque_jo'], inplace=True)
final_df.rename(columns={'num_risque_jo': 'risk_level'}, inplace=True)

# Remove any duplicates that may have been created during the merge
final_df = final_df.drop_duplicates()

# Sort and drop NaN values
final_df['code_commune'] = final_df['code_commune'].astype(str).str[:-3].astype(int)
final_df = final_df.sort_values(by=['code_commune', 'datetime'], ascending=[True, True])
final_df = final_df.dropna()

# Save the final DataFrame to a new CSV file
final_df.to_csv('OneDrive\Escritorio\Machine_Learning\LockIn\Wayqu\processed_data/final_data.csv', index=False)

print("Final data has been saved to 'processed_data/final_data.csv'.")