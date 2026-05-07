import pandas as pd
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets')

FILES = {
    'global':     'GlobalTemperatures.csv',
    'country':    'GlobalLandTemperaturesByCountry.csv',
    'major_city': 'GlobalLandTemperaturesByMajorCity.csv',
    'state':      'GlobalLandTemperaturesByState.csv',
    'city':       'GlobalLandTemperaturesByCity.csv',
}

def load_data(file_path: str, nrows: int = None) -> pd.DataFrame:
    """Load a CSV and parse the 'dt' date column."""
    df = pd.read_csv(file_path, nrows=nrows, parse_dates=['dt'] if _has_dt(file_path) else False)
    return df

def _has_dt(file_path: str) -> bool:
    """Peek at header to check for 'dt' column."""
    try:
        header = pd.read_csv(file_path, nrows=0).columns.tolist()
        return 'dt' in header
    except Exception:
        return False

def load_dataset(key: str, nrows: int = None) -> pd.DataFrame:
    """Load a single named dataset."""
    path = os.path.join(BASE_PATH, FILES[key])
    df = load_data(path, nrows=nrows)
    return df

def load_all_datasets(nrows_city: int = 500_000) -> dict:
    """
    Load all datasets.  The full city file is ~508 MB so we sample it
    to keep memory reasonable inside Streamlit.
    """
    datasets = {}
    for key, fname in FILES.items():
        path = os.path.join(BASE_PATH, fname)
        if not os.path.exists(path):
            continue
        n = nrows_city if key == 'city' else None
        datasets[key] = load_data(path, nrows=n)
    return datasets
