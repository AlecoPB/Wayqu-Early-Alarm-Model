"""
File to understand better some files
"""
import pandas as pd
import pd_tools as pdt

# Code to extract unique communes
'''
aid_catnat = pdt.from_file("modified_catnat.csv", ';')

unique_communes = aid_catnat['cod_commune'].unique()

unique_communes_df = pd.DataFrame(unique_communes, columns=['unique_communes'])

# Sort the DataFrame by commune
unique_communes_df.sort_values(by='unique_communes', ascending=True, inplace=True)

# Convert to string and pad with zeros to ensure 5-digit formatting
unique_communes_df['unique_communes'] = \
    unique_communes_df['unique_communes'].astype(int).astype(str).str.zfill(5)

# Save as csv
unique_communes_df.to_csv('unique_communes.csv', sep=';', index=False)

'''
# Code to extract average temperatures per commune
pdt.extract_temperatures('raw data/temperature-quotidienne-departementale.csv')
avg_temperatures = pdt.from_file('processed_data/average_temperatures.csv', ';').copy()
processed_result = pdt.from_file('processed_data/middle_data.csv', ';').copy()

# Convert 'datetime' to datetime format and extract day and month
avg_temperatures['datetime'] = pd.to_datetime(avg_temperatures['datetime'])
processed_result['datetime'] = pd.to_datetime(processed_result['datetime'])

# Create new columns for day and month
avg_temperatures['day_month'] = avg_temperatures['datetime'].dt.strftime('%m-%d')
processed_result['day_month'] = processed_result['datetime'].dt.strftime('%m-%d')

# Ensure the 'code_commune' in processed_result is in the correct format (first two digits)
processed_result['code_commune_short'] = processed_result['code_commune'].astype(str).str[:2]

# Create a new DataFrame with the relevant columns from avg_temperatures
avg_temperatures['code_commune_short'] = avg_temperatures['code_commune'].astype(str)

# Merge the DataFrames on the short code_commune and day_month
merged_df = pd.merge(processed_result, avg_temperatures[['code_commune_short', 'day_month', 'average_celsius']],
                     left_on=['code_commune_short', 'day_month'],
                     right_on=['code_commune_short', 'day_month'],
                     how='left',
                     suffixes=('', '_avg'))

# Fill the empty average_celsius in processed_result with values from avg_temperatures
merged_df['average_celsius'] = merged_df['average_celsius'].combine_first(merged_df['average_celsius_avg'])

# Drop the temporary columns used for merging
merged_df.drop(columns=['code_commune_short', 'day_month', 'average_celsius_avg'], inplace=True)

# Save the updated DataFrame back to CSV or use it as needed
merged_df.to_csv('processed_data/processed_temperatures.csv', index=False)

print("Done")