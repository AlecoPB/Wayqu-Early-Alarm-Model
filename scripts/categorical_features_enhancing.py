# -*- coding: utf-8 -*-
"""
Created on Sun May 11 22:33:58 2025

@author: ajoaq
"""
import pandas as pd
import pd_tools as pdt

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/augmented_data_remapped_classes.csv', ';')

df['datetime'] = pd.to_datetime(df['datetime'])

# One-hot encode the deparmental codes
pd.get_dummies(df['code_dept'], prefix='dept')

# Extract features from date
df['month'] = df['datetime'].dt.month
df['season'] = df['datetime'].dt.month % 12 // 3 + 1  # Season 1–4
df['dayofweek'] = df['datetime'].dt.dayofweek
df['year'] = df['datetime'].dt.year

# Save enhanced df
df.to_csv(f'{_PATH_}/data/enhanced_features.csv', sep=';', index=False)
