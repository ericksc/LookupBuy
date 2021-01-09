import pandas as pd
from pathlib import Path

def load_csv2df():
    try:
        return pd.concat([ pd.read_csv(filename) for filename in Path().rglob('*.csv')])
    except ValueError as err:
        raise ValueError(f'No files found on directory. Please check if CSV files exist. {err}')
