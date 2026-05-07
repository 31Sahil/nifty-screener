"""
Nifty 100 Technical Screener — Streamlit App
=============================================
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
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nifty 100 Screener",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — premium dark theme ──────────────────────────────────────────
st.markdown("""
<style>
/* Base dark background */
[data-testid="stAppViewContainer"] { background: #0d1117; }
[data-testid="stSidebar"]          { background: #161b22; border-right: 1px solid #30363d; }
[data-testid="stHeader"]           { background: transparent; }
.main .block-container             { padding-top: 1rem; max-width: 100%; }

/* Typography */
h1, h2, h3 { color: #e6edf3 !important; }
p, label, .stMarkdown { color: #8b949e !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px 16px !important;
}
[data-testid="metric-container"] label { color: #8b949e !important; font-size:0.78rem !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* Sidebar headers */
.sidebar-section {
    color: #58a6ff !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.4rem 0;
    padding-bottom: 4px;
    border-bottom: 1px solid #30363d;
}

/* Slider */
[data-testid="stSlider"] > div > div { background: #30363d; }

/* Selectbox / multiselect */
[data-testid="stSelectbox"] > div, [data-testid="stMultiSelect"] > div {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #30363d;
    border-radius: 8px;
}
[data-testid="stDataFrame"] th { background: #161b22 !important; color: #58a6ff !important; }
[data-testid="stDataFrame"] td { background: #0d1117 !important; color: #e6edf3 !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
}

/* Buttons */
.stButton button {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
}
.stButton button:hover { background: #30363d; border-color: #58a6ff; }

/* Signal badges */
.badge-strong-buy  { background:#0d4429; color:#3fb950; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-buy         { background:#122d22; color:#56d364; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-neutral     { background:#21262d; color:#8b949e; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-sell        { background:#3d1212; color:#f85149; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-strong-sell { background:#2d0f0f; color:#da3633; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:700; }

/* Title banner */
.screener-title {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 16px;
}
.screener-title h1 { margin:0; font-size:1.8rem !important; }
.screener-title p  { margin:4px 0 0 0; color:#8b949e !important; font-size:0.88rem !important; }
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

# ── Indicator Computation ─────────────────────────────────────────────────────
def _ewm(s, com):
    return s.ewm(com=com, min_periods=int(com)+1, adjust=False).mean()

def compute_all(df):
    """Compute all 50 indicators on a single stock's OHLCV DataFrame."""
    o, h, l, c, v = df['Open'], df['High'], df['Low'], df['Close'], df['Volume']
    out = pd.DataFrame(index=df.index)
    out['Open']  = o
    out['High']  = h
    out['Low']   = l
    out['Close'] = c
    out['Volume']= v

    # ── Daily change ─────────────────────────────────────────────────────
    out['Chg_Pct'] = c.pct_change() * 100

    # ── Moving averages ──────────────────────────────────────────────────
    for w in [20, 50, 200]:
        out[f'SMA_{w}'] = c.rolling(w).mean()
    for w in [9, 20, 50, 200]:
        out[f'EMA_{w}'] = c.ewm(span=w, adjust=False).mean()

    # DEMA, TEMA (20-day)
    e20 = c.ewm(span=20, adjust=False).mean()
    ee20 = e20.ewm(span=20, adjust=False).mean()
    eee20 = ee20.ewm(span=20, adjust=False).mean()
    out['DEMA_20'] = 2*e20 - ee20
    out['TEMA_20'] = 3*e20 - 3*ee20 + eee20

    # Hull MA 20
    wma_half = c.rolling(10).apply(lambda x: np.average(x, weights=range(1,11)), raw=True)
    wma_full = c.rolling(20).apply(lambda x: np.average(x, weights=range(1,21)), raw=True)
    hull_raw = 2*wma_half - wma_full
    n_sqrt = int(round(20**0.5))
    out['HullMA_20'] = hull_raw.rolling(n_sqrt).apply(
        lambda x: np.average(x, weights=range(1, n_sqrt+1)), raw=True)

    # VWAP 20
    tp = (h + l + c) / 3
    out['VWAP_20'] = (tp * v).rolling(20).sum() / v.rolling(20).sum()
    out['VWAP_Pct'] = (c - out['VWAP_20']) / out['VWAP_20'] * 100

    # ── Momentum ─────────────────────────────────────────────────────────
    for p in [9, 14]:
        d = c.diff()
        gain = _ewm(d.clip(lower=0), p-1)
        loss = _ewm((-d).clip(lower=0), p-1)
        out[f'RSI_{p}'] = 100 - 100/(1 + gain/loss)

    # MFI 14
    mf = tp * v
    pos = mf.where(tp > tp.shift(1), 0).rolling(14).sum()
    neg = mf.where(tp < tp.shift(1), 0).rolling(14).sum()
    out['MFI_14'] = 100 - 100/(1 + pos/neg.replace(0, np.nan))

    # Stochastic
    hh14 = h.rolling(14).max()
    ll14 = l.rolling(14).min()
    out['Stoch_K'] = 100*(c - ll14)/(hh14 - ll14).replace(0, np.nan)
    out['Stoch_D'] = out['Stoch_K'].rolling(3).mean()

    # Williams %R
    out['WillR_14'] = -100*(hh14 - c)/(hh14 - ll14).replace(0, np.nan)

    # CCI 20
    sma_tp20 = tp.rolling(20).mean()
    mad20 = tp.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    out['CCI_20'] = (tp - sma_tp20) / (0.015 * mad20)

    # ROC 10, 20
    for p in [10, 20]:
        out[f'ROC_{p}'] = (c - c.shift(p)) / c.shift(p) * 100

    # Chande Momentum Oscillator 14
    d = c.diff()
    su = d.clip(lower=0).rolling(14).sum()
    sd = (-d).clip(lower=0).rolling(14).sum()
    out['CMO_14'] = (su - sd) / (su + sd).replace(0, np.nan) * 100

    # TRIX 15
    e1 = c.ewm(span=15, adjust=False).mean()
    e2 = e1.ewm(span=15, adjust=False).mean()
    e3 = e2.ewm(span=15, adjust=False).mean()
    out['TRIX_15'] = e3.pct_change() * 100

    # Ultimate Oscillator
    bp = c - pd.concat([l, c.shift(1)], axis=1).min(axis=1)
    tr_ = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    a7  = bp.rolling(7).sum()  / tr_.rolling(7).sum()
    a14 = bp.rolling(14).sum() / tr_.rolling(14).sum()
    a28 = bp.rolling(28).sum() / tr_.rolling(28).sum()
    out['UltOsc'] = (4*a7 + 2*a14 + a28) / 7 * 100

    # MACD
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    out['MACD']      = ema12 - ema26
    out['MACD_Sig']  = out['MACD'].ewm(span=9, adjust=False).mean()
    out['MACD_Hist'] = out['MACD'] - out['MACD_Sig']

    # ── Volatility ───────────────────────────────────────────────────────
    # ATR 14
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    out['ATR_14']  = tr.ewm(com=13, min_periods=14, adjust=False).mean()
    out['ATR_Pct'] = out['ATR_14'] / c * 100

    # Bollinger Bands
    bb_mid = c.rolling(20).mean()
    bb_std = c.rolling(20).std()
    out['BB_Upper'] = bb_mid + 2*bb_std
    out['BB_Lower'] = bb_mid - 2*bb_std
    out['BB_Pct']   = (c - out['BB_Lower']) / (out['BB_Upper'] - out['BB_Lower']) * 100
    out['BB_Width'] = (out['BB_Upper'] - out['BB_Lower']) / bb_mid * 100

    # Keltner Channels (20, 2×ATR)
    kelt_mid = c.ewm(span=20, adjust=False).mean()
    out['Kelt_Upper'] = kelt_mid + 2*out['ATR_14']
    out['Kelt_Lower'] = kelt_mid - 2*out['ATR_14']
    out['Kelt_Pct']   = (c - out['Kelt_Lower']) / (out['Kelt_Upper'] - out['Kelt_Lower']) * 100

    # Donchian Channel 20
    out['Don_High']  = h.rolling(20).max()
    out['Don_Low']   = l.rolling(20).min()
    out['Don_Pct']   = (c - out['Don_Low']) / (out['Don_High'] - out['Don_Low']).replace(0, np.nan) * 100

    # Historical Volatility 20
    log_ret = np.log(c / c.shift(1))
    out['HV_20'] = log_ret.rolling(20).std() * np.sqrt(252) * 100

    # ── Trend Strength ───────────────────────────────────────────────────
    atr14 = out['ATR_14']
    up_m  = h.diff().clip(lower=0)
    dn_m  = (-l.diff()).clip(lower=0)
    pdm = up_m.where(up_m > dn_m, 0)
    ndm = dn_m.where(dn_m > up_m, 0)
    out['PDI'] = 100 * pdm.ewm(com=13, min_periods=14, adjust=False).mean() / atr14
    out['NDI'] = 100 * ndm.ewm(com=13, min_periods=14, adjust=False).mean() / atr14
    dx = (100*(out['PDI'] - out['NDI']).abs() / (out['PDI'] + out['NDI']).replace(0, np.nan))
    out['ADX_14'] = dx.ewm(com=13, min_periods=14, adjust=False).mean()

    # Aroon 25 — use nanargmax to handle NaN windows safely
    def _aroon_up(x):
        try: return (np.nanargmax(x) / 25) * 100
        except: return np.nan
    def _aroon_dn(x):
        try: return (np.nanargmin(x) / 25) * 100
        except: return np.nan
    out['Aroon_Up']   = h.rolling(26).apply(_aroon_up, raw=True)
    out['Aroon_Down'] = l.rolling(26).apply(_aroon_dn, raw=True)
    out['Aroon_Osc']  = out['Aroon_Up'] - out['Aroon_Down']

    # Supertrend (10, 3)
    atr10 = tr.ewm(com=9, min_periods=10, adjust=False).mean()
    mid = (h + l) / 2
    upper_band = mid + 3 * atr10
    lower_band = mid - 3 * atr10
    supertrend = pd.Series(np.nan, index=df.index)
    direction  = pd.Series(1, index=df.index)
    for i in range(1, len(df)):
        ub = upper_band.iloc[i]
        lb = lower_band.iloc[i]
        prev_st = supertrend.iloc[i-1]
        prev_ub = upper_band.iloc[i-1]
        prev_lb = lower_band.iloc[i-1]
        # adjust bands
        if lb < prev_lb or c.iloc[i-1] < prev_lb: lb = lb
        else: lb = prev_lb
        if ub > prev_ub or c.iloc[i-1] > prev_ub: ub = ub
        else: ub = prev_ub
        upper_band.iloc[i] = ub
        lower_band.iloc[i] = lb
        if pd.isna(prev_st) or prev_st == prev_ub:
            supertrend.iloc[i] = lb if c.iloc[i] > ub else ub
        else:
            supertrend.iloc[i] = lb if c.iloc[i] > lb else ub
        direction.iloc[i] = 1 if c.iloc[i] > supertrend.iloc[i] else -1
    out['Supertrend']    = supertrend
    out['ST_Direction']  = direction   # 1=bullish, -1=bearish

    # ── Volume ───────────────────────────────────────────────────────────
    # OBV
    out['OBV'] = (np.sign(c.diff()) * v).fillna(0).cumsum()

    # CMF 20
    mfm = ((c - l) - (h - c)) / (h - l).replace(0, np.nan)
    out['CMF_20'] = (mfm * v).rolling(20).sum() / v.rolling(20).sum()

    # Volume Ratio vs 20-day avg
    out['Vol_Ratio'] = v / v.rolling(20).mean()

    # Elder Ray
    ema13 = c.ewm(span=13, adjust=False).mean()
    out['Elder_Bull'] = h - ema13
    out['Elder_Bear'] = l - ema13

    # Pivot Points (based on previous day's H/L/C)
    out['Pivot_PP'] = (h.shift(1) + l.shift(1) + c.shift(1)) / 3
    out['Pivot_R1'] = 2*out['Pivot_PP'] - l.shift(1)
    out['Pivot_S1'] = 2*out['Pivot_PP'] - h.shift(1)
    out['Pivot_R2'] = out['Pivot_PP'] + (h.shift(1) - l.shift(1))
    out['Pivot_S2'] = out['Pivot_PP'] - (h.shift(1) - l.shift(1))

    # ── Signal Score ─────────────────────────────────────────────────────
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
    if score >= 8:   sig_label = 'STRONG BUY'
    elif score >= 4: sig_label = 'BUY'
    elif score <= -8: sig_label = 'STRONG SELL'
    elif score <= -4: sig_label = 'SELL'
    else:             sig_label = 'NEUTRAL'
    out['Signal'] = sig_label

    return out

# ── Data Fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    """Fetch 1 year of OHLCV and compute all indicators. Cached for 1 hour."""
    rows = []
    history = {}
    progress = st.progress(0, text="Loading Nifty 100 data from Yahoo Finance…")

    for i, ticker in enumerate(TICKERS):
        progress.progress((i+1)/len(TICKERS),
                          text=f"Processing {ticker.replace('.NS','')} ({i+1}/{len(TICKERS)})…")
        try:
            raw = yf.download(ticker, period='1y', interval='1d',
                              auto_adjust=True, progress=False)
            if raw.empty or len(raw) < 30:
                continue
            raw.columns = [c[0] if isinstance(c, tuple) else c for c in raw.columns]
            raw = raw[['Open','High','Low','Close','Volume']].dropna()
            ind = compute_all(raw)
            history[ticker] = ind   # full 1-year history for charts
            lat = ind.iloc[-1].to_dict()
            lat['Ticker']  = ticker.replace('.NS','')
            lat['Date']    = ind.index[-1].strftime('%d-%b-%Y')
            lat['Sector']  = TICKER_SECTOR.get(ticker, 'Others')
            rows.append(lat)
        except Exception:
            continue

    progress.empty()

    df = pd.DataFrame(rows)
    if df.empty:
        return df, history

    # Round numeric cols
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].round(2)
    return df, history

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar(df):
    with st.sidebar:
        st.markdown("## ⚙️ Screener Filters")

        # Signal filter
        st.markdown('<p class="sidebar-section">Signal</p>', unsafe_allow_html=True)
        all_signals = ['ALL','STRONG BUY','BUY','NEUTRAL','SELL','STRONG SELL']
        sel_signal = st.selectbox("Signal Filter", all_signals, index=0,
                                   label_visibility="collapsed")

        # Sector filter
        st.markdown('<p class="sidebar-section">Sector</p>', unsafe_allow_html=True)
        sectors = ['ALL'] + sorted(df['Sector'].unique().tolist()) if 'Sector' in df.columns else ['ALL']
        sel_sector = st.selectbox("Sector", sectors, index=0, label_visibility="collapsed")

        filters = {}

        def add_slider(label, col, default_min=None, default_max=None):
            if col not in df.columns: return
            vals = df[col].dropna()
            if vals.empty or len(vals) < 2: return
            mn, mx = float(vals.min()), float(vals.max())
            if mn >= mx: return
            # Clamp defaults strictly within actual data range to avoid invalid slider
            lo_def = float(np.clip(default_min if default_min is not None else mn, mn, mx))
            hi_def = float(np.clip(default_max if default_max is not None else mx, mn, mx))
            if lo_def >= hi_def:
                lo_def, hi_def = mn, mx   # fallback: show full range
            try:
                lo, hi = st.slider(label, min_value=mn, max_value=mx,
                                   value=(lo_def, hi_def),
                                   format="%.1f", label_visibility="visible")
                if lo > mn or hi < mx:
                    filters[col] = (lo, hi)
            except Exception:
                pass   # skip slider if data is still problematic

        # ── Momentum ─────────────────────────────────────────────────────
        st.markdown('<p class="sidebar-section">Momentum</p>', unsafe_allow_html=True)
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

        # ── MACD ─────────────────────────────────────────────────────────
        st.markdown('<p class="sidebar-section">MACD</p>', unsafe_allow_html=True)
        add_slider("MACD", "MACD")
        add_slider("MACD Histogram", "MACD_Hist")

        # ── Volatility ───────────────────────────────────────────────────
        st.markdown('<p class="sidebar-section">Volatility & Bands</p>', unsafe_allow_html=True)
        add_slider("ATR 14 (%)", "ATR_Pct", 0, 10)
        add_slider("Bollinger %B", "BB_Pct", -20, 120)
        add_slider("Bollinger Width %", "BB_Width", 0, 30)
        add_slider("Keltner %", "Kelt_Pct", -20, 120)
        add_slider("Donchian %", "Don_Pct", 0, 100)
        add_slider("Hist. Volatility 20", "HV_20", 0, 100)

        # ── Trend Strength ───────────────────────────────────────────────
        st.markdown('<p class="sidebar-section">Trend Strength</p>', unsafe_allow_html=True)
        add_slider("ADX 14", "ADX_14", 0, 60)
        add_slider("+DI 14", "PDI", 0, 60)
        add_slider("-DI 14", "NDI", 0, 60)
        add_slider("Aroon Up", "Aroon_Up", 0, 100)
        add_slider("Aroon Down", "Aroon_Down", 0, 100)
        add_slider("Aroon Oscillator", "Aroon_Osc", -100, 100)

        # ── Volume ───────────────────────────────────────────────────────
        st.markdown('<p class="sidebar-section">Volume</p>', unsafe_allow_html=True)
        add_slider("CMF 20", "CMF_20", -0.5, 0.5)
        add_slider("Volume Ratio", "Vol_Ratio", 0, 5)
        add_slider("VWAP % from Close", "VWAP_Pct", -20, 20)

        # ── Score ────────────────────────────────────────────────────────
        st.markdown('<p class="sidebar-section">Composite Score</p>', unsafe_allow_html=True)
        add_slider("Signal Score", "Score", -15, 15)

        return sel_signal, sel_sector, filters

# ── Apply Filters ─────────────────────────────────────────────────────────────
def apply_filters(df, sel_signal, sel_sector, filters):
    mask = pd.Series(True, index=df.index)
    if sel_signal != 'ALL':
        mask &= df['Signal'] == sel_signal
    if sel_sector != 'ALL' and 'Sector' in df.columns:
        mask &= df['Sector'] == sel_sector
    for col, (lo, hi) in filters.items():
        if col in df.columns:
            mask &= df[col].between(lo, hi, inclusive='both')
    return df[mask].copy()

# ── Signal Badge HTML ─────────────────────────────────────────────────────────
def badge(sig):
    cls = sig.lower().replace(' ','-')
    return f'<span class="badge-{cls}">{sig}</span>'

SIG_COLORS = {
    'STRONG BUY': '#3fb950', 'BUY': '#56d364', 'NEUTRAL': '#8b949e',
    'SELL': '#f85149', 'STRONG SELL': '#da3633',
}

# ── Stock Detail Chart ────────────────────────────────────────────────────────
def render_stock_chart(ticker_ns, history):
    ind = history.get(ticker_ns)
    if ind is None or len(ind) < 20:
        st.warning("Not enough data for chart.")
        return

    ind = ind.iloc[-90:]   # last 90 trading days

    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        row_heights=[0.45, 0.20, 0.20, 0.15],
        vertical_spacing=0.03,
        subplot_titles=["Price + Bollinger Bands", "RSI 14", "MACD", "Volume"]
    )

    # ── Candlestick ───────────────────────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=ind.index, open=ind['Open'], high=ind['High'],
        low=ind['Low'], close=ind['Close'],
        increasing_line_color='#3fb950', decreasing_line_color='#f85149',
        name='OHLC', showlegend=False), row=1, col=1)

    # Bollinger bands
    for band_col, color, dash in [('BB_Upper','#58a6ff','dash'),
                                   ('BB_Lower','#58a6ff','dash')]:
        if band_col in ind.columns:
            fig.add_trace(go.Scatter(x=ind.index, y=ind[band_col],
                line=dict(color=color, width=1, dash=dash),
                name=band_col, showlegend=False, opacity=0.6), row=1, col=1)

    # EMA 20, EMA 50
    for ema_col, color in [('EMA_20','#f0883e'),('EMA_50','#bc8cff')]:
        if ema_col in ind.columns:
            fig.add_trace(go.Scatter(x=ind.index, y=ind[ema_col],
                line=dict(color=color, width=1.5),
                name=ema_col, showlegend=True), row=1, col=1)

    # Supertrend
    if 'Supertrend' in ind.columns and 'ST_Direction' in ind.columns:
        bull = ind[ind['ST_Direction']>0]
        bear = ind[ind['ST_Direction']<0]
        for sub, color in [(bull,'#3fb950'),(bear,'#f85149')]:
            if not sub.empty:
                fig.add_trace(go.Scatter(
                    x=sub.index, y=sub['Supertrend'],
                    mode='markers', marker=dict(color=color, size=4, symbol='circle'),
                    name='Supertrend', showlegend=False), row=1, col=1)

    # ── RSI ───────────────────────────────────────────────────────────────
    if 'RSI_14' in ind.columns:
        fig.add_trace(go.Scatter(x=ind.index, y=ind['RSI_14'],
            line=dict(color='#f0883e', width=1.5),
            name='RSI 14'), row=2, col=1)
        for level, color in [(70,'#f85149'),(30,'#3fb950'),(50,'#30363d')]:
            fig.add_hline(y=level, line_dash='dash', line_color=color,
                          line_width=1, opacity=0.5, row=2, col=1)
        fig.update_yaxes(range=[0,100], row=2, col=1)

    # ── MACD ─────────────────────────────────────────────────────────────
    if 'MACD' in ind.columns and 'MACD_Sig' in ind.columns:
        colors = ['#3fb950' if v >= 0 else '#f85149'
                  for v in ind.get('MACD_Hist', [0]*len(ind))]
        fig.add_trace(go.Bar(x=ind.index, y=ind['MACD_Hist'],
            marker_color=colors, name='MACD Hist', showlegend=False), row=3, col=1)
        fig.add_trace(go.Scatter(x=ind.index, y=ind['MACD'],
            line=dict(color='#58a6ff', width=1.5), name='MACD'), row=3, col=1)
        fig.add_trace(go.Scatter(x=ind.index, y=ind['MACD_Sig'],
            line=dict(color='#f0883e', width=1.5), name='Signal'), row=3, col=1)
        fig.add_hline(y=0, line_dash='dash', line_color='#30363d',
                      line_width=1, row=3, col=1)

    # ── Volume ────────────────────────────────────────────────────────────
    vol_colors = ['#3fb950' if c >= o else '#f85149'
                  for c, o in zip(ind['Close'], ind['Open'])]
    fig.add_trace(go.Bar(x=ind.index, y=ind['Volume'],
        marker_color=vol_colors, name='Volume', showlegend=False), row=4, col=1)
    if 'Volume' in ind.columns:
        vol_ma = ind['Volume'].rolling(20).mean()
        fig.add_trace(go.Scatter(x=ind.index, y=vol_ma,
            line=dict(color='#f0883e', width=1),
            name='Vol MA 20', showlegend=False), row=4, col=1)

    fig.update_layout(
        height=680, template='plotly_dark',
        paper_bgcolor='#0d1117', plot_bgcolor='#0d1117',
        font=dict(color='#8b949e', size=11),
        legend=dict(bgcolor='#161b22', bordercolor='#30363d', borderwidth=1,
                    font=dict(size=10)),
        margin=dict(l=10, r=10, t=36, b=10),
        xaxis_rangeslider_visible=False,
    )
    for i in range(1,5):
        fig.update_xaxes(gridcolor='#21262d', row=i, col=1)
        fig.update_yaxes(gridcolor='#21262d', row=i, col=1)

    st.plotly_chart(fig, use_container_width=True)

# ── Market Heatmap ────────────────────────────────────────────────────────────
def render_heatmap(df):
    if df.empty or 'Chg_Pct' not in df.columns:
        st.info("No data for heatmap.")
        return
    df2 = df[['Ticker','Chg_Pct','Signal','Close','Sector']].dropna()
    fig = px.treemap(
        df2,
        path=['Sector','Ticker'],
        values=df2['Close'].abs(),
        color='Chg_Pct',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        hover_data={'Chg_Pct':':.2f', 'Close':':.2f', 'Signal':True},
        custom_data=['Ticker','Chg_Pct','Signal'],
    )
    fig.update_traces(
        texttemplate='<b>%{label}</b><br>%{customdata[1]:.1f}%',
        textfont_size=12,
    )
    fig.update_layout(
        height=520, template='plotly_dark',
        paper_bgcolor='#0d1117', plot_bgcolor='#0d1117',
        margin=dict(l=0, r=0, t=20, b=0),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(title='Chg%', tickfont=dict(color='#8b949e')),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Signal Distribution Chart ─────────────────────────────────────────────────
def render_signal_donut(df):
    if df.empty or 'Signal' not in df.columns: return
    counts = df['Signal'].value_counts().reindex(
        ['STRONG BUY','BUY','NEUTRAL','SELL','STRONG SELL'], fill_value=0)
    colors = ['#3fb950','#56d364','#8b949e','#f85149','#da3633']
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.65, marker_colors=colors,
        textinfo='label+value',
        hovertemplate='%{label}: %{value} stocks<extra></extra>',
    ))
    fig.update_layout(
        height=260, template='plotly_dark',
        paper_bgcolor='#0d1117', plot_bgcolor='#0d1117',
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(font=dict(size=10), bgcolor='#0d1117'),
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Display Columns ───────────────────────────────────────────────────────────
DISPLAY_COLS = {
    'Core':    ['Ticker','Date','Sector','Close','Chg_Pct','Signal','Score'],
    'Trend':   ['SMA_20','SMA_50','SMA_200','EMA_20','EMA_50','EMA_200',
                'DEMA_20','TEMA_20','HullMA_20','VWAP_20','VWAP_Pct'],
    'Momentum':['RSI_14','RSI_9','MFI_14','Stoch_K','Stoch_D','WillR_14',
                'CCI_20','ROC_10','ROC_20','CMO_14','TRIX_15','UltOsc'],
    'MACD':    ['MACD','MACD_Sig','MACD_Hist'],
    'Volatility':['ATR_14','ATR_Pct','BB_Pct','BB_Width','Kelt_Pct','Don_Pct','HV_20'],
    'Trend Strength':['ADX_14','PDI','NDI','Aroon_Up','Aroon_Down','Aroon_Osc'],
    'Volume':  ['OBV','CMF_20','Vol_Ratio','Elder_Bull','Elder_Bear'],
}

# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    # Title
    st.markdown("""
    <div class="screener-title">
        <h1>📊 Nifty 100 Technical Screener</h1>
        <p>50 indicators · Live NSE data via Yahoo Finance · Auto-refresh every hour</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    with st.spinner("Fetching live market data…"):
        df, history = load_data()

    if df.empty:
        st.error("Could not fetch data. Please check your internet connection.")
        st.stop()

    # Last updated
    last_date = df['Date'].iloc[0] if 'Date' in df.columns else 'N/A'

    # Sidebar filters
    sel_signal, sel_sector, filters = render_sidebar(df)

    # Apply filters
    filtered = apply_filters(df, sel_signal, sel_sector, filters)

    # ── Summary Metrics ───────────────────────────────────────────────────
    n_total     = len(df)
    n_shown     = len(filtered)
    n_adv       = (filtered['Chg_Pct'] > 0).sum() if 'Chg_Pct' in filtered.columns else 0
    n_dec       = (filtered['Chg_Pct'] < 0).sum() if 'Chg_Pct' in filtered.columns else 0
    n_buy       = (filtered['Signal'].isin(['BUY','STRONG BUY'])).sum()
    n_sell      = (filtered['Signal'].isin(['SELL','STRONG SELL'])).sum()
    n_neutral   = (filtered['Signal'] == 'NEUTRAL').sum()
    avg_rsi     = filtered['RSI_14'].mean() if 'RSI_14' in filtered.columns else 0
    avg_adx     = filtered['ADX_14'].mean() if 'ADX_14' in filtered.columns else 0

    c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns(9)
    c1.metric("Universe",    n_total)
    c2.metric("Showing",     n_shown)
    c3.metric("🟢 Advancing", n_adv)
    c4.metric("🔴 Declining", n_dec)
    c5.metric("BUY",         n_buy,   delta=f"+ {(filtered['Signal']=='STRONG BUY').sum()} Strong")
    c6.metric("SELL",        n_sell,  delta=f"- {(filtered['Signal']=='STRONG SELL').sum()} Strong")
    c7.metric("NEUTRAL",     n_neutral)
    c8.metric("Avg RSI 14",  f"{avg_rsi:.1f}")
    c9.metric("Avg ADX 14",  f"{avg_adx:.1f}")

    st.markdown(f"<p style='color:#8b949e;font-size:0.8rem;margin:4px 0 12px 0;'>"
                f"📅 Data as of: {last_date} &nbsp;·&nbsp; "
                f"Active filters: {len(filters)} indicator(s)"
                f"</p>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Screener Table", "🌡️ Market Heatmap", "📈 Stock Deep Dive", "🍩 Signal Overview"])

    # ── Tab 1: Screener Table ─────────────────────────────────────────────
    with tab1:
        if filtered.empty:
            st.warning("No stocks match the current filters. Adjust the sidebar sliders.")
        else:
            # Column group selector
            col_grp = st.selectbox(
                "Show indicator group:",
                list(DISPLAY_COLS.keys()),
                index=0,
                label_visibility="visible",
            )
            show_cols = DISPLAY_COLS[col_grp]
            # only keep cols that exist
            show_cols = [c for c in show_cols if c in filtered.columns]
            view = filtered[show_cols].sort_values('Score', ascending=False) \
                   if 'Score' in show_cols else filtered[show_cols]

            # Color-code Signal column
            def style_signal(val):
                colors = {
                    'STRONG BUY':  'background:#0d4429;color:#3fb950',
                    'BUY':         'background:#122d22;color:#56d364',
                    'NEUTRAL':     'background:#21262d;color:#8b949e',
                    'SELL':        'background:#3d1212;color:#f85149',
                    'STRONG SELL': 'background:#2d0f0f;color:#da3633',
                }
                return colors.get(val, '')

            def style_chg(val):
                try:
                    f = float(val)
                    return 'color:#3fb950' if f > 0 else ('color:#f85149' if f < 0 else '')
                except: return ''

            try:
                styled = view.style
                if 'Signal' in view.columns:
                    styled = styled.map(style_signal, subset=['Signal'])
                if 'Chg_Pct' in view.columns:
                    styled = styled.map(style_chg, subset=['Chg_Pct'])
                fmt = {}
                if 'Chg_Pct' in view.columns: fmt['Chg_Pct'] = '{:.2f}%'
                if 'Close'   in view.columns: fmt['Close']   = '₹{:.2f}'
                if fmt: styled = styled.format(fmt, na_rep='-')
                if 'Score' in view.columns:
                    styled = styled.background_gradient(
                        subset=['Score'], cmap='RdYlGn', vmin=-15, vmax=15)
                st.dataframe(styled, use_container_width=True, height=500,
                             hide_index=True)
            except Exception:
                st.dataframe(view, use_container_width=True, height=500,
                             hide_index=True)

            # Download
            csv = filtered.to_csv(index=False)
            st.download_button(
                "⬇️  Download filtered results (CSV)",
                data=csv,
                file_name=f"nifty100_screener_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )

    # ── Tab 2: Heatmap ───────────────────────────────────────────────────
    with tab2:
        st.markdown("#### 📦 Sector Heatmap — Daily Change %")
        st.caption("Box size = market price · Color = daily % change (green=up, red=down)")
        render_heatmap(filtered if not filtered.empty else df)

    # ── Tab 3: Stock Deep Dive ────────────────────────────────────────────
    with tab3:
        if history:
            tickers_clean = sorted([t.replace('.NS','') for t in history.keys()])
            # Default to top BUY stock
            default_stock = filtered.sort_values('Score', ascending=False)['Ticker'].iloc[0] \
                            if not filtered.empty else tickers_clean[0]
            sel_stock = st.selectbox("Select stock for deep dive:",
                                     tickers_clean,
                                     index=tickers_clean.index(default_stock)
                                           if default_stock in tickers_clean else 0)
            ticker_ns = sel_stock + '.NS'

            if ticker_ns in history:
                # Key metrics for selected stock
                row = df[df['Ticker']==sel_stock]
                if not row.empty:
                    r = row.iloc[0]
                    cols = st.columns(6)
                    cols[0].metric("Close ₹",   f"{r.get('Close','-'):.2f}")
                    cols[1].metric("Chg %",     f"{r.get('Chg_Pct',0):.2f}%",
                                   delta=f"{r.get('Chg_Pct',0):.2f}%")
                    cols[2].metric("RSI 14",    f"{r.get('RSI_14','-'):.1f}")
                    cols[3].metric("ADX 14",    f"{r.get('ADX_14','-'):.1f}")
                    cols[4].metric("Score",     f"{int(r.get('Score',0))}")
                    sig_val = r.get('Signal', 'NEUTRAL')
                    cols[5].metric("Signal",    sig_val)
                    st.markdown("---")

                render_stock_chart(ticker_ns, history)

                # All indicators table
                if ticker_ns in history:
                    latest = history[ticker_ns].iloc[-1].drop(
                        ['Open','High','Low','Close','Volume'], errors='ignore')
                    ind_df = pd.DataFrame({'Indicator': latest.index,
                                           'Value': latest.values}).dropna()
                    ind_df['Value'] = ind_df['Value'].apply(
                        lambda x: f"{x:.2f}" if isinstance(x, float) else str(x))
                    with st.expander("📋 All 50 indicator values"):
                        st.dataframe(ind_df, use_container_width=True,
                                     hide_index=True, height=400)

    # ── Tab 4: Signal Overview ────────────────────────────────────────────
    with tab4:
        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.markdown("#### Signal Distribution")
            render_signal_donut(filtered if not filtered.empty else df)

        with col_b:
            st.markdown("#### Top Opportunities")
            sub_tabs = st.tabs(["🟢 Top BUY", "🔴 Top SELL"])

            with sub_tabs[0]:
                top_buy = df[df['Signal'].isin(['STRONG BUY','BUY'])] \
                          .nlargest(10, 'Score')[
                              ['Ticker','Close','Chg_Pct','RSI_14','ADX_14',
                               'CMF_20','Score','Signal']]
                if not top_buy.empty:
                    try:
                        st.dataframe(
                            top_buy.style
                                .map(style_signal, subset=['Signal'])
                                .format({'Close':'₹{:.2f}','Chg_Pct':'{:.2f}%',
                                         'RSI_14':'{:.1f}','ADX_14':'{:.1f}',
                                         'CMF_20':'{:.3f}'}, na_rep='-'),
                            use_container_width=True, hide_index=True)
                    except Exception:
                        st.dataframe(top_buy, use_container_width=True, hide_index=True)

            with sub_tabs[1]:
                top_sell = df[df['Signal'].isin(['STRONG SELL','SELL'])] \
                           .nsmallest(10, 'Score')[
                               ['Ticker','Close','Chg_Pct','RSI_14','ADX_14',
                                'CMF_20','Score','Signal']]
                if not top_sell.empty:
                    try:
                        st.dataframe(
                            top_sell.style
                                .map(style_signal, subset=['Signal'])
                                .format({'Close':'₹{:.2f}','Chg_Pct':'{:.2f}%',
                                         'RSI_14':'{:.1f}','ADX_14':'{:.1f}',
                                         'CMF_20':'{:.3f}'}, na_rep='-'),
                            use_container_width=True, hide_index=True)
                    except Exception:
                        st.dataframe(top_sell, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown(
        "<p style='color:#30363d;font-size:0.75rem;text-align:center;'>"
        "Data: Yahoo Finance (NSE) · Indicators: 50 · "
        "Cache: 1 hour · Built with Streamlit</p>",
        unsafe_allow_html=True)

if __name__ == '__main__':
    main()
