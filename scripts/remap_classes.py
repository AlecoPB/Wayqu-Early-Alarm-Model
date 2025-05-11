# -*- coding: utf-8 -*-
"""
Created on Tue May  6 17:23:53 2025

@author: ajoaq
"""
import pd_tools as pdt
import pandas as pd

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/augmented_data.csv', ';')

df['datetime'] = pd.to_datetime(df['datetime'])

# Get unique values and their counts
risk_counts = df['num_risque_jo'].value_counts().sort_index()
print("Current risk values and counts:")
print(risk_counts)

# Find min and max
min_risk = df['num_risque_jo'].min()
max_risk = df['num_risque_jo'].max()
print(f"\nCurrent range: {min_risk} to {max_risk}")

# Ensure chronological order
df = df.sort_values(['code_commune', 'datetime'])

# Fill NaN columns with 0 to represent the lack of a disaster.
df['num_risque_jo'] = df['num_risque_jo'].fillna(0).astype(int)

# Create mapping from current values to new 1-based values
unique_risks = sorted(df['num_risque_jo'].unique())
risk_mapping = {old: (1 if old == 0 else new + 1) for new, old in enumerate(unique_risks)}

# Set event date only when risk > 0
df['last_event_date'] = df['datetime'].where(df['num_risque_jo'] > 0)

# Forward fill for all rows by group
df['last_event_date'] = df.groupby('code_commune')['last_event_date'].ffill()

# Compute days since last event for rows with no event
mask = df['num_risque_jo'] == 0
df.loc[mask, 'duration_days'] = (df.loc[mask, 'datetime'] - df.loc[mask, 'last_event_date']).dt.days

# Track rows where we had no last event
df['has_last_event'] = df['last_event_date'].notna().astype(int)

# Fill remaining NaNs in duration_days with a sentinel (e.g. -1)
df['duration_days'] = df['duration_days'].fillna(-1).astype(int)

# Drop helper column
df = df.drop(columns='last_event_date')

# Apply mapping
df['num_risque_jo'] = df['num_risque_jo'].map(risk_mapping)

# Save remapped df
df.to_csv(f'{_PATH_}data/augmented_data_remapped_classes.csv', sep=';', index=False)

# Verify new range
print("\nAfter remapping:")
print(f"New range: {df['num_risque_jo'].min()} to {df['num_risque_jo'].max()}")
print("New value counts:")
print(df['num_risque_jo'].value_counts().sort_index())