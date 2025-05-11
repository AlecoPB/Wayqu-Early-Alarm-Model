"""
Final touches to processed_result
"""
import pd_tools as pdt

processed_result = pdt.from_file('processed_data/processed_result.csv', ';')

# Renaming columns
processed_result = processed_result.rename(columns={'rr': 'rain_24',
                                                    'tntxm': 'average_celsius',
                                                    'ffm': 'average_wind'})

# Sort the DataFrame by 'datetime' and assign back to the DataFrame
processed_result = processed_result.sort_values(by=['code_commune', 'datetime'], ascending=[True, True])

# Save as CSV
processed_result.to_csv('processed_data/middle_data.csv', sep=';', index=False)

print('Done, saved to middle_data.csv')