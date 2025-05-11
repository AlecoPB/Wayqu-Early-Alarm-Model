# -*- coding: utf-8 -*-
"""
Created on Mon May 12 00:44:06 2025

@author: ajoaq
"""

import pandas as pd
import pd_tools as pdt
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/enhanced_features.csv', ';')

df['datetime'] = pd.to_datetime(df['datetime'])

def prepare_for_modeling(df: pd.DataFrame, model_type: str = 'tree'):
    # Make a copy to avoid changing original
    df = df.copy()

    # -------------------
    # Drop unused or already removed columns
    drop_cols = ['datetime', 'code_commune', 'days_since_rain', 'dg',
                    'risk_duration_flag', 'freeze_thaw_cycle', 'frost_impact']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

    # -------------------
    # Rename for clarity
    rename_map = {
        'rr': 'rainfall_mm',
        'drr': 'rainfall_duration_hr',
        'tnsol': 'soil_temperature_c',
        'tntxm': 'avg_temperature_c',
        'ffm': 'avg_wind_speed_kph',
        'wind_chill': 'wind_chill_index',
        'rr_intensity': 'rainfall_intensity_mmph',
        'cummulative_rr': 'rainfall_cumulative_7d_mm',
        'temp_fluctuation': 'temperature_fluctuation_c',
        'code_dept': 'department_code',
        'dept_avr_rr': 'dept_avg_rainfall_mm',
        'duration_days': 'event_duration_days',
        'has_last_event': 'had_previous_event',
        'dayofweek': 'day_of_week',
        'num_risque_jo': 'disaster_class'
    }
    df = df.rename(columns=rename_map)

    # -------------------
    # Encode cyclical 'day_of_week'
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    df.drop(columns='day_of_week', inplace=True)

    # -------------------
    # Separate features and label
    y = df['disaster_class']
    X = df.drop(columns='disaster_class')

    # -------------------
    # Define column groups
    numeric_features = [
        'rainfall_mm', 'rainfall_duration_hr', 'soil_temperature_c',
        'avg_temperature_c', 'avg_wind_speed_kph', 'wind_chill_index',
        'rainfall_intensity_mmph', 'rainfall_cumulative_7d_mm',
        'temperature_fluctuation_c', 'dept_avg_rainfall_mm',
        'event_duration_days', 'dow_sin', 'dow_cos'
    ]

    categorical_features = ['department_code', 'month']
    passthrough_features = ['had_previous_event', 'year']

    # -------------------
    # Preprocessing pipeline
    transformers = []

    if model_type != 'tree':
        transformers.append((
            'num', Pipeline([
                ('impute', SimpleImputer(strategy='mean')),
                ('scale', StandardScaler())
            ]), numeric_features
        ))
    else:
        transformers.append(('num', 'passthrough', numeric_features))

    transformers.append((
        'cat', OneHotEncoder(handle_unknown='ignore', sparse=False),
        categorical_features
    ))

    transformers.append((
        'bin', 'passthrough', passthrough_features
    ))

    preprocessor = ColumnTransformer(transformers)

    # Transform the dataset
    X_transformed = preprocessor.fit_transform(X)

    # Get column names (optional, if you want to return DataFrame)
    cat_cols = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
    feature_names = (
        numeric_features + list(cat_cols) + passthrough_features
        if model_type != 'tree' else
        numeric_features + list(cat_cols) + passthrough_features
    )

    X_df = pd.DataFrame(X_transformed, columns=feature_names)

    return X_df, y
