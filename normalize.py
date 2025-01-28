"""
Normalizing and encoding data
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset (replace 'your_file.csv' with your actual file path)
file_path = 'processed_data/final_data.csv'
data = pd.read_csv(file_path)

# Scaling data
"""
# Define columns to scale
columns_to_scale = ['rain_24', 'average_celsius', 'average_wind']

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Apply scaling
data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

# Save the transformed dataset
output_path = 'processed_data/scaled_final_data.csv'
data.to_csv(output_path, index=False)

print(f"Feature scaling complete. Scaled dataset saved to '{output_path}'")
"""

# Correlation analysis
# Compute correlation matrix
correlation_matrix = data.corr()

# Display correlation with 'duration_days'
print(correlation_matrix['duration_days'])