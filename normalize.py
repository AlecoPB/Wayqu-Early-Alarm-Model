"""
Normalizing and encoding data
"""

import pandas as pd

# Load the dataset
file_path = 'OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/processed_data/final_data.csv' # Location might change
data = pd.read_csv(file_path)


##############
# Scaling data
"""
from sklearn.preprocessing import MinMaxScaler
# Define columns to scale
columns_to_scale = ['rain_24', 'average_celsius', 'average_wind']

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Apply scaling
data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

# Save the transformed dataset
output_path = 'normalized_data/scaled_final_data.csv'
data.to_csv(output_path, index=False)

print(f"Feature scaling complete. Scaled dataset saved to '{output_path}'")
"""

##############
# Correlation analysis
"""
# Convert 'datetime' to numerical values (days since the first date)
data['datetime'] = pd.to_datetime(data['datetime'])
data['datetime_numeric'] = (data['datetime'] - data['datetime'].min()).dt.days

# Drop original 'datetime' for correlation analysis
data_for_corr = data.drop(columns=['datetime'])

# Compute correlation matrix
correlation_matrix = data_for_corr.corr()

# Display correlation with 'duration_days'
print("Correlation with 'duration_days':")
print(correlation_matrix['duration_days'])
"""

##############
# Ordinal risk level encoding

from sklearn.preprocessing import OrdinalEncoder

# Apply ordinal encoding to 'risk_level'
ordinal_encoder = OrdinalEncoder()
data['risk_level_ordinal'] = ordinal_encoder.fit_transform(data[['risk_level']])

# Save the dataset with ordinal encoding
data.to_csv('normalized_data/data_with_ordinal_encoding.csv', index=False)
print("Ordinal encoding applied. Dataset saved to 'data_with_ordinal_encoding.csv'.")


##############
# One-hot risk level encoding
"""
# Apply one-hot encoding to 'risk_level'
data = pd.get_dummies(data, columns=['risk_level'], prefix='risk_level')

# Save the dataset with one-hot encoding
data.to_csv('data_with_one_hot_encoding.csv', index=False)
print("One-hot encoding applied. Dataset saved to 'data_with_one_hot_encoding.csv'.")
"""