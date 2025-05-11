# -*- coding: utf-8 -*-
"""
Created on Sat May 10 20:55:14 2025

@author: ajoaq
"""

import pandas as pd
import pd_tools as pdt

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/augmented_data_remapped_classes.csv', ';')

def find_missing_dates(df, datetime_col='datetime'):
    """
    Scan a DataFrame for missing dates in a datetime column.
    
    Parameters:
    - df: pandas DataFrame
    - datetime_col: name of the datetime column (default 'datetime')
    
    Returns:
    - List of missing dates
    - Prints summary information
    """
    # Ensure the column is in datetime format
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    
    # Extract just the date part (without time)
    df['date'] = df[datetime_col].dt.date
    
    # Find all unique dates in the dataset
    unique_dates = df['date'].unique()
    
    # Create a date range covering the min to max date in data
    min_date = df['date'].min()
    max_date = df['date'].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D').date
    
    # Find which dates are missing
    missing_dates = [date for date in all_dates if date not in unique_dates]
    
    # Print summary
    print(f"Date range in data: {min_date} to {max_date}")
    print(f"Total days in range: {len(all_dates)}")
    print(f"Days with data: {len(unique_dates)}")
    print(f"Missing days: {len(missing_dates)}")
    
    if missing_dates:
        print("\nMissing dates:")
        for date in missing_dates:
            print(date.strftime('%Y-%m-%d'))
    else:
        print("\nNo missing dates found in the range.")
    
    return missing_dates

# Example usage:
if __name__ == "__main__":
    missing_dates = find_missing_dates(df)