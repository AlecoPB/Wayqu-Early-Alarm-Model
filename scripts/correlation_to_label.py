import pandas as pd
import pd_tools as pdt
import matplotlib.pyplot as plt
from sklearn.feature_selection import f_classif, mutual_info_classif
from sklearn.preprocessing import StandardScaler

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/augmented_data_remapped_classes.csv', ';')

df['datetime'] = pd.to_datetime(df['datetime'])

# Filter for relevant columns (example - adjust per your needs)
numeric_cols = [
    'rr',                # Rainfall
    'drr',               # Rainfall duration
    'tnsol',             # Soil temperature
    'dg',                # Freezing duration
    'tntxm',             # Average temperature
    'ffm',               # Average wind speed  
    'cumulative_rr_7d',  # 7-day rain sum
    'rr_intensity',      # Rain intensity mm/h
    'days_since_rain',   # Days since last rain
    'dept_avg_rr',       # Average rr per department
    'wind_chill',        # Freeze and wind interaction
    'temp_fluctuation',  # Delta Temperature
    'duration_days'      # Disaster duration
]
# Subset and drop missing values
# df = df.dropna(subset=numeric_cols)

X = df[numeric_cols]

# Detect and replace inf/-inf with NaN
X = X.replace([float('inf'), float('-inf')], pd.NA)

# Drop rows with any NaN in the features
X = X.dropna()

# Also align y with filtered X
y = df.loc[X.index, 'num_risque_jo']

# Scale features
X_scaled = StandardScaler().fit_transform(X)

# Compute scores
f_scores, f_pvals = f_classif(X_scaled, y)
mi_scores = mutual_info_classif(X_scaled, y, discrete_features=False)

# Build result table
result = pd.DataFrame({
    'Feature': numeric_cols,
    #'F_score': f_scores,
    #'F_pval': f_pvals,
    'Mutual_Info': mi_scores
}).sort_values('Mutual_Info', ascending=False)

# Print as table
print("\n=== Feature Correlation to Multiclass Target ===")
print(result.to_string(index=False, float_format="%.4f"))

# Plot
plt.figure(figsize=(10, 6))
# plt.barh(result['Feature'], result['F_score'], color='steelblue', label='F-score')
plt.barh(result['Feature'], result['Mutual_Info'], color='orange', alpha=0.6, label='Mutual Info')
plt.xlabel('Score')
plt.title('Feature Discriminative Power (F-score vs Mutual Info)')
plt.legend()
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()