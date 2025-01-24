"""
Filtering weather data
"""
import pd_tools as pdt

for i in range(1, 92):

    # Format i with leading zeros for single-digit numbers
    filename = f'raw data/Q_{i:02d}_previous-1950-2023_RR-T-Vent.csv'

    # Apply the function to the current file
    pdt.extract_useful_data_from_meteo(filename, i)

    print(f'Processing {filename}')
    
print('done')
