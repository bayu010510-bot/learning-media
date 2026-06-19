import streamlit as st
import pandas as pd
import os
import re
import base64
import random
import hashlib
import requests

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA SPEKTAKULER
# ==========================================
st.set_page_config(page_title="Learning Media | Edisi Spektakuler", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0B0F19; background-image: radial-gradient(circle at 50% 0%, #172136 0%, #0B0F19 100%); color: #F8FAFC; }
    h1, h2, h3, h4, h5, p, span, label { color: #F8FAFC !important; }
    
    /* Efek Teks Spesial */
    .gradient-text { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .vs-text { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 50px; }
    
    /* Input & Glassmorphism Card */
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(0, 198, 255, 0.4) !important; border-radius: 10px; }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span { color: #00C6FF !important; -webkit-text-fill-color: #00C6FF !important; font-weight: bold; font-size: 16px; }
    .glass-card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 30px; text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s; }
    .glass-card:hover { transform: translateY(-5px); border-color: rgba(0, 198, 255, 0.4); box-shadow: 0 0 30px rgba(0, 198, 255, 0.2); }
    .score-card { background: linear-gradient(135deg, rgba(0, 198, 255, 0.1) 0%, rgba(0, 114, 255, 0.1) 100%); border: 1px solid #00C6FF; border-radius: 15px; padding: 20px; text-align: center; }
    
    /* Tombol Interaktif Tingkat Tinggi */
    .stButton>button { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; width: 100%; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4); transition: all 0.3s ease; }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 0 25px rgba(0, 198, 255, 0.7); }
    .btn-red>button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); }
    .btn-red>button:hover { box-shadow: 0 0 25px rgba(255, 75, 43, 0.8); }
    .btn-green>button { background: linear-gradient(135deg, #10B981 0%, #047857 100%); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }
    .btn-green>button:hover { box-shadow: 0 0 25px rgba(16, 185, 129, 0.8); }
    
    div[data-testid="stMetricValue"] { color: #00C6FF !important; font-size: 35px !important; font-weight: 900 !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI MESIN CLOUD (SUPABASE & GOOGLE)
# ==========================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"].strip()
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()
    HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}
except Exception:
    st.error("🚨 Kunci Supabase belum disetel di Streamlit Secrets!")
    st.stop()

# Menghidupkan Robot Google Drive
try:
    import json
    import io
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    
    DRIVE_FOLDER_ID = st.secrets["GOOGLE_DRIVE_FOLDER_ID"].strip()
    creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    GOOGLE_READY = True
except Exception as e:
    GOOGLE_READY = False
    st.sidebar.warning(f"⚠️ Robot Drive Tertidur: {e}")

def upload_to_drive(file_buffer, file_name, mime_type):
    media = MediaIoBaseUpload(io.BytesIO(file_buffer), mimetype=mime_type, resumable=True)
    file_metadata = {'name': file_name, 'parents': [DRIVE_FOLDER_ID]}
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    drive_service.permissions().create(fileId=file.get('id'), body={'type': 'anyone', 'role': 'reader'}).execute()
    return file.get('webViewLink')

# ==========================================
# 3. FUNGSI DATABASE ANTI-CRASH
# ==========================================
def db_get_user(username):
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?username=ilike.{username}", headers=HEADERS).json()
        return res[0] if isinstance(res, list) and len(res) > 0 else None
    except: return None

def db_create_user(username, hashed_pwd):
    data = {"username": username, "password": hashed_pwd, "avatar_name": "Geni Us", "title": "🏅 Pemula", "points": 0, "streak": 1}
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

def db_get_learned_history(username):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/kuis_history_cloud?username=eq.{username}", headers=HEADERS).json()
    return set([row["id_kuis"] for row in res]) if isinstance(res, list) else set()

def db_add_kuis_history(username, id_kuis):
    requests.post(f"{SUPABASE_URL}/rest/v1/kuis_history_cloud", headers=HEADERS, json={"username": username, "id_kuis": id_kuis})

def db_get_leaderboard():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,points,title&order=points.desc&limit=5", headers=HEADERS).json()
    return res if isinstance(res, list) else []

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

def db_save_materi(mapel, kelas, bab, sub_bab, file_name, drive_link):
    data = {"mapel": mapel, "kelas": kelas, "bab": bab, "sub_bab": sub_bab, "file_name": file_name, "drive_link": drive_link}
    requests.post(f"{SUPABASE_URL}/rest/v1/materi_cloud", headers=HEADERS, json=data)

def db_get_materi(mapel, kelas, bab, sub_bab):
    url = f"{SUPABASE_URL}/rest/v1/materi_cloud?mapel=eq.{mapel}&kelas=eq.{kelas}&bab=eq.{bab}&sub_bab=eq.{sub_bab}"
    res = requests.get(url, headers=HEADERS).json()
    return res if isinstance(res, list) else []

# ==========================================
# 4. INISIALISASI SESSION & UTILITAS
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "gacha_claimed" not in st.session_state: st.session_state.gacha_claimed = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "drill_aktif" not in st.session_state: st.session_state.drill_aktif = False
if "hasil_drill" not in st.session_state: st.session_state.hasil_drill = None

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

def tampilkan_avatar(keyword, ukuran="130px"):
    st.markdown(f"<div style='text-align:center; font-size:80px; animation: float 3s ease-in-out infinite;'>{'👨‍🎓' if keyword=='genius' else '👩‍🎓'}</div>", unsafe_allow_html=True)

# ==========================================
# 5. PORTAL LOGIN / REGISTER CLOUD
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; margin-top:50px; font-size:50px;'>Learning Media <span class='gradient-text'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:40px;'>Sistem Edukasi Terpadu Berbasis Cloud & AI.</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
    with col_form:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 MASUK", "📝 DAFTAR"])
        
        with tab_log:
            l_user = st.text_input("Username Ksatria:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            if st.button("🚀 LOGIN SEKARANG"):
                if l_user and l_pass:
                    user_record = db_get_user(l_user)
                    if user_record and user_record.get("password") == hash_password(l_pass):
                        st.session_state.username = user_record["username"] 
                        st.session_state.logged_in = True; st.rerun()
                    else: st.error("❌ Username atau Sandi salah/tidak ditemukan!")
                else: st.warning("Isi semua kolom!")
                
        with tab_reg:
            r_user = st.text_input("Username Baru (Maks 15 Huruf):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Sandi Baru:", type="password", key="r_pwd").strip()
            if st.button("✨ DAFTAR AKUN CLOUD"):
                if r_user and r_pass:
                    if db_get_user(r_user): st.error("⚠️ Username sudah ada yang punya!")
                    else:
                        db_create_user(r_user, hash_password(r_pass))
                        st.success("🎉 Akun berhasil diukir di Server! Silakan Login.")
                else: st.warning("Isi semua kolom!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 6. MEMUAT DATA PEMAIN AKTIF
# ==========================================
player = st.session_state.username
user_data = db_get_user(player)

if not user_data:
    st.session_state.logged_in = False; st.rerun()

avatar_db = user_data.get("avatar_name", "Geni Us")
title_db = user_data.get("title", "🏅 Pemula")
points_db = user_data.get("points", 0)
streak_db = user_data.get("streak", 1)

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
    tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
    st.markdown(f"<h2 style='text-align:center; margin-top:10px; margin-bottom:0;' class='gradient-text'>{player}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-top:5px;'><span style='background:rgba(0,198,255,0.1); color:#00C6FF; padding:4px 15px; border-radius:20px; font-weight:bold; border:1px solid #00C6FF;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-top:10px;'><span style='background:{tier_color}30; color:{tier_color}; padding:4px 15px; border-radius:20px; font-weight:bold; border:1px solid {tier_color};'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    prog = points_db % 100
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border-radius: 10px; height: 10px; margin: 20px 0; border: 1px solid rgba(255,255,255,0.1);'>
            <div style='background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%); width: {prog}%; height: 100%; border-radius: 10px; box-shadow: 0 0 15px #00C6FF;'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-weight:bold; color:#94A3B8; font-size:14px;'>
            <span>Lvl {user_level}</span><span style='color:#00C6FF;'>⭐ {points_db} XP</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    menu = st.radio("NAVIGASI SISTEM", ["🏠 Beranda Pusat", "⚔️ Mode Duel Ranked (PvP)", "📖 Arena Drill & Materi", "🛒 Black Market Profil", "⚙️ Konsol Super Admin"])
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT PROTOKOL"):
        st.session_state.logged_in = False; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 1: BERANDA PUSAT (DENGAN GACHA)
# ==========================================
if menu == "🏠 Beranda Pusat":
    st.markdown(f"<h1>SELAMAT DATANG, <span class='gradient-text'>{player.upper()}</span>! 🚀</h1>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='border-color:#F59E0B; background:rgba(245, 158, 11, 0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FCD34D; margin-top:0;'>🎁 Peti Harta Karun Harian Tersedia!</h2>", unsafe_allow_html=True)
        if st.button("🗝️ BUKA PETI & KLAIM XP"):
            bonus = random.choice([20, 50, 100, 150])
            db_update_points(player, points_db + bonus)
            st.session_state.gacha_claimed = True
            st.toast(f"JACKPOT! Kamu mendapat +{bonus} XP!", icon="🎉")
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h2 style='margin:0;'>{streak_db} Hari</h2><p style='color:#94A3B8; margin:0;'>Login Beruntun</p></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h2 style='margin:0;'>{len(learned_db)}</h2><p style='color:#94A3B8; margin:0;'>Misi Drill Diselesaikan</p></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:40px;'>🏆</div><h2 style='color:{tier_color}; margin:0;'>{tier_name.split()[1]}</h2><p style='color:#94A3B8; margin:0;'>Kasta Pemain</p></div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3>📊 PAPAN PERINGKAT GLOBAL (REAL-TIME CLOUD)</h3>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    for i, row in enumerate(ranking_data):
        medali = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        bg_color = "rgba(255, 215, 0, 0.1)" if i==0 else "rgba(255,255,255,0.02)"
        bdr_color = "rgba(255, 215, 0, 0.5)" if i==0 else "rgba(255,255,255,0.08)"
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid {bdr_color}; border-radius: 15px; padding: 15px 25px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>
            <h3 style='margin:0;'>{medali} {row.get("username", "Ksatria Anonim")} <span style='font-size:14px; font-weight:normal; color:#94A3B8;'>({row.get("title", "")})</span></h3>
            <h3 style='margin:0; color:#00C6FF;'>⭐ {row.get("points", 0)} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: MODE DUEL PVP (CURI XP)
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1>⚔️ <span class='gradient-text'>ARENA DUEL MULTIPLAYER CLOUD</span></h1>", unsafe_allow_html=True)
    st.caption("Pilih Mapel, temukan lawan acak di seluruh server, dan curi XP mereka dengan menjawab cepat!")
    
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
                st.session_state.lawan_duel = (lawan["username"], lawan.get("points", 0))
                st.session_state.kuis_duel = True
                soal_asli = random.choice(pool_pvp[mapel_duel])
                opsi_acak = soal_asli["opsi"].copy()
                random.shuffle(opsi_acak)
                st.session_state.soal_pvp_aktif = {"soal": soal_asli["soal"], "opsi": opsi_acak, "jawaban": soal_asli["jawaban"]}
            else: st.error("Tidak ada lawan online saat ini.")
            
    if st.session_state.lawan_duel and st.session_state.kuis_duel and st.session_state.soal_pvp_aktif:
        l_nama, l_pts = st.session_state.lawan_duel
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='glass-card' style='border-color:#00C6FF;'><h2 style='color:#00C6FF; margin:0;'>{player}</h2><p>⭐ {points_db} XP</p></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div style='text-align:center; margin-top:20px;'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='glass-card' style='border-color:#FF416C;'><h2 style='color:#FF416C; margin:0;'>{l_nama}</h2><p>⭐ {l_pts} XP</p></div>", unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
        ds = st.session_state.soal_pvp_aktif
        st.write(ds['soal'])
        j_user = st.radio("Pilih Serangan Taktismu:", ds['opsi'], key="duel_ans")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ EKSEKUSI SERANGAN CLOUD"):
            if j_user == ds['jawaban']:
                db_update_pvp_win(player, l_nama, points_db, l_pts)
                st.toast("CRITICAL STRIKE! Serangan masuk!", icon="⚔️")
                st.session_state.kuis_duel = False 
                st.success(f"🎉 **KAMU MENANG!** +100 XP ditambahkan ke database. {l_nama} kehilangan 20 XP.")
            else:
                db_update_pvp_lose(player, points_db)
                st.toast("BLOCKED! Pertahanan lawan terlalu kuat.", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"💀 **KAMU KALAH!** Jawaban salah. Kamu kehilangan 30 XP.")
            if st.button("🔄 Segarkan Data"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: ARENA DRILL & MATERI CERDAS
# ==========================================
elif menu == "📖 Arena Drill & Materi":
    st.markdown("<h1>📖 <span class='gradient-text'>PUSAT MATERI & EVALUASI</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 20px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("📚 Pilih Mata Pelajaran:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("🎓 Pilih Kelas:", kelas_list if kelas_list else ["-"])
        
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("📑 Sektor Bab Utama:", bab_list if bab_list else ["-"])
        sub_list = DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).get(p_bab, {}).get("sub_bab", ["-"])
        with col4: p_sub = st.selectbox("🔖 Fokus Sub-bab:", sub_list)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    tab_mat, tab_doc, tab_drill = st.tabs(["📌 Rangkuman Ekstra", "📂 Berkas Guru (G-Drive)", "⚔️ Uji Evaluasi (Drill)"])
    
    with tab_mat:
        try: st.markdown(f"<div class='glass-card' style='text-align:left;'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Catatan rangkuman belum ditambahkan oleh Admin.")

    with tab_doc:
        st.markdown("### ☁️ Arsip Dokumen Google Drive Aktif")
        materi_cloud = db_get_materi(p_mapel, p_kelas, p_bab, p_sub)
        
        if materi_cloud:
            for item in materi_cloud:
                st.markdown(f"""
                <div style='background:rgba(15,23,42,0.8); border:1px solid #00C6FF; padding:15px; border-radius:10px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;'>
                    <h4 style='margin:0; color:#F8FAFC;'>📄 {item['file_name']}</h4>
                    <a href="{item['drive_link']}" target="_blank" style='background:#00C6FF; color:#0B0F19; padding:8px 15px; border-radius:8px; text-decoration:none; font-weight:bold;'>🔗 BUKA DOKUMEN</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 Belum ada dokumen PDF/PPT yang diunggah Admin untuk sub-bab ini.")

    with tab_drill:
        st.markdown("### 🎯 Simulasi Soal HOTS (Diacak)")
        soal_tersedia = []
        try: soal_tersedia = BANK_SOAL_PRO[p_mapel][p_kelas][p_bab][p_sub]
        except KeyError: pass
        
        if not soal_tersedia:
            st.info("📭 Admin belum menyuntikkan soal evaluasi di sektor ini.")
        else:
            if not st.session_state.drill_aktif and not st.session_state.hasil_drill:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🚀 MULAI GENERASI SOAL EVALUASI"):
                    jml_soal = min(5, len(soal_tersedia))
                    soal_terpilih = random.sample(soal_tersedia, jml_soal)
                    data_sesi = []
                    for s in soal_terpilih:
                        opsi_acak = s["opsi"].copy()
                        random.shuffle(opsi_acak)
                        data_sesi.append({"soal": s["soal"], "opsi_acak": opsi_acak, "jawaban_asli": s["jawaban"], "pembahasan": s["pem"]})
                    st.session_state.soal_drill_saat_ini = data_sesi
                    st.session_state.drill_aktif = True
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            elif st.session_state.drill_aktif:
                st.progress(100)
                with st.form(key="form_drill"):
                    jawaban_user = []
                    for i, s in enumerate(st.session_state.soal_drill_saat_ini):
                        st.markdown(f"<div class='glass-card' style='text-align:left; padding:20px; margin-bottom:15px; border-left:4px solid #00C6FF;'>", unsafe_allow_html=True)
                        st.markdown(f"**Pertanyaan {i+1}:**<br>{s['soal']}", unsafe_allow_html=True)
                        ans = st.radio(f"Pilih jawaban akurat:", s['opsi_acak'], key=f"d_ans_{i}", label_visibility="collapsed")
                        jawaban_user.append(ans)
                        st.markdown("</div>", unsafe_allow_html=True)
                    submit_drill = st.form_submit_button("📝 KUMPULKAN & KOREKSI OTOMATIS")
                    
                if submit_drill:
                    skor_benar = 0
                    eval_data = []
                    for i, s in enumerate(st.session_state.soal_drill_saat_ini):
                        j_user = jawaban_user[i]
                        j_asli = s['jawaban_asli']
                        benar = (j_user == j_asli)
                        if benar: skor_benar += 1
                        eval_data.append({"soal": s['soal'], "jawaban_anda": j_user, "jawaban_benar": j_asli, "pem": s['pembahasan'], "is_correct": benar})
                    st.session_state.hasil_drill = {"skor_benar": skor_benar, "total": len(st.session_state.soal_drill_saat_ini), "evaluasi": eval_data}
                    st.session_state.drill_aktif = False
                    st.rerun()
            
            elif st.session_state.hasil_drill:
                hasil = st.session_state.hasil_drill
                skor, tot = hasil["skor_benar"], hasil["total"]
                xp_gained = skor * 30
                akurasi = int((skor / tot) * 100)
                
                st.markdown("### 📊 DASHBOARD METRIK EVALUASI")
                c_met1, c_met2, c_met3 = st.columns(3)
                with c_met1: st.markdown(f"<div class='score-card'><h4>🎯 Akurasi</h4><h1 style='color:#00C6FF; margin:0;'>{akurasi}%</h1></div>", unsafe_allow_html=True)
                with c_met2: st.markdown(f"<div class='score-card'><h4>✅ Benar</h4><h1 style='color:#10B981; margin:0;'>{skor}/{tot}</h1></div>", unsafe_allow_html=True)
                with c_met3: st.markdown(f"<div class='score-card'><h4>⚡ XP Didapat</h4><h1 style='color:#F59E0B; margin:0;'>+{xp_gained}</h1></div>", unsafe_allow_html=True)
                
                if xp_gained > 0:
                    db_update_points(player, points_db + xp_gained)
                    id_drill = f"drill_{p_mapel}_{p_kelas}_{p_bab}_{p_sub}"
                    if akurasi == 100 and id_drill not in learned_db:
                        db_add_kuis_history(player, id_drill)
                    st.toast(f"Sinkronisasi Cloud Selesai! XP diamankan.", icon="🏆")
                
                st.write("<br>", unsafe_allow_html=True)
                for i, ev in enumerate(hasil["evaluasi"]):
                    ikon, warna = ("✅", "#10B981") if ev["is_correct"] else ("❌", "#EF4444")
                    with st.expander(f"{ikon} Analisis Soal {i+1} | Kunci: {ev['jawaban_benar']}"):
                        st.write(ev['soal'])
                        st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; border-left:3px solid {warna};'><b>🧠 Pembahasan Master:</b><br>{ev['pem']}</div>", unsafe_allow_html=True)
                
                st.write("<br>", unsafe_allow_html=True)
                if st.button("🔄 Akhiri Sesi Evaluasi"):
                    st.session_state.hasil_drill = None
                    st.rerun()

# ==========================================
# HALAMAN 4: TOKO GELAR (BLACK MARKET)
# ==========================================
elif menu == "🛒 Black Market Profil":
    st.markdown("<h1>🛒 <span class='gradient-text'>BLACK MARKET PROFIL</span></h1>", unsafe_allow_html=True)
    tab_av, tab_gl = st.tabs(["👤 Kostum Avatar", "👑 Bursa Gelar Elit"])
    
    with tab_av:
        st.caption("Pilih entitas ksatria yang merepresentasikan gayamu.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("TERAPKAN: GENI US"):
                db_update_avatar(player, "Geni Us")
                st.toast("Proses Klona Berhasil!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            st.write("<br>", unsafe_allow_html=True)
            if st.button("TERAPKAN: SMAR T"):
                db_update_avatar(player, "Smar T")
                st.toast("Proses Klona Berhasil!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left;'><h3>Tukar XP dengan Kehormatan</h3>", unsafe_allow_html=True)
        st.write(f"Saldo XP Kamu Saat Ini: ⭐ **{points_db} XP**")
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        for gelar, harga in DAFTAR_GELAR.items():
            cg1, cg2, cg3 = st.columns([3, 1, 1])
            cg1.markdown(f"#### {gelar}")
            cg2.markdown(f"<p style='color:#F59E0B; font-weight:bold; font-size:18px;'>💰 {harga} XP</p>", unsafe_allow_html=True)
            with cg3:
                if title_db == gelar: st.button("✅ Aktif Dipakai", key=f"ak_{gelar}", disabled=True)
                else:
                    if st.button("Tukar & Pakai", key=f"by_{gelar}"):
                        if points_db >= harga:
                            db_update_title(player, gelar, cost=harga)
                            st.toast(f"Status diperbarui menjadi {gelar}!", icon="👑"); st.rerun()
                        else: st.error("XP Tidak Cukup!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 5: KONSOL ADMIN (DENGAN DRIVE UPLOAD)
# ==========================================
elif menu == "⚙️ Konsol Super Admin":
    st.markdown("<h1>⚙️ <span class='gradient-text'>SERVER COMMAND CENTER</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='border-color:#EF4444;'><h2>🔒 GATEWAY KEAMANAN TINGKAT 5</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Masukkan Master Key:", type="password")
        if st.button("Buka Enkripsi"):
            if pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
            else: st.error("Akses Ditolak. Alarm Keamanan Aktif!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("🔓 Akses Server Master Terbuka. Selamat Bekerja.")
        tab_stat, tab_db, tab_drive = st.tabs(["📊 Analitik Cloud", "👥 Database Pengguna", "☁️ Integrasi Google Drive"])
        
        users_admin = db_get_all_users_admin()
        
        with tab_stat:
            total_akun = len(users_admin)
            total_xp = sum([r.get("points", 0) for r in users_admin])
            max_streak = max([r.get("streak", 0) for r in users_admin]) if users_admin else 0
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Siswa", f"{total_akun} Ksatria")
            c2.metric("Ekonomi XP Berjalan", f"{total_xp} XP")
            c3.metric("Rekor Log Aktif", f"{max_streak} Hari")
            
        with tab_db:
            st.caption("Memantau langsung pergerakan XP dan pertumbuhan siswa di tabel Supabase.")
            if users_admin:
                df = pd.DataFrame(users_admin)
                df = df[["username", "title", "points", "streak"]]
                df.columns = ["Username", "Gelar/Tier", "Kekayaan XP", "Hari Aktif"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("Belum ada siswa yang mendaftar.")
            
        with tab_drive:
            st.markdown("### 📤 Suntik Materi ke Google Drive")
            st.caption("Sistem Robot (Service Account) akan secara otomatis memindahkan file yang di-upload di sini langsung ke Google Drive dan mencatat URL-nya ke dalam Supabase untuk diakses siswa.")
            
            c1, c2 = st.columns(2)
            with c1: up_mapel = st.selectbox("📚 Target Mata Pelajaran:", list(DATA_MATERI.keys()), key="adm_m")
            k_list = list(DATA_MATERI.get(up_mapel, {}).keys())
            with c2: up_kelas = st.selectbox("🎓 Target Kelas:", k_list if k_list else ["-"], key="adm_k")
            
            c3, c4 = st.columns(2)
            b_list = list(DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).keys())
            with c3: up_bab = st.selectbox("📑 Target Bab:", b_list if b_list else ["-"], key="adm_b")
            s_list = DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).get(up_bab, {}).get("sub_bab", ["-"])
            with c4: up_sub = st.selectbox("🔖 Target Sub-bab:", s_list, key="adm_s")
            
            st.write("<br>", unsafe_allow_html=True)
            up_file = st.file_uploader("📂 Pilih File Materi (Mendukung segala format dokumen/gambar):")
            
            if up_file:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🚀 UNGGAH KE CLOUD DRIVE SEKARANG"):
                    if not GOOGLE_READY:
                        st.error("🚨 Sinyal ke Google Terputus: Pastikan 'GCP_CREDENTIALS' di Secrets tersetting dengan format yang benar.")
                    else:
                        with st.spinner('Meretas jalan masuk ke Google Drive... Mohon tunggu.'):
                            try:
                                file_buffer = up_file.getvalue()
                                # Eksekusi Robot Google
                                link_publik = upload_to_drive(file_buffer, up_file.name, up_file.type)
                                # Eksekusi Catat ke Supabase
                                db_save_materi(up_mapel, up_kelas, up_bab, up_sub, up_file.name, link_publik)
                                
                                st.success(f"✅ Operasi Berhasil! Berkas resmi tayang di server.\n\nLink Akses: {link_publik}")
                            except Exception as e:
                                st.error(f"❌ Terjadi kesalahan injeksi data: {e}")
                st.markdown("</div>", unsafe_allow_html=True)

        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("🔴 TUTUP DAN KUNCI KONSOL ADMIN"): st.session_state.is_admin = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
