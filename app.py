import streamlit as st
import pandas as pd
import os
import re
import base64
import random
import hashlib
import requests
import time
import io
from PIL import Image

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA AKADEMIS (AKSARA)
# ==========================================
st.set_page_config(page_title="Aksara | Platform Edukasi", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# --- WADAH KACA: container Streamlit sungguhan yang diberi kunci agar bisa didesain lewat CSS ---
# (Jika versi Streamlit lama belum mendukung parameter key, otomatis jatuh ke container biasa.)
def _wadah(awalan, nama):
    try: return st.container(key=f"{awalan}_{nama}")
    except TypeError: return st.container()

def kartu(nama): return _wadah("kartu", nama)          # kartu kaca besar
def baris(nama): return _wadah("baris", nama)          # baris kaca ramping
def tombol_merah(nama): return _wadah("btnred", nama)   # tombol aksi berbahaya
def tombol_hijau(nama): return _wadah("btngreen", nama) # tombol aksi positif

# CSS GLASSMORPHISM PREMIUM — AURORA MESH, KACA BERLAPIS, TIPOGRAFI EDITORIAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800;9..144,900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    /* =====================================================
       1. DESIGN TOKENS
       ===================================================== */
    :root {
        --ink: #0B1220;
        --ink-soft: #334155;
        --muted: #64748B;
        --blue: #2563EB;
        --indigo: #4F46E5;
        --violet: #8B5CF6;
        --fuchsia: #D946EF;
        --emerald: #10B981;
        --rose: #EF4444;

        --font-display: 'Fraunces', Georgia, serif;
        --font-ui: 'Outfit', -apple-system, 'Segoe UI', sans-serif;

        --glass-sheen: linear-gradient(135deg, rgba(255,255,255,0.88) 0%, rgba(255,255,255,0.58) 50%, rgba(255,255,255,0.76) 100%);
        --glass-edge: rgba(255, 255, 255, 0.92);
        --glass-blur: blur(26px) saturate(190%);

        --shadow-sm: 0 6px 18px rgba(30, 41, 90, 0.06);
        --shadow-md: 0 16px 40px rgba(30, 41, 90, 0.09), 0 2px 6px rgba(15, 23, 42, 0.03);
        --shadow-lg: 0 30px 64px rgba(55, 70, 180, 0.16), 0 4px 12px rgba(15, 23, 42, 0.04);
        --inner-light: inset 0 1px 0 rgba(255,255,255,1), inset 0 -1px 0 rgba(255,255,255,0.4);
        --ease: cubic-bezier(0.22, 0.9, 0.3, 1);
    }

    /* =====================================================
       2. TIPOGRAFI: Fraunces (judul) + Outfit (antarmuka)
       ===================================================== */
    html, body, .stApp { font-family: var(--font-ui) !important; }
    .stApp p, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp label, .stApp li, .stApp a, .stApp button, .stApp input, .stApp textarea, .stApp td, .stApp th {
        font-family: var(--font-ui) !important;
    }
    .stApp h1 { font-family: var(--font-display) !important; font-weight: 800; letter-spacing: -1px; line-height: 1.12; }
    .stApp h2, .stApp h3 { font-weight: 800; letter-spacing: -0.5px; }

    /* Warna dipaksa HANYA untuk elemen tanpa warna inline */
    .stApp h1:not([style*="color:"]), .stApp h2:not([style*="color:"]), .stApp h3:not([style*="color:"]) { color: var(--ink) !important; }
    .stApp h4:not([style*="color:"]), .stApp h5:not([style*="color:"]), .stApp h6:not([style*="color:"]),
    .stApp p:not([style*="color:"]), .stApp label:not([style*="color:"]), .stApp li:not([style*="color:"]) {
        color: var(--ink-soft) !important; font-weight: 500;
    }
    .stApp [data-testid="stWidgetLabel"] p { font-weight: 700; font-size: 14px; letter-spacing: 0.2px; }
    .stApp [data-testid="stCaptionContainer"] p { color: var(--muted) !important; font-weight: 500; }
    .stApp a { color: var(--blue); font-weight: 600; }
    ::selection { background: rgba(99, 102, 241, 0.25); }

    .gradient-text {
        background: linear-gradient(120deg, #2563EB 0%, #7C3AED 35%, #D946EF 65%, #2563EB 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        display: inline-block;
        filter: drop-shadow(0 6px 16px rgba(99, 102, 241, 0.28));
        animation: gradient-flow 9s linear infinite;
    }
    .vs-text {
        font-family: var(--font-display);
        background: linear-gradient(135deg, #0F172A 0%, #6366F1 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900; font-size: 52px;
        letter-spacing: 2px;
        filter: drop-shadow(0 6px 14px rgba(99, 102, 241, 0.25));
    }

    @keyframes gradient-flow { to { background-position: 200% center; } }
    @keyframes fadeInUp { from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);} }
    @keyframes aurora-drift {
        0%   { transform: translate3d(0, 0, 0) scale(1) rotate(0deg); }
        50%  { transform: translate3d(2%, -3%, 0) scale(1.08) rotate(3deg); }
        100% { transform: translate3d(-3%, 2%, 0) scale(1.04) rotate(-3deg); }
    }
    @keyframes pulse-ring { 0% { box-shadow: 0 0 0 0 rgba(139,92,246,0.35); } 100% { box-shadow: 0 0 0 18px rgba(139,92,246,0); } }

    /* =====================================================
       3. LATAR AURORA MESH (BERGERAK HALUS)
       ===================================================== */
    .stApp {
        background:
            radial-gradient(1200px 700px at 0% 0%, rgba(186, 230, 253, 0.95) 0%, transparent 60%),
            radial-gradient(1000px 700px at 100% 0%, rgba(221, 214, 254, 0.95) 0%, transparent 60%),
            radial-gradient(1100px 800px at 100% 100%, rgba(167, 243, 208, 0.80) 0%, transparent 60%),
            radial-gradient(900px 700px at 0% 100%, rgba(251, 207, 232, 0.65) 0%, transparent 60%),
            #F4F7FF !important;
        background-attachment: fixed !important;
        color: var(--ink);
        overflow-x: hidden;
        isolation: isolate;
    }
    .stApp::before {
        content: ""; position: fixed; inset: -10%; z-index: -1; pointer-events: none;
        background:
            radial-gradient(34% 34% at 18% 22%, rgba(96, 165, 250, 0.40), transparent 70%),
            radial-gradient(30% 30% at 82% 18%, rgba(167, 139, 250, 0.38), transparent 70%),
            radial-gradient(32% 32% at 74% 82%, rgba(45, 212, 191, 0.30), transparent 70%),
            radial-gradient(28% 28% at 22% 80%, rgba(244, 114, 182, 0.24), transparent 70%);
        filter: blur(42px);
        animation: aurora-drift 26s ease-in-out infinite alternate;
    }
    .stApp::after {
        content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none;
        background-image: radial-gradient(rgba(99, 102, 241, 0.16) 1px, transparent 1.3px);
        background-size: 30px 30px;
        -webkit-mask-image: radial-gradient(ellipse at 50% 25%, #000 0%, transparent 78%);
        mask-image: radial-gradient(ellipse at 50% 25%, #000 0%, transparent 78%);
    }
    [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main, .main { background: transparent !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stDecoration"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}

    /* Blok <style> murni tidak boleh menyisakan jarak kosong */
    :is(.element-container, [data-testid="stElementContainer"]):has(style):not(:has(p, h1, h2, h3, h4, img, audio, button, input)) { display: none !important; }

    .block-container {
        animation: fadeInUp 0.8s var(--ease);
        max-width: 1240px; margin-left: auto; margin-right: auto;
        padding: 2.2rem 2rem 5rem 2rem !important;
    }

    /* =====================================================
       4. WADAH KACA (container Streamlit bertanda kartu_*, baris_*)
       ===================================================== */
    [class*="st-key-kartu_"] {
        background: var(--glass-sheen);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-edge);
        border-radius: 30px;
        padding: 34px 38px !important;
        box-shadow: var(--shadow-md), var(--inner-light);
        transition: box-shadow 0.45s var(--ease), border-color 0.45s ease;
    }
    [class*="st-key-kartu_"]:hover { border-color: rgba(191, 219, 254, 1); box-shadow: var(--shadow-lg), var(--inner-light); }
    [class*="st-key-kartu_"] [data-testid="stForm"] { background: transparent; border: none !important; padding: 0 !important; box-shadow: none; }

    [class*="st-key-baris_"] {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid var(--glass-edge);
        border-radius: 22px;
        padding: 16px 24px !important;
        box-shadow: var(--shadow-sm), var(--inner-light);
        transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease), border-color 0.35s ease;
    }
    [class*="st-key-baris_"]:hover { transform: translateY(-2px); border-color: #BFDBFE; box-shadow: var(--shadow-md), var(--inner-light); }
    [class*="st-key-baris_"] [data-testid="stHorizontalBlock"], [class*="st-key-kartu_honor"] [data-testid="stHorizontalBlock"] { align-items: center; }
    [class*="st-key-baris_"] .stButton > button, [class*="st-key-baris_"] [data-testid="stButton"] > button { min-height: 2.7rem; padding: 8px 20px !important; font-size: 14px; }

    /* Varian kartu */
    .st-key-kartu_hero {
        background:
            radial-gradient(520px 260px at 100% 0%, rgba(167, 139, 250, 0.30), transparent 70%),
            radial-gradient(420px 220px at 0% 100%, rgba(96, 165, 250, 0.26), transparent 70%),
            var(--glass-sheen);
        padding: 40px 44px !important;
    }
    .st-key-kartu_honor {
        background:
            radial-gradient(420px 200px at 0% 0%, rgba(96, 165, 250, 0.22), transparent 70%),
            linear-gradient(135deg, rgba(239, 246, 255, 0.92), rgba(255, 255, 255, 0.80));
        border-color: rgba(191, 219, 254, 0.9);
        padding: 26px 38px !important;
    }
    .st-key-kartu_login { padding: 38px 40px 42px 40px !important; }
    .st-key-kartu_lobby { text-align: center; padding: 48px 40px !important; }

    /* =====================================================
       5. KOMPONEN HTML: KARTU STATISTIK, PAPAN PERINGKAT, DLL
       ===================================================== */
    .hero { text-align: center; margin: 0.5rem 0 2.2rem 0; }
    .stApp .hero .hero-title { font-family: var(--font-display); font-size: clamp(56px, 9vw, 96px); font-weight: 900; letter-spacing: -3px; line-height: 1; margin: 0; }
    .hero-sub { margin: 18px 0 0 0; font-size: 14px; letter-spacing: 7px; font-weight: 700; color: var(--muted); }
    .divider { height: 1px; margin: 26px 0; background: linear-gradient(90deg, transparent, rgba(148,163,184,0.45), transparent); }

    .stat-card {
        position: relative; overflow: hidden; text-align: center;
        padding: 30px 22px 26px 22px; border-radius: 28px;
        background: var(--glass-sheen); border: 1px solid var(--glass-edge);
        box-shadow: var(--shadow-md), var(--inner-light);
        transition: transform 0.45s var(--ease), box-shadow 0.45s var(--ease);
    }
    .stat-card::before { content: ""; position: absolute; left: 22px; right: 22px; top: 0; height: 4px; border-radius: 0 0 6px 6px; background: var(--accent, #2563EB); opacity: 0.85; }
    .stat-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-lg), var(--inner-light); }
    .stat-icon {
        width: 64px; height: 64px; margin: 0 auto 16px auto; display: grid; place-items: center;
        font-size: 30px; border-radius: 20px; background: #FFFFFF;
        box-shadow: 0 12px 26px rgba(30, 41, 90, 0.10), inset 0 1px 0 #FFFFFF; border: 1px solid #E2E8F0;
    }
    .stat-value { font-size: 44px; font-weight: 900; line-height: 1; color: var(--ink); letter-spacing: -1.5px; }
    .stat-label { margin-top: 10px; font-size: 12px; letter-spacing: 2px; font-weight: 800; color: var(--muted); }

    .section-title { font-family: var(--font-display); font-size: 30px; font-weight: 900; letter-spacing: -1px; margin: 2.2rem 0 1.2rem 0; color: var(--ink); }

    .lb { display: flex; flex-direction: column; gap: 12px; }
    .lb-row {
        position: relative; overflow: hidden; display: flex; align-items: center; gap: 18px;
        padding: 18px 28px; border-radius: 24px; border: 1px solid var(--bdr, #E2E8F0);
        background: var(--bg, rgba(255,255,255,0.8)); backdrop-filter: blur(15px);
        box-shadow: var(--shadow-sm), var(--inner-light);
        transition: transform 0.4s var(--ease), box-shadow 0.4s var(--ease);
    }
    .lb-row:hover { transform: translateY(-3px) scale(1.01); box-shadow: var(--shadow-md), var(--inner-light); }
    .lb-row::after { content: ""; position: absolute; left: 0; bottom: 0; height: 3px; width: var(--w, 0%); background: linear-gradient(90deg, #60A5FA, #8B5CF6, #D946EF); opacity: 0.7; }
    .lb-rank { min-width: 46px; height: 46px; display: grid; place-items: center; font-size: 22px; font-weight: 900; color: var(--ink); background: rgba(255,255,255,0.85); border-radius: 16px; border: 1px solid rgba(226,232,240,0.9); }
    .lb-name { flex: 1; font-size: 18px; font-weight: 800; color: var(--ink); }
    .lb-title { font-size: 11px; font-weight: 800; color: #4F46E5; background: #E0E7FF; padding: 6px 14px; border-radius: 100px; border: 1px solid #C7D2FE; letter-spacing: 0.5px; white-space: nowrap; }
    .lb-pts { font-size: 20px; font-weight: 900; color: var(--blue); white-space: nowrap; }

    .avatar-emoji {
        width: 120px; height: 120px; margin: 0 auto 14px auto; border-radius: 50%; display: grid; place-items: center;
        font-size: 62px; background: linear-gradient(145deg, #FFFFFF, #EEF2FF); border: 1px solid #FFFFFF;
        box-shadow: 0 18px 40px rgba(37, 99, 235, 0.18), inset 0 1px 0 #FFFFFF; animation: fadeInUp 1s ease;
    }
    .avatar-ring {
        width: 128px; height: 128px; margin: 0 auto 14px auto; border-radius: 50%; padding: 4px;
        background: conic-gradient(from 210deg, #60A5FA, #8B5CF6, #D946EF, #60A5FA);
        box-shadow: 0 18px 40px rgba(99, 102, 241, 0.28); transition: transform 0.5s var(--ease);
    }
    .avatar-ring:hover { transform: scale(1.06) rotate(-2deg); }
    .avatar-ring img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 4px solid #FFFFFF; display: block; background: #FFFFFF; }

    .profile { text-align: center; }
    .profile-name { font-size: 22px; font-weight: 800; color: var(--ink); margin: 6px 0 8px 0; letter-spacing: -0.3px; }
    .badge-row { margin-bottom: 10px; }
    .badge { display: inline-block; padding: 6px 18px; border-radius: 100px; font-weight: 700; font-size: 11px; letter-spacing: 0.5px; }
    .badge-title { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }
    .badge-tier { background: #FFFFFF; color: var(--tier, #64748B); border: 1px solid color-mix(in srgb, var(--tier, #64748B) 35%, transparent); font-weight: 800; box-shadow: 0 6px 16px color-mix(in srgb, var(--tier, #64748B) 16%, transparent); }
    .xp-bar { background: #E2E8F0; border-radius: 100px; height: 10px; margin: 20px 0 12px 0; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.06); }
    .xp-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #60A5FA, #8B5CF6); box-shadow: 0 0 10px rgba(139,92,246,0.5); }
    .xp-meta { display: flex; justify-content: space-between; font-weight: 800; color: #475569; font-size: 13px; }
    .xp-pts { color: #6366F1; }
    .nav-label { text-align: center; font-size: 11px; font-weight: 800; color: var(--muted); letter-spacing: 3px; margin-bottom: 12px; }

    .mad-card {
        overflow: hidden; border-radius: 30px; background: var(--glass-sheen); border: 1px solid var(--glass-edge);
        box-shadow: var(--shadow-md), var(--inner-light); transition: transform 0.5s var(--ease), box-shadow 0.5s var(--ease);
    }
    .mad-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-lg), var(--inner-light); }
    .mad-img { position: relative; height: 210px; overflow: hidden; background: linear-gradient(135deg, #BFDBFE, #DDD6FE 55%, #FBCFE8); }
    .mad-img img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.8s var(--ease); }
    .mad-card:hover .mad-img img { transform: scale(1.06); }
    .mad-img::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(15,23,42,0) 45%, rgba(15,23,42,0.28) 100%); pointer-events: none; }
    .mad-img .mading-tag { position: absolute; left: 20px; top: 20px; z-index: 2; margin: 0; background: rgba(255,255,255,0.88); backdrop-filter: blur(10px); }
    .mad-text { padding: 26px 30px 30px 30px; }
    .mading-tag { background: linear-gradient(135deg, #EFF6FF, #EEF2FF); color: #2563EB; padding: 6px 18px; border-radius: 100px; border: 1px solid #BFDBFE; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08); font-size: 11px; font-weight: 800; display: inline-block; text-transform: uppercase; letter-spacing: 1px; }
    .mading-title-text { color: #0F172A; font-family: var(--font-display); font-size: 25px; font-weight: 800; margin-bottom: 10px; line-height: 1.3; letter-spacing: -0.5px; }
    .mading-meta { color: #64748B; font-size: 12px; margin-bottom: 18px; font-weight: 700; letter-spacing: 1px; }
    .mading-body { color: #334155; font-size: 15px; line-height: 1.8; font-weight: 500; }

    .room-title { font-size: 18px; font-weight: 800; color: var(--ink); }
    .room-meta { margin-top: 4px; font-size: 13px; color: #475569; font-weight: 600; }
    .room-code { color: var(--blue); font-weight: 800; letter-spacing: 1px; }

    .lobby { text-align: center; }
    .lobby-mapel { font-size: 20px; color: #475569; font-weight: 500; }
    .lobby-mapel b { color: var(--ink); font-weight: 800; }
    .lobby-label { margin-top: 34px; font-size: 14px; color: var(--muted); font-weight: 800; letter-spacing: 6px; }
    .lobby-code { font-family: var(--font-display); font-size: clamp(56px, 10vw, 100px); font-weight: 900; letter-spacing: 14px; line-height: 1.1; margin: 6px 0 0 0; background: linear-gradient(135deg, #2563EB, #7C3AED 60%, #D946EF); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 10px 24px rgba(99,102,241,0.25)); }
    .lobby-count { margin-top: 30px; font-size: 16px; font-weight: 700; color: #334155; }
    .chips { margin-top: 14px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; padding: 20px; border-radius: 22px; background: rgba(248,250,252,0.9); border: 1px solid #E2E8F0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
    .chip { padding: 8px 18px; border-radius: 100px; background: #FFFFFF; border: 1px solid #DBEAFE; color: var(--ink); font-weight: 700; font-size: 15px; box-shadow: 0 4px 12px rgba(37,99,235,0.06); }

    .tele-row { display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; margin-bottom: 12px; border-radius: 22px; background: rgba(255,255,255,0.82); border: 1px solid var(--glass-edge); box-shadow: var(--shadow-sm), var(--inner-light); font-size: 16px; font-weight: 700; color: var(--ink); }
    .tele-status { font-size: 12px; color: var(--muted); margin-left: 14px; font-weight: 700; padding: 4px 12px; border-radius: 100px; background: #F1F5F9; }
    .tele-score { color: var(--blue); font-weight: 900; }

    .q-meta { text-align: right; color: var(--muted); font-weight: 800; font-size: 14px; margin: 14px 0 18px 0; letter-spacing: 1.5px; }
    .q-card {
        text-align: center; font-family: var(--font-display); font-size: clamp(22px, 2.6vw, 30px); font-weight: 800; line-height: 1.5; color: var(--ink);
        padding: 64px 56px; margin-bottom: 26px; border-radius: 32px; letter-spacing: -0.3px;
        background: radial-gradient(520px 240px at 50% 0%, rgba(167,139,250,0.22), transparent 70%), var(--glass-sheen);
        border: 1px solid var(--glass-edge); box-shadow: var(--shadow-lg), var(--inner-light); backdrop-filter: var(--glass-blur);
    }

    .score-card { text-align: center; padding: 40px 30px; border-radius: 30px; background: linear-gradient(135deg, rgba(239,246,255,0.92), rgba(255,255,255,0.78)); border: 1px solid rgba(191,219,254,0.95); box-shadow: var(--shadow-md), var(--inner-light); transition: transform 0.45s var(--ease), box-shadow 0.45s var(--ease); }
    .score-card:hover { transform: translateY(-6px) scale(1.015); box-shadow: var(--shadow-lg), var(--inner-light); }
    .score-card.good { background: linear-gradient(135deg, #DCFCE7, #F0FDF4); border-color: #86EFAC; }
    .score-label { color: #3B82F6; font-size: 15px; font-weight: 800; letter-spacing: 2px; margin-bottom: 14px; }
    .score-value { color: var(--ink); font-family: var(--font-display); font-size: 76px; font-weight: 900; line-height: 1; letter-spacing: -2px; }
    .score-card.good .score-label { color: #16A34A; }
    .score-card.good .score-value { color: #15803D; }

    .duel-card { text-align: center; padding: 32px 24px; border-radius: 28px; border: 1px solid var(--bdr); background: var(--bg); box-shadow: var(--shadow-md), var(--inner-light); }
    .duel-name { font-family: var(--font-display); font-size: 28px; font-weight: 800; color: var(--clr); letter-spacing: -0.5px; }
    .duel-pts { margin-top: 8px; font-size: 16px; font-weight: 800; color: var(--clr2); }
    .vs-wrap { text-align: center; padding-top: 22px; }

    .reader-card { text-align: left; line-height: 2; font-size: 17px; font-weight: 500; color: #334155; padding: 56px 64px; border-radius: 30px; background: var(--glass-sheen); border: 1px solid var(--glass-edge); box-shadow: var(--shadow-md), var(--inner-light); }
    .reader-card h1, .reader-card h2, .reader-card h3, .reader-card h4 { font-family: var(--font-display) !important; color: var(--ink) !important; margin: 1.6em 0 0.6em 0; line-height: 1.3; }
    .reader-card ul, .reader-card ol { padding-left: 1.4em; }
    .reader-card strong, .reader-card b { color: var(--ink); font-weight: 800; }

    .gelar-name { font-size: 17px; font-weight: 800; color: var(--ink); }
    .gelar-price { color: #3B82F6; font-weight: 900; font-size: 17px; }


    .stApp [data-testid="stImage"] img { border-radius: 22px; box-shadow: var(--shadow-md); }
    [class*="st-key-kartu_av_"] { text-align: center; }
    .mad-card { margin-bottom: 8px; }

    /* =====================================================
       6. TOMBOL (PILL GRADIENT + KILAU)
       ===================================================== */
    .stButton > button, [data-testid="stButton"] > button,
    .stDownloadButton > button, [data-testid="stDownloadButton"] > button,
    [data-testid="stFormSubmitButton"] > button {
        position: relative; overflow: hidden;
        width: 100%; min-height: 3.1rem;
        padding: 14px 32px !important;
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 55%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.38) !important;
        border-radius: 100px !important;
        font-weight: 700; font-size: 16px; letter-spacing: 0.4px;
        box-shadow: 0 14px 30px rgba(79, 70, 229, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease), filter 0.35s ease;
    }
    .stButton > button::after, [data-testid="stButton"] > button::after,
    .stDownloadButton > button::after, [data-testid="stDownloadButton"] > button::after,
    [data-testid="stFormSubmitButton"] > button::after {
        content: ""; position: absolute; top: 0; left: -120%; width: 55%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.5), transparent);
        transform: skewX(-20deg); transition: left 0.8s ease; pointer-events: none;
    }
    .stButton > button:hover, [data-testid="stButton"] > button:hover,
    .stDownloadButton > button:hover, [data-testid="stDownloadButton"] > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-3px) scale(1.01);
        filter: brightness(1.07) saturate(1.1);
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }
    .stButton > button:hover::after, [data-testid="stButton"] > button:hover::after,
    .stDownloadButton > button:hover::after, [data-testid="stDownloadButton"] > button:hover::after,
    [data-testid="stFormSubmitButton"] > button:hover::after { left: 140%; }
    .stButton > button:active, [data-testid="stButton"] > button:active,
    .stDownloadButton > button:active, [data-testid="stFormSubmitButton"] > button:active {
        transform: translateY(1px) scale(0.99);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
    }
    .stButton > button:focus-visible, [data-testid="stButton"] > button:focus-visible,
    [data-testid="stFormSubmitButton"] > button:focus-visible { outline: 3px solid rgba(99, 102, 241, 0.45); outline-offset: 3px; }
    .stButton > button:disabled, [data-testid="stButton"] > button:disabled {
        background: rgba(241, 245, 249, 0.95) !important;
        color: #64748B !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: none; filter: none; transform: none; cursor: not-allowed;
    }
    .stButton > button:disabled::after, [data-testid="stButton"] > button:disabled::after { display: none; }

    .stApp .stButton > button p, .stApp [data-testid="stButton"] > button p,
    .stApp .stDownloadButton > button p, .stApp [data-testid="stDownloadButton"] > button p,
    .stApp [data-testid="stFormSubmitButton"] > button p { color: inherit !important; font-weight: inherit; margin: 0; }

    /* Varian merah & hijau (dibungkus container btnred_* / btngreen_*) */
    .stApp [class*="st-key-btnred_"] [data-testid="stButton"] > button, .stApp [class*="st-key-btnred_"] .stButton > button {
        background: linear-gradient(135deg, #F43F5E 0%, #DC2626 100%) !important;
        box-shadow: 0 14px 30px rgba(239, 68, 68, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }
    .stApp [class*="st-key-btnred_"] [data-testid="stButton"] > button:hover, .stApp [class*="st-key-btnred_"] .stButton > button:hover {
        box-shadow: 0 20px 40px rgba(239, 68, 68, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }
    .stApp [class*="st-key-btngreen_"] [data-testid="stButton"] > button, .stApp [class*="st-key-btngreen_"] .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        box-shadow: 0 14px 30px rgba(16, 185, 129, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }
    .stApp [class*="st-key-btngreen_"] [data-testid="stButton"] > button:hover, .stApp [class*="st-key-btngreen_"] .stButton > button:hover {
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }

    /* Pilihan kuis: kartu putih dengan lencana huruf A/B/C/D otomatis */
    .st-key-quizopts { counter-reset: opt; }
    .stApp .st-key-quizopts [data-testid="stButton"] > button, .stApp .st-key-quizopts .stButton > button {
        min-height: 5.6rem; padding: 18px 26px 18px 76px !important;
        border-radius: 26px !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.97), rgba(248,250,252,0.90)) !important;
        border: 2px solid rgba(226, 232, 240, 0.95) !important;
        color: var(--ink) !important;
        font-size: 16px; font-weight: 600; line-height: 1.4; white-space: normal;
        justify-content: flex-start; text-align: left;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05), inset 0 1px 0 #FFFFFF;
    }
    .stApp .st-key-quizopts [data-testid="stButton"] > button p, .stApp .st-key-quizopts .stButton > button p { text-align: left; }
    .stApp .st-key-quizopts [data-testid="stButton"] > button:hover, .stApp .st-key-quizopts .stButton > button:hover {
        background: linear-gradient(135deg, #ECFDF5, #F0FDF4) !important;
        border-color: #10B981 !important; color: #047857 !important;
        box-shadow: 0 18px 36px rgba(16, 185, 129, 0.20); filter: none;
    }
    .st-key-quizopts [data-testid="stButton"] > button::after, .st-key-quizopts .stButton > button::after { display: none; }
    .st-key-quizopts [data-testid="stColumn"] button::before, .st-key-quizopts [data-testid="column"] button::before {
        counter-increment: opt; content: counter(opt, upper-alpha);
        position: absolute; left: 20px; top: 50%; transform: translateY(-50%);
        width: 40px; height: 40px; border-radius: 14px; display: grid; place-items: center;
        background: linear-gradient(135deg, #2563EB, #7C3AED); color: #FFFFFF;
        font-weight: 800; font-size: 17px; box-shadow: 0 8px 18px rgba(79, 70, 229, 0.30);
        transition: background 0.3s ease;
    }
    .st-key-quizopts [data-testid="stColumn"] button:hover::before, .st-key-quizopts [data-testid="column"] button:hover::before { background: linear-gradient(135deg, #10B981, #059669); }

    /* =====================================================
       7. INPUT, SELECT, TEXTAREA, UPLOADER, RADIO
       ===================================================== */
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.92) !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 20px !important;
        box-shadow: inset 0 2px 4px rgba(15, 23, 42, 0.03);
        transition: border-color 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
    }
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div { background: transparent !important; border: none !important; box-shadow: none !important; }
    div[data-baseweb="input"]:hover, div[data-baseweb="textarea"]:hover, div[data-baseweb="select"] > div:hover { border-color: #BFDBFE !important; }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: #60A5FA !important;
        background: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.22), inset 0 2px 4px rgba(15, 23, 42, 0.01) !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span, textarea, input { color: var(--ink) !important; font-weight: 600; font-size: 15px; }
    input::placeholder, textarea::placeholder { color: #94A3B8 !important; opacity: 1; font-weight: 500; }

    div[data-baseweb="popover"] > div { border-radius: 20px !important; }
    div[data-baseweb="popover"] ul[role="listbox"], div[data-baseweb="popover"] [data-baseweb="menu"] {
        background: rgba(255, 255, 255, 0.97) !important;
        border: 1px solid #E2E8F0; border-radius: 20px; padding: 6px;
        box-shadow: var(--shadow-lg);
    }
    div[data-baseweb="popover"] li { color: var(--ink-soft) !important; font-family: 'Outfit', sans-serif !important; font-weight: 600; border-radius: 14px; margin: 2px 0; transition: background 0.2s ease; }
    div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li[aria-selected="true"] { background: #EFF6FF !important; color: var(--blue) !important; }

    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.72) !important;
        border: 2px dashed #BFDBFE !important;
        border-radius: 24px !important;
        padding: 26px !important;
        transition: border-color 0.3s ease, background 0.3s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover { border-color: #60A5FA !important; background: rgba(239, 246, 255, 0.92) !important; }
    [data-testid="stFileUploader"] button {
        border-radius: 100px !important; padding: 8px 22px !important;
        background: #FFFFFF !important; border: 1px solid #BFDBFE !important;
        color: var(--blue) !important; font-weight: 700;
    }

    /* Radio (opsi biasa): kapsul kaca lembut */
    div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.66) !important;
        padding: 12px 18px; border-radius: 18px; margin-bottom: 8px;
        border: 1px solid rgba(226, 232, 240, 0.9);
        transition: all 0.35s var(--ease); cursor: pointer;
    }
    div[role="radiogroup"] > label p, div[role="radiogroup"] > label div { color: #334155 !important; font-weight: 700; font-size: 14px; letter-spacing: 0.3px; }
    div[role="radiogroup"] > label:hover { background: #EFF6FF !important; border: 1px solid #BFDBFE; transform: translateX(6px); box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08); }
    div[role="radiogroup"] > label:hover p, div[role="radiogroup"] > label:hover div { color: #2563EB !important; }
    div[role="radiogroup"] > label:has(input:checked) { background: #EEF2FF !important; border: 1px solid #A5B4FC; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.14); }

    /* =====================================================
       8. TAB (SEGMENTED CONTROL KACA)
       ===================================================== */
    div[data-baseweb="tab-list"] {
        gap: 6px; padding: 6px;
        background: rgba(255, 255, 255, 0.55);
        border: 1px solid var(--glass-edge);
        border-radius: 100px;
        box-shadow: inset 0 2px 6px rgba(15, 23, 42, 0.05), var(--shadow-sm);
        backdrop-filter: blur(14px);
    }
    button[data-baseweb="tab"] {
        background: transparent !important;
        color: var(--muted) !important;
        font-weight: 700; font-size: 15px;
        border-radius: 100px !important;
        padding: 10px 22px !important; height: auto !important;
        transition: background 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
    }
    .stApp button[data-baseweb="tab"] p { color: inherit !important; font-weight: 700; margin: 0; }
    button[data-baseweb="tab"]:hover { color: var(--blue) !important; background: rgba(255, 255, 255, 0.55) !important; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--blue) !important;
        background: #FFFFFF !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.16), inset 0 1px 0 #FFFFFF;
    }
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }
    div[data-baseweb="tab-panel"] { padding-top: 1.6rem; }

    /* =====================================================
       9. METRIC, TABEL, ALERT, TOAST, PROGRESS
       ===================================================== */
    [data-testid="stMetric"] {
        background: var(--glass-sheen);
        border: 1px solid var(--glass-edge);
        border-radius: 28px; padding: 26px 28px;
        box-shadow: var(--shadow-md), var(--inner-light);
        text-align: center; align-items: center;
    }
    [data-testid="stMetricLabel"] { justify-content: center; }
    [data-testid="stMetricLabel"] p { font-weight: 800; letter-spacing: 1.5px; font-size: 12px; color: var(--muted) !important; }
    div[data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px !important; font-weight: 900 !important; letter-spacing: -1px;
        justify-content: center;
    }
    [data-testid="stDataFrame"] { border-radius: 24px; overflow: hidden; border: 1px solid var(--glass-edge); box-shadow: var(--shadow-md); }
    [data-testid="stAlert"], [data-testid="stAlertContainer"] { border-radius: 20px !important; box-shadow: var(--shadow-sm); }
    [data-testid="stToast"] { border-radius: 22px !important; background: rgba(255, 255, 255, 0.94) !important; border: 1px solid var(--glass-edge); box-shadow: var(--shadow-lg); backdrop-filter: blur(18px); }
    .stProgress > div > div > div { background-color: rgba(148, 163, 184, 0.22) !important; border-radius: 100px; }
    .stProgress > div > div > div > div { background-image: linear-gradient(90deg, #38BDF8, #6366F1, #D946EF); border-radius: 100px; box-shadow: 0 2px 12px rgba(99, 102, 241, 0.45); }
    hr { border-color: rgba(148, 163, 184, 0.28); }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #93C5FD, #A5B4FC); border-radius: 100px; border: 2px solid rgba(255,255,255,0.6); }

    /* =====================================================
       10. SIDEBAR MENGAMBANG (KACA) + NAVIGASI
       ===================================================== */
    [data-testid="stSidebar"] { background-color: transparent !important; border: none !important; }
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(160deg, rgba(255,255,255,0.90) 0%, rgba(255,255,255,0.68) 100%) !important;
        backdrop-filter: blur(40px) saturate(200%);
        -webkit-backdrop-filter: blur(40px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-radius: 36px;
        margin: 1.2rem;
        height: calc(100vh - 2.4rem) !important;
        box-shadow: 18px 24px 60px rgba(30, 41, 120, 0.14), inset 0 1px 0 rgba(255,255,255,1);
        overflow-y: auto; overflow-x: hidden;
    }
    [data-testid="stSidebarContent"] { background: transparent !important; }
    [data-testid="stSidebarHeader"] { background: transparent; min-height: 0; height: auto; padding: 0.8rem 1rem 0 1rem; margin: 0; }
    [data-testid="stSidebarHeader"] img, [data-testid="stLogo"] { display: none; }
    [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"] {
        background: rgba(255, 255, 255, 0.85); border-radius: 16px;
        box-shadow: var(--shadow-sm); border: 1px solid var(--glass-edge);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label { background: transparent !important; padding: 13px 22px; border-radius: 100px; margin-bottom: 6px; border: 1px solid transparent; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label > :first-child:not(:has(p)) { display: none; }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: rgba(239, 246, 255, 0.95) !important; border: 1px solid #BFDBFE; transform: translateX(8px); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.08); }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.45);
        box-shadow: 0 12px 26px rgba(79, 70, 229, 0.34), inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transform: translateX(4px);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) div { color: #FFFFFF !important; }

    /* =====================================================
       11. RESPONSIF & AKSESIBILITAS
       ===================================================== */
    @media (max-width: 768px) {
        .block-container { padding: 1.4rem 1rem 4rem 1rem !important; }
        [class*="st-key-kartu_"] { padding: 22px 20px !important; border-radius: 24px; }
        .st-key-kartu_hero { padding: 26px 22px !important; }
        .q-card { padding: 36px 24px; }
        .reader-card { padding: 28px 22px; }
        .lb-row { padding: 14px 16px; gap: 12px; flex-wrap: wrap; }
        button[data-baseweb="tab"] { padding: 8px 14px !important; font-size: 13px; }
        [data-testid="stSidebar"] > div:first-child { margin: 0.5rem; height: calc(100vh - 1rem) !important; border-radius: 28px; }
    }
    @media (prefers-reduced-motion: reduce) {
        .stApp::before, .gradient-text, .block-container { animation: none !important; }
        .stat-card, .lb-row, .mad-card, .score-card, .stButton > button { transition: none !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI MESIN CLOUD (SUPABASE)
# ==========================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"].strip()
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()
    HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}
except Exception:
    st.error("🚨 Kunci Supabase belum disetel di Streamlit Secrets!")
    st.stop()

# ==========================================
# 3. FUNGSI DATABASE LENGKAP (ANTI-LAG ENGINE)
# ==========================================
def db_get_user(username):
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?username=ilike.{username}", headers=HEADERS).json()
        return res[0] if isinstance(res, list) and len(res) > 0 else None
    except: return None

def db_create_user(username, hashed_pwd):
    data = {"username": username, "password": hashed_pwd, "avatar_name": "Geni Us", "title": "📜 Cendekiawan Muda", "points": 0, "streak": 1, "display_name": username}
    requests.post(f"{SUPABASE_URL}/rest/v1/users_cloud", headers=HEADERS, json=data)

def db_update_points(username, new_points):
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json={"points": new_points})

def db_update_avatar(username, avatar_name):
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json={"avatar_name": avatar_name})

def db_update_title(username, title, cost=0):
    payload = {"title": title}
    if cost > 0:
        current = db_get_user(username)
        if current: payload["points"] = current["points"] - cost
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json=payload)

def db_update_profile(username, display_name, custom_avatar=None):
    payload = {"display_name": display_name}
    if custom_avatar:
        payload["custom_avatar"] = custom_avatar
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json=payload)

def db_get_learned_history(username):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/kuis_history_cloud?username=eq.{username}", headers=HEADERS).json()
    return set([row["id_kuis"] for row in res]) if isinstance(res, list) else set()

def db_add_kuis_history(username, id_kuis):
    requests.post(f"{SUPABASE_URL}/rest/v1/kuis_history_cloud", headers=HEADERS, json={"username": username, "id_kuis": id_kuis})

@st.cache_data(ttl=60)
def db_get_leaderboard():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,display_name,points,title&order=points.desc&limit=10", headers=HEADERS).json()
    return res if isinstance(res, list) else []

@st.cache_data(ttl=60)
def db_get_all_users_admin():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,title,points,streak&order=points.desc", headers=HEADERS).json()
    return res if isinstance(res, list) else []

def db_get_random_opponent(exclude_username):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?username=neq.{exclude_username}&limit=10", headers=HEADERS).json()
    return random.choice(res) if isinstance(res, list) and len(res) > 0 else None

def db_update_pvp_win(winner, loser, winner_current_pts, loser_current_pts):
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{winner}", headers=HEADERS, json={"points": winner_current_pts + 100})
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{loser}", headers=HEADERS, json={"points": max(0, loser_current_pts - 20)})

def db_update_pvp_lose(loser, loser_current_pts):
    requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{loser}", headers=HEADERS, json={"points": max(0, loser_current_pts - 30)})

# --- FUNGSI MULTIPLAYER LOBBY SYSTEM ---
def db_create_quiz_session(code, host, mapel):
    data = {"session_code": code, "host_username": host, "mapel": mapel, "status": "waiting"}
    requests.post(f"{SUPABASE_URL}/rest/v1/quiz_sessions", headers=HEADERS, json=data)

def db_get_quiz_session(code):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/quiz_sessions?session_code=eq.{code}", headers=HEADERS).json()
    return res[0] if isinstance(res, list) and len(res) > 0 else None

def db_get_waiting_sessions():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/quiz_sessions?status=eq.waiting", headers=HEADERS).json()
    return res if isinstance(res, list) else []

def db_update_session_status(code, status):
    requests.patch(f"{SUPABASE_URL}/rest/v1/quiz_sessions?session_code=eq.{code}", headers=HEADERS, json={"status": status})

def db_join_session(code, username):
    check = requests.get(f"{SUPABASE_URL}/rest/v1/session_players?session_code=eq.{code}&username=eq.{username}", headers=HEADERS).json()
    if isinstance(check, list) and len(check) == 0:
        data = {"session_code": code, "username": username, "score": 0, "status": "joined"}
        requests.post(f"{SUPABASE_URL}/rest/v1/session_players", headers=HEADERS, json=data)

def db_get_session_players(code):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/session_players?session_code=eq.{code}&order=score.desc", headers=HEADERS).json()
    return res if isinstance(res, list) else []

def db_update_player_score(code, username, score):
    url = f"{SUPABASE_URL}/rest/v1/session_players?session_code=eq.{code}&username=eq.{username}"
    requests.patch(url, headers=HEADERS, json={"score": score, "status": "finished"})

# --- FUNGSI CUSTOM QUIZ (PABRIK SOAL) ---
def db_save_custom_quiz(title, creator, questions):
    data = {"title": title, "creator": creator, "questions": questions}
    requests.post(f"{SUPABASE_URL}/rest/v1/custom_quizzes", headers=HEADERS, json=data)

@st.cache_data(ttl=60)
def db_get_all_custom_quizzes():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/custom_quizzes", headers=HEADERS).json()
    return res if isinstance(res, list) else []

def db_get_custom_quiz_by_title(title):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/custom_quizzes?title=eq.{title}", headers=HEADERS).json()
    return res[0] if isinstance(res, list) and len(res) > 0 else None

# ==========================================
# 4. INISIALISASI SESSION & UTILITAS
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "gacha_claimed" not in st.session_state: st.session_state.gacha_claimed = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False

if "quizizz_aktif" not in st.session_state: st.session_state.quizizz_aktif = False
if "qz_soal" not in st.session_state: st.session_state.qz_soal = []
if "qz_index" not in st.session_state: st.session_state.qz_index = 0
if "qz_score" not in st.session_state: st.session_state.qz_score = 0
if "qz_selesai" not in st.session_state: st.session_state.qz_selesai = False
if "current_room_code" not in st.session_state: st.session_state.current_room_code = ""
if "is_host" not in st.session_state: st.session_state.is_host = False
if "temp_q" not in st.session_state: st.session_state.temp_q = []
if "sfx" not in st.session_state: st.session_state.sfx = ""

PASSWORD_ADMIN = "LEARNWITHLM"
# Gelar Akademis & Prestigius
DAFTAR_GELAR = {"📜 Cendekiawan Muda": 0, "🖋️ Pujangga Aksara": 200, "🏛️ Anggota Akademi": 400, "👑 Mahaguru Server": 1000}

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def bersihkan_nama(teks): return re.sub(r'[\\/*?:"<>|]', "", teks)

try:
    from database_rangkuman import DATA_MATERI
    from database_soal import BANK_SOAL_PRO
except ImportError:
    DATA_MATERI, BANK_SOAL_PRO = {}, {}
    st.warning("⚠️ File database lokal (Akademik) belum terpasang sempurna.")

if not st.session_state.logged_in:
    st.markdown("""<style>[data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"] {display: none !important;} [data-testid="stSidebar"] {display: none !important;}</style>""", unsafe_allow_html=True)

def tampilkan_avatar(keyword):
    st.markdown(f"<div class='avatar-emoji'>{'🎓' if keyword=='genius' else '📚'}</div>", unsafe_allow_html=True)

# ==========================================
# 5. PORTAL LOGIN / REGISTER (GERBANG AKADEMI)
# ==========================================
if not st.session_state.logged_in:
    # Deteksi dan Tampilkan Logo jika ada
    logo_path = None
    if os.path.exists("logo.jpg"): logo_path = "logo.jpg"
    elif os.path.exists("logo.png"): logo_path = "logo.png"
    
    if logo_path:
        st.image(logo_path, width=110, output_format="auto")
        st.markdown("<style>[data-testid='stImage'] { display:flex; justify-content:center; } [data-testid='stImage'] img { border-radius: 30px; box-shadow: 0 18px 44px rgba(37,99,235,0.18), inset 0 1px 0 rgba(255,255,255,1); border: 1px solid rgba(255,255,255,0.95); padding:8px; background:rgba(255,255,255,0.85); }</style>", unsafe_allow_html=True)
    
    st.markdown("<div class='hero'><h1 class='hero-title'><span class='gradient-text'>AKSARA</span></h1><div class='hero-sub'>INSTITUT EDUKASI INTERAKTIF</div></div>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.2, 1])
    with col_form:
        with kartu("login"):
            tab_log, tab_reg = st.tabs(["🔐 GERBANG MASUK", "📝 REGISTRASI"])
            
            with tab_log:
                l_user = st.text_input("Nama Cendekiawan:", key="l_usr").strip()
                l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
                if st.button("Masuki Akademi"):
                    if l_user and l_pass:
                        user_record = db_get_user(l_user)
                        if user_record and user_record.get("password") == hash_password(l_pass):
                            st.session_state.username = user_record["username"] 
                            st.session_state.logged_in = True; st.rerun()
                        else: st.error("Kredensial tidak dikenali institut!")
                    else: st.warning("Formulir belum lengkap!")
                    
            with tab_reg:
                r_user = st.text_input("Nama Panggilan (Maks 15 Karakter):", max_chars=15, key="r_usr").strip()
                r_pass = st.text_input("Sandi Keamanan:", type="password", key="r_pwd").strip()
                if st.button("Daftarkan Nama Saya"):
                    if r_user and r_pass:
                        if db_get_user(r_user): st.error("Nama ini sudah terdaftar dalam arsip akademi!")
                        else:
                            db_create_user(r_user, hash_password(r_pass))
                            st.success("Pendaftaran Berhasil! Silakan masuk melalui Gerbang Masuk.")
                    else: st.warning("Formulir belum lengkap!")
    st.stop()

# ==========================================
# 6. MEMUAT DATA PEMAIN & EFEK SUARA BARU
# ==========================================
if st.session_state.sfx == "benar":
    st.markdown('<audio autoplay style="display:none;"><source src="https://actions.google.com/sounds/v1/bell/bell_ring.ogg" type="audio/ogg"></audio>', unsafe_allow_html=True)
    st.session_state.sfx = ""
elif st.session_state.sfx == "salah":
    st.markdown('<audio autoplay style="display:none;"><source src="https://actions.google.com/sounds/v1/impacts/wood_hit_hollow.ogg" type="audio/ogg"></audio>', unsafe_allow_html=True)
    st.session_state.sfx = ""

player = st.session_state.username
user_data = db_get_user(player)

if not user_data:
    st.session_state.logged_in = False; st.rerun()

avatar_db = user_data.get("avatar_name", "Geni Us")
title_db = user_data.get("title", "📜 Cendekiawan Muda")
points_db = user_data.get("points", 0)
streak_db = user_data.get("streak", 1)

display_name_db = user_data.get("display_name")
if not display_name_db: display_name_db = player
custom_avatar_db = user_data.get("custom_avatar")

learned_db = db_get_learned_history(player)
user_level = (points_db // 100) + 1

def get_tier(lvl):
    if lvl < 3: return "🥉 Tingkat Dasar", "#D97706" 
    elif lvl < 6: return "🥈 Tingkat Menengah", "#64748B"
    elif lvl < 10: return "🥇 Tingkat Atas", "#EAB308"
    elif lvl < 15: return "💎 Sarjana", "#06B6D4" 
    else: return "🌌 Mahaguru", "#8B5CF6" 
tier_name, tier_color = get_tier(user_level)

# --- SIDEBAR NAVIGASI MENGAMBANG (GLASSMORPHISM PANEL BERSIH & JELAS) ---
with st.sidebar:
    # 1. AVATAR & PROFIL PANEL
    if custom_avatar_db:
        st.markdown(f"<div class='profile'><div class='avatar-ring'><img src='{custom_avatar_db}'></div></div>", unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<div class='profile'><div class='profile-name'>{display_name_db}</div><div class='badge-row'><span class='badge badge-title'>{title_db}</span></div><div class='badge-row'><span class='badge badge-tier' style='--tier:{tier_color};'>{tier_name}</span></div></div>", unsafe_allow_html=True)
    
    # 2. LEVEL PROGRESS BAR
    prog = points_db % 100
    st.markdown(f"""
        <div class='xp-bar'><div class='xp-fill' style='width:{prog}%;'></div></div>
        <div class='xp-meta'><span>Lvl {user_level}</span><span class='xp-pts'>✨ {points_db} Pts</span></div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div><div class='nav-label'>MENU UTAMA</div>", unsafe_allow_html=True)
    
    # 3. RADIO MENU
    menu = st.radio("NAVIGASI INSTITUT", [
        "🏠 Dashboard Utama", 
        "📢 Mading Pemberitahuan", 
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ], label_visibility="collapsed", key="navigasi_utama")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # 4. TOMBOL LOGOUT
    with tombol_merah("logout"):
        if st.button("Keluar Aplikasi"):
            st.session_state.logged_in = False
            st.rerun()


# ==========================================
# HALAMAN 1: DASHBOARD UTAMA
# ==========================================
def kartu_statistik(ikon, nilai, label, aksen="#2563EB", warna_nilai=False):
    gaya_nilai = " style='color:var(--accent);'" if warna_nilai else ""
    return f"<div class='stat-card' style='--accent:{aksen};'><div class='stat-icon'>{ikon}</div><div class='stat-value'{gaya_nilai}>{nilai}</div><div class='stat-label'>{label}</div></div>"

if menu == "🏠 Dashboard Utama":
    with kartu("hero"):
        st.markdown(f"<h1 style='font-size:clamp(34px, 4.4vw, 54px); margin-bottom:5px; font-weight:900; letter-spacing:-1.5px;'>Welcome back, <span class='gradient-text'>{display_name_db}</span></h1>", unsafe_allow_html=True)
        st.caption("Akses semua catatan akademi dan pantau perkembangan belajarmu hari ini.")
    
    if not st.session_state.gacha_claimed:
        with kartu("honor"):
            h_judul, h_aksi = st.columns([3, 2])
            with h_judul:
                st.markdown("<h2 style='color:#2563EB; margin:0; font-size:26px; font-weight:800; letter-spacing:-0.5px;'>✨ Daily Honor Roll</h2>", unsafe_allow_html=True)
            with h_aksi:
                if st.button("Buka Scroll Keberuntungan"):
                    bonus = random.choice([20, 50, 100, 150, 200])
                    db_update_points(player, points_db + bonus)
                    st.session_state.gacha_claimed = True
                    st.session_state.sfx = "benar" 
                    st.balloons()
                    st.success(f"DIBERKAHI! Kamu mendapat +{bonus} Poin Akademik!")
                    time.sleep(1)
                    st.rerun()

    c1, c2, c3 = st.columns(3)
    c1.markdown(kartu_statistik("⏳", streak_db, "HARI AKTIF"), unsafe_allow_html=True)
    c2.markdown(kartu_statistik("📚", len(learned_db), "MODUL SELESAI"), unsafe_allow_html=True)
    c3.markdown(kartu_statistik("🏛️", f"Lvl {user_level}", "STATUS AKADEMI", aksen=tier_color, warna_nilai=True), unsafe_allow_html=True)
        
    st.markdown("<div class='section-title'><span class='gradient-text'>Hall of Scholars</span> (Top 10)</div>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    if ranking_data:
        poin_tertinggi = max([(r.get("points", 0) or 0) for r in ranking_data])
        baris_html = ""
        for i, row in enumerate(ranking_data):
            if i == 0: medali, bg_color, bdr_color = "👑", "linear-gradient(90deg, #FEF3C7, #FFFBEB)", "#FCD34D"
            elif i == 1: medali, bg_color, bdr_color = "🥈", "linear-gradient(90deg, #F1F5F9, #FFFFFF)", "#CBD5E1"
            elif i == 2: medali, bg_color, bdr_color = "🥉", "linear-gradient(90deg, #FFEDD5, #FFF7ED)", "#FDBA74"
            else: medali, bg_color, bdr_color = f"#{i+1}", "rgba(255,255,255,0.8)", "#E2E8F0"
            
            d_name = row.get("display_name")
            if not d_name: d_name = row.get("username", "Anonim")
            
            poin_baris = row.get("points", 0) or 0
            persen = int(poin_baris / poin_tertinggi * 100) if poin_tertinggi > 0 else 0
            judul_baris = row.get("title", "")
            chip_judul = f"<span class='lb-title'>{judul_baris}</span>" if judul_baris else ""
            
            baris_html += f"<div class='lb-row' style='--bg:{bg_color}; --bdr:{bdr_color}; --w:{persen}%;'><div class='lb-rank'>{medali}</div><div class='lb-name'>{d_name}</div>{chip_judul}<div class='lb-pts'>✨ {row.get('points', 0)}</div></div>"
        st.markdown(f"<div class='lb'>{baris_html}</div>", unsafe_allow_html=True)


# ==============================================================================
# HALAMAN 2: MADING PEMBERITAHUAN
# ==============================================================================
def sumber_gambar(g):
    if isinstance(g, str): return g
    try: return f"data:{g.type};base64," + base64.b64encode(g.getvalue()).decode()
    except Exception: return ""

def kartu_mading_html(item):
    tag = f"<span class='mading-tag'>{item['kategori']}</span>"
    src = sumber_gambar(item['gambar']) if item['gambar'] else ""
    gambar_html = f"<div class='mad-img'><img src='{src}'>{tag}</div>" if src else f"<div class='mad-img'>{tag}</div>"
    deskripsi = str(item['deskripsi']).replace("\n", "<br>")
    return f"<div class='mad-card'>{gambar_html}<div class='mad-text'><div class='mading-title-text'>{item['judul']}</div><div class='mading-meta'>RELEASED: {item['tanggal']}</div><div class='mading-body'>{deskripsi}</div></div></div>"

if menu == "📢 Mading Pemberitahuan":
    st.markdown("<h1 style='font-size:42px; margin-bottom: 5px; font-weight:900;'>Bulletin Board</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color:#475569; font-weight:500;'>Informasi kreatif, pengumuman penting, dan galeri poster institut.</p>", unsafe_allow_html=True)
    
    if 'list_mading' not in st.session_state:
        st.session_state.list_mading = [
            {
                "judul": "Grand Launching Fitur Live Arena Quiz!",
                "kategori": "Event",
                "tanggal": "06 Juli 2026",
                "deskripsi": "Siapkan strategimu dan uji kemampuanmu langsung di menu Live Arena Quiz yang baru saja aktif. Kumpulkan poin sebanyak-banyaknya untuk menaikkan peringkat tier-mu!",
                "gambar": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=800&auto=format&fit=crop"
            },
            {
                "judul": "Tips & Trik Menguasai Modul Pembelajaran Efektif",
                "kategori": "Edukasi",
                "tanggal": "04 Juli 2026",
                "deskripsi": "Buka menu Ruang Belajar & Modul secara berkala. Selesaikan kuis harian untuk mengklaim poin tambahan agar kamu bisa membuka item premium di Black Market Profil.",
                "gambar": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=800&auto=format&fit=crop"
            }
        ]
        
    tab_jelajah, tab_tambah = st.tabs(["🖼️ Eksplorasi Mading", "✍️ Pasang Pengumuman"])
    
    with tab_jelajah:
        if not st.session_state.list_mading:
            st.info("Mading saat ini kosong. Jadilah yang pertama memasang poster!")
        else:
            kolom_mading = st.columns(2)
            for indeks, item in enumerate(st.session_state.list_mading):
                with kolom_mading[indeks % 2]:
                    try:
                        st.markdown(kartu_mading_html(item), unsafe_allow_html=True)
                    except:
                        st.caption("⚠️ Gagal memuat berkas gambar poster.")
                    
    with tab_tambah:
        with kartu("mading_form"):
            st.markdown("<h3 style='font-size:24px; margin-bottom:10px; font-weight:800;'>Buat Poster Mading Baru</h3>", unsafe_allow_html=True)
            
            with st.form("form_tambah_mading", clear_on_submit=True):
                judul_baru = st.text_input("Judul Poster / Pengumuman")
                kategori_baru = st.selectbox("Label Kategori", ["Event", "Informasi", "Pembaruan", "Edukasi", "Prestasi"])
                deskripsi_baru = st.text_area("Isi Informasi / Deskripsi Singkat", height=150)
                
                pilihan_media = st.radio("Media Gambar", ["URL Tautan Eksternal", "Unggah Perangkat"])
                tautan_gambar = ""
                
                if pilihan_media == "URL Tautan Eksternal":
                    tautan_gambar = st.text_input("URL Gambar (HTTPS)")
                else:
                    berkas_unggah = st.file_uploader("Unggah JPG/PNG", type=["jpg", "jpeg", "png"])
                    if berkas_unggah is not None:
                        tautan_gambar = berkas_unggah
                        
                tombol_submit = st.form_submit_button("Publikasikan Poster")
                
                if tombol_submit:
                    if judul_baru.strip() != "" and deskripsi_baru.strip() != "":
                        import datetime
                        waktu_sekarang = datetime.date.today().strftime("%d %B %Y")
                        
                        st.session_state.list_mading.insert(0, {
                            "judul": judul_baru,
                            "kategori": kategori_baru,
                            "tanggal": waktu_sekarang,
                            "deskripsi": deskripsi_baru,
                            "gambar": tautan_gambar
                        })
                        st.success("Berhasil dipublikasikan!")
                        st.rerun()
                    else:
                        st.error("Judul dan Deskripsi wajib diisi.")


# ==========================================
# HALAMAN 3: LIVE ARENA QUIZ
# ==========================================
elif menu == "⚡ Live Arena Quiz (NEW!)":
    st.markdown("<h1><span class='gradient-text'>ARENA UJIAN TERBUKA</span></h1>", unsafe_allow_html=True)
    
    custom_quizzes_db = db_get_all_custom_quizzes()
    list_custom_titles = [f"🌟 {q['title']} (Karya {q['creator']})" for q in custom_quizzes_db]
    pilihan_mapel_gabungan = list(BANK_SOAL_PRO.keys()) + list_custom_titles

    if not st.session_state.quizizz_aktif and not st.session_state.qz_selesai and not st.session_state.current_room_code:
        tab_solo, tab_join, tab_host, tab_create = st.tabs(["🎮 MANDIRI", "👥 AULA BERSAMA", "👑 BUKA AULA", "🛠️ ARSIPATOR"])
        
        with tab_solo:
            with kartu("solo"):
                mapel_solo = st.selectbox("Pilih Kurikulum Ujian:", pilihan_mapel_gabungan, key="solo_m")
                if st.button("Mulai Studi Mandiri", key="btn_solo"):
                    if mapel_solo.startswith("🌟 "):
                        title_only = mapel_solo.replace("🌟 ", "").split(" (Karya ")[0]
                        cq = db_get_custom_quiz_by_title(title_only)
                        semua_soal = cq["questions"]
                    else:
                        semua_soal = []
                        for kl, d_bab in BANK_SOAL_PRO.get(mapel_solo, {}).items():
                            for bb, d_sub in d_bab.items():
                                for sub, list_soal in d_sub.items(): semua_soal.extend(list_soal)
                    
                    if len(semua_soal) >= 3:
                        st.session_state.qz_soal = random.sample(semua_soal, min(5, len(semua_soal)))
                        st.session_state.qz_index = 0
                        st.session_state.qz_score = 0
                        st.session_state.quizizz_aktif = True
                        st.session_state.is_host = False
                        st.rerun()
                    else: st.error("Materi ujian terlalu minim data.")
            
        with tab_join:
            with kartu("join"):
                st.markdown("<h3 style='font-size:22px;'>AULA AKTIF</h3>", unsafe_allow_html=True)
                c_ref, _ = st.columns([1, 3])
                with c_ref:
                    if st.button("Refresh Server"): st.rerun()
                
                active_rooms = db_get_waiting_sessions()
                if active_rooms:
                    for room in active_rooms:
                        with baris(f"room_{room['session_code']}"):
                            r_info, r_aksi = st.columns([4, 1])
                            with r_info:
                                st.markdown(f"<div class='room-title'>{room['mapel']}</div><div class='room-meta'>Host: {room['host_username']} &nbsp;|&nbsp; Kode: <span class='room-code'>{room['session_code']}</span></div>", unsafe_allow_html=True)
                            with r_aksi:
                                if st.button(f"Masuk Aula Ini", key=f"join_{room['session_code']}"):
                                    db_join_session(room['session_code'], player)
                                    st.session_state.current_room_code = room['session_code']
                                    st.session_state.is_host = False
                                    st.rerun()
                else:
                    st.caption("Tidak ada aula terbuka saat ini.")
                    
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                st.caption("Atau masukkan PIN Privat:")
                kode_input = st.text_input("PIN 6 Digit (Akses Privat):", max_chars=6).strip()
                if st.button("Gabung via PIN"):
                    if kode_input:
                        room = db_get_quiz_session(kode_input)
                        if room:
                            if room["status"] == "finished": st.error("Sesi telah ditutup.")
                            else:
                                db_join_session(kode_input, player)
                                st.session_state.current_room_code = kode_input
                                st.session_state.is_host = False
                                st.rerun()
                        else: st.error("PIN tidak valid.")
            
        with tab_host:
            with kartu("host"):
                st.markdown("<h3 style='font-size:22px;'>BUKA AULA BARU</h3>", unsafe_allow_html=True)
                mapel_guru = st.selectbox("Materi Ujian:", pilihan_mapel_gabungan, key="guru_m")
                if st.button("Buka Server Baru"):
                    random_code = str(random.randint(100000, 999999))
                    db_create_quiz_session(random_code, player, mapel_guru)
                    st.session_state.current_room_code = random_code
                    st.session_state.is_host = True
                    st.rerun()

        with tab_create:
            with kartu("create"):
                st.markdown("<h3 style='font-size:22px;'>MANUFAKTUR SOAL</h3>", unsafe_allow_html=True)
                judul_baru = st.text_input("Label / Judul Ujian Custom:").strip()
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                for i, q in enumerate(st.session_state.temp_q):
                    st.caption(f"✓ Terarsip: {q['soal']} (Jawaban: {q['jawaban']})")
                    
                with st.form("form_tambah_soal", clear_on_submit=True):
                    soal_text = st.text_area("Deskripsi Pertanyaan:", height=100)
                    c1, c2 = st.columns(2)
                    op_benar = c1.text_input("Opsi Valid (Kunci Benar):")
                    op_salah1 = c2.text_input("Opsi Palsu 1:")
                    op_salah2 = c1.text_input("Opsi Palsu 2:")
                    op_salah3 = c2.text_input("Opsi Palsu 3:")
                    
                    if st.form_submit_button("Simpan Soal Ini"):
                        if soal_text and op_benar and op_salah1 and op_salah2 and op_salah3:
                            st.session_state.temp_q.append({
                                "soal": soal_text,
                                "opsi": [op_benar, op_salah1, op_salah2, op_salah3],
                                "jawaban": op_benar
                            })
                            st.rerun()
                        else: st.warning("Data form belum utuh.")
                
                if st.button("Publikasikan ke Cloud"):
                    if not judul_baru: st.error("Label modul wajib diisi.")
                    elif db_get_custom_quiz_by_title(judul_baru): st.error("Label sudah eksis di cloud.")
                    elif len(st.session_state.temp_q) < 3: st.error("Gagal, butuh minimal 3 butir soal.")
                    else:
                        db_save_custom_quiz(judul_baru, player, st.session_state.temp_q)
                        st.session_state.temp_q = []
                        st.cache_data.clear()
                        st.success("Modul berhasil didistribusikan.")
                        time.sleep(1.5)
                        st.rerun()

    elif st.session_state.current_room_code and not st.session_state.quizizz_aktif and not st.session_state.qz_selesai:
        code = st.session_state.current_room_code
        room_info = db_get_quiz_session(code)
        players = db_get_session_players(code)
        
        with kartu("lobby"):
            st.markdown(f"<div class='lobby'><div class='lobby-mapel'>Sesi Modul: <b>{room_info['mapel']}</b></div><div class='lobby-label'>KODE AKSES PRIVAT</div><div class='lobby-code'>{code}</div><div class='lobby-count'>Partisipan Hadir: {len(players)}</div></div>", unsafe_allow_html=True)
            
            if players:
                chips_html = "".join([f"<span class='chip'>{p['username']}</span>" for p in players])
                st.markdown(f"<div class='chips'>{chips_html}</div>", unsafe_allow_html=True)
            else:
                st.caption("Menunggu koneksi partisipan...")
                
            c_ref, c_act = st.columns(2)
            with c_ref:
                with tombol_hijau("periksa"):
                    if st.button("Periksa Status"): st.rerun()
                
            with c_act:
                if st.session_state.is_host:
                    if st.button("Mulai Sesi (Start)"):
                        if len(players) == 0: st.error("Butuh minimal 1 partisipan klien.")
                        else:
                            db_update_session_status(code, "active")
                            st.rerun()
                else:
                    st.info("Menunggu eksekusi Host untuk memulai sesi...")
                    if room_info["status"] == "active":
                        m_aktif = room_info["mapel"]
                        if m_aktif.startswith("🌟 "):
                            title_only = m_aktif.replace("🌟 ", "").split(" (Karya ")[0]
                            cq = db_get_custom_quiz_by_title(title_only)
                            semua_soal = cq["questions"]
                        else:
                            semua_soal = []
                            for kl, d_bab in BANK_SOAL_PRO.get(m_aktif, {}).items():
                                for bb, d_sub in d_bab.items():
                                    for sub, list_soal in d_sub.items(): semua_soal.extend(list_soal)
                                    
                        st.session_state.qz_soal = random.sample(semua_soal, min(5, len(semua_soal)))
                        st.session_state.qz_index = 0
                        st.session_state.qz_score = 0
                        st.session_state.quizizz_aktif = True
                        st.rerun()
                        
            with tombol_merah("disconnect"):
                if st.button("Disconnect Server", key="exit_rm"):
                    if st.session_state.is_host: db_update_session_status(code, "finished")
                    st.session_state.current_room_code = ""
                    st.rerun()

        if st.session_state.is_host and room_info["status"] == "active":
            st.markdown("<h3 style='text-align:left; font-size:22px; margin-top:1.4rem;'>LIVE TELEMETRY</h3>", unsafe_allow_html=True)
            for rank, p in enumerate(players):
                status_icon = "Selesai" if p["status"] == "finished" else "Mengerjakan"
                st.markdown(f"<div class='tele-row'><span>{rank+1}. {p['username']} <span class='tele-status'>[{status_icon}]</span></span><span class='tele-score'>{p['score']} Pts</span></div>", unsafe_allow_html=True)

    elif st.session_state.quizizz_aktif:
        idx = st.session_state.qz_index
        total_soal = len(st.session_state.qz_soal)
        
        progress_val = int((idx / total_soal) * 100)
        st.progress(progress_val)
        st.markdown(f"<div class='q-meta'>PAGE {idx+1} OF {total_soal}</div>", unsafe_allow_html=True)
        
        soal_aktif = st.session_state.qz_soal[idx]
        opsi_acak = soal_aktif["opsi"].copy()
        random.shuffle(opsi_acak)
        
        st.markdown(f"<div class='q-card'>{soal_aktif['soal']}</div>", unsafe_allow_html=True)
        
        def cek_jawaban(jawaban_dipilih):
            if jawaban_dipilih == soal_aktif["jawaban"]:
                st.session_state.qz_score += 20
                st.session_state.sfx = "benar" 
                st.toast("Jawaban Benar: +20", icon="✅")
            else:
                st.session_state.sfx = "salah" 
                st.toast(f"Jawaban Salah. Kunci: {soal_aktif['jawaban']}", icon="❌")
            
            st.session_state.qz_index += 1
            if st.session_state.qz_index >= total_soal:
                st.session_state.quizizz_aktif = False
                st.session_state.qz_selesai = True
                if st.session_state.current_room_code:
                    db_update_player_score(st.session_state.current_room_code, player, st.session_state.qz_score)
            time.sleep(0.3)
            st.rerun()
        
        try: wadah_pilihan = st.container(key="quizopts")
        except TypeError: wadah_pilihan = st.container()
        with wadah_pilihan:
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            with c1: 
                if st.button(opsi_acak[0], key=f"o0_{idx}"): cek_jawaban(opsi_acak[0])
            with c2: 
                if st.button(opsi_acak[1], key=f"o1_{idx}"): cek_jawaban(opsi_acak[1])
            if len(opsi_acak) > 2:
                with c3: 
                    if st.button(opsi_acak[2], key=f"o2_{idx}"): cek_jawaban(opsi_acak[2])
                with c4: 
                    if st.button(opsi_acak[3], key=f"o3_{idx}"): cek_jawaban(opsi_acak[3])

    elif st.session_state.qz_selesai:
        final_xp = st.session_state.qz_score
        total_soal = len(st.session_state.qz_soal)
        akurasi = int((final_xp / 100) * 100) if total_soal > 0 else 0
        
        if akurasi > 70: st.balloons()
        
        st.markdown("<h1 style='text-align:center; font-size:clamp(40px, 6vw, 64px); margin:1.2rem 0 1.8rem 0;'><span class='gradient-text'>Sesi Selesai</span></h1>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='score-card'><div class='score-label'>Akurasi Logika</div><div class='score-value'>{akurasi}%</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='score-card good'><div class='score-label'>Poin Diperoleh</div><div class='score-value'>+{final_xp}</div></div>", unsafe_allow_html=True)
        
        st.write("")
        _, c_simpan, _ = st.columns([1, 2, 1])
        with c_simpan:
            if st.button("Simpan & Kembali ke Lobby"):
                if final_xp > 0: db_update_points(player, points_db + final_xp)
                st.session_state.qz_selesai = False
                st.session_state.current_room_code = ""
                st.rerun()


# ==========================================
# HALAMAN 4: MODE DUEL PVP
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1><span class='gradient-text'>ARENA DEBAT DEWAN</span></h1>", unsafe_allow_html=True)
    st.caption("Uji arsitektur berpikirmu menghadapi node cendekiawan lain secara asinkron.")
    
    pool_pvp = {}
    for mp, data_kelas in BANK_SOAL_PRO.items():
        pool_pvp[mp] = []
        for kl, data_bab in data_kelas.items():
            for bb, data_sub in data_bab.items():
                for sub, list_soal in data_sub.items():
                    pool_pvp[mp].extend(list_soal)
                
    if not pool_pvp:
        st.warning("⚠️ Database argumen debat belum diinisialisasi.")
        st.stop()
        
    if "lawan_duel" not in st.session_state: st.session_state.lawan_duel = None
    if "kuis_duel" not in st.session_state: st.session_state.kuis_duel = False
    if "soal_pvp_aktif" not in st.session_state: st.session_state.soal_pvp_aktif = None
    
    with kartu("duel_setup"):
        col_mapel, col_btn = st.columns([3,1])
        with col_mapel: mapel_duel = st.selectbox("Topik Arsitektur Debat:", list(pool_pvp.keys()))
        
        with col_btn:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("Cari Lawan Terdekat"):
                lawan = db_get_random_opponent(player)
                if lawan and len(pool_pvp[mapel_duel]) > 0:
                    l_disp = lawan.get("display_name")
                    if not l_disp: l_disp = lawan["username"]
                    
                    st.session_state.lawan_duel = (lawan["username"], l_disp, lawan.get("points", 0))
                    st.session_state.kuis_duel = True
                    soal_asli = random.choice(pool_pvp[mapel_duel])
                    opsi_acak = soal_asli["opsi"].copy()
                    random.shuffle(opsi_acak)
                    st.session_state.soal_pvp_aktif = {"soal": soal_asli["soal"], "opsi": opsi_acak, "jawaban": soal_asli["jawaban"]}
                else: st.error("Node aktif tidak ditemukan.")
            
    if st.session_state.lawan_duel and st.session_state.kuis_duel and st.session_state.soal_pvp_aktif:
        l_user, l_nama, l_pts = st.session_state.lawan_duel
        
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='duel-card' style='--bdr:#BFDBFE; --bg:linear-gradient(135deg, #EFF6FF, #FFFFFF); --clr:#1D4ED8; --clr2:#3B82F6;'><div class='duel-name'>{display_name_db}</div><div class='duel-pts'>✨ {points_db} Pts</div></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div class='vs-wrap'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='duel-card' style='--bdr:#FECACA; --bg:linear-gradient(135deg, #FEF2F2, #FFFFFF); --clr:#B91C1C; --clr2:#EF4444;'><div class='duel-name'>{l_nama}</div><div class='duel-pts'>✨ {l_pts} Pts</div></div>", unsafe_allow_html=True)
        
        with kartu("duel"):
            ds = st.session_state.soal_pvp_aktif
            st.markdown(f"<h3 style='font-size:24px; font-weight:800; color:#0F172A; line-height:1.7;'>{ds['soal']}</h3>", unsafe_allow_html=True)
            j_user = st.radio("Pilih Argumen Anda:", ds['opsi'], key="duel_ans")
            
            with tombol_hijau("eksekusi"):
                if st.button("Eksekusi Argumen Debat"):
                    if j_user == ds['jawaban']:
                        db_update_pvp_win(player, l_user, points_db, l_pts)
                        st.session_state.sfx = "benar" 
                        st.toast("Argumen Diterima.", icon="📜")
                        st.session_state.kuis_duel = False 
                        st.success(f"Logika Sempurna. Anda menang! (+100 Pts). Data {l_nama} berkurang 20 Pts.")
                    else:
                        db_update_pvp_lose(player, points_db)
                        st.session_state.sfx = "salah" 
                        st.toast("Argumen Gagal.", icon="🛡️")
                        st.session_state.kuis_duel = False
                        st.error(f"Kalkulasi meleset. Debat berakhir. Anda kehilangan 30 Pts.")
                    
                    st.write("<br>", unsafe_allow_html=True)
                    if st.button("Kembali ke Mimbar Utama"): st.rerun()


# ==========================================
# HALAMAN 5: RUANG BELAJAR & MODUL
# ==========================================
elif menu == "📖 Ruang Belajar & Modul":
    st.markdown("<h1><span class='gradient-text'>ARSIP SENTRAL (MODUL)</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with kartu("filter"):
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("Indeks Manuskrip:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("Tingkatan Kurikulum:", kelas_list if kelas_list else ["-"])
        
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("Sektor Bab:", bab_list if bab_list else ["-"])
        sub_list = DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).get(p_bab, {}).get("sub_bab", ["-"])
        with col4: p_sub = st.selectbox("Fokus Kajian Detail:", sub_list)
        
    st.write("")
    tab_mat, tab_doc = st.tabs(["📌 Ekstrak Data", "📂 Lampiran Dokumen"])
    
    with tab_mat:
        try: st.markdown(f"<div class='reader-card'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Sektor data ini kosong atau belum dialokasikan.")

    with tab_doc:
        with kartu("lampiran"):
            st.markdown("<h3 style='font-size:22px;'>📂 Repositori Eksternal</h3>", unsafe_allow_html=True)
            st.caption("Referensi visual pendukung akan dirujuk di partisi ini.")
            
            folder_t = os.path.join("uploads", bersihkan_nama(p_mapel), bersihkan_nama(p_kelas), bersihkan_nama(p_bab), bersihkan_nama(p_sub))
            if os.path.exists(folder_t) and len(os.listdir(folder_t)) > 0:
                for f in os.listdir(folder_t):
                    ext = f.split('.')[-1].lower()
                    file_path = os.path.join(folder_t, f)
                    
                    if ext in ['jpg', 'jpeg', 'png']:
                        st.image(file_path, caption=f"🖼️ {f}", use_container_width=True)
                    else:
                        with open(file_path, "rb") as file:
                            st.download_button(label=f"⬇️ UNDUH DOKUMEN: {f}", data=file.read(), file_name=f, mime="application/octet-stream")
            else:
                st.caption("Tidak ada lampiran yang dikaitkan pada sektor ini.")


# ==========================================
# HALAMAN 6: TOKO GELAR (BLACK MARKET)
# ==========================================
elif menu == "🛒 Black Market Profil":
    st.markdown("<h1><span class='gradient-text'>BIRO KUSTOMISASI</span></h1>", unsafe_allow_html=True)
    
    tab_av, tab_gl, tab_edit = st.tabs(["👤 Identitas Standar", "👑 Ekstraksi Gelar", "⚙️ Konfigurasi Kustom"])
    
    with tab_av:
        c1, c2 = st.columns(2)
        with c1:
            with kartu("av_geni"):
                st.markdown("<h2 style='font-size:22px; margin-bottom:10px;'>Geni Us</h2>", unsafe_allow_html=True)
                tampilkan_avatar("genius")
                if st.button("INISIALISASI: GENI US"):
                    db_update_profile(player, display_name_db, custom_avatar="")
                    db_update_avatar(player, "Geni Us")
                    st.toast("Paket Tampilan Diterapkan.", icon="🖼️"); st.rerun()
        with c2:
            with kartu("av_smart"):
                st.markdown("<h2 style='font-size:22px; margin-bottom:10px;'>Smar T</h2>", unsafe_allow_html=True)
                tampilkan_avatar("smart")
                if st.button("INISIALISASI: SMAR T"):
                    db_update_profile(player, display_name_db, custom_avatar="")
                    db_update_avatar(player, "Smar T")
                    st.toast("Paket Tampilan Diterapkan.", icon="🖼️"); st.rerun()
            
    with tab_gl:
        with kartu("gelar"):
            st.markdown("<h3 style='font-size:24px;'>Marketplace Kredensial</h3>", unsafe_allow_html=True)
            st.write(f"Saldo Tersedia: ✨ **{points_db} Pts**")
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            for no_gelar, (gelar, harga) in enumerate(DAFTAR_GELAR.items()):
                with baris(f"gelar_{no_gelar}"):
                    cg1, cg2, cg3 = st.columns([3, 1, 1])
                    cg1.markdown(f"<div class='gelar-name'>{gelar}</div>", unsafe_allow_html=True)
                    cg2.markdown(f"<div class='gelar-price'>✨ {harga}</div>", unsafe_allow_html=True)
                    with cg3:
                        if title_db == gelar: st.button("Tersemat", key=f"ak_{gelar}", disabled=True)
                        else:
                            if st.button("Beli Akses", key=f"by_{gelar}"):
                                if points_db >= harga:
                                    db_update_title(player, gelar, cost=harga)
                                    st.toast(f"Pembaruan Gelar Sukses: {gelar}", icon="📜"); st.rerun()
                                else: st.error("Saldo Pts tidak mencukupi.")
        
    with tab_edit:
        with kartu("profil"):
            st.markdown("<h3 style='font-size:24px;'>Kustomisasi Modul Visual</h3>", unsafe_allow_html=True)
            st.caption("Ubah nama tampilan dan unggah file avatar (JPG/PNG).")
            
            new_display = st.text_input("Definisi Nama Baru:", value=display_name_db, max_chars=20)
            new_foto = st.file_uploader("Suntikkan Paket Wajah (Otomatis Kompresi):", type=['png', 'jpg', 'jpeg'])
            
            if st.button("Simpan Perubahan Profil"):
                b64_foto = custom_avatar_db 
                
                if new_foto:
                    try:
                        img = Image.open(new_foto)
                        img = img.convert("RGB") 
                        img.thumbnail((150, 150))
                        buf = io.BytesIO()
                        img.save(buf, format="JPEG", quality=65)
                        b64_foto = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
                    except Exception as e:
                        st.error(f"Gagal memproses render: {e}")
                
                db_update_profile(player, new_display, b64_foto)
                st.toast("Profil berhasil diperbarui.", icon="✅")
                time.sleep(1)
                st.rerun()


# ==========================================
# HALAMAN 7: KONSOL ADMIN
# ==========================================
elif menu == "⚙️ Konsol Super Admin":
    st.markdown("<h1><span class='gradient-text'>SYSTEM ROOT ACCESS</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        _, c_portal, _ = st.columns([1, 1.6, 1])
        with c_portal:
            with kartu("admin"):
                st.markdown("<h2 style='font-size:24px; margin-bottom:10px;'>ENCRYPTED PORTAL</h2>", unsafe_allow_html=True)
                pwd = st.text_input("Masukan Kernel Password:", type="password")
                with tombol_merah("bypass"):
                    if st.button("Bypass Protocol"):
                        if pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
                        else: st.error("Akses Ditolak. Protokol pertahanan aktif.")
    else:
        st.success("Akses Root diizinkan.")
        tab_stat, tab_db, tab_upload = st.tabs(["📈 Log Sistem", "👥 Skema Pengguna", "📤 Distribusi Aset"])
        
        users_admin = db_get_all_users_admin()
        df = pd.DataFrame(users_admin) if users_admin else pd.DataFrame()
        
        with tab_stat:
            st.markdown("<h3 style='font-size:22px; margin-top:6px;'>Statistik Global Server</h3>", unsafe_allow_html=True)
            if not df.empty:
                c1, c2, c3 = st.columns(3)
                c1.metric("Node Klien Aktif", f"{len(df)}")
                c2.metric("Massa Poin Sirkulasi", f"{df['points'].sum()} Pts")
                c3.metric("Rerata Skor Global", f"{int(df['points'].mean())} Pts")
                
                with kartu("chart"):
                    st.markdown("<h4 style='font-size:18px;'>Distribusi Kekayaan Poin</h4>", unsafe_allow_html=True)
                    chart_data = df.set_index("username")["points"]
                    st.bar_chart(chart_data, use_container_width=True)
            else: st.info("Sistem belum merekam jejak.")
            
        with tab_db:
            if not df.empty:
                df_view = df[["username", "title", "points", "streak"]]
                df_view.columns = ["Username (ID)", "Label Status", "Points", "Ping Harian"]
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            
        with tab_upload:
            with kartu("upload"):
                st.markdown("<h3 style='font-size:22px;'>Manajemen Aset Statis</h3>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1: up_mapel = st.selectbox("Target Folder (Mapel):", list(DATA_MATERI.keys()), key="adm_m")
                k_list = list(DATA_MATERI.get(up_mapel, {}).keys())
                with c2: up_kelas = st.selectbox("Target Direktori (Tingkat):", k_list if k_list else ["-"], key="adm_k")
                
                c3, c4 = st.columns(2)
                b_list = list(DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).keys())
                with c3: up_bab = st.selectbox("Target Partisi (Bab):", b_list if b_list else ["-"], key="adm_b")
                s_list = DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).get(up_bab, {}).get("sub_bab", ["-"])
                with c4: up_sub = st.selectbox("Target Node (Sub):", s_list, key="adm_s")
                
                up_file = st.file_uploader("Pilih Berkas Payload (PDF/IMG):")
                
                with tombol_hijau("injeksi"):
                    if up_file and st.button("Injeksi ke Lokal Server"):
                        try:
                            folder_t = os.path.join("uploads", bersihkan_nama(up_mapel), bersihkan_nama(up_kelas), bersihkan_nama(up_bab), bersihkan_nama(up_sub))
                            os.makedirs(folder_t, exist_ok=True)
                            with open(os.path.join(folder_t, up_file.name), "wb") as f: f.write(up_file.getbuffer())
                            st.success("File sukses diunggah ke server lokal.")
                        except Exception as e: st.error(f"Injeksi gagal: {e}")

        st.write("")
        with tombol_merah("tutup_root"):
            if st.button("Tutup Akses Root"): st.session_state.is_admin = False; st.rerun()
