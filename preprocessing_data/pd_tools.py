"""
Tools for pandas
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