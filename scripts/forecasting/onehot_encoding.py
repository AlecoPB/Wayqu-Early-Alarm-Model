import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# Load the dataset
# NOTE: The location might vary
data = pd.read_csv("C:/Users/ajoaq/OneDrive/Documentos/GitHub\Wayqu-Early-Alarm-Model/normalized_data/data_with_ordinal_encoding.csv")

# Drop 'duration_days' if they exist
if 'duration_days' in data.columns:
    data.drop(columns=['duration_days'], inplace=True)

# Convert 'datetime' to pandas datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Extract useful time-based features
data['year'] = data['datetime'].dt.year
data['month'] = data['datetime'].dt.month
data['day'] = data['datetime'].dt.day

# Drop the original datetime column
data.drop(columns=['datetime'], inplace=True)

# One-Hot Encoding for 'risk_level'
ohe = OneHotEncoder(sparse_output=False, drop='first')
risk_level_encoded = ohe.fit_transform(data[['risk_level']])
risk_level_encoded_df = pd.DataFrame(risk_level_encoded, columns=ohe.get_feature_names_out(['risk_level']))

# Concatenate the encoded values and drop original 'risk_level'
data = pd.concat([data.drop(columns=['risk_level']), risk_level_encoded_df], axis=1)

# Separate features and target
X = data.drop(columns=risk_level_encoded_df.columns)  # Features
y = risk_level_encoded_df  # Target (One-Hot Encoded Risk Levels)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the XGBoost Model
xgb_model = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss')
xgb_model.fit(X_train_scaled, y_train)

# Make Predictions
y_pred = xgb_model.predict(X_test_scaled)

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
plt.axvline(0, color="red", linestyle="--")
plt.show()