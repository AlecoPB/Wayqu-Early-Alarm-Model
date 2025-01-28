"""
Preprocessing the raw catnat_gaspar.csv file
"""
import pandas as pd
import pd_tools as pdt

# Import and create a copy
catnat = pdt.from_file('catnat_gaspar.csv', ';')
modified_catnat = catnat[['cod_commune', 'num_risque_jo', 'lib_risque_jo', 'dat_deb', 'dat_fin']].copy()

# Filter the DataFrame to keep only rows from 2010-2023
modified_catnat = modified_catnat[modified_catnat['dat_deb'] >= '1987-01-01']
modified_catnat = modified_catnat[modified_catnat['dat_deb'] < '2024-01-01']

# Eliminate rows where 'lib_risque_jo' contains an specific event
unwanted_events = ['Mouvements de terrain différentiels consécutifs à la sécheresse et à la réhydratation des sols',
                  'Sécheresse',
                  'Sécheressse',
                  'Secousse Sismique']

modified_catnat = pdt.remove_events(modified_catnat, unwanted_events)

# Convert cod_commune to numeric, eliminate invalid values
modified_catnat.loc[:, 'cod_commune'] = pd.to_numeric(modified_catnat['cod_commune'], errors='coerce')
modified_catnat = modified_catnat[modified_catnat['cod_commune'] >= 1]

# Convert to string and pad with zeros to ensure 5-digit formatting
modified_catnat['cod_commune'] = modified_catnat['cod_commune'].astype(int).astype(str).str.zfill(5)

# Convert the date columns to datetime
modified_catnat['dat_deb'] = pd.to_datetime(modified_catnat['dat_deb'])
modified_catnat['dat_fin'] = pd.to_datetime(modified_catnat['dat_fin'])

# Sort the DataFrame by 'dat_deb' and assign back to the DataFrame
modified_catnat.sort_values(by='dat_deb', ascending=True, inplace=True)

# Calculate the duration in days
modified_catnat['duration_days'] = (modified_catnat['dat_fin'] - modified_catnat['dat_deb']).dt.days

# Eliminate too long lasting events
modified_catnat = modified_catnat[modified_catnat['duration_days'] <= 20]

# Remove NaN values
pdt.prune(modified_catnat)

# Formatting
modified_catnat = modified_catnat.drop(columns=['dat_fin'])
modified_catnat = modified_catnat.rename(columns={'dat_deb': 'datetime'})
modified_catnat = modified_catnat.rename(columns={'cod_commune': 'code_commune'})

# Save as csv
modified_catnat.to_csv('processed_data/processed_catnat.csv', sep=';', index=False)

print("Done")