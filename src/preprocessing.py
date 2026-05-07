import pandas as pd
import numpy as np
import re


# ─────────────────────────────────────────────
# Core cleaner
# ─────────────────────────────────────────────

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning & feature-engineering pipeline for any temperature dataset."""
    df = df.copy()

    # 1. Parse dates
    if 'dt' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['dt']):
        df['dt'] = pd.to_datetime(df['dt'], errors='coerce')

    # 2. Extract time features
    if 'dt' in df.columns:
        df['year']   = df['dt'].dt.year
        df['month']  = df['dt'].dt.month
        df['decade'] = (df['year'] // 10 * 10).astype('Int64')
        df['season'] = df['month'].map(_month_to_season)

    # 3. Unify temperature column name
    if 'LandAverageTemperature' in df.columns and 'AverageTemperature' not in df.columns:
        df['AverageTemperature'] = df['LandAverageTemperature']

    # 4. Drop rows with no usable temperature
    temp_cols = [c for c in df.columns if 'Temperature' in c and 'Uncertainty' not in c]
    if temp_cols:
        df = df.dropna(subset=temp_cols, how='all')

    # 5. Convert lat / lon strings → float (e.g. "51.37N" → 51.37)
    for col in ('Latitude', 'Longitude'):
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].apply(_parse_coord)

    # 6. Tidy text columns
    for col in ('Country', 'City', 'State'):
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    return df


# ─────────────────────────────────────────────
# Missing-value audit
# ─────────────────────────────────────────────

def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return a tidy DataFrame with count & % of missing values per column."""
    total   = df.isnull().sum()
    percent = (total / len(df) * 100).round(2)
    report  = pd.DataFrame({'Missing Count': total, 'Missing %': percent})
    return report[report['Missing Count'] > 0].sort_values('Missing %', ascending=False)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _month_to_season(month):
    if pd.isna(month):
        return None
    m = int(month)
    if m in (12, 1, 2):
        return 'Winter'
    elif m in (3, 4, 5):
        return 'Spring'
    elif m in (6, 7, 8):
        return 'Summer'
    else:
        return 'Autumn'


def _parse_coord(value: str) -> float:
    """Convert '51.37N' → 51.37, '23.00W' → -23.00."""
    if pd.isna(value) or not isinstance(value, str):
        return np.nan
    value = value.strip()
    match = re.match(r'^([0-9.]+)([NSEW]?)$', value)
    if not match:
        return np.nan
    num, direction = float(match.group(1)), match.group(2)
    if direction in ('S', 'W'):
        num = -num
    return num
