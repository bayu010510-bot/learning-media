import streamlit as st
import streamlit.components.v1 as components
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

# CSS HYPER-MODERN, HIGH-CONTRAST LUXURY GLASSMORPHISM
st.markdown("""
    <style>
    /* Menggunakan Font "Outfit" yang sangat modern, elegan, dan tajam (Bebas Teks Bunglon) */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* Latar Belakang Aurora Mesh (Terang, Halus, Nyaman di Mata) */
    .stApp { 
        background: radial-gradient(circle at 0% 0%, #E0F2FE 0%, transparent 40%),
                    radial-gradient(circle at 100% 0%, #EDE9FE 0%, transparent 40%),
                    radial-gradient(circle at 100% 100%, #CCFBF1 0%, transparent 40%),
                    radial-gradient(circle at 0% 100%, #F1F5F9 0%, transparent 40%),
                    #F8FAFC;
        color: #0F172A; 
        overflow-x: hidden;
    }
    
    /* Tipografi dengan Kontras Tinggi (Anti Teks Bunglon) */
    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; font-weight: 800; letter-spacing: -0.5px; color: #0F172A !important; }
    h4, h5, p, span, label, li { color: #334155 !important; font-weight: 500; }
    
    /* Efek Teks Gradient Spektakuler (Vibrant Tech Blue) */
    .gradient-text { 
        background: linear-gradient(135deg, #2563EB 0%, #8B5CF6 50%, #D946EF 100%);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 900; 
        display: inline-block;
        text-shadow: 0 8px 24px rgba(37, 99, 235, 0.2);
    }
    
    .vs-text { 
        background: linear-gradient(to right, #0F172A 0%, #64748B 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 900; font-size: 45px; 
        letter-spacing: 2px;
    }
    
    /* Animasi Masuk Super Halus */
    @keyframes fadeInUp { from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);} }
    .block-container { animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1); padding-top: 2rem !important; }
    
    /* HYPER-GLASSMORPHISM KARTU (Opasitas Putih Tinggi = Anti Bunglon) */
    .glass-card { 
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(32px) saturate(200%); 
        -webkit-backdrop-filter: blur(32px) saturate(200%);
        border-radius: 32px; 
        border: 1px solid rgba(255, 255, 255, 1); 
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.04), inset 0 2px 0 rgba(255, 255, 255, 1); 
        padding: 40px; 
        text-align: center; 
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); 
    }
    .glass-card:hover { 
        transform: translateY(-4px); 
        background: rgba(255, 255, 255, 0.96);
        box-shadow: 0 25px 50px rgba(37, 99, 235, 0.08), inset 0 2px 0 rgba(255, 255, 255, 1); 
        border-color: #DBEAFE;
    }
    
    /* Kartu Skor Kuis & Badge Lab */
    .score-card { 
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.92) 0%, rgba(255, 255, 255, 0.92) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid #BFDBFE; 
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.06), inset 0 2px 0 rgba(255, 255, 255, 1);
        border-radius: 28px; padding: 35px; text-align: center; 
        transition: 0.4s ease; 
    }
    .score-card:hover { transform: translateY(-5px) scale(1.02); box-shadow: 0 20px 45px rgba(37, 99, 235, 0.12); }

    /* Kartu Misi & Materi Lab Simulasi */
    .lab-badge {
        display: inline-block;
        background: linear-gradient(135deg, #EFF6FF 0%, #E0E7FF 100%);
        color: #1D4ED8 !important;
        font-weight: 800;
        font-size: 12px;
        padding: 6px 16px;
        border-radius: 100px;
        border: 1px solid #BFDBFE;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .mission-step {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        border-radius: 0 16px 16px 0;
        padding: 16px 20px;
        margin-bottom: 12px;
        text-align: left;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
        transition: 0.3s ease;
    }
    .mission-step:hover {
        background: #EFF6FF;
        transform: translateX(4px);
    }
    .formula-box {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #F8FAFC !important;
        border-radius: 20px;
        padding: 20px 25px;
        font-family: 'Outfit', sans-serif;
        font-size: 20px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.15);
        margin: 15px 0;
        border: 1px solid #334155;
    }
    
    /* Buttons: Spektakuler Pill-Shaped Gradient */
    .stButton>button { 
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important; 
        border-radius: 100px;
        border: none; 
        padding: 16px 32px; 
        font-weight: 700; 
        font-size: 16px; 
        width: 100%; 
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3), inset 0 2px 0 rgba(255,255,255,0.2); 
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); 
        letter-spacing: 0.5px;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #1D4ED8 0%, #4338CA 100%) !important; 
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4), inset 0 2px 0 rgba(255,255,255,0.3); 
    }
    .stButton>button:active { transform: translateY(1px); box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3); }
    
    /* Varian Button Glass Kuis */
    .quiz-btn>button { background: rgba(255,255,255,0.95); border: 2px solid #E2E8F0; font-size: 16px; font-weight: 600; padding: 22px; border-radius: 24px; color: #0F172A !important; transition: 0.3s; box-shadow: 0 5px 15px rgba(0,0,0,0.03); }
    .quiz-btn>button:hover { background: #F0FDF4; border-color: #10B981; color: #059669 !important; box-shadow: 0 12px 30px rgba(16, 185, 129, 0.15); }
    
    .btn-red>button { background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3), inset 0 2px 0 rgba(255,255,255,0.2); }
    .btn-red>button:hover { background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%) !important; box-shadow: 0 15px 35px rgba(239, 68, 68, 0.4); }
    
    .btn-green>button { background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important; box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3), inset 0 2px 0 rgba(255,255,255,0.2); }
    .btn-green>button:hover { background: linear-gradient(135deg, #059669 0%, #047857 100%) !important; box-shadow: 0 15px 35px rgba(16, 185, 129, 0.4); }
    
    /* Input Fields (Sangat Bersih, Mewah & Elegan) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, div[data-baseweb="textarea"] > div { 
        background-color: #FFFFFF !important; 
        border: 2px solid #E2E8F0 !important; 
        border-radius: 20px; transition: 0.3s; 
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within, div[data-baseweb="textarea"] > div:focus-within { 
        border-color: #60A5FA !important; 
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.2), inset 0 2px 4px rgba(0,0,0,0.01);
    }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span, textarea { color: #0F172A !important; font-weight: 600; font-size: 15px; }
    
    div[data-testid="stMetricValue"] { color: #2563EB !important; font-size: 42px !important; font-weight: 900 !important; text-shadow: none; letter-spacing: -1px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    /* Tab Styling Minimalist Mewah */
    button[data-baseweb="tab"] { background: transparent !important; color: #64748B !important; font-weight: 700; font-size: 15px; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #2563EB !important; }
    div[data-baseweb="tab-highlight"] { background-color: #2563EB !important; height: 4px; border-radius: 4px; }

    /* FLOATING SIDEBAR (GLASSMORPHISM PANEL CERAH - ANTI BUNGLON) */
    [data-testid="stSidebar"] { 
        background-color: transparent !important; 
        border: none;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(40px) saturate(200%);
        -webkit-backdrop-filter: blur(40px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 36px;
        margin: 1.5rem;
        height: calc(100vh - 3rem) !important;
        box-shadow: 10px 10px 40px rgba(15, 23, 42, 0.08), inset 0 2px 0 rgba(255,255,255,1);
        overflow: hidden;
    }
    [data-testid="stSidebarHeader"] { display: none; }
    
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #60A5FA, #8B5CF6); border-radius: 10px; box-shadow: 0 2px 10px rgba(96, 165, 250, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI MESIN CLOUD (SUPABASE + SAFE FALLBACK)
# ==========================================
if "local_users_fallback" not in st.session_state:
    st.session_state.local_users_fallback = {}

SUPABASE_URL = ""
SUPABASE_KEY = ""
HEADERS = {}

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()
    HEADERS = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
except Exception:
    st.warning("⚠️ Kunci Supabase belum terbaca di Streamlit Secrets. Berjalan dalam Mode Simulasi Lokal Sementara.")

# ==========================================
# 3. FUNGSI DATABASE LENGKAP (ANTI-CRASH & ANTI-LAG ENGINE)
# ==========================================
def db_get_user(username):
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?username=ilike.{username}", headers=HEADERS, timeout=6).json()
            if isinstance(res, list) and len(res) > 0:
                return res[0]
        except Exception:
            pass
    return st.session_state.local_users_fallback.get(username.lower())

def db_create_user(username, hashed_pwd):
    data = {
        "username": username,
        "password": hashed_pwd,
        "avatar_name": "Geni Us",
        "title": "📜 Cendekiawan Muda",
        "points": 0,
        "streak": 1,
        "display_name": username
    }
    st.session_state.local_users_fallback[username.lower()] = data
    if SUPABASE_URL:
        try:
            requests.post(f"{SUPABASE_URL}/rest/v1/users_cloud", headers=HEADERS, json=data, timeout=6)
        except Exception:
            st.toast("Mode Offline Aktif: Akun disimpan sementara di sesi lokal.", icon="⚠️")

def db_update_points(username, new_points):
    if username.lower() in st.session_state.local_users_fallback:
        st.session_state.local_users_fallback[username.lower()]["points"] = new_points
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json={"points": new_points}, timeout=6)
        except Exception:
            pass

def db_update_avatar(username, avatar_name):
    if username.lower() in st.session_state.local_users_fallback:
        st.session_state.local_users_fallback[username.lower()]["avatar_name"] = avatar_name
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json={"avatar_name": avatar_name}, timeout=6)
        except Exception:
            pass

def db_update_title(username, title, cost=0):
    payload = {"title": title}
    current = db_get_user(username)
    if cost > 0 and current:
        payload["points"] = current.get("points", 0) - cost
    if username.lower() in st.session_state.local_users_fallback:
        st.session_state.local_users_fallback[username.lower()].update(payload)
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json=payload, timeout=6)
        except Exception:
            pass

def db_update_profile(username, display_name, custom_avatar=None):
    payload = {"display_name": display_name}
    if custom_avatar is not None:
        payload["custom_avatar"] = custom_avatar
    if username.lower() in st.session_state.local_users_fallback:
        st.session_state.local_users_fallback[username.lower()].update(payload)
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}", headers=HEADERS, json=payload, timeout=6)
        except Exception:
            pass

def db_get_learned_history(username):
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/kuis_history_cloud?username=eq.{username}", headers=HEADERS, timeout=6).json()
            return set([row["id_kuis"] for row in res]) if isinstance(res, list) else set()
        except Exception:
            return set()
    return set()

def db_add_kuis_history(username, id_kuis):
    if SUPABASE_URL:
        try:
            requests.post(f"{SUPABASE_URL}/rest/v1/kuis_history_cloud", headers=HEADERS, json={"username": username, "id_kuis": id_kuis}, timeout=6)
        except Exception:
            pass

@st.cache_data(ttl=60)
def db_get_leaderboard():
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,display_name,points,title&order=points.desc&limit=10", headers=HEADERS, timeout=6).json()
            if isinstance(res, list):
                return res
        except Exception:
            pass
    return []

@st.cache_data(ttl=60)
def db_get_all_users_admin():
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,title,points,streak&order=points.desc", headers=HEADERS, timeout=6).json()
            if isinstance(res, list):
                return res
        except Exception:
            pass
    return []

def db_get_random_opponent(exclude_username):
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?username=neq.{exclude_username}&limit=10", headers=HEADERS, timeout=6).json()
            if isinstance(res, list) and len(res) > 0:
                return random.choice(res)
        except Exception:
            pass
    return None

def db_update_pvp_win(winner, loser, winner_current_pts, loser_current_pts):
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{winner}", headers=HEADERS, json={"points": winner_current_pts + 100}, timeout=6)
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{loser}", headers=HEADERS, json={"points": max(0, loser_current_pts - 20)}, timeout=6)
        except Exception:
            pass

def db_update_pvp_lose(loser, loser_current_pts):
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{loser}", headers=HEADERS, json={"points": max(0, loser_current_pts - 30)}, timeout=6)
        except Exception:
            pass

# --- FUNGSI MULTIPLAYER LOBBY SYSTEM ---
def db_create_quiz_session(code, host, mapel):
    if SUPABASE_URL:
        try:
            data = {"session_code": code, "host_username": host, "mapel": mapel, "status": "waiting"}
            requests.post(f"{SUPABASE_URL}/rest/v1/quiz_sessions", headers=HEADERS, json=data, timeout=6)
        except Exception:
            pass

def db_get_quiz_session(code):
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/quiz_sessions?session_code=eq.{code}", headers=HEADERS, timeout=6).json()
            return res[0] if isinstance(res, list) and len(res) > 0 else None
        except Exception:
            pass
    return None

def db_get_waiting_sessions():
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/quiz_sessions?status=eq.waiting", headers=HEADERS, timeout=6).json()
            return res if isinstance(res, list) else []
        except Exception:
            pass
    return []

def db_update_session_status(code, status):
    if SUPABASE_URL:
        try:
            requests.patch(f"{SUPABASE_URL}/rest/v1/quiz_sessions?session_code=eq.{code}", headers=HEADERS, json={"status": status}, timeout=6)
        except Exception:
            pass

def db_join_session(code, username):
    if SUPABASE_URL:
        try:
            check = requests.get(f"{SUPABASE_URL}/rest/v1/session_players?session_code=eq.{code}&username=eq.{username}", headers=HEADERS, timeout=6).json()
            if isinstance(check, list) and len(check) == 0:
                data = {"session_code": code, "username": username, "score": 0, "status": "joined"}
                requests.post(f"{SUPABASE_URL}/rest/v1/session_players", headers=HEADERS, json=data, timeout=6)
        except Exception:
            pass

def db_get_session_players(code):
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/session_players?session_code=eq.{code}&order=score.desc", headers=HEADERS, timeout=6).json()
            return res if isinstance(res, list) else []
        except Exception:
            pass
    return []

def db_update_player_score(code, username, score):
    if SUPABASE_URL:
        try:
            url = f"{SUPABASE_URL}/rest/v1/session_players?session_code=eq.{code}&username=eq.{username}"
            requests.patch(url, headers=HEADERS, json={"score": score, "status": "finished"}, timeout=6)
        except Exception:
            pass

# --- FUNGSI CUSTOM QUIZ (PABRIK SOAL) ---
def db_save_custom_quiz(title, creator, questions):
    if SUPABASE_URL:
        try:
            data = {"title": title, "creator": creator, "questions": questions}
            requests.post(f"{SUPABASE_URL}/rest/v1/custom_quizzes", headers=HEADERS, json=data, timeout=6)
        except Exception:
            pass

@st.cache_data(ttl=60)
def db_get_all_custom_quizzes():
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/custom_quizzes", headers=HEADERS, timeout=6).json()
            return res if isinstance(res, list) else []
        except Exception:
            pass
    return []

def db_get_custom_quiz_by_title(title):
    if SUPABASE_URL:
        try:
            res = requests.get(f"{SUPABASE_URL}/rest/v1/custom_quizzes?title=eq.{title}", headers=HEADERS, timeout=6).json()
            return res[0] if isinstance(res, list) and len(res) > 0 else None
        except Exception:
            pass
    return None

# ==========================================
# 3B. GENERATOR FILE SIMULASI LOKAL DI FOLDER UPLOADS & KATALOG PHET
# ==========================================
def inisialisasi_file_simulasi_uploads():
    """Membuat file game simulasi interaktif HTML5 secara otomatis di dalam folder uploads/simulasi_interaktif/"""
    folder_sim = os.path.join("uploads", "simulasi_interaktif")
    os.makedirs(folder_sim, exist_ok=True)
    file_target = os.path.join(folder_sim, "lab_fisika_pegas_dan_energi.html")
    
    if not os.path.exists(file_target):
        html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');
  * { box-sizing: border-box; font-family: 'Outfit', sans-serif; }
  body { margin: 0; padding: 20px; background: linear-gradient(135deg, #F0F9FF 0%, #EDE9FE 100%); color: #0F172A; }
  .lab-wrapper { max-width: 960px; margin: 0 auto; background: rgba(255,255,255,0.92); border-radius: 28px; padding: 24px; box-shadow: 0 15px 40px rgba(37,99,235,0.08); border: 1px solid #FFFFFF; }
  .header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 2px solid #F1F5F9; padding-bottom: 12px; }
  .header-bar h2 { margin: 0; font-size: 22px; background: linear-gradient(135deg, #2563EB, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .badge { background: #DBEAFE; color: #1D4ED8; padding: 6px 14px; border-radius: 99px; font-weight: 700; font-size: 12px; }
  .main-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
  canvas { width: 100%; height: 360px; background: #FFFFFF; border-radius: 20px; border: 2px solid #E2E8F0; box-shadow: inset 0 4px 12px rgba(0,0,0,0.03); }
  .controls { display: flex; flex-direction: column; gap: 14px; background: #F8FAFC; padding: 20px; border-radius: 20px; border: 1px solid #E2E8F0; }
  .control-group label { display: flex; justify-content: space-between; font-weight: 700; font-size: 14px; color: #334155; margin-bottom: 6px; }
  input[type=range] { width: 100%; accent-color: #2563EB; cursor: pointer; }
  .telemetry { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
  .metric-box { background: #FFFFFF; padding: 12px; border-radius: 14px; border: 1px solid #E2E8F0; text-align: center; }
  .metric-box span { display: block; font-size: 11px; color: #64748B; font-weight: 700; text-transform: uppercase; }
  .metric-box strong { font-size: 20px; color: #2563EB; font-weight: 800; }
  .btn-action { background: linear-gradient(135deg, #2563EB, #4F46E5); color: white; border: none; padding: 12px; border-radius: 99px; font-weight: 700; cursor: pointer; transition: 0.2s; }
  .btn-action:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37,99,235,0.25); }
</style>
</head>
<body>
<div class="lab-wrapper">
  <div class="header-bar">
    <h2>🔬 Aksara Interactive Physics Engine: Osilasi & Hukum Hooke</h2>
    <span class="badge">HTML5 Local Engine (uploads/)</span>
  </div>
  <div class="main-grid">
    <div>
      <canvas id="simCanvas" width="560" height="360"></canvas>
    </div>
    <div class="controls">
      <div class="control-group">
        <label><span>Konstanta Pegas (k)</span><span id="kVal">200 N/m</span></label>
        <input type="range" id="kSlider" min="50" max="500" step="10" value="200">
      </div>
      <div class="control-group">
        <label><span>Gaya Tarik (F)</span><span id="fVal">60 N</span></label>
        <input type="range" id="fSlider" min="0" max="150" step="5" value="60">
      </div>
      <div class="control-group">
        <label><span>Getaran Osilasi (Amplitudo)</span><span id="oscState">Aktif</span></label>
        <button class="btn-action" onclick="toggleOsc()">⚡ Lepas & Getarkan Pegas!</button>
      </div>
      <div class="telemetry">
        <div class="metric-box">
          <span>Pertambahan (Δx)</span>
          <strong id="dxOut">0.30 m</strong>
        </div>
        <div class="metric-box">
          <span>Energi Potensial (Ep)</span>
          <strong id="epOut">9.00 J</strong>
        </div>
      </div>
      <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:10px 14px; font-size:12px; color:#1E3A8A; font-weight:600;">
        💡 <b>Misi Lab:</b> Atur k = 300 N/m dan F = 90 N. Amati nilai Δx dan Energi Potensial Pegasnya!
      </div>
    </div>
  </div>
</div>
<script>
const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');
const kSlider = document.getElementById('kSlider');
const fSlider = document.getElementById('fSlider');
let oscillating = false;
let t = 0;

function toggleOsc() {
  oscillating = !oscillating;
  document.getElementById('oscState').innerText = oscillating ? "Bergetar" : "Statis";
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const k = parseFloat(kSlider.value);
  const F = parseFloat(fSlider.value);
  const dxStatic = F / k;
  let currentDx = dxStatic;
  if (oscillating) {
    t += 0.08;
    currentDx = dxStatic * Math.cos(Math.sqrt(k / 50) * t) * Math.exp(-0.005 * t);
  } else {
    t = 0;
  }
  const Ep = 0.5 * k * (dxStatic * dxStatic);

  document.getElementById('kVal').innerText = k + " N/m";
  document.getElementById('fVal').innerText = F + " N";
  document.getElementById('dxOut').innerText = dxStatic.toFixed(2) + " m";
  document.getElementById('epOut').innerText = Ep.toFixed(2) + " J";

  // Dinding Penyangga Kiri
  ctx.fillStyle = "#334155";
  ctx.fillRect(30, 80, 16, 180);

  // Garis Titik Setimbang
  const eqX = 180;
  ctx.setLineDash([6, 6]);
  ctx.strokeStyle = "#94A3B8";
  ctx.beginPath();
  ctx.moveTo(eqX, 60);
  ctx.lineTo(eqX, 290);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = "#64748B";
  ctx.font = "600 12px Outfit";
  ctx.fillText("Titik Setimbang (x=0)", eqX - 50, 50);

  // Posisi Ujung Pegas
  const pixelStretch = currentDx * 180;
  const endX = eqX + pixelStretch;

  // Gambar Pegas Zig-Zag
  const coils = 14;
  ctx.beginPath();
  ctx.moveTo(46, 170);
  const step = (endX - 46) / coils;
  for (let i = 1; i < coils; i++) {
    const x = 46 + i * step;
    const y = 170 + (i % 2 === 0 ? -24 : 24);
    ctx.lineTo(x, y);
  }
  ctx.lineTo(endX, 170);
  ctx.lineWidth = Math.max(3, k / 75);
  ctx.strokeStyle = "#2563EB";
  ctx.stroke();

  // Beban Balok
  ctx.fillStyle = "#4F46E5";
  ctx.beginPath();
  ctx.roundRect(endX, 135, 70, 70, 14);
  ctx.fill();
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "700 14px Outfit";
  ctx.fillText(F + " N", endX + 18, 175);

  // Bar Energi Potensial di Bawah
  ctx.fillStyle = "#E2E8F0";
  ctx.beginPath();
  ctx.roundRect(46, 315, 460, 20, 10);
  ctx.fill();
  const barWidth = Math.min(460, (Ep / 60) * 460);
  ctx.fillStyle = "#10B981";
  ctx.beginPath();
  ctx.roundRect(46, 315, barWidth, 20, 10);
  ctx.fill();
  ctx.fillStyle = "#0F172A";
  ctx.font = "700 12px Outfit";
  ctx.fillText("Bar Energi Potensial Elastis (Ep): " + Ep.toFixed(1) + " Joule", 50, 308);

  requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>"""
        with open(file_target, "w", encoding="utf-8") as f:
            f.write(html_content)

inisialisasi_file_simulasi_uploads()

# KATALOG LENGKAP SIMULASI PHET COLORADO & MATERI PENDAMPING
KATALOG_SIMULASI_LAB = {
    "🔩 Fisika: Hukum Hooke & Elastisitas Pegas": {
        "kategori": "Fisika Kelas XI",
        "phet_url": "https://phet.colorado.edu/sims/html/hookes-law/latest/hookes-law_all.html?locale=in",
        "inti_10_detik": "Semakin besar gaya tarik (F) yang diberikan pada pegas, semakin panjang pertambahan panjangnya (Δx) secara linier—selama belum melewati batas elastisitasnya. Energi yang tersimpan di dalam pegas disebut Energi Potensial Elastis.",
        "rumus_emas": "F = k · Δx   &   Ep = ½ · k · (Δx)²",
        "jembatan_keledai": "F-K-X (Fokus Kuat X-tra): Gaya sebanding dengan Konstanta dikali Pertambahan Panjang.",
        "variabel": [
            {"Simbol & Nama": "F (Gaya Pegas)", "Satuan": "Newton (N)", "Peran & Efek Visual": "Tarikan/dorongan tangan atau beban. Jika F dinaikkan 2x lipat, Δx ikut naik 2x lipat."},
            {"Simbol & Nama": "k (Konstanta Pegas)", "Satuan": "N/m", "Peran & Efek Visual": "Tingkat kekakuan pegas. Semakin besar k, lilitan kawat makin tebal dan pegas makin sulit ditarik."},
            {"Simbol & Nama": "Δx (Pertambahan Panjang)", "Satuan": "Meter (m)", "Peran & Efek Visual": "Selisih panjang akhir dikurangi panjang mula-mula dari garis titik setimbang."},
            {"Simbol & Nama": "Ep (Energi Potensial)", "Satuan": "Joule (J)", "Peran & Efek Visual": "Luas daerah segitiga di bawah grafik F terhadap Δx. Jika Δx naik 2x, Ep melonjak 4x lipat!"}
        ],
        "misi": [
            "Misi 1 (Eksplorasi Kekakuan): Buka tab 'Pengantar' di simulasi PhET. Atur Konstanta Pegas (k) ke 200 N/m, lalu berikan Gaya Tarik (F) sebesar 100 N. Catat berapa meter nilai perpindahan (Δx) yang muncul!",
            "Misi 2 (Susunan Seri vs Paralel): Pindah ke tab 'Sistem'. Bandingkan 2 pegas yang disusun Paralel (berdampingan) dengan 2 pegas Seri (memanjang). Manakah yang lebih kaku dan menghasilkan Δx lebih kecil?",
            "Misi 3 (Lonjakan Energi Kuadratik): Buka tab 'Energi'. Geser perpindahan (Δx) dari 0,2 m menjadi 0,4 m (naik 2 kali lipat). Amati grafik batang Energi Potensial: apakah tingginya naik 2 kali atau 4 kali lipat?"
        ],
        "kuis_lab": {
            "soal": "Berdasarkan eksperimen di atas, sebuah pegas memiliki konstanta k = 400 N/m. Jika pegas ditarik dengan gaya F = 80 N, berapakah pertambahan panjang (Δx) dan Energi Potensial Elastis (Ep) yang tersimpan?",
            "opsi": [
                "Δx = 0,2 m dan Ep = 8 Joule",
                "Δx = 0,5 m dan Ep = 16 Joule",
                "Δx = 0,2 m dan Ep = 16 Joule",
                "Δx = 0,4 m dan Ep = 32 Joule"
            ],
            "jawaban": "Δx = 0,2 m dan Ep = 8 Joule",
            "pembahasan_konsep": "Langkah 1: Cari pertambahan panjang dengan Hukum Hooke: Δx = F / k = 80 / 400 = 0,2 meter. Langkah 2: Hitung Energi Potensial Pegas: Ep = ½ · k · (Δx)² = ½ · 400 · (0,2)² = 200 · 0,04 = 8 Joule.",
            "trik_mentor": "Trik Kilat Tanpa Kuadrat: Karena F = k·Δx, rumus Ep bisa disingkat menjadi Ep = ½ · F · Δx! Langsung kalikan saja: ½ × 80 N × 0,2 m = 8 Joule. Selesai dalam 3 detik!"
        }
    },
    "🌊 Fisika: Fluida Statis & Tekanan Hidrostatis": {
        "kategori": "Fisika Kelas XI",
        "phet_url": "https://phet.colorado.edu/sims/html/under-pressure/latest/under-pressure_all.html?locale=in",
        "inti_10_detik": "Tekanan di dalam zat cair (Hidrostatis) hanya bergantung pada kedalaman (h), massa jenis cairan (ρ), dan gravitasi (g)—sama sekali tidak peduli bentuk wadahnya (Paradoks Hidrostatis).",
        "rumus_emas": "Ph = ρ · g · h   &   P_total = P₀ + (ρ · g · h)",
        "jembatan_keledai": "RO-G-H (Rogo Dalam Hati): Massa Jenis (ρ) × Gravitasi (g) × Kedalaman dari permukaan (h).",
        "variabel": [
            {"Simbol & Nama": "Ph (Tekanan Hidrostatis)", "Satuan": "Pascal (Pa)", "Peran & Efek Visual": "Tekanan murni akibat berat zat cair di atas titik ukur."},
            {"Simbol & Nama": "ρ (Massa Jenis Fluida)", "Satuan": "kg/m³", "Peran & Efek Visual": "Kerapatan cairan (Bensin = 700, Air = 1000, Madu = 1420 kg/m³). Makin pekat, tekanan makin besar."},
            {"Simbol & Nama": "h (Kedalaman Titik)", "Satuan": "Meter (m)", "Peran & Efek Visual": "Diukur dari PERMUKAAN ATAS cairan ke bawah, bukan dari dasar kolam!"},
            {"Simbol & Nama": "P₀ (Tekanan Atmosfer)", "Satuan": "101.325 Pa", "Peran & Efek Visual": "Tekanan udara luar yang menekan permukaan cairan terbuka."}
        ],
        "misi": [
            "Misi 1 (Uji Kedalaman): Tarik alat ukur Barometer (bulatan ungu) ke kedalaman 1 meter, 2 meter, dan 3 meter di bawah air. Perhatikan bagaimana angka tekanan terus bertambah seiring bertambahnya kedalaman!",
            "Misi 2 (Paradoks Bejana Berhubungan): Pilih wadah ke-3 (bentuk corong miring dan pipa sempit). Letakkan dua alat ukur tekanan pada kedalaman 2 meter di pipa lebar dan pipa sempit. Apakah tekanannya sama persis?",
            "Misi 3 (Eksperimen Massa Jenis Madu vs Bensin): Ganti jenis cairan (Fluid Density) dari Air (Water) menjadi Madu (Honey). Amati kenaikan drastis pada jarum barometer!"
        ],
        "kuis_lab": {
            "soal": "Saat kamu menyelam pada kedalaman 3 meter di dalam kolam berisi cairan dengan massa jenis ρ = 1.000 kg/m³ (g = 10 m/s²) dan tekanan atmosfer dimatikan (Off / P₀ = 0), berapakah tekanan hidrostatis yang terbaca pada sensor?",
            "opsi": [
                "30.000 Pa (30 kPa)",
                "10.000 Pa (10 kPa)",
                "131.325 Pa (131,3 kPa)",
                "3.000 Pa (3 kPa)"
            ],
            "jawaban": "30.000 Pa (30 kPa)",
            "pembahasan_konsep": "Gunakan rumus tekanan hidrostatis murni (karena atmosfer Off / P₀ = 0): Ph = ρ · g · h = 1.000 kg/m³ × 10 m/s² × 3 m = 30.000 Pascal atau 30 kPa.",
            "trik_mentor": "Di dalam air murni (ρ = 1.000, g = 10), setiap turun 1 meter ke bawah, tekanan bertambah tepat 10 kPa! Jadi kalau turun 3 meter, langsung 3 × 10 kPa = 30 kPa!"
        }
    },
    "🎯 Fisika: Gerak Parabola (Projectile Motion)": {
        "kategori": "Fisika Kelas XI",
        "phet_url": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html?locale=in",
        "inti_10_detik": "Gerak parabola adalah perpaduan dua gerak sekaligus: sumbu mendatar (X) bergerak lurus beraturan (kecepatan tetap), sedangkan sumbu vertikal (Y) diperlambat oleh gravitasi bumi hingga berhenti sesaat di titik puncak.",
        "rumus_emas": "X_maks = (v₀² · sin 2θ) / g   &   Y_maks = (v₀² · sin²θ) / (2g)",
        "jembatan_keledai": "Sudut Emas 45°: Tembakan meriam selalu mencapai jarak terjauh pada sudut elevasi 45 derajat!",
        "variabel": [
            {"Simbol & Nama": "v₀ (Kecepatan Awal)", "Satuan": "m/s", "Peran & Efek Visual": "Kekuatan lontaran meriam. Menaikkan v₀ memperbesar jarak tempuh secara kuadratik."},
            {"Simbol & Nama": "θ (Sudut Elevasi)", "Satuan": "Derajat (°)", "Peran & Efek Visual": "Kemiringan moncong meriam. Sudut komplemen (misal 30° dan 60°) menghasilkan jarak jatuh yang sama!"},
            {"Simbol & Nama": "vy (Kecepatan Vertikal)", "Satuan": "m/s", "Peran & Efek Visual": "Bernilai NOL tepat di titik tertinggi lintasan parabola."}
        ],
        "misi": [
            "Misi 1 (Bukti Sudut Emas 45°): Arahkan meriam pada sudut 30°, 45°, dan 60° dengan kecepatan awal tetap (18 m/s), lalu tembakkan! Buktikan bahwa sudut 45° mendarat paling jauh!",
            "Misi 2 (Pasangan Sudut Kembar): Bandingkan titik jatuh peluru pada sudut 30° dan 60°. Mengapa keduanya jatuh di titik sasaran yang sama persis?",
            "Misi 3 (Massa Benda Tanpa Hambatan Udara): Matikan centang 'Hambatan Udara' (Air Resistance). Ganti peluru meriam menjadi Mobil atau Piano. Tembakkan! Apakah massa benda memengaruhi jarak jatuh di ruang hampa?"
        ],
        "kuis_lab": {
            "soal": "Jika hambatan udara diabaikan, sebuah meriam menembakkan bola besi 10 kg dan labu 5 kg dengan kecepatan awal dan sudut elevasi yang sama persis. Bagaimana perbandingan jarak jatuh kedua benda tersebut?",
            "opsi": [
                "Keduanya mendarat di titik jarak yang sama persis",
                "Bola besi jatuh lebih dekat karena lebih berat",
                "Labu terbang dua kali lebih jauh karena lebih ringan",
                "Bola besi mencapai titik puncak lebih tinggi"
            ],
            "jawaban": "Keduanya mendarat di titik jarak yang sama persis",
            "pembahasan_konsep": "Dalam rumus gerak parabola (X_maks = v₀² sin 2θ / g), variabel massa (m) sama sekali tidak ada! Artinya, tanpa gesekan udara, percepatan gravitasi bekerja sama persis pada semua benda berapa pun massanya.",
            "trik_mentor": "Ingat eksperimen Galileo: Tanpa udara, bulu ayam dan bola bowling jatuh berbarengan. Di soal gerak parabola bebas hambatan udara, abaikan angka kilogram/massa bendaเพราะ itu hanya pengecoh!"
        }
    },
    "⚗️ Kimia: Kesetimbangan Reaksi Reversibel (Le Chatelier)": {
        "kategori": "Kimia Kelas XI",
        "phet_url": "https://phet.colorado.edu/sims/html/reversible-reactions/latest/reversible-reactions_all.html?locale=in",
        "inti_10_detik": "Kesetimbangan kimia bersifat dinamis: reaksi maju dan balik terus berlangsung dengan laju yang sama. Jika diganggu (suhu/konsentrasi diubah), sistem otomatis bergeser ke arah yang melawan gangguan tersebut.",
        "rumus_emas": "Kc = [Produk] dipangkatkan koefisien / [Reaktan] dipangkatkan koefisien",
        "jembatan_keledai": "Ta-Ka / Ku-Ki (Tambah Lari ke Kanan/Lawan, Kurang Tarik ke Kiri/Diri): Suhu Naik ➔ Lari ke Endoterm!",
        "variabel": [
            {"Simbol & Nama": "A ⇌ B (Reaktan & Produk)", "Satuan": "Molekul / Molar", "Peran & Efek Visual": "Partikel di ruang kiri (A) dan ruang kanan (B) yang melompati bukit energi aktivasi."},
            {"Simbol & Nama": "T (Suhu Sistem)", "Satuan": "Kelvin (K)", "Peran & Efek Visual": "Memperbesar energi kinetik partikel sehingga lebih mudah melompati penghalang energi."},
            {"Simbol & Nama": "ΔH (Entalpi Reaksi)", "Satuan": "kJ/mol", "Peran & Efek Visual": "Selisih tinggi lantai reaktan A dan produk B pada diagram potensial."}
        ],
        "misi": [
            "Misi 1 (Mencapai Kesetimbangan Dinamis): Masukkan 50 molekul A di ruang kiri. Perhatikan partikel melompat ke ruang B hingga jumlah A dan B menjadi konstan namun partikel masih terus bolak-balik!",
            "Misi 2 (Gangguan Suhu / Asas Le Chatelier): Naikkan tinggi lantai B sehingga lebih tinggi dari A (reaksi Endoterm ke kanan). Panaskan wadah (Add Heat)! Amati apakah molekul lebih banyak berkumpul di B!",
            "Misi 3 (Gangguan Konsentrasi): Tambahkan 30 molekul A lagi ke ruang kiri. Lihat bagaimana sistem menggeser molekul ke kanan untuk menyeimbangkan diri kembali!"
        ],
        "kuis_lab": {
            "soal": "Pada reaksi kesetimbangan eksoterm: N₂(g) + 3H₂(g) ⇌ 2NH₃(g) (ΔH = -92 kJ), apa yang harus dilakukan insinyur pabrik agar produksi gas amonia (NH₃) di sebelah kanan meningkat maksimal?",
            "opsi": [
                "Menurunkan suhu dan menaikkan tekanan (memperkecil volume)",
                "Menaikkan suhu setinggi mungkin dan menurunkan tekanan",
                "Mengurangi konsentrasi gas N₂ dan H₂ dari wadah",
                "Menambahkan katalis agar nilai Kc bertambah besar"
            ],
            "jawaban": "Menurunkan suhu dan menaikkan tekanan (memperkecil volume)",
            "pembahasan_konsep": "Karena reaksi ke kanan bersifat Eksoterm (ΔH negatif), menurunkan suhu akan menggeser kesetimbangan ke arah Eksoterm (kanan). Selain itu, jumlah koefisien gas di kanan (2) lebih kecil daripada di kiri (1+3 = 4), sehingga menaikkan tekanan akan menggeser kesetimbangan ke arah koefisien kecil (kanan/NH₃).",
            "trik_mentor": "Hafalan Cepat Proses Haber-Bosch: Amonia suka DINGIN dan SEMPIT (Suhu diturunkan ke arah eksoterm, Volume diperkecil/Tekanan dinaikkan ke koefisien kecil)!"
        }
    },
    "🧪 Kimia: Skala pH Larutan Asam & Basa": {
        "kategori": "Kimia Kelas XI",
        "phet_url": "https://phet.colorado.edu/sims/html/ph-scale/latest/ph-scale_all.html?locale=in",
        "inti_10_detik": "Skala pH (0 hingga 14) mengukur derajat keasaman secara logaritmik: setiap perubahan 1 angka pH berarti konsentrasi ion H⁺ berubah 10 kali lipat! pH di bawah 7 bersifat Asam, 7 Netral, dan di atas 7 Basa.",
        "rumus_emas": "pH = -log [H⁺]   &   pH + pOH = 14",
        "jembatan_keledai": "Pengenceran 10x = Geser 1 Angka menuju pH 7 (Netral)!",
        "variabel": [
            {"Simbol & Nama": "[H₃O⁺] / [H⁺]", "Satuan": "Molar (mol/L)", "Peran & Efek Visual": "Ion pembawa sifat asam (warna merah). Makin banyak H⁺, nilai pH makin kecil (mendekati 0)."},
            {"Simbol & Nama": "[OH⁻]", "Satuan": "Molar (mol/L)", "Peran & Efek Visual": "Ion pembawa sifat basa (warna biru). Makin banyak OH⁻, nilai pH makin besar (mendekati 14)."},
            {"Simbol & Nama": "V (Volume Air Pengencer)", "Satuan": "Liter (L)", "Peran & Efek Visual": "Menambahkan air murni mengencerkan larutan sehingga pH asam naik mendekati 7, dan pH basa turun mendekati 7."}
        ],
        "misi": [
            "Misi 1 (Klasifikasi Cairan Harian): Pilih cairan Asam Baterai (Battery Acid), Kopi, Air Murni, dan Sabun Cuci Tangan. Tarik sensor pH hijau ke dalam gelas dan urutkan dari paling asam ke paling basa!",
            "Misi 2 (Efek Logaritmik Pengenceran 10x): Buka tab 'Micro'. Tuangkan 0,10 L Asam Baterai (pH = 1,00), lalu tambahkan air dari keran hingga volume total menjadi 1,00 L (diencerkan 10 kali). Berapakah nilai pH barunya?",
            "Misi 3 (Rasio Ion H₃O⁺ vs OH⁻): Nyalakan centang 'H₃O⁺/OH⁻ ratio'. Amati perubahan jumlah titik merah dan titik biru saat larutan diubah dari asam ke basa!"
        ],
        "kuis_lab": {
            "soal": "Sebuah larutan asam kuat memiliki pH = 2. Jika larutan tersebut diencerkan dengan air murni hingga volumenya menjadi 100 kali lipat volume semula, berapakah pH larutan setelah diencerkan?",
            "opsi": [
                "pH = 4",
                "pH = 200",
                "pH = 1",
                "pH = 6"
            ],
            "jawaban": "pH = 4",
            "pembahasan_konsep": "Saat pH = 2, konsentrasi [H⁺] awal adalah 10⁻² M. Ketika diencerkan 100 kali (10² kali), konsentrasi [H⁺] turun menjadi 10⁻² / 10² = 10⁻⁴ M. Maka pH baru = -log(10⁻⁴) = 4.",
            "trik_mentor": "Trik Logaritma Nol: Hitung saja jumlah angka nol pada pengencerannya! Diencerkan 10 kali (satu nol) ➔ pH asam naik +1. Diencerkan 100 kali (dua nol) ➔ pH asam naik +2 (dari 2 menjadi 4)!"
        }
    }
}

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
if "lab_claimed" not in st.session_state: st.session_state.lab_claimed = set()

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
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;} [data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

def tampilkan_avatar(keyword):
    st.markdown(f"<div style='text-align:center; font-size:80px; filter: drop-shadow(0 15px 25px rgba(37,99,235,0.2)); animation: fadeInUp 1s ease;'>{'🎓' if keyword=='genius' else '📚'}</div>", unsafe_allow_html=True)

# ==========================================
# 5. PORTAL LOGIN / REGISTER (GERBANG AKADEMI)
# ==========================================
if not st.session_state.logged_in:
    st.write("<br><br>", unsafe_allow_html=True)
    
    logo_path = None
    if os.path.exists("logo.jpg"): logo_path = "logo.jpg"
    elif os.path.exists("logo.png"): logo_path = "logo.png"
    
    if logo_path:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.image(logo_path, width=110, output_format="auto")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<style>img { border-radius: 30px; box-shadow: 0 15px 40px rgba(0,0,0,0.06); border: 1px solid #E2E8F0; padding:8px; background:#FFFFFF; }</style>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; font-size:75px; font-weight:900; margin-bottom: 0; letter-spacing:-2px;'><span class='gradient-text'>AKSARA</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748B; margin-bottom:50px; font-size:16px; letter-spacing:6px; font-weight:700;'>INSTITUT EDUKASI INTERAKTIF</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.2, 1])
    with col_form:
        st.markdown("<div class='glass-card' style='padding:50px 40px;'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 GERBANG MASUK", "📝 REGISTRASI"])
        
        with tab_log:
            st.write("<br>", unsafe_allow_html=True)
            l_user = st.text_input("Nama Cendekiawan:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("Masuki Akademi"):
                if l_user and l_pass:
                    user_record = db_get_user(l_user)
                    if user_record and user_record.get("password") == hash_password(l_pass):
                        st.session_state.username = user_record["username"] 
                        st.session_state.logged_in = True; st.rerun()
                    else: st.error("Kredensial tidak dikenali institut!")
                else: st.warning("Formulir belum lengkap!")
                
        with tab_reg:
            st.write("<br>", unsafe_allow_html=True)
            r_user = st.text_input("Nama Panggilan (Maks 15 Karakter):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Sandi Keamanan:", type="password", key="r_pwd").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("Daftarkan Nama Saya"):
                if r_user and r_pass:
                    if db_get_user(r_user): st.error("Nama ini sudah terdaftar dalam arsip akademi!")
                    else:
                        db_create_user(r_user, hash_password(r_pass))
                        st.success("Pendaftaran Berhasil! Silakan masuk melalui Gerbang Masuk.")
                else: st.warning("Formulir belum lengkap!")
        st.markdown("</div>", unsafe_allow_html=True)
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
    st.markdown("""
    <style>
    /* Radio Menu Navigasi (Pill-Shaped Hover Effect Mewah) */
    div[role="radiogroup"] > label {
        background: transparent !important;
        padding: 13px 22px;
        border-radius: 100px;
        margin-bottom: 6px;
        border: 1px solid transparent;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
    }

    /* Warna Teks Default Sidebar - Sangat Kontras */
    div[role="radiogroup"] > label p, 
    div[role="radiogroup"] > label div {
        color: #334155 !important; 
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 0.3px;
    }

    div[role="radiogroup"] > label:hover {
        background: #EFF6FF !important;
        border: 1px solid #BFDBFE;
        transform: translateX(8px);
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.05);
    }
    
    div[role="radiogroup"] > label:hover p,
    div[role="radiogroup"] > label:hover div {
        color: #2563EB !important;
    }
    
    /* Tombol Logout Minimalis Pill */
    .stButton > button {
        border-radius: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    # 2. AVATAR & PROFIL PANEL
    if custom_avatar_db:
        st.markdown(f"""
        <div style='text-align:center;'>
            <img src='{custom_avatar_db}' style='width:110px; height:110px; border-radius:50%; object-fit:cover; border:4px solid #FFFFFF; padding:2px; box-shadow: 0 15px 35px rgba(15,23,42,0.1), inset 0 2px 4px rgba(0,0,0,0.05); margin-bottom:12px; transition: 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);' onmouseover='this.style.transform="scale(1.08) translateY(-5px)"; this.style.boxShadow="0 25px 45px rgba(37,99,235,0.15)"' onmouseout='this.style.transform="scale(1) translateY(0)"'>
        </div>
        """, unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<h2 style='text-align:center; margin-top:8px; margin-bottom:4px; font-weight:800; font-size:21px; color:#0F172A;'>{display_name_db}</h2>", unsafe_allow_html=True)
    
    # Badge Judul & Tingkatan
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='background:#F1F5F9; color:#475569; padding:5px 16px; border-radius:100px; font-weight:700; font-size:11px; letter-spacing:0.5px; border:1px solid #E2E8F0;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:22px;'><span style='color:{tier_color}; background:#FFFFFF; padding:5px 16px; border-radius:100px; font-weight:800; border:1px solid {tier_color}55; font-size:11px; letter-spacing:0.5px; box-shadow: 0 4px 15px {tier_color}22;'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    # 3. LEVEL PROGRESS BAR
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: #E2E8F0; border-radius: 100px; height: 10px; margin: 12px 0; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);'>
            <div style='background: linear-gradient(90deg, #60A5FA, #8B5CF6); width: {prog}%; height: 100%; border-radius: 100px; box-shadow: 0 0 10px rgba(139,92,246,0.5);'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:800; color:#475569; font-size:13px;'>
            <span>Lvl {user_level}</span><span style='color:#6366F1;'>✨ {points_db} Pts</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:none; height:1px; background: #E2E8F0; margin: 22px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:11px; font-weight:800; color:#64748B; letter-spacing:3px; margin-bottom:12px;'>MENU UTAMA</p>", unsafe_allow_html=True)
    
    # 4. RADIO MENU (Dengan tambahan Lab Simulasi & Game PhET)
    menu = st.radio("NAVIGASI INSTITUT", [
        "🏠 Dashboard Utama", 
        "📢 Mading Pemberitahuan", 
        "🧪 Lab Simulasi & Game (PhET)",
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ], label_visibility="collapsed", key="navigasi_utama")
    
    st.markdown("<hr style='border:none; height:1px; background: #E2E8F0; margin: 22px 0;'>", unsafe_allow_html=True)
    
    # 5. TOMBOL LOGOUT
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("Keluar Aplikasi"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if menu == "🏠 Dashboard Utama":
    st.markdown(f"<h1 style='font-size:46px; margin-bottom:5px; font-weight:900; letter-spacing:-1.5px;'>Welcome back, <span class='gradient-text'>{display_name_db}</span></h1>", unsafe_allow_html=True)
    st.caption("Akses semua catatan akademi dan pantau perkembangan belajarmu hari ini.")
    st.write("<br>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='padding:35px; text-align:center; background: linear-gradient(135deg, rgba(239,246,255,0.9), rgba(255,255,255,0.9)); border-color:rgba(191,219,254,0.8);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#2563EB; margin-top:0; font-size:24px; font-weight:800; letter-spacing:-0.5px;'>✨ Daily Honor Roll</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Buka Scroll Keberuntungan"):
            bonus = random.choice([20, 50, 100, 150, 200])
            db_update_points(player, points_db + bonus)
            st.session_state.gacha_claimed = True
            st.session_state.sfx = "benar" 
            st.balloons()
            st.success(f"DIBERKAHI! Kamu mendapat +{bonus} Poin Akademik!")
            time.sleep(1)
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='glass-card'><div style='font-size:45px; margin-bottom:15px; filter:drop-shadow(0 8px 15px rgba(0,0,0,0.05));'>⏳</div><h2 style='margin:0; font-size:40px; font-weight:900; color:#0F172A;'>{streak_db}</h2><p style='color:#475569; font-weight:700; letter-spacing:1.5px; margin:0; font-size:13px; margin-top:5px;'>HARI AKTIF</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='glass-card'><div style='font-size:45px; margin-bottom:15px; filter:drop-shadow(0 8px 15px rgba(0,0,0,0.05));'>📚</div><h2 style='margin:0; font-size:40px; font-weight:900; color:#0F172A;'>{len(learned_db)}</h2><p style='color:#475569; font-weight:700; letter-spacing:1.5px; margin:0; font-size:13px; margin-top:5px;'>MODUL SELESAI</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='glass-card' style='border-bottom: 5px solid {tier_color}; box-shadow: 0 20px 50px {tier_color}22, inset 0 2px 0 rgba(255,255,255,1);'><div style='font-size:45px; margin-bottom:15px; filter:drop-shadow(0 8px 15px {tier_color}66);'>🏛️</div><h2 style='color:{tier_color}; margin:0; font-size:40px; font-weight:900;'>Lvl {user_level}</h2><p style='color:#475569; font-weight:700; letter-spacing:1.5px; margin:0; font-size:13px; margin-top:5px;'>STATUS AKADEMI</p></div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:26px; margin-bottom:25px; font-weight:900;'><span class='gradient-text'>Hall of Scholars</span> (Top 10)</h3>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    for i, row in enumerate(ranking_data):
        if i == 0: medali, bg_color, bdr_color = "👑", "linear-gradient(90deg, #FEF3C7, #FFFBEB)", "#FCD34D"
        elif i == 1: medali, bg_color, bdr_color = "🥈", "linear-gradient(90deg, #F1F5F9, #FFFFFF)", "#CBD5E1"
        elif i == 2: medali, bg_color, bdr_color = "🥉", "linear-gradient(90deg, #FFEDD5, #FFF7ED)", "#FDBA74"
        else: medali, bg_color, bdr_color = f"#{i+1}", "rgba(255,255,255,0.8)", "#E2E8F0"
        
        d_name = row.get("display_name")
        if not d_name: d_name = row.get("username", "Anonim")
        
        st.markdown(f"""
        <div style='background: {bg_color}; backdrop-filter: blur(15px); border: 1px solid {bdr_color}; border-radius: 24px; padding: 22px 35px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); box-shadow: 0 10px 30px rgba(0,0,0,0.02), inset 0 2px 0 rgba(255,255,255,1);' onmouseover='this.style.transform=\"translateY(-3px) scale(1.01)\"; this.style.boxShadow=\"0 20px 40px rgba(37,99,235,0.08), inset 0 2px 0 rgba(255,255,255,1)\"' onmouseout='this.style.transform=\"translateY(0) scale(1)\"; this.style.boxShadow=\"0 10px 30px rgba(0,0,0,0.02), inset 0 2px 0 rgba(255,255,255,1)\"'>
            <h3 style='margin:0; font-size:18px; font-weight:800; color:#1E293B;'>{medali} <span style='color:#0F172A; margin-left:15px;'>{d_name}</span> <span style='font-size:11px; font-weight:800; color:#4F46E5; background:#E0E7FF; padding:6px 14px; border-radius:100px; margin-left:15px; border:1px solid #C7D2FE; letter-spacing:0.5px;'>{row.get("title", "")}</span></h3>
            <h3 style='margin:0; color:#2563EB; font-weight:900; font-size:20px;'>✨ {row.get("points", 0)}</h3>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# HALAMAN 2: MADING PEMBERITAHUAN
# ==============================================================================
st.markdown("""
<style>
.mading-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(24px) saturate(200%);
    -webkit-backdrop-filter: blur(24px) saturate(200%);
    border-radius: 32px;
    padding: 35px;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.04), inset 0 2px 0 rgba(255,255,255,1);
    border: 1px solid rgba(255, 255, 255, 1);
    margin-bottom: 40px;
    transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.mading-container:hover {
    transform: translateY(-6px);
    background: rgba(255, 255, 255, 0.95);
    border-color: #BFDBFE;
    box-shadow: 0 30px 60px rgba(37, 99, 235, 0.08), inset 0 2px 0 rgba(255,255,255,1);
}
.mading-tag {
    background: #EFF6FF;
    color: #2563EB;
    padding: 6px 18px;
    border-radius: 100px;
    border: 1px solid #BFDBFE;
    font-size: 11px;
    font-weight: 800;
    display: inline-block;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.mading-title-text {
    color: #0F172A;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 10px;
    line-height: 1.4;
    letter-spacing: -0.5px;
}
.mading-meta {
    color: #64748B;
    font-size: 12px;
    margin-bottom: 24px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.mading-body {
    color: #334155;
    font-size: 15px;
    line-height: 1.8;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

if menu == "📢 Mading Pemberitahuan":
    st.markdown("<h1 style='font-size:42px; margin-bottom: 5px; font-weight:900;'>Bulletin Board</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color:#475569; font-weight:500;'>Informasi kreatif, pengumuman penting, dan galeri poster institut.</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
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
                    st.markdown(f"""
                    <div class="mading-container">
                        <span class="mading-tag">{item['kategori']}</span>
                        <div class="mading-title-text">{item['judul']}</div>
                        <div class="mading-meta">RELEASED: {item['tanggal']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if item['gambar']:
                        try:
                            st.markdown(f"<div style='margin-top:-25px; padding:0 30px;'><img src='{item['gambar']}' style='width:100%; border-radius:20px; border:4px solid #FFFFFF; box-shadow:0 15px 35px rgba(0,0,0,0.08);'></div>", unsafe_allow_html=True)
                        except:
                            st.caption("⚠️ Gagal memuat berkas gambar poster.")
                            
                    st.markdown(f"""
                    <div style='background: transparent; padding: 25px 35px 35px 35px;'>
                        <p class="mading-body">{item['deskripsi']}</p>
                    </div>
                    <div style='margin-bottom: 10px;'></div>
                    """, unsafe_allow_html=True)
                    
    with tab_tambah:
        st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:24px; margin-bottom:25px; font-weight:800;'>Buat Poster Mading Baru</h3>", unsafe_allow_html=True)
        
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
                    
            st.write("<br>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# HALAMAN BARU: LAB SIMULASI INTERAKTIF & GAME EDUKASI (PHET COLORADO + UPLOADS)
# ==============================================================================
elif menu == "🧪 Lab Simulasi & Game (PhET)":
    st.markdown("<h1 style='font-size:44px; margin-bottom:5px;'><span class='gradient-text'>LABORATORIUM VIRTUAL & GAME EDUKASI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#475569;'>Eksperimen sains interaktif berbasis PhET Colorado & HTML5 Engine lengkap dengan misi penyelidikan dan tantangan berhadiah poin.</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)

    tab_phet, tab_lokal, tab_custom_url = st.tabs([
        "🌐 Katalog Simulasi PhET & Materi Lengkap",
        "🎮 Game Simulasi Lokal (Folder uploads/)",
        "🔗 Muat Tautan PhET / Game Baru"
    ])

    with tab_phet:
        col_pilih, col_tinggi = st.columns([3, 1])
        with col_pilih:
            pilihan_sim = st.selectbox(
                "🔬 Pilih Modul Eksperimen Interaktif:",
                list(KATALOG_SIMULASI_LAB.keys())
            )
        with col_tinggi:
            tinggi_layar = st.slider("📏 Tinggi Layar Lab (px):", min_value=480, max_value=850, value=600, step=20)

        data_sim = KATALOG_SIMULASI_LAB[pilihan_sim]

        # 1. PANEL INTI 10 DETIK & RUMUS EMAS (DI ATAS KANVAS)
        st.markdown(f"""
        <div class='glass-card' style='text-align:left; padding:30px; margin-bottom:25px;'>
            <span class='lab-badge'>{data_sim['kategori']} &nbsp;|&nbsp; Interactive PhET Simulation</span>
            <h2 style='margin-top:0; margin-bottom:10px; font-size:28px;'>{pilihan_sim}</h2>
            <p style='font-size:16px; line-height:1.7; color:#1E293B; margin-bottom:15px;'>
                <b>⚡ Inti 10 Detik:</b> {data_sim['inti_10_detik']}
            </p>
            <div class='formula-box'>📐 Rumus Emas: &nbsp; {data_sim['rumus_emas']}</div>
            <p style='text-align:center; font-size:14px; color:#2563EB; font-weight:700; margin:0;'>
                💡 Jembatan Keledai: "{data_sim['jembatan_keledai']}"
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 2. KANVAS INTERAKTIF PHET COLORADO
        st.markdown("<div class='glass-card' style='padding:18px; margin-bottom:25px;'>", unsafe_allow_html=True)
        components.iframe(data_sim["phet_url"], height=tinggi_layar, scrolling=True)
        st.caption("💡 Tips: Klik tombol layar penuh atau geser slider di dalam simulasi untuk melihat perubahan grafik dan vektor secara langsung.")
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. BEDAH VARIABEL & MISI EKSPERIMEN TERPANDU (LKPD DIGITAL)
        c_var, c_misi = st.columns([1.15, 1])
        with c_var:
            st.markdown("<div class='glass-card' style='text-align:left; padding:30px; height:100%;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size:22px; margin-top:0;'>📊 Bedah Variabel & Kausalitas</h3>", unsafe_allow_html=True)
            df_var = pd.DataFrame(data_sim["variabel"])
            st.dataframe(df_var, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_misi:
            st.markdown("<div class='glass-card' style='text-align:left; padding:30px; height:100%;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size:22px; margin-top:0;'>🎯 Misi Penyelidikan Siswa (LKPD)</h3>", unsafe_allow_html=True)
            for m_teks in data_sim["misi"]:
                st.markdown(f"<div class='mission-step'><b>{m_teks.split(':')[0]}:</b>{m_teks.split(':', 1)[1]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 4. TANTANGAN LAB BERHADIAH POIN (+50 XP)
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left; padding:35px; border:2px solid #BFDBFE;'>", unsafe_allow_html=True)
        st.markdown("<span class='lab-badge'>🏆 Tantangan Evaluasi Eksperimen (+50 Poin)</span>", unsafe_allow_html=True)
        kuis_info = data_sim["kuis_lab"]
        st.markdown(f"<h3 style='font-size:21px; line-height:1.6; margin-top:5px;'>{kuis_info['soal']}</h3>", unsafe_allow_html=True)
        
        jawaban_lab = st.radio("Pilih Hasil Analisis Eksperimenmu:", kuis_info["opsi"], key=f"rad_lab_{pilihan_sim}")
        st.write("<br>", unsafe_allow_html=True)

        if st.button("🚀 Periksa Jawaban & Klaim +50 Poin Eksperimen", key=f"btn_lab_{pilihan_sim}"):
            if jawaban_lab == kuis_info["jawaban"]:
                st.session_state.sfx = "benar"
                if pilihan_sim not in st.session_state.lab_claimed:
                    db_update_points(player, points_db + 50)
                    st.session_state.lab_claimed.add(pilihan_sim)
                    st.balloons()
                    st.success("🎉 ANALISIS SEMPURNA! Kamu berhak mendapatkan +50 Poin Akademik dari eksperimen ini!")
                else:
                    st.success("✅ Jawabanmu Tepat! (Poin untuk modul lab ini sudah pernah kamu klaim pada sesi ini).")
            else:
                st.session_state.sfx = "salah"
                st.error(f"❌ Analisis belum tepat. Kunci yang benar: **{kuis_info['jawaban']}**")

            st.markdown(f"""
            <div style='background:#F0FDF4; border:1px solid #86EFAC; border-radius:20px; padding:22px; margin-top:15px;'>
                <h4 style='color:#166534 !important; margin-top:0;'>📘 Pembahasan Konsep Mendalam:</h4>
                <p style='color:#14532D !important; margin-bottom:12px;'>{kuis_info['pembahasan_konsep']}</p>
                <h4 style='color:#1D4ED8 !important; margin-top:0;'>⚡ Trik Kilat Mentor:</h4>
                <p style='color:#1E3A8A !important; margin:0;'>{kuis_info['trik_mentor']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_lokal:
        st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:24px; margin-top:0;'>🎮 Koleksi Game & Simulasi Interaktif dari Folder <code>uploads/</code></h3>", unsafe_allow_html=True)
        st.caption("Semua berkas `.html` yang tersimpan di dalam folder `uploads/simulasi_interaktif/` maupun subfolder modul otomatis dimuat sebagai game interaktif di sini.")

        folder_sim = os.path.join("uploads", "simulasi_interaktif")
        os.makedirs(folder_sim, exist_ok=True)

        # Cari semua file .html di seluruh direktori uploads/
        daftar_html = []
        for root_dir
