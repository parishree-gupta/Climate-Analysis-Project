"""
Generates a comprehensive analysis.ipynb for the Global Temperature EDA project.
Run from the project root: python3 scripts/generate_notebook.py
"""
import json, os

NB_PATH = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'analysis.ipynb')

def code(src):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src}

def md(src):
    return {"cell_type":"markdown","metadata":{},"source":src}

# ─────────────────────────────────────────────────────────────────────────────
cells = []

# ── 0. Title ─────────────────────────────────────────────────────────────────
cells.append(md([
    "# 🌡️ Global Temperature EDA\n",
    "> **Dataset:** Berkeley Earth Surface Temperature · 5 CSVs · 1750 – 2015  \n",
    "> **Sections:** Setup → Data Loading → Preprocessing → Missing Values →  \n",
    "> Global Trends → Seasonal Patterns → Country Analysis → City Analysis →  \n",
    "> Distributions → Warming Analysis → Geo-Visualisation\n",
]))

# ── 1. Setup ─────────────────────────────────────────────────────────────────
cells.append(md(["## 1. Setup & Imports"]))
cells.append(code([
    "import sys, os\n",
    "sys.path.insert(0, os.path.abspath('..'))\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.ticker as ticker\n",
    "import seaborn as sns\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Project modules\n",
    "from src.data_loader   import load_dataset\n",
    "from src.preprocessing import preprocess, missing_value_report\n",
    "from src.analysis      import (\n",
    "    summary_stats, correlation_matrix,\n",
    "    global_yearly_trend, global_seasonal_trend,\n",
    "    top_warming_countries, country_yearly_trend, country_monthly_profile,\n",
    "    top_hottest_cities, top_coldest_cities, city_yearly_trend,\n",
    "    temperature_distribution, monthly_boxplot_data,\n",
    ")\n",
    "from src.visualization import (\n",
    "    plot_global_trend, plot_seasonal_trend,\n",
    "    plot_top_warming_countries, plot_country_trend, plot_country_monthly_profile,\n",
    "    plot_hottest_cities, plot_coldest_cities,\n",
    "    plot_temperature_distribution, plot_monthly_boxplot,\n",
    "    plot_correlation_heatmap, plot_temperature_map, plot_country_choropleth,\n",
    ")\n",
    "\n",
    "# Matplotlib dark style\n",
    "plt.rcParams.update({\n",
    "    'figure.facecolor': '#0E1117',\n",
    "    'axes.facecolor':   '#1A1D2E',\n",
    "    'axes.edgecolor':   '#333',\n",
    "    'axes.labelcolor':  '#E0E0E0',\n",
    "    'xtick.color':      '#A0A0B0',\n",
    "    'ytick.color':      '#A0A0B0',\n",
    "    'text.color':       '#E0E0E0',\n",
    "    'grid.color':       '#2A2D3E',\n",
    "    'grid.linestyle':   '--',\n",
    "    'grid.alpha':       0.5,\n",
    "    'figure.dpi':       120,\n",
    "    'font.family':      'sans-serif',\n",
    "})\n",
    "CYAN   = '#00D4FF'\n",
    "RED    = '#FF6B6B'\n",
    "AMBER  = '#FFD166'\n",
    "GREEN  = '#55EFC4'\n",
    "print('✅  All imports successful')\n",
]))

# ── 2. Data Loading ───────────────────────────────────────────────────────────
cells.append(md(["## 2. Data Loading"]))
cells.append(code([
    "# Load and preprocess all datasets\n",
    "print('Loading global temperatures...')\n",
    "g_df  = preprocess(load_dataset('global'))\n",
    "\n",
    "print('Loading country temperatures...')\n",
    "c_df  = preprocess(load_dataset('country'))\n",
    "\n",
    "print('Loading major-city temperatures...')\n",
    "mc_df = preprocess(load_dataset('major_city'))\n",
    "\n",
    "print('Loading state temperatures...')\n",
    "s_df  = preprocess(load_dataset('state'))\n",
    "\n",
    "print('\\n✅  All datasets loaded!')\n",
    "print(f'  Global     : {g_df.shape}')\n",
    "print(f'  Country    : {c_df.shape}')\n",
    "print(f'  Major City : {mc_df.shape}')\n",
    "print(f'  State      : {s_df.shape}')\n",
]))
cells.append(code([
    "# Quick peek at each dataset\n",
    "for name, df in [('Global', g_df), ('Country', c_df), ('Major City', mc_df)]:\n",
    "    print(f'\\n{'─'*60}')\n",
    "    print(f'  {name}  —  columns: {list(df.columns)}')\n",
    "    display(df.head(3))\n",
]))

# ── 3. Preprocessing & Missing Values ────────────────────────────────────────
cells.append(md(["## 3. Preprocessing & Missing Value Audit"]))
cells.append(code([
    "for name, df in [('Global', g_df), ('Country', c_df), ('Major City', mc_df), ('State', s_df)]:\n",
    "    mv = missing_value_report(df)\n",
    "    print(f'\\n── {name} ─────────────────────────────')\n",
    "    if mv.empty:\n",
    "        print('   ✅ No missing values')\n",
    "    else:\n",
    "        display(mv)\n",
]))
cells.append(code([
    "# Visualise missing-value % for major-city dataset\n",
    "mv = missing_value_report(mc_df)\n",
    "if not mv.empty:\n",
    "    fig, ax = plt.subplots(figsize=(7, 3))\n",
    "    mv['Missing %'].plot(kind='barh', ax=ax, color=RED)\n",
    "    ax.set_xlabel('Missing %')\n",
    "    ax.set_title('Missing Values — Major City Dataset', color=CYAN)\n",
    "    plt.tight_layout(); plt.show()\n",
]))

# ── 4. Descriptive Statistics ─────────────────────────────────────────────────
cells.append(md(["## 4. Descriptive Statistics"]))
cells.append(code([
    "print('=== Global Dataset ===')\n",
    "display(summary_stats(g_df))\n",
]))
cells.append(code([
    "print('=== Country Dataset ===')\n",
    "display(summary_stats(c_df))\n",
]))

# ── 5. Global Trend ───────────────────────────────────────────────────────────
cells.append(md(["## 5. Global Land Temperature Trend"]))
cells.append(code([
    "yearly = global_yearly_trend(g_df)\n",
    "rolling = yearly['MeanTemp'].rolling(10, center=True).mean()\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(13, 4))\n",
    "ax.plot(yearly['year'], yearly['MeanTemp'], color=CYAN, lw=1.2, alpha=0.7, label='Annual Mean')\n",
    "ax.plot(yearly['year'], rolling, color=AMBER, lw=2.5, linestyle='--', label='10-yr Rolling Avg')\n",
    "ax.set_title('Global Land Average Temperature (1750–2015)', fontsize=14, color=CYAN)\n",
    "ax.set_xlabel('Year'); ax.set_ylabel('°C')\n",
    "ax.legend(); ax.grid(True)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# Interactive Plotly version\n",
    "plot_global_trend(yearly).show()\n",
]))

# ── 6. Seasonal Patterns ──────────────────────────────────────────────────────
cells.append(md(["## 6. Seasonal Temperature Patterns"]))
cells.append(code([
    "seasonal = global_seasonal_trend(g_df)\n",
    "print(seasonal.head())\n",
]))
cells.append(code([
    "season_palette = {'Winter':'#74B9FF','Spring':'#55EFC4','Summer':'#FDCB6E','Autumn':'#E17055'}\n",
    "fig, ax = plt.subplots(figsize=(13, 4))\n",
    "for season, grp in seasonal.groupby('season'):\n",
    "    ax.plot(grp['year'], grp['MeanTemp'], label=season,\n",
    "            color=season_palette.get(season, CYAN), lw=1.5)\n",
    "ax.set_title('Seasonal Temperature Trends', fontsize=14, color=CYAN)\n",
    "ax.set_xlabel('Year'); ax.set_ylabel('°C')\n",
    "ax.legend(); ax.grid(True)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# Monthly climatology (all global records)\n",
    "monthly_avg = g_df.groupby('month')['AverageTemperature'].mean()\n",
    "MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 4))\n",
    "bars = ax.bar(MONTHS, monthly_avg.values,\n",
    "              color=plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, 12)))\n",
    "ax.set_title('Monthly Mean Temperature (Global)', fontsize=13, color=CYAN)\n",
    "ax.set_ylabel('°C'); ax.grid(axis='y', alpha=0.4)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 7. Correlation ─────────────────────────────────────────────────────────────
cells.append(md(["## 7. Correlation Analysis"]))
cells.append(code([
    "corr = correlation_matrix(g_df)\n",
    "print(corr)\n",
]))
cells.append(code([
    "# Plotly heatmap\n",
    "plot_correlation_heatmap(corr).show()\n",
]))
cells.append(code([
    "# Seaborn version\n",
    "fig, ax = plt.subplots(figsize=(7, 5))\n",
    "sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r',\n",
    "            linewidths=0.5, ax=ax, cbar_kws={'shrink':0.8})\n",
    "ax.set_title('Correlation Matrix — Global Dataset', color=CYAN)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 8. Country Analysis ────────────────────────────────────────────────────────
cells.append(md(["## 8. Country-Level Analysis"]))
cells.append(code([
    "# Top warming countries\n",
    "warming = top_warming_countries(c_df, n=15)\n",
    "display(warming)\n",
]))
cells.append(code([
    "# Bar chart\n",
    "fig, ax = plt.subplots(figsize=(10, 6))\n",
    "colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(warming)))\n",
    "ax.barh(warming['Country'], warming['Warming'], color=colors[::-1])\n",
    "ax.set_title('Countries with Greatest Temperature Rise', fontsize=13, color=CYAN)\n",
    "ax.set_xlabel('Warming (°C)')\n",
    "ax.invert_yaxis(); ax.grid(axis='x', alpha=0.4)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# Plotly interactive\n",
    "plot_top_warming_countries(warming).show()\n",
]))
cells.append(code([
    "# Single-country deep dive — India\n",
    "country = 'India'\n",
    "trend   = country_yearly_trend(c_df, country)\n",
    "profile = country_monthly_profile(c_df, country)\n",
    "\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 4))\n",
    "\n",
    "axes[0].plot(trend['year'], trend['MeanTemp'], color=CYAN, lw=1.8)\n",
    "axes[0].set_title(f'{country} — Annual Trend', color=CYAN)\n",
    "axes[0].set_xlabel('Year'); axes[0].set_ylabel('°C')\n",
    "axes[0].grid(True)\n",
    "\n",
    "MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\n",
    "axes[1].bar([MONTHS[m-1] for m in profile['month']], profile['MeanTemp'],\n",
    "            color=plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, 12)))\n",
    "axes[1].set_title(f'{country} — Monthly Profile', color=CYAN)\n",
    "axes[1].set_ylabel('°C'); axes[1].grid(axis='y', alpha=0.4)\n",
    "\n",
    "plt.suptitle(f'{country} Temperature Analysis', color=AMBER, fontsize=14)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# Compare multiple countries — annual trend overlay\n",
    "compare_countries = ['India', 'Russia', 'Brazil', 'United States', 'Australia']\n",
    "COLORS = [CYAN, RED, AMBER, GREEN, '#B39DDB']\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(13, 5))\n",
    "for country, color in zip(compare_countries, COLORS):\n",
    "    tr = country_yearly_trend(c_df, country)\n",
    "    if not tr.empty:\n",
    "        ax.plot(tr['year'], tr['MeanTemp'].rolling(5).mean(),\n",
    "                label=country, color=color, lw=2)\n",
    "ax.set_title('Country Temperature Comparison (5-yr Smoothed)', fontsize=13, color=CYAN)\n",
    "ax.set_xlabel('Year'); ax.set_ylabel('°C')\n",
    "ax.legend(); ax.grid(True)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# World Choropleth\n",
    "plot_country_choropleth(c_df).show()\n",
]))

# ── 9. City Analysis ──────────────────────────────────────────────────────────
cells.append(md(["## 9. City-Level Analysis"]))
cells.append(code([
    "hottest = top_hottest_cities(mc_df, n=15)\n",
    "coldest = top_coldest_cities(mc_df, n=15)\n",
    "print('Top 15 Hottest Cities:')\n",
    "display(hottest)\n",
    "print('\\nTop 15 Coldest Cities:')\n",
    "display(coldest)\n",
]))
cells.append(code([
    "fig, axes = plt.subplots(1, 2, figsize=(15, 6))\n",
    "\n",
    "axes[0].barh(hottest['City'] + ', ' + hottest['Country'], hottest['MeanTemp'], color=RED, alpha=0.85)\n",
    "axes[0].invert_yaxis()\n",
    "axes[0].set_title('☀️  Hottest Cities', color=CYAN); axes[0].set_xlabel('°C')\n",
    "axes[0].grid(axis='x', alpha=0.4)\n",
    "\n",
    "axes[1].barh(coldest['City'] + ', ' + coldest['Country'], coldest['MeanTemp'], color='#74B9FF', alpha=0.85)\n",
    "axes[1].set_title('❄️  Coldest Cities', color=CYAN); axes[1].set_xlabel('°C')\n",
    "axes[1].grid(axis='x', alpha=0.4)\n",
    "\n",
    "plt.suptitle('City Temperature Rankings', color=AMBER, fontsize=14)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# City trend — Bombay (Mumbai)\n",
    "city   = 'Bombay'\n",
    "c_trend = city_yearly_trend(mc_df, city)\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(12, 4))\n",
    "ax.plot(c_trend['year'], c_trend['MeanTemp'], color=CYAN, lw=1.8)\n",
    "ax.plot(c_trend['year'], c_trend['MeanTemp'].rolling(10).mean(),\n",
    "        color=AMBER, lw=2.5, linestyle='--', label='10-yr Rolling')\n",
    "ax.set_title(f'{city} — Annual Temperature Trend', fontsize=13, color=CYAN)\n",
    "ax.set_xlabel('Year'); ax.set_ylabel('°C')\n",
    "ax.legend(); ax.grid(True)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# City scatter map\n",
    "plot_temperature_map(mc_df).show()\n",
]))

# ── 10. Distributions ─────────────────────────────────────────────────────────
cells.append(md(["## 10. Temperature Distributions"]))
cells.append(code([
    "fig, axes = plt.subplots(1, 3, figsize=(16, 4))\n",
    "\n",
    "datasets_list = [('Global', g_df), ('Country', c_df), ('Major City', mc_df)]\n",
    "for ax, (name, df) in zip(axes, datasets_list):\n",
    "    series = temperature_distribution(df)\n",
    "    ax.hist(series, bins=60, color=CYAN, alpha=0.75, edgecolor='#1A1D2E')\n",
    "    ax.axvline(series.mean(), color=AMBER, linewidth=2, linestyle='--',\n",
    "               label=f'Mean {series.mean():.1f}°C')\n",
    "    ax.set_title(f'{name} Distribution', color=CYAN)\n",
    "    ax.set_xlabel('°C'); ax.legend(); ax.grid(axis='y', alpha=0.4)\n",
    "\n",
    "plt.suptitle('Temperature Distributions', color=AMBER, fontsize=14)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# Monthly box-plot\n",
    "MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\n",
    "mb_data = monthly_boxplot_data(mc_df)\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(13, 5))\n",
    "month_groups = [mb_data[mb_data['month'] == m]['AverageTemperature'].dropna() for m in range(1,13)]\n",
    "bp = ax.boxplot(month_groups, patch_artist=True, labels=MONTHS,\n",
    "                medianprops=dict(color=AMBER, linewidth=2))\n",
    "for patch, color in zip(bp['boxes'],\n",
    "                         plt.cm.RdYlBu_r(np.linspace(0.05, 0.95, 12))):\n",
    "    patch.set_facecolor(color); patch.set_alpha(0.75)\n",
    "ax.set_title('Monthly Temperature Distribution (Major Cities)', fontsize=13, color=CYAN)\n",
    "ax.set_ylabel('°C'); ax.grid(axis='y', alpha=0.4)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 11. Warming Analysis ──────────────────────────────────────────────────────
cells.append(md(["## 11. Warming Analysis — Pre vs Post 1950"]))
cells.append(code([
    "# Split era: pre vs post-1950\n",
    "pre  = c_df[c_df['year'] < 1950]\n",
    "post = c_df[c_df['year'] >= 1950]\n",
    "\n",
    "pre_mean  = pre.groupby('Country')['AverageTemperature'].mean().rename('Pre_1950')\n",
    "post_mean = post.groupby('Country')['AverageTemperature'].mean().rename('Post_1950')\n",
    "\n",
    "era_df = pd.concat([pre_mean, post_mean], axis=1).dropna()\n",
    "era_df['Warming'] = era_df['Post_1950'] - era_df['Pre_1950']\n",
    "era_df = era_df.sort_values('Warming', ascending=False)\n",
    "\n",
    "print('Countries that warmed the most (Pre vs Post 1950):')\n",
    "display(era_df.head(15))\n",
]))
cells.append(code([
    "fig, ax = plt.subplots(figsize=(11, 5))\n",
    "top15 = era_df.head(15)\n",
    "colors = plt.cm.Reds(np.linspace(0.4, 0.9, 15))\n",
    "ax.barh(top15.index, top15['Warming'], color=colors[::-1])\n",
    "ax.set_title('Temperature Increase: Post-1950 vs Pre-1950 (Top 15)', fontsize=13, color=CYAN)\n",
    "ax.set_xlabel('Warming (°C)')\n",
    "ax.invert_yaxis(); ax.grid(axis='x', alpha=0.4)\n",
    "plt.tight_layout(); plt.show()\n",
]))
cells.append(code([
    "# Global annual mean — decade-level trend\n",
    "decade_avg = g_df.groupby('decade')['AverageTemperature'].mean()\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(11, 4))\n",
    "ax.bar(decade_avg.index, decade_avg.values, width=8,\n",
    "       color=plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, len(decade_avg))),\n",
    "       edgecolor='#1A1D2E')\n",
    "ax.set_title('Global Mean Temperature by Decade', fontsize=13, color=CYAN)\n",
    "ax.set_xlabel('Decade'); ax.set_ylabel('°C')\n",
    "ax.grid(axis='y', alpha=0.4)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 12. State Analysis ────────────────────────────────────────────────────────
cells.append(md(["## 12. US State-Level Patterns"]))
cells.append(code([
    "us_states = s_df[s_df['Country'] == 'United States']\n",
    "if not us_states.empty:\n",
    "    state_avg = us_states.groupby('State')['AverageTemperature'].mean().dropna().sort_values(ascending=False)\n",
    "    print(f'{len(state_avg)} US states found')\n",
    "    display(state_avg.head(10))\n",
]))
cells.append(code([
    "if not us_states.empty:\n",
    "    top_n  = state_avg.head(10)\n",
    "    bot_n  = state_avg.tail(10)\n",
    "\n",
    "    fig, axes = plt.subplots(1, 2, figsize=(15, 5))\n",
    "    axes[0].barh(top_n.index, top_n.values, color=RED, alpha=0.85)\n",
    "    axes[0].invert_yaxis()\n",
    "    axes[0].set_title('Hottest US States', color=CYAN); axes[0].set_xlabel('°C')\n",
    "    axes[0].grid(axis='x', alpha=0.4)\n",
    "\n",
    "    axes[1].barh(bot_n.index, bot_n.values, color='#74B9FF', alpha=0.85)\n",
    "    axes[1].set_title('Coldest US States', color=CYAN); axes[1].set_xlabel('°C')\n",
    "    axes[1].grid(axis='x', alpha=0.4)\n",
    "\n",
    "    plt.suptitle('US State Temperature Rankings', color=AMBER, fontsize=14)\n",
    "    plt.tight_layout(); plt.show()\n",
]))

# ── 13. Key Takeaways ─────────────────────────────────────────────────────────
cells.append(md([
    "## 13. 📝 Key Takeaways\n\n",
    "| Finding | Detail |\n",
    "|---------|--------|\n",
    "| **Global warming trend** | Clear upward trend from ~1850, accelerating post-1950 |\n",
    "| **Hottest decade** | 2000s consistently the warmest on record |\n",
    "| **Seasonal spread** | Summer–Winter gap has narrowed slightly in many regions |\n",
    "| **Most-warming countries** | Arctic/sub-arctic nations show greatest rise (Russia, Canada, etc.) |\n",
    "| **Hottest cities** | Equatorial/desert cities (Djibouti, Niamey, etc.) |\n",
    "| **Coldest cities** | High-latitude Siberian & Canadian cities |\n",
    "| **Data coverage** | Pre-1850 records are sparse; uncertainty is higher |\n",
    "| **Missing data** | Temperature uncertainty columns have the most gaps |\n",
]))

# ── Build notebook JSON ───────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
        "language_info": {"name":"python","version":"3.9.0"},
    },
    "cells": cells,
}

os.makedirs(os.path.dirname(NB_PATH), exist_ok=True)
with open(NB_PATH, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f'✅  Notebook written → {NB_PATH}')
print(f'   Total cells: {len(cells)}')
