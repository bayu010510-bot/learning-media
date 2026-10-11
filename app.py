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

# CSS LUXURY MINIMALIST GLASSMORPHISM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Luxury Dark Background dengan Ambient Glow */
    .stApp { 
        background-color: #050507; 
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(212, 175, 55, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.02) 0%, transparent 50%);
        color: #F1F5F9; 
    }
    
    /* Tipografi Khusus Judul (Minimalist Luxury) */
    h1, h2, h3 { font-family: 'Cinzel', serif !important; font-weight: 600; letter-spacing: 1.5px; }
    h4, h5, p, span, label { color: #CBD5E1 !important; font-weight: 300; }
    
    /* Efek Teks Premium Gold (Lebih Halus, Tidak Terlalu Silau) */
    .gradient-text { 
        background: linear-gradient(135deg, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 700; 
        text-shadow: 0 4px 15px rgba(212, 175, 55, 0.1); 
    }
    .vs-text { 
        background: linear-gradient(135deg, #E2E8F0 0%, #94A3B8 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 400; font-size: 45px; 
        letter-spacing: 5px;
        font-family: 'Cinzel', serif; 
    }
    
    /* Animasi Masuk Halus */
    @keyframes fadeInUp { from {opacity: 0; transform: translateY(15px);} to {opacity: 1; transform: translateY(0);} }
    .stApp > header { background-color: transparent; }
    .block-container { animation: fadeInUp 1s cubic-bezier(0.2, 0.8, 0.2, 1); }
    
    /* GLASSMORPHISM CORE: Kartu Elegan Tanpa Shadow Berlebih */
    .glass-card { 
        background: rgba(255, 255, 255, 0.02); 
        backdrop-filter: blur(24px) saturate(150%); 
        -webkit-backdrop-filter: blur(24px) saturate(150%);
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px; 
        text-align: center; 
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); 
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); 
    }
    .glass-card:hover { 
        transform: translateY(-4px); 
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(212, 175, 55, 0.2); 
        box-shadow: 0 15px 50px rgba(212, 175, 55, 0.08); 
    }
    
    /* Kartu Skor Kuis */
    .score-card { 
        background: rgba(212, 175, 55, 0.02); 
        backdrop-filter: blur(16px); 
        border: 1px solid rgba(212, 175, 55, 0.15); 
        border-radius: 20px; padding: 35px; text-align: center; 
        transition: 0.4s ease; 
    }
    .score-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1); }
    
    /* Buttons: Minimalist Glass / Ghost Button Style */
    .stButton>button { 
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        color: #D4AF37 !important; 
        border-radius: 12px; 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        padding: 12px 24px; 
        font-weight: 500; 
        font-size: 14px; 
        width: 100%; 
        box-shadow: none; 
        transition: all 0.3s ease; 
        letter-spacing: 1px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stButton>button:hover { 
        background: rgba(212, 175, 55, 0.1) !important; 
        color: #FFF !important; 
        border: 1px solid rgba(212, 175, 55, 0.6); 
        transform: translateY(-2px); 
    }
    
    /* Varian Button Glass */
    .quiz-btn>button { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); font-size: 16px; font-weight: 400; padding: 25px; border-radius: 16px; color: #F1F5F9 !important; transition: 0.3s; }
    .quiz-btn>button:hover { background: rgba(212, 175, 55, 0.05); border-color: rgba(212, 175, 55, 0.4); color: #D4AF37 !important; }
    
    .btn-red>button { border-color: rgba(255, 65, 108, 0.3); color: #FF416C !important; }
    .btn-red>button:hover { background: rgba(255, 65, 108, 0.1) !important; border-color: #FF416C; color: #FFF !important; }
    
    .btn-green>button { border-color: rgba(16, 185, 129, 0.3); color: #10B981 !important; }
    .btn-green>button:hover { background: rgba(16, 185, 129, 0.1) !important; border-color: #10B981; color: #FFF !important; }
    
    /* Input Fields (Sleek Glass) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { 
        background-color: rgba(255, 255, 255, 0.02) !important; 
        border: 1px solid rgba(255, 255, 255, 0.08) !important; 
        border-radius: 12px; transition: 0.3s; 
    }
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within { 
        border-color: rgba(212, 175, 55, 0.5) !important; 
        background-color: rgba(255, 255, 255, 0.04) !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span { color: #E2E8F0 !important; font-weight: 400; font-size: 15px; }
    
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 36px !important; font-family: 'Cinzel', serif; font-weight: 600 !important; text-shadow: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    /* Sidebar Minimalist Glass */
    [data-testid="stSidebar"] { 
        background-color: rgba(5, 5, 7, 0.6) !important; 
        backdrop-filter: blur(30px); 
        border-right: 1px solid rgba(255, 255, 255, 0.05); 
    }
    
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #B38728, #FCF6BA); border-radius: 10px; }
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
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;} [data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

def tampilkan_avatar(keyword):
    st.markdown(f"<div style='text-align:center; font-size:80px; text-shadow: 0 10px 30px rgba(212,175,55,0.2); animation: fadeInUp 1s ease;'>{'🎓' if keyword=='genius' else '📚'}</div>", unsafe_allow_html=True)

# ==========================================
# 5. PORTAL LOGIN / REGISTER (GERBANG AKADEMI)
# ==========================================
if not st.session_state.logged_in:
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Deteksi dan Tampilkan Logo jika ada
    logo_path = None
    if os.path.exists("logo.jpg"): logo_path = "logo.jpg"
    elif os.path.exists("logo.png"): logo_path = "logo.png"
    
    if logo_path:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.image(logo_path, width=120, output_format="auto")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<style>img { border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255, 255, 255, 0.1); }</style>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; font-size:65px; font-weight:800; margin-bottom: 0;'><span class='gradient-text'>AKSARA</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:50px; font-size:18px; font-family:Cinzel, serif; letter-spacing:4px;'>INSTITUT EDUKASI INTERAKTIF</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.2, 1])
    with col_form:
        st.markdown("<div class='glass-card' style='padding:40px;'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 GERBANG MASUK", "📝 REGISTRASI AKADEMI"])
        
        with tab_log:
            l_user = st.text_input("Nama Cendekiawan:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🏛️ MASUKI AKADEMI"):
                if l_user and l_pass:
                    user_record = db_get_user(l_user)
                    if user_record and user_record.get("password") == hash_password(l_pass):
                        st.session_state.username = user_record["username"] 
                        st.session_state.logged_in = True; st.rerun()
                    else: st.error("❌ Kredensial tidak dikenali institut!")
                else: st.warning("Gulungan formulir belum lengkap!")
                
        with tab_reg:
            r_user = st.text_input("Nama Panggilan (Maks 15 Karakter):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Sandi Keamanan:", type="password", key="r_pwd").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("✨ DAFTARKAN NAMA SAYA"):
                if r_user and r_pass:
                    if db_get_user(r_user): st.error("⚠️ Nama ini sudah terdaftar dalam arsip akademi!")
                    else:
                        db_create_user(r_user, hash_password(r_pass))
                        st.success("🎉 Pendaftaran Berhasil! Silakan masuk melalui Gerbang Masuk.")
                else: st.warning("Gulungan formulir belum lengkap!")
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
    if lvl < 3: return "🥉 Tingkat Dasar", "rgba(205, 127, 50, 0.8)"
    elif lvl < 6: return "🥈 Tingkat Menengah", "rgba(192, 192, 192, 0.8)"
    elif lvl < 10: return "🥇 Tingkat Atas", "rgba(212, 175, 55, 0.8)"
    elif lvl < 15: return "💎 Sarjana", "rgba(0, 237, 255, 0.8)"
    else: return "🌌 Mahaguru", "rgba(157, 0, 255, 0.8)"
tier_name, tier_color = get_tier(user_level)

# --- SIDEBAR NAVIGASI ELEGAN (GLASSMORPHISM) ---
with st.sidebar:
    st.markdown("""
    <style>
    /* Radio Menu Navigasi (Sleek Glass Mode) */
    div[role="radiogroup"] > label {
        background: transparent !important;
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 6px;
        border: 1px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    div[role="radiogroup"] > label p, 
    div[role="radiogroup"] > label div {
        color: #94A3B8 !important; 
        font-weight: 400;
        font-size: 14px;
    }

    div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transform: translateX(5px);
    }
    
    div[role="radiogroup"] > label:hover p,
    div[role="radiogroup"] > label:hover div {
        color: #F8FAFC !important;
    }
    
    /* Tombol Logout Minimalis */
    .stButton > button {
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    # 2. AVATAR & PROFIL PANEL
    if custom_avatar_db:
        st.markdown(f"""
        <div style='text-align:center;'>
            <img src='{custom_avatar_db}' style='width:110px; height:110px; border-radius:50%; object-fit:cover; border:2px solid rgba(212, 175, 55, 0.3); padding:4px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin-bottom:15px; transition: 0.3s;' onmouseover='this.style.transform="scale(1.05)"' onmouseout='this.style.transform="scale(1)"'>
        </div>
        """, unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<h2 style='text-align:center; margin-top:5px; margin-bottom:2px; font-weight:600; font-size:20px; color:#F8FAFC;'>{display_name_db}</h2>", unsafe_allow_html=True)
    
    # Badge Judul & Tingkatan
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='background:rgba(255,255,255,0.05); color:#CBD5E1; padding:4px 14px; border-radius:20px; font-weight:400; border:1px solid rgba(255,255,255,0.1); font-size:11px; letter-spacing:0.5px;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:25px;'><span style='color:{tier_color}; padding:4px 14px; border-radius:20px; font-weight:500; border:1px solid {tier_color}; font-size:11px; letter-spacing:0.5px;'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    # 3. LEVEL PROGRESS BAR
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border-radius: 10px; height: 6px; margin: 15px 0; overflow:hidden;'>
            <div style='background: linear-gradient(90deg, #B38728, #FCF6BA); width: {prog}%; height: 100%; border-radius: 10px; box-shadow: 0 0 10px rgba(212,175,55,0.3);'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:400; color:#94A3B8; font-size:12px;'>
            <span>Lvl {user_level}</span><span style='color:#D4AF37;'>✨ {points_db} Pts</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:none; height:1px; background: rgba(255,255,255,0.05); margin: 25px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px; font-weight:500; color:#64748B; letter-spacing:2px; margin-bottom:12px;'>MAIN MENU</p>", unsafe_allow_html=True)
    
    # 4. RADIO MENU
    menu = st.radio("NAVIGASI INSTITUT", [
        "🏠 Dashboard Utama", 
        "📢 Mading Pemberitahuan", 
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ], label_visibility="collapsed", key="navigasi_utama")
    
    st.markdown("<hr style='border:none; height:1px; background: rgba(255,255,255,0.05); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # 5. TOMBOL LOGOUT
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("🚪 KELUAR AKADEMI"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if menu == "🏠 Dashboard Utama":
    st.markdown(f"<h1 style='font-size:40px; margin-bottom:5px; font-weight:400;'>WELCOME, <span class='gradient-text'>{display_name_db.upper()}</span></h1>", unsafe_allow_html=True)
    st.caption("Akses semua catatan akademi dan tingkatkan prestasimu di sini.")
    st.write("<br>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='padding:25px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#D4AF37; margin-top:0; font-size:22px; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:400;'>✨ Daily Honor Roll</h2>", unsafe_allow_html=True)
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
    c1.markdown(f"<div class='glass-card'><div style='font-size:35px; margin-bottom:15px; opacity:0.8;'>⏳</div><h2 style='margin:0; font-size:32px; font-family:\"Plus Jakarta Sans\", sans-serif;'>{streak_db}</h2><p style='color:#64748B; font-weight:400; letter-spacing:1px; margin:0; font-size:12px;'>HARI AKTIF</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='glass-card'><div style='font-size:35px; margin-bottom:15px; opacity:0.8;'>📚</div><h2 style='margin:0; font-size:32px; font-family:\"Plus Jakarta Sans\", sans-serif;'>{len(learned_db)}</h2><p style='color:#64748B; font-weight:400; letter-spacing:1px; margin:0; font-size:12px;'>MODUL SELESAI</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:35px; margin-bottom:15px; opacity:0.8;'>🏛️</div><h2 style='color:{tier_color}; margin:0; font-size:32px; font-family:\"Plus Jakarta Sans\", sans-serif;'>Lvl {user_level}</h2><p style='color:#64748B; font-weight:400; letter-spacing:1px; margin:0; font-size:12px;'>STATUS AKADEMI</p></div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:24px; margin-bottom:20px; font-weight:400;'><span class='gradient-text'>Hall of Scholars</span> (Top 10)</h3>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    for i, row in enumerate(ranking_data):
        if i == 0: medali, bg_color, bdr_color = "👑", "rgba(212, 175, 55, 0.05)", "rgba(212, 175, 55, 0.3)"
        elif i == 1: medali, bg_color, bdr_color = "🥈", "rgba(192, 192, 192, 0.02)", "rgba(192, 192, 192, 0.2)"
        elif i == 2: medali, bg_color, bdr_color = "🥉", "rgba(205, 127, 50, 0.02)", "rgba(205, 127, 50, 0.2)"
        else: medali, bg_color, bdr_color = f"#{i+1}", "rgba(255,255,255,0.01)", "rgba(255,255,255,0.05)"
        
        d_name = row.get("display_name")
        if not d_name: d_name = row.get("username", "Anonim")
        
        st.markdown(f"""
        <div style='background: {bg_color}; backdrop-filter: blur(10px); border: 1px solid {bdr_color}; border-radius: 12px; padding: 18px 30px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; transition: 0.3s;' onmouseover='this.style.background=\"rgba(255,255,255,0.04)\"' onmouseout='this.style.background=\"{bg_color}\"'>
            <h3 style='margin:0; font-size:16px; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:400; color:#94A3B8;'>{medali} <span style='color:#F8FAFC; margin-left:15px; font-weight:500;'>{d_name}</span> <span style='font-size:10px; font-weight:400; color:#D4AF37; background:rgba(212,175,55,0.05); padding:4px 10px; border-radius:4px; margin-left:10px; border:1px solid rgba(212,175,55,0.2); letter-spacing:1px; text-transform:uppercase;'>{row.get("title", "")}</span></h3>
            <h3 style='margin:0; color:#D4AF37; font-weight:600; font-family:\"Plus Jakarta Sans\", sans-serif; font-size:16px;'>✨ {row.get("points", 0)}</h3>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# HALAMAN 2: MADING PEMBERITAHUAN (LUXURY GLASS)
# ==============================================================================
st.markdown("""
<style>
.mading-container {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 30px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.mading-container:hover {
    transform: translateY(-4px);
    background: rgba(255, 255, 255, 0.035);
    border-color: rgba(212, 175, 55, 0.2);
}
.mading-tag {
    background: rgba(212, 175, 55, 0.05);
    color: #D4AF37;
    padding: 4px 12px;
    border-radius: 6px;
    border: 1px solid rgba(212, 175, 55, 0.2);
    font-size: 10px;
    font-weight: 500;
    display: inline-block;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.mading-title-text {
    color: #F8FAFC;
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
    line-height: 1.4;
}
.mading-meta {
    color: #64748B;
    font-size: 11px;
    margin-bottom: 18px;
    font-weight: 300;
    letter-spacing: 0.5px;
}
.mading-body {
    color: #CBD5E1;
    font-size: 13px;
    line-height: 1.6;
    font-weight: 300;
}
</style>
""", unsafe_allow_html=True)

if menu == "📢 Mading Pemberitahuan":
    st.markdown("<h1 style='font-size:35px; font-weight: 500; margin-bottom: 5px;'>Bulletin Board</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 14px;'>Informasi kreatif, pengumuman penting, dan galeri poster institut.</p>", unsafe_allow_html=True)
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
                            # Gambar dengan inline style minimalis agar menyatu dengan background
                            st.markdown(f"<div style='margin-top:-20px; padding:0 24px;'><img src='{item['gambar']}' style='width:100%; border-radius:8px; border:1px solid rgba(255,255,255,0.05);'></div>", unsafe_allow_html=True)
                        except:
                            st.caption("⚠️ Gagal memuat berkas gambar poster.")
                            
                    st.markdown(f"""
                    <div style='background: transparent; padding: 15px 24px 24px 24px;'>
                        <p class="mading-body">{item['deskripsi']}</p>
                    </div>
                    <div style='margin-bottom: 10px;'></div>
                    """, unsafe_allow_html=True)
                    
    with tab_tambah:
        st.markdown("<div class='glass-card' style='text-align:left; padding:30px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:20px; margin-bottom:15px;'>Buat Poster Mading Baru</h3>", unsafe_allow_html=True)
        
        with st.form("form_tambah_mading", clear_on_submit=True):
            judul_baru = st.text_input("Judul Poster / Pengumuman")
            kategori_baru = st.selectbox("Label Kategori", ["Event", "Informasi", "Pembaruan", "Edukasi", "Prestasi"])
            deskripsi_baru = st.text_area("Isi Informasi / Deskripsi Singkat")
            
            pilihan_media = st.radio("Media Gambar", ["URL Tautan Eksternal", "Unggah Perangkat"])
            tautan_gambar = ""
            
            if pilihan_media == "URL Tautan Eksternal":
                tautan_gambar = st.text_input("URL Gambar (HTTPS)")
            else:
                berkas_unggah = st.file_uploader("Unggah JPG/PNG", type=["jpg", "jpeg", "png"])
                if berkas_unggah is not None:
                    tautan_gambar = berkas_unggah
                    
            st.write("<br>", unsafe_allow_html=True)
            tombol_submit = st.form_submit_button("PUBLIKASIKAN POSTER")
            
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
            st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'>", unsafe_allow_html=True)
            mapel_solo = st.selectbox("Pilih Kurikulum Ujian:", pilihan_mapel_gabungan, key="solo_m")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("MULAI STUDI MANDIRI", key="btn_solo"):
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
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_join:
            st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size:20px; font-weight:400;'>AULA AKTIF</h3>", unsafe_allow_html=True)
            c_ref, _ = st.columns([1, 3])
            with c_ref:
                if st.button("Refresh Daftar Server"): st.rerun()
            st.write("<br>", unsafe_allow_html=True)
            
            active_rooms = db_get_waiting_sessions()
            if active_rooms:
                for room in active_rooms:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255, 255, 255, 0.05); border-radius:12px; padding:20px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center;'>
                        <div><h4 style='margin:0; color:#E2E8F0; font-size:16px; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:400;'>{room['mapel']}</h4><span style='font-size:12px; color:#64748B;'>Host: {room['host_username']} &nbsp;|&nbsp; Kode: {room['session_code']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"MASUK AULA INI", key=f"join_{room['session_code']}"):
                        db_join_session(room['session_code'], player)
                        st.session_state.current_room_code = room['session_code']
                        st.session_state.is_host = False
                        st.rerun()
            else:
                st.caption("Tidak ada aula terbuka saat ini.")
                
            st.markdown("<hr style='border:1px solid rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)
            st.caption("Atau masukkan PIN Privat:")
            kode_input = st.text_input("PIN 6 Digit (Akses Privat):", max_chars=6).strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("GABUNG VIA PIN"):
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
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_host:
            st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size:20px; font-weight:400;'>BUKA AULA BARU</h3>", unsafe_allow_html=True)
            mapel_guru = st.selectbox("Materi Ujian:", pilihan_mapel_gabungan, key="guru_m")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("BUKA SERVER"):
                random_code = str(random.randint(100000, 999999))
                db_create_quiz_session(random_code, player, mapel_guru)
                st.session_state.current_room_code = random_code
                st.session_state.is_host = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_create:
            st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size:20px; font-weight:400;'>MANUFAKTUR SOAL</h3>", unsafe_allow_html=True)
            judul_baru = st.text_input("Label / Judul Ujian Custom:").strip()
            
            st.markdown("<hr style='border:1px solid rgba(255,255,255,0.05); margin: 25px 0;'>", unsafe_allow_html=True)
            for i, q in enumerate(st.session_state.temp_q):
                st.caption(f"✓ Terarsip: {q['soal']} (Jawaban: {q['jawaban']})")
                
            with st.form("form_tambah_soal", clear_on_submit=True):
                soal_text = st.text_area("Deskripsi Pertanyaan:", height=80)
                c1, c2 = st.columns(2)
                op_benar = c1.text_input("Opsi Valid (Kunci Benar):")
                op_salah1 = c2.text_input("Opsi Palsu 1:")
                op_salah2 = c1.text_input("Opsi Palsu 2:")
                op_salah3 = c2.text_input("Opsi Palsu 3:")
                
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("SIMPAN SOAL INI"):
                    if soal_text and op_benar and op_salah1 and op_salah2 and op_salah3:
                        st.session_state.temp_q.append({
                            "soal": soal_text,
                            "opsi": [op_benar, op_salah1, op_salah2, op_salah3],
                            "jawaban": op_benar
                        })
                        st.rerun()
                    else: st.warning("Data form belum utuh.")
            
            st.write("<br>", unsafe_allow_html=True)
            if st.button("PUBLIKASIKAN KE CLOUD"):
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
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.current_room_code and not st.session_state.quizizz_aktif and not st.session_state.qz_selesai:
        code = st.session_state.current_room_code
        room_info = db_get_quiz_session(code)
        players = db_get_session_players(code)
        
        st.markdown(f"<div class='glass-card' style='padding:50px;'>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-size:16px; color:#94A3B8; font-weight:400;'>Sesi Modul: <span style='color:#E2E8F0;'>{room_info['mapel']}</span></h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:12px; color:#64748B; margin-top:20px; font-weight:300; letter-spacing:2px;'>KODE AKSES PRIVAT</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size:75px; font-weight:400; color:#D4AF37; letter-spacing:15px; margin:0; font-family:\"Plus Jakarta Sans\", sans-serif;'>{code}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin-top:30px; font-size:14px; color:#CBD5E1;'>Partisipan Hadir: {len(players)}</p>", unsafe_allow_html=True)
        
        if players:
            names = ", ".join([p["username"] for p in players])
            st.markdown(f"<div style='background:rgba(255,255,255,0.02); padding:15px; border-radius:10px; color:#94A3B8; font-size:14px; border:1px solid rgba(255,255,255,0.05);'>{names}</div>", unsafe_allow_html=True)
        else:
            st.caption("Sistem menunggu *handshake* partisipan...")
            
        st.write("<br><br>", unsafe_allow_html=True)
        c_ref, c_act = st.columns(2)
        with c_ref:
            if st.button("PERIKSA STATUS"): st.rerun()
            
        with c_act:
            if st.session_state.is_host:
                if st.button("MULAI SESI (START)"):
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
                    
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("DISCONNECT SERVER", key="exit_rm"):
            if st.session_state.is_host: db_update_session_status(code, "finished")
            st.session_state.current_room_code = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.is_host and room_info["status"] == "active":
            st.write("<br><br>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:left; font-size:18px; font-weight:400;'>LIVE TELEMETRY</h3>", unsafe_allow_html=True)
            for rank, p in enumerate(players):
                status_icon = "Selesai" if p["status"] == "finished" else "Sinkronisasi Data"
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); border-radius:8px; padding:15px 25px; margin-bottom:10px; display:flex; justify-content:space-between; font-size:14px; font-family:\"Plus Jakarta Sans\", sans-serif; color:#CBD5E1;'>
                    <span>{rank+1}. {p['username']} <span style='font-size:11px; color:#64748B; margin-left:10px;'>[{status_icon}]</span></span>
                    <span style='color:#D4AF37; font-weight:500;'>{p['score']} Pts</span>
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.quizizz_aktif:
        idx = st.session_state.qz_index
        total_soal = len(st.session_state.qz_soal)
        
        progress_val = int((idx / total_soal) * 100)
        st.progress(progress_val)
        st.markdown(f"<div style='text-align:right; color:#64748B; font-weight:400; font-size:12px; margin-top:8px; letter-spacing:1px;'>PAGE {idx+1} OF {total_soal}</div>", unsafe_allow_html=True)
        
        soal_aktif = st.session_state.qz_soal[idx]
        opsi_acak = soal_aktif["opsi"].copy()
        random.shuffle(opsi_acak)
        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass-card' style='font-size:20px; font-weight:300; padding:50px 40px; line-height:1.6; color:#F8FAFC;'>{soal_aktif['soal']}</div><br><br>", unsafe_allow_html=True)
        
        st.markdown("<div class='quiz-btn'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        st.write("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        
        def cek_jawaban(jawaban_dipilih):
            if jawaban_dipilih == soal_aktif["jawaban"]:
                st.session_state.qz_score += 20
                st.session_state.sfx = "benar" 
                st.toast("Akurasi Valid: +20", icon="✅")
            else:
                st.session_state.sfx = "salah" 
                st.toast(f"Data Invalid. Log Kunci: {soal_aktif['jawaban']}", icon="❌")
            
            st.session_state.qz_index += 1
            if st.session_state.qz_index >= total_soal:
                st.session_state.quizizz_aktif = False
                st.session_state.qz_selesai = True
                if st.session_state.current_room_code:
                    db_update_player_score(st.session_state.current_room_code, player, st.session_state.qz_score)
            time.sleep(0.3)
            st.rerun()
            
        with c1: 
            if st.button(opsi_acak[0], key=f"o0_{idx}"): cek_jawaban(opsi_acak[0])
        with c2: 
            if st.button(opsi_acak[1], key=f"o1_{idx}"): cek_jawaban(opsi_acak[1])
        if len(opsi_acak) > 2:
            with c3: 
                if st.button(opsi_acak[2], key=f"o2_{idx}"): cek_jawaban(opsi_acak[2])
            with c4: 
                if st.button(opsi_acak[3], key=f"o3_{idx}"): cek_jawaban(opsi_acak[3])
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.qz_selesai:
        final_xp = st.session_state.qz_score
        total_soal = len(st.session_state.qz_soal)
        akurasi = int((final_xp / 100) * 100) if total_soal > 0 else 0
        
        if akurasi > 70: st.balloons()
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-size:45px; font-weight:400;'><span class='gradient-text'>SESI SELESAI</span></h1>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='score-card'><h3 style='color:#64748B; font-size:14px; font-family:\"Plus Jakarta Sans\", sans-serif; letter-spacing:1px; margin-bottom:10px;'>Akurasi Logika</h3><h1 style='color:#E2E8F0; font-size:50px; margin:0; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:300;'>{akurasi}%</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='score-card'><h3 style='color:#64748B; font-size:14px; font-family:\"Plus Jakarta Sans\", sans-serif; letter-spacing:1px; margin-bottom:10px;'>Poin Terektraksi</h3><h1 style='color:#D4AF37; font-size:50px; margin:0; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:400;'>+{final_xp}</h1></div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        if st.button("SINKRONISASI DATA & KEMBALI"):
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
        
    col_mapel, col_btn = st.columns([3,1])
    with col_mapel: mapel_duel = st.selectbox("Topik Arsitektur Debat:", list(pool_pvp.keys()))
    
    if "lawan_duel" not in st.session_state: st.session_state.lawan_duel = None
    if "kuis_duel" not in st.session_state: st.session_state.kuis_duel = False
    if "soal_pvp_aktif" not in st.session_state: st.session_state.soal_pvp_aktif = None
    
    with col_btn:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("PING LAWAN TERDEKAT"):
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
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.05); margin: 40px 0;'>", unsafe_allow_html=True)
        
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='glass-card' style='padding:25px;'><h2 style='color:#E2E8F0; margin:0; font-size:20px; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:400;'>{display_name_db}</h2><p style='font-size:14px; font-weight:300; color:#D4AF37; margin:0;'>✨ {points_db} Pts</p></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div style='text-align:center; margin-top:20px;'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='glass-card' style='padding:25px;'><h2 style='color:#E2E8F0; margin:0; font-size:20px; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:400;'>{l_nama}</h2><p style='font-size:14px; font-weight:300; color:#94A3B8; margin:0;'>✨ {l_pts} Pts</p></div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left; padding:40px;'>", unsafe_allow_html=True)
        ds = st.session_state.soal_pvp_aktif
        st.markdown(f"<h3 style='font-size:18px; font-weight:300; color:#F8FAFC; font-family:\"Plus Jakarta Sans\", sans-serif; line-height:1.6;'>{ds['soal']}</h3>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        j_user = st.radio("Suntikkan Argumen Data:", ds['opsi'], key="duel_ans")
        
        st.write("<br><br>", unsafe_allow_html=True)
        if st.button("EKSEKUSI ARGUMEN DEBAT"):
            if j_user == ds['jawaban']:
                db_update_pvp_win(player, l_user, points_db, l_pts)
                st.session_state.sfx = "benar" 
                st.toast("Argumen Telak Diterima Sistem.", icon="📜")
                st.session_state.kuis_duel = False 
                st.success(f"Logika Sempurna. Anda menang! (+100 Pts). Data {l_nama} didepresiasi 20 Pts.")
            else:
                db_update_pvp_lose(player, points_db)
                st.session_state.sfx = "salah" 
                st.toast("Syntax Argumen Gagal.", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"Kalkulasi meleset. Debat berakhir. Anda kehilangan 30 Pts.")
            
            st.write("<br>", unsafe_allow_html=True)
            if st.button("KEMBALI KE MIMBAR UTAMA"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# HALAMAN 5: RUANG BELAJAR & MODUL
# ==========================================
elif menu == "📖 Ruang Belajar & Modul":
    st.markdown("<h1><span class='gradient-text'>ARSIP SENTRAL (MODUL)</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 30px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("Indeks Manuskrip:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("Tingkatan Kurikulum:", kelas_list if kelas_list else ["-"])
        
        st.write("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("Sektor Bab:", bab_list if bab_list else ["-"])
        sub_list = DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).get(p_bab, {}).get("sub_bab", ["-"])
        with col4: p_sub = st.selectbox("Fokus Kajian Detail:", sub_list)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    tab_mat, tab_doc = st.tabs(["📌 Ekstrak Data", "📂 Lampiran Dokumen"])
    
    with tab_mat:
        try: st.markdown(f"<div class='glass-card' style='text-align:left; line-height:1.8; font-size:15px; font-weight:300; color:#E2E8F0;'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Sektor data ini kosong atau belum dialokasikan.")

    with tab_doc:
        st.markdown("<h3 style='font-size:18px; font-weight:400;'>📂 Repositori Eksternal</h3>", unsafe_allow_html=True)
        st.caption("Referensi visual pendukung akan dirujuk di partisi ini.")
        st.write("<br>", unsafe_allow_html=True)
        
        folder_t = os.path.join("uploads", bersihkan_nama(p_mapel), bersihkan_nama(p_kelas), bersihkan_nama(p_bab), bersihkan_nama(p_sub))
        if os.path.exists(folder_t) and len(os.listdir(folder_t)) > 0:
            for f in os.listdir(folder_t):
                ext = f.split('.')[-1].lower()
                file_path = os.path.join(folder_t, f)
                
                if ext in ['jpg', 'jpeg', 'png']:
                    st.markdown("<div class='glass-card' style='padding:15px;'>", unsafe_allow_html=True)
                    st.image(file_path, caption=f"🖼️ {f}", use_container_width=True)
                    st.markdown("</div><br>", unsafe_allow_html=True)
                else:
                    with open(file_path, "rb") as file:
                        st.download_button(label=f"⬇️ UNDUH PERKAMEN: {f}", data=file.read(), file_name=f, mime="application/octet-stream")
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
            st.markdown("<div class='glass-card'><h2 style='font-size:18px; font-weight:400; font-family:\"Plus Jakarta Sans\", sans-serif;'>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("INISIALISASI: GENI US"):
                db_update_profile(player, display_name_db, custom_avatar="")
                db_update_avatar(player, "Geni Us")
                st.toast("Paket Tampilan Diterapkan.", icon="🖼️"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2 style='font-size:18px; font-weight:400; font-family:\"Plus Jakarta Sans\", sans-serif;'>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("INISIALISASI: SMAR T"):
                db_update_profile(player, display_name_db, custom_avatar="")
                db_update_avatar(player, "Smar T")
                st.toast("Paket Tampilan Diterapkan.", icon="🖼️"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'><h3 style='font-size:18px; font-weight:400;'>Marketplace Kredensial</h3>", unsafe_allow_html=True)
        st.write(f"Saldo Tersedia: ✨ **{points_db} Pts**")
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.05); margin: 25px 0;'>", unsafe_allow_html=True)
        for gelar, harga in DAFTAR_GELAR.items():
            cg1, cg2, cg3 = st.columns([3, 1, 1])
            cg1.markdown(f"<h4 style='font-size:15px; font-family:\"Plus Jakarta Sans\", sans-serif; font-weight:300; color:#E2E8F0;'>{gelar}</h4>", unsafe_allow_html=True)
            cg2.markdown(f"<p style='color:#D4AF37; font-weight:500; font-size:14px; margin:0;'>✨ {harga}</p>", unsafe_allow_html=True)
            with cg3:
                if title_db == gelar: st.button("Tersemat", key=f"ak_{gelar}", disabled=True)
                else:
                    if st.button("Beli Hak Akses", key=f"by_{gelar}"):
                        if points_db >= harga:
                            db_update_title(player, gelar, cost=harga)
                            st.toast(f"Pembaruan Gelar Sukses: {gelar}", icon="📜"); st.rerun()
                        else: st.error("Saldo Pts tidak mencukupi.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_edit:
        st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:18px; font-weight:400;'>Kustomisasi Modul Visual</h3>", unsafe_allow_html=True)
        st.caption("Timpa nama tampilan dan unggah file render (JPG/PNG).")
        st.write("<br>", unsafe_allow_html=True)
        
        new_display = st.text_input("Definisi Nama Baru:", value=display_name_db, max_chars=20)
        st.write("<br>", unsafe_allow_html=True)
        new_foto = st.file_uploader("Suntikkan Paket Wajah (Otomatis Kompresi):", type=['png', 'jpg', 'jpeg'])
        
        st.write("<br><br>", unsafe_allow_html=True)
        if st.button("OVERRIDE DATABASE PROFIL"):
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
            st.toast("Profil berhasil dioverride sistem.", icon="✅")
            time.sleep(1)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# HALAMAN 7: KONSOL ADMIN
# ==========================================
elif menu == "⚙️ Konsol Super Admin":
    st.markdown("<h1><span class='gradient-text'>SYSTEM ROOT ACCESS</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='padding:40px;'><h2 style='font-size:18px; font-weight:400; margin-bottom:20px; font-family:\"Plus Jakarta Sans\", sans-serif; color:#E2E8F0;'>ENCRYPTED PORTAL</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukan Kernel Password:", type="password")
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("BYPASS PROTOCOL"):
            if pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
            else: st.error("Akses Ditolak. Protokol pertahanan aktif.")
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.success("Akses Root diizinkan.")
        tab_stat, tab_db, tab_upload = st.tabs(["📈 Log Sistem", "👥 Skema Pengguna", "📤 Distribusi Aset"])
        
        users_admin = db_get_all_users_admin()
        df = pd.DataFrame(users_admin) if users_admin else pd.DataFrame()
        
        with tab_stat:
            st.markdown("<h3 style='font-size:16px; font-weight:400;'>Statistik Global Server</h3>", unsafe_allow_html=True)
            if not df.empty:
                c1, c2, c3 = st.columns(3)
                c1.metric("Node Klien Aktif", f"{len(df)}")
                c2.metric("Massa Poin Sirkulasi", f"{df['points'].sum()} Pts")
                c3.metric("Rerata Skor Global", f"{int(df['points'].mean())} Pts")
                
                st.write("<br>", unsafe_allow_html=True)
                st.markdown("<div class='glass-card' style='padding:30px;'><h4 style='font-size:14px; font-weight:400; color:#94A3B8;'>Distribusi Kekayaan Poin</h4>", unsafe_allow_html=True)
                chart_data = df.set_index("username")["points"]
                st.bar_chart(chart_data, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.info("Sistem belum merekam jejak.")
            
        with tab_db:
            if not df.empty:
                df_view = df[["username", "title", "points", "streak"]]
                df_view.columns = ["Username (ID)", "Label Status", "Points", "Ping Harian"]
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            
        with tab_upload:
            st.markdown("<div class='glass-card' style='text-align:left; padding:35px;'><h3 style='font-size:16px; font-weight:400;'>Manajemen Aset Statis</h3>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1: up_mapel = st.selectbox("Target Folder (Mapel):", list(DATA_MATERI.keys()), key="adm_m")
            k_list = list(DATA_MATERI.get(up_mapel, {}).keys())
            with c2: up_kelas = st.selectbox("Target Direktori (Tingkat):", k_list if k_list else ["-"], key="adm_k")
            
            c3, c4 = st.columns(2)
            b_list = list(DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).keys())
            with c3: up_bab = st.selectbox("Target Partisi (Bab):", b_list if b_list else ["-"], key="adm_b")
            s_list = DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).get(up_bab, {}).get("sub_bab", ["-"])
            with c4: up_sub = st.selectbox("Target Node (Sub):", s_list, key="adm_s")
            
            st.write("<br>", unsafe_allow_html=True)
            up_file = st.file_uploader("Pilih Berkas Payload (PDF/IMG):")
            st.write("<br>", unsafe_allow_html=True)
            
            if up_file and st.button("INJEKSI KE LOKAL SERVER"):
                try:
                    folder_t = os.path.join("uploads", bersihkan_nama(up_mapel), bersihkan_nama(up_kelas), bersihkan_nama(up_bab), bersihkan_nama(up_sub))
                    os.makedirs(folder_t, exist_ok=True)
                    with open(os.path.join(folder_t, up_file.name), "wb") as f: f.write(up_file.getbuffer())
                    st.success("File sukses diunggah ke server lokal.")
                except Exception as e: st.error(f"Injeksi gagal: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("TUTUP AKSES ROOT"): st.session_state.is_admin = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
