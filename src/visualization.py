import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── Shared theme ────────────────────────────────────────────────────────────
TEMPLATE   = "plotly_dark"
PRIMARY    = "#00D4FF"
SECONDARY  = "#FF6B6B"
ACCENT     = "#FFD166"
BG_COLOR   = "#0E1117"
PAPER_BG   = "#1A1D2E"
FONT_COLOR = "#E0E0E0"

_layout_defaults = dict(
    template=TEMPLATE,
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=BG_COLOR,
    font=dict(family="Inter, Roboto, sans-serif", color=FONT_COLOR),
    margin=dict(t=60, l=50, r=30, b=50),
)


def _apply(fig, title: str = "", height: int = 420) -> go.Figure:
    fig.update_layout(title=dict(text=title, font=dict(size=17, color=PRIMARY)),
                      height=height, **_layout_defaults)
    return fig


# ── Global trend line ────────────────────────────────────────────────────────

def plot_global_trend(df: pd.DataFrame) -> go.Figure:
    """Annual mean temperature with a smooth trendline."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'], y=df['MeanTemp'],
        mode='lines', name='Annual Mean',
        line=dict(color=PRIMARY, width=2),
    ))
    # rolling 10-yr average
    rolling = df['MeanTemp'].rolling(10, center=True).mean()
    fig.add_trace(go.Scatter(
        x=df['year'], y=rolling,
        mode='lines', name='10-yr Rolling Avg',
        line=dict(color=ACCENT, width=3, dash='dot'),
    ))
    return _apply(fig, "🌍  Global Land Temperature Trend (Annual)", height=430)


# ── Seasonal trend ───────────────────────────────────────────────────────────

def plot_seasonal_trend(df: pd.DataFrame) -> go.Figure:
    """Temperature trend split by season."""
    season_colors = {
        'Winter': '#74B9FF', 'Spring': '#55EFC4',
        'Summer': '#FDCB6E', 'Autumn': '#E17055',
    }
    fig = go.Figure()
    for season, grp in df.groupby('season'):
        fig.add_trace(go.Scatter(
            x=grp['year'], y=grp['MeanTemp'],
            mode='lines', name=season,
            line=dict(color=season_colors.get(season, PRIMARY), width=2),
        ))
    return _apply(fig, "🍂  Seasonal Temperature Trends", height=430)


# ── Country bar charts ───────────────────────────────────────────────────────

def plot_top_warming_countries(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of most-warming countries."""
    colors = [f"hsl({int(220 - i*14)},80%,60%)" for i in range(len(df))]
    fig = go.Figure(go.Bar(
        y=df['Country'], x=df['Warming'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(0,0,0,0)', width=0)),
        text=df['Warming'].round(2).astype(str) + ' °C',
        textposition='outside',
    ))
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return _apply(fig, "🔥  Countries with Greatest Temperature Rise", height=480)


def plot_country_trend(df: pd.DataFrame, country: str) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=df['year'], y=df['MeanTemp'],
        mode='lines+markers',
        line=dict(color=PRIMARY, width=2),
        marker=dict(size=4, color=SECONDARY),
    ))
    return _apply(fig, f"📈  {country} — Annual Temperature Trend", height=400)



def plot_country_monthly_profile(df: pd.DataFrame, country: str) -> go.Figure:
    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig = go.Figure(go.Bar(
        x=[MONTHS[m-1] for m in df['month']],
        y=df['MeanTemp'],
        marker=dict(
            color=df['MeanTemp'],
            colorscale='RdBu_r',
            showscale=True,
            colorbar=dict(title='°C'),
        ),
    ))
    return _apply(fig, f"📅  {country} — Monthly Temperature Profile", height=400)

# ── City bar charts ──────────────────────────────────────────────────────────

def plot_hottest_cities(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Bar(
        y=df['City'] + ', ' + df['Country'],
        x=df['MeanTemp'],
        orientation='h',
        marker=dict(color=SECONDARY, opacity=0.85),
        text=df['MeanTemp'].round(1).astype(str) + ' °C',
        textposition='outside',
    ))
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return _apply(fig, "☀️  Hottest Cities (All-time Avg)", height=500)


def plot_coldest_cities(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Bar(
        y=df['City'] + ', ' + df['Country'],
        x=df['MeanTemp'],
        orientation='h',
        marker=dict(color='#74B9FF', opacity=0.85),
        text=df['MeanTemp'].round(1).astype(str) + ' °C',
        textposition='outside',
    ))
    fig.update_layout(yaxis={'categoryorder': 'total descending'})
    return _apply(fig, "❄️  Coldest Cities (All-time Avg)", height=500)


# ── Distribution plots ───────────────────────────────────────────────────────

def plot_temperature_distribution(series: pd.Series, label: str = "") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=series, nbinsx=60, name='Count',
        marker=dict(color=PRIMARY, opacity=0.75, line=dict(color=PAPER_BG, width=0.5)),
    ))
    fig.add_vline(x=series.mean(), line_dash='dash', line_color=ACCENT,
                  annotation_text=f'Mean {series.mean():.1f}°C',
                  annotation_font_color=ACCENT)
    return _apply(fig, f"📊  Temperature Distribution  {label}", height=380)


def plot_monthly_boxplot(df: pd.DataFrame) -> go.Figure:
    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig = go.Figure()
    for m in range(1, 13):
        vals = df[df['month'] == m]['AverageTemperature'].dropna()
        fig.add_trace(go.Box(
            y=vals, name=MONTHS[m-1],
            marker_color=f"hsl({int(m*30)},70%,55%)",
            line_color=FONT_COLOR,
        ))
    return _apply(fig, "📦  Monthly Temperature Distribution (Box-plots)", height=430)


# ── Correlation heatmap ──────────────────────────────────────────────────────

def plot_correlation_heatmap(corr: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale='RdBu_r', zmid=0,
        text=corr.round(2).values,
        texttemplate='%{text}',
        showscale=True,
    ))
    return _apply(fig, "🔗  Correlation Heatmap", height=420)


# ── Geo scatter map ──────────────────────────────────────────────────────────

def plot_temperature_map(df: pd.DataFrame) -> go.Figure:
    """Scatter map coloured by mean temperature per city."""
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        return None

    plot_df = (
        df.groupby(['City', 'Country', 'Latitude', 'Longitude'])['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
        .dropna()
    )
    plot_df['Latitude'] = pd.to_numeric(plot_df['Latitude'], errors='coerce')
    plot_df['Longitude'] = pd.to_numeric(plot_df['Longitude'], errors='coerce')

    plot_df = plot_df.dropna(subset=['Latitude', 'Longitude'])

    fig = px.scatter_mapbox(
        plot_df, lat='Latitude', lon='Longitude',
        color='MeanTemp', size=plot_df['MeanTemp'].clip(lower=1),
        hover_name='City', hover_data={'Country': True, 'MeanTemp': ':.1f'},
        color_continuous_scale='RdBu_r',
        mapbox_style='carto-darkmatter',
        zoom=1,
    )
    fig.update_layout(
        height=520, paper_bgcolor=PAPER_BG,
        font=dict(family="Inter, Roboto, sans-serif", color=FONT_COLOR),
        margin=dict(t=40, l=0, r=0, b=0),
        coloraxis_colorbar=dict(title='°C'),
    )
    return fig


# ── Choropleth map ───────────────────────────────────────────────────────────

def plot_country_choropleth(df: pd.DataFrame) -> go.Figure:
    """World choropleth of mean temperature by country."""
    country_avg = (
        df.groupby('Country')['AverageTemperature']
        .mean()
        .reset_index()
        .rename(columns={'AverageTemperature': 'MeanTemp'})
        .dropna()
    )
    fig = px.choropleth(
        country_avg,
        locations='Country', locationmode='country names',
        color='MeanTemp',
        color_continuous_scale='RdBu_r',
        title='🗺️  World Mean Temperature by Country',
    )
    fig.update_layout(
        height=480, paper_bgcolor=PAPER_BG,
        geo=dict(bgcolor=BG_COLOR, showframe=False, showcoastlines=True,
                 coastlinecolor='#333'),
        font=dict(family="Inter, Roboto, sans-serif", color=FONT_COLOR),
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig
