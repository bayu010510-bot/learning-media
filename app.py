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
# 1. KONFIGURASI HALAMAN & TEMA SPEKTAKULER
# ==========================================
st.set_page_config(page_title="Learning Media | Ultimate Edition", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# CSS Super Canggih V2.0 (Animasi Masuk, Glow Bergerak, UI Halus)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { 
        background-color: #050810; 
        background-image: radial-gradient(circle at 50% -20%, #1a2a4c 0%, #050810 80%); 
        color: #F8FAFC; 
    }
    h1, h2, h3, h4, h5, p, span, label { color: #F8FAFC !important; }
    
    /* Efek Teks Spesial & Animasi */
    .gradient-text { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .vs-text { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 55px; text-shadow: 0 0 30px rgba(255, 65, 108, 0.6); }
    
    /* Animasi Masuk (Fade-In Up) */
    @keyframes fadeInUp { from {opacity: 0; transform: translateY(30px);} to {opacity: 1; transform: translateY(0);} }
    .stApp > header { background-color: transparent; }
    .block-container { animation: fadeInUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); }
    
    /* Animasi Detak Jantung */
    @keyframes pulse-glow { 0% { box-shadow: 0 0 0 0 rgba(0, 198, 255, 0.5); } 70% { box-shadow: 0 0 0 20px rgba(0, 198, 255, 0); } 100% { box-shadow: 0 0 0 0 rgba(0, 198, 255, 0); } }
    
    /* Holographic Glassmorphism V2 */
    .glass-card { 
        background: rgba(15, 23, 42, 0.5); 
        backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        border-radius: 24px; 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        padding: 35px; 
        text-align: center; 
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5); 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
    }
    .glass-card:hover { transform: translateY(-8px); border-color: rgba(0, 198, 255, 0.8); box-shadow: 0 15px 40px rgba(0, 198, 255, 0.25); }
    
    /* Kartu Skor Kuis */
    .score-card { background: linear-gradient(135deg, rgba(0, 198, 255, 0.1) 0%, rgba(0, 114, 255, 0.2) 100%); border: 1px solid #00C6FF; border-radius: 20px; padding: 25px; text-align: center; backdrop-filter: blur(15px); transition: 0.3s; }
    .score-card:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(0, 198, 255, 0.4); }
    
    /* Animated Gradient Buttons */
    .stButton>button { 
        background: linear-gradient(270deg, #00C6FF, #0072FF, #00C6FF);
        background-size: 200% 200%;
        color: white; border-radius: 14px; border: none; padding: 16px 28px; font-weight: 900; font-size: 16px; width: 100%; 
        box-shadow: 0 8px 20px rgba(0, 114, 255, 0.4); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 2px;
        animation: GradientFlow 3s ease infinite;
    }
    @keyframes GradientFlow { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
    .stButton>button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 12px 30px rgba(0, 198, 255, 0.8); }
    .stButton>button:active { transform: translateY(2px) scale(0.95); }
    
    /* Tombol Kuis Khusus (Quizizz Style) */
    .quiz-btn>button { background: rgba(15, 23, 42, 0.7); border: 2px solid rgba(0, 198, 255, 0.5); font-size: 20px; text-transform: none; padding: 25px; height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 20px; }
    .quiz-btn>button:hover { background: rgba(0, 198, 255, 0.2); border-color: #00C6FF; }
    
    .btn-red>button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); box-shadow: 0 8px 20px rgba(255, 75, 43, 0.4); animation: none; }
    .btn-red>button:hover { box-shadow: 0 12px 30px rgba(255, 75, 43, 0.8); }
    .btn-green>button { background: linear-gradient(135deg, #10B981 0%, #047857 100%); box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4); animation: pulse-glow 2s infinite; }
    
    /* Input Fields */
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.6) !important; border: 2px solid rgba(0, 198, 255, 0.3) !important; border-radius: 14px; transition: 0.3s; }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within { border-color: #00C6FF !important; box-shadow: 0 0 15px rgba(0, 198, 255, 0.4); }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span { color: #00C6FF !important; -webkit-text-fill-color: #00C6FF !important; font-weight: bold; font-size: 16px; }
    
    div[data-testid="stMetricValue"] { color: #00C6FF !important; font-size: 45px !important; font-weight: 900 !important; text-shadow: 0 0 20px rgba(0, 198, 255, 0.3); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    /* Sidebar Premium */
    [data-testid="stSidebar"] { background-color: rgba(10, 15, 30, 0.98) !important; backdrop-filter: blur(25px); border-right: 1px solid rgba(255,255,255,0.05); padding-top: 10px; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00C6FF, #0072FF); box-shadow: 0 0 10px #00C6FF; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI MESIN CLOUD (SUPABASE ONLY)
# ==========================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"].strip()
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()
    HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}
except Exception:
    st.error("🚨 Kunci Supabase belum disetel di Streamlit Secrets!")
    st.stop()

# ==========================================
# 3. FUNGSI DATABASE LENGKAP (ANTI-LAG ENGINE INJECTED)
# ==========================================
def db_get_user(username):
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?username=ilike.{username}", headers=HEADERS).json()
        return res[0] if isinstance(res, list) and len(res) > 0 else None
    except: return None

def db_create_user(username, hashed_pwd):
    data = {"username": username, "password": hashed_pwd, "avatar_name": "Geni Us", "title": "🏅 Pemula", "points": 0, "streak": 1, "display_name": username}
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

# ANTI-LAG FIX: Cache Leaderboard selama 60 detik agar server gratisan tidak choke
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

# ANTI-LAG FIX: Cache Daftar Kuis Komunitas agar loading perpustakaan kilat
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
DAFTAR_GELAR = {"⚡ Petarung Cepat": 150, "🧪 Alkemis Gila": 200, "👑 Raja Duel": 400, "🌌 Penguasa Server": 1000}

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def bersihkan_nama(teks): return re.sub(r'[\\/*?:"<>|]', "", teks)

try:
    from database_rangkuman import DATA_MATERI
    from database_soal import BANK_SOAL_PRO
except ImportError:
    DATA_MATERI, BANK_SOAL_PRO = {}, {}
    st.warning("⚠️ File database lokal belum terpasang sempurna.")

if not st.session_state.logged_in:
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;} [data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

def tampilkan_avatar(keyword):
    st.markdown(f"<div style='text-align:center; font-size:80px; text-shadow: 0 0 20px rgba(255,255,255,0.2); animation: pulse-glow 3s infinite;'>{'👨‍🎓' if keyword=='genius' else '👩‍🎓'}</div>", unsafe_allow_html=True)

# ==========================================
# 5. PORTAL LOGIN / REGISTER CLOUD
# ==========================================
if not st.session_state.logged_in:
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:65px; font-weight:900;'>Learning Media <span class='gradient-text'>ULTIMATE</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:50px; font-size:20px; letter-spacing:1px;'>Sistem Edukasi Interaktif Generasi Berikutnya.</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
    with col_form:
        st.markdown("<div class='glass-card' style='padding:40px;'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 MASUK ARENA", "📝 TEMPA AKUN"])
        
        with tab_log:
            l_user = st.text_input("Username Ksatria:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🚀 MULAI PETUALANGAN"):
                if l_user and l_pass:
                    user_record = db_get_user(l_user)
                    if user_record and user_record.get("password") == hash_password(l_pass):
                        st.session_state.username = user_record["username"] 
                        st.session_state.logged_in = True; st.rerun()
                    else: st.error("❌ Identitas tidak dikenali server!")
                else: st.warning("Formulir belum lengkap!")
                
        with tab_reg:
            r_user = st.text_input("Username Baru (Maks 15 Karakter):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Sandi Kuat:", type="password", key="r_pwd").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("✨ DAFTARKAN DIRIKU"):
                if r_user and r_pass:
                    if db_get_user(r_user): st.error("⚠️ Username ini sudah diklaim ksatria lain!")
                    else:
                        db_create_user(r_user, hash_password(r_pass))
                        st.success("🎉 Berhasil! Silakan kembali ke tab Masuk Arena.")
                else: st.warning("Formulir belum lengkap!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 6. MEMUAT DATA PEMAIN & EFEK SUARA
# ==========================================
if st.session_state.sfx == "benar":
    st.markdown('<audio autoplay style="display:none;"><source src="https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg" type="audio/ogg"></audio>', unsafe_allow_html=True)
    st.session_state.sfx = ""
elif st.session_state.sfx == "salah":
    st.markdown('<audio autoplay style="display:none;"><source src="https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg" type="audio/ogg"></audio>', unsafe_allow_html=True)
    st.session_state.sfx = ""

player = st.session_state.username
user_data = db_get_user(player)

if not user_data:
    st.session_state.logged_in = False; st.rerun()

avatar_db = user_data.get("avatar_name", "Geni Us")
title_db = user_data.get("title", "🏅 Pemula")
points_db = user_data.get("points", 0)
streak_db = user_data.get("streak", 1)

display_name_db = user_data.get("display_name")
if not display_name_db: display_name_db = player
custom_avatar_db = user_data.get("custom_avatar")

learned_db = db_get_learned_history(player)
user_level = (points_db // 100) + 1

def get_tier(lvl):
    if lvl < 3: return "🥉 Bronze", "#CD7F32"
    elif lvl < 6: return "🥈 Silver", "#C0C0C0"
    elif lvl < 10: return "🥇 Gold", "#FFD700"
    elif lvl < 15: return "💎 Platinum", "#00EDFF"
    else: return "🌌 Mythic", "#9D00FF"
tier_name, tier_color = get_tier(user_level)

# --- SIDEBAR NAVIGASI SPEKTAKULER ---
with st.sidebar:
    st.write("<br>", unsafe_allow_html=True)
    
    if custom_avatar_db:
        st.markdown(f"<div style='text-align:center;'><img src='{custom_avatar_db}' style='width:140px; height:140px; border-radius:50%; object-fit:cover; border:3px solid #00C6FF; box-shadow: 0 0 20px rgba(0,198,255,0.6); margin-bottom:15px; transition: 0.3s;' onmouseover='this.style.transform=\"scale(1.05)\"' onmouseout='this.style.transform=\"scale(1)\"'></div>", unsafe_allow_html=True)
    else:
        tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
        
    st.markdown(f"<h2 style='text-align:center; margin-top:10px; margin-bottom:5px; font-weight:900; font-size:26px;' class='gradient-text'>{display_name_db}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='background:rgba(0,198,255,0.1); color:#00C6FF; padding:5px 18px; border-radius:20px; font-weight:800; border:1px solid rgba(0,198,255,0.4); text-transform:uppercase; font-size:12px; letter-spacing:1px;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><span style='background:{tier_color}20; color:{tier_color}; padding:5px 18px; border-radius:20px; font-weight:800; border:1px solid {tier_color}; text-transform:uppercase; font-size:12px; letter-spacing:1px; box-shadow: 0 0 10px {tier_color}40;'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border-radius: 12px; height: 14px; margin: 20px 0; border: 1px solid rgba(255,255,255,0.1); overflow:hidden;'>
            <div style='background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%); width: {prog}%; height: 100%; border-radius: 12px; box-shadow: 0 0 15px #00C6FF;'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:bold; color:#94A3B8; font-size:15px;'>
            <span>Lvl {user_level}</span><span style='color:#00C6FF;'>⭐ {points_db} XP</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    menu = st.radio("NAVIGASI SISTEM", [
        "🏠 Dashboard Utama", 
        "⚡ Live Arena Quiz (NEW!)", 
        "⚔️ Mode Duel Ranked (PvP)", 
        "📖 Ruang Belajar & Modul", 
        "🛒 Black Market Profil", 
        "⚙️ Konsol Super Admin"
    ])
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT PROTOKOL"):
        st.session_state.logged_in = False; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# HALAMAN 1: DASHBOARD UTAMA
# ==========================================
if menu == "🏠 Dashboard Utama":
    st.markdown(f"<h1 style='font-size:45px; margin-bottom:30px;'>SELAMAT DATANG KEMBALI, <span class='gradient-text'>{display_name_db.upper()}</span>! 🚀</h1>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='border-color:rgba(245, 158, 11, 0.5); background:rgba(245, 158, 11, 0.05); padding:25px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FCD34D; margin-top:0; font-size:28px;'>🎁 Peti Keberuntungan Harian!</h2>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🗝️ BUKA PETI SEKARANG"):
            bonus = random.choice([20, 50, 100, 150, 200])
            db_update_points(player, points_db + bonus)
            st.session_state.gacha_claimed = True
            st.session_state.sfx = "benar" 
            st.balloons()
            st.success(f"JACKPOT! Kamu mendapat +{bonus} XP!")
            time.sleep(1)
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='glass-card'><div style='font-size:60px; margin-bottom:10px;'>🔥</div><h2 style='margin:0; font-size:40px;'>{streak_db}</h2><p style='color:#94A3B8; font-weight:bold; letter-spacing:1px; margin:0;'>HARI AKTIF</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='glass-card'><div style='font-size:60px; margin-bottom:10px;'>📚</div><h2 style='margin:0; font-size:40px;'>{len(learned_db)}</h2><p style='color:#94A3B8; font-weight:bold; letter-spacing:1px; margin:0;'>MISI SELESAI</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='glass-card' style='border-color:{tier_color}80;'><div style='font-size:60px; margin-bottom:10px; text-shadow:0 0 20px {tier_color}80;'>🏆</div><h2 style='color:{tier_color}; margin:0; font-size:40px;'>Lvl {user_level}</h2><p style='color:#94A3B8; font-weight:bold; letter-spacing:1px; margin:0;'>GLOBAL RANK</p></div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:28px; margin-bottom:20px;'><span class='gradient-text'>📊 HALL OF FAME</span> (TOP 10 SERVER)</h3>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    for i, row in enumerate(ranking_data):
        if i == 0: medali, bg_color, bdr_color = "👑", "rgba(255, 215, 0, 0.15)", "rgba(255, 215, 0, 0.6)"
        elif i == 1: medali, bg_color, bdr_color = "🥈", "rgba(192, 192, 192, 0.1)", "rgba(192, 192, 192, 0.5)"
        elif i == 2: medali, bg_color, bdr_color = "🥉", "rgba(205, 127, 50, 0.1)", "rgba(205, 127, 50, 0.5)"
        else: medali, bg_color, bdr_color = f"#{i+1}", "rgba(255,255,255,0.02)", "rgba(255,255,255,0.05)"
        
        d_name = row.get("display_name")
        if not d_name: d_name = row.get("username", "Anonim")
        
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid {bdr_color}; border-radius: 16px; padding: 18px 30px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; transition: 0.3s; box-shadow: 0 5px 15px rgba(0,0,0,0.2);' onmouseover='this.style.transform=\"translateX(10px)\"' onmouseout='this.style.transform=\"translateX(0)\"'>
            <h3 style='margin:0; font-size:22px;'>{medali} <span style='color:#F8FAFC; margin-left:15px; font-weight:800;'>{d_name}</span> <span style='font-size:12px; font-weight:800; color:#94A3B8; background:rgba(0,0,0,0.4); padding:4px 12px; border-radius:12px; margin-left:10px; border:1px solid rgba(255,255,255,0.1); letter-spacing:1px; text-transform:uppercase;'>{row.get("title", "")}</span></h3>
            <h3 style='margin:0; color:#00C6FF; font-weight:900; text-shadow: 0 0 15px rgba(0,198,255,0.4);'>⭐ {row.get("points", 0)} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: LIVE ARENA QUIZ (ROOMS + UGC)
# ==========================================
elif menu == "⚡ Live Arena Quiz (NEW!)":
    st.markdown("<h1>⚡ <span class='gradient-text'>LIVE ARENA QUIZIZZ ROOMS</span></h1>", unsafe_allow_html=True)
    
    custom_quizzes_db = db_get_all_custom_quizzes()
    list_custom_titles = [f"🌟 {q['title']} (by {q['creator']})" for q in custom_quizzes_db]
    pilihan_mapel_gabungan = list(BANK_SOAL_PRO.keys()) + list_custom_titles

    if not st.session_state.quizizz_aktif and not st.session_state.qz_selesai and not st.session_state.current_room_code:
        tab_solo, tab_join, tab_host, tab_create = st.tabs(["🎮 LATIHAN SOLO", "👥 GABUNG KAMAR", "👑 HOST KAMAR", "🛠️ PABRIK SOAL (BARU)"])
        
        with tab_solo:
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            mapel_solo = st.selectbox("🎯 Pilih Kuis:", pilihan_mapel_gabungan, key="solo_m")
            st.write("<br>", unsafe_allow_html=True)
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if st.button("🚀 MULAI LATIHAN SOLO", key="btn_solo"):
                if mapel_solo.startswith("🌟 "):
                    title_only = mapel_solo.replace("🌟 ", "").split(" (by ")[0]
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
                else: st.error("Soal di kuis ini terlalu sedikit!")
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        with tab_join:
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>🌐 LOBBY KAMAR MULTIPLAYER</h3>", unsafe_allow_html=True)
            c_ref, _ = st.columns([1, 3])
            with c_ref:
                if st.button("🔄 Refresh Daftar Kamar Server"): st.rerun()
            st.write("<br>", unsafe_allow_html=True)
            
            active_rooms = db_get_waiting_sessions()
            if active_rooms:
                for room in active_rooms:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.05); border:1px solid rgba(0, 198, 255, 0.4); border-radius:14px; padding:20px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center;'>
                        <div><h4 style='margin:0; color:#00C6FF; font-size:22px;'>📚 {room['mapel']}</h4><span style='font-size:14px; color:#94A3B8; font-weight:bold;'>Host: {room['host_username']} &nbsp;|&nbsp; PIN: {room['session_code']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🚪 GABUNG KAMAR INI", key=f"join_{room['session_code']}"):
                        db_join_session(room['session_code'], player)
                        st.session_state.current_room_code = room['session_code']
                        st.session_state.is_host = False
                        st.success("🎯 Berhasil masuk lobby!")
                        st.rerun()
                    st.write("<br>", unsafe_allow_html=True)
            else:
                st.info("📭 Server saat ini sepi. Belum ada kamar kuis yang dibuat.")
                
            st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
            st.caption("Atau masukkan PIN secara manual (untuk kamar Private):")
            kode_input = st.text_input("Ketik 6 Digit PIN Kamar:", max_chars=6, placeholder="Contoh: 849204").strip()
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🚪 MASUK VIA PIN", use_container_width=True):
                if kode_input:
                    room = db_get_quiz_session(kode_input)
                    if room:
                        if room["status"] == "finished": st.error("❌ Kamar kuis ini sudah selesai dilaksanakan!")
                        else:
                            db_join_session(kode_input, player)
                            st.session_state.current_room_code = kode_input
                            st.session_state.is_host = False
                            st.success("🎯 Berhasil masuk lobby!")
                            st.rerun()
                    else: st.error("❌ Kode Kamar tidak ditemukan di database cloud!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab_host:
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            st.markdown("<h3>👑 JADI HOST KAMAR BARU</h3>", unsafe_allow_html=True)
            mapel_guru = st.selectbox("🎯 Pilih Kuis Yang Akan Diujikan:", pilihan_mapel_gabungan, key="guru_m")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("👑 GENERATE ROOM PUBLIK", use_container_width=True):
                random_code = str(random.randint(100000, 999999))
                db_create_quiz_session(random_code, player, mapel_guru)
                st.session_state.current_room_code = random_code
                st.session_state.is_host = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_create:
            st.markdown("<div class='glass-card' style='text-align:left; border-color:#10B981;'>", unsafe_allow_html=True)
            st.markdown("<h3>🛠️ PABRIK KUIS KOMUNITAS</h3>", unsafe_allow_html=True)
            st.caption("Kuis yang kamu buat di sini akan permanen masuk ke dalam server dan bisa dipilih oleh semua orang sebagai arena bertarung!")
            
            judul_baru = st.text_input("📝 Berikan Judul Kuis Kamu (Contoh: Tebak Karakter Anime):").strip()
            
            st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
            for i, q in enumerate(st.session_state.temp_q):
                st.success(f"✅ Soal {i+1} Tersimpan: {q['soal']} (Kunci: {q['jawaban']})")
                
            with st.form("form_tambah_soal", clear_on_submit=True):
                st.markdown("#### ➕ Tambah Soal Baru")
                soal_text = st.text_area("Pertanyaan:", height=100)
                c1, c2 = st.columns(2)
                op_benar = c1.text_input("Opsi 1 (Ketik Jawaban BENAR di sini):", placeholder="Wajib jawaban benar")
                op_salah1 = c2.text_input("Opsi 2 (Pengecoh):")
                op_salah2 = c1.text_input("Opsi 3 (Pengecoh):")
                op_salah3 = c2.text_input("Opsi 4 (Pengecoh):")
                
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("SIMPAN SOAL INI KE DALAM DRAFT"):
                    if soal_text and op_benar and op_salah1 and op_salah2 and op_salah3:
                        st.session_state.temp_q.append({
                            "soal": soal_text,
                            "opsi": [op_benar, op_salah1, op_salah2, op_salah3],
                            "jawaban": op_benar
                        })
                        st.rerun()
                    else: st.warning("Harap isi semua opsi A, B, C, D!")
            
            st.write("<br>", unsafe_allow_html=True)
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if st.button("🚀 PUBLISH KUIS KE SERVER GLOBAL"):
                if not judul_baru: st.error("Judul Kuis tidak boleh kosong!")
                elif db_get_custom_quiz_by_title(judul_baru): st.error("Judul ini sudah dipakai orang lain! Pilih judul yang lebih unik.")
                elif len(st.session_state.temp_q) < 3: st.error("Minimal harus membuat 3 soal!")
                else:
                    db_save_custom_quiz(judul_baru, player, st.session_state.temp_q)
                    st.session_state.temp_q = []
                    # ANTI-LAG FIX: Paksa reset cache manual agar kuis baru langsung tampil tanpa nunggu 60 detik!
                    st.cache_data.clear()
                    st.success("🎉 Kuis Berhasil Diterbitkan ke Server Publik! Silakan cek di tab Host Kamar.")
                    time.sleep(1.5)
                    st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

    elif st.session_state.current_room_code and not st.session_state.quizizz_aktif and not st.session_state.qz_selesai:
        code = st.session_state.current_room_code
        room_info = db_get_quiz_session(code)
        players = db_get_session_players(code)
        
        st.markdown(f"<div class='glass-card' style='border-color:#00C6FF; padding:50px;'>", unsafe_allow_html=True)
        st.markdown(f"<h4>Kamar Kuis Aktif: <span style='color:#00C6FF;'>{room_info['mapel']}</span></h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:20px; color:#94A3B8; margin:0; margin-top:20px;'>KODE PIN KAMAR (UNTUK PRIVATE):</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size:90px; font-weight:900; color:#F59E0B; letter-spacing:10px; text-shadow:0 0 40px rgba(245,158,11,0.6); margin:10px 0;'>{code}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='margin-top:30px;'>👥 Pemain di Dalam Lobby ({len(players)} Orang)</h5>", unsafe_allow_html=True)
        
        if players:
            names = ", ".join([p["username"] for p in players])
            st.markdown(f"<div style='background:rgba(0,0,0,0.4); padding:20px; border-radius:15px; color:#10B981; font-weight:bold; font-size:18px; border:1px solid rgba(16,185,129,0.3);'>{names}</div>", unsafe_allow_html=True)
        else:
            st.caption("Menunggu petarung bergabung...")
            
        st.write("<br><br>", unsafe_allow_html=True)
        c_ref, c_act = st.columns(2)
        with c_ref:
            if st.button("🔄 SEGARKAN LOBBY"): st.rerun()
            
        with c_act:
            if st.session_state.is_host:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🚀 MULAI PERMAINAN KUIS (START)"):
                    if len(players) == 0: st.error("Minimal harus ada 1 pemain di lobby untuk memulai!")
                    else:
                        db_update_session_status(code, "active")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("⏱️ Harap tenang, kuis akan segera dimulai ketika Host menekan tombol Start.")
                if room_info["status"] == "active":
                    m_aktif = room_info["mapel"]
                    if m_aktif.startswith("🌟 "):
                        title_only = m_aktif.replace("🌟 ", "").split(" (by ")[0]
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
        if st.button("❌ KELUAR / BUBARKAN KAMAR", key="exit_rm"):
            if st.session_state.is_host: db_update_session_status(code, "finished")
            st.session_state.current_room_code = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.is_host and room_info["status"] == "active":
            st.write("<br><br>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:left;'>📈 LIVE REAL-TIME LEADERBOARD SISWA</h3>", unsafe_allow_html=True)
            for rank, p in enumerate(players):
                status_icon = "✅ Selesai" if p["status"] == "finished" else "⏳ Bertarung"
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(0,198,255,0.2); border-radius:12px; padding:15px 25px; margin-bottom:10px; display:flex; justify-content:space-between; font-size:18px;'>
                    <b>#{rank+1} {p['username']} <span style='font-size:14px; color:#94A3B8; margin-left:10px;'>({status_icon})</span></b>
                    <span style='color:#00C6FF; font-weight:900;'>⭐ {p['score']} Skor</span>
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.quizizz_aktif:
        idx = st.session_state.qz_index
        total_soal = len(st.session_state.qz_soal)
        
        progress_val = int((idx / total_soal) * 100)
        st.progress(progress_val)
        st.markdown(f"<div style='text-align:right; color:#00C6FF; font-weight:bold; font-size:18px; margin-top:10px;'>Pertanyaan {idx+1} dari {total_soal}</div>", unsafe_allow_html=True)
        
        soal_aktif = st.session_state.qz_soal[idx]
        opsi_acak = soal_aktif["opsi"].copy()
        random.shuffle(opsi_acak)
        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass-card' style='font-size:28px; font-weight:900; padding:60px 40px; border-color:#00C6FF; box-shadow:0 0 30px rgba(0,198,255,0.2);'>{soal_aktif['soal']}</div>br><br>", unsafe_allow_html=True)
        
        st.markdown("<div class='quiz-btn'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        st.write("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        
        def cek_jawaban(jawaban_dipilih):
            if jawaban_dipilih == soal_aktif["jawaban"]:
                st.session_state.qz_score += 20
                st.session_state.sfx = "benar" 
                st.toast("🔥 JAWABAN BENAR! Combo +20 Skor!", icon="✅")
            else:
                st.session_state.sfx = "salah" 
                st.toast(f"❌ SALAH! Kunci: {soal_aktif['jawaban']}", icon="💀")
            
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
        else: st.snow()
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; font-size:60px;'>🏁 <span class='gradient-text'>PERMAINAN SELESAI!</span></h1>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='score-card'><h3>Akurasi Jawaban Anda</h3><h1 style='color:#00C6FF; font-size:70px; margin:0; text-shadow:0 0 20px rgba(0,198,255,0.4);'>{akurasi}%</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='score-card'><h3>XP Permanen Didapatkan</h3><h1 style='color:#10B981; font-size:70px; margin:0; text-shadow:0 0 20px rgba(16,185,129,0.4);'>+{final_xp} XP</h1></div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
        if st.button("📥 AMANKAN XP DAN KEMBALI KE LOBBY UTAMA"):
            if final_xp > 0: db_update_points(player, points_db + final_xp)
            st.session_state.qz_selesai = False
            st.session_state.current_room_code = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: MODE DUEL PVP
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1>⚔️ <span class='gradient-text'>ARENA DUEL MULTIPLAYER CLOUD</span></h1>", unsafe_allow_html=True)
    st.caption("Pilih Mapel, temukan lawan acak di seluruh server, dan curi XP mereka dengan answering fast!")
    
    pool_pvp = {}
    for mp, data_kelas in BANK_SOAL_PRO.items():
        pool_pvp[mp] = []
        for kl, data_bab in data_kelas.items():
            for bb, data_sub in data_bab.items():
                for sub, list_soal in data_sub.items():
                    pool_pvp[mp].extend(list_soal)
                
    if not pool_pvp:
        st.warning("⚠️ Bank soal PvP belum diaktifkan oleh Admin.")
        st.stop()
        
    col_mapel, col_btn = st.columns([3,1])
    with col_mapel: mapel_duel = st.selectbox("🎯 Pilih Arena Mata Pelajaran:", list(pool_pvp.keys()))
    
    if "lawan_duel" not in st.session_state: st.session_state.lawan_duel = None
    if "kuis_duel" not in st.session_state: st.session_state.kuis_duel = False
    if "soal_pvp_aktif" not in st.session_state: st.session_state.soal_pvp_aktif = None
    
    with col_btn:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🔍 CARI LAWAN SEPADAN"):
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
            else: st.error("Tidak ada lawan online saat ini.")
            
    if st.session_state.lawan_duel and st.session_state.kuis_duel and st.session_state.soal_pvp_aktif:
        l_user, l_nama, l_pts = st.session_state.lawan_duel
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 40px 0;'>", unsafe_allow_html=True)
        
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='glass-card' style='border-color:#00C6FF;'><h2 style='color:#00C6FF; margin:0; font-size:35px;'>{display_name_db}</h2><p style='font-size:20px; font-weight:bold;'>⭐ {points_db} XP</p></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div style='text-align:center; margin-top:20px;'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='glass-card' style='border-color:#FF416C;'><h2 style='color:#FF416C; margin:0; font-size:35px;'>{l_nama}</h2><p style='font-size:20px; font-weight:bold;'>⭐ {l_pts} XP</p></div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left; padding:40px;'>", unsafe_allow_html=True)
        ds = st.session_state.soal_pvp_aktif
        st.markdown(f"<h3 style='font-size:26px; font-weight:900;'>{ds['soal']}</h3>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        j_user = st.radio("Pilih Serangan Taktismu:", ds['opsi'], key="duel_ans")
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("⚡ EKSEKUSI SERANGAN CLOUD"):
            if j_user == ds['jawaban']:
                db_update_pvp_win(player, l_user, points_db, l_pts)
                st.session_state.sfx = "benar" 
                st.toast("CRITICAL STRIKE! Serangan masuk!", icon="⚔️")
                st.session_state.kuis_duel = False 
                st.success(f"🎉 **KAMU MENANG!** +100 XP ditambahkan ke database. {l_nama} kehilangan 20 XP.")
            else:
                db_update_pvp_lose(player, points_db)
                st.session_state.sfx = "salah" 
                st.toast("BLOCKED! Pertahanan lawan terlalu kuat.", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"💀 **KAMU KALAH!** Jawaban salah. Kamu kehilangan 30 XP.")
            
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🔄 Segarkan Data Server"): st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 4: RUANG BELAJAR & MODUL (LOCAL SYSTEM)
# ==========================================
elif menu == "📖 Ruang Belajar & Modul":
    st.markdown("<h1>📖 <span class='gradient-text'>RUANG MATERI INTERAKTIF</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 30px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("📚 Pilih Mata Pelajaran:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("🎓 Pilih Kelas:", kelas_list if kelas_list else ["-"])
        
        st.write("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("📑 Sektor Bab Utama:", bab_list if bab_list else ["-"])
        sub_list = DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).get(p_bab, {}).get("sub_bab", ["-"])
        with col4: p_sub = st.selectbox("🔖 Fokus Sub-bab:", sub_list)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br><br>", unsafe_allow_html=True)
    tab_mat, tab_doc = st.tabs(["📌 Rangkuman & Catatan Ekstra", "📂 Modul Interaktif Lokal"])
    
    with tab_mat:
        try: st.markdown(f"<div class='glass-card' style='text-align:left; line-height:2; font-size:18px;'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Catatan rangkuman belum ditambahkan oleh Admin.")

    with tab_doc:
        st.markdown("### 📁 Arsip Dokumen Lokal")
        st.caption("Materi PDF/Gambar yang diunggah Admin akan muncul di sini.")
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
                        st.download_button(label=f"⬇️ UNDUH DOKUMEN: {f}", data=file.read(), file_name=f, mime="application/octet-stream")
        else:
            st.info("📭 Admin belum menyuntikkan dokumen pendukung lokal untuk materi ini.")

# ==========================================
# HALAMAN 5: TOKO GELAR (BLACK MARKET)
# ==========================================
elif menu == "🛒 Black Market Profil":
    st.markdown("<h1>🛒 <span class='gradient-text'>BLACK MARKET PROFIL</span></h1>", unsafe_allow_html=True)
    
    tab_av, tab_gl, tab_edit = st.tabs(["👤 Kostum Avatar Default", "👑 Bursa Gelar Elit", "⚙️ Edit Profil Pribadi (KUSTOM)"])
    
    with tab_av:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("TERAPKAN: GENI US"):
                db_update_profile(player, display_name_db, custom_avatar="")
                db_update_avatar(player, "Geni Us")
                st.toast("Proses Klona Berhasil!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("TERAPKAN: SMAR T"):
                db_update_profile(player, display_name_db, custom_avatar="")
                db_update_avatar(player, "Smar T")
                st.toast("Proses Klona Berhasil!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left;'><h3>Tukar XP dengan Kehormatan</h3>", unsafe_allow_html=True)
        st.write(f"Saldo XP Kamu Saat Ini: ⭐ **{points_db} XP**")
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
        for gelar, harga in DAFTAR_GELAR.items():
            cg1, cg2, cg3 = st.columns([3, 1, 1])
            cg1.markdown(f"<h4 style='font-size:22px;'>{gelar}</h4>", unsafe_allow_html=True)
            cg2.markdown(f"<p style='color:#F59E0B; font-weight:900; font-size:22px;'>💰 {harga} XP</p>", unsafe_allow_html=True)
            with cg3:
                if title_db == gelar: st.button("✅ Sedang Dipakai", key=f"ak_{gelar}", disabled=True)
                else:
                    if st.button("Tukar & Pakai", key=f"by_{gelar}"):
                        if points_db >= harga:
                            db_update_title(player, gelar, cost=harga)
                            st.toast(f"Status diperbarui menjadi {gelar}!", icon="👑"); st.rerun()
                        else: st.error("XP Tidak Cukup!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_edit:
        st.markdown("<div class='glass-card' style='text-align:left; border-color:#00C6FF;'>", unsafe_allow_html=True)
        st.markdown("<h3>⚙️ Kustomisasi Identitas Bebas</h3>", unsafe_allow_html=True)
        st.caption("Ubah nama dan foto profil aslimu di sini. Tenang saja, Username asli, XP, dan Gelar-mu tidak akan hilang!")
        st.write("<br>", unsafe_allow_html=True)
        
        new_display = st.text_input("Ganti Nama Tampilan (Display Name):", value=display_name_db, max_chars=20)
        st.write("<br>", unsafe_allow_html=True)
        new_foto = st.file_uploader("Unggah Foto Profil (Akan dikompres otomatis anti-lag):", type=['png', 'jpg', 'jpeg'])
        
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
        if st.button("💾 SIMPAN PERUBAHAN PROFIL"):
            b64_foto = custom_avatar_db 
            
            if new_foto:
                try:
                    img = Image.open(new_foto)
                    img = img.convert("RGB") 
                    # ANTI-LAG FIX: Konversi foto dipangkas ke 150x150 & quality 65 agar string Base64 super ringan di Cloud
                    img.thumbnail((150, 150))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=65)
                    b64_foto = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
                except Exception as e:
                    st.error(f"Gagal memproses gambar: {e}")
            
            db_update_profile(player, new_display, b64_foto)
            st.toast("Identitas berhasil diperbarui ke server global!", icon="✅")
            time.sleep(1)
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 6: KONSOL ADMIN & PUSAT ANALITIK
# ==========================================
elif menu == "⚙️ Konsol Super Admin":
    st.markdown("<h1>⚙️ <span class='gradient-text'>SERVER COMMAND CENTER</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='border-color:#EF4444;'><h2>🔒 GATEWAY KEAMANAN TINGKAT TINGGI</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukkan Master Key Enkripsi:", type="password")
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("Buka Akses Root"):
            if pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
            else: st.error("Akses Ditolak!")
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.success("🔓 Akses Server Master Terbuka.")
        tab_stat, tab_db, tab_upload = st.tabs(["📈 Analitik Pendidikan", "👥 Database Pengguna", "📤 Unggah File Lokal"])
        
        users_admin = db_get_all_users_admin()
        df = pd.DataFrame(users_admin) if users_admin else pd.DataFrame()
        
        with tab_stat:
            st.markdown("### 📈 Visualisasi Data Performa Siswa")
            if not df.empty:
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Siswa", f"{len(df)} Ksatria")
                c2.metric("Ekonomi XP Beredar", f"{df['points'].sum()} XP")
                c3.metric("Rata-rata XP", f"{int(df['points'].mean())} XP")
                
                st.write("<br>", unsafe_allow_html=True)
                st.markdown("<div class='glass-card'><h4>Distribusi Kekayaan XP Siswa</h4>", unsafe_allow_html=True)
                chart_data = df.set_index("username")["points"]
                st.bar_chart(chart_data, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.info("Visualisasi belum tersedia.")
            
        with tab_db:
            if not df.empty:
                df_view = df[["username", "title", "points", "streak"]]
                df_view.columns = ["Username", "Gelar/Tier", "Kekayaan XP", "Hari Aktif"]
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            
        with tab_upload:
            st.markdown("### 📤 Distribusi Materi Lokal")
            c1, c2 = st.columns(2)
            with c1: up_mapel = st.selectbox("📚 Target Mapel:", list(DATA_MATERI.keys()), key="adm_m")
            k_list = list(DATA_MATERI.get(up_mapel, {}).keys())
            with c2: up_kelas = st.selectbox("🎓 Target Kelas:", k_list if k_list else ["-"], key="adm_k")
            
            c3, c4 = st.columns(2)
            b_list = list(DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).keys())
            with c3: up_bab = st.selectbox("📑 Target Bab:", b_list if b_list else ["-"], key="adm_b")
            s_list = DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).get(up_bab, {}).get("sub_bab", ["-"])
            with c4: up_sub = st.selectbox("🔖 Target Sub-bab:", s_list, key="adm_s")
            
            st.write("<br>", unsafe_allow_html=True)
            up_file = st.file_uploader("📂 Pilih File Materi:")
            st.write("<br>", unsafe_allow_html=True)
            
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if up_file and st.button("🚀 UNGGAH KE SERVER LOKAL"):
                try:
                    folder_t = os.path.join("uploads", bersihkan_nama(up_mapel), bersihkan_nama(up_kelas), bersihkan_nama(up_bab), bersihkan_nama(up_sub))
                    os.makedirs(folder_t, exist_ok=True)
                    with open(os.path.join(folder_t, up_file.name), "wb") as f: f.write(up_file.getbuffer())
                    st.success("✅ File berhasil disimpan!")
                except Exception as e: st.error(f"❌ Gagal: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("🔴 TUTUP & KUNCI KONSOL"): st.session_state.is_admin = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
