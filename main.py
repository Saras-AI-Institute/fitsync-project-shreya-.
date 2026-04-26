# import streamlit as st

# st.set_page_config(layout="wide", page_title="FitSync")

# st.title("Welcome to FitSync")
# st.write("Your personal health analytics dashboard")
# st.write("Use the sidebar to navigate between pages")


import streamlit as st
from modules.proccessor import process_data
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="FitSync", page_icon="💚")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a0a0a !important;
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
}
[data-testid="stSidebar"] { background-color: #0e0e0e !important; }
.block-container { padding: 2.5rem 3rem !important; max-width: 1200px; }

/* ── Hero ── */
.hero-tag {
    display: inline-flex; align-items: center; gap: 6px;
    background: #111; border: 1px solid #222; border-radius: 6px;
    padding: 5px 12px; font-size: 11px; color: #666;
    font-family: 'IBM Plex Mono', monospace; letter-spacing: 0.5px;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 700; letter-spacing: -2px; line-height: 1.05;
    margin: 0.5rem 0 1rem;
}
.hero-title .accent {
    background: linear-gradient(90deg, #00ff88, #00ccff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-size: 16px; color: #666; max-width: 540px;
    line-height: 1.7; font-weight: 400; margin-bottom: 2.5rem;
}
.status-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: #111; border: 1px solid #1a1a1a;
    border-radius: 20px; padding: 6px 14px;
    font-size: 12px; color: #888;
    font-family: 'IBM Plex Mono', monospace;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #00ff88; box-shadow: 0 0 6px #00ff88;
    animation: pulse 2s infinite; display: inline-block;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.35} }

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 2rem; }
.kpi {
    background: #0f0f0f; border: 1px solid #1a1a1a;
    border-radius: 14px; padding: 1.2rem 1.4rem;
    position: relative; overflow: hidden;
    transition: border-color .2s, transform .15s;
}
.kpi:hover { border-color: #333; transform: translateY(-2px); }
.kpi::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; border-radius: 2px 2px 0 0;
}
.kpi.green::after  { background: linear-gradient(90deg,#00ff88,transparent); }
.kpi.blue::after   { background: linear-gradient(90deg,#00ccff,transparent); }
.kpi.amber::after  { background: linear-gradient(90deg,#ffaa00,transparent); }
.kpi.red::after    { background: linear-gradient(90deg,#ff4466,transparent); }
.kpi-label {
    font-size: 11px; color: #555; font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px;
}
.kpi-val { font-size: 28px; font-weight: 700; letter-spacing: -1px; line-height: 1; }
.kpi-val.green { color: #00ff88; }
.kpi-val.blue  { color: #00ccff; }
.kpi-val.amber { color: #ffaa00; }
.kpi-val.red   { color: #ff4466; }
.kpi-delta { font-size: 12px; color: #444; margin-top: 5px; font-family: 'IBM Plex Mono', monospace; }
.kpi-delta .up   { color: #00ff88; }
.kpi-delta .down { color: #ff4466; }

/* ── Bottom cards ── */
.bottom-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 12px; }
.card {
    background: #0f0f0f; border: 1px solid #1a1a1a;
    border-radius: 14px; padding: 1.4rem;
}
.card-label {
    font-size: 11px; color: #555; font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 1rem;
}
.bar-chart { display: flex; align-items: flex-end; gap: 6px; height: 80px; }
.bar {
    flex: 1; border-radius: 3px 3px 0 0;
    transition: opacity .2s; opacity: 0.85;
}
.bar:hover { opacity: 1; }
.week-dots { display: flex; gap: 6px; margin-top: 8px; }
.wd { flex: 1; height: 6px; border-radius: 3px; background: #1a1a1a; }
.wd.g { background: #00ff88; }
.wd.b { background: #00ccff; }
.wd.a { background: #ffaa00; }

/* ── Nav items ── */
.nav-item {
    display: flex; align-items: center; justify-content: space-between;
    background: #151515; border: 1px solid #1e1e1e;
    border-radius: 10px; padding: 12px 14px;
    margin-bottom: 10px; cursor: pointer;
    transition: background .2s, border-color .2s;
}
.nav-item:hover { background: #1a1a1a; border-color: #333; }
.nav-dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 10px; display: inline-block; }
.nav-title { font-size: 14px; font-weight: 500; }
.nav-sub { font-size: 12px; color: #555; margin-top: 1px; }

/* ── Divider ── */
.divider { height: 1px; background: #1a1a1a; margin: 2rem 0; }
.footer { font-size: 12px; color: #444; font-family: 'IBM Plex Mono', monospace; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df = process_data()
last7 = df[df['Date'] >= df['Date'].max() - pd.Timedelta(days=6)]
today = df.iloc[-1]
yesterday = df.iloc[-2]

avg_steps    = last7['Steps'].mean()
avg_sleep    = last7['Sleep_Hours'].mean()
avg_recovery = last7['Recovery_Score'].mean()
avg_hr       = last7['Heart_Rate_BPM'].mean()

step_delta   = avg_steps    - df['Steps'].mean()
sleep_delta  = avg_sleep    - df['Sleep_Hours'].mean()

today_date = datetime.now().strftime("%b %d, %Y")

# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_status = st.columns([6, 1])
with col_logo:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.5rem">
      <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#00ff88,#00ccff);display:flex;align-items:center;justify-content:center">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 3 L10 17 M4 8 L10 3 L16 8 M6 13 Q10 17 14 13" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
      </div>
      <div>
        <div style="font-size:22px;font-weight:700;letter-spacing:-0.5px">FitSync</div>
        <div style="font-size:11px;color:#555;font-family:'IBM Plex Mono',monospace;letter-spacing:1px;text-transform:uppercase">Health Analytics</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_status:
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;margin-top:0.5rem">
      <div class="status-pill">
        <span class="status-dot"></span> Live · {today_date}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin: 2rem 0 1.5rem">
  <div class="hero-tag">★ Personal Health Intelligence</div>
  <div class="hero-title">Your body,<br><span class="accent">decoded daily.</span></div>
  <div class="hero-desc">
    Track recovery, sleep, steps & more — all in one analytics hub built for peak performance.
    Navigate to <strong style="color:#fff">Dashboard</strong> for live charts or <strong style="color:#fff">Trends</strong> for deep dives.
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
step_sign  = "+" if step_delta >= 0 else ""
sleep_sign = "+" if sleep_delta >= 0 else ""
step_cls   = "up" if step_delta >= 0 else "down"
sleep_cls  = "up" if sleep_delta >= 0 else "down"

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi green">
    <div class="kpi-label">7-day avg steps</div>
    <div class="kpi-val green">{avg_steps:,.0f}</div>
    <div class="kpi-delta"><span class="{step_cls}">{step_sign}{step_delta:,.0f}</span> vs all-time avg</div>
  </div>
  <div class="kpi blue">
    <div class="kpi-label">Avg sleep</div>
    <div class="kpi-val blue">{avg_sleep:.1f}h</div>
    <div class="kpi-delta"><span class="{sleep_cls}">{sleep_sign}{sleep_delta:.2f}h</span> vs all-time avg</div>
  </div>
  <div class="kpi amber">
    <div class="kpi-label">Avg recovery</div>
    <div class="kpi-val amber">{avg_recovery:.0f}</div>
    <div class="kpi-delta">out of <span style="color:#888">100</span> this week</div>
  </div>
  <div class="kpi red">
    <div class="kpi-label">Avg heart rate</div>
    <div class="kpi-val red">{avg_hr:.0f} bpm</div>
    <div class="kpi-delta">resting · 7-day avg</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Bottom Grid ───────────────────────────────────────────────────────────────
scores  = last7['Recovery_Score'].tolist()
max_s   = max(scores) if scores else 100

def score_color(s):
    if s >= 75: return "#00ff88"
    if s >= 55: return "#00ccff"
    return "#ffaa00"

bars_html = "".join(
    f'<div class="bar" style="height:{s/max_s*74:.0f}px;background:{score_color(s)}" title="{s:.0f}"></div>'
    for s in scores
)

dot_classes = ["g" if s >= 75 else "b" if s >= 55 else "a" for s in scores]
dots_html = "".join(f'<div class="wd {c}"></div>' for c in dot_classes)

left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown(f"""
    <div class="card">
      <div class="card-label">This week — recovery score</div>
      <div class="bar-chart">{bars_html}</div>
      <div class="week-dots">{dots_html}</div>
      <div style="display:flex;justify-content:space-between;margin-top:10px">
        <span style="font-size:11px;color:#555;font-family:'IBM Plex Mono',monospace">Mon</span>
        <span style="font-size:11px;color:#555;font-family:'IBM Plex Mono',monospace">Sun</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class="card">
      <div class="card-label">Navigate</div>
      <div class="nav-item">
        <div>
          <span class="nav-dot" style="background:#00ff88"></span>
          <span class="nav-title">Dashboard</span>
          <div class="nav-sub" style="margin-left:18px">KPIs, scatter plots & trends</div>
        </div>
        <span style="color:#555;font-size:18px">→</span>
      </div>
      <div class="nav-item">
        <div>
          <span class="nav-dot" style="background:#00ccff"></span>
          <span class="nav-title">Trends</span>
          <div class="nav-sub" style="margin-left:18px">Histograms & monthly patterns</div>
        </div>
        <span style="color:#555;font-size:18px">→</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="footer">FitSync · Built with Streamlit · Saras AI Institute</div>',
    unsafe_allow_html=True
)