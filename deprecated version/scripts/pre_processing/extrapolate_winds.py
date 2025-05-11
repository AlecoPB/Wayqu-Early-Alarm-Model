"""
Extrapolate wind speeds to regions
"""
import pd_tools as pdt
import pandas as pd

# Define wind speeds
wind_data = {
    "paris": {"01": 11.5, "02": 11.2, "03": 10.7, "04": 9.9,
              "05": 9.1, "06": 8.7, "07": 8.4, "08": 8.1,
              "09": 9.8, "10": 10.3, "11": 10.3, "12": 11.1},
    "marseille": {"01": 12.7, "02": 13.1, "03": 12.9, "04": 12.6,
                  "05": 11.3, "06": 10.9, "07": 10.9, "08": 10.5,
                  "09": 11.0, "10": 12.0, "11": 12.9, "12": 12.8},
    "brest": {"01": 16.8, "02": 16.0, "03": 15.0, "04": 14.0,
              "05": 12.9, "06": 11.9, "07": 11.4, "08": 11.2,
              "09": 12.3, "10": 14.2, "11": 15.7, "12": 14.7},
    "stras": {"01": 8.3, "02": 8.2, "03": 8.0, "04": 7.2,
              "05": 6.6, "06": 6.4, "07": 6.2, "08": 5.9,
              "09": 6.3, "10": 6.7, "11": 7.1, "12": 8.0},
    "bord": {"01": 7.1, "02": 7.3, "03": 7.2, "04": 7.1,
             "05": 6.5, "06": 6.2, "07": 5.9, "08": 5.7,
             "09": 6.0, "10": 6.6, "11": 6.8, "12": 7.0},
    "lyon": {"01": 8.2, "02": 8.5, "03": 8.7, "04": 8.6,
             "05": 7.9, "06": 7.4, "07": 7.2, "08": 6.9,
             "09": 7.4, "10": 7.9, "11": 8.1, "12": 8.2}
}

# Department groups
region_map = {
    "paris": [2, 75, 14, 27, 28, 45, 59, 60, 61, 62, 76, 77, 78, 80, 91, 92, 93, 94, 95],
    "marseille": [13, 4, 5, 6, 11, 30, 34, 48, 66, 83, 84],
    "brest": [29, 22, 35, 44, 49, 50, 53, 56, 72, 85],
    "stras": [67, 68, 8, 10, 21, 25, 39, 51, 52, 54, 55, 57, 58, 70, 71, 88, 89, 90],
    "bord": [9, 18, 33, 16, 17, 19, 23, 24, 31, 32, 36, 37, 40, 41, 46, 47, 64, 79, 81, 82, 86, 87],
    "lyon": [69, 1, 3, 7, 12, 15, 26, 38, 42, 43, 63, 65, 73, 74]
}

# Load data
wind_df = pdt.from_file('processed_data/middle_data.csv', ';').copy()

# Reduce to department code
wind_df['short_code_commune'] = wind_df['code_commune'].astype(str).str[:-3].astype(int)

# Extract month and pad with zero
wind_df['datetime'] = pd.to_datetime(wind_df['datetime'], errors='coerce')
wind_df['month'] = wind_df['datetime'].dt.month.astype(str).str.zfill(2)

# Create a reverse lookup map for department to region
dept_to_region = {dept: region for region, depts in region_map.items() for dept in depts}

# Map regions and fill wind speeds
wind_df['region'] = wind_df['short_code_commune'].map(dept_to_region)
wind_df['average_wind'] = wind_df.apply(
    lambda row: wind_data[row['region']][row['month']]
    if pd.isna(row['average_wind']) and row['region'] and row['month'] in wind_data[row['region']]
    else row['average_wind'],
    axis=1
)

# Drop the "short_code_commune" column when done
wind_df.drop(columns=['short_code_commune', 'month', 'region'], inplace=True)

# Save the updated DataFrame back to CSV
wind_df.to_csv('processed_data/processed_winds.csv', index=False)

print("Done")