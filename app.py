
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import html

# =====================================================
# 1. PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="BFSI | Fraud Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BLACK = "#0a0a0a"
BLUE = "#007ba7"
ROSE = "#ff2d95"
CYAN = "#00c8f8"
WHITE = "#f5f9ff"
MUTED = "#91a6b9"

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "reports" / "simulated_fraud_alerts.csv"

# =====================================================
# 2. PREMIUM CSS THEME
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --black: #0a0a0a;
    --blue: #007ba7;
    --rose: #ff2d95;
    --cyan: #00c8f8;
    --white: #f5f9ff;
}

html, body, [data-testid="stApp"],
[data-testid="stMain"] {
    background: #0a0a0a !important;
    color: #f5f9ff !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stHeader"] {
    background: rgba(10,10,10,0.92) !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1600px !important;
}

h1, h2, h3, p {
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0d1520 !important;
    border-right: 1px solid #ff2d95;
}

#MainMenu, footer {
    visibility: hidden;
}

/* Header */

.hero {
    position: relative;
    overflow: hidden;
    background:
      radial-gradient(
        ellipse at 80% 10%,
        rgba(255,45,149,0.11),
        transparent 38%
      ),
      radial-gradient(
        ellipse at 15% 80%,
        rgba(0,123,167,0.16),
        transparent 45%
      ),
      #0b1017;
    border: 1px solid rgba(0,200,248,0.40);
    border-radius: 20px;
    padding: 27px 30px;
    margin-bottom: 22px;
    box-shadow:
      0 12px 40px rgba(0,0,0,0.35),
      inset 0 1px 0 rgba(255,255,255,0.04);
}

.hero::after {
    content: "";
    position: absolute;
    right: -70px;
    top: -110px;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    border: 1px solid rgba(255,45,149,0.14);
    box-shadow:
      0 0 0 38px rgba(0,123,167,0.025),
      0 0 0 85px rgba(255,45,149,0.018);
    pointer-events: none;
}

.hero-title {
    color: #f5f9ff;
    font-size: clamp(25px, 2.6vw, 40px);
    font-weight: 850;
    letter-spacing: -1.2px;
    margin: 0;
}

.hero-title .brand {
    color: #00c8f8;
}

.hero-title .separator {
    color: #ff2d95;
}

.hero-subtitle {
    color: #91a6b9;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    margin-top: 11px;
}

.status-pill {
    display: inline-block;
    color: #00c8f8;
    background: rgba(0,123,167,0.12);
    border: 1px solid rgba(0,200,248,0.35);
    border-radius: 999px;
    padding: 8px 13px;
    margin-top: 18px;
    font-size: 11px;
    font-weight: 700;
}

.status-dot {
    color: #3af5ae;
}

/* KPI Cards */

.kpi-card {
    position: relative;
    overflow: hidden;
    min-height: 145px;
    background:
      linear-gradient(
        135deg,
        rgba(0,123,167,0.22),
        rgba(11,20,32,0.98) 70%
      );
    border: 1px solid rgba(0,200,248,0.50);
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow:
      0 8px 26px rgba(0,0,0,0.35),
      0 0 14px rgba(0,123,167,0.08);
}

.kpi-card::before {
    content: "";
    position: absolute;
    height: 3px;
    top: 0;
    left: 15px;
    right: 15px;
    background: linear-gradient(
        90deg, #00c8f8, #007ba7, #ff2d95
    );
    border-radius: 20px;
}

.kpi-icon {
    font-size: 23px;
    margin-bottom: 12px;
}

.kpi-label {
    color: #00c8f8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.kpi-value {
    color: #ffffff;
    font-size: clamp(26px, 2.7vw, 38px);
    font-weight: 850;
    margin: 8px 0;
    letter-spacing: -1px;
}

.kpi-note {
    color: #91a6b9;
    font-size: 11px;
}

/* Section titles */

.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #f5f9ff;
    font-size: 18px;
    font-weight: 800;
    margin: 20px 0 12px;
}

.section-heading .symbol {
    color: #ff2d95;
}

.neon-divider {
    height: 1px;
    margin: 19px 0 15px;
    background: linear-gradient(
      90deg,
      transparent,
      #ff2d95,
      #007ba7,
      transparent
    );
    box-shadow: 0 0 9px rgba(255,45,149,0.25);
}

/* Plotly chart containers */

[data-testid="stPlotlyChart"] {
    background: #0c121a;
    border: 1px solid rgba(0,200,248,0.38);
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.28);
}

/* Filters */

[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #101b28 !important;
    color: #ffffff !important;
    border-color: rgba(0,200,248,0.45) !important;
    border-radius: 10px !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #ff2d95 !important;
    box-shadow: 0 0 0 1px #ff2d95 !important;
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,200,248,0.55);
    border-radius: 14px;
    overflow: hidden;
}

/* Buttons */

.stDownloadButton button {
    background: linear-gradient(
        100deg, #007ba7, #005c85
    ) !important;
    color: #ffffff !important;
    border: 1px solid #ff2d95 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px;
    box-shadow: 0 0 15px rgba(0,123,167,0.20);
}

.stDownloadButton button:hover {
    border-color: #00c8f8 !important;
    box-shadow: 0 0 18px rgba(255,45,149,0.28);
}

/* Info */

[data-testid="stAlert"] {
    background: #0c1b28 !important;
    border: 1px solid rgba(255,45,149,0.50) !important;
    border-radius: 12px;
}

.footer-line {
    text-align: center;
    padding: 24px 8px 10px;
    color: #ff2d95;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.footer-sub {
    color: #91a6b9;
    font-size: 10px;
    letter-spacing: 1px;
    margin-top: 8px;
}

/* Responsive */

@media (max-width: 768px) {
    .hero { padding: 20px; }
    .hero-title { font-size: 26px; }
    .kpi-card { min-height: 125px; }
    .hero-subtitle { letter-spacing: 1px; }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. DATA LOADING
# =====================================================

@st.cache_data
def load_data(path, modified_time):
    return pd.read_csv(path)

if not CSV_FILE.exists():
    st.error(
        "Alert CSV not found. "
        "Run src/realtime_fraud_simulator.py first."
    )
    st.stop()

df = load_data(
    str(CSV_FILE),
    CSV_FILE.stat().st_mtime
)

required_cols = [
    "risk_score",
    "risk_level",
    "actual_is_fraud"
]

missing = [
    col for col in required_cols
    if col not in df.columns
]

if missing:
    st.error(f"Missing CSV columns: {missing}")
    st.stop()

if df.empty:
    st.warning("No fraud alerts available.")
    st.stop()

df["risk_score"] = pd.to_numeric(
    df["risk_score"], errors="coerce"
).fillna(0)

df["actual_is_fraud"] = pd.to_numeric(
    df["actual_is_fraud"], errors="coerce"
).fillna(0).astype(int)

if "amount_usd" in df.columns:
    df["amount_usd"] = pd.to_numeric(
        df["amount_usd"], errors="coerce"
    )

# =====================================================
# 4. HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        🛡️ <span class="brand">BFSI</span>
        <span class="separator">|</span>
        Fraud Alert Monitoring
    </div>
    <div class="hero-subtitle">
        HISTORICAL FRAUD SIMULATION
        &nbsp; | &nbsp;
        RISK INTELLIGENCE DASHBOARD
    </div>
    <div class="status-pill">
        <span class="status-dot">●</span>
        DASHBOARD ONLINE
        &nbsp; • &nbsp;
        HISTORICAL DATA REPLAY
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 5. KPI METRICS
# =====================================================

total_alerts = len(df)
high_alerts = int((df["risk_score"] >= 70).sum())
medium_alerts = int(
    df["risk_score"].between(40, 69).sum()
)

actual_fraud = int(df["actual_is_fraud"].sum())
false_alerts = total_alerts - actual_fraud

precision = (
    actual_fraud / total_alerts * 100
    if total_alerts else 0
)

def kpi_card(icon, label, value, note):
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        kpi_card(
            "📋",
            "TOTAL ALERTS",
            f"{total_alerts:,}",
            "Flagged transactions"
        ),
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        kpi_card(
            "⚠️",
            "HIGH RISK ALERTS",
            f"{high_alerts:,}",
            "Priority investigation queue"
        ),
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        kpi_card(
            "🛡️",
            "ACTUAL FRAUD",
            f"{actual_fraud:,}",
            "Dataset-labeled fraud"
        ),
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        kpi_card(
            "🎯",
            "ALERT PRECISION",
            f"{precision:.2f}%",
            "Of generated alerts"
        ),
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="neon-divider"></div>',
    unsafe_allow_html=True
)

# =====================================================
# 6. CHARTS
# =====================================================

left, right = st.columns(2, gap="medium")

with left:

    risk_data = pd.DataFrame({
        "Risk Level": ["Medium", "High"],
        "Alerts": [medium_alerts, high_alerts]
    })

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=risk_data["Risk Level"],
            y=risk_data["Alerts"],
            marker=dict(
                color=BLUE,
                line=dict(
                    color=CYAN,
                    width=1.5
                )
            ),
            text=risk_data["Alerts"],
            textposition="outside",
            textfont=dict(
                color=WHITE,
                size=14
            ),
            width=0.55,
            hovertemplate=(
                "%{x}<br>"
                "Alerts: %{y}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=dict(
            text="▥  Alerts by Risk Level",
            font=dict(color=WHITE, size=17)
        ),
        paper_bgcolor="#0c121a",
        plot_bgcolor="#0c121a",
        font=dict(color=WHITE),
        height=360,
        margin=dict(l=30, r=25, t=65, b=45),
        showlegend=False,
        xaxis=dict(
            title="Risk Level",
            showgrid=False,
            linecolor=ROSE,
            tickfont=dict(color=WHITE)
        ),
        yaxis=dict(
            title="Number of Alerts",
            rangemode="tozero",
            gridcolor="rgba(255,45,149,0.20)",
            zerolinecolor=ROSE,
            dtick=2
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with right:

    fig2 = go.Figure()

    fig2.add_trace(
        go.Pie(
            labels=["Actual Fraud", "False Alert"],
            values=[actual_fraud, false_alerts],
            hole=0.65,
            marker=dict(
                colors=[BLUE, ROSE],
                line=dict(
                    color="#0c121a",
                    width=4
                )
            ),
            textinfo="percent",
            textfont=dict(
                size=14,
                color=WHITE
            ),
            hovertemplate=(
                "%{label}: %{value}"
                "<br>%{percent}<extra></extra>"
            )
        )
    )

    fig2.update_layout(
        title=dict(
            text="◉  Fraud Alert Outcomes",
            font=dict(color=WHITE, size=17)
        ),
        paper_bgcolor="#0c121a",
        plot_bgcolor="#0c121a",
        font=dict(color=WHITE),
        height=360,
        margin=dict(l=15, r=15, t=65, b=30),
        legend=dict(
            orientation="h",
            y=-0.1,
            x=0.5,
            xanchor="center",
            font=dict(color=WHITE)
        ),
        annotations=[
            dict(
                text=(
                    f"<b>{total_alerts}</b>"
                    "<br><span style='font-size:11px'>"
                    "TOTAL ALERTS</span>"
                ),
                x=0.5,
                y=0.5,
                font=dict(
                    size=24,
                    color=CYAN
                ),
                showarrow=False
            )
        ]
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.markdown(
    '<div class="neon-divider"></div>',
    unsafe_allow_html=True
)

# =====================================================
# 7. TRANSACTION TABLE & FILTERS
# =====================================================

st.markdown(
    """
    <div class="section-heading">
        <span class="symbol">▤</span>
        Transaction Alert Details
    </div>
    """,
    unsafe_allow_html=True
)

search_col, filter_col = st.columns([3, 1])

with search_col:
    search = st.text_input(
        "Search alerts",
        placeholder="Search merchant, risk level, status...",
        label_visibility="collapsed"
    )

with filter_col:
    selected_risk = st.selectbox(
        "Risk Level",
        ["All Risk Levels", "High", "Medium"],
        label_visibility="collapsed"
    )

filtered = df.copy()

if selected_risk != "All Risk Levels":
    filtered = filtered[
        filtered["risk_level"].astype(str).str.lower()
        == selected_risk.lower()
    ]

if search.strip():
    searchable = [
        col for col in [
            "merchant",
            "risk_level",
            "alert_status",
            "priority"
        ]
        if col in filtered.columns
    ]

    if searchable:
        mask = (
            filtered[searchable]
            .astype(str)
            .apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    regex=False,
                    na=False
                )
            )
            .any(axis=1)
        )
        filtered = filtered[mask]

# Table styling
def style_alerts(row):
    if row["risk_score"] >= 70:
        return [
            "background-color: #25111e; "
            "color: #ff9acb;"
        ] * len(row)

    return [
        "background-color: #0c2331; "
        "color: #d7f4ff;"
    ] * len(row)

display_df = filtered.copy()

if "amount_usd" in display_df.columns:
    display_df["amount_usd"] = (
        display_df["amount_usd"].round(2)
    )

styled = display_df.style.apply(
    style_alerts,
    axis=1
)

st.dataframe(
    styled,
    use_container_width=True,
    hide_index=True,
    height=360
)

st.caption(
    f"Showing {len(filtered)} of "
    f"{len(df)} generated alerts"
)

# =====================================================
# 8. DOWNLOAD
# =====================================================

st.download_button(
    label="⬇  DOWNLOAD FRAUD ALERTS CSV",
    data=filtered.to_csv(index=False),
    file_name="bfsi_fraud_alerts.csv",
    mime="text/csv",
    use_container_width=False
)

# =====================================================
# 9. DISCLAIMER & FOOTER
# =====================================================

st.info(
    "Historical transaction simulation using a "
    "deliberately stratified sample. "
    "The displayed alert precision is not an "
    "estimate of production performance."
)

st.markdown("""
<div class="footer-line">
    BFSI FRAUD RISK ANALYTICS
    <div class="footer-sub">
        PYTHON &nbsp; • &nbsp;
        MYSQL &nbsp; • &nbsp;
        POWER BI &nbsp; • &nbsp;
        STREAMLIT
        <br><br>
        DETECT &nbsp; • &nbsp;
        ANALYZE &nbsp; • &nbsp;
        PREVENT
    </div>
</div>
""", unsafe_allow_html=True)
