"""
Reusable Streamlit UI components for the climate EDA app.
"""
import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# CSS injection (dark glassmorphism theme)
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* ── Root / page ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0E1117 !important;
    font-family: 'Inter', sans-serif;
    color: #E0E0E0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141728 0%, #0E1117 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg,rgba(0,212,255,0.08),rgba(255,107,107,0.06));
    border: 1px solid rgba(0,212,255,0.18);
    border-radius: 14px;
    padding: 16px 20px !important;
    backdrop-filter: blur(10px);
    transition: transform 0.2s;
}
[data-testid="stMetric"]:hover { transform: translateY(-2px); }
[data-testid="stMetricValue"]  { color: #00D4FF !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"]  { color: #A0A0B0 !important; font-size: 0.85rem !important; }
[data-testid="stMetricDelta"]  { font-size: 0.9rem !important; }

/* ── Section header card ── */
.section-header {
    background: linear-gradient(90deg,rgba(0,212,255,0.12) 0%,rgba(255,107,107,0.06) 100%);
    border-left: 4px solid #00D4FF;
    border-radius: 0 10px 10px 0;
    padding: 10px 18px;
    margin: 24px 0 16px 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0.3px;
}

/* ── Info / warning pills ── */
.pill-info  { display:inline-block; background:rgba(0,212,255,0.15);
              border:1px solid rgba(0,212,255,0.35); border-radius:20px;
              padding:3px 14px; font-size:0.82rem; color:#00D4FF; }
.pill-warn  { display:inline-block; background:rgba(255,209,102,0.15);
              border:1px solid rgba(255,209,102,0.35); border-radius:20px;
              padding:3px 14px; font-size:0.82rem; color:#FFD166; }

/* ── Divider ── */
.fancy-divider {
    height:2px;
    background:linear-gradient(90deg,transparent,rgba(0,212,255,0.4),transparent);
    border:none; margin:24px 0;
}

/* ── Tab labels ── */
button[data-baseweb="tab"] { font-size:0.95rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:#00D4FF !important; }

/* ── Data table ── */
[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-thumb { background:#2A2D3E; border-radius:4px; }
</style>
"""


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Individual components
# ─────────────────────────────────────────────────────────────────────────────

def section_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def fancy_divider():
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)


def info_pill(text: str):
    st.markdown(f'<span class="pill-info">{text}</span>', unsafe_allow_html=True)


def warn_pill(text: str):
    st.markdown(f'<span class="pill-warn">{text}</span>', unsafe_allow_html=True)


def metric_row(metrics: list[dict]):
    """
    Render a row of st.metric cards.
    Each dict: {label, value, delta (optional)}
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.metric(
                label=m['label'],
                value=m['value'],
                delta=m.get('delta'),
            )


def hero_banner():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #141728 0%, #1A1D3E 50%, #0E1117 100%);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 18px;
        padding: 36px 40px 28px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position:absolute; top:-60px; right:-60px; width:220px; height:220px;
            background:radial-gradient(circle,rgba(0,212,255,0.15),transparent 70%);
            border-radius:50%;
        "></div>
        <div style="
            position:absolute; bottom:-40px; left:40px; width:160px; height:160px;
            background:radial-gradient(circle,rgba(255,107,107,0.1),transparent 70%);
            border-radius:50%;
        "></div>
        <h1 style="margin:0 0 8px; font-size:2.2rem; font-weight:700;
                   background:linear-gradient(90deg,#00D4FF,#74B9FF);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            🌡️ Global Temperature Explorer
        </h1>
        <p style="margin:0; color:#A0A0C0; font-size:1rem; max-width:600px;">
            Interactive EDA &amp; pattern analysis across global, country, and city-level
            climate records from <strong style="color:#FFD166;">1750 – 2015</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)


def sidebar_nav():
    """Renders sidebar title + returns selected page."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px;">
            <div style="font-size:2.4rem;">🌍</div>
            <div style="font-size:1.1rem; font-weight:700; color:#00D4FF;">Climate EDA</div>
            <div style="font-size:0.75rem; color:#606070;">Global Temperature Analysis</div>
        </div>
        """, unsafe_allow_html=True)

        pages = {
            "🏠  Overview":           "Overview",
            "📊  Global Trends":      "Global Trends",
            "🌏  Country Analysis":   "Country Analysis",
            "🏙️  City Analysis":      "City Analysis",
            "📦  Distributions":      "Distributions",
            "🗺️  World Map":          "World Map",
        }
        choice = st.radio("Navigate", list(pages.keys()), label_visibility="collapsed")
        st.markdown("---")
        st.caption("Data: Berkeley Earth Surface Temp Dataset")
        return pages[choice]
