"""
Nifty 100 Technical Screener — Pro Edition v2
===============================================
50 indicators · Smart Alerts · Sector Scorecard · Watchlist
Live Yahoo Finance data · Deploy free on Streamlit Cloud
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nifty 100 Pro Screener",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State Init ────────────────────────────────────────────────────────
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = set()

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg,#040D20 0%,#080F26 55%,#040D20 100%) !important;
    background-attachment: fixed !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.main .block-container { padding-top:0.5rem !important; max-width:100% !important; }

[data-testid="stMain"]::before {
    content:''; position:fixed; inset:0;
    background-image: radial-gradient(circle,rgba(0,201,255,0.03) 1px,transparent 1px);
    background-size: 30px 30px; pointer-events:none; z-index:0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(4,10,25,0.97) !important;
    border-right: 1px solid rgba(0,201,255,0.1) !important;
}
[data-testid="stSidebar"] label { color:#94A3B8 !important; font-size:0.77rem !important; }
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color:#E2E8F0 !important; }

/* Typography */
h1,h2,h3,h4,h5,h6 { color:#F1F5F9 !important; font-family:'Inter',sans-serif !important; }
.stMarkdown p, p { color:#94A3B8 !important; }

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background:rgba(255,255,255,0.03) !important;
    border:1px solid rgba(0,201,255,0.18) !important;
    border-radius:8px !important; color:#CBD5E1 !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color:rgba(0,201,255,0.45) !important;
}

/* Text input (search) */
[data-testid="stTextInput"] input {
    background:rgba(255,255,255,0.03) !important;
    border:1px solid rgba(0,201,255,0.18) !important;
    border-radius:8px !important; color:#F1F5F9 !important;
    font-family:'Inter',sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color:rgba(0,201,255,0.5) !important;
    box-shadow:0 0 0 2px rgba(0,201,255,0.08) !important;
}

/* Slider */
[data-testid="stSlider"] label { color:#94A3B8 !important; font-size:0.76rem !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:rgba(255,255,255,0.025) !important;
    border:1px solid rgba(0,201,255,0.1) !important;
    border-radius:12px !important; padding:4px !important; gap:4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background:transparent !important; border-radius:8px !important;
    color:#4B5563 !important; font-weight:500 !important; font-size:0.83rem !important;
    padding:8px 18px !important; border:none !important;
    font-family:'Inter',sans-serif !important; transition:all 0.2s ease !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background:linear-gradient(135deg,rgba(0,201,255,0.12),rgba(139,92,246,0.12)) !important;
    color:#00C9FF !important;
    border:1px solid rgba(0,201,255,0.22) !important;
    box-shadow:0 0 16px rgba(0,201,255,0.08) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border:1px solid rgba(0,201,255,0.1) !important;
    border-radius:12px !important; overflow:hidden !important;
}
[data-testid="stDataFrame"] th {
    background:rgba(0,201,255,0.06) !important;
    color:#00C9FF !important; font-weight:600 !important;
    font-size:0.71rem !important; letter-spacing:0.06em !important;
    text-transform:uppercase !important;
}
[data-testid="stDataFrame"] td {
    background:rgba(4,13,32,0.85) !important; color:#CBD5E1 !important;
    font-family:'JetBrains Mono',monospace !important; font-size:0.81rem !important;
}

/* Expander */
[data-testid="stExpander"] {
    background:rgba(255,255,255,0.02) !important;
    border:1px solid rgba(0,201,255,0.1) !important; border-radius:10px !important;
}
[data-testid="stExpander"] summary { color:#94A3B8 !important; font-size:0.82rem !important; }

/* Buttons */
.stButton button {
    background:linear-gradient(135deg,rgba(0,201,255,0.1),rgba(139,92,246,0.1)) !important;
    color:#00C9FF !important; border:1px solid rgba(0,201,255,0.22) !important;
    border-radius:8px !important; font-family:'Inter',sans-serif !important;
    font-weight:500 !important; transition:all 0.2s !important;
}
.stButton button:hover {
    background:linear-gradient(135deg,rgba(0,201,255,0.2),rgba(139,92,246,0.2)) !important;
    box-shadow:0 0 20px rgba(0,201,255,0.12) !important;
}
[data-testid="stDownloadButton"] button {
    background:rgba(16,185,129,0.08) !important; color:#10B981 !important;
    border:1px solid rgba(16,185,129,0.28) !important; border-radius:8px !important;
}

/* Checkbox */
[data-testid="stCheckbox"] label { color:#94A3B8 !important; font-size:0.82rem !important; }

/* Progress */
[data-testid="stProgressBar"] > div { background:rgba(0,201,255,0.1) !important; border-radius:4px !important; }
[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#00C9FF,#8B5CF6) !important; border-radius:4px !important; }

/* Alert messages */
[data-testid="stAlert"] {
    border-radius:10px !important; background:rgba(0,201,255,0.04) !important;
    border-left:3px solid rgba(0,201,255,0.4) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background:rgba(0,201,255,0.18); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:rgba(0,201,255,0.36); }

/* Hide default st.metric */
[data-testid="metric-container"] { display:none !important; }

/* ══ Custom Components ══════════════════════════════════════════════════════ */

/* Header */
.hdr {
    display:flex; align-items:center; justify-content:space-between;
    background:linear-gradient(135deg,rgba(0,201,255,0.055) 0%,rgba(139,92,246,0.055) 100%);
    border:1px solid rgba(0,201,255,0.14); border-radius:18px;
    padding:22px 32px; margin-bottom:14px;
    position:relative; overflow:hidden;
}
.hdr::before {
    content:''; position:absolute; inset:0;
    background:radial-gradient(ellipse at 15% 50%,rgba(0,201,255,0.06) 0%,transparent 60%),
               radial-gradient(ellipse at 85% 50%,rgba(139,92,246,0.06) 0%,transparent 60%);
    pointer-events:none;
}
.hdr-icon { font-size:2rem; margin-right:16px; filter:drop-shadow(0 0 10px rgba(0,201,255,0.5)); }
.hdr-title {
    font-size:1.85rem; font-weight:800; letter-spacing:-0.03em;
    background:linear-gradient(135deg,#F1F5F9 0%,#CBD5E1 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    line-height:1.1; font-family:'Inter',sans-serif;
}
.hdr-accent {
    background:linear-gradient(135deg,#00C9FF 0%,#8B5CF6 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hdr-sub { color:#475569; font-size:0.83rem; margin-top:5px; }
.hdr-right { text-align:right; }
.live-badge {
    display:inline-flex; align-items:center; gap:7px;
    background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.28);
    color:#10B981; font-size:0.7rem; font-weight:700; letter-spacing:0.1em;
    padding:4px 14px; border-radius:20px; margin-bottom:6px;
}
.live-dot {
    width:6px; height:6px; background:#10B981; border-radius:50%;
    animation:blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; box-shadow:0 0 6px #10B981; }
    50% { opacity:0.3; box-shadow:none; }
}
.hdr-date { color:#334155; font-size:0.76rem; font-family:'JetBrains Mono',monospace; }

/* KPI row */
.kpi-row {
    display:grid; grid-template-columns:repeat(9,1fr);
    gap:10px; margin-bottom:10px;
}
.kpi-card {
    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);
    border-radius:12px; padding:14px 16px;
    position:relative; overflow:hidden;
    transition:transform 0.2s ease,border-color 0.2s ease;
}
.kpi-card::after {
    content:''; position:absolute; top:0; left:0; right:0;
    height:2px; border-radius:2px 2px 0 0;
    background:var(--c,rgba(0,201,255,0.45));
}
.kpi-card:hover { transform:translateY(-2px); border-color:rgba(0,201,255,0.18); }
.kpi-label { font-size:0.65rem; font-weight:700; letter-spacing:0.09em; text-transform:uppercase; color:#334155; margin-bottom:5px; }
.kpi-val { font-size:1.55rem; font-weight:700; color:#F1F5F9; font-family:'JetBrains Mono',monospace; line-height:1.1; }
.kpi-sub { font-size:0.68rem; color:#334155; margin-top:3px; font-family:'JetBrains Mono',monospace; }

/* Sentiment bar */
.sent-wrap {
    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);
    border-radius:12px; padding:12px 20px; margin-bottom:10px;
    display:flex; align-items:center; gap:14px;
}
.sent-lbl { font-size:0.67rem; font-weight:700; text-transform:uppercase; letter-spacing:0.09em; color:#334155; white-space:nowrap; }
.sent-track { flex:1; height:7px; border-radius:7px; background:rgba(255,255,255,0.04); display:flex; overflow:hidden; }
.sent-green { background:linear-gradient(90deg,#059669,#10B981); }
.sent-gray  { background:rgba(100,116,139,0.35); }
.sent-red   { background:linear-gradient(90deg,#F43F5E,#EF4444); }
.sent-stat-row { display:flex; gap:16px; }
.sent-stat { font-size:0.74rem; font-family:'JetBrains Mono',monospace; white-space:nowrap; }

/* Breadth panel */
.breadth-grid {
    display:grid; grid-template-columns:repeat(6,1fr);
    gap:8px; margin-bottom:10px;
}
.breadth-item {
    background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05);
    border-radius:10px; padding:10px 12px; text-align:center;
}
.breadth-val { font-size:1.05rem; font-weight:700; color:#F1F5F9; font-family:'JetBrains Mono',monospace; }
.breadth-lbl { font-size:0.62rem; color:#334155; margin-top:2px; text-transform:uppercase; letter-spacing:0.07em; }

/* Alert cards */
.alert-grid {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:12px; margin-bottom:10px;
}
.alert-card {
    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);
    border-radius:14px; padding:16px 18px;
    transition:transform 0.2s ease,border-color 0.2s ease;
}
.alert-card:hover { transform:translateY(-1px); }
.alert-card.bull { border-left:3px solid rgba(16,185,129,0.5); }
.alert-card.bear { border-left:3px solid rgba(244,63,94,0.5); }
.alert-card.info { border-left:3px solid rgba(0,201,255,0.45); }
.alert-card.warn { border-left:3px solid rgba(245,158,11,0.5); }
.alert-icon { font-size:1.2rem; margin-bottom:6px; }
.alert-title { font-size:0.88rem; font-weight:700; color:#F1F5F9; margin-bottom:2px; }
.alert-desc { font-size:0.71rem; color:#475569; margin-bottom:8px; line-height:1.4; }
.alert-count {
    display:inline-block; background:rgba(0,201,255,0.1); color:#00C9FF;
    font-size:0.68rem; font-weight:700; padding:2px 10px; border-radius:12px;
    margin-bottom:8px; font-family:'JetBrains Mono',monospace;
}
.alert-count.green { background:rgba(16,185,129,0.12); color:#10B981; }
.alert-count.red   { background:rgba(244,63,94,0.12); color:#F43F5E; }
.alert-count.amber { background:rgba(245,158,11,0.12); color:#F59E0B; }
.alert-tickers { display:flex; flex-wrap:wrap; gap:5px; }
.t-pill {
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
    color:#CBD5E1; font-size:0.69rem; font-weight:500;
    padding:2px 9px; border-radius:7px;
    font-family:'JetBrains Mono',monospace;
}

/* Section title */
.sec-title {
    font-size:0.78rem; font-weight:700; letter-spacing:0.08em;
    text-transform:uppercase; color:#00C9FF;
    margin-bottom:10px; display:flex; align-items:center; gap:8px;
}
.sec-title::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg,rgba(0,201,255,0.3),transparent);
}

/* Signal badges */
.sig { display:inline-flex; align-items:center; padding:2px 11px; border-radius:20px; font-size:0.7rem; font-weight:700; letter-spacing:0.04em; }
.sig-STRONG-BUY  { background:rgba(16,185,129,0.12);  color:#10B981; border:1px solid rgba(16,185,129,0.3); }
.sig-BUY         { background:rgba(52,211,153,0.1);   color:#34D399; border:1px solid rgba(52,211,153,0.25); }
.sig-NEUTRAL     { background:rgba(100,116,139,0.12); color:#94A3B8; border:1px solid rgba(100,116,139,0.25); }
.sig-SELL        { background:rgba(244,63,94,0.1);    color:#F43F5E; border:1px solid rgba(244,63,94,0.25); }
.sig-STRONG-SELL { background:rgba(239,68,68,0.1);   color:#EF4444; border:1px solid rgba(239,68,68,0.25); }

/* Sidebar section */
.sb-sec {
    font-size:0.67rem; font-weight:700; letter-spacing:0.12em;
    text-transform:uppercase; color:#00C9FF !important;
    margin:1.3rem 0 0.45rem 0; padding-bottom:5px;
    border-bottom:1px solid rgba(0,201,255,0.13);
}

/* Comparison panel */
.cmp-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px; }
.cmp-card {
    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07);
    border-radius:12px; padding:16px 18px;
}
.cmp-ticker { font-size:1.05rem; font-weight:800; color:#F1F5F9; margin-bottom:10px; font-family:'JetBrains Mono',monospace; }
.cmp-row { display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.04); }
.cmp-lbl { font-size:0.72rem; color:#475569; }
.cmp-val { font-size:0.76rem; font-weight:600; color:#CBD5E1; font-family:'JetBrains Mono',monospace; }

/* Watchlist badge */
.wl-badge {
    display:inline-flex; align-items:center; gap:5px;
    background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.28);
    color:#F59E0B; font-size:0.7rem; font-weight:700; letter-spacing:0.06em;
    padding:3px 12px; border-radius:16px;
}

/* Footer */
.footer-txt { color:rgba(51,65,85,0.7); font-size:0.72rem; text-align:center; margin-top:0.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Universe ──────────────────────────────────────────────────────────────────
TICKERS = [
    'ABB.NS','ADANIENT.NS','ADANIGREEN.NS','ADANIPORTS.NS','AMBUJACEM.NS',
    'APOLLOHOSP.NS','ASIANPAINT.NS','AUROPHARMA.NS','AXISBANK.NS','BAJAJ-AUTO.NS',
    'BAJAJFINSV.NS','BAJFINANCE.NS','BANDHANBNK.NS','BANKBARODA.NS','BERGEPAINT.NS',
    'BHARTIARTL.NS','BOSCHLTD.NS','BPCL.NS','BRITANNIA.NS','CANBK.NS',
    'CHOLAFIN.NS','CIPLA.NS','COALINDIA.NS','COLPAL.NS','DABUR.NS',
    'DIVISLAB.NS','DMART.NS','DRREDDY.NS','EICHERMOT.NS','FEDERALBNK.NS',
    'FORTIS.NS','GAIL.NS','GODREJCP.NS','GRASIM.NS','HAVELLS.NS',
    'HCLTECH.NS','HDFCBANK.NS','HDFCLIFE.NS','HEROMOTOCO.NS','HINDALCO.NS',
    'HINDUNILVR.NS','HINDZINC.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS',
    'IDFCFIRSTB.NS','INDIGO.NS','INDUSINDBK.NS','IOC.NS','IRCTC.NS',
    'ITC.NS','JSWSTEEL.NS','KOTAKBANK.NS','LALPATHLAB.NS','LT.NS',
    'LUPIN.NS','M&M.NS','MARICO.NS','MARUTI.NS','MAXHEALTH.NS',
    'METROPOLIS.NS','MFSL.NS','MOTHERSON.NS','MUTHOOTFIN.NS','NAUKRI.NS',
    'NESTLEIND.NS','NMDC.NS','NTPC.NS','NYKAA.NS','ONGC.NS',
    'PAYTM.NS','PIDILITIND.NS','PNB.NS','POLICYBZR.NS','POWERGRID.NS',
    'RELIANCE.NS','SAIL.NS','SBICARD.NS','SBILIFE.NS','SBIN.NS',
    'SHREECEM.NS','SIEMENS.NS','SUNPHARMA.NS','TATACONSUM.NS','TATAPOWER.NS',
    'TATASTEEL.NS','TCS.NS','TECHM.NS','TITAN.NS','TORNTPHARM.NS',
    'TRENT.NS','ULTRACEMCO.NS','VEDL.NS','WIPRO.NS',
]

SECTORS = {
    'Banking & Finance': ['HDFCBANK.NS','ICICIBANK.NS','AXISBANK.NS','SBIN.NS','KOTAKBANK.NS',
                          'BAJFINANCE.NS','BAJAJFINSV.NS','BANDHANBNK.NS','BANKBARODA.NS','CANBK.NS',
                          'CHOLAFIN.NS','FEDERALBNK.NS','IDFCFIRSTB.NS','INDUSINDBK.NS','PNB.NS',
                          'SBICARD.NS','SBILIFE.NS','HDFCLIFE.NS','ICICIGI.NS','ICICIPRULI.NS','MUTHOOTFIN.NS'],
    'IT & Technology':   ['TCS.NS','HCLTECH.NS','WIPRO.NS','TECHM.NS','NAUKRI.NS','PAYTM.NS','POLICYBZR.NS','NYKAA.NS'],
    'Oil & Gas':         ['RELIANCE.NS','ONGC.NS','BPCL.NS','GAIL.NS','IOC.NS'],
    'FMCG':              ['HINDUNILVR.NS','ITC.NS','BRITANNIA.NS','NESTLEIND.NS','DABUR.NS',
                          'MARICO.NS','COLPAL.NS','GODREJCP.NS','TATACONSUM.NS'],
    'Pharma':            ['SUNPHARMA.NS','DRREDDY.NS','CIPLA.NS','DIVISLAB.NS','LUPIN.NS',
                          'AUROPHARMA.NS','TORNTPHARM.NS','LALPATHLAB.NS','METROPOLIS.NS','MAXHEALTH.NS','FORTIS.NS'],
    'Auto':              ['MARUTI.NS','BAJAJ-AUTO.NS','EICHERMOT.NS','HEROMOTOCO.NS','M&M.NS',
                          'MOTHERSON.NS','BOSCHLTD.NS'],
    'Metals & Mining':   ['TATASTEEL.NS','JSWSTEEL.NS','HINDALCO.NS','VEDL.NS','SAIL.NS',
                          'COALINDIA.NS','NMDC.NS','HINDZINC.NS'],
    'Cement':            ['ULTRACEMCO.NS','GRASIM.NS','AMBUJACEM.NS','SHREECEM.NS'],
    'Capital Goods':     ['LT.NS','SIEMENS.NS','ABB.NS','HAVELLS.NS','BOSCHLTD.NS'],
    'Consumer':          ['TITAN.NS','DMART.NS','TRENT.NS','BERGEPAINT.NS','PIDILITIND.NS','ASIANPAINT.NS'],
    'Power & Utilities': ['POWERGRID.NS','NTPC.NS','TATAPOWER.NS','ADANIGREEN.NS','ADANIPORTS.NS'],
    'Telecom':           ['BHARTIARTL.NS'],
    'Aviation':          ['INDIGO.NS'],
    'Others':            ['ADANIENT.NS','APOLLOHOSP.NS','CHOLAFIN.NS','IRCTC.NS','MFSL.NS'],
}
TICKER_SECTOR = {t: s for s, tks in SECTORS.items() for t in tks}

# ── Chart constants ───────────────────────────────────────────────────────────
CHART_BG   = '#040D20'
CHART_GRID = 'rgba(255,255,255,0.04)'
C_GREEN    = '#10B981'
C_RED      = '#F43F5E'
C_CYAN     = '#00C9FF'
C_AMBER    = '#F59E0B'
C_PURPLE   = '#8B5CF6'
C_VIOLET   = '#A78BFA'

# ── Indicator Computation ─────────────────────────────────────────────────────
def _ewm(s, com):
    return s.ewm(com=com, min_periods=int(com)+1, adjust=False).mean()

def compute_all(df):
    o, h, l, c, v = df['Open'], df['High'], df['Low'], df['Close'], df['Volume']
    out = pd.DataFrame(index=df.index)
    out['Open']=o; out['High']=h; out['Low']=l; out['Close']=c; out['Volume']=v
    out['Chg_Pct'] = c.pct_change() * 100

    for w in [20,50,200]: out[f'SMA_{w}'] = c.rolling(w).mean()
    for w in [9,20,50,200]: out[f'EMA_{w}'] = c.ewm(span=w,adjust=False).mean()

    e20=c.ewm(span=20,adjust=False).mean(); ee20=e20.ewm(span=20,adjust=False).mean()
    eee20=ee20.ewm(span=20,adjust=False).mean()
    out['DEMA_20']=2*e20-ee20; out['TEMA_20']=3*e20-3*ee20+eee20

    wma_h=c.rolling(10).apply(lambda x:np.average(x,weights=range(1,11)),raw=True)
    wma_f=c.rolling(20).apply(lambda x:np.average(x,weights=range(1,21)),raw=True)
    hull_raw=2*wma_h-wma_f; ns=int(round(20**0.5))
    out['HullMA_20']=hull_raw.rolling(ns).apply(lambda x:np.average(x,weights=range(1,ns+1)),raw=True)

    tp=(h+l+c)/3
    out['VWAP_20']=(tp*v).rolling(20).sum()/v.rolling(20).sum()
    out['VWAP_Pct']=(c-out['VWAP_20'])/out['VWAP_20']*100

    for p in [9,14]:
        d=c.diff(); gain=_ewm(d.clip(lower=0),p-1); loss=_ewm((-d).clip(lower=0),p-1)
        out[f'RSI_{p}']=100-100/(1+gain/loss)

    mf=tp*v
    pos=mf.where(tp>tp.shift(1),0).rolling(14).sum()
    neg=mf.where(tp<tp.shift(1),0).rolling(14).sum()
    out['MFI_14']=100-100/(1+pos/neg.replace(0,np.nan))

    hh14=h.rolling(14).max(); ll14=l.rolling(14).min()
    out['Stoch_K']=100*(c-ll14)/(hh14-ll14).replace(0,np.nan)
    out['Stoch_D']=out['Stoch_K'].rolling(3).mean()
    out['WillR_14']=-100*(hh14-c)/(hh14-ll14).replace(0,np.nan)

    sma_tp20=tp.rolling(20).mean()
    mad20=tp.rolling(20).apply(lambda x:np.mean(np.abs(x-x.mean())),raw=True)
    out['CCI_20']=(tp-sma_tp20)/(0.015*mad20)

    for p in [10,20]: out[f'ROC_{p}']=(c-c.shift(p))/c.shift(p)*100

    d=c.diff(); su=d.clip(lower=0).rolling(14).sum(); sd=(-d).clip(lower=0).rolling(14).sum()
    out['CMO_14']=(su-sd)/(su+sd).replace(0,np.nan)*100

    e1=c.ewm(span=15,adjust=False).mean(); e2=e1.ewm(span=15,adjust=False).mean()
    e3=e2.ewm(span=15,adjust=False).mean(); out['TRIX_15']=e3.pct_change()*100

    bp=c-pd.concat([l,c.shift(1)],axis=1).min(axis=1)
    tr_=pd.concat([h-l,(h-c.shift(1)).abs(),(l-c.shift(1)).abs()],axis=1).max(axis=1)
    a7=bp.rolling(7).sum()/tr_.rolling(7).sum()
    a14=bp.rolling(14).sum()/tr_.rolling(14).sum()
    a28=bp.rolling(28).sum()/tr_.rolling(28).sum()
    out['UltOsc']=(4*a7+2*a14+a28)/7*100

    ema12=c.ewm(span=12,adjust=False).mean(); ema26=c.ewm(span=26,adjust=False).mean()
    out['MACD']=ema12-ema26; out['MACD_Sig']=out['MACD'].ewm(span=9,adjust=False).mean()
    out['MACD_Hist']=out['MACD']-out['MACD_Sig']

    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    out['ATR_14']=tr.ewm(com=13,min_periods=14,adjust=False).mean()
    out['ATR_Pct']=out['ATR_14']/c*100

    bb_mid=c.rolling(20).mean(); bb_std=c.rolling(20).std()
    out['BB_Upper']=bb_mid+2*bb_std; out['BB_Lower']=bb_mid-2*bb_std
    out['BB_Pct']=(c-out['BB_Lower'])/(out['BB_Upper']-out['BB_Lower'])*100
    out['BB_Width']=(out['BB_Upper']-out['BB_Lower'])/bb_mid*100

    kelt_mid=c.ewm(span=20,adjust=False).mean()
    out['Kelt_Upper']=kelt_mid+2*out['ATR_14']; out['Kelt_Lower']=kelt_mid-2*out['ATR_14']
    out['Kelt_Pct']=(c-out['Kelt_Lower'])/(out['Kelt_Upper']-out['Kelt_Lower'])*100

    out['Don_High']=h.rolling(20).max(); out['Don_Low']=l.rolling(20).min()
    out['Don_Pct']=(c-out['Don_Low'])/(out['Don_High']-out['Don_Low']).replace(0,np.nan)*100

    log_ret=np.log(c/c.shift(1))
    out['HV_20']=log_ret.rolling(20).std()*np.sqrt(252)*100

    atr14=out['ATR_14']
    up_m=h.diff().clip(lower=0); dn_m=(-l.diff()).clip(lower=0)
    pdm=up_m.where(up_m>dn_m,0); ndm=dn_m.where(dn_m>up_m,0)
    out['PDI']=100*pdm.ewm(com=13,min_periods=14,adjust=False).mean()/atr14
    out['NDI']=100*ndm.ewm(com=13,min_periods=14,adjust=False).mean()/atr14
    dx=(100*(out['PDI']-out['NDI']).abs()/(out['PDI']+out['NDI']).replace(0,np.nan))
    out['ADX_14']=dx.ewm(com=13,min_periods=14,adjust=False).mean()

    def _aroon_up(x):
        try: return (np.nanargmax(x)/25)*100
        except: return np.nan
    def _aroon_dn(x):
        try: return (np.nanargmin(x)/25)*100
        except: return np.nan
    out['Aroon_Up']=h.rolling(26).apply(_aroon_up,raw=True)
    out['Aroon_Down']=l.rolling(26).apply(_aroon_dn,raw=True)
    out['Aroon_Osc']=out['Aroon_Up']-out['Aroon_Down']

    atr10=tr.ewm(com=9,min_periods=10,adjust=False).mean()
    mid=(h+l)/2; upper_band=mid+3*atr10; lower_band=mid-3*atr10
    supertrend=pd.Series(np.nan,index=df.index); direction=pd.Series(1,index=df.index)
    for i in range(1,len(df)):
        ub=upper_band.iloc[i]; lb=lower_band.iloc[i]
        prev_st=supertrend.iloc[i-1]; prev_ub=upper_band.iloc[i-1]; prev_lb=lower_band.iloc[i-1]
        lb=lb if lb<prev_lb or c.iloc[i-1]<prev_lb else prev_lb
        ub=ub if ub>prev_ub or c.iloc[i-1]>prev_ub else prev_ub
        upper_band.iloc[i]=ub; lower_band.iloc[i]=lb
        if pd.isna(prev_st) or prev_st==prev_ub:
            supertrend.iloc[i]=lb if c.iloc[i]>ub else ub
        else:
            supertrend.iloc[i]=lb if c.iloc[i]>lb else ub
        direction.iloc[i]=1 if c.iloc[i]>supertrend.iloc[i] else -1
    out['Supertrend']=supertrend; out['ST_Direction']=direction

    out['OBV']=(np.sign(c.diff())*v).fillna(0).cumsum()
    mfm=((c-l)-(h-c))/(h-l).replace(0,np.nan)
    out['CMF_20']=(mfm*v).rolling(20).sum()/v.rolling(20).sum()
    out['Vol_Ratio']=v/v.rolling(20).mean()

    ema13=c.ewm(span=13,adjust=False).mean()
    out['Elder_Bull']=h-ema13; out['Elder_Bear']=l-ema13

    out['Pivot_PP']=(h.shift(1)+l.shift(1)+c.shift(1))/3
    out['Pivot_R1']=2*out['Pivot_PP']-l.shift(1)
    out['Pivot_S1']=2*out['Pivot_PP']-h.shift(1)
    out['Pivot_R2']=out['Pivot_PP']+(h.shift(1)-l.shift(1))
    out['Pivot_S2']=out['Pivot_PP']-(h.shift(1)-l.shift(1))

    def score_latest(r):
        s=0; cl=r.get('Close',np.nan)
        for col in ['SMA_20','SMA_50','SMA_200','EMA_20','EMA_50','EMA_200']:
            v_=r.get(col,np.nan)
            if pd.notna(v_) and pd.notna(cl): s+=1 if cl>v_ else -1
        rsi=r.get('RSI_14',np.nan)
        if pd.notna(rsi):
            if rsi<30: s+=2
            elif rsi>70: s-=2
        mfi=r.get('MFI_14',np.nan)
        if pd.notna(mfi):
            if mfi<20: s+=2
            elif mfi>80: s-=2
        macd=r.get('MACD',np.nan); sig=r.get('MACD_Sig',np.nan)
        if pd.notna(macd) and pd.notna(sig): s+=1 if macd>sig else -1
        bb=r.get('BB_Pct',np.nan)
        if pd.notna(bb):
            if bb<0: s+=2
            elif bb>100: s-=2
            elif bb<20: s+=1
            elif bb>80: s-=1
        sk=r.get('Stoch_K',np.nan)
        if pd.notna(sk):
            if sk<20: s+=1
            elif sk>80: s-=1
        cci=r.get('CCI_20',np.nan)
        if pd.notna(cci):
            if cci<-100: s+=1
            elif cci>100: s-=1
        wr=r.get('WillR_14',np.nan)
        if pd.notna(wr):
            if wr<-80: s+=1
            elif wr>-20: s-=1
        roc=r.get('ROC_10',np.nan)
        if pd.notna(roc): s+=1 if roc>0 else -1
        adx=r.get('ADX_14',np.nan); pdi=r.get('PDI',np.nan); ndi=r.get('NDI',np.nan)
        if pd.notna(adx) and adx>25 and pd.notna(pdi) and pd.notna(ndi):
            s+=1 if pdi>ndi else -1
        cmf=r.get('CMF_20',np.nan)
        if pd.notna(cmf): s+=1 if cmf>0 else -1
        st_dir=r.get('ST_Direction',np.nan)
        if pd.notna(st_dir): s+=1 if st_dir>0 else -1
        return int(s)

    score=score_latest(out.iloc[-1])
    out['Score']=score
    if score>=8:    sig_label='STRONG BUY'
    elif score>=4:  sig_label='BUY'
    elif score<=-8: sig_label='STRONG SELL'
    elif score<=-4: sig_label='SELL'
    else:           sig_label='NEUTRAL'
    out['Signal']=sig_label
    return out

# ── Data Fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    rows=[]; history={}
    progress=st.progress(0,text="Initialising market data feed…")

    for i,ticker in enumerate(TICKERS):
        progress.progress((i+1)/len(TICKERS),
            text=f"⚡ Fetching {ticker.replace('.NS','')}  ({i+1}/{len(TICKERS)})")
        try:
            raw=yf.download(ticker,period='1y',interval='1d',auto_adjust=True,progress=False)
            if raw.empty or len(raw)<30: continue
            raw.columns=[c[0] if isinstance(c,tuple) else c for c in raw.columns]
            raw=raw[['Open','High','Low','Close','Volume']].dropna()
            ind=compute_all(raw)
            history[ticker]=ind
            lat=ind.iloc[-1].to_dict()
            lat['Ticker']=ticker.replace('.NS','')
            lat['Date']=ind.index[-1].strftime('%d-%b-%Y')
            lat['Sector']=TICKER_SECTOR.get(ticker,'Others')

            # ── 52-Week High / Low ────────────────────────────────────────
            lat['W52_High']=float(raw['High'].max())
            lat['W52_Low']=float(raw['Low'].min())
            lat['W52_HighPct']=round((lat['Close']-lat['W52_High'])/lat['W52_High']*100,2)
            lat['W52_LowPct']=round((lat['Close']-lat['W52_Low'])/lat['W52_Low']*100,2)

            # ── Alert flags ───────────────────────────────────────────────
            lat['RSI_Oversold']  =bool(lat.get('RSI_14',50)<30)
            lat['RSI_Overbought']=bool(lat.get('RSI_14',50)>70)
            lat['MACD_Bullish']  =bool(lat.get('MACD',0)>lat.get('MACD_Sig',0))
            lat['Golden_Cross']  =bool(lat.get('EMA_20',0)>lat.get('EMA_50',0))
            lat['BB_Squeeze']    =bool(lat.get('BB_Width',99)<8)
            lat['Vol_Spike']     =bool(lat.get('Vol_Ratio',0)>2)
            lat['Near52H']       =bool(lat.get('W52_HighPct',-100)>-5)
            lat['Strong_Up']     =bool(lat.get('ADX_14',0)>25 and lat.get('PDI',0)>lat.get('NDI',0))
            lat['ST_Bullish']    =bool(lat.get('ST_Direction',-1)>0)
            lat['Oversold_BB']   =bool(lat.get('BB_Pct',50)<5)
            rows.append(lat)
        except Exception:
            continue

    progress.empty()
    df=pd.DataFrame(rows)
    if df.empty: return df,history
    num_cols=df.select_dtypes(include=np.number).columns
    df[num_cols]=df[num_cols].round(2)
    return df,history

# ── Filters ───────────────────────────────────────────────────────────────────
def apply_filters(df, sel_signal, sel_sector, filters, search_term, wl_only):
    mask=pd.Series(True,index=df.index)
    if sel_signal!='ALL': mask&=df['Signal']==sel_signal
    if sel_sector!='ALL' and 'Sector' in df.columns: mask&=df['Sector']==sel_sector
    for col,(lo,hi) in filters.items():
        if col in df.columns: mask&=df[col].between(lo,hi,inclusive='both')
    if search_term:
        mask&=df['Ticker'].str.contains(search_term.upper(),na=False)
    if wl_only and st.session_state.watchlist:
        mask&=df['Ticker'].isin(st.session_state.watchlist)
    return df[mask].copy()

# ── Style helpers ─────────────────────────────────────────────────────────────
SIG_PALETTE={'STRONG BUY':'#10B981','BUY':'#34D399','NEUTRAL':'#94A3B8',
             'SELL':'#F43F5E','STRONG SELL':'#EF4444'}

def style_signal(val):
    m={'STRONG BUY': 'background:rgba(16,185,129,0.15);color:#10B981',
       'BUY':        'background:rgba(52,211,153,0.12);color:#34D399',
       'NEUTRAL':    'background:rgba(100,116,139,0.12);color:#94A3B8',
       'SELL':       'background:rgba(244,63,94,0.12);color:#F43F5E',
       'STRONG SELL':'background:rgba(239,68,68,0.12);color:#EF4444'}
    return m.get(val,'')

def style_chg(val):
    try:
        f=float(val)
        return 'color:#10B981' if f>0 else ('color:#F43F5E' if f<0 else '')
    except: return ''

def style_w52(val):
    try:
        f=float(val)
        if f>-3: return 'color:#F59E0B;font-weight:600'
        if f<-20: return 'color:#94A3B8'
        return ''
    except: return ''

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar(df):
    with st.sidebar:
        st.markdown("""
        <div style="padding:14px 4px 6px 4px;">
          <div style="font-size:1rem;font-weight:700;color:#F1F5F9;">⚙ Filter Controls</div>
          <div style="font-size:0.74rem;color:#334155;margin-top:3px;">Narrow the 95-stock universe</div>
        </div>""", unsafe_allow_html=True)

        # ── Signal & Sector ────────────────────────────────────────────────
        st.markdown('<p class="sb-sec">🎯 Signal & Sector</p>',unsafe_allow_html=True)
        sel_signal=st.selectbox("Signal",['ALL','STRONG BUY','BUY','NEUTRAL','SELL','STRONG SELL'],index=0)
        sectors=['ALL']+sorted(df['Sector'].unique().tolist()) if 'Sector' in df.columns else ['ALL']
        sel_sector=st.selectbox("Sector",sectors,index=0)

        filters={}

        def add_slider(label,col,d_min=None,d_max=None):
            if col not in df.columns: return
            vals=df[col].dropna()
            if vals.empty or len(vals)<2: return
            mn,mx=float(vals.min()),float(vals.max())
            if mn>=mx: return
            lo_def=float(np.clip(d_min if d_min is not None else mn,mn,mx))
            hi_def=float(np.clip(d_max if d_max is not None else mx,mn,mx))
            if lo_def>=hi_def: lo_def,hi_def=mn,mx
            try:
                lo,hi=st.slider(label,min_value=mn,max_value=mx,
                                value=(lo_def,hi_def),format="%.1f")
                if lo>mn or hi<mx: filters[col]=(lo,hi)
            except Exception: pass

        # ── Momentum ───────────────────────────────────────────────────────
        with st.expander("📈 Momentum", expanded=False):
            add_slider("RSI 14","RSI_14",0,100)
            add_slider("RSI 9 (fast)","RSI_9",0,100)
            add_slider("MFI 14","MFI_14",0,100)
            add_slider("Stoch %K","Stoch_K",0,100)
            add_slider("Stoch %D","Stoch_D",0,100)
            add_slider("Williams %R","WillR_14",-100,0)
            add_slider("CCI 20","CCI_20",-300,300)
            add_slider("ROC 10%","ROC_10",-30,30)
            add_slider("ROC 20%","ROC_20",-40,40)
            add_slider("Chande MO","CMO_14",-100,100)
            add_slider("TRIX 15","TRIX_15",-1,1)
            add_slider("Ultimate Osc","UltOsc",0,100)

        # ── MACD ───────────────────────────────────────────────────────────
        with st.expander("〰 MACD", expanded=False):
            add_slider("MACD Line","MACD")
            add_slider("MACD Histogram","MACD_Hist")

        # ── Volatility ─────────────────────────────────────────────────────
        with st.expander("🌊 Volatility & Bands", expanded=False):
            add_slider("ATR 14 (%)","ATR_Pct",0,10)
            add_slider("Bollinger %B","BB_Pct",-20,120)
            add_slider("Bollinger Width %","BB_Width",0,30)
            add_slider("Keltner %","Kelt_Pct",-20,120)
            add_slider("Donchian %","Don_Pct",0,100)
            add_slider("Hist. Volatility","HV_20",0,100)

        # ── Trend ──────────────────────────────────────────────────────────
        with st.expander("📡 Trend Strength", expanded=False):
            add_slider("ADX 14","ADX_14",0,60)
            add_slider("+DI 14","PDI",0,60)
            add_slider("-DI 14","NDI",0,60)
            add_slider("Aroon Up","Aroon_Up",0,100)
            add_slider("Aroon Down","Aroon_Down",0,100)
            add_slider("Aroon Osc","Aroon_Osc",-100,100)

        # ── Volume ─────────────────────────────────────────────────────────
        with st.expander("📦 Volume", expanded=False):
            add_slider("CMF 20","CMF_20",-0.5,0.5)
            add_slider("Volume Ratio","Vol_Ratio",0,5)
            add_slider("VWAP % Diff","VWAP_Pct",-20,20)

        # ── 52-Week ────────────────────────────────────────────────────────
        with st.expander("📅 52-Week Range", expanded=False):
            add_slider("% from 52W High","W52_HighPct",-50,0)
            add_slider("% above 52W Low","W52_LowPct",0,200)

        # ── Score ──────────────────────────────────────────────────────────
        with st.expander("🎲 Composite Score", expanded=False):
            add_slider("Signal Score","Score",-15,15)

        st.markdown("---")
        n_active=len(filters)
        status_color="#00C9FF" if n_active>0 else "#334155"
        st.markdown(
            f"<div style='font-size:0.74rem;color:{status_color};'>"
            f"{'✦ '+str(n_active)+' active filter(s)' if n_active else 'No filters active'}</div>"
            f"<div style='font-size:0.7rem;color:#1E293B;margin-top:4px;'>"
            f"⭐ Watchlist: {len(st.session_state.watchlist)} stocks</div>",
            unsafe_allow_html=True)

        return sel_signal,sel_sector,filters

# ── KPI Card helper ───────────────────────────────────────────────────────────
def kpi(label,value,sub="",cls="kpi-cyan"):
    return (f'<div class="kpi-card {cls}" style="--c:{"rgba(0,201,255,0.45)" if cls=="kpi-cyan" else "rgba(139,92,246,0.45)" if cls=="kpi-purple" else "rgba(16,185,129,0.5)" if cls=="kpi-green" else "rgba(244,63,94,0.5)" if cls=="kpi-red" else "rgba(245,158,11,0.5)" if cls=="kpi-amber" else "rgba(100,116,139,0.45)"};">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-val">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div>')

# ── Sentiment Bar ─────────────────────────────────────────────────────────────
def render_sentiment(df):
    if df.empty or 'Signal' not in df.columns: return
    n=len(df)
    if n==0: return
    nb=df['Signal'].isin(['BUY','STRONG BUY']).sum()
    nn=df['Signal'].eq('NEUTRAL').sum()
    ns=df['Signal'].isin(['SELL','STRONG SELL']).sum()
    wb,wn,ws=nb/n*100,nn/n*100,ns/n*100
    mood="BULLISH" if nb>ns else ("BEARISH" if ns>nb else "NEUTRAL")
    mc={"BULLISH":"#10B981","BEARISH":"#F43F5E","NEUTRAL":"#94A3B8"}[mood]
    st.markdown(f"""
    <div class="sent-wrap">
      <div class="sent-lbl">Market<br>Breadth</div>
      <div style="font-size:0.95rem;font-weight:800;color:{mc};font-family:'Inter',sans-serif;white-space:nowrap;min-width:80px;">{mood}</div>
      <div class="sent-track">
        <div class="sent-seg sent-green" style="width:{wb:.1f}%"></div>
        <div class="sent-seg sent-gray"  style="width:{wn:.1f}%"></div>
        <div class="sent-seg sent-red"   style="width:{ws:.1f}%"></div>
      </div>
      <div class="sent-stat-row">
        <div class="sent-stat" style="color:#10B981;">▲ {nb} BUY</div>
        <div class="sent-stat" style="color:#94A3B8;">— {nn} NEUTRAL</div>
        <div class="sent-stat" style="color:#F43F5E;">▼ {ns} SELL</div>
      </div>
    </div>""",unsafe_allow_html=True)

# ── Market Breadth Panel ──────────────────────────────────────────────────────
def render_breadth(df):
    if df.empty: return
    n=len(df)
    pct_above_sma200=df[df['Close']>df['SMA_200']].shape[0]/n*100 if 'SMA_200' in df.columns else 0
    pct_above_sma50 =df[df['Close']>df['SMA_50']].shape[0]/n*100  if 'SMA_50'  in df.columns else 0
    pct_golden_cross =df['Golden_Cross'].sum()/n*100 if 'Golden_Cross' in df.columns else 0
    pct_st_bull      =df['ST_Bullish'].sum()/n*100   if 'ST_Bullish'  in df.columns else 0
    avg_score        =df['Score'].mean() if 'Score' in df.columns else 0
    near52h_n        =int(df['Near52H'].sum()) if 'Near52H' in df.columns else 0

    def bval(v,fmt="{:.0f}%",color_fn=None):
        s=fmt.format(v)
        color="#F1F5F9"
        if color_fn: color=color_fn(v)
        return f'<div class="breadth-val" style="color:{color};">{s}</div>'

    def gc(v): return "#10B981" if v>=60 else ("#F43F5E" if v<=40 else "#94A3B8")

    items=[
        (bval(pct_above_sma200,color_fn=gc),"% Above SMA 200"),
        (bval(pct_above_sma50,color_fn=gc),"% Above SMA 50"),
        (bval(pct_golden_cross,color_fn=gc),"Golden Cross"),
        (bval(pct_st_bull,color_fn=gc),"Supertrend Bull"),
        (f'<div class="breadth-val" style="color:{"#10B981" if avg_score>0 else "#F43F5E"};">{avg_score:+.1f}</div>',"Avg Signal Score"),
        (f'<div class="breadth-val" style="color:#F59E0B;">{near52h_n}</div>',"Near 52W High"),
    ]
    html='<div class="breadth-grid">'
    for val_html,lbl in items:
        html+=f'<div class="breadth-item">{val_html}<div class="breadth-lbl">{lbl}</div></div>'
    html+='</div>'
    st.markdown(html,unsafe_allow_html=True)

# ── Smart Alerts Tab ──────────────────────────────────────────────────────────
def render_alerts(df):
    if df.empty:
        st.info("Load data to see alerts."); return

    def pill_list(tickers):
        return ''.join(f'<span class="t-pill">{t}</span>' for t in tickers[:20])

    ALERT_DEFS=[
        ('RSI_Oversold','🔵','RSI Oversold (<30)','Potential reversal — price may be bottoming','bull',
         'green','Oversold stocks are near buy zones — watch for RSI turning upward'),
        ('RSI_Overbought','🔴','RSI Overbought (>70)','Extended rally — watch for pullback','bear',
         'red','These stocks may be due for a correction or consolidation'),
        ('MACD_Bullish','🟢','MACD Bullish','MACD crossed above signal line — building momentum','bull',
         'green','Momentum is accelerating to the upside'),
        ('Golden_Cross','⭐','Golden Cross','EMA 20 above EMA 50 — bullish trend structure','bull',
         'green','Classic medium-term bullish alignment'),
        ('BB_Squeeze','💥','Bollinger Squeeze','Bands are very tight — volatility expansion imminent','info',
         'cyan','Low volatility precedes big moves — watch direction of breakout'),
        ('Vol_Spike','📦','Volume Spike (>2× avg)','Unusually high volume signals institutional activity','warn',
         'amber','High-conviction moves — confirm with price direction'),
        ('Near52H','🚀','Near 52-Week High','Within 5% of yearly peak — breakout territory','bull',
         'green','Stocks at highs can continue higher with momentum'),
        ('Strong_Up','📈','Strong Uptrend','ADX > 25 with +DI above -DI — trend is in force','bull',
         'green','Trend-following setup — ride the momentum'),
        ('ST_Bullish','✅','Supertrend Bullish','Price above Supertrend line — confirmed uptrend','bull',
         'green','Supertrend is a reliable trend-following indicator'),
        ('Oversold_BB','🎯','BB Lower Touch','Price near/below lower Bollinger Band','bull',
         'green','Mean-reversion opportunity — watch for bounce'),
    ]

    st.markdown('<div class="sec-title">🚨 Smart Alerts — Auto-detected Signals</div>',
                unsafe_allow_html=True)
    st.markdown("<div style='color:#334155;font-size:0.75rem;margin-bottom:12px;'>"
                "These patterns are detected automatically from today's latest indicator values.</div>",
                unsafe_allow_html=True)

    # Build alert grid (2 columns)
    col1, col2 = st.columns(2)
    for idx,(flag,icon,title,desc,card_cls,count_cls,tip) in enumerate(ALERT_DEFS):
        if flag not in df.columns: continue
        flagged=df[df[flag]==True]['Ticker'].tolist()
        if not flagged: continue
        card_html=(
            f'<div class="alert-card {card_cls}">'
            f'<div class="alert-icon">{icon}</div>'
            f'<div class="alert-title">{title}</div>'
            f'<div class="alert-desc">{desc}</div>'
            f'<div class="alert-count {count_cls}">{len(flagged)} stock{"s" if len(flagged)!=1 else ""}</div>'
            f'<div class="alert-tickers">{pill_list(flagged)}</div>'
            f'</div>'
        )
        if idx%2==0:
            with col1: st.markdown(card_html,unsafe_allow_html=True)
        else:
            with col2: st.markdown(card_html,unsafe_allow_html=True)

    # ── Alert Summary Table ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="sec-title">📋 Alert Summary per Stock</div>',unsafe_allow_html=True)
    flag_cols=[f for f,*_ in ALERT_DEFS if f in df.columns]
    alert_sum=df[['Ticker','Sector','Close','Signal','Score']+flag_cols].copy()
    alert_sum['Alerts']=alert_sum[flag_cols].sum(axis=1)
    alert_sum=alert_sum[alert_sum['Alerts']>0].sort_values('Alerts',ascending=False)
    if not alert_sum.empty:
        disp=alert_sum[['Ticker','Sector','Close','Signal','Score','Alerts']].copy()
        try:
            st.dataframe(
                disp.style
                    .map(style_signal,subset=['Signal'])
                    .background_gradient(subset=['Alerts'],cmap='YlOrRd')
                    .format({'Close':'₹{:.2f}'},na_rep='—'),
                use_container_width=True,hide_index=True,height=350)
        except Exception:
            st.dataframe(disp,use_container_width=True,hide_index=True)
    else:
        st.info("No stocks triggered multiple alerts today.")

# ── Sector Scorecard ──────────────────────────────────────────────────────────
def render_sector_scorecard(df):
    if df.empty or 'Sector' not in df.columns:
        st.info("No sector data."); return

    st.markdown('<div class="sec-title">🏭 Sector Scorecard</div>',unsafe_allow_html=True)
    st.markdown("<div style='color:#334155;font-size:0.75rem;margin-bottom:10px;'>"
                "Aggregated metrics per sector — sorted by Avg Score (best to worst)</div>",
                unsafe_allow_html=True)

    grp=df.groupby('Sector')
    sc=grp.agg(
        Stocks   =('Ticker','count'),
        Advancing=('Chg_Pct',lambda x:(x>0).sum()),
        Avg_Chg  =('Chg_Pct','mean'),
        Avg_Score=('Score','mean'),
        Avg_RSI  =('RSI_14','mean'),
        Avg_ADX  =('ADX_14','mean'),
        Pct_Buy  =('Signal',lambda x: x.isin(['BUY','STRONG BUY']).sum()/len(x)*100),
        Pct_Sell =('Signal',lambda x: x.isin(['SELL','STRONG SELL']).sum()/len(x)*100),
        Vol_Ratio=('Vol_Ratio','mean'),
    ).round(1).sort_values('Avg_Score',ascending=False).reset_index()

    sc.columns=['Sector','Stocks','Adv','Avg Chg%','Avg Score','Avg RSI',
                'Avg ADX','% BUY','% SELL','Avg Vol Ratio']

    def ss_score(v):
        if v>=3:   return 'background:rgba(16,185,129,0.15);color:#10B981'
        if v<=-3:  return 'background:rgba(244,63,94,0.12);color:#F43F5E'
        return ''
    def ss_chg(v):
        if v>0:  return 'color:#10B981'
        if v<0:  return 'color:#F43F5E'
        return ''
    try:
        styled_sc=sc.style
        if 'Avg Score' in sc.columns: styled_sc=styled_sc.map(ss_score,subset=['Avg Score'])
        if 'Avg Chg%'  in sc.columns: styled_sc=styled_sc.map(ss_chg,  subset=['Avg Chg%'])
        if '% BUY'  in sc.columns: styled_sc=styled_sc.background_gradient(subset=['% BUY'],  cmap='Greens',vmin=0,vmax=100)
        if '% SELL' in sc.columns: styled_sc=styled_sc.background_gradient(subset=['% SELL'], cmap='Reds',  vmin=0,vmax=100)
        styled_sc=styled_sc.format({
            'Avg Chg%':'{:+.1f}%','Avg Score':'{:+.1f}','Avg RSI':'{:.1f}',
            'Avg ADX':'{:.1f}','% BUY':'{:.0f}%','% SELL':'{:.0f}%',
            'Avg Vol Ratio':'{:.2f}x'
        },na_rep='—')
        st.dataframe(styled_sc,use_container_width=True,hide_index=True,height=420)
    except Exception:
        st.dataframe(sc,use_container_width=True,hide_index=True)

    # ── Sector Heatmap (bar chart) ─────────────────────────────────────────
    st.markdown('<div class="sec-title" style="margin-top:16px;">📊 Sector Score Comparison</div>',
                unsafe_allow_html=True)
    bar_colors=[C_GREEN if v>=0 else C_RED for v in sc['Avg Score']]
    fig=go.Figure(go.Bar(
        x=sc['Sector'], y=sc['Avg Score'],
        marker_color=bar_colors,marker_line_width=0,
        text=[f"{v:+.1f}" for v in sc['Avg Score']],
        textposition='outside',
        textfont=dict(size=10,color='#94A3B8'),
        hovertemplate='<b>%{x}</b><br>Avg Score: %{y:+.1f}<br>%{text}<extra></extra>',
    ))
    fig.add_hline(y=0,line_color='rgba(255,255,255,0.1)',line_width=1)
    fig.update_layout(
        height=280, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        margin=dict(l=8,r=8,t=30,b=100),
        xaxis=dict(gridcolor=CHART_GRID,tickangle=-35,tickfont=dict(color='#64748B',size=10)),
        yaxis=dict(gridcolor=CHART_GRID,tickfont=dict(color='#64748B',size=10)),
        font=dict(family='Inter',color='#64748B'),
    )
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

# ── Stock Chart ───────────────────────────────────────────────────────────────
def render_stock_chart(ticker_ns, history, days=90, overlay2=None):
    ind=history.get(ticker_ns)
    if ind is None or len(ind)<20:
        st.warning("Not enough data."); return
    ind=ind.iloc[-min(days,len(ind)):]

    fig=make_subplots(rows=4,cols=1,shared_xaxes=True,
                      row_heights=[0.45,0.20,0.20,0.15],vertical_spacing=0.025,
                      subplot_titles=["  Price · Bollinger Bands · EMA 20/50",
                                      f"  {overlay2 or 'RSI 14'}",
                                      "  MACD (12,26,9)","  Volume"])

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=ind.index,open=ind['Open'],high=ind['High'],
        low=ind['Low'],close=ind['Close'],
        increasing_line_color=C_GREEN,decreasing_line_color=C_RED,
        increasing_fillcolor=C_GREEN,decreasing_fillcolor=C_RED,
        name='OHLC',showlegend=False),row=1,col=1)

    # Bollinger
    if 'BB_Upper' in ind.columns and 'BB_Lower' in ind.columns:
        fig.add_trace(go.Scatter(x=ind.index,y=ind['BB_Upper'],mode='lines',
            line=dict(color=C_CYAN,width=1,dash='dot'),showlegend=False,opacity=0.45),row=1,col=1)
        fig.add_trace(go.Scatter(x=ind.index,y=ind['BB_Lower'],mode='lines',
            line=dict(color=C_CYAN,width=1,dash='dot'),
            fill='tonexty',fillcolor='rgba(0,201,255,0.035)',
            showlegend=False,opacity=0.45),row=1,col=1)

    for col,color,lbl in [('EMA_20',C_AMBER,'EMA 20'),('EMA_50',C_PURPLE,'EMA 50')]:
        if col in ind.columns:
            fig.add_trace(go.Scatter(x=ind.index,y=ind[col],
                line=dict(color=color,width=1.5),name=lbl,showlegend=True),row=1,col=1)

    # Supertrend
    if 'Supertrend' in ind.columns and 'ST_Direction' in ind.columns:
        for sub,color in [(ind[ind['ST_Direction']>0],C_GREEN),(ind[ind['ST_Direction']<0],C_RED)]:
            if not sub.empty:
                fig.add_trace(go.Scatter(x=sub.index,y=sub['Supertrend'],mode='markers',
                    marker=dict(color=color,size=3,symbol='circle',line=dict(width=0)),
                    showlegend=False),row=1,col=1)

    # ── Overlay 2 (configurable) ────────────────────────────────────────────
    OV_MAP={
        'RSI 14':   ('RSI_14',   C_AMBER,  [70,30,50], [0,100]),
        'RSI 9':    ('RSI_9',    C_VIOLET, [70,30,50], [0,100]),
        'MFI 14':   ('MFI_14',   C_CYAN,   [80,20,50], [0,100]),
        'Stoch %K': ('Stoch_K',  C_AMBER,  [80,20],    [0,100]),
        'Williams %R':('WillR_14',C_PURPLE, [-80,-20],  [-100,0]),
        'CCI 20':   ('CCI_20',   C_VIOLET, [100,-100],  None),
        'CMF 20':   ('CMF_20',   C_CYAN,   [0],         None),
    }
    ov_key=overlay2 or 'RSI 14'
    if ov_key in OV_MAP:
        ov_col,ov_color,ov_levels,ov_range=OV_MAP[ov_key]
        if ov_col in ind.columns:
            fill_arg='tozeroy' if 'RSI' in ov_col else 'none'
            fc=f'rgba({",".join(str(int(ov_color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.06)' if 'RSI' in ov_col else None
            fig.add_trace(go.Scatter(x=ind.index,y=ind[ov_col],
                line=dict(color=ov_color,width=1.8),
                fill=fill_arg if fc else 'none',
                fillcolor=fc,name=ov_key),row=2,col=1)
            for lv in ov_levels:
                lcolor=C_RED if lv>50 else (C_GREEN if 0<lv<50 else 'rgba(255,255,255,0.1)')
                if ov_col=='WillR_14': lcolor=C_RED if lv==-20 else C_GREEN
                if ov_col=='CCI_20':  lcolor=C_RED if lv>0 else C_GREEN
                if ov_col=='CMF_20':  lcolor='rgba(255,255,255,0.1)'
                fig.add_hline(y=lv,line_dash='dash',line_color=lcolor,
                              line_width=1,opacity=0.55,row=2,col=1)
            if ov_range: fig.update_yaxes(range=ov_range,row=2,col=1)

    # MACD
    if 'MACD' in ind.columns and 'MACD_Sig' in ind.columns:
        hist_v=ind.get('MACD_Hist',pd.Series([0]*len(ind)))
        bar_c=[C_GREEN if v>=0 else C_RED for v in hist_v]
        fig.add_trace(go.Bar(x=ind.index,y=hist_v,marker_color=bar_c,
                             marker_line_width=0,opacity=0.65,name='Hist',showlegend=False),row=3,col=1)
        fig.add_trace(go.Scatter(x=ind.index,y=ind['MACD'],
            line=dict(color=C_CYAN,width=1.6),name='MACD'),row=3,col=1)
        fig.add_trace(go.Scatter(x=ind.index,y=ind['MACD_Sig'],
            line=dict(color=C_VIOLET,width=1.6),name='Signal'),row=3,col=1)
        fig.add_hline(y=0,line_dash='dot',line_color='rgba(255,255,255,0.08)',
                      line_width=1,row=3,col=1)

    # Volume
    vol_c=[C_GREEN if c_>=o_ else C_RED for c_,o_ in zip(ind['Close'],ind['Open'])]
    fig.add_trace(go.Bar(x=ind.index,y=ind['Volume'],marker_color=vol_c,
                         marker_line_width=0,opacity=0.6,name='Vol',showlegend=False),row=4,col=1)
    if 'Volume' in ind.columns:
        fig.add_trace(go.Scatter(x=ind.index,y=ind['Volume'].rolling(20).mean(),
            line=dict(color=C_AMBER,width=1,dash='dash'),showlegend=False),row=4,col=1)

    fig.update_layout(
        height=680,paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        font=dict(family='Inter, sans-serif',color='#64748B',size=11),
        legend=dict(bgcolor='rgba(4,13,32,0.8)',bordercolor='rgba(0,201,255,0.15)',
                    borderwidth=1,font=dict(size=10),x=0.01,y=0.99),
        margin=dict(l=8,r=8,t=30,b=8),xaxis_rangeslider_visible=False,
    )
    for i in range(1,5):
        fig.update_xaxes(gridcolor=CHART_GRID,showgrid=True,zeroline=False,
                         showspikes=True,spikecolor='rgba(0,201,255,0.22)',
                         spikethickness=1,row=i,col=1)
        fig.update_yaxes(gridcolor=CHART_GRID,showgrid=True,zeroline=False,row=i,col=1)
    for ann in fig.layout.annotations:
        ann.font.color='#475569'; ann.font.size=10

    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

# ── Comparison Chart ──────────────────────────────────────────────────────────
def render_comparison(ticker1, ticker2, history, days=90):
    if ticker1==ticker2:
        st.info("Select two different stocks to compare."); return
    ind1=history.get(ticker1+'.NS')
    ind2=history.get(ticker2+'.NS')
    if ind1 is None or ind2 is None:
        st.warning("History not available for one of the stocks."); return
    ind1=ind1.iloc[-days:]; ind2=ind2.iloc[-days:]
    n1=ind1['Close']/ind1['Close'].iloc[0]*100
    n2=ind2['Close']/ind2['Close'].iloc[0]*100

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=ind1.index,y=n1,mode='lines',
        line=dict(color=C_CYAN,width=2),name=ticker1,
        hovertemplate='%{x}<br><b>'+ticker1+'</b>: %{y:.1f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=ind2.index,y=n2,mode='lines',
        line=dict(color=C_AMBER,width=2),name=ticker2,
        hovertemplate='%{x}<br><b>'+ticker2+'</b>: %{y:.1f}<extra></extra>'))
    fig.add_hline(y=100,line_dash='dot',line_color='rgba(255,255,255,0.12)',line_width=1)

    final1=float(n1.iloc[-1]); final2=float(n2.iloc[-1])
    winner=ticker1 if final1>final2 else ticker2
    fig.update_layout(
        height=300,paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        font=dict(family='Inter',color='#64748B',size=11),
        legend=dict(bgcolor='rgba(4,13,32,0.8)',bordercolor='rgba(0,201,255,0.15)',
                    borderwidth=1,font=dict(size=11)),
        margin=dict(l=8,r=8,t=40,b=8),
        xaxis=dict(gridcolor=CHART_GRID,showgrid=True,zeroline=False),
        yaxis=dict(gridcolor=CHART_GRID,showgrid=True,zeroline=False,
                   title=dict(text='Normalised (base=100)',font=dict(size=10,color='#475569'))),
        title=dict(text=f'Performance Comparison — winner: <b>{winner}</b> ({final1:+.1f}% vs {final2:+.1f}%)',
                   font=dict(size=11,color='#94A3B8'),x=0.01),
    )
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

# ── Comparison Metric Cards ───────────────────────────────────────────────────
def render_comparison_cards(df, ticker1, ticker2):
    r1=df[df['Ticker']==ticker1]
    r2=df[df['Ticker']==ticker2]
    if r1.empty or r2.empty: return
    r1,r2=r1.iloc[0],r2.iloc[0]

    metrics=[
        ("Close Price", f"₹{r1.get('Close',0):.2f}", f"₹{r2.get('Close',0):.2f}"),
        ("Day Change",  f"{r1.get('Chg_Pct',0):+.2f}%", f"{r2.get('Chg_Pct',0):+.2f}%"),
        ("Signal",      r1.get('Signal','—'),            r2.get('Signal','—')),
        ("Score",       f"{int(r1.get('Score',0)):+d}",  f"{int(r2.get('Score',0)):+d}"),
        ("RSI 14",      f"{r1.get('RSI_14',0):.1f}",    f"{r2.get('RSI_14',0):.1f}"),
        ("ADX 14",      f"{r1.get('ADX_14',0):.1f}",    f"{r2.get('ADX_14',0):.1f}"),
        ("MACD Hist",   f"{r1.get('MACD_Hist',0):.3f}", f"{r2.get('MACD_Hist',0):.3f}"),
        ("BB %B",       f"{r1.get('BB_Pct',0):.1f}",    f"{r2.get('BB_Pct',0):.1f}"),
        ("52W High %",  f"{r1.get('W52_HighPct',0):.1f}%",f"{r2.get('W52_HighPct',0):.1f}%"),
        ("Vol Ratio",   f"{r1.get('Vol_Ratio',0):.2f}x",f"{r2.get('Vol_Ratio',0):.2f}x"),
    ]
    rows1=''.join(f'<div class="cmp-row"><div class="cmp-lbl">{lbl}</div><div class="cmp-val">{v1}</div></div>'
                  for lbl,v1,_ in metrics)
    rows2=''.join(f'<div class="cmp-row"><div class="cmp-lbl">{lbl}</div><div class="cmp-val">{v2}</div></div>'
                  for lbl,_,v2 in metrics)
    st.markdown(
        f'<div class="cmp-grid">'
        f'<div class="cmp-card"><div class="cmp-ticker">{ticker1}</div>{rows1}</div>'
        f'<div class="cmp-card"><div class="cmp-ticker">{ticker2}</div>{rows2}</div>'
        f'</div>',unsafe_allow_html=True)

# ── Heatmap ───────────────────────────────────────────────────────────────────
def render_heatmap(df):
    if df.empty or 'Chg_Pct' not in df.columns:
        st.info("No data for heatmap."); return
    df2=df[['Ticker','Chg_Pct','Signal','Close','Sector']].dropna()
    fig=px.treemap(df2,path=['Sector','Ticker'],values=df2['Close'].abs(),color='Chg_Pct',
        color_continuous_scale=[[0,'#7f1d1d'],[0.35,'#EF4444'],[0.5,'#1e293b'],
                                 [0.65,'#059669'],[1,'#064e3b']],
        color_continuous_midpoint=0,
        hover_data={'Chg_Pct':':.2f','Close':':.2f','Signal':True},
        custom_data=['Ticker','Chg_Pct','Signal'])
    fig.update_traces(
        texttemplate='<b>%{label}</b><br>%{customdata[1]:.1f}%',
        textfont=dict(family='JetBrains Mono',size=11),
        marker_line_color='rgba(0,0,0,0.4)',marker_line_width=1.5)
    fig.update_layout(height=540,paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        margin=dict(l=0,r=0,t=20,b=0),
        coloraxis_colorbar=dict(title=dict(text='Δ%',font=dict(color='#64748B',size=11)),
            tickfont=dict(color='#64748B',family='JetBrains Mono'),thickness=14,len=0.7))
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

# ── Signal Donut ──────────────────────────────────────────────────────────────
def render_signal_donut(df):
    if df.empty or 'Signal' not in df.columns: return
    order=['STRONG BUY','BUY','NEUTRAL','SELL','STRONG SELL']
    counts=df['Signal'].value_counts().reindex(order,fill_value=0)
    colors=[C_GREEN,'#34D399','#475569',C_RED,'#EF4444']
    total=counts.sum(); dominant=counts.idxmax() if total>0 else 'NEUTRAL'
    dom_color=SIG_PALETTE.get(dominant,'#94A3B8')
    fig=go.Figure(go.Pie(
        labels=counts.index,values=counts.values,hole=0.68,
        marker=dict(colors=colors,line=dict(color=CHART_BG,width=2)),
        textinfo='label+value',textfont=dict(family='Inter',size=11,color='#94A3B8'),
        hovertemplate='%{label}: <b>%{value}</b><extra></extra>',
        pull=[0.04 if v==counts.max() else 0 for v in counts.values]))
    fig.add_annotation(text=f'<b>{dominant}</b>',x=0.5,y=0.52,showarrow=False,
        font=dict(size=12,color=dom_color,family='Inter'),xanchor='center')
    fig.add_annotation(text=f'{total} stocks',x=0.5,y=0.42,showarrow=False,
        font=dict(size=10,color='#334155',family='JetBrains Mono'),xanchor='center')
    fig.update_layout(height=280,paper_bgcolor=CHART_BG,plot_bgcolor=CHART_BG,
        margin=dict(l=0,r=0,t=10,b=0),
        legend=dict(font=dict(size=10,family='Inter',color='#64748B'),bgcolor=CHART_BG))
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

# ── Display column groups ─────────────────────────────────────────────────────
DISPLAY_COLS={
    '⭐ Core':      ['Ticker','Date','Sector','Close','Chg_Pct','W52_HighPct','Signal','Score'],
    '📊 Moving Avgs':['Ticker','SMA_20','SMA_50','SMA_200','EMA_20','EMA_50','EMA_200','DEMA_20','TEMA_20','HullMA_20','VWAP_20'],
    '🚀 Momentum':  ['Ticker','RSI_14','RSI_9','MFI_14','Stoch_K','Stoch_D','WillR_14','CCI_20','ROC_10','ROC_20','CMO_14','UltOsc'],
    '〰 MACD':      ['Ticker','MACD','MACD_Sig','MACD_Hist'],
    '🌊 Volatility':['Ticker','ATR_14','ATR_Pct','BB_Pct','BB_Width','Kelt_Pct','Don_Pct','HV_20'],
    '📡 Trend':     ['Ticker','ADX_14','PDI','NDI','Aroon_Up','Aroon_Down','Aroon_Osc','ST_Direction'],
    '📦 Volume':    ['Ticker','OBV','CMF_20','Vol_Ratio','Elder_Bull','Elder_Bear'],
    '📅 52-Week':   ['Ticker','Close','W52_High','W52_Low','W52_HighPct','W52_LowPct'],
}

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    with st.spinner("Connecting to live market feed…"):
        df,history=load_data()

    if df.empty:
        st.error("⚠️ Unable to fetch data. Check internet connection."); st.stop()

    last_date=df['Date'].iloc[0] if 'Date' in df.columns else 'N/A'

    # ── Header ────────────────────────────────────────────────────────────────
    wl_n=len(st.session_state.watchlist)
    wl_str=f"&nbsp;·&nbsp; ⭐ Watchlist: {wl_n}" if wl_n else ""
    st.markdown(f"""
    <div class="hdr">
      <div style="display:flex;align-items:center;">
        <div class="hdr-icon">⚡</div>
        <div>
          <div class="hdr-title">NIFTY 100 <span class="hdr-accent">PRO SCREENER</span></div>
          <div class="hdr-sub">50 Indicators &nbsp;·&nbsp; Smart Alerts &nbsp;·&nbsp; Sector Scorecard &nbsp;·&nbsp; Live NSE Data{wl_str}</div>
        </div>
      </div>
      <div class="hdr-right">
        <div class="live-badge"><span class="live-dot"></span>LIVE DATA</div><br>
        <div class="hdr-date">Last close: {last_date}</div>
      </div>
    </div>""",unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    sel_signal,sel_sector,filters=render_sidebar(df)

    # ── Search + Watchlist row ────────────────────────────────────────────────
    sc1,sc2,sc3=st.columns([3,2,2])
    with sc1:
        search_term=st.text_input("🔍 Search stock by ticker",placeholder="e.g. RELIANCE, TCS, HDFC…",
                                   label_visibility="collapsed")
    with sc2:
        wl_only=st.checkbox(f"⭐ Watchlist only ({wl_n} stocks)",value=False)
    with sc3:
        if st.button("🔄 Clear all filters + search"):
            st.rerun()

    filtered=apply_filters(df,sel_signal,sel_sector,filters,search_term,wl_only)

    # ── KPI Row ───────────────────────────────────────────────────────────────
    n_total  =len(df); n_shown=len(filtered)
    n_adv    =int((filtered['Chg_Pct']>0).sum()) if 'Chg_Pct' in filtered.columns else 0
    n_dec    =int((filtered['Chg_Pct']<0).sum()) if 'Chg_Pct' in filtered.columns else 0
    n_sbuy   =int((filtered['Signal']=='STRONG BUY').sum())
    n_buy    =int(filtered['Signal'].isin(['BUY','STRONG BUY']).sum())
    n_sell   =int(filtered['Signal'].isin(['SELL','STRONG SELL']).sum())
    n_ssell  =int((filtered['Signal']=='STRONG SELL').sum())
    n_neutral=int((filtered['Signal']=='NEUTRAL').sum())
    avg_rsi  =filtered['RSI_14'].mean() if 'RSI_14' in filtered.columns else 0
    avg_adx  =filtered['ADX_14'].mean() if 'ADX_14' in filtered.columns else 0

    kpis=[
        kpi("Universe",   str(n_total),  "Nifty 100",          "kpi-cyan"),
        kpi("Showing",    str(n_shown),  f"{len(filters)+bool(search_term)} filter(s)","kpi-purple"),
        kpi("▲ Advancing",str(n_adv),   "today",               "kpi-green"),
        kpi("▼ Declining",str(n_dec),   "today",               "kpi-red"),
        kpi("BUY Signals",str(n_buy),   f"incl {n_sbuy} strong","kpi-green"),
        kpi("SELL Signals",str(n_sell), f"incl {n_ssell} strong","kpi-red"),
        kpi("Neutral",    str(n_neutral),"no bias",             "kpi-slate"),
        kpi("Avg RSI 14", f"{avg_rsi:.1f}","0-100",             "kpi-amber"),
        kpi("Avg ADX 14", f"{avg_adx:.1f}","trend str.",        "kpi-purple"),
    ]
    st.markdown('<div class="kpi-row">'+''.join(kpis)+'</div>',unsafe_allow_html=True)

    # Sentiment + Breadth
    render_sentiment(filtered if not filtered.empty else df)
    render_breadth(filtered if not filtered.empty else df)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1,tab2,tab3,tab4,tab5,tab6=st.tabs([
        "📋  Screener",
        "🚨  Smart Alerts",
        "🏭  Sector Scorecard",
        "🌡️  Market Heatmap",
        "📈  Stock Deep Dive",
        "🍩  Signal Overview",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 1 — Screener
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        if filtered.empty:
            st.warning("⚠️ No stocks match the current filters.")
        else:
            tc1,tc2,tc3=st.columns([3,1,1])
            with tc1:
                col_grp=st.selectbox("Indicator group:",list(DISPLAY_COLS.keys()),index=0)
            with tc2:
                sort_asc=st.selectbox("Sort:",["↓ Score High→Low","↑ Score Low→High"],index=0)
            with tc3:
                highlight_wl=st.checkbox("Highlight Watchlist",value=False)

            show_cols=[c for c in DISPLAY_COLS[col_grp] if c in filtered.columns]
            view=filtered[show_cols].copy()
            if 'Score' in show_cols:
                view=view.sort_values('Score',ascending=(sort_asc=="↑ Score Low→High"))

            # Add watchlist star column
            if highlight_wl and st.session_state.watchlist:
                view.insert(0,'⭐',view['Ticker'].apply(
                    lambda t:'⭐' if t in st.session_state.watchlist else ''))

            try:
                styled=view.style
                if 'Signal'     in view.columns: styled=styled.map(style_signal,subset=['Signal'])
                if 'Chg_Pct'    in view.columns: styled=styled.map(style_chg,subset=['Chg_Pct'])
                if 'W52_HighPct'in view.columns: styled=styled.map(style_w52,subset=['W52_HighPct'])
                fmt={}
                if 'Chg_Pct'     in view.columns: fmt['Chg_Pct']     ='{:+.2f}%'
                if 'Close'        in view.columns: fmt['Close']        ='₹{:.2f}'
                if 'W52_HighPct'  in view.columns: fmt['W52_HighPct']  ='{:.1f}%'
                if 'W52_LowPct'   in view.columns: fmt['W52_LowPct']   ='{:+.1f}%'
                if fmt: styled=styled.format(fmt,na_rep='—')
                if 'Score' in view.columns:
                    styled=styled.background_gradient(subset=['Score'],cmap='RdYlGn',vmin=-15,vmax=15)
                st.dataframe(styled,use_container_width=True,height=480,hide_index=True)
            except Exception:
                st.dataframe(view,use_container_width=True,height=480,hide_index=True)

            dc1,dc2=st.columns([1,3])
            with dc1:
                st.download_button("⬇ Export CSV",
                    data=filtered.to_csv(index=False),
                    file_name=f"nifty100_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv")
            with dc2:
                st.markdown(f"<div style='color:#334155;font-size:0.76rem;padding-top:10px;'>"
                            f"Showing <b style='color:#00C9FF'>{n_shown}</b> of {n_total} stocks</div>",
                            unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 2 — Smart Alerts
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        render_alerts(df)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 3 — Sector Scorecard
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        render_sector_scorecard(filtered if not filtered.empty else df)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 4 — Market Heatmap
    # ══════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<div class="sec-title">🌡 Sector Heatmap — Daily Change %</div>',
                    unsafe_allow_html=True)
        st.caption("Box size = stock price · Colour = daily % change (green = up, red = down)")
        render_heatmap(filtered if not filtered.empty else df)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 5 — Stock Deep Dive
    # ══════════════════════════════════════════════════════════════════════════
    with tab5:
        if not history:
            st.info("No history loaded."); return

        tickers_clean=sorted([t.replace('.NS','') for t in history.keys()])
        default_stock=(filtered.sort_values('Score',ascending=False)['Ticker'].iloc[0]
                       if not filtered.empty else tickers_clean[0])

        dd1,dd2,dd3,dd4=st.columns([2,2,2,2])
        with dd1:
            sel_stock=st.selectbox("Stock:",tickers_clean,
                index=tickers_clean.index(default_stock) if default_stock in tickers_clean else 0)
        with dd2:
            compare_mode=st.checkbox("📊 Compare with another stock",value=False)
        with dd3:
            timeframe=st.selectbox("Timeframe:",["1 Month (21d)","3 Months (63d)","6 Months (126d)","1 Year (252d)"],index=1)
        with dd4:
            ov_indicator=st.selectbox("Panel 2 indicator:",
                ['RSI 14','RSI 9','MFI 14','Stoch %K','Williams %R','CCI 20','CMF 20'],index=0)

        days_map={"1 Month (21d)":21,"3 Months (63d)":63,"6 Months (126d)":126,"1 Year (252d)":252}
        days=days_map[timeframe]
        ticker_ns=sel_stock+'.NS'

        # ── Watchlist toggle ───────────────────────────────────────────────
        wl_col1,wl_col2=st.columns([1,5])
        with wl_col1:
            if sel_stock in st.session_state.watchlist:
                if st.button("★ Remove from Watchlist"):
                    st.session_state.watchlist.discard(sel_stock)
                    st.rerun()
            else:
                if st.button("☆ Add to Watchlist"):
                    st.session_state.watchlist.add(sel_stock)
                    st.rerun()

        # ── Stock KPIs ─────────────────────────────────────────────────────
        row=df[df['Ticker']==sel_stock]
        if not row.empty:
            r=row.iloc[0]
            chg=r.get('Chg_Pct',0); sig=r.get('Signal','NEUTRAL'); sc_val=int(r.get('Score',0))
            sig_cls=sig.replace(' ','-'); chg_sign='+' if chg>0 else ''
            w52pct=r.get('W52_HighPct',0)
            w52color='#F59E0B' if w52pct>-5 else '#94A3B8'

            dive_kpis=[
                kpi("Close",f"₹{r.get('Close',0):.2f}",r.get('Date',''),"kpi-cyan"),
                kpi("Day Change",f"{chg_sign}{chg:.2f}%","","kpi-green" if chg>0 else "kpi-red"),
                kpi("RSI 14",f"{r.get('RSI_14',0):.1f}","0-100","kpi-amber"),
                kpi("ADX 14",f"{r.get('ADX_14',0):.1f}","trend str.","kpi-purple"),
                kpi("52W High %",f"{w52pct:.1f}%","from 52W high","kpi-amber"),
                kpi("Score",f"{sc_val:+d}","composite","kpi-green" if sc_val>0 else "kpi-red"),
            ]
            st.markdown(
                '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:10px;">'
                +''.join(dive_kpis)+'</div>',unsafe_allow_html=True)
            st.markdown(
                f'<div style="margin-bottom:8px;">'
                f'<span class="sig sig-{sig_cls}">{sig}</span>'
                f'&nbsp;&nbsp;<span style="color:#334155;font-size:0.76rem;">{r.get("Sector","")}</span>'
                f'{"&nbsp;&nbsp;<span class=wl-badge>⭐ In Watchlist</span>" if sel_stock in st.session_state.watchlist else ""}'
                f'</div>',unsafe_allow_html=True)

        # ── Chart ──────────────────────────────────────────────────────────
        render_stock_chart(ticker_ns,history,days=days,overlay2=ov_indicator)

        # ── Comparison ─────────────────────────────────────────────────────
        if compare_mode:
            st.markdown('<div class="sec-title" style="margin-top:8px;">📊 Stock Comparison</div>',
                        unsafe_allow_html=True)
            cmp_col1,cmp_col2=st.columns([1,3])
            with cmp_col1:
                other_tickers=[t for t in tickers_clean if t!=sel_stock]
                cmp_stock=st.selectbox("Compare with:",other_tickers,index=0)
            render_comparison_cards(df,sel_stock,cmp_stock)
            render_comparison(sel_stock,cmp_stock,history,days=days)

        # ── All indicators ─────────────────────────────────────────────────
        if ticker_ns in history:
            latest=history[ticker_ns].iloc[-1].drop(['Open','High','Low','Close','Volume'],errors='ignore')
            ind_df=pd.DataFrame({'Indicator':latest.index,'Value':latest.values}).dropna()
            ind_df['Value']=ind_df['Value'].apply(
                lambda x:f"{x:+.3f}" if isinstance(x,float) else str(x))
            with st.expander("📋 All 50 Indicator Values"):
                st.dataframe(ind_df,use_container_width=True,hide_index=True,height=380)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 6 — Signal Overview
    # ══════════════════════════════════════════════════════════════════════════
    with tab6:
        col_a,col_b=st.columns([1,2])
        with col_a:
            st.markdown('<div class="sec-title">🍩 Signal Distribution</div>',unsafe_allow_html=True)
            render_signal_donut(filtered if not filtered.empty else df)

        with col_b:
            st.markdown('<div class="sec-title">⭐ Top Opportunities</div>',unsafe_allow_html=True)
            sub_a,sub_b,sub_c=st.tabs(["🟢 Top BUY","🔴 Top SELL","⭐ Watchlist"])

            OPP_COLS=['Ticker','Close','Chg_Pct','RSI_14','ADX_14','W52_HighPct','CMF_20','Score','Signal']
            fmt3={k:v for k,v in {'Close':'₹{:.2f}','Chg_Pct':'{:+.2f}%',
                                   'RSI_14':'{:.1f}','ADX_14':'{:.1f}',
                                   'W52_HighPct':'{:.1f}%','CMF_20':'{:.3f}'}.items()
                  if k in df.columns}

            def show_opp_table(sub_df):
                if sub_df.empty:
                    st.info("No stocks in this category."); return
                try:
                    valid_cols=[c for c in OPP_COLS if c in sub_df.columns]
                    sub_show=sub_df[valid_cols]
                    valid_fmt={k:v for k,v in fmt3.items() if k in sub_show.columns}
                    st.dataframe(
                        sub_show.style.map(style_signal,subset=['Signal'])
                                .format(valid_fmt,na_rep='—'),
                        use_container_width=True,hide_index=True,height=360)
                except Exception:
                    st.dataframe(sub_df[[c for c in OPP_COLS if c in sub_df.columns]],
                                 use_container_width=True,hide_index=True)

            with sub_a:
                show_opp_table(df[df['Signal'].isin(['STRONG BUY','BUY'])].nlargest(12,'Score'))
            with sub_b:
                show_opp_table(df[df['Signal'].isin(['STRONG SELL','SELL'])].nsmallest(12,'Score'))
            with sub_c:
                if st.session_state.watchlist:
                    show_opp_table(df[df['Ticker'].isin(st.session_state.watchlist)].sort_values('Score',ascending=False))
                else:
                    st.info("Your watchlist is empty. Go to Stock Deep Dive and click ☆ Add to Watchlist.")

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div class='footer-txt'>"
        "Data: Yahoo Finance (NSE) &nbsp;·&nbsp; 50 Indicators &nbsp;·&nbsp; "
        "1-Hour Cache &nbsp;·&nbsp; Smart Alerts &nbsp;·&nbsp; "
        "Sector Scorecard &nbsp;·&nbsp; ⚡ Nifty 100 Pro Screener v2"
        "</div>",unsafe_allow_html=True)

if __name__=='__main__':
    main()
