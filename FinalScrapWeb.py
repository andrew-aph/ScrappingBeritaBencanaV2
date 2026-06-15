import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import re
import json
import plotly.graph_objects as go

# =====================================================
# CONFIG PAGE
# =====================================================

st.set_page_config(
    page_title="SIBERNA — Sistem Informasi Berita Bencana Nasional",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS — ADAPTIVE LIGHT/DARK MODE
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Outfit:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

:root {
    --bg-primary:       #0d1117;
    --bg-secondary:     #161b22;
    --bg-card:          #1c2230;
    --bg-card-hover:    #212d3d;
    --border:           rgba(255,255,255,0.08);
    --border-accent:    rgba(251,146,60,0.45);
    --accent-primary:   #fb923c;
    --accent-red:       #f87171;
    --accent-green:     #34d399;
    --accent-blue:      #60a5fa;
    --accent-yellow:    #fbbf24;
    --accent-purple:    #a78bfa;
    --text-primary:     #e2e8f0;
    --text-secondary:   #94a3b8;
    --text-muted:       #475569;
    --grid-line:        rgba(255,255,255,0.025);
    --shadow-card:      0 4px 24px rgba(0,0,0,0.4);
    --sidebar-top-bar:  linear-gradient(90deg, #fb923c, #f43f5e);
}

@media (prefers-color-scheme: light) {
    :root {
        --bg-primary:       #f8fafc;
        --bg-secondary:     #ffffff;
        --bg-card:          #ffffff;
        --bg-card-hover:    #f1f5f9;
        --border:           rgba(15,23,42,0.09);
        --border-accent:    rgba(234,88,12,0.35);
        --accent-primary:   #ea580c;
        --accent-red:       #dc2626;
        --accent-green:     #059669;
        --accent-blue:      #2563eb;
        --accent-yellow:    #d97706;
        --accent-purple:    #7c3aed;
        --text-primary:     #0f172a;
        --text-secondary:   #475569;
        --text-muted:       #94a3b8;
        --grid-line:        rgba(15,23,42,0.04);
        --shadow-card:      0 2px 16px rgba(15,23,42,0.08);
        --sidebar-top-bar:  linear-gradient(90deg, #ea580c, #e11d48);
    }
}

.stApp {
    background-color: var(--bg-primary) !important;
    background-image:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 44px 44px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px;
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}

[data-testid="stSidebar"]::before {
    content: "";
    display: block;
    height: 3px;
    background: var(--sidebar-top-bar);
    margin-bottom: 0;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

.sidebar-section-header {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent-primary) !important;
    border-bottom: 1px solid var(--border-accent);
    padding-bottom: 6px;
    margin: 20px 0 12px 0;
}

.main-header {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-primary);
    border-radius: 8px;
    padding: 24px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-card);
}

.main-header::before {
    content: "SIBERNA";
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Outfit', sans-serif;
    font-size: 80px;
    font-weight: 800;
    color: var(--accent-primary);
    opacity: 0.04;
    letter-spacing: -2px;
    pointer-events: none;
}

.main-header-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    color: var(--accent-primary);
    text-transform: uppercase;
    margin-bottom: 6px;
}

.main-header h1 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.5px !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
}

.main-header-sub {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 6px;
}

.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: var(--accent-red);
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
    box-shadow: var(--shadow-card);
}

.metric-card:hover {
    background: var(--bg-card-hover);
    border-color: rgba(251,146,60,0.3);
    box-shadow: 0 8px 32px rgba(251,146,60,0.08);
}

.metric-card::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    border-radius: 8px 8px 0 0;
}

.metric-card.orange::after { background: linear-gradient(90deg, var(--accent-primary), var(--accent-yellow)); }
.metric-card.red::after    { background: linear-gradient(90deg, var(--accent-red), #fb7185); }
.metric-card.green::after  { background: linear-gradient(90deg, var(--accent-green), #6ee7b7); }
.metric-card.blue::after   { background: linear-gradient(90deg, var(--accent-blue), #93c5fd); }

.metric-card-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 10px;
}

.metric-card-value {
    font-family: 'Outfit', sans-serif;
    font-size: 36px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}

.metric-card-value.orange { color: var(--accent-primary); }
.metric-card-value.red    { color: var(--accent-red); }
.metric-card-value.green  { color: var(--accent-green); }
.metric-card-value.blue   { color: var(--accent-blue); }

.metric-card-desc {
    font-size: 11px;
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-weight: 700;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--text-secondary) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 12px 20px !important;
    margin-right: 4px !important;
    transition: all 0.2s !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--accent-primary) !important;
    border-bottom: 2px solid var(--accent-primary) !important;
    background: rgba(251,146,60,0.06) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: rgba(128,128,128,0.05) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

div.stButton > button,
div.stDownloadButton > button,
div.stLinkButton > a {
    background: transparent !important;
    border: 1px solid var(--accent-primary) !important;
    color: var(--accent-primary) !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    padding: 10px 20px !important;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stLinkButton > a:hover {
    background: rgba(251,146,60,0.1) !important;
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 20px rgba(251,146,60,0.15) !important;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-primary), #ea580c) !important;
    color: #fff !important;
    border: none !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(251,146,60,0.25) !important;
}

div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 25px rgba(251,146,60,0.4) !important;
    transform: translateY(-1px);
}

div.stDownloadButton > button::before {
    font-family: "Font Awesome 6 Free";
    font-weight: 900;
    content: "\f019  ";
}

[data-baseweb="select"] > div,
[data-baseweb="base-input"] > input,
.stDateInput input {
    background: var(--bg-primary) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border-radius: 6px !important;
}

[data-baseweb="tag"] {
    background: rgba(251,146,60,0.12) !important;
    border: 1px solid rgba(251,146,60,0.3) !important;
    color: var(--accent-primary) !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    margin-bottom: 8px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    box-shadow: var(--shadow-card) !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(251,146,60,0.3) !important;
    box-shadow: 0 4px 20px rgba(251,146,60,0.06) !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    padding: 14px 16px !important;
}
            
[data-testid="stExpander"] summary:hover {
    color: var(--accent-primary) !important;
}
            
[data-testid="stExpander"] > details > div,
[data-testid="stExpanderDetails"],
[data-testid="stExpander"] .streamlit-expanderContent,
[data-testid="stExpander"] > div > div {
    padding-bottom: 32px !important;
    overflow: visible !important;
}
            
[data-testid="stAlert"] {
    background: rgba(251,146,60,0.07) !important;
    border: 1px solid rgba(251,146,60,0.25) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}

.stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
}

.stTextInput input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 2px rgba(251,146,60,0.2) !important;
}

hr {
    border-color: var(--border) !important;
    margin: 24px 0 !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

.news-source-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-weight: 700;
    margin-right: 8px;
}

.badge-detik  { background: rgba(248,113,113,0.15); color: var(--accent-red);    border: 1px solid rgba(248,113,113,0.3); }
.badge-kompas { background: rgba(96,165,250,0.15);  color: var(--accent-blue);   border: 1px solid rgba(96,165,250,0.3); }
.badge-metrotv{ background: rgba(251,191,36,0.15);  color: var(--accent-yellow); border: 1px solid rgba(251,191,36,0.3); }

.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(128,128,128,0.07);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 3px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-secondary);
    margin-right: 6px;
    margin-top: 4px;
}

.bencana-tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    font-weight: 700;
    text-transform: uppercase;
}

.tag-banjir   { background: rgba(96,165,250,0.12);   color: var(--accent-blue);   border: 1px solid rgba(96,165,250,0.3); }
.tag-longsor  { background: rgba(180,120,60,0.12);    color: #c8894d;              border: 1px solid rgba(180,120,60,0.3); }
.tag-gempa    { background: rgba(248,113,113,0.12);   color: var(--accent-red);    border: 1px solid rgba(248,113,113,0.3); }
.tag-angin    { background: rgba(167,139,250,0.12);   color: var(--accent-purple); border: 1px solid rgba(167,139,250,0.25); }
.tag-api      { background: rgba(251,146,60,0.12);    color: var(--accent-primary);border: 1px solid rgba(251,146,60,0.3); }
.tag-default  { background: rgba(148,163,184,0.08);   color: var(--text-secondary);border: 1px solid var(--border); }

.section-title {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border-accent);
    opacity: 0.5;
}

.sidebar-logo {
    padding: 20px 16px 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}

.sidebar-logo-title {
    font-family: 'Outfit', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: var(--accent-primary) !important;
    letter-spacing: -0.5px;
}

.sidebar-logo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--text-muted) !important;
    letter-spacing: 0.05em;
    margin-top: 2px;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-red)) !important;
}

.stCaption, small {
    color: var(--text-muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
}

div.stLinkButton > a {
    display: inline-block !important;
    text-align: center !important;
    text-decoration: none !important;
}

.stDateInput [data-baseweb="input"] {
    background: var(--bg-primary) !important;
}

p, span, div, li {
    color: var(--text-primary);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-baseweb="popover"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

[data-baseweb="menu"] {
    background: var(--bg-secondary) !important;
}

[data-baseweb="menu-item"]:hover {
    background: rgba(251,146,60,0.08) !important;
}

.fa-solid, .fa-regular, .fa-brands {
    color: inherit !important;
}

.chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    box-shadow: var(--shadow-card);
}

.chart-card-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER CONSTANTS ─────────────────────────────────────────────────────────
HEADERS = {"User-Agent": "Mozilla/5.0"}

# =====================================================
# PLOTLY THEME CONFIG (shared)
# =====================================================

PLOTLY_TRANSPARENT = "rgba(0,0,0,0)"
PLOTLY_FONT_COLOR  = "#94a3b8"
PLOTLY_GRID_COLOR  = "rgba(255,255,255,0.06)"
PLOTLY_FONT_FAMILY = "DM Mono, monospace"

def _base_layout(height=260):
    return dict(
        paper_bgcolor=PLOTLY_TRANSPARENT,
        plot_bgcolor=PLOTLY_TRANSPARENT,
        font=dict(color=PLOTLY_FONT_COLOR, family=PLOTLY_FONT_FAMILY, size=11),
        margin=dict(l=10, r=60, t=10, b=10),
        showlegend=False,
        height=height,
    )

# =====================================================
# NORMALISASI TANGGAL
# =====================================================

def normalize_date(date_str):
    bulan_map = {
        "Jan": "Januari", "Feb": "Februari", "Mar": "Maret", "Apr": "April",
        "May": "Mei", "Jun": "Juni", "Jul": "Juli", "Aug": "Agustus",
        "Sep": "September", "Oct": "Oktober", "Nov": "November", "Dec": "Desember",
        "January": "Januari", "February": "Februari", "March": "Maret",
        "June": "Juni", "July": "Juli", "August": "Agustus",
        "October": "Oktober", "December": "Desember"
    }
    try:
        date_str = date_str.replace("WIB", "").strip()
        if "," in date_str:
            date_str = date_str.split(",")[1].strip()
        parts = date_str.split()
        day = str(int(parts[0]))
        month = bulan_map.get(parts[1], parts[1])
        year = parts[2]
        return f"{day} {month} {year}"
    except:
        return date_str

# =====================================================
# PARSE DATETIME
# =====================================================

def parse_date_to_datetime(date_str):
    bulan_map = {
        "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
        "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
        "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
    }
    try:
        parts = date_str.split()
        day = parts[0]
        month = bulan_map.get(parts[1], "01")
        year = parts[2]
        return pd.to_datetime(f"{year}-{month}-{day}")
    except:
        return None

# =====================================================
# FILTER TAG KEBENCANAAN
# =====================================================

def is_kebencanaan(tag):
    if tag is None:
        return False
    keywords = [
        "bencana", "banjir", "puting beliung", "gelombang pasang",
        "abrasi", "longsor", "kekeringan", "gempa",
        "gunung meletus", "erupsi", "kebakaran hutan"
    ]
    tag = tag.lower()
    return any(k in tag for k in keywords)

# =====================================================
# DAFTAR PROVINSI INDONESIA
# =====================================================

PROVINSI_LIST = [
    "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Kepulauan Riau",
    "Jambi", "Sumatera Selatan", "Bangka Belitung", "Bengkulu", "Lampung",
    "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur",
    "Banten", "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur",
    "Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan",
    "Kalimantan Timur", "Kalimantan Utara",
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
    "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat",
    "Maluku", "Maluku Utara", "Papua", "Papua Barat",
    "Papua Selatan", "Papua Tengah", "Papua Pegunungan", "Papua Barat Daya"
]

# =====================================================
# FILTER LOKASI INDONESIA
# =====================================================

def is_indonesia_news(text):
    if not text:
        return False
    text = text.lower()

    for prov in PROVINSI_LIST:
        if prov.lower() in text:
            return True

    kota_keywords = [
        "jakarta","bandung","surabaya","medan","semarang",
        "makassar","palembang","balikpapan","pontianak",
        "padang","pekanbaru","yogyakarta","solo","malang",
        "bogor","depok","tangerang","bekasi",
        "denpasar","mataram","kupang",
        "manado","kendari","palu","gorontalo",
        "ambon","sorong","jayapura"
    ]

    instansi_keywords = [
        "bnpb","bpbd","bmkg","basarnas",
        "kementerian","pemprov","pemkab","pemkot",
        "gubernur","bupati","wali kota",
        "tni","polri"
    ]

    waktu_keywords = ["wib","wita","wit"]

    lokal_keywords = [
        "tanah air","nusantara","di indonesia",
        "wilayah indonesia","provinsi","kabupaten",
        "kecamatan","desa","kelurahan"
    ]

    luar_keywords = [
        "jepang","china","tiongkok","amerika","as ",
        "india","pakistan","turki","filipina",
        "thailand","vietnam","myanmar",
        "bangladesh","nepal","korea","iran",
        "irak","israel","palestina","afrika",
        "eropa","australia"
    ]

    if any(k in text for k in luar_keywords):
        return False
    if any(k in text for k in kota_keywords):
        return True
    if any(k in text for k in instansi_keywords):
        return True
    if any(k in text for k in waktu_keywords):
        return True
    if any(k in text for k in lokal_keywords):
        return True

    return False

# =====================================================
# EKSTRAKSI INFORMASI BENCANA
# =====================================================

def get_context_window(words, index, window=5):
    start = max(0, index - window)
    end = min(len(words), index + window + 1)
    return words[start:end]

def extract_disaster_info(row):
    text = row["Isi Berita"]
    if not text:
        return pd.Series({"Provinsi": "-", "Jenis Bencana": "-", "Kronologis": "-"})

    text_lower = text.lower()

    def clean_number(match_group):
        if match_group:
            num_str = re.sub(r'[^\d]', '', match_group)
            return num_str
        return "-"

    num_pattern = r'(\d{1,3}(?:\.\d{3})*|\d+)'

    terdampak_kk = "-"
    kk_match = re.search(num_pattern + r'\s*kk', text_lower)
    if kk_match:
        terdampak_kk = clean_number(kk_match.group(1))

    terdampak_jiwa = "-"
    jiwa_match = re.search(num_pattern + r'\s*(jiwa|orang)', text_lower)
    if jiwa_match:
        terdampak_jiwa = clean_number(jiwa_match.group(1))

    mengungsi_kk = "-"
    kk_m_match = re.search(num_pattern + r'\s*kk.*mengungsi', text_lower)
    if kk_m_match:
        mengungsi_kk = clean_number(kk_m_match.group(1))

    mengungsi_jiwa = "-"
    jiwa_m_match = re.search(num_pattern + r'\s*(jiwa|orang).*mengungsi', text_lower)
    if jiwa_m_match:
        mengungsi_jiwa = clean_number(jiwa_m_match.group(1))

    rumah_rusak = "-"
    words = text_lower.split()
    for i, w in enumerate(words):
        if w == "rumah":
            context = words[max(0, i-5): min(len(words), i+6)]
            context_text = " ".join(context)
            rumah_match = re.search(num_pattern, context_text)
            if rumah_match:
                rumah_rusak = clean_number(rumah_match.group(1))
                break

    korban_meninggal = "-"
    words = text_lower.split()
    for i, w in enumerate(words):
        if w in ["meninggal", "tewas", "hilang"]:
            context = words[max(0, i-5): min(len(words), i+6)]
            context_text = " ".join(context)
            match = re.search(num_pattern, context_text)
            if match:
                korban_meninggal = clean_number(match.group(1))
                break

    korban_luka = "-"
    words = text_lower.split()
    for i, w in enumerate(words):
        if w in ["luka", "terluka", "cedera"]:
            context = words[max(0, i-5): min(len(words), i+6)]
            context_text = " ".join(context)
            match = re.search(num_pattern + r'\s*(orang|jiwa)?\s*(luka|terluka|cedera)', context_text)
            if match:
                korban_luka = clean_number(match.group(1))
                break

    provinsi = "-"
    for prov in PROVINSI_LIST:
        if prov.lower() in text_lower:
            provinsi = prov
            break

    if provinsi == "-":
        kota_to_prov = {
            "jakarta": "DKI Jakarta",
            "bandung": "Jawa Barat",
            "bogor": "Jawa Barat",
            "depok": "Jawa Barat",
            "bekasi": "Jawa Barat",
            "surabaya": "Jawa Timur",
            "malang": "Jawa Timur",
            "semarang": "Jawa Tengah",
            "solo": "Jawa Tengah",
            "yogyakarta": "DI Yogyakarta",
            "medan": "Sumatera Utara",
            "makassar": "Sulawesi Selatan",
            "denpasar": "Bali",
            "palembang": "Sumatera Selatan",
            "balikpapan": "Kalimantan Timur",
            "pontianak": "Kalimantan Barat",
            "manado": "Sulawesi Utara",
            "jayapura": "Papua"
        }
        for kota, prov in kota_to_prov.items():
            if kota in text_lower:
                provinsi = prov
                break

    jenis = "-"
    mapping_bencana = {
        "banjir": "Banjir",
        "puting beliung": "Puting Beliung",
        "rob": "Gelombang Pasang",
        "abrasi": "Abrasi",
        "longsor": "Tanah Longsor",
        "kekeringan": "Kekeringan",
        "gempa": "Gempa Bumi",
        "erupsi": "Gunung Meletus",
        "karhutla": "Kebakaran Hutan"
    }
    for key, val in mapping_bencana.items():
        if key in text_lower:
            jenis = val
            break

    return pd.Series({
        "Provinsi": provinsi,
        "Jenis Bencana": jenis,
        "Kronologis": text[:300] + "...",
        "Link Berita": row["Link"] if row["Link"] else "-",
        "Terdampak KK": terdampak_kk,
        "Terdampak Jiwa": terdampak_jiwa,
        "Mengungsi KK": mengungsi_kk,
        "Mengungsi Jiwa": mengungsi_jiwa,
        "Korban Meninggal": korban_meninggal,
        "Korban Luka": korban_luka,
        "Rumah Rusak": rumah_rusak
    })

# =====================================================
# SCRAPER DETIK
# =====================================================

def scrape_detik(keywords, start_date, end_date):
    seen = set()
    for keyword in keywords:
        page = 1
        stop = False
        while not stop:
            url = f"https://www.detik.com/search/searchnews?query={keyword}&sortby=time&page={page}"
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all("article")
            if len(articles) == 0:
                break
            for article in articles:
                try:
                    link = article.find("a")["href"]
                    title = article.find("h3").text.strip()
                    if title in seen:
                        continue
                    seen.add(title)
                    news = requests.get(link, headers=HEADERS)
                    ns = BeautifulSoup(news.text, "html.parser")
                    date_elem = ns.find("div", class_="detail__date")
                    date = date_elem.text.strip() if date_elem else ""
                    date = normalize_date(date)
                    date_dt = parse_date_to_datetime(date)
                    if date_dt is None:
                        continue
                    if date_dt < pd.to_datetime(start_date):
                        stop = True
                        break
                    if not (pd.to_datetime(start_date) <= date_dt <= pd.to_datetime(end_date)):
                        continue
                    content = ""
                    section = ns.find("div", class_="detail__body-text itp_bodycontent")
                    if section:
                        content = " ".join(p.text.strip() for p in section.find_all("p"))
                        content = content.replace("SCROLL TO CONTINUE WITH CONTENT", "")
                    tags = ""
                    tag_section = ns.find("div", class_="nav")
                    if tag_section:
                        tags = ", ".join(t.text.strip() for t in tag_section.find_all("a"))
                    if not is_kebencanaan(tags):
                        continue
                    full_text = f"{title} {content} {tags}"
                    if not is_indonesia_news(full_text):
                        continue
                    yield {"Judul": title, "Tanggal": date, "Link": link, "Tag": tags, "Isi Berita": content}
                except:
                    pass
            page += 1

# =====================================================
# SCRAPER KOMPAS
# =====================================================

def scrape_kompas(keywords, start_date, end_date):
    seen = set()
    for keyword in keywords:
        page = 1
        stop = False
        while not stop:
            url = f"https://search.kompas.com/search?q={keyword}&sort=latest&page={page}"
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all("div", class_="articleItem")
            if len(articles) == 0:
                break
            for article in articles:
                try:
                    title = article.find("h2", class_="articleTitle").text.strip()
                    link = article.find("a", class_="article-link")["href"]
                    if title in seen:
                        continue
                    seen.add(title)
                    date = article.find("div", class_="articlePost-date").text.strip()
                    date = normalize_date(date)
                    date_dt = parse_date_to_datetime(date)
                    if date_dt is None:
                        continue
                    if date_dt < pd.to_datetime(start_date):
                        stop = True
                        break
                    if not (pd.to_datetime(start_date) <= date_dt <= pd.to_datetime(end_date)):
                        continue
                    news = requests.get(link, headers=HEADERS)
                    ns = BeautifulSoup(news.text, "html.parser")
                    content = ""
                    section = ns.find("div", class_="read__content")
                    if section:
                        for baca in section.find_all("p"):
                            if "baca juga" in baca.get_text(strip=True).lower():
                                baca.decompose()
                        content = " ".join(p.get_text(" ", strip=True) for p in section.find_all("p"))
                    tags = ""
                    tag_section = ns.find("div", class_="tagsCloud-tag")
                    if tag_section:
                        tags = ", ".join(t.text.strip() for t in tag_section.find_all("a"))
                    if not is_kebencanaan(tags):
                        continue
                    full_text = f"{title} {content} {tags}"
                    if not is_indonesia_news(full_text):
                        continue
                    yield {"Judul": title, "Tanggal": date, "Link": link, "Tag": tags, "Isi Berita": content}
                    time.sleep(1)
                except:
                    pass
            page += 1

# =====================================================
# SCRAPER METROTV
# =====================================================

def scrape_metrotv(keywords, start_date, end_date):
    seen = set()
    for keyword in keywords:
        page = 0
        stop = False
        while not stop:
            url = f"https://www.metrotvnews.com/search?query={keyword}&page={page}"
            r = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all("div", class_="item")
            if len(articles) == 0:
                break
            for article in articles:
                try:
                    link = article.find("a")["href"]
                    title = article.find("h3").text.strip()
                    if link.startswith("/"):
                        link = "https://www.metrotvnews.com" + link
                    if title in seen:
                        continue
                    seen.add(title)
                    news = requests.get(link, headers=HEADERS)
                    ns = BeautifulSoup(news.text, "html.parser")
                    date = ""
                    date_tags = ns.select("p.date")
                    for tag in date_tags:
                        text = tag.get_text(strip=True)
                        if "•" in text:
                            date = text.split("•")[-1].strip()
                        else:
                            date = text
                    date = normalize_date(date)
                    date_dt = parse_date_to_datetime(date)
                    if date_dt is None:
                        continue
                    if date_dt < pd.to_datetime(start_date):
                        stop = True
                        break
                    if not (pd.to_datetime(start_date) <= date_dt <= pd.to_datetime(end_date)):
                        continue
                    content = ""
                    section = ns.find("div", class_="news-text")
                    if section:
                        for table in section.find_all("table"):
                            table.decompose()
                        for read in section.find_all("div", class_="readother"):
                            read.decompose()
                        paragraphs = []
                        for p in section.find_all("p"):
                            text = p.get_text(" ", strip=True)
                            if "baca juga" in text.lower():
                                continue
                            paragraphs.append(text)
                        content = " ".join(paragraphs)
                    tags = ""
                    tag_section = ns.find("div", class_="tag-content")
                    if tag_section:
                        tags = ", ".join(t.text.strip() for t in tag_section.find_all("a"))
                    if not is_kebencanaan(tags):
                        continue
                    full_text = f"{title} {content} {tags}"
                    if not is_indonesia_news(full_text):
                        continue
                    yield {"Judul": title, "Tanggal": date, "Link": link, "Tag": tags, "Isi Berita": content}
                    time.sleep(1)
                except:
                    pass
            page += 1

# =====================================================
# HELPER BADGES
# =====================================================

def get_bencana_badge(jenis):
    mapping = {
        "Banjir": "tag-banjir",
        "Tanah Longsor": "tag-longsor",
        "Gempa Bumi": "tag-gempa",
        "Puting Beliung": "tag-angin",
        "Kebakaran Hutan": "tag-api",
        "Gunung Meletus": "tag-api",
        "Gelombang Pasang": "tag-banjir",
    }
    css_class = mapping.get(jenis, "tag-default")
    return f'<span class="bencana-tag {css_class}">{jenis}</span>'

def get_source_badge(site):
    mapping = {
        "Detik": "badge-detik",
        "Kompas": "badge-kompas",
        "MetroTV": "badge-metrotv"
    }
    css_class = mapping.get(site, "tag-default")
    return f'<span class="news-source-badge {css_class}">{site}</span>'

# =====================================================
# ✅ CHART 1 — Per Sumber (Donut) — PLOTLY
# =====================================================

def render_chart_sumber(site_counts):
    colors_map = {
        "Detik":   "#E24B4A",
        "Kompas":  "#1D9E75",
        "MetroTV": "#378ADD",
    }
    labels = list(site_counts.index)
    values = [int(v) for v in site_counts.values]
    colors = [colors_map.get(l, "#888780") for l in labels]

    st.markdown(
        '<div class="chart-card-label" style="font-family:DM Mono,monospace;font-size:9px;'
        'letter-spacing:0.08em;text-transform:uppercase;color:#94a3b8;margin-bottom:4px;">'
        '🌐 PER SUMBER</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.60,
        marker=dict(
            colors=colors,
            line=dict(color=PLOTLY_TRANSPARENT, width=0),  # no border
        ),
        textinfo="label+percent",
        textfont=dict(size=10, color="#e2e8f0", family=PLOTLY_FONT_FAMILY),
        insidetextorientation="radial",
        hovertemplate="%{label}: <b>%{value}</b> berita (%{percent})<extra></extra>",
    ))

    layout = _base_layout(height=260)
    layout.update(margin=dict(l=10, r=10, t=10, b=10))
    fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# =====================================================
# ✅ CHART 2 — Tipe Bencana (Horizontal Bar) — PLOTLY
# =====================================================

def render_chart_bencana(jenis_counts):
    jenis_colors_map = {
        "Banjir":           "#378ADD",
        "Tanah Longsor":    "#BA7517",
        "Gempa Bumi":       "#E24B4A",
        "Puting Beliung":   "#7F77DD",
        "Kebakaran Hutan":  "#EF9F27",
        "Gunung Meletus":   "#D85A30",
        "Abrasi":           "#1D9E75",
        "Kekeringan":       "#BA7517",
        "Gelombang Pasang": "#378ADD",
    }

    labels = list(jenis_counts.index)
    values = [int(v) for v in jenis_counts.values]
    colors = [jenis_colors_map.get(l, "#888780") for l in labels]

    # Sort ascending so largest bar is at top
    paired = sorted(zip(values, labels, colors), key=lambda x: x[0])
    values, labels, colors = zip(*paired) if paired else ([], [], [])
    values, labels, colors = list(values), list(labels), list(colors)

    st.markdown(
        '<div class="chart-card-label" style="font-family:DM Mono,monospace;font-size:9px;'
        'letter-spacing:0.08em;text-transform:uppercase;color:#94a3b8;margin-bottom:4px;">'
        '⚠️ TIPE BENCANA</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=values,
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(size=12, color="#ffffff", family=PLOTLY_FONT_FAMILY),
        hovertemplate="%{y}: <b>%{x}</b> kejadian<extra></extra>",
        width=0.6,
    ))

    chart_height = max(220, len(labels) * 48 + 40)
    layout = _base_layout(height=chart_height)
    layout.update(
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
            tickfont=dict(size=10, color="#94a3b8"),
            showline=False,
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color="#94a3b8"),
            showline=False,
        ),
        bargap=0.3,
    )
    fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# =====================================================
# ✅ CHART 3 — Top Provinsi (Horizontal Bar) — PLOTLY
# =====================================================

def render_chart_provinsi(prov_counts):
    PROV_COLORS_LIST = ["#BA7517", "#1D9E75", "#E24B4A", "#378ADD", "#7F77DD",
                        "#EF9F27", "#D85A30", "#60a5fa", "#a78bfa", "#34d399"]

    labels = list(prov_counts.index)
    values = [int(v) for v in prov_counts.values]
    colors = [PROV_COLORS_LIST[i % len(PROV_COLORS_LIST)] for i in range(len(labels))]

    # Sort ascending so largest bar is at top
    paired = sorted(zip(values, labels, colors), key=lambda x: x[0])
    values, labels, colors = zip(*paired) if paired else ([], [], [])
    values, labels, colors = list(values), list(labels), list(colors)

    st.markdown(
        '<div class="chart-card-label" style="font-family:DM Mono,monospace;font-size:9px;'
        'letter-spacing:0.08em;text-transform:uppercase;color:#94a3b8;margin-bottom:4px;">'
        '📍 TOP PROVINSI</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=values,
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(size=12, color="#ffffff", family=PLOTLY_FONT_FAMILY),
        hovertemplate="%{y}: <b>%{x}</b> berita<extra></extra>",
        width=0.6,
    ))

    chart_height = max(220, len(labels) * 48 + 40)
    layout = _base_layout(height=chart_height)
    layout.update(
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
            tickfont=dict(size=10, color="#94a3b8"),
            showline=False,
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color="#94a3b8"),
            showline=False,
        ),
        bargap=0.3,
    )
    fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-title"><i class="fa-solid fa-satellite-dish"></i> SIBERNA</div>
        <div class="sidebar-logo-sub">Sistem Informasi Berita Bencana Nasional</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-header"><i class="fa-solid fa-database"></i>&nbsp; Sumber Data</div>', unsafe_allow_html=True)

    websites = st.multiselect(
        "Portal Berita",
        ["Detik", "Kompas", "MetroTV"],
        placeholder="Pilih sumber..."
    )

    st.markdown('<div class="sidebar-section-header"><i class="fa-solid fa-sliders"></i>&nbsp; Parameter Scraping</div>', unsafe_allow_html=True)

    keywords = st.multiselect(
        "Kata Kunci",
        [
            "Bencana", "Banjir", "Puting Beliung", "Gelombang Pasang",
            "Abrasi", "Tanah Longsor", "Kekeringan", "Gempa Bumi",
            "Gunung Meletus", "Kebakaran Hutan"
        ],
        placeholder="Pilih keyword..."
    )

    st.markdown('<div class="sidebar-section-header"><i class="fa-regular fa-calendar"></i>&nbsp; Rentang Waktu</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Dari", label_visibility="visible")
    end_date = col2.date_input("Hingga", label_visibility="visible")

    st.markdown("<br>", unsafe_allow_html=True)

    run = st.button("🛰  Mulai Monitoring", use_container_width=True, type="primary")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:DM Mono,monospace;font-size:9px;color:var(--text-muted);
        letter-spacing:0.05em;text-transform:uppercase;border-top:1px solid var(--border);
        padding-top:12px;margin-top:32px;padding-bottom:8px;">
        <i class="fa-solid fa-circle-nodes"></i> SIBERNA v2.0 · 2026<br><br>
        <i class="fa-solid fa-shield-halved"></i> Monitoring Bencana Nasional
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div class="main-header">
    <div class="main-header-label"><i class="fa-solid fa-gauge-high"></i> Command Dashboard</div>
    <h1><i class="fa-solid fa-tower-broadcast"></i> Monitoring Bencana Nasional</h1>
    <div class="main-header-sub">
        <span class="live-dot"></span>
        Sistem pemantauan berita kebencanaan realtime dari berbagai portal nasional
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI METRICS ROW
# =====================================================

metric_placeholder = st.empty()

def render_metrics():
    df = st.session_state.get("data_scraping", pd.DataFrame())

    m1, m2, m3, m4 = metric_placeholder.columns(4)

    total_val = len(df)
    src_val = df["Website"].nunique() if not df.empty else 0

    if "tabel_bencana" in st.session_state:
        tb = st.session_state["tabel_bencana"]
        jenis_val = tb[tb["Jenis Bencana"] != "-"]["Jenis Bencana"].nunique()
    else:
        jenis_val = 0

    status = st.session_state.get("status", "IDLE")

    if status == "RUNNING":
        status_str = "RUNNING"
        status_color = "var(--accent-yellow)"
    elif status == "SELESAI":
        status_str = "SELESAI"
        status_color = "var(--accent-green)"
    else:
        status_str = "IDLE"
        status_color = "var(--text-muted)"

    with m1:
        st.markdown(f"""<div class="metric-card orange">
        <div class="metric-card-label"><i class="fa-solid fa-newspaper"></i> Total Berita</div>
        <div class="metric-card-value orange">{total_val}</div>
        <div class="metric-card-desc">artikel terkumpul</div></div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""<div class="metric-card blue">
        <div class="metric-card-label"><i class="fa-solid fa-globe"></i> Sumber Portal</div>
        <div class="metric-card-value blue">{src_val}</div>
        <div class="metric-card-desc">portal aktif discan</div></div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""<div class="metric-card red">
        <div class="metric-card-label"><i class="fa-solid fa-triangle-exclamation"></i> Jenis Bencana</div>
        <div class="metric-card-value red">{jenis_val}</div>
        <div class="metric-card-desc">tipe terdeteksi</div></div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""<div class="metric-card green">
        <div class="metric-card-label"><i class="fa-solid fa-circle-dot"></i> Status Sistem</div>
        <div class="metric-card-value" style="color:{status_color};">{status_str}</div>
        <div class="metric-card-desc">kondisi monitor</div></div>""", unsafe_allow_html=True)

render_metrics()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "🗂  Dataset Berita",
    "📊  Detail & Analisis",
    "⚠️  Tabel Kejadian Bencana"
])

with tab1:
    st.markdown('<div class="section-title"><i class="fa-solid fa-rss"></i>&nbsp; Live Feed</div>', unsafe_allow_html=True)
    status_box = st.empty()
    table_box = st.empty()
    download_box = st.empty()

    if "data_scraping" in st.session_state and not run:
        df_old = st.session_state["data_scraping"]
        table_box.dataframe(
            df_old,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Link": st.column_config.LinkColumn("Link", display_text="→ Buka"),
                "Judul": st.column_config.TextColumn("Judul", width="large"),
                "Isi Berita": st.column_config.TextColumn("Preview Isi", width="medium"),
            }
        )
        with download_box:
            st.divider()
            csv = df_old.to_csv(index=False, sep=";").encode("utf-8")
            st.download_button(
                "Download Dataset CSV",
                csv,
                "hasil_scraping_berita.csv",
                "text/csv",
                use_container_width=True
            )

# =====================================================
# RUN SCRAPER
# =====================================================

if run:
    st.session_state["status"] = "RUNNING"
    if not websites:
        st.error("⚠️ Pilih minimal satu sumber berita di sidebar.")
    elif not keywords:
        st.error("⚠️ Pilih minimal satu kata kunci di sidebar.")
    else:
        temp_data = []
        status_text = []

        progress_bar = st.progress(0)
        total_sites = len(websites)

        for idx, site in enumerate(websites):
            status_text.append(f"⏳ {site}")

            with tab1:
                status_box.markdown(f"""
                <div style="background:rgba(251,146,60,0.07);border:1px solid rgba(251,146,60,0.2);
                    border-radius:6px;padding:12px 16px;font-family:DM Mono,monospace;
                    font-size:11px;color:var(--accent-primary);letter-spacing:0.05em;">
                    <i class="fa-solid fa-satellite fa-spin"></i>&nbsp; SCRAPING AKTIF — {' · '.join(status_text)}
                </div>
                """, unsafe_allow_html=True)

            with st.spinner(f"Mengambil data dari {site}..."):
                if site == "Detik":
                    generator = scrape_detik(keywords, start_date, end_date)
                elif site == "Kompas":
                    generator = scrape_kompas(keywords, start_date, end_date)
                elif site == "MetroTV":
                    generator = scrape_metrotv(keywords, start_date, end_date)

                for row in generator:
                    st.session_state["status"] = "RUNNING"
                    render_metrics()

                    row["Website"] = site
                    temp_data.append(row)

                    df = pd.DataFrame(temp_data)
                    df["Tanggal_dt"] = df["Tanggal"].apply(parse_date_to_datetime)
                    df = df.sort_values("Tanggal_dt", ascending=False).reset_index(drop=True)
                    df["No"] = df.index + 1
                    df = df[["No", "Judul", "Tanggal", "Website", "Tag", "Link", "Isi Berita"]]

                    st.session_state["data_scraping"] = df
                    render_metrics()

                    disaster_df = df.copy()
                    info = disaster_df.apply(extract_disaster_info, axis=1)
                    disaster_df = pd.concat([disaster_df, info], axis=1)
                    disaster_df = disaster_df[disaster_df["Jenis Bencana"] != "-"]
                    st.session_state["tabel_bencana"] = disaster_df

                    with tab1:
                        table_box.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Link": st.column_config.LinkColumn("Link", display_text="→ Buka"),
                                "Judul": st.column_config.TextColumn("Judul", width="large"),
                                "Isi Berita": st.column_config.TextColumn("Preview Isi", width="medium"),
                            }
                        )

            status_text[-1] = f"✅ {site}"
            progress_bar.progress((idx + 1) / total_sites)

        progress_bar.empty()

        if len(temp_data) > 0:
            st.session_state["status"] = "SELESAI"
            render_metrics()
            st.session_state["data_scraping"] = df

            with download_box:
                st.divider()
                csv_dl = df.to_csv(index=False, sep=";").encode("utf-8")
                st.download_button(
                    "Download Dataset CSV",
                    csv_dl,
                    "hasil_scraping_berita.csv",
                    "text/csv",
                    use_container_width=True
                )

            with tab1:
                status_box.markdown(f"""
                <div style="background:rgba(52,211,153,0.07);border:1px solid rgba(52,211,153,0.25);
                    border-radius:6px;padding:12px 16px;font-family:DM Mono,monospace;
                    font-size:11px;color:var(--accent-green);letter-spacing:0.05em;">
                    <i class="fa-solid fa-circle-check"></i>&nbsp; SELESAI — {len(df)} berita berhasil dikumpulkan dari {df['Website'].nunique()} sumber
                </div>
                """, unsafe_allow_html=True)

            disaster_df = df.copy()
            info = disaster_df.apply(extract_disaster_info, axis=1)
            disaster_df = pd.concat([disaster_df, info], axis=1)
            disaster_df = disaster_df[disaster_df["Jenis Bencana"] != "-"]
            disaster_df["Waktu Kejadian"] = disaster_df["Tanggal"]
            disaster_df = disaster_df[[
                "No", "Provinsi", "Jenis Bencana", "Waktu Kejadian",
                "Terdampak KK", "Terdampak Jiwa", "Mengungsi KK", "Mengungsi Jiwa",
                "Korban Meninggal", "Korban Luka", "Rumah Rusak",
                "Kronologis", "Link Berita"
            ]]
            st.session_state["data_scraping"] = df
            st.session_state["tabel_bencana"] = disaster_df

        else:
            with tab1:
                status_box.markdown("""
                <div style="background:rgba(248,113,113,0.07);border:1px solid rgba(248,113,113,0.25);
                    border-radius:6px;padding:12px 16px;font-family:DM Mono,monospace;
                    font-size:11px;color:var(--accent-red);letter-spacing:0.05em;">
                    <i class="fa-solid fa-circle-xmark"></i>&nbsp; TIDAK ADA DATA — Tidak ditemukan berita untuk parameter yang dipilih
                </div>
                """, unsafe_allow_html=True)

# =====================================================
# TAB 2 — DETAIL & ANALISIS
# =====================================================

if "data_scraping" in st.session_state:
    final_df = st.session_state["data_scraping"]

    with tab2:

        if len(final_df) > 0:
            st.markdown('<div class="section-title"><i class="fa-solid fa-chart-pie"></i>&nbsp; Distribusi & Analisis</div>', unsafe_allow_html=True)

            ana1, ana2, ana3 = st.columns(3)

            # ── Chart 1: Per Sumber (Donut) ──
            with ana1:
                site_counts = final_df["Website"].value_counts()
                render_chart_sumber(site_counts)

            # ── Chart 2: Tipe Bencana (Horizontal Bar) ──
            with ana2:
                if "tabel_bencana" in st.session_state:
                    tb2 = st.session_state["tabel_bencana"]
                    jenis_counts = tb2[tb2["Jenis Bencana"] != "-"]["Jenis Bencana"].value_counts().head(5)
                    if not jenis_counts.empty:
                        render_chart_bencana(jenis_counts)

            # ── Chart 3: Top Provinsi (Horizontal Bar) ──
            with ana3:
                if "tabel_bencana" in st.session_state:
                    tb3 = st.session_state["tabel_bencana"]
                    prov_counts = tb3[tb3["Provinsi"] != "-"]["Provinsi"].value_counts().head(5)
                    if not prov_counts.empty:
                        render_chart_provinsi(prov_counts)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title"><i class="fa-solid fa-newspaper"></i>&nbsp; Artikel Berita</div>', unsafe_allow_html=True)

        fcol1, fcol2 = st.columns([3, 1])
        search = fcol1.text_input("", placeholder="🔍  Cari judul berita...", label_visibility="collapsed")

        site_filter_opts = ["Semua"] + list(final_df["Website"].unique())
        site_filter = fcol2.selectbox("", site_filter_opts, label_visibility="collapsed")

        view_df = final_df.copy()
        if search:
            view_df = view_df[view_df["Judul"].str.contains(search, case=False)]
        if site_filter != "Semua":
            view_df = view_df[view_df["Website"] == site_filter]

        st.caption(f"Menampilkan {len(view_df)} dari {len(final_df)} berita")
        st.markdown("<br>", unsafe_allow_html=True)

        for i, row in view_df.iterrows():
            site_badge = get_source_badge(row['Website'])
            expander_label = f"[{row['Website']}] {row['Judul']}"

            with st.expander(expander_label):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
                    {site_badge}
                    <span class="meta-chip"><i class="fa-regular fa-calendar"></i>&nbsp;{row['Tanggal']}</span>
                    <span class="meta-chip"><i class="fa-solid fa-tag"></i>&nbsp;{row['Tag'][:70] + '...' if len(str(row['Tag'])) > 70 else row['Tag']}</span>
                </div>
                """, unsafe_allow_html=True)

                col_left, col_right = st.columns([3, 1])

                with col_left:
                    st.markdown(f"""
                    <div style="background:rgba(128,128,128,0.06);border:1px solid var(--border);
                        border-radius:6px;padding:16px;font-size:13px;line-height:1.7;
                        color:var(--text-secondary);font-family:Plus Jakarta Sans,sans-serif;">
                        {row['Isi Berita']}
                    </div>
                    """, unsafe_allow_html=True)

                with col_right:
                    st.markdown(f"""
                    <div style="background:rgba(251,146,60,0.05);border:1px solid rgba(251,146,60,0.15);
                        border-radius:6px;padding:14px;text-align:center;">
                        <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.06em;
                            color:var(--text-secondary);text-transform:uppercase;margin-bottom:8px;">
                            <i class="fa-solid fa-circle-info"></i>&nbsp; Metadata
                        </div>
                        <div style="font-family:Outfit,sans-serif;font-size:20px;font-weight:800;
                            color:var(--accent-primary);margin-bottom:2px;">{row['Website']}</div>
                        <div style="font-family:DM Mono,monospace;font-size:10px;color:var(--text-muted);">
                            {row['Tanggal']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.link_button("↗ Buka Artikel", row["Link"], use_container_width=True)

# =====================================================
# TAB 3 — TABEL KEJADIAN BENCANA
# =====================================================

if "tabel_bencana" in st.session_state:
    with tab3:
        tabel = st.session_state["tabel_bencana"]

        st.markdown('<div class="section-title"><i class="fa-solid fa-list-check"></i>&nbsp; Rekap Kejadian Bencana</div>', unsafe_allow_html=True)

        filter_col1, filter_col2 = st.columns(2)

        all_jenis = ["Semua"] + sorted(tabel[tabel["Jenis Bencana"] != "-"]["Jenis Bencana"].unique().tolist())
        all_prov = ["Semua"] + sorted(tabel[tabel["Provinsi"] != "-"]["Provinsi"].unique().tolist())

        jenis_filter = filter_col1.selectbox("Filter Jenis Bencana", all_jenis)
        prov_filter = filter_col2.selectbox("Filter Provinsi", all_prov)

        filtered_tabel = tabel.copy()
        if jenis_filter != "Semua":
            filtered_tabel = filtered_tabel[filtered_tabel["Jenis Bencana"] == jenis_filter]
        if prov_filter != "Semua":
            filtered_tabel = filtered_tabel[filtered_tabel["Provinsi"] == prov_filter]

        st.markdown("<br>", unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)

        with s1:
            n_prov = filtered_tabel[filtered_tabel["Provinsi"] != "-"]["Provinsi"].nunique()
            st.markdown(f"""
            <div style="background:rgba(52,211,153,0.07);border:1px solid rgba(52,211,153,0.2);
                border-radius:6px;padding:14px 18px;">
                <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.06em;
                    color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px;">
                    <i class="fa-solid fa-map-pin"></i>&nbsp; Provinsi Terdampak
                </div>
                <div style="font-family:Outfit,sans-serif;font-size:28px;font-weight:800;color:var(--accent-green);">{n_prov}</div>
            </div>
            """, unsafe_allow_html=True)

        with s2:
            n_types = filtered_tabel[filtered_tabel["Jenis Bencana"] != "-"]["Jenis Bencana"].nunique()
            st.markdown(f"""
            <div style="background:rgba(248,113,113,0.07);border:1px solid rgba(248,113,113,0.2);
                border-radius:6px;padding:14px 18px;">
                <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.06em;
                    color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px;">
                    <i class="fa-solid fa-bolt"></i>&nbsp; Tipe Bencana
                </div>
                <div style="font-family:Outfit,sans-serif;font-size:28px;font-weight:800;color:var(--accent-red);">{n_types}</div>
            </div>
            """, unsafe_allow_html=True)

        with s3:
            jiwa_vals = filtered_tabel[filtered_tabel["Terdampak Jiwa"] != "-"]["Terdampak Jiwa"]
            jiwa_total = sum([int(v) for v in jiwa_vals if str(v).isdigit()])
            st.markdown(f"""
            <div style="background:rgba(251,146,60,0.07);border:1px solid rgba(251,146,60,0.2);
                border-radius:6px;padding:14px 18px;">
                <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.06em;
                    color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px;">
                    <i class="fa-solid fa-person-shelter"></i>&nbsp; Total Jiwa Terdampak
                </div>
                <div style="font-family:Outfit,sans-serif;font-size:28px;font-weight:800;
                    color:var(--accent-primary);">{jiwa_total:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with s4:
            meninggal_vals = filtered_tabel[filtered_tabel["Korban Meninggal"] != "-"]["Korban Meninggal"]
            meninggal_total = sum([int(v) for v in meninggal_vals if str(v).isdigit()])
            st.markdown(f"""
            <div style="background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.3);
                border-radius:6px;padding:14px 18px;">
                <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.06em;
                    color:var(--text-secondary);text-transform:uppercase;margin-bottom:6px;">
                    <i class="fa-solid fa-heart-crack"></i>&nbsp; Korban Meninggal
                </div>
                <div style="font-family:Outfit,sans-serif;font-size:28px;font-weight:800;
                    color:var(--accent-red);">{meninggal_total:,}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.dataframe(
            filtered_tabel,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Link Berita": st.column_config.LinkColumn("Link Berita", display_text="→ Buka"),
                "Kronologis": st.column_config.TextColumn("Kronologis", width="large"),
                "Jenis Bencana": st.column_config.TextColumn("Jenis Bencana", width="medium"),
            }
        )

        st.divider()

        csv2 = filtered_tabel.to_csv(index=False, sep=";").encode("utf-8")
        st.download_button(
            "Download Tabel Bencana CSV",
            csv2,
            "tabel_kejadian_bencana.csv",
            "text/csv",
            use_container_width=True
        )