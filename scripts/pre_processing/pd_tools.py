"""
Tools for preprocessing data
"""
import pandas as pd


def from_file(filename, delimiter):
    """Creates a pd.DataFrame from a file

    Args:
        filename (string): file to load from
        delimiter : column separator
    """

    return pd.DataFrame(pd.read_csv(filename, delimiter=delimiter))


def prune(df):
    """Removes NaN values

    Args:
        df (DataFrame)
    """
    return df.dropna()


def remove_events(df, events):
    """Removes an event from a DF
    
    Args:
        df (DataFrame)
        event (string): name of the event to be removed
    """
    for event in events:
       df = df[~df['lib_risque_jo'].str.contains(event, na=False)]

    return df


def extract_useful_data_from_meteo(cvs, n_dep):
    """Extracts only the useful data from affected communes.

    Args:
        cvs (string): CVS file containing the rain data.
        n_dep (int): number of the department to be worked on.
    """
    # Import weather data and the list of communes
    o_df = from_file(cvs, ';')
    df = o_df[['NUM_POSTE', 'AAAAMMJJ', 'RR', 'TNTXM', 'FFM']].copy()
    list_of_communes = from_file('unique_communes.csv', ';')

    # Only from 1987 onwards
    df['datetime'] = pd.to_datetime(df['AAAAMMJJ'], format='%Y%m%d')
    df = df[df['datetime'] >= '1987-01-01']

    # Only from communes that give us data
    list_of_communes = list_of_communes['unique_communes'].astype(str).str[:5]
    filtered_df = df[df['NUM_POSTE'].astype(str).str[:5].isin(list_of_communes)].copy()

    # Removing the last two digits using vectorized operation
    filtered_df.loc[:, 'NUM_POSTE'] = filtered_df['NUM_POSTE'].astype(str).str[:-3]

    # Convert to string and pad with zeros to ensure 5-digit formatting
    filtered_df.loc[:, 'NUM_POSTE'] = filtered_df['NUM_POSTE'].astype(int).astype(str).str.zfill(5)

    # Sort the DataFrame by 'datetime' and assign back to the DataFrame
    filtered_df = filtered_df.sort_values(by='datetime', ascending=True)

    # Remove NaN values
    prune(filtered_df)

    # Formatting
    filtered_df = filtered_df.drop(columns=['AAAAMMJJ'])
    filtered_df = filtered_df.rename(columns={'NUM_POSTE': 'code_commune'})

    # Format i with leading zeros for single-digit numbers
    filename = f'processed_data/processed_departments/processed_dep_{n_dep:02d}.csv'

    # Save as CSV
    filtered_df.to_csv(filename, sep=';', index=False)

def extract_temperatures(csv):

    avg_temperature = from_file(csv, ';')

    # Convert commune code to numeric, eliminate invalid values
    avg_temperature.loc[:, 'Code INSEE département'] = pd.to_numeric(avg_temperature['Code INSEE département'], errors='coerce')
    avg_temperature = avg_temperature[avg_temperature['Code INSEE département'] >= 1]

    # Convert the date columns to datetime
    avg_temperature['Date'] = pd.to_datetime(avg_temperature['Date'])

    # Rename
    avg_temperature = avg_temperature.rename(columns={'Date': 'datetime',
                                                      'Code INSEE département': 'code_commune',
                                                      'TMoy (°C)': 'average_celsius'})

    # Filter the DataFrame to keep only rows from 2010-2023
    avg_temperature = avg_temperature[avg_temperature['datetime'] >= '2019-01-01']
    avg_temperature = avg_temperature[avg_temperature['datetime'] <= '2019-12-31']

    # Convert to string and pad with zeros to ensure 2-digit formatting
    avg_temperature['code_commune'] = avg_temperature['code_commune'].astype(int).astype(str).str.zfill(2)

    # Save as csv
    avg_temperature.to_csv('processed_data/average_temperatures.csv', sep=';', index=False)


def cumulative_rainfall(csv):
    """Calculates the cumulative raifall and adds it to the table
    csv : file to extract the DataFrame
    """

    # Create DataFrame from csv file
    rain_df = from_file(csv, ';')

    ## IMPORTANT - CORRECT AND FINISH ###
    #   Sort by commune and datetime
    rain_df = rain_df.sort_values(by=['code_commune', 'datetime'])

    rain_df['cumulative_rainfall'] = (
        rain_df.groupby(window=7, min_periods=1).sum().reset_index(level=0, drop=True)
    )