"""
Main Streamlit application — Global Temperature EDA Explorer.
Run:  streamlit run app/app.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd

# ── Project modules ─────────────────────────────────────────────────────────
from src.data_loader   import load_dataset
from src.preprocessing import preprocess, missing_value_report
from src.analysis      import (
    summary_stats, correlation_matrix,
    global_yearly_trend, global_seasonal_trend,
    top_warming_countries, country_yearly_trend, country_monthly_profile,
    top_hottest_cities, top_coldest_cities, city_yearly_trend,
    temperature_distribution, monthly_boxplot_data,
)
from src.visualization import (
    plot_global_trend, plot_seasonal_trend,
    plot_top_warming_countries, plot_country_trend, plot_country_monthly_profile,
    plot_hottest_cities, plot_coldest_cities,
    plot_temperature_distribution, plot_monthly_boxplot,
    plot_correlation_heatmap, plot_temperature_map, plot_country_choropleth,
)
from app.components import (
    inject_css, hero_banner, sidebar_nav,
    section_header, fancy_divider, metric_row, info_pill, warn_pill,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Temperature Explorer",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Cached data loaders ──────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def get_global():
    df = load_dataset('global')
    return preprocess(df)

@st.cache_data(show_spinner=False)
def get_country():
    df = load_dataset('country')
    return preprocess(df)

@st.cache_data(show_spinner=False)
def get_major_city():
    df = load_dataset('major_city')
    return preprocess(df)

@st.cache_data(show_spinner=False)
def get_city_sample(n: int = 400_000):
    df = load_dataset('city', nrows=n)
    return preprocess(df)

# ── Navigation ───────────────────────────────────────────────────────────────

page = sidebar_nav()
hero_banner()

# ════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════

if page == "Overview":
    with st.spinner("Loading datasets…"):
        g_df  = get_global()
        c_df  = get_country()
        mc_df = get_major_city()

    # ── KPI Metrics ──────────────────────────────────────────────────────────
    section_header("📋  Dataset Overview")

    metric_row([
        {"label": "📅 Date Range (Global)",
         "value": f"{int(g_df['year'].min())} – {int(g_df['year'].max())}"},
        {"label": "🌍 Countries",
         "value": f"{c_df['Country'].nunique():,}"},
        {"label": "🏙️ Major Cities",
         "value": f"{mc_df['City'].nunique():,}"},
        {"label": "🌡️ Global Mean Temp",
         "value": f"{g_df['AverageTemperature'].mean():.2f} °C"},
        {"label": "📈 Hottest Year",
         "value": str(int(
             g_df.groupby('year')['AverageTemperature'].mean().idxmax()
         ))},
    ])

    fancy_divider()

    # ── Dataset previews ──────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🌍 Global", "🌏 By Country", "🏙️ Major Cities"])

    with tab1:
        section_header("Global Temperatures — Sample")
        st.dataframe(g_df.head(200), use_container_width=True, height=320)
        section_header("Missing Values")
        mv = missing_value_report(g_df)
        if mv.empty:
            info_pill("✅  No missing values in Global dataset")
        else:
            st.dataframe(mv, use_container_width=True)

    with tab2:
        section_header("Country Temperatures — Sample")
        st.dataframe(c_df.head(200), use_container_width=True, height=320)
        section_header("Missing Values")
        mv = missing_value_report(c_df)
        if mv.empty:
            info_pill("✅  No missing values")
        else:
            st.dataframe(mv, use_container_width=True)

    with tab3:
        section_header("Major City Temperatures — Sample")
        st.dataframe(mc_df.head(200), use_container_width=True, height=320)
        section_header("Missing Values")
        mv = missing_value_report(mc_df)
        if mv.empty:
            info_pill("✅  No missing values")
        else:
            st.dataframe(mv, use_container_width=True)

    fancy_divider()

    # ── Summary stats ─────────────────────────────────────────────────────────
    section_header("📊  Descriptive Statistics — Global Dataset")
    st.dataframe(summary_stats(g_df), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: GLOBAL TRENDS
# ════════════════════════════════════════════════════════════════════════════

elif page == "Global Trends":
    with st.spinner("Loading global data…"):
        g_df = get_global()

    section_header("🌍  Global Land Temperature Trends")

    # Year range filter
    yr_min, yr_max = int(g_df['year'].min()), int(g_df['year'].max())
    y1, y2 = st.slider("Year range", yr_min, yr_max, (yr_min, yr_max))
    g_filtered = g_df[(g_df['year'] >= y1) & (g_df['year'] <= y2)]

    yearly = global_yearly_trend(g_filtered)
    st.plotly_chart(plot_global_trend(yearly), use_container_width=True)

    fancy_divider()

    col1, col2 = st.columns(2)
    with col1:
        section_header("🍂  Seasonal Trends")
        seasonal = global_seasonal_trend(g_filtered)
        if not seasonal.empty:
            st.plotly_chart(plot_seasonal_trend(seasonal), use_container_width=True)
        else:
            warn_pill("Season data unavailable for this dataset.")

    with col2:
        section_header("📦  Monthly Distribution")
        mb_data = monthly_boxplot_data(g_filtered)
        st.plotly_chart(plot_monthly_boxplot(mb_data), use_container_width=True)

    fancy_divider()

    section_header("🔗  Correlation Matrix")
    corr = correlation_matrix(g_filtered)
    st.plotly_chart(plot_correlation_heatmap(corr), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: COUNTRY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════

elif page == "Country Analysis":
    with st.spinner("Loading country data…"):
        c_df = get_country()

    # ── Top warming countries ─────────────────────────────────────────────────
    section_header("🔥  Countries with Greatest Warming")
    n_countries = st.slider("How many countries to show?", 5, 30, 15)
    warming_df = top_warming_countries(c_df, n=n_countries)
    if not warming_df.empty:
        st.plotly_chart(plot_top_warming_countries(warming_df), use_container_width=True)

    fancy_divider()

    # ── Single-country deep-dive ──────────────────────────────────────────────
    section_header("🔍  Country Deep-Dive")
    all_countries = sorted(c_df['Country'].dropna().unique().tolist())
    selected_country = st.selectbox("Select a country", all_countries,
                                     index=all_countries.index('India') if 'India' in all_countries else 0)

    col1, col2 = st.columns(2)
    with col1:
        trend = country_yearly_trend(c_df, selected_country)
        st.plotly_chart(plot_country_trend(trend, selected_country), use_container_width=True)
    with col2:
        profile = country_monthly_profile(c_df, selected_country)
        st.plotly_chart(plot_country_monthly_profile(profile, selected_country), use_container_width=True)

    fancy_divider()

    # ── Choropleth ────────────────────────────────────────────────────────────
    section_header("🗺️  Global Temperature Choropleth")
    st.plotly_chart(plot_country_choropleth(c_df), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: CITY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════

elif page == "City Analysis":
    with st.spinner("Loading major-city data…"):
        mc_df = get_major_city()

    tab1, tab2 = st.tabs(["🏆  Top / Bottom Cities", "🔍  City Deep-Dive"])

    with tab1:
        col1, col2 = st.columns(2)
        n_cities = st.slider("How many cities?", 5, 30, 15)
        with col1:
            hot = top_hottest_cities(mc_df, n=n_cities)
            st.plotly_chart(plot_hottest_cities(hot), use_container_width=True)
        with col2:
            cold = top_coldest_cities(mc_df, n=n_cities)
            st.plotly_chart(plot_coldest_cities(cold), use_container_width=True)

    with tab2:
        all_cities = sorted(mc_df['City'].dropna().unique().tolist())
        selected_city = st.selectbox("Select a city", all_cities,
                                      index=all_cities.index('Mumbai') if 'Mumbai' in all_cities
                                            else all_cities.index('Bombay') if 'Bombay' in all_cities
                                            else 0)
        trend = city_yearly_trend(mc_df, selected_city)
        if not trend.empty:
            fig = plot_country_trend(trend, selected_city)
            fig.update_layout(title=f"📈  {selected_city} — Annual Temperature Trend")
            st.plotly_chart(fig, use_container_width=True)
        else:
            warn_pill(f"No data found for {selected_city}")

        # Monthly box-plot for selected city
        section_header(f"📦  {selected_city} — Monthly Distribution")
        city_data = mc_df[mc_df['City'].str.title() == selected_city.title()]
        mb = monthly_boxplot_data(city_data)
        if not mb.empty:
            st.plotly_chart(plot_monthly_boxplot(mb), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: DISTRIBUTIONS
# ════════════════════════════════════════════════════════════════════════════

elif page == "Distributions":
    with st.spinner("Loading data…"):
        g_df  = get_global()
        c_df  = get_country()
        mc_df = get_major_city()

    section_header("📊  Temperature Distributions")

    col1, col2 = st.columns(2)
    with col1:
        series = temperature_distribution(g_df)
        st.plotly_chart(plot_temperature_distribution(series, "(Global)"), use_container_width=True)
    with col2:
        series = temperature_distribution(c_df)
        st.plotly_chart(plot_temperature_distribution(series, "(All Countries)"), use_container_width=True)

    fancy_divider()

    section_header("📦  Monthly Box-plots  (Major Cities)")
    st.plotly_chart(plot_monthly_boxplot(monthly_boxplot_data(mc_df)), use_container_width=True)

    fancy_divider()

    section_header("📊  Descriptive Statistics")
    dataset_choice = st.radio("Dataset", ["Global", "Country", "Major City"], horizontal=True)
    df_map = {"Global": g_df, "Country": c_df, "Major City": mc_df}
    st.dataframe(summary_stats(df_map[dataset_choice]), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: WORLD MAP
# ════════════════════════════════════════════════════════════════════════════

elif page == "World Map":
    with st.spinner("Loading map data (this may take a moment)…"):
        mc_df = get_major_city()

    section_header("🗺️  Interactive Temperature Map — Major Cities")
    info_pill("Colour & size = all-time mean temperature per city")
    st.markdown("")

    map_fig = plot_temperature_map(mc_df)
    if map_fig:
        st.plotly_chart(map_fig, use_container_width=True)
    else:
        warn_pill("Latitude / Longitude columns not found in dataset.")

    fancy_divider()

    section_header("🌍  World Choropleth — Country Averages")
    with st.spinner("Building choropleth…"):
        c_df = get_country()
    st.plotly_chart(plot_country_choropleth(c_df), use_container_width=True)
