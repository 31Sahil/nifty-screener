"""
Nifty 100 Technical Screener — Premium Edition
================================================
50 indicators · Live Yahoo Finance data · Daily auto-refresh
Deploy free on Streamlit Cloud
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

# ── Premium CSS — Deep Navy Glassmorphism ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ══ Base ══════════════════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }
html, body { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #040D20 0%, #080F26 50%, #040D20 100%) !important;
    background-attachment: fixed !important;
}
[data-testid="stHeader"] { background: transparent !important; }
.main .block-container { padding-top: 0.6rem !important; max-width:100% !important; }

/* Dot grid overlay */
[data-testid="stMain"]::before {
    content: '';
    position: fixed; inset: 0;
    background-image: radial-gradient(circle, rgba(0,201,255,0.035) 1px, transparent 1px);
    background-size: 30px 30px;
    pointer-events: none;
    z-index: 0;
}

/* ══ Sidebar ══ */
[data-testid="stSidebar"] {
    background: rgba(4, 10, 25, 0.97) !important;
    border-right: 1px solid rgba(0,201,255,0.1) !important;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #E2E8F0 !important; }
[data-testid="stSidebar"] label { color: #94A3B8 !important; font-size:0.78rem !important; }

/* ══ Typography ══ */
h1,h2,h3,h4,h5,h6 { color:#F1F5F9 !important; font-family:'Inter',sans-serif !important; }
.stMarkdown p, p { color:#94A3B8 !important; }

/* ══ Selectbox ══ */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,201,255,0.18) !important;
    border-radius: 8px !important; color: #CBD5E1 !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(0,201,255,0.45) !important;
    box-shadow: 0 0 12px rgba(0,201,255,0.08) !important;
}

/* ══ Slider ══ */
[data-testid="stSlider"] label { color:#94A3B8 !important; font-size:0.76rem !important; }

/* ══ Tabs ══ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(0,201,255,0.1) !important;
    border-radius: 12px !important;
    padding: 4px !important; gap: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #4B5563 !important;
    font-weight: 500 !important; font-size: 0.84rem !important;
    padding: 8px 20px !important; border: none !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,201,255,0.12), rgba(139,92,246,0.12)) !important;
    color: #00C9FF !important;
    border: 1px solid rgba(0,201,255,0.22) !important;
    box-shadow: 0 0 16px rgba(0,201,255,0.08) !important;
}

/* ══ Dataframe ══ */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,201,255,0.1) !important;
    border-radius: 12px !important; overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: rgba(0,201,255,0.06) !important;
    color: #00C9FF !important; font-weight:600 !important;
    font-size:0.72rem !important; letter-spacing:0.06em !important;
    text-transform: uppercase !important;
}
[data-testid="stDataFrame"] td {
    background: rgba(4,13,32,0.85) !important;
    color: #CBD5E1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.81rem !important;
}

/* ══ Expander ══ */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(0,201,255,0.1) !important;
    border-radius: 12px !important;
}

/* ══ Buttons ══ */
.stButton button {
    background: linear-gradient(135deg,rgba(0,201,255,0.1),rgba(139,92,246,0.1)) !important;
    color: #00C9FF !important;
    border: 1px solid rgba(0,201,255,0.22) !important;
    border-radius: 8px !important;
    font-family:'Inter',sans-serif !important; font-weight:500 !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: linear-gradient(135deg,rgba(0,201,255,0.18),rgba(139,92,246,0.18)) !important;
    box-shadow: 0 0 20px rgba(0,201,255,0.12) !important;
}
[data-testid="stDownloadButton"] button {
    background: rgba(16,185,129,0.08) !important;
    color: #10B981 !important;
    border: 1px solid rgba(16,185,129,0.28) !important;
    border-radius: 8px !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(16,185,129,0.15) !important;
    box-shadow: 0 0 16px rgba(16,185,129,0.1) !important;
}

/* ══ Progress bar ══ */
[data-testid="stProgressBar"] > div { background:rgba(0,201,255,0.1) !important; border-radius:4px !important; }
[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#00C9FF,#8B5CF6) !important; border-radius:4px !important; }

/* ══ Alert ══ */
[data-testid="stAlert"] {
    border-radius:10px !important;
    background:rgba(0,201,255,0.04) !important;
    border-left:3px solid rgba(0,201,255,0.4) !important;
}

/* ══ Scrollbar ══ */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background:rgba(0,201,255,0.18); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:rgba(0,201,255,0.36); }

/* ══ Hide default st.metric ══ */
[data-testid="metric-container"] { display:none !important; }

/* ══ Custom Components ══════════════════════════════════════════════════════ */

/* Header */
.hdr {
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(135deg,rgba(0,201,255,0.055) 0%,rgba(139,92,246,0.055) 100%);
    border: 1px solid rgba(0,201,255,0.14);
    border-radius: 18px; padding: 22px 32px; margin-bottom: 14px;
    position: relative; overflow: hidden;
}
.hdr::before {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse at 15% 50%,rgba(0,201,255,0.06) 0%,transparent 60%),
                radial-gradient(ellipse at 85% 50%,rgba(139,92,246,0.06) 0%,transparent 60%);
    pointer-events:none;
}
.hdr-icon { font-size:2rem; margin-right:16px; filter:drop-shadow(0 0 10px rgba(0,201,255,0.5)); }
.hdr-title {
    font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(135deg,#F1F5F9 0%,#CBD5E1 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    line-height: 1.1; font-family:'Inter',sans-serif;
}
.hdr-accent {
    background: linear-gradient(135deg,#00C9FF 0%,#8B5CF6 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hdr-sub { color:#475569; font-size:0.84rem; margin-top:5px; font-weight:400; }
.hdr-right { text-align:right; }
.live-badge {
    display:inline-flex; align-items:center; gap:7px;
    background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.28);
    color:#10B981; font-size:0.7rem; font-weight:700; letter-spacing:0.1em;
    padding:4px 14px; border-radius:20px; margin-bottom:6px;
}
.live-dot {
    width:6px; height:6px; background:#10B981; border-radius:50%;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; box-shadow:0 0 6px #10B981; }
    50% { opacity:0.3; box-shadow:none; }
}
.hdr-date { color:#334155; font-size:0.76rem; font-family:'JetBrains Mono',monospace; }

/* KPI row */
.kpi-row {
    display: grid; grid-template-columns: repeat(9,1fr);
    gap: 10px; margin-bottom: 12px;
}
.kpi-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 14px 16px;
    position: relative; overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.kpi-card::after {
    content:''; position:absolute; top:0; left:0; right:0;
    height:2px; border-radius:2px 2px 0 0;
    background: var(--c, rgba(0,201,255,0.45));
}
.kpi-card:hover { transform:translateY(-2px); border-color:rgba(0,201,255,0.18); }
.kpi-label {
    font-size:0.65rem; font-weight:700; letter-spacing:0.09em;
    text-transform:uppercase; color:#334155; margin-bottom:5px;
}
.kpi-val {
    font-size:1.55rem; font-weight:700; color:#F1F5F9;
    font-family:'JetBrains Mono',monospace; line-height:1.1;
}
.kpi-sub { font-size:0.68rem; color:#334155; margin-top:3px; font-family:'JetBrains Mono',monospace; }

/* Sentiment bar */
.sent-wrap {
    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);
    border-radius:12px; padding:12px 20px; margin-bottom:12px;
    display:flex; align-items:center; gap:14px;
}
.sent-lbl { font-size:0.67rem; font-weight:700; text-transform:uppercase;
            letter-spacing:0.09em; color:#334155; white-space:nowrap; }
.sent-track { flex:1; height:7px; border-radius:7px; background:rgba(255,255,255,0.04); display:flex; overflow:hidden; }
.sent-green { background:linear-gradient(90deg,#059669,#10B981); }
.sent-gray  { background:rgba(100,116,139,0.35); }
.sent-red   { background:linear-gradient(90deg,#F43F5E,#EF4444); }
.sent-stat-row { display:flex; gap:16px; }
.sent-stat { font-size:0.74rem; font-family:'JetBrains Mono',monospace; white-space:nowrap; }

/* Signal badges */
.sig {
    display:inline-flex; align-items:center;
    padding:2px 11px; border-radius:20px;
    font-size:0.7rem; font-weight:700; letter-spacing:0.04em;
}
.sig-STRONG-BUY  { background:rgba(16,185,129,0.12); color:#10B981; border:1px solid rgba(16,185,129,0.3); }
.sig-BUY         { background:rgba(52,211,153,0.1);  color:#34D399; border:1px solid rgba(52,211,153,0.25); }
.sig-NEUTRAL     { background:rgba(100,116,139,0.12); color:#94A3B8; border:1px solid rgba(100,116,139,0.25); }
.sig-SELL        { background:rgba(244,63,94,0.1);   color:#F43F5E; border:1px solid rgba(244,63,94,0.25); }
.sig-STRONG-SELL { background:rgba(220,38,38,0.1);   color:#EF4444; border:1px solid rgba(220,38,38,0.25); }

/* Sidebar section */
.sb-sec {
    font-size:0.67rem; font-weight:700; letter-spacing:0.12em;
    text-transform:uppercase; color:#00C9FF !important;
    margin:1.3rem 0 0.45rem 0; padding-bottom:5px;
    border-bottom:1px solid rgba(0,201,255,0.13);
}

/* Section title */
.sec-title {
    font-size:0.8rem; font-weight:700; letter-spacing:0.08em;
    text-transform:uppercase; color:#00C9FF;
    margin-bottom:10px; display:flex; align-items:center; gap:8px;
}
.sec-title::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg,rgba(0,201,255,0.3),transparent);
}

.footer-txt { color:rgba(51,65,85,0.7); font-size:0.72rem; text-align:center; margin-top:1rem; }
</style>
""", unsafe_allow_html=True)

# ── Nifty 100 Universe ────────────────────────────────────────────────────────
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

# ── Indicator Computation (unchanged) ─────────────────────────────────────────
def _ewm(s, com):
    return s.ewm(com=com, min_periods=int(com)+1, adjust=False).mean()

def compute_all(df):
    o, h, l, c, v = df['Open'], df['High'], df['Low'], df['Close'], df['Volume']
    out = pd.DataFrame(index=df.index)
    out['Open'] = o; out['High'] = h; out['Low'] = l; out['Close'] = c; out['Volume'] = v
    out['Chg_Pct'] = c.pct_change() * 100

    for w in [20, 50, 200]:
        out[f'SMA_{w}'] = c.rolling(w).mean()
    for w in [9, 20, 50, 200]:
        out[f'EMA_{w}'] = c.ewm(span=w, adjust=False).mean()

    e20 = c.ewm(span=20, adjust=False).mean()
    ee20 = e20.ewm(span=20, adjust=False).mean()
    eee20 = ee20.ewm(span=20, adjust=False).mean()
    out['DEMA_20'] = 2*e20 - ee20
    out['TEMA_20'] = 3*e20 - 3*ee20 + eee20

    wma_half = c.rolling(10).apply(lambda x: np.average(x, weights=range(1,11)), raw=True)
    wma_full = c.rolling(20).apply(lambda x: np.average(x, weights=range(1,21)), raw=True)
    hull_raw = 2*wma_half - wma_full
    n_sqrt = int(round(20**0.5))
    out['HullMA_20'] = hull_raw.rolling(n_sqrt).apply(
        lambda x: np.average(x, weights=range(1, n_sqrt+1)), raw=True)

    tp = (h + l + c) / 3
    out['VWAP_20'] = (tp * v).rolling(20).sum() / v.rolling(20).sum()
    out['VWAP_Pct'] = (c - out['VWAP_20']) / out['VWAP_20'] * 100

    for p in [9, 14]:
        d = c.diff()
        gain = _ewm(d.clip(lower=0), p-1)
        loss = _ewm((-d).clip(lower=0), p-1)
        out[f'RSI_{p}'] = 100 - 100/(1 + gain/loss)

    mf = tp * v
    pos = mf.where(tp > tp.shift(1), 0).rolling(14).sum()
    neg = mf.where(tp < tp.shift(1), 0).rolling(14).sum()
    out['MFI_14'] = 100 - 100/(1 + pos/neg.replace(0, np.nan))

    hh14 = h.rolling(14).max()
    ll14 = l.rolling(14).min()
    out['Stoch_K'] = 100*(c - ll14)/(hh14 - ll14).replace(0, np.nan)
    out['Stoch_D'] = out['Stoch_K'].rolling(3).mean()
    out['WillR_14'] = -100*(hh14 - c)/(hh14 - ll14).replace(0, np.nan)

    sma_tp20 = tp.rolling(20).mean()
    mad20 = tp.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    out['CCI_20'] = (tp - sma_tp20) / (0.015 * mad20)

    for p in [10, 20]:
        out[f'ROC_{p}'] = (c - c.shift(p)) / c.shift(p) * 100

    d = c.diff()
    su = d.clip(lower=0).rolling(14).sum()
    sd = (-d).clip(lower=0).rolling(14).sum()
    out['CMO_14'] = (su - sd) / (su + sd).replace(0, np.nan) * 100

    e1 = c.ewm(span=15, adjust=False).mean()
    e2 = e1.ewm(span=15, adjust=False).mean()
    e3 = e2.ewm(span=15, adjust=False).mean()
    out['TRIX_15'] = e3.pct_change() * 100

    bp = c - pd.concat([l, c.shift(1)], axis=1).min(axis=1)
    tr_ = pd.concat([h-l, (h-c.shift(1)).abs(), (l-c.shift(1)).abs()], axis=1).max(axis=1)
    a7  = bp.rolling(7).sum()  / tr_.rolling(7).sum()
    a14 = bp.rolling(14).sum() / tr_.rolling(14).sum()
    a28 = bp.rolling(28).sum() / tr_.rolling(28).sum()
    out['UltOsc'] = (4*a7 + 2*a14 + a28) / 7 * 100

    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    out['MACD']      = ema12 - ema26
    out['MACD_Sig']  = out['MACD'].ewm(span=9, adjust=False).mean()
    out['MACD_Hist'] = out['MACD'] - out['MACD_Sig']

    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    out['ATR_14']  = tr.ewm(com=13, min_periods=14, adjust=False).mean()
    out['ATR_Pct'] = out['ATR_14'] / c * 100

    bb_mid = c.rolling(20).mean()
    bb_std = c.rolling(20).std()
    out['BB_Upper'] = bb_mid + 2*bb_std
    out['BB_Lower'] = bb_mid - 2*bb_std
    out['BB_Pct']   = (c - out['BB_Lower']) / (out['BB_Upper'] - out['BB_Lower']) * 100
    out['BB_Width'] = (out['BB_Upper'] - out['BB_Lower']) / bb_mid * 100

    kelt_mid = c.ewm(span=20, adjust=False).mean()
    out['Kelt_Upper'] = kelt_mid + 2*out['ATR_14']
    out['Kelt_Lower'] = kelt_mid - 2*out['ATR_14']
    out['Kelt_Pct']   = (c - out['Kelt_Lower']) / (out['Kelt_Upper'] - out['Kelt_Lower']) * 100

    out['Don_High'] = h.rolling(20).max()
    out['Don_Low']  = l.rolling(20).min()
    out['Don_Pct']  = (c - out['Don_Low']) / (out['Don_High'] - out['Don_Low']).replace(0, np.nan) * 100

    log_ret = np.log(c / c.shift(1))
    out['HV_20'] = log_ret.rolling(20).std() * np.sqrt(252) * 100

    atr14 = out['ATR_14']
    up_m = h.diff().clip(lower=0); dn_m = (-l.diff()).clip(lower=0)
    pdm = up_m.where(up_m > dn_m, 0); ndm = dn_m.where(dn_m > up_m, 0)
    out['PDI'] = 100 * pdm.ewm(com=13, min_periods=14, adjust=False).mean() / atr14
    out['NDI'] = 100 * ndm.ewm(com=13, min_periods=14, adjust=False).mean() / atr14
    dx = (100*(out['PDI'] - out['NDI']).abs() / (out['PDI'] + out['NDI']).replace(0, np.nan))
    out['ADX_14'] = dx.ewm(com=13, min_periods=14, adjust=False).mean()

    def _aroon_up(x):
        try: return (np.nanargmax(x) / 25) * 100
        except: return np.nan
    def _aroon_dn(x):
        try: return (np.nanargmin(x) / 25) * 100
        except: return np.nan
    out['Aroon_Up']   = h.rolling(26).apply(_aroon_up, raw=True)
    out['Aroon_Down'] = l.rolling(26).apply(_aroon_dn, raw=True)
    out['Aroon_Osc']  = out['Aroon_Up'] - out['Aroon_Down']

    atr10 = tr.ewm(com=9, min_periods=10, adjust=False).mean()
    mid = (h + l) / 2
    upper_band = mid + 3 * atr10
    lower_band = mid - 3 * atr10
    supertrend = pd.Series(np.nan, index=df.index)
    direction  = pd.Series(1, index=df.index)
    for i in range(1, len(df)):
        ub = upper_band.iloc[i]; lb = lower_band.iloc[i]
        prev_st = supertrend.iloc[i-1]
        prev_ub = upper_band.iloc[i-1]; prev_lb = lower_band.iloc[i-1]
        if lb < prev_lb or c.iloc[i-1] < prev_lb: lb = lb
        else: lb = prev_lb
        if ub > prev_ub or c.iloc[i-1] > prev_ub: ub = ub
        else: ub = prev_ub
        upper_band.iloc[i] = ub; lower_band.iloc[i] = lb
        if pd.isna(prev_st) or prev_st == prev_ub:
            supertrend.iloc[i] = lb if c.iloc[i] > ub else ub
        else:
            supertrend.iloc[i] = lb if c.iloc[i] > lb else ub
        direction.iloc[i] = 1 if c.iloc[i] > supertrend.iloc[i] else -1
    out['Supertrend']   = supertrend
    out['ST_Direction'] = direction

    out['OBV'] = (np.sign(c.diff()) * v).fillna(0).cumsum()

    mfm = ((c - l) - (h - c)) / (h - l).replace(0, np.nan)
    out['CMF_20'] = (mfm * v).rolling(20).sum() / v.rolling(20).sum()
    out['Vol_Ratio'] = v / v.rolling(20).mean()

    ema13 = c.ewm(span=13, adjust=False).mean()
    out['Elder_Bull'] = h - ema13
    out['Elder_Bear'] = l - ema13

    out['Pivot_PP'] = (h.shift(1) + l.shift(1) + c.shift(1)) / 3
    out['Pivot_R1'] = 2*out['Pivot_PP'] - l.shift(1)
    out['Pivot_S1'] = 2*out['Pivot_PP'] - h.shift(1)
    out['Pivot_R2'] = out['Pivot_PP'] + (h.shift(1) - l.shift(1))
    out['Pivot_S2'] = out['Pivot_PP'] - (h.shift(1) - l.shift(1))

    def score_latest(r):
        s = 0
        cl = r.get('Close', np.nan)
        for col in ['SMA_20','SMA_50','SMA_200','EMA_20','EMA_50','EMA_200']:
            v_ = r.get(col, np.nan)
            if pd.notna(v_) and pd.notna(cl): s += 1 if cl > v_ else -1
        rsi = r.get('RSI_14', np.nan)
        if pd.notna(rsi):
            if rsi < 30: s += 2
            elif rsi > 70: s -= 2
        mfi = r.get('MFI_14', np.nan)
        if pd.notna(mfi):
            if mfi < 20: s += 2
            elif mfi > 80: s -= 2
        macd = r.get('MACD', np.nan); sig = r.get('MACD_Sig', np.nan)
        if pd.notna(macd) and pd.notna(sig): s += 1 if macd > sig else -1
        bb = r.get('BB_Pct', np.nan)
        if pd.notna(bb):
            if bb < 0: s += 2
            elif bb > 100: s -= 2
            elif bb < 20: s += 1
            elif bb > 80: s -= 1
        sk = r.get('Stoch_K', np.nan)
        if pd.notna(sk):
            if sk < 20: s += 1
            elif sk > 80: s -= 1
        cci = r.get('CCI_20', np.nan)
        if pd.notna(cci):
            if cci < -100: s += 1
            elif cci > 100: s -= 1
        wr = r.get('WillR_14', np.nan)
        if pd.notna(wr):
            if wr < -80: s += 1
            elif wr > -20: s -= 1
        roc = r.get('ROC_10', np.nan)
        if pd.notna(roc): s += 1 if roc > 0 else -1
        adx = r.get('ADX_14', np.nan); pdi = r.get('PDI', np.nan); ndi = r.get('NDI', np.nan)
        if pd.notna(adx) and adx > 25 and pd.notna(pdi) and pd.notna(ndi):
            s += 1 if pdi > ndi else -1
        cmf = r.get('CMF_20', np.nan)
        if pd.notna(cmf): s += 1 if cmf > 0 else -1
        st_dir = r.get('ST_Direction', np.nan)
        if pd.notna(st_dir): s += 1 if st_dir > 0 else -1
        return int(s)

    score = score_latest(out.iloc[-1])
    out['Score'] = score
    if score >= 8:    sig_label = 'STRONG BUY'
    elif score >= 4:  sig_label = 'BUY'
    elif score <= -8: sig_label = 'STRONG SELL'
    elif score <= -4: sig_label = 'SELL'
    else:             sig_label = 'NEUTRAL'
    out['Signal'] = sig_label
    return out

# ── Data Fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    rows = []; history = {}
    progress = st.progress(0, text="Initialising market data feed…")
    for i, ticker in enumerate(TICKERS):
        progress.progress(
            (i+1)/len(TICKERS),
            text=f"⚡ Processing {ticker.replace('.NS','')}  ({i+1}/{len(TICKERS)})")
        try:
            raw = yf.download(ticker, period='1y', interval='1d',
                              auto_adjust=True, progress=False)
            if raw.empty or len(raw) < 30: continue
            raw.columns = [c[0] if isinstance(c, tuple) else c for c in raw.columns]
            raw = raw[['Open','High','Low','Close','Volume']].dropna()
            ind = compute_all(raw)
            history[ticker] = ind
            lat = ind.iloc[-1].to_dict()
            lat['Ticker'] = ticker.replace('.NS','')
            lat['Date']   = ind.index[-1].strftime('%d-%b-%Y')
            lat['Sector'] = TICKER_SECTOR.get(ticker, 'Others')
            rows.append(lat)
        except Exception:
            continue
    progress.empty()
    df = pd.DataFrame(rows)
    if df.empty: return df, history
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].round(2)
    return df, history

# ── Filter Application ────────────────────────────────────────────────────────
def apply_filters(df, sel_signal, sel_sector, filters):
    mask = pd.Series(True, index=df.index)
    if sel_signal != 'ALL': mask &= df['Signal'] == sel_signal
    if sel_sector != 'ALL' and 'Sector' in df.columns:
        mask &= df['Sector'] == sel_sector
    for col, (lo, hi) in filters.items():
        if col in df.columns:
            mask &= df[col].between(lo, hi, inclusive='both')
    return df[mask].copy()

# ── Signal styling ────────────────────────────────────────────────────────────
SIG_PALETTE = {
    'STRONG BUY':  '#10B981',
    'BUY':         '#34D399',
    'NEUTRAL':     '#94A3B8',
    'SELL':        '#F43F5E',
    'STRONG SELL': '#EF4444',
}

def style_signal(val):
    m = {
        'STRONG BUY':  'background:rgba(16,185,129,0.15);color:#10B981',
        'BUY':         'background:rgba(52,211,153,0.12);color:#34D399',
        'NEUTRAL':     'background:rgba(100,116,139,0.12);color:#94A3B8',
        'SELL':        'background:rgba(244,63,94,0.12);color:#F43F5E',
        'STRONG SELL': 'background:rgba(239,68,68,0.12);color:#EF4444',
    }
    return m.get(val, '')

def style_chg(val):
    try:
        f = float(val)
        return 'color:#10B981' if f > 0 else ('color:#F43F5E' if f < 0 else '')
    except: return ''

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar(df):
    with st.sidebar:
        st.markdown("""
        <div style="padding:14px 4px 6px 4px;">
          <div style="font-size:1rem;font-weight:700;color:#F1F5F9;letter-spacing:-0.01em;">
            ⚙ Filter Controls
          </div>
          <div style="font-size:0.74rem;color:#334155;margin-top:3px;">
            Narrow down the 95-stock universe
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="sb-sec">🎯 Signal & Sector</p>', unsafe_allow_html=True)
        all_signals = ['ALL','STRONG BUY','BUY','NEUTRAL','SELL','STRONG SELL']
        sel_signal = st.selectbox("Signal", all_signals, index=0,
                                   label_visibility="visible")
        sectors = ['ALL'] + sorted(df['Sector'].unique().tolist()) if 'Sector' in df.columns else ['ALL']
        sel_sector = st.selectbox("Sector", sectors, index=0,
                                   label_visibility="visible")

        filters = {}

        def add_slider(label, col, default_min=None, default_max=None):
            if col not in df.columns: return
            vals = df[col].dropna()
            if vals.empty or len(vals) < 2: return
            mn, mx = float(vals.min()), float(vals.max())
            if mn >= mx: return
            lo_def = float(np.clip(default_min if default_min is not None else mn, mn, mx))
            hi_def = float(np.clip(default_max if default_max is not None else mx, mn, mx))
            if lo_def >= hi_def: lo_def, hi_def = mn, mx
            try:
                lo, hi = st.slider(label, min_value=mn, max_value=mx,
                                   value=(lo_def, hi_def), format="%.1f",
                                   label_visibility="visible")
                if lo > mn or hi < mx: filters[col] = (lo, hi)
            except Exception:
                pass

        st.markdown('<p class="sb-sec">📈 Momentum</p>', unsafe_allow_html=True)
        add_slider("RSI 14", "RSI_14", 0, 100)
        add_slider("RSI 9 (fast)", "RSI_9", 0, 100)
        add_slider("MFI 14", "MFI_14", 0, 100)
        add_slider("Stoch %K", "Stoch_K", 0, 100)
        add_slider("Stoch %D", "Stoch_D", 0, 100)
        add_slider("Williams %R", "WillR_14", -100, 0)
        add_slider("CCI 20", "CCI_20", -300, 300)
        add_slider("ROC 10%", "ROC_10", -30, 30)
        add_slider("ROC 20%", "ROC_20", -40, 40)
        add_slider("Chande MO", "CMO_14", -100, 100)
        add_slider("TRIX 15", "TRIX_15", -1, 1)
        add_slider("Ultimate Osc", "UltOsc", 0, 100)

        st.markdown('<p class="sb-sec">〰 MACD</p>', unsafe_allow_html=True)
        add_slider("MACD Line", "MACD")
        add_slider("MACD Histogram", "MACD_Hist")

        st.markdown('<p class="sb-sec">🌊 Volatility & Bands</p>', unsafe_allow_html=True)
        add_slider("ATR 14 (%)", "ATR_Pct", 0, 10)
        add_slider("Bollinger %B", "BB_Pct", -20, 120)
        add_slider("Bollinger Width %", "BB_Width", 0, 30)
        add_slider("Keltner %", "Kelt_Pct", -20, 120)
        add_slider("Donchian %", "Don_Pct", 0, 100)
        add_slider("Hist. Volatility 20", "HV_20", 0, 100)

        st.markdown('<p class="sb-sec">📡 Trend Strength</p>', unsafe_allow_html=True)
        add_slider("ADX 14", "ADX_14", 0, 60)
        add_slider("+DI 14", "PDI", 0, 60)
        add_slider("-DI 14", "NDI", 0, 60)
        add_slider("Aroon Up", "Aroon_Up", 0, 100)
        add_slider("Aroon Down", "Aroon_Down", 0, 100)
        add_slider("Aroon Osc", "Aroon_Osc", -100, 100)

        st.markdown('<p class="sb-sec">📦 Volume</p>', unsafe_allow_html=True)
        add_slider("CMF 20", "CMF_20", -0.5, 0.5)
        add_slider("Volume Ratio", "Vol_Ratio", 0, 5)
        add_slider("VWAP % from Close", "VWAP_Pct", -20, 20)

        st.markdown('<p class="sb-sec">🎲 Composite Score</p>', unsafe_allow_html=True)
        add_slider("Signal Score", "Score", -15, 15)

        st.markdown("---")
        if filters:
            st.markdown(f"<div style='font-size:0.74rem;color:#00C9FF;'>"
                        f"✦ {len(filters)} active filter(s)</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:0.74rem;color:#334155;'>"
                        "No filters active — showing all</div>", unsafe_allow_html=True)

        return sel_signal, sel_sector, filters

# ── KPI Cards ─────────────────────────────────────────────────────────────────
def render_kpi(label, value, sub="", cls="kpi-cyan"):
    return (f'<div class="kpi-card {cls}">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-val">{value}</div>'
            f'<div class="kpi-sub">{sub}</div>'
            f'</div>')

# ── Sentiment Bar ─────────────────────────────────────────────────────────────
def render_sentiment(df):
    if df.empty or 'Signal' not in df.columns: return
    n = len(df)
    if n == 0: return
    n_buy  = (df['Signal'].isin(['BUY','STRONG BUY'])).sum()
    n_neu  = (df['Signal'] == 'NEUTRAL').sum()
    n_sell = (df['Signal'].isin(['SELL','STRONG SELL'])).sum()
    w_buy  = n_buy  / n * 100
    w_neu  = n_neu  / n * 100
    w_sell = n_sell / n * 100

    bull_color = "#10B981" if w_buy >= w_sell else "#F43F5E"
    mood_lbl   = "BULLISH" if w_buy > w_sell else ("BEARISH" if w_sell > w_buy else "NEUTRAL")
    mood_color = "#10B981" if mood_lbl == "BULLISH" else ("#F43F5E" if mood_lbl == "BEARISH" else "#94A3B8")

    html = f"""
    <div class="sent-wrap">
      <div class="sent-lbl">Market<br>Mood</div>
      <div style="font-size:0.95rem;font-weight:800;color:{mood_color};
                  font-family:'Inter',sans-serif;white-space:nowrap;min-width:80px;">
        {mood_lbl}
      </div>
      <div class="sent-track">
        <div class="sent-seg sent-green" style="width:{w_buy:.1f}%"></div>
        <div class="sent-seg sent-gray"  style="width:{w_neu:.1f}%"></div>
        <div class="sent-seg sent-red"   style="width:{w_sell:.1f}%"></div>
      </div>
      <div class="sent-stat-row">
        <div class="sent-stat" style="color:#10B981;">▲ {n_buy} BUY</div>
        <div class="sent-stat" style="color:#94A3B8;">— {n_neu} NEUTRAL</div>
        <div class="sent-stat" style="color:#F43F5E;">▼ {n_sell} SELL</div>
      </div>
    </div>"""
    st.markdown(html, unsafe_allow_html=True)

# ── Stock Chart ───────────────────────────────────────────────────────────────
CHART_BG   = '#040D20'
CHART_GRID = 'rgba(255,255,255,0.04)'
C_GREEN    = '#10B981'
C_RED      = '#F43F5E'
C_CYAN     = '#00C9FF'
C_AMBER    = '#F59E0B'
C_PURPLE   = '#8B5CF6'
C_VIOLET   = '#A78BFA'

def render_stock_chart(ticker_ns, history):
    ind = history.get(ticker_ns)
    if ind is None or len(ind) < 20:
        st.warning("Not enough data available for this stock.")
        return
    ind = ind.iloc[-90:]

    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        row_heights=[0.45, 0.20, 0.20, 0.15],
        vertical_spacing=0.025,
        subplot_titles=["  Price · Bollinger Bands · EMA 20/50 · Supertrend",
                        "  RSI 14",
                        "  MACD (12,26,9)",
                        "  Volume"])

    # ── Candlestick ────────────────────────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=ind.index, open=ind['Open'], high=ind['High'],
        low=ind['Low'], close=ind['Close'],
        increasing_line_color=C_GREEN,
        decreasing_line_color=C_RED,
        increasing_fillcolor=C_GREEN,
        decreasing_fillcolor=C_RED,
        name='OHLC', showlegend=False), row=1, col=1)

    # Bollinger fill
    if 'BB_Upper' in ind.columns and 'BB_Lower' in ind.columns:
        fig.add_trace(go.Scatter(
            x=ind.index, y=ind['BB_Upper'], mode='lines',
            line=dict(color=C_CYAN, width=1, dash='dot'),
            name='BB Upper', showlegend=False, opacity=0.5), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=ind.index, y=ind['BB_Lower'], mode='lines',
            line=dict(color=C_CYAN, width=1, dash='dot'),
            fill='tonexty', fillcolor='rgba(0,201,255,0.04)',
            name='BB Lower', showlegend=False, opacity=0.5), row=1, col=1)

    # EMA lines
    for col, color, lbl in [('EMA_20', C_AMBER, 'EMA 20'), ('EMA_50', C_PURPLE, 'EMA 50')]:
        if col in ind.columns:
            fig.add_trace(go.Scatter(
                x=ind.index, y=ind[col],
                line=dict(color=color, width=1.5),
                name=lbl, showlegend=True), row=1, col=1)

    # Supertrend dots
    if 'Supertrend' in ind.columns and 'ST_Direction' in ind.columns:
        for sub, color in [(ind[ind['ST_Direction']>0], C_GREEN),
                           (ind[ind['ST_Direction']<0], C_RED)]:
            if not sub.empty:
                fig.add_trace(go.Scatter(
                    x=sub.index, y=sub['Supertrend'],
                    mode='markers',
                    marker=dict(color=color, size=3.5, symbol='circle',
                                line=dict(width=0)),
                    name='Supertrend', showlegend=False), row=1, col=1)

    # ── RSI ────────────────────────────────────────────────────────────────
    if 'RSI_14' in ind.columns:
        fig.add_trace(go.Scatter(
            x=ind.index, y=ind['RSI_14'],
            line=dict(color=C_AMBER, width=1.8),
            fill='tozeroy', fillcolor='rgba(245,158,11,0.06)',
            name='RSI 14'), row=2, col=1)
        for level, color in [(70, C_RED), (30, C_GREEN), (50, 'rgba(255,255,255,0.1)')]:
            fig.add_hline(y=level, line_dash='dash', line_color=color,
                          line_width=1, opacity=0.6, row=2, col=1)
        fig.update_yaxes(range=[0, 100], row=2, col=1)

    # ── MACD ───────────────────────────────────────────────────────────────
    if 'MACD' in ind.columns and 'MACD_Sig' in ind.columns:
        hist_vals = ind.get('MACD_Hist', pd.Series([0]*len(ind)))
        bar_colors = [C_GREEN if v >= 0 else C_RED for v in hist_vals]
        fig.add_trace(go.Bar(
            x=ind.index, y=hist_vals,
            marker_color=bar_colors, marker_line_width=0,
            opacity=0.7, name='Hist', showlegend=False), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=ind.index, y=ind['MACD'],
            line=dict(color=C_CYAN, width=1.6),
            name='MACD'), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=ind.index, y=ind['MACD_Sig'],
            line=dict(color=C_VIOLET, width=1.6),
            name='Signal'), row=3, col=1)
        fig.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.1)',
                      line_width=1, row=3, col=1)

    # ── Volume ─────────────────────────────────────────────────────────────
    vol_colors = [C_GREEN if c_ >= o_ else C_RED
                  for c_, o_ in zip(ind['Close'], ind['Open'])]
    fig.add_trace(go.Bar(
        x=ind.index, y=ind['Volume'],
        marker_color=vol_colors, marker_line_width=0,
        opacity=0.65, name='Volume', showlegend=False), row=4, col=1)
    if 'Volume' in ind.columns:
        fig.add_trace(go.Scatter(
            x=ind.index, y=ind['Volume'].rolling(20).mean(),
            line=dict(color=C_AMBER, width=1.2, dash='dash'),
            name='Vol MA20', showlegend=False), row=4, col=1)

    # ── Layout ─────────────────────────────────────────────────────────────
    fig.update_layout(
        height=680,
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        font=dict(family='Inter, sans-serif', color='#64748B', size=11),
        legend=dict(bgcolor='rgba(4,13,32,0.8)', bordercolor='rgba(0,201,255,0.15)',
                    borderwidth=1, font=dict(size=10), x=0.01, y=0.99),
        margin=dict(l=8, r=8, t=30, b=8),
        xaxis_rangeslider_visible=False,
    )
    for ax_n in ['xaxis','xaxis2','xaxis3','xaxis4']:
        fig.update_layout({ax_n: dict(gridcolor=CHART_GRID, showgrid=True, zeroline=False,
                                      showspikes=True, spikecolor='rgba(0,201,255,0.25)',
                                      spikethickness=1)})
    for ax_n in ['yaxis','yaxis2','yaxis3','yaxis4']:
        fig.update_layout({ax_n: dict(gridcolor=CHART_GRID, showgrid=True, zeroline=False)})

    # Subplot title styling
    for ann in fig.layout.annotations:
        ann.font.color = '#475569'
        ann.font.size  = 10

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ── Market Heatmap ────────────────────────────────────────────────────────────
def render_heatmap(df):
    if df.empty or 'Chg_Pct' not in df.columns:
        st.info("No data for heatmap."); return
    df2 = df[['Ticker','Chg_Pct','Signal','Close','Sector']].dropna()
    fig = px.treemap(
        df2, path=['Sector','Ticker'],
        values=df2['Close'].abs(),
        color='Chg_Pct',
        color_continuous_scale=[[0,'#7f1d1d'],[0.35,'#EF4444'],
                                 [0.5,'#1e293b'],
                                 [0.65,'#059669'],[1,'#064e3b']],
        color_continuous_midpoint=0,
        hover_data={'Chg_Pct':':.2f','Close':':.2f','Signal':True},
        custom_data=['Ticker','Chg_Pct','Signal'],
    )
    fig.update_traces(
        texttemplate='<b>%{label}</b><br>%{customdata[1]:.1f}%',
        textfont=dict(family='JetBrains Mono', size=11),
        marker_line_color='rgba(0,0,0,0.4)', marker_line_width=1.5,
    )
    fig.update_layout(
        height=540,
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        margin=dict(l=0, r=0, t=20, b=0),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title=dict(text='Δ%', font=dict(color='#64748B', size=11)),
            tickfont=dict(color='#64748B', family='JetBrains Mono'),
            thickness=14, len=0.7,
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ── Signal Donut ──────────────────────────────────────────────────────────────
def render_signal_donut(df):
    if df.empty or 'Signal' not in df.columns: return
    order  = ['STRONG BUY','BUY','NEUTRAL','SELL','STRONG SELL']
    counts = df['Signal'].value_counts().reindex(order, fill_value=0)
    colors = [C_GREEN, '#34D399', '#475569', C_RED, '#EF4444']
    total  = counts.sum()
    dominant = counts.idxmax() if total > 0 else 'NEUTRAL'
    dom_color = SIG_PALETTE.get(dominant, '#94A3B8')

    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.68,
        marker=dict(colors=colors,
                    line=dict(color=CHART_BG, width=2)),
        textinfo='label+value',
        textfont=dict(family='Inter', size=11, color='#94A3B8'),
        hovertemplate='%{label}: <b>%{value}</b> stocks<extra></extra>',
        pull=[0.04 if v == counts.max() else 0 for v in counts.values],
    ))
    fig.add_annotation(
        text=f'<b>{dominant}</b>',
        x=0.5, y=0.52, showarrow=False,
        font=dict(size=12, color=dom_color, family='Inter'),
        xanchor='center')
    fig.add_annotation(
        text=f'{total} stocks',
        x=0.5, y=0.42, showarrow=False,
        font=dict(size=10, color='#334155', family='JetBrains Mono'),
        xanchor='center')
    fig.update_layout(
        height=280,
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(font=dict(size=10, family='Inter', color='#64748B'),
                    bgcolor=CHART_BG),
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ── Display Column Groups ─────────────────────────────────────────────────────
DISPLAY_COLS = {
    '⭐ Core':         ['Ticker','Date','Sector','Close','Chg_Pct','Signal','Score'],
    '📊 Moving Avgs':  ['Ticker','SMA_20','SMA_50','SMA_200','EMA_20','EMA_50','EMA_200',
                        'DEMA_20','TEMA_20','HullMA_20','VWAP_20','VWAP_Pct'],
    '🚀 Momentum':     ['Ticker','RSI_14','RSI_9','MFI_14','Stoch_K','Stoch_D','WillR_14',
                        'CCI_20','ROC_10','ROC_20','CMO_14','TRIX_15','UltOsc'],
    '〰 MACD':         ['Ticker','MACD','MACD_Sig','MACD_Hist'],
    '🌊 Volatility':   ['Ticker','ATR_14','ATR_Pct','BB_Pct','BB_Width','Kelt_Pct','Don_Pct','HV_20'],
    '📡 Trend':        ['Ticker','ADX_14','PDI','NDI','Aroon_Up','Aroon_Down','Aroon_Osc'],
    '📦 Volume':       ['Ticker','OBV','CMF_20','Vol_Ratio','Elder_Bull','Elder_Bear'],
}

# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    # ── Load data ────────────────────────────────────────────────────────────
    with st.spinner("Connecting to live market feed…"):
        df, history = load_data()

    if df.empty:
        st.error("⚠️ Unable to fetch market data. Please check your internet connection.")
        st.stop()

    last_date = df['Date'].iloc[0] if 'Date' in df.columns else 'N/A'

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hdr">
      <div style="display:flex;align-items:center;">
        <div class="hdr-icon">⚡</div>
        <div>
          <div class="hdr-title">NIFTY 100 <span class="hdr-accent">PRO SCREENER</span></div>
          <div class="hdr-sub">50 Technical Indicators &nbsp;·&nbsp; Live NSE Data via Yahoo Finance &nbsp;·&nbsp; 1-Hour Auto-Refresh</div>
        </div>
      </div>
      <div class="hdr-right">
        <div class="live-badge"><span class="live-dot"></span>LIVE DATA</div><br>
        <div class="hdr-date">Last close: {last_date}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar filters ──────────────────────────────────────────────────────
    sel_signal, sel_sector, filters = render_sidebar(df)
    filtered = apply_filters(df, sel_signal, sel_sector, filters)

    # ── Compute KPI values ───────────────────────────────────────────────────
    n_total   = len(df)
    n_shown   = len(filtered)
    n_adv     = int((filtered['Chg_Pct'] > 0).sum()) if 'Chg_Pct' in filtered.columns else 0
    n_dec     = int((filtered['Chg_Pct'] < 0).sum()) if 'Chg_Pct' in filtered.columns else 0
    n_sbuy    = int((filtered['Signal'] == 'STRONG BUY').sum())
    n_buy     = int((filtered['Signal'].isin(['BUY','STRONG BUY'])).sum())
    n_sell    = int((filtered['Signal'].isin(['SELL','STRONG SELL'])).sum())
    n_ssell   = int((filtered['Signal'] == 'STRONG SELL').sum())
    n_neutral = int((filtered['Signal'] == 'NEUTRAL').sum())
    avg_rsi   = filtered['RSI_14'].mean() if 'RSI_14' in filtered.columns else 0
    avg_adx   = filtered['ADX_14'].mean() if 'ADX_14' in filtered.columns else 0
    avg_score = filtered['Score'].mean() if 'Score' in filtered.columns else 0

    # ── KPI Row ──────────────────────────────────────────────────────────────
    kpis = [
        render_kpi("Universe",   str(n_total),  "Nifty 100",   "kpi-cyan"),
        render_kpi("Showing",    str(n_shown),  f"{len(filters)} filter(s)", "kpi-purple"),
        render_kpi("▲ Advancing", str(n_adv),  "today",        "kpi-green"),
        render_kpi("▼ Declining", str(n_dec),  "today",        "kpi-red"),
        render_kpi("BUY Signals", str(n_buy),  f"incl {n_sbuy} strong","kpi-green"),
        render_kpi("SELL Signals",str(n_sell), f"incl {n_ssell} strong","kpi-red"),
        render_kpi("Neutral",    str(n_neutral),"no signal",   "kpi-slate"),
        render_kpi("Avg RSI 14", f"{avg_rsi:.1f}", "0-100",    "kpi-amber"),
        render_kpi("Avg ADX 14", f"{avg_adx:.1f}", "trend str.","kpi-purple"),
    ]
    st.markdown('<div class="kpi-row">' + ''.join(kpis) + '</div>', unsafe_allow_html=True)

    # ── Sentiment Bar ────────────────────────────────────────────────────────
    render_sentiment(filtered if not filtered.empty else df)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋  Screener",
        "🌡️  Market Heatmap",
        "📈  Stock Deep Dive",
        "🍩  Signal Overview",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # Tab 1 — Screener Table
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
        if filtered.empty:
            st.warning("⚠️ No stocks match the current filters. Adjust the sidebar controls.")
        else:
            col_left, col_right = st.columns([3, 1])
            with col_left:
                col_grp = st.selectbox(
                    "Indicator group to display:",
                    list(DISPLAY_COLS.keys()), index=0)
            with col_right:
                sort_asc = st.selectbox("Sort by Score:", ["↓ Descending", "↑ Ascending"], index=0)

            show_cols = [c for c in DISPLAY_COLS[col_grp] if c in filtered.columns]
            view = filtered[show_cols]
            if 'Score' in show_cols:
                view = view.sort_values('Score', ascending=(sort_asc == "↑ Ascending"))

            try:
                styled = view.style
                if 'Signal' in view.columns:
                    styled = styled.map(style_signal, subset=['Signal'])
                if 'Chg_Pct' in view.columns:
                    styled = styled.map(style_chg, subset=['Chg_Pct'])
                fmt = {}
                if 'Chg_Pct' in view.columns: fmt['Chg_Pct'] = '{:+.2f}%'
                if 'Close'   in view.columns: fmt['Close']   = '₹{:.2f}'
                if fmt: styled = styled.format(fmt, na_rep='—')
                if 'Score' in view.columns:
                    styled = styled.background_gradient(
                        subset=['Score'], cmap='RdYlGn', vmin=-15, vmax=15)
                st.dataframe(styled, use_container_width=True, height=480, hide_index=True)
            except Exception:
                st.dataframe(view, use_container_width=True, height=480, hide_index=True)

            c_dl, c_info = st.columns([1, 3])
            with c_dl:
                st.download_button(
                    "⬇ Export to CSV",
                    data=filtered.to_csv(index=False),
                    file_name=f"nifty100_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )
            with c_info:
                st.markdown(
                    f"<div style='color:#334155;font-size:0.76rem;padding-top:10px;'>"
                    f"Showing <b style='color:#00C9FF'>{n_shown}</b> of {n_total} stocks"
                    f"  ·  Sort: {sort_asc}</div>",
                    unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # Tab 2 — Heatmap
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<div class="sec-title">🌡 Sector Heatmap — Daily Change %</div>',
                    unsafe_allow_html=True)
        st.markdown("<div style='color:#334155;font-size:0.76rem;margin-bottom:8px;'>"
                    "Box size = stock price · Colour = daily % change</div>",
                    unsafe_allow_html=True)
        render_heatmap(filtered if not filtered.empty else df)

    # ════════════════════════════════════════════════════════════════════════
    # Tab 3 — Stock Deep Dive
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        if not history:
            st.info("No history loaded."); return

        tickers_clean = sorted([t.replace('.NS','') for t in history.keys()])
        default_stock = (filtered.sort_values('Score', ascending=False)['Ticker'].iloc[0]
                         if not filtered.empty else tickers_clean[0])

        sel_stock = st.selectbox(
            "Select stock:",
            tickers_clean,
            index=tickers_clean.index(default_stock)
                  if default_stock in tickers_clean else 0)
        ticker_ns = sel_stock + '.NS'

        row = df[df['Ticker'] == sel_stock]
        if not row.empty:
            r = row.iloc[0]
            chg  = r.get('Chg_Pct', 0)
            sig  = r.get('Signal', 'NEUTRAL')
            sc   = int(r.get('Score', 0))
            sig_cls = sig.replace(' ', '-')
            chg_color = C_GREEN if chg > 0 else (C_RED if chg < 0 else '#94A3B8')
            chg_sign  = '+' if chg > 0 else ''

            dive_kpis = [
                render_kpi("Close Price",  f"₹{r.get('Close',0):.2f}",  r.get('Date',''), "kpi-cyan"),
                render_kpi("Day Change",   f"{chg_sign}{chg:.2f}%",     "", "kpi-green" if chg>0 else "kpi-red"),
                render_kpi("RSI 14",       f"{r.get('RSI_14',0):.1f}",  "0-100",        "kpi-amber"),
                render_kpi("ADX 14",       f"{r.get('ADX_14',0):.1f}",  "trend str.",   "kpi-purple"),
                render_kpi("MACD Hist",    f"{r.get('MACD_Hist',0):.2f}","momentum",     "kpi-cyan"),
                render_kpi("Score",        f"{sc:+d}",                   "composite",    "kpi-green" if sc>0 else "kpi-red"),
            ]
            # 6-column mini-KPI row
            st.markdown(
                '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:12px;">'
                + ''.join(dive_kpis) + '</div>',
                unsafe_allow_html=True)
            st.markdown(
                f'<div style="margin-bottom:8px;">'
                f'<span class="sig sig-{sig_cls}">{sig}</span>'
                f'&nbsp;&nbsp;<span style="color:#334155;font-size:0.76rem;">'
                f'{r.get("Sector","")}</span></div>',
                unsafe_allow_html=True)

        render_stock_chart(ticker_ns, history)

        # All indicators
        if ticker_ns in history:
            latest = history[ticker_ns].iloc[-1].drop(
                ['Open','High','Low','Close','Volume'], errors='ignore')
            ind_df = pd.DataFrame({'Indicator': latest.index, 'Value': latest.values}).dropna()
            ind_df['Value'] = ind_df['Value'].apply(
                lambda x: f"{x:+.3f}" if isinstance(x, float) else str(x))
            with st.expander("📋 All 50 Indicator Values"):
                st.dataframe(ind_df, use_container_width=True, hide_index=True, height=400)

    # ════════════════════════════════════════════════════════════════════════
    # Tab 4 — Signal Overview
    # ════════════════════════════════════════════════════════════════════════
    with tab4:
        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.markdown('<div class="sec-title">🍩 Signal Distribution</div>',
                        unsafe_allow_html=True)
            render_signal_donut(filtered if not filtered.empty else df)

        with col_b:
            st.markdown('<div class="sec-title">⭐ Top Opportunities</div>',
                        unsafe_allow_html=True)
            sub_a, sub_b = st.tabs(["🟢 Top BUY", "🔴 Top SELL"])

            OPP_COLS = ['Ticker','Close','Chg_Pct','RSI_14','ADX_14','CMF_20','Score','Signal']

            with sub_a:
                top_buy = (df[df['Signal'].isin(['STRONG BUY','BUY'])]
                           .nlargest(12, 'Score')
                           [[c for c in OPP_COLS if c in df.columns]])
                if not top_buy.empty:
                    try:
                        fmt2 = {k: v for k, v in
                                {'Close':'₹{:.2f}','Chg_Pct':'{:+.2f}%',
                                 'RSI_14':'{:.1f}','ADX_14':'{:.1f}',
                                 'CMF_20':'{:.3f}'}.items()
                                if k in top_buy.columns}
                        st.dataframe(
                            top_buy.style
                                .map(style_signal, subset=['Signal'])
                                .format(fmt2, na_rep='—'),
                            use_container_width=True, hide_index=True, height=380)
                    except Exception:
                        st.dataframe(top_buy, use_container_width=True, hide_index=True)
                else:
                    st.info("No BUY signals in current filter.")

            with sub_b:
                top_sell = (df[df['Signal'].isin(['STRONG SELL','SELL'])]
                            .nsmallest(12, 'Score')
                            [[c for c in OPP_COLS if c in df.columns]])
                if not top_sell.empty:
                    try:
                        fmt2 = {k: v for k, v in
                                {'Close':'₹{:.2f}','Chg_Pct':'{:+.2f}%',
                                 'RSI_14':'{:.1f}','ADX_14':'{:.1f}',
                                 'CMF_20':'{:.3f}'}.items()
                                if k in top_sell.columns}
                        st.dataframe(
                            top_sell.style
                                .map(style_signal, subset=['Signal'])
                                .format(fmt2, na_rep='—'),
                            use_container_width=True, hide_index=True, height=380)
                    except Exception:
                        st.dataframe(top_sell, use_container_width=True, hide_index=True)
                else:
                    st.info("No SELL signals in current filter.")

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div class='footer-txt'>"
        "Data: Yahoo Finance (NSE) &nbsp;·&nbsp; 50 Indicators &nbsp;·&nbsp; "
        "1-Hour Cache &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; "
        "⚡ Nifty 100 Pro Screener"
        "</div>",
        unsafe_allow_html=True)

if __name__ == '__main__':
    main()
