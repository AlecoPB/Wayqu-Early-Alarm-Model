# -*- coding: utf-8 -*-
"""
Created on Tue May  6 17:52:42 2025

@author: ajoaq
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pd_tools as pdt
import numpy as np

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/augmented_data_remapped_classes.csv', ';')

df['datetime'] = pd.to_datetime(df['datetime'])

# Filter for relevant columns (example - adjust per your needs)
numeric_cols = [
    'rr',                # Rainfall
    'drr',               # Rainfall duration
    'tnsol',             # Soil temperature
    'dg',                # Freezing duration
    'tntxm',             # Average temperature
    'ffm',               # Average wind speed  
    'cumulative_rr_7d',  # 7-day rain sum
    'rr_intensity',      # Rain intensity mm/h
    'days_since_rain',   # Days since last rain
    'dept_avg_rr',       # Average rr per department
    'wind_chill',        # Freeze and wind interaction
    'temp_fluctuation',  # Delta Temperature
    'duration_days'      # Disaster duration
]

# Subset and drop missing values
corr_df = df[numeric_cols].dropna()
print(f"Working with {len(corr_df)} complete records")

# Pearson correlation (linear relationships)
corr_matrix = corr_df.corr(method='pearson')

plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    fmt=".2f",       # 2 decimal places
    cmap="coolwarm", # Blue(-1) to Red(+1)
    vmin=-1, vmax=1, # Fix color scale
    mask=np.triu(np.ones_like(corr_matrix)),  # Show lower triangle only,¿
    annot=True      # Show values
)
plt.title("Correlation Matrix (Pearson)")
plt.tight_layout()
plt.show()

top_pairs = corr_matrix.unstack().sort_values(ascending=False)

# Check if rainfall predicts future disasters
df['disaster_next_week'] = df.groupby('code_dept')['duration_days'].shift(-7)
print(df[['rr', 'disaster_next_week']].corr())

# Save correlation matrix
corr_matrix.to_csv(f"{_PATH_}data/correlation_matrix.csv")

# Save top variable pairs
top_pairs.to_csv(f"{_PATH_}data/top_correlations.csv")

