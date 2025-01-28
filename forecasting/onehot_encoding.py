import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay

# Load the dataset
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

# Model Evaluation
accuracy = accuracy_score(y_test.values.argmax(axis=1), y_pred.argmax(axis=1))
print(f"Model Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test.values.argmax(axis=1), y_pred.argmax(axis=1)))

# Confusion Matrix
ConfusionMatrixDisplay.from_predictions(y_test.values.argmax(axis=1), y_pred.argmax(axis=1))
plt.title("Confusion Matrix for XGBClassifier")
plt.show()
