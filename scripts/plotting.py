import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pd_tools as pdt

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

df = pdt.from_file(f'{_PATH_}data/augmented_data_remapped_classes.csv', ';')

# df = df.rename(columns={'code_commune_x': 'code_commune'})

# Configuration - USER CAN CHANGE THESE
START_YEAR = 2020
END_YEAR = 2021
DEPT_CODE = df['code_dept'].sample(1).iloc[0] # Directly taken from code_dept
COLUMN_TO_PLOT = "rr"  # Default: rainfall in mm

df['datetime'] = pd.to_datetime(df['datetime'])

# Filter rows for given department and datetime year range
filtered_df = df[
    (df['code_dept'] == DEPT_CODE) #&
    #(df['datetime'].dt.year.between(START_YEAR, END_YEAR))
]
#filtered_df.to_csv(f'{_PATH_}/optimized_data/data/debugging_data.csv')

# Resample to weekly averages for cleaner plot
plot_data = filtered_df.resample('M', on='datetime')[COLUMN_TO_PLOT].mean()
#plot_data = filtered_df[{'datetime', 'code_dept'
plot_data.to_csv(f'{_PATH_}/optimized_data/data/debugging_data.csv')

# Create plot
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=plot_data,
    linewidth=2,
    color='steelblue'
)

# Formatting
plt.title(f"Weekly {COLUMN_TO_PLOT} in Department {DEPT_CODE} ({START_YEAR}-{END_YEAR})")
plt.xlabel("Date")
plt.ylabel(f"{COLUMN_TO_PLOT} (mm)" if COLUMN_TO_PLOT == 'rr' else COLUMN_TO_PLOT)
plt.grid(alpha=0.3)
sns.despine()

# Highlight extreme values
max_val = plot_data.max()
if max_val > 0:
    plt.axhline(y=max_val, color='firebrick', linestyle='--', alpha=0.5)
    plt.text(
        x=plot_data.index[-1], 
        y=max_val*1.05, 
        s=f"Max: {max_val:.1f}", 
        color='firebrick'
    )

plt.tight_layout()
plt.show()