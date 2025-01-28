"""
Model trained with ordinal encoding of risk level
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load dataset (with ordinal encoding and duration_days dropped)
data = pd.read_csv('C:/Users/ajoaq/OneDrive/Documentos/GitHub\Wayqu-Early-Alarm-Model/normalized_data/data_with_ordinal_encoding.csv')

# Drop 'duration_days' and 'risk_level' if they exist
if 'duration_days' in data.columns:
    data.drop(columns=['duration_days', 'risk_level'], inplace=True)

# Define Features (X) and Target (y)
X = data.drop(columns=['risk_level_ordinal', 'datetime'])  # Drop target + datetime
y = data['risk_level_ordinal']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling (Standardization)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize XGBRegressor
model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, random_state=42)

# Train Model
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

# Evaluation Metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Performance:")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R² Score: {r2:.4f}")

## Plotting
# Scatter plot of actual vs predicted values
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
plt.xlabel("Actual Risk Level")
plt.ylabel("Predicted Risk Level")
plt.title("Actual vs Predicted Risk Levels")
plt.axline((0, 0), slope=1, color="red", linestyle="--")  # Ideal predictions line
plt.show()

# Residual plot (errors)
residuals = y_test - y_pred
plt.figure(figsize=(8, 6))
sns.histplot(residuals, bins=30, kde=True)
plt.xlabel("Prediction Error (Residuals)")
plt.ylabel("Frequency")
plt.title("Distribution of Prediction Errors")
plt.axvline(0, color="red", linestyle="--")  # Perfect predictions reference
plt.show()