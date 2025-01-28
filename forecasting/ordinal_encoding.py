"""
Model trained with ordinal encoding of risk level
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load dataset (with ordinal encoding and duration_days dropped)
data = pd.read_csv('normalized_data/data_with_ordinal_encoding.csv')

# Drop 'duration_days' if it exists
if 'duration_days' in data.columns:
    data.drop(columns=['duration_days'], inplace=True)

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

## Test for data leakage
import seaborn as sns
import matplotlib.pyplot as plt

# Check correlation again
correlation_matrix = pd.DataFrame(X_train, columns=X.columns).corrwith(pd.Series(y_train))
correlation_matrix.sort_values(ascending=False, inplace=True)

# Visualize
plt.figure(figsize=(10, 5))
sns.barplot(x=correlation_matrix.index, y=correlation_matrix.values)
plt.xticks(rotation=90)
plt.title("Feature Correlations with Target (Risk Level)")
plt.show()

print(correlation_matrix)
