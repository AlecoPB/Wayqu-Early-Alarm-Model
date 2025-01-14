"""
Preprocessing the raw catnat_gaspar.csv file
"""
import pandas as pd
import pd_tools as pdt

# Import and create a copy
catnat = pdt.from_file('catnat_gaspar.csv', ';')
modified_catnat = catnat[['cod_nat_catnat', 'cod_commune', 'lib_risque_jo', 'dat_deb']].copy()

# Filter the DataFrame to keep only rows from 2010 onwards
modified_catnat = modified_catnat[modified_catnat['dat_deb'] >= '2010-01-01']

# Eliminate rows where 'lib_risque_jo' contains an specific event
unwanted_events = ['Mouvements de terrain différentiels consécutifs à la sécheresse et à la réhydratation des sols',
                  'Sécheresse',
                  'Sécheressse',
                  'Secousse Sismique']

modified_catnat = pdt.remove_events(modified_catnat, unwanted_events)

# Convert cod_commune to numeric and assign back to the DataFrame using .loc
modified_catnat.loc[:, 'cod_commune'] = pd.to_numeric(modified_catnat['cod_commune'], errors='coerce')
modified_catnat = modified_catnat[modified_catnat['cod_commune'] >= 1]

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

# Save as csv
modified_catnat.to_csv('modified_catnat.csv', sep=';', index=False)

print("Done")