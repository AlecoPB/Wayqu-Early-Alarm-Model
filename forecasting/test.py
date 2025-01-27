"""
Predicting Risk Levels for Future Dates
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# Load the data
data = pd.read_csv("OneDrive\Escritorio\Machine_Learning\LockIn\Wayqu\processed_data/final_data.csv")

# Extract time-based features from 'datetime'
data['datetime'] = pd.to_datetime(data['datetime'])
data['month'] = data['datetime'].dt.month
data['day_of_week'] = data['datetime'].dt.dayofweek

# Drop unused columns
data = data.drop(['code_commune', 'datetime'], axis=1)

# Define features (X) and target (y)
X = data.drop('risk_level', axis=1)
y = data['risk_level']

# Split the data into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train an XGBoost model
model = xgb.XGBRegressor(
    objective='reg:squarederror',  # Use 'reg:squarederror' for regression
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

# Example: Predicting risk level for future dates
# Create new data with specific future dates
future_dates = pd.DataFrame({
    'datetime': pd.to_datetime(['2025-06-15', '2025-06-16']),  # Specify future dates here
    'rain_24': [10.5, 8.0],  # Hypothetical values
    'average_celsius': [18.3, 20.1],
    'average_wind': [6.5, 5.0],
    'duration_days': [7, 6]
})

# Extract time-based features from future dates
future_dates['month'] = future_dates['datetime'].dt.month
future_dates['day_of_week'] = future_dates['datetime'].dt.dayofweek

# Drop unnecessary columns
future_features = future_dates.drop(['datetime'], axis=1)

# Predict risk levels
future_dates['Predicted Risk Level'] = model.predict(future_features)

# Display the results
print(future_dates)

# Optional: Plot predicted risk levels for the future dates
plt.figure(figsize=(8, 5))
plt.plot(future_dates['datetime'], future_dates['Predicted Risk Level'], marker='o', label='Predicted Risk Level')
plt.title("Predicted Risk Levels for Future Dates")
plt.xlabel("Date")
plt.ylabel("Risk Level")
plt.legend()
plt.grid()
plt.show()
