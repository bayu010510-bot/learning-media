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

# CSS Super Elegan & Akademis (Royal Navy & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800;900&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Background Royal Navy */
    .stApp { 
        background-color: #060B19; 
        background-image: radial-gradient(circle at 50% 0%, #112240 0%, #060B19 80%); 
        color: #F8FAFC; 
    }
    
    /* Tipografi Khusus Judul (Akademis/Klasik) */
    h1, h2, h3 { font-family: 'Cinzel', serif !important; text-transform: uppercase; letter-spacing: 2px; }
    h4, h5, p, span, label { color: #E2E8F0 !important; }
    
    /* Efek Teks Prestisius (Emas & Platinum) */
    .gradient-text { background: linear-gradient(135deg, #D4AF37 0%, #FFF5D1 50%, #D4AF37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; text-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
    .vs-text { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 55px; text-shadow: 0 0 30px rgba(255, 65, 108, 0.6); font-family: 'Cinzel', serif; }
    
    /* Animasi Masuk (Fade-In Halus) */
    @keyframes fadeInUp { from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);} }
    .stApp > header { background-color: transparent; }
    .block-container { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1); }
    
    /* Logo Glow Effect */
    .aksara-logo { border-radius: 15px; box-shadow: 0 0 30px rgba(212, 175, 55, 0.5); transition: 0.5s; border: 2px solid rgba(212, 175, 55, 0.3); }
    .aksara-logo:hover { box-shadow: 0 0 50px rgba(212, 175, 55, 0.8); transform: scale(1.02); }
    
    /* Holographic Glassmorphism (Elegan) */
    .glass-card { 
        background: rgba(17, 34, 64, 0.6); 
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border-radius: 16px; 
        border: 1px solid rgba(212, 175, 55, 0.2); 
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 35px; 
        text-align: center; 
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4); 
        transition: all 0.4s ease; 
    }
    .glass-card:hover { transform: translateY(-5px); border-color: rgba(212, 175, 55, 0.6); box-shadow: 0 15px 40px rgba(212, 175, 55, 0.15); }
    
    /* Kartu Skor Kuis */
    .score-card { background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(17, 34, 64, 0.8) 100%); border: 1px solid #D4AF37; border-radius: 16px; padding: 30px; text-align: center; backdrop-filter: blur(15px); transition: 0.3s; }
    .score-card:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(212, 175, 55, 0.3); }
    
    /* Buttons: Royal Gold & Navy */
    .stButton>button { 
        background: linear-gradient(135deg, #112240 0%, #0A192F 100%);
        color: #D4AF37 !important; border-radius: 10px; border: 1px solid #D4AF37; padding: 15px 25px; font-weight: 800; font-size: 15px; width: 100%; 
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1.5px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #D4AF37 0%, #B89022 100%); color: #060B19 !important; border: 1px solid #FFF; transform: translateY(-3px); box-shadow: 0 10px 25px rgba(212, 175, 55, 0.5); }
    
    .quiz-btn>button { background: rgba(17, 34, 64, 0.8); border: 2px solid rgba(212, 175, 55, 0.4); font-size: 18px; text-transform: none; padding: 25px; height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 16px; color: #F8FAFC !important; }
    .quiz-btn>button:hover { background: rgba(212, 175, 55, 0.15); border-color: #D4AF37; color: #D4AF37 !important; }
    
    .btn-red>button { background: linear-gradient(135deg, #8B0000 0%, #4A0000 100%); border-color: #FF416C; color: #FFF !important; }
    .btn-red>button:hover { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); border-color: #FFF; box-shadow: 0 8px 25px rgba(255, 65, 108, 0.5); }
    
    .btn-green>button { background: linear-gradient(135deg, #064E3B 0%, #022C22 100%); border-color: #10B981; color: #FFF !important; }
    .btn-green>button:hover { background: linear-gradient(135deg, #10B981 0%, #047857 100%); border-color: #FFF; box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5); }
    
    /* Input Fields (Elegan) */
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: rgba(10, 25, 47, 0.8) !important; border: 1px solid rgba(212, 175, 55, 0.3) !important; border-radius: 10px; transition: 0.3s; }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within { border-color: #D4AF37 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span { color: #D4AF37 !important; -webkit-text-fill-color: #D4AF37 !important; font-weight: 600; font-size: 16px; }
    
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 40px !important; font-family: 'Cinzel', serif; font-weight: 900 !important; text-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    /* Sidebar Akademis */
    [data-testid="stSidebar"] { background-color: rgba(6, 11, 25, 0.95) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(212, 175, 55, 0.15); padding-top: 10px; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #B89022, #D4AF37); box-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }
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
    st.markdown(f"<div style='text-align:center; font-size:80px; text-shadow: 0 0 30px rgba(212,175,55,0.3); animation: fadeInUp 1s ease;'>{'🎓' if keyword=='genius' else '📚'}</div>", unsafe_allow_html=True)

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
        st.image(logo_path, width=150, output_format="auto")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<style>img { border-radius: 20px; box-shadow: 0 0 40px rgba(212, 175, 55, 0.4); border: 2px solid rgba(212, 175, 55, 0.2); }</style>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; font-size:75px; font-weight:900;'><span class='gradient-text'>AKSARA</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:50px; font-size:22px; font-family:Cinzel, serif; letter-spacing:3px;'>INSTITUT EDUKASI INTERAKTIF</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
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
# Audio Kelas Atas (Lonceng untuk Benar, Suara Kayu Solid untuk Salah)
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
    if lvl < 3: return "🥉 Tingkat Dasar", "#CD7F32"
    elif lvl < 6: return "🥈 Tingkat Menengah", "#C0C0C0"
    elif lvl < 10: return "🥇 Tingkat Atas", "#D4AF37"
    elif lvl < 15: return "💎 Sarjana", "#00EDFF"
    else: return "🌌 Mahaguru", "#9D00FF"
tier_name, tier_color = get_tier(user_level)

# --- SIDEBAR NAVIGASI ELEGAN ---
with st.sidebar:
    # 1. INJEKSI CSS MODERN (Revisi Teks Bunglon)
    st.markdown("""
    <style>
    /* Mengatur latar belakang sidebar menjadi cerah */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Mengubah st.radio menjadi tombol navigasi modern */
    div[role="radiogroup"] > label {
        background: #ffffff;
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
        border: 1px solid #edf2f7;
        cursor: pointer;
    }
    
    /* PERBAIKAN TEKS BUNGLON: Memaksa teks radio button berwarna gelap */
    div[role="radiogroup"] > label p, 
    div[role="radiogroup"] > label div {
        color: #2d3436 !important; 
        font-weight: 600;
    }

    div[role="radiogroup"] > label:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(9, 132, 227, 0.1);
        border-color: #0984e3;
        background: #f1faff;
    }
    
    /* PERBAIKAN TEKS BUNGLON SAAT HOVER: Teks menjadi biru */
    div[role="radiogroup"] > label:hover p,
    div[role="radiogroup"] > label:hover div {
        color: #0984e3 !important;
    }
    
    /* Desain Tombol Keluar / Logout */
    .stButton > button {
        width: 100%;
        background: #ff7675;
        color: white !important; /* Memastikan teks tombol keluar tetap putih */
        border-radius: 12px;
        border: none;
        padding: 12px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 118, 117, 0.2);
    }
    .stButton > button:hover {
        background: #d63031;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 118, 117, 0.35);
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    
    # 2. AVATAR & PROFIL
    if custom_avatar_db:
        st.markdown(f"""
        <div style='text-align:center;'>
            <img src='{custom_avatar_db}' style='width:130px; height:130px; border-radius:50%; object-fit:cover; border:4px solid #ffffff; box-shadow: 0 8px 25px rgba(9,132,227,0.2); margin-bottom:15px; transition: 0.3s;' onmouseover='this.style.transform="scale(1.05)"' onmouseout='this.style.transform="scale(1)"'>
        </div>
        """, unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<h2 style='text-align:center; margin-top:10px; margin-bottom:5px; font-weight:800; font-size:22px; color:#2d3436; text-shadow: 1px 1px 2px rgba(0,0,0,0.05);'>{display_name_db}</h2>", unsafe_allow_html=True)
    
    # Badge Title & Tier
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='background:#e3f2fd; color:#0984e3; padding:6px 18px; border-radius:20px; font-weight:700; border:1px solid #bbdefb; font-size:12px; letter-spacing:0.5px;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><span style='background:{tier_color}15; color:{tier_color}; padding:5px 18px; border-radius:20px; font-weight:700; border:1px solid {tier_color}50; font-size:12px; letter-spacing:0.5px; box-shadow: 0 4px 10px {tier_color}20;'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    # 3. PROGRESS BAR
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: #f1f2f6; border-radius: 10px; height: 10px; margin: 20px 0; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #dfe6e9;'>
            <div style='background: linear-gradient(90deg, #74b9ff 0%, #0984e3 100%); width: {prog}%; height: 100%; border-radius: 10px; box-shadow: 0 0 10px rgba(9,132,227,0.3);'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:700; color:#636e72; font-size:13px;'>
            <span>Lvl {user_level}</span><span style='color:#0984e3;'>✨ {points_db} Poin</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Pembatas Estetik
    st.markdown("<hr style='border:none; height:1px; background: linear-gradient(90deg, transparent, #dfe6e9, transparent); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # Judul Navigasi Modern
    st.markdown("<p style='text-align:center; font-size:12px; font-weight:800; color:#b2bec3; letter-spacing:1px; margin-bottom:10px;'>MENU NAVIGASI</p>", unsafe_allow_html=True)
    
    # 4. MENU NAVIGASI
    menu = st.radio("NAVIGASI INSTITUT", [
        "🏠 Dashboard Utama", 
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ], label_visibility="collapsed")
    
    st.markdown("<hr style='border:none; height:1px; background: linear-gradient(90deg, transparent, #dfe6e9, transparent); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # 5. TOMBOL KELUAR
    if st.button("🚪 KELUAR AKADEMI"):
        st.session_state.logged_in = False
        st.rerun()
    
    # 2. AVATAR & PROFIL
    if custom_avatar_db:
        st.markdown(f"""
        <div style='text-align:center;'>
            <img src='{custom_avatar_db}' style='width:130px; height:130px; border-radius:50%; object-fit:cover; border:4px solid #ffffff; box-shadow: 0 8px 25px rgba(9,132,227,0.2); margin-bottom:15px; transition: 0.3s;' onmouseover='this.style.transform="scale(1.05)"' onmouseout='this.style.transform="scale(1)"'>
        </div>
        """, unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<h2 style='text-align:center; margin-top:10px; margin-bottom:5px; font-weight:800; font-size:22px; color:#2d3436; text-shadow: 1px 1px 2px rgba(0,0,0,0.05);'>{display_name_db}</h2>", unsafe_allow_html=True)
    
    # Badge Title & Tier
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='background:#e3f2fd; color:#0984e3; padding:6px 18px; border-radius:20px; font-weight:700; border:1px solid #bbdefb; font-size:12px; letter-spacing:0.5px;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><span style='background:{tier_color}15; color:{tier_color}; padding:5px 18px; border-radius:20px; font-weight:700; border:1px solid {tier_color}50; font-size:12px; letter-spacing:0.5px; box-shadow: 0 4px 10px {tier_color}20;'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    # 3. PROGRESS BAR
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: #f1f2f6; border-radius: 10px; height: 10px; margin: 20px 0; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #dfe6e9;'>
            <div style='background: linear-gradient(90deg, #74b9ff 0%, #0984e3 100%); width: {prog}%; height: 100%; border-radius: 10px; box-shadow: 0 0 10px rgba(9,132,227,0.3);'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:700; color:#636e72; font-size:13px;'>
            <span>Lvl {user_level}</span><span style='color:#0984e3;'>✨ {points_db} Poin</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Pembatas Estetik
    st.markdown("<hr style='border:none; height:1px; background: linear-gradient(90deg, transparent, #dfe6e9, transparent); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # Judul Navigasi Modern
    st.markdown("<p style='text-align:center; font-size:12px; font-weight:800; color:#b2bec3; letter-spacing:1px; margin-bottom:10px;'>MENU NAVIGASI</p>", unsafe_allow_html=True)
    
    # 4. MENU NAVIGASI
    menu = st.radio("NAVIGASI INSTITUT", [
        "🏠 Dashboard Utama", 
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ], label_visibility="collapsed")
    
    st.markdown("<hr style='border:none; height:1px; background: linear-gradient(90deg, transparent, #dfe6e9, transparent); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # 5. TOMBOL KELUAR
    if st.button("🚪 KELUAR AKADEMI"):
        st.session_state.logged_in = False
        st.rerun()
    
    # 2. AVATAR & PROFIL (Bercahaya & Elegan)
    if custom_avatar_db:
        st.markdown(f"""
        <div style='text-align:center;'>
            <img src='{custom_avatar_db}' style='width:130px; height:130px; border-radius:50%; object-fit:cover; border:4px solid #ffffff; box-shadow: 0 8px 25px rgba(9,132,227,0.2); margin-bottom:15px; transition: 0.3s;' onmouseover='this.style.transform="scale(1.05)"' onmouseout='this.style.transform="scale(1)"'>
        </div>
        """, unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<h2 style='text-align:center; margin-top:10px; margin-bottom:5px; font-weight:800; font-size:22px; color:#2d3436; text-shadow: 1px 1px 2px rgba(0,0,0,0.05);'>{display_name_db}</h2>", unsafe_allow_html=True)
    
    # Badge Title & Tier
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='background:#e3f2fd; color:#0984e3; padding:6px 18px; border-radius:20px; font-weight:700; border:1px solid #bbdefb; font-size:12px; letter-spacing:0.5px;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><span style='background:{tier_color}15; color:{tier_color}; padding:5px 18px; border-radius:20px; font-weight:700; border:1px solid {tier_color}50; font-size:12px; letter-spacing:0.5px; box-shadow: 0 4px 10px {tier_color}20;'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    # 3. PROGRESS BAR (Gradasi Biru Cerah)
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: #f1f2f6; border-radius: 10px; height: 10px; margin: 20px 0; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #dfe6e9;'>
            <div style='background: linear-gradient(90deg, #74b9ff 0%, #0984e3 100%); width: {prog}%; height: 100%; border-radius: 10px; box-shadow: 0 0 10px rgba(9,132,227,0.3);'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:700; color:#636e72; font-size:13px;'>
            <span>Lvl {user_level}</span><span style='color:#0984e3;'>✨ {points_db} Poin</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Pembatas Estetik
    st.markdown("<hr style='border:none; height:1px; background: linear-gradient(90deg, transparent, #dfe6e9, transparent); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # Judul Navigasi Modern
    st.markdown("<p style='text-align:center; font-size:12px; font-weight:800; color:#b2bec3; letter-spacing:1px; margin-bottom:10px;'>MENU NAVIGASI</p>", unsafe_allow_html=True)
    
    # 4. MENU NAVIGASI (Otomatis terkena gaya CSS di atas)
    menu = st.radio("NAVIGASI INSTITUT", [
        "🏠 Dashboard Utama", 
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ], label_visibility="collapsed")
    
    st.markdown("<hr style='border:none; height:1px; background: linear-gradient(90deg, transparent, #dfe6e9, transparent); margin: 25px 0;'>", unsafe_allow_html=True)
    
    # 5. TOMBOL KELUAR (Tombol Streamlit asli, didesain ulang via CSS)
    if st.button("🚪 KELUAR AKADEMI"):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if menu == "🏠 Dashboard Utama":
    st.markdown(f"<h1 style='font-size:45px; margin-bottom:10px;'>SELAMAT DATANG, <span class='gradient-text'>{display_name_db.upper()}</span></h1>", unsafe_allow_html=True)
    st.caption("Akses semua catatan akademi dan tingkatkan prestasimu di sini.")
    st.write("<br>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='border-color:rgba(212, 175, 55, 0.6); background:rgba(212, 175, 55, 0.05); padding:25px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#D4AF37; margin-top:0; font-size:26px;'>📜 Gulungan Keberuntungan Harian</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🗝️ BUKA GULUNGAN SEKARANG"):
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
    c1.markdown(f"<div class='glass-card'><div style='font-size:50px; margin-bottom:10px;'>⏳</div><h2 style='margin:0; font-size:35px;'>{streak_db}</h2><p style='color:#94A3B8; font-weight:bold; letter-spacing:1px; margin:0;'>HARI AKTIF</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='glass-card'><div style='font-size:50px; margin-bottom:10px;'>📚</div><h2 style='margin:0; font-size:35px;'>{len(learned_db)}</h2><p style='color:#94A3B8; font-weight:bold; letter-spacing:1px; margin:0;'>MODUL SELESAI</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='glass-card' style='border-color:{tier_color}80;'><div style='font-size:50px; margin-bottom:10px; text-shadow:0 0 20px {tier_color}80;'>🏛️</div><h2 style='color:{tier_color}; margin:0; font-size:35px;'>Lvl {user_level}</h2><p style='color:#94A3B8; font-weight:bold; letter-spacing:1px; margin:0;'>STATUS AKADEMI</p></div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:28px; margin-bottom:20px;'><span class='gradient-text'>🏛️ HALL OF SCHOLARS</span> (TOP 10 AKADEMI)</h3>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    for i, row in enumerate(ranking_data):
        if i == 0: medali, bg_color, bdr_color = "👑", "rgba(212, 175, 55, 0.15)", "rgba(212, 175, 55, 0.6)"
        elif i == 1: medali, bg_color, bdr_color = "🥈", "rgba(192, 192, 192, 0.1)", "rgba(192, 192, 192, 0.5)"
        elif i == 2: medali, bg_color, bdr_color = "🥉", "rgba(205, 127, 50, 0.1)", "rgba(205, 127, 50, 0.5)"
        else: medali, bg_color, bdr_color = f"#{i+1}", "rgba(255,255,255,0.02)", "rgba(255,255,255,0.05)"
        
        d_name = row.get("display_name")
        if not d_name: d_name = row.get("username", "Anonim")
        
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid {bdr_color}; border-radius: 12px; padding: 18px 30px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; transition: 0.3s; box-shadow: 0 5px 15px rgba(0,0,0,0.2);' onmouseover='this.style.transform=\"translateY(-3px)\"' onmouseout='this.style.transform=\"translateY(0)\"'>
            <h3 style='margin:0; font-size:20px;'>{medali} <span style='color:#F8FAFC; margin-left:15px; font-weight:800; font-family:\"Plus Jakarta Sans\", sans-serif;'>{d_name}</span> <span style='font-size:12px; font-weight:800; color:#D4AF37; background:rgba(0,0,0,0.5); padding:4px 12px; border-radius:6px; margin-left:10px; border:1px solid rgba(212,175,55,0.3); letter-spacing:1px; text-transform:uppercase;'>{row.get("title", "")}</span></h3>
            <h3 style='margin:0; color:#D4AF37; font-weight:900; text-shadow: 0 0 10px rgba(212,175,55,0.4);'>✨ {row.get("points", 0)}</h3>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: LIVE ARENA QUIZ (ROOMS + UGC)
# ==========================================
elif menu == "⚡ Live Arena Quiz (NEW!)":
    st.markdown("<h1>⚡ <span class='gradient-text'>ARENA UJIAN TERBUKA</span></h1>", unsafe_allow_html=True)
    
    custom_quizzes_db = db_get_all_custom_quizzes()
    list_custom_titles = [f"🌟 {q['title']} (Karya {q['creator']})" for q in custom_quizzes_db]
    pilihan_mapel_gabungan = list(BANK_SOAL_PRO.keys()) + list_custom_titles

    if not st.session_state.quizizz_aktif and not st.session_state.qz_selesai and not st.session_state.current_room_code:
        tab_solo, tab_join, tab_host, tab_create = st.tabs(["🎮 STUDI MANDIRI", "👥 AULA BERSAMA", "👑 BUKA AULA BARU", "🛠️ ARSIPATOR (BUAT SOAL)"])
        
        with tab_solo:
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            mapel_solo = st.selectbox("🎯 Pilih Gulungan Ujian:", pilihan_mapel_gabungan, key="solo_m")
            st.write("<br>", unsafe_allow_html=True)
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if st.button("🚀 MULAI STUDI MANDIRI", key="btn_solo"):
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
                else: st.error("Materi ujian ini terlalu sedikit!")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        with tab_join:
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>🌐 AULA UJIAN AKTIF</h3>", unsafe_allow_html=True)
            c_ref, _ = st.columns([1, 3])
            with c_ref:
                if st.button("🔄 Periksa Aula Server"): st.rerun()
            st.write("<br>", unsafe_allow_html=True)
            
            active_rooms = db_get_waiting_sessions()
            if active_rooms:
                for room in active_rooms:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(212, 175, 55, 0.3); border-radius:10px; padding:20px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center;'>
                        <div><h4 style='margin:0; color:#D4AF37; font-size:20px;'>📚 {room['mapel']}</h4><span style='font-size:14px; color:#94A3B8; font-weight:bold;'>Pengawas: {room['host_username']} &nbsp;|&nbsp; Sandi Aula: {room['session_code']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🚪 MASUKI AULA INI", key=f"join_{room['session_code']}"):
                        db_join_session(room['session_code'], player)
                        st.session_state.current_room_code = room['session_code']
                        st.session_state.is_host = False
                        st.success("🎯 Berhasil masuk!")
                        st.rerun()
                    st.write("<br>", unsafe_allow_html=True)
            else:
                st.info("📭 Akademi sedang tenang. Belum ada ujian bersama yang dibuat.")
                
            st.markdown("<hr style='border:1px solid rgba(212,175,55,0.2); margin: 30px 0;'>", unsafe_allow_html=True)
            st.caption("Atau masukkan Sandi Rahasia Aula (untuk Aula Privat):")
            kode_input = st.text_input("Ketik 6 Digit Sandi:", max_chars=6, placeholder="Contoh: 849204").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🚪 MASUK VIA SANDI", use_container_width=True):
                if kode_input:
                    room = db_get_quiz_session(kode_input)
                    if room:
                        if room["status"] == "finished": st.error("❌ Aula ujian ini sudah ditutup!")
                        else:
                            db_join_session(kode_input, player)
                            st.session_state.current_room_code = kode_input
                            st.session_state.is_host = False
                            st.success("🎯 Berhasil masuk!")
                            st.rerun()
                    else: st.error("❌ Sandi tidak ditemukan di arsip akademi!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_host:
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            st.markdown("<h3>👑 JADI PENGAWAS AULA BARU</h3>", unsafe_allow_html=True)
            mapel_guru = st.selectbox("🎯 Pilih Materi Ujian:", pilihan_mapel_gabungan, key="guru_m")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("👑 BUKA AULA PUBLIK", use_container_width=True):
                random_code = str(random.randint(100000, 999999))
                db_create_quiz_session(random_code, player, mapel_guru)
                st.session_state.current_room_code = random_code
                st.session_state.is_host = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_create:
            st.markdown("<div class='glass-card' style='text-align:left; border-color:#10B981;'>", unsafe_allow_html=True)
            st.markdown("<h3>🛠️ RUANG ARSIPATOR (BUAT SOAL)</h3>", unsafe_allow_html=True)
            st.caption("Ujian yang kamu susun akan dimasukkan secara permanen ke perpustakaan agung Aksara.")
            
            judul_baru = st.text_input("📝 Berikan Judul Ujian Kamu:").strip()
            
            st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
            for i, q in enumerate(st.session_state.temp_q):
                st.success(f"✅ Soal {i+1} Tersimpan: {q['soal']} (Kunci: {q['jawaban']})")
                
            with st.form("form_tambah_soal", clear_on_submit=True):
                st.markdown("#### ➕ Susun Soal Baru")
                soal_text = st.text_area("Pertanyaan:", height=100)
                c1, c2 = st.columns(2)
                op_benar = c1.text_input("Opsi 1 (Jawaban BENAR):", placeholder="Wajib jawaban benar")
                op_salah1 = c2.text_input("Opsi 2 (Pengecoh):")
                op_salah2 = c1.text_input("Opsi 3 (Pengecoh):")
                op_salah3 = c2.text_input("Opsi 4 (Pengecoh):")
                
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("SIMPAN SOAL KE DRAFT"):
                    if soal_text and op_benar and op_salah1 and op_salah2 and op_salah3:
                        st.session_state.temp_q.append({
                            "soal": soal_text,
                            "opsi": [op_benar, op_salah1, op_salah2, op_salah3],
                            "jawaban": op_benar
                        })
                        st.rerun()
                    else: st.warning("Harap lengkapi seluruh opsi A, B, C, D!")
            
            st.write("<br>", unsafe_allow_html=True)
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if st.button("🚀 TERBITKAN KE PERPUSTAKAAN GLOBAL"):
                if not judul_baru: st.error("Judul tidak boleh kosong!")
                elif db_get_custom_quiz_by_title(judul_baru): st.error("Judul ini sudah terpakai di arsip! Pilih judul lain.")
                elif len(st.session_state.temp_q) < 3: st.error("Minimal susun 3 soal untuk diakui Akademi!")
                else:
                    db_save_custom_quiz(judul_baru, player, st.session_state.temp_q)
                    st.session_state.temp_q = []
                    st.cache_data.clear() # Anti-lag: Reset cache manual untuk kuis baru
                    st.success("🎉 Karya Berhasil Diterbitkan! Silakan cek di tab Buka Aula.")
                    time.sleep(1.5)
                    st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

    elif st.session_state.current_room_code and not st.session_state.quizizz_aktif and not st.session_state.qz_selesai:
        code = st.session_state.current_room_code
        room_info = db_get_quiz_session(code)
        players = db_get_session_players(code)
        
        st.markdown(f"<div class='glass-card' style='border-color:#D4AF37; padding:50px;'>", unsafe_allow_html=True)
        st.markdown(f"<h4>Aula Ujian Aktif: <span style='color:#D4AF37;'>{room_info['mapel']}</span></h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:18px; color:#94A3B8; margin:0; margin-top:20px; font-family:Cinzel,serif;'>SANDI AKSES AULA (PRIVAT):</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size:90px; font-weight:900; color:#D4AF37; letter-spacing:10px; text-shadow:0 0 40px rgba(212,175,55,0.6); margin:10px 0;'>{code}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='margin-top:30px;'>👥 Cendekiawan Hadir ({len(players)} Orang)</h5>", unsafe_allow_html=True)
        
        if players:
            names = ", ".join([p["username"] for p in players])
            st.markdown(f"<div style='background:rgba(0,0,0,0.3); padding:15px; border-radius:10px; color:#D4AF37; font-weight:bold; font-size:16px; border:1px solid rgba(212,175,55,0.3);'>{names}</div>", unsafe_allow_html=True)
        else:
            st.caption("Menunggu partisipan tiba...")
            
        st.write("<br><br>", unsafe_allow_html=True)
        c_ref, c_act = st.columns(2)
        with c_ref:
            if st.button("🔄 PERIKSA KEHADIRAN"): st.rerun()
            
        with c_act:
            if st.session_state.is_host:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🚀 MULAI UJIAN (START)"):
                    if len(players) == 0: st.error("Dibutuhkan minimal 1 siswa untuk memulai!")
                    else:
                        db_update_session_status(code, "active")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("⏱️ Ujian akan segera dimulai saat Pengawas memberi aba-aba.")
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
        if st.button("❌ TINGGALKAN / TUTUP AULA", key="exit_rm"):
            if st.session_state.is_host: db_update_session_status(code, "finished")
            st.session_state.current_room_code = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.is_host and room_info["status"] == "active":
            st.write("<br><br>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:left;'>📈 PAPAN NILAI REAL-TIME</h3>", unsafe_allow_html=True)
            for rank, p in enumerate(players):
                status_icon = "✅ Selesai" if p["status"] == "finished" else "⏳ Mengerjakan"
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(212,175,55,0.2); border-radius:8px; padding:15px 25px; margin-bottom:10px; display:flex; justify-content:space-between; font-size:16px;'>
                    <b>#{rank+1} {p['username']} <span style='font-size:12px; color:#94A3B8; margin-left:10px;'>({status_icon})</span></b>
                    <span style='color:#D4AF37; font-weight:900;'>✨ {p['score']} Nilai</span>
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.quizizz_aktif:
        idx = st.session_state.qz_index
        total_soal = len(st.session_state.qz_soal)
        
        progress_val = int((idx / total_soal) * 100)
        st.progress(progress_val)
        st.markdown(f"<div style='text-align:right; color:#D4AF37; font-weight:bold; font-size:16px; margin-top:10px; font-family:Cinzel,serif;'>Lembar {idx+1} dari {total_soal}</div>", unsafe_allow_html=True)
        
        soal_aktif = st.session_state.qz_soal[idx]
        opsi_acak = soal_aktif["opsi"].copy()
        random.shuffle(opsi_acak)
        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass-card' style='font-size:26px; font-weight:800; padding:50px 40px; border-color:#D4AF37; box-shadow:0 0 20px rgba(212,175,55,0.15); font-family:\"Plus Jakarta Sans\", sans-serif;'>{soal_aktif['soal']}</div><br><br>", unsafe_allow_html=True)
        
        st.markdown("<div class='quiz-btn'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        st.write("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        
        def cek_jawaban(jawaban_dipilih):
            if jawaban_dipilih == soal_aktif["jawaban"]:
                st.session_state.qz_score += 20
                st.session_state.sfx = "benar" 
                st.toast("📜 BENAR! Nilai ditambah 20!", icon="✅")
            else:
                st.session_state.sfx = "salah" 
                st.toast(f"❌ KELIRU! Kunci: {soal_aktif['jawaban']}", icon="💀")
            
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
        st.markdown("<h1 style='text-align:center; font-size:55px;'>🏁 <span class='gradient-text'>UJIAN SELESAI</span></h1>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='score-card'><h3 style='color:#E2E8F0;'>Akurasi Pemahaman</h3><h1 style='color:#D4AF37; font-size:65px; margin:0; font-family:Cinzel,serif; text-shadow:0 0 20px rgba(212,175,55,0.4);'>{akurasi}%</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='score-card'><h3 style='color:#E2E8F0;'>Poin Diraih</h3><h1 style='color:#10B981; font-size:65px; margin:0; font-family:Cinzel,serif; text-shadow:0 0 20px rgba(16,185,129,0.4);'>+{final_xp} ✨</h1></div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
        if st.button("📥 AMANKAN POIN DAN KEMBALI KE LOBBY"):
            if final_xp > 0: db_update_points(player, points_db + final_xp)
            st.session_state.qz_selesai = False
            st.session_state.current_room_code = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: MODE DUEL PVP
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1>⚔️ <span class='gradient-text'>MIMBAR DEBAT AKADEMIK</span></h1>", unsafe_allow_html=True)
    st.caption("Uji kecerdasanmu dengan cendekiawan lain dari seluruh server.")
    
    pool_pvp = {}
    for mp, data_kelas in BANK_SOAL_PRO.items():
        pool_pvp[mp] = []
        for kl, data_bab in data_kelas.items():
            for bb, data_sub in data_bab.items():
                for sub, list_soal in data_sub.items():
                    pool_pvp[mp].extend(list_soal)
                
    if not pool_pvp:
        st.warning("⚠️ Bank soal debat belum disiapkan oleh Mahaguru.")
        st.stop()
        
    col_mapel, col_btn = st.columns([3,1])
    with col_mapel: mapel_duel = st.selectbox("🎯 Pilih Topik Debat:", list(pool_pvp.keys()))
    
    if "lawan_duel" not in st.session_state: st.session_state.lawan_duel = None
    if "kuis_duel" not in st.session_state: st.session_state.kuis_duel = False
    if "soal_pvp_aktif" not in st.session_state: st.session_state.soal_pvp_aktif = None
    
    with col_btn:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🔍 CARI LAWAN DEBAT"):
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
            else: st.error("Tidak ada cendekiawan online saat ini.")
            
    if st.session_state.lawan_duel and st.session_state.kuis_duel and st.session_state.soal_pvp_aktif:
        l_user, l_nama, l_pts = st.session_state.lawan_duel
        st.markdown("<hr style='border:1px solid rgba(212,175,55,0.2); margin: 40px 0;'>", unsafe_allow_html=True)
        
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='glass-card' style='border-color:#D4AF37;'><h2 style='color:#D4AF37; margin:0; font-size:30px;'>{display_name_db}</h2><p style='font-size:18px; font-weight:bold;'>✨ {points_db} Poin</p></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div style='text-align:center; margin-top:20px;'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='glass-card' style='border-color:#FF416C;'><h2 style='color:#FF416C; margin:0; font-size:30px;'>{l_nama}</h2><p style='font-size:18px; font-weight:bold;'>✨ {l_pts} Poin</p></div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left; padding:40px;'>", unsafe_allow_html=True)
        ds = st.session_state.soal_pvp_aktif
        st.markdown(f"<h3 style='font-size:24px; font-weight:900; color:#F8FAFC; text-transform:none; font-family:\"Plus Jakarta Sans\", sans-serif;'>{ds['soal']}</h3>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        j_user = st.radio("Pilih Argumen Anda:", ds['opsi'], key="duel_ans")
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
        if st.button("⚡ AJUKAN ARGUMEN KE DEWAN"):
            if j_user == ds['jawaban']:
                db_update_pvp_win(player, l_user, points_db, l_pts)
                st.session_state.sfx = "benar" 
                st.toast("Argumen Telak! Diterima!", icon="📜")
                st.session_state.kuis_duel = False 
                st.success(f"🎉 **KAMU MENANG!** +100 Poin. {l_nama} kehilangan 20 Poin.")
            else:
                db_update_pvp_lose(player, points_db)
                st.session_state.sfx = "salah" 
                st.toast("Bantahan Gagal!", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"💀 **KAMU KALAH DEBAT!** Jawaban keliru. Kamu kehilangan 30 Poin.")
            
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🔄 Kembali ke Mimbar Utama"): st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 4: RUANG BELAJAR & MODUL
# ==========================================
elif menu == "📖 Ruang Belajar & Modul":
    st.markdown("<h1>📖 <span class='gradient-text'>PERPUSTAKAAN AGUNG</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 30px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("📚 Pilih Manuskrip:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("🎓 Pilih Tingkat:", kelas_list if kelas_list else ["-"])
        
        st.write("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("📑 Bab Utama:", bab_list if bab_list else ["-"])
        sub_list = DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).get(p_bab, {}).get("sub_bab", ["-"])
        with col4: p_sub = st.selectbox("🔖 Fokus Kajian:", sub_list)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    tab_mat, tab_doc = st.tabs(["📌 Intisari Pengetahuan", "📂 Arsip Dokumen Pendukung"])
    
    with tab_mat:
        try: st.markdown(f"<div class='glass-card' style='text-align:left; line-height:2; font-size:17px;'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Gulungan intisari belum ditulis oleh Mahaguru.")

    with tab_doc:
        st.markdown("### 📁 Arsip Lanjutan")
        st.caption("Referensi visual atau perkamen tambahan akan muncul di sini.")
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
            st.info("📭 Akademi belum menyuntikkan dokumen tambahan untuk materi ini.")

# ==========================================
# HALAMAN 5: TOKO GELAR (BLACK MARKET)
# ==========================================
elif menu == "🛒 Black Market Profil":
    st.markdown("<h1>🛒 <span class='gradient-text'>BIRO IDENTITAS AKADEMI</span></h1>", unsafe_allow_html=True)
    
    tab_av, tab_gl, tab_edit = st.tabs(["👤 Potret Standar", "👑 Penukaran Gelar Kehormatan", "⚙️ Restorasi Profil Pribadi"])
    
    with tab_av:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("TERAPKAN: GENI US"):
                db_update_profile(player, display_name_db, custom_avatar="")
                db_update_avatar(player, "Geni Us")
                st.toast("Potret Diterapkan!", icon="🖼️"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("TERAPKAN: SMAR T"):
                db_update_profile(player, display_name_db, custom_avatar="")
                db_update_avatar(player, "Smar T")
                st.toast("Potret Diterapkan!", icon="🖼️"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left;'><h3>Validasi Pencapaian</h3>", unsafe_allow_html=True)
        st.write(f"Sisa Poin Anda Saat Ini: ✨ **{points_db}**")
        st.markdown("<hr style='border:1px solid rgba(212,175,55,0.2); margin: 30px 0;'>", unsafe_allow_html=True)
        for gelar, harga in DAFTAR_GELAR.items():
            cg1, cg2, cg3 = st.columns([3, 1, 1])
            cg1.markdown(f"<h4 style='font-size:20px; font-family:Cinzel,serif;'>{gelar}</h4>", unsafe_allow_html=True)
            cg2.markdown(f"<p style='color:#D4AF37; font-weight:900; font-size:20px;'>✨ {harga}</p>", unsafe_allow_html=True)
            with cg3:
                if title_db == gelar: st.button("✅ Aktif", key=f"ak_{gelar}", disabled=True)
                else:
                    if st.button("Klaim Gelar", key=f"by_{gelar}"):
                        if points_db >= harga:
                            db_update_title(player, gelar, cost=harga)
                            st.toast(f"Gelar resmi dinaikkan menjadi {gelar}!", icon="📜"); st.rerun()
                        else: st.error("Poin Akademik Tidak Cukup!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_edit:
        st.markdown("<div class='glass-card' style='text-align:left; border-color:#D4AF37;'>", unsafe_allow_html=True)
        st.markdown("<h3>⚙️ Kustomisasi Data Pribadi</h3>", unsafe_allow_html=True)
        st.caption("Ubah nama pena dan potret wajah aslimu. Prestasi akademik tidak akan hilang.")
        st.write("<br>", unsafe_allow_html=True)
        
        new_display = st.text_input("Ganti Nama Pena:", value=display_name_db, max_chars=20)
        st.write("<br>", unsafe_allow_html=True)
        new_foto = st.file_uploader("Unggah Potret Profil (Dikemas ulang otomatis):", type=['png', 'jpg', 'jpeg'])
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
        if st.button("💾 SAHKAN PERUBAHAN IDENTITAS"):
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
                    st.error(f"Gagal memproses gambar: {e}")
            
            db_update_profile(player, new_display, b64_foto)
            st.toast("Identitas berhasil disahkan oleh akademi!", icon="✅")
            time.sleep(1)
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 6: KONSOL ADMIN
# ==========================================
elif menu == "⚙️ Konsol Super Admin":
    st.markdown("<h1>⚙️ <span class='gradient-text'>RUANG DEWAN MAHAGURU</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='border-color:#8B0000;'><h2>🔒 SEGEL TINGKAT TINGGI</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukkan Kata Kunci Dekan:", type="password")
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("Buka Segel"):
            if pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
            else: st.error("Akses Ditolak!")
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.success("🔓 Segel Dewan Terbuka.")
        tab_stat, tab_db, tab_upload = st.tabs(["📈 Analitik Prestasi", "👥 Arsip Cendekiawan", "📤 Distribusi Modul"])
        
        users_admin = db_get_all_users_admin()
        df = pd.DataFrame(users_admin) if users_admin else pd.DataFrame()
        
        with tab_stat:
            st.markdown("### 📈 Evaluasi Kinerja Siswa")
            if not df.empty:
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Pendaftar", f"{len(df)} Siswa")
                c2.metric("Total Poin Beredar", f"{df['points'].sum()} ✨")
                c3.metric("Rata-rata Kemampuan", f"{int(df['points'].mean())} ✨")
                
                st.write("<br>", unsafe_allow_html=True)
                st.markdown("<div class='glass-card'><h4>Peta Persebaran Prestasi</h4>", unsafe_allow_html=True)
                chart_data = df.set_index("username")["points"]
                st.bar_chart(chart_data, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.info("Data belum terkumpul.")
            
        with tab_db:
            if not df.empty:
                df_view = df[["username", "title", "points", "streak"]]
                df_view.columns = ["Nama Pena", "Gelar Kehormatan", "Kekayaan Poin", "Kehadiran"]
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            
        with tab_upload:
            st.markdown("### 📤 Distribusi Perkamen Ekstra")
            c1, c2 = st.columns(2)
            with c1: up_mapel = st.selectbox("📚 Target Manuskrip:", list(DATA_MATERI.keys()), key="adm_m")
            k_list = list(DATA_MATERI.get(up_mapel, {}).keys())
            with c2: up_kelas = st.selectbox("🎓 Target Tingkat:", k_list if k_list else ["-"], key="adm_k")
            
            c3, c4 = st.columns(2)
            b_list = list(DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).keys())
            with c3: up_bab = st.selectbox("📑 Target Bab:", b_list if b_list else ["-"], key="adm_b")
            s_list = DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).get(up_bab, {}).get("sub_bab", ["-"])
            with c4: up_sub = st.selectbox("🔖 Target Kajian:", s_list, key="adm_s")
            
            st.write("<br>", unsafe_allow_html=True)
            up_file = st.file_uploader("📂 Sisipkan File (PDF/Gambar):")
            st.write("<br>", unsafe_allow_html=True)
            
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if up_file and st.button("🚀 SIMPAN KE PERPUSTAKAAN"):
                try:
                    folder_t = os.path.join("uploads", bersihkan_nama(up_mapel), bersihkan_nama(up_kelas), bersihkan_nama(up_bab), bersihkan_nama(up_sub))
                    os.makedirs(folder_t, exist_ok=True)
                    with open(os.path.join(folder_t, up_file.name), "wb") as f: f.write(up_file.getbuffer())
                    st.success("✅ Perkamen berhasil diamankan!")
                except Exception as e: st.error(f"❌ Gagal menyegel: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("🔴 SEGEL KEMBALI KONSOL"): st.session_state.is_admin = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
