"""
Preprocessing the raw catnat_gaspar.csv file
"""
import pandas as pd
import pd_tools as pdt

_PATH_ = 'C:/Users/ajoaq/OneDrive/Documentos/GitHub/Wayqu-Early-Alarm-Model/'

# --- Helper function to print row counts ---
def print_row_count(df, step_name):
    print(f"{step_name}: {len(df)} rows remaining")

# Import and create a copy
catnat = pdt.from_file(f'{_PATH_}raw data/catnat_gaspar.csv', ';')
modified_catnat = catnat[['cod_commune', 'num_risque_jo', 'lib_risque_jo', 'dat_deb', 'dat_fin']].copy()
print_row_count(modified_catnat, "Initial load")

# Filter the DataFrame to keep only rows from 1987-2023
initial_count = len(modified_catnat)
modified_catnat = modified_catnat[modified_catnat['dat_deb'] >= '1987-01-01']
print(f"After 1987 filter: {len(modified_catnat)} rows (removed {initial_count - len(modified_catnat)})")

initial_count = len(modified_catnat)
modified_catnat = modified_catnat[modified_catnat['dat_deb'] < '2024-01-01']
print(f"After 2024 filter: {len(modified_catnat)} rows (removed {initial_count - len(modified_catnat)})")

# Eliminate unwanted events
initial_count = len(modified_catnat)
unwanted_events = [
    'Mouvements de terrain différentiels consécutifs à la sécheresse et à la réhydratation des sols',
    'Sécheresse',
    'Sécheressse',
    'Secousse Sismique'
]
modified_catnat = pdt.remove_events(modified_catnat, unwanted_events)
print(f"After removing unwanted events: {len(modified_catnat)} rows (removed {initial_count - len(modified_catnat)})")

# Convert cod_commune to numeric
initial_count = len(modified_catnat)
modified_catnat.loc[:, 'cod_commune'] = pd.to_numeric(modified_catnat['cod_commune'], errors='coerce')
print(f"After numeric conversion: {len(modified_catnat)} rows (invalid values set to NaN)")

# Eliminate invalid commune codes
initial_count = len(modified_catnat)
modified_catnat = modified_catnat[modified_catnat['cod_commune'] >= 1]
print(f"After valid commune filter: {len(modified_catnat)} rows (removed {initial_count - len(modified_catnat)})")

# Format commune codes
modified_catnat['cod_commune'] = modified_catnat['cod_commune'].astype(int).astype(str).str.zfill(5)

# Convert dates to datetime
modified_catnat['dat_deb'] = pd.to_datetime(modified_catnat['dat_deb'])
modified_catnat['dat_fin'] = pd.to_datetime(modified_catnat['dat_fin'])

# Sort by start date
modified_catnat.sort_values(by='dat_deb', ascending=True, inplace=True)

# Calculate duration
modified_catnat['duration_days'] = (modified_catnat['dat_fin'] - modified_catnat['dat_deb']).dt.days

# Filter short-duration events
initial_count = len(modified_catnat)
modified_catnat = modified_catnat[modified_catnat['duration_days'] <= 20]
print(f"After duration filter: {len(modified_catnat)} rows (removed {initial_count - len(modified_catnat)})")

# Remove NaN values
initial_count = len(modified_catnat)
pdt.prune(modified_catnat)
print(f"After NaN removal: {len(modified_catnat)} rows (removed {initial_count - len(modified_catnat)})")

# Final formatting
modified_catnat = modified_catnat.drop(columns=['dat_fin'])
modified_catnat = modified_catnat.rename(columns={
    'dat_deb': 'datetime',
    'cod_commune': 'code_commune'
})

# Save results
modified_catnat.to_csv(f'{_PATH_}processed_data/processed_catnat.csv', sep=';', index=False)
print(f"\nFinal output: {len(modified_catnat)} rows")
print("Done")