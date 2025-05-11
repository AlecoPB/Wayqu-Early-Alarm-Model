# -*- coding: utf-8 -*-
"""
Created on Tue May  6 15:07:49 2025

@author: ajoaq
"""

import pd_tools as pdt

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/catnat_meteo_merged.csv', ';')

# Drop redundant columns and rename
df.rename(columns={'code_commune_x': 'code_commune'}, inplace=True)
df.drop(columns=['code_commune_y', 'lib_risque_jo'], inplace=True)

## TEMPORAL FEATURES
# Cumulative rainfall
df['cumulative_rr_7d'] = df.groupby('code_commune')['rr'].rolling(7, min_periods=1, closed='left').sum().reset_index(level=0, drop=True)

# Rainfall Intensity
df['rr_intensity'] = df['rr'] / df['drr']  # mm/hour (if drr is in hours)

# Days since last rain
df['days_since_rain'] = (
    df.groupby('code_commune')['rr']
    .apply(lambda x: x.eq(0).groupby(x.ne(0).cumsum()).cumsum())
    .reset_index(level=0, drop=True)
)


## SOIL/LAND INTERACTION
# Soil saturation index
df['dept_avg_rr'] = df.groupby('code_dept')['rr'].transform('mean')

## GEOSPACIAL FEATURES
# Department-level aggregates
df['dept_avg_rr'] = df.groupby('code_dept')['rr'].transform('mean')

## RISK EVENT FEATURES
# Risk persistence
df['risk_duration_flag'] = (df['duration_days'] > 3).astype(int)  # Binary flag for prolonged risk

## FROST RELATED FEATURES
# Freezing-Thawing cycles
df['freeze_thaw_cycle'] = (df['dg'] > 0).astype(int)  # Binary flag for freezing events

# Frost Duration Impact
df['frost_impact'] = df['dg'] * df['tntxm']  # Hypothetical metric

## TEMPERATURE-WIND INTERACTION
# Wind Chill Effect
df['wind_chill'] = 13.12 + 0.6215 * df['tntxm'] - 11.37 * (df['ffm'] ** 0.16) + 0.3965 * df['tntxm'] * (df['ffm'] ** 0.16)

# Temperature Extremes
df['temp_fluctuation'] = df.groupby('code_commune')['tntxm'].diff().abs()  # Daily ΔT

# Prune NaN values
pdt.prune(df)

# Save as CSV
df.to_csv(f'{_PATH_}data/augmented_data.csv', sep=';', index=False)
print('done')
