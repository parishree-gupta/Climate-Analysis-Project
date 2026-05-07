import pandas as pd
import numpy as np


# ─────────────────────────────────────────────
# Basic EDA
# ─────────────────────────────────────────────

def summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics for all numeric columns."""
    return df.describe().T


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation matrix for numeric columns."""
    numeric = df.select_dtypes(include=[float, int])
    return numeric.corr()


# ─────────────────────────────────────────────
# Global-level trends
# ─────────────────────────────────────────────

def global_yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Annual mean land temperature from the GlobalTemperatures dataset.
    Works on any df that has 'year' and 'AverageTemperature'.
    """
    return (
        df.groupby('year')['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
    )


def global_seasonal_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Mean temperature per season per year."""
    if 'season' not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(['year', 'season'])['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
    )


# ─────────────────────────────────────────────
# Country-level analysis
# ─────────────────────────────────────────────

def top_warming_countries(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """
    Countries with the largest temperature rise:
      warming = mean(last 30 years) − mean(first 30 years).
    """
    if 'Country' not in df.columns or 'year' not in df.columns:
        return pd.DataFrame()

    early = df[df['year'] <= df['year'].min() + 29]
    late  = df[df['year'] >= df['year'].max() - 29]

    early_avg = early.groupby('Country')['AverageTemperature'].mean().rename('EarlyMean')
    late_avg  = late.groupby('Country')['AverageTemperature'].mean().rename('LateMean')

    result = pd.concat([early_avg, late_avg], axis=1).dropna()
    result['Warming'] = result['LateMean'] - result['EarlyMean']
    return result.sort_values('Warming', ascending=False).head(n).reset_index()


def country_yearly_trend(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Annual mean temperature for a single country."""
    sub = df[df['Country'].str.title() == country.title()]
    return (
        sub.groupby('year')['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
    )


def country_monthly_profile(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Monthly climatology (mean temp per calendar month) for a country."""
    sub = df[df['Country'].str.title() == country.title()]
    return (
        sub.groupby('month')['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
    )


def country_decade_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Mean temperature by country × decade (for heat-map)."""
    if 'decade' not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(['Country', 'decade'])['AverageTemperature']
        .mean()
        .unstack('decade')
    )


# ─────────────────────────────────────────────
# City-level analysis
# ─────────────────────────────────────────────

def top_hottest_cities(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """Cities with highest all-time mean temperature."""
    if 'City' not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(['City', 'Country'])['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
        .sort_values('MeanTemp', ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def top_coldest_cities(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """Cities with lowest all-time mean temperature."""
    if 'City' not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby(['City', 'Country'])['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
        .sort_values('MeanTemp')
        .head(n)
        .reset_index(drop=True)
    )


def city_yearly_trend(df: pd.DataFrame, city: str) -> pd.DataFrame:
    """Annual mean temperature for a single city."""
    sub = df[df['City'].str.title() == city.title()]
    return (
        sub.groupby('year')['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
    )


# ─────────────────────────────────────────────
# Distribution helpers
# ─────────────────────────────────────────────

def temperature_distribution(df: pd.DataFrame) -> pd.Series:
    """Return the AverageTemperature column, cleaned."""
    return df['AverageTemperature'].dropna()


def monthly_boxplot_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with month and AverageTemperature for a monthly box-plot."""
    return df[['month', 'AverageTemperature']].dropna()
