"""
Enhanced Baseline Setup with Visualization and Detailed Results
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

# Store datetime column before dropping it 
# for visualization later
datetime_column = data['datetime'].copy() 

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
    objective='reg:squarederror',
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

# Convert test set back to include dates for better visualization
X_test_with_dates = X_test.copy()
# Use the saved datetime_column and align it with X_test using the index
X_test_with_dates['datetime'] = datetime_column.iloc[X_test.index]  

# Combine predictions with actual values for comparison
results = X_test_with_dates.copy()
results['Actual'] = y_test.values
results['Predicted'] = y_pred

# Sort by datetime for a better plot
results = results.sort_values(by='datetime')

# Plotting the actual vs predicted values
plt.figure(figsize=(14, 7))
plt.plot(results['datetime'], results['Actual'], label='Actual Risk Level', marker='o', alpha=0.7)
plt.plot(results['datetime'], results['Predicted'], label='Predicted Risk Level', marker='x', alpha=0.7)
plt.title("Actual vs Predicted Risk Levels")
plt.xlabel("Date")
plt.ylabel("Risk Level")
plt.legend()
plt.grid()
plt.show()

# Example: Predicting risk level for new data
new_data = pd.DataFrame({
    'rain_24': [12.3],
    'average_celsius': [15.6],
    'average_wind': [5.2],
    'duration_days': [7],
    'month': [6],
    'day_of_week': [2]
})
prediction = model.predict(new_data)
print(f"Predicted Risk Level for New Data: {prediction[0]:.4f}")