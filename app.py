import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
import base64
import random
import hashlib
import requests

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media | Edisi Cloud Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- KONEKSI GLOBAL SUPABASE (API REST) ---
SUPABASE_URL = st.secrets["SUPABASE_URL"].strip()
SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- KONEKSI ROBOT GOOGLE DRIVE ---
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
    st.error(f"🚨 Sistem Google Drive Belum Siap: {e}")

# --- FUNGSI UPLOAD GOOGLE DRIVE ---
def upload_to_drive(file_buffer, file_name, mime_type):
    # 1. Menembak file ke Google Drive
    media = MediaIoBaseUpload(io.BytesIO(file_buffer), mimetype=mime_type, resumable=True)
    file_metadata = {'name': file_name, 'parents': [DRIVE_FOLDER_ID]}
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    
    # 2. Membuka gembok file agar bisa dibaca semua siswa
    permission = {'type': 'anyone', 'role': 'reader'}
    drive_service.permissions().create(fileId=file.get('id'), body=permission).execute()
    
    return file.get('webViewLink')

# --- FUNGSI UTILITAS DATABASE SUPABASE ---
def db_get_user(username):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?username=ilike.{username}"
    res = requests.get(url, headers=HEADERS).json()
    if isinstance(res, list) and len(res) > 0: return res[0]
    return None

def db_create_user(username, hashed_pwd):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud"
    data = {"username": username, "password": hashed_pwd, "avatar_name": "Geni Us", "title": "🏅 Pemula", "points": 0, "streak": 1}
    requests.post(url, headers=HEADERS, json=data)

def db_update_points(username, new_points):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}"
    requests.patch(url, headers=HEADERS, json={"points": new_points})

def db_update_avatar(username, avatar_name):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}"
    requests.patch(url, headers=HEADERS, json={"avatar_name": avatar_name})

def db_update_title(username, title, cost=0):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{username}"
    payload = {"title": title}
    if cost > 0:
        current = db_get_user(username)
        if current: payload["points"] = current["points"] - cost
    requests.patch(url, headers=HEADERS, json=payload)

def db_get_learned_history(username):
    url = f"{SUPABASE_URL}/rest/v1/kuis_history_cloud?username=eq.{username}"
    res = requests.get(url, headers=HEADERS).json()
    if isinstance(res, list): return set([row["id_kuis"] for row in res])
    return set()

def db_add_kuis_history(username, id_kuis):
    url = f"{SUPABASE_URL}/rest/v1/kuis_history_cloud"
    requests.post(url, headers=HEADERS, json={"username": username, "id_kuis": id_kuis})

def db_get_leaderboard():
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,points,title&order=points.desc&limit=5"
    res = requests.get(url, headers=HEADERS).json()
    return res if isinstance(res, list) else []

# --- FUNGSI BARU: MENYIMPAN & MENGAMBIL MATERI DARI SUPABASE ---
def db_save_materi(mapel, kelas, bab, sub_bab, file_name, drive_link):
    url = f"{SUPABASE_URL}/rest/v1/materi_cloud"
    data = {"mapel": mapel, "kelas": kelas, "bab": bab, "sub_bab": sub_bab, "file_name": file_name, "drive_link": drive_link}
    requests.post(url, headers=HEADERS, json=data)

def db_get_materi(mapel, kelas, bab, sub_bab):
    url = f"{SUPABASE_URL}/rest/v1/materi_cloud?mapel=eq.{mapel}&kelas=eq.{kelas}&bab=eq.{bab}&sub_bab=eq.{sub_bab}"
    res = requests.get(url, headers=HEADERS).json()
    return res if isinstance(res, list) else []

# --- INISIALISASI MEMORI ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "gacha_claimed" not in st.session_state: st.session_state.gacha_claimed = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "drill_aktif" not in st.session_state: st.session_state.drill_aktif = False
if "soal_drill_saat_ini" not in st.session_state: st.session_state.soal_drill_saat_ini = []
if "hasil_drill" not in st.session_state: st.session_state.hasil_drill = None

PASSWORD_ADMIN = "LEARNWITHLM"

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def bersihkan_nama(teks): return re.sub(r'[\\/*?:"<>|]', "", teks)

# --- IMPORT DARI FILE EKSTERNAL ---
try:
    from database_rangkuman import DATA_MATERI
    from database_soal import BANK_SOAL_PRO
except ImportError:
    DATA_MATERI, BANK_SOAL_PRO = {}, {}

DAFTAR_GELAR = {"⚡ Petarung Cepat": 150, "🧪 Alkemis Gila": 200, "👑 Raja Duel": 400, "🌌 Penguasa Server": 1000}

# --- KUSTOMISASI CSS PRO UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0B0F19; background-image: radial-gradient(circle at 50% 0%, #172136 0%, #0B0F19 100%); color: #F8FAFC; }
    h1, h2, h3, h4, h5, p, span, label { color: #F8FAFC !important; }
    .gradient-text { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(0, 198, 255, 0.4) !important; border-radius: 10px; }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span { color: #00C6FF !important; -webkit-text-fill-color: #00C6FF !important; font-weight: bold; font-size: 16px; }
    .glass-card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 30px; text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
    .score-card { background: linear-gradient(135deg, rgba(0, 198, 255, 0.1) 0%, rgba(0, 114, 255, 0.1) 100%); border: 1px solid #00C6FF; border-radius: 15px; padding: 20px; text-align: center; }
    .stButton>button { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; width: 100%; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4); }
    .btn-red>button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); }
    .btn-green>button { background: linear-gradient(135deg, #10B981 0%, #047857 100%); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }
    div[data-testid="stMetricValue"] { color: #00C6FF !important; font-size: 35px !important; font-weight: 900 !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;} [data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

def tampilkan_avatar(keyword, ukuran="130px"):
    st.markdown(f"<div style='text-align:center; font-size:80px;'>{'👨‍🎓' if keyword=='genius' else '👩‍🎓'}</div>", unsafe_allow_html=True)

# ==========================================
# PORTAL AUTENTIKASI CLOUD
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; margin-top:50px; font-size:50px;'>Learning Media <span class='gradient-text'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:40px;'>Infrastruktur Google Drive Terintegrasi.</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
    with col_form:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 MASUK", "📝 DAFTAR"])
        
        with tab_log:
            l_user = st.text_input("Username:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            if st.button("🚀 LOGIN"):
                if l_user and l_pass:
                    user_record = db_get_user(l_user)
                    if user_record and user_record.get("password") == hash_password(l_pass):
                        st.session_state.username = user_record["username"] 
                        st.session_state.logged_in = True; st.rerun()
                    else: st.error("❌ Username/Sandi salah!")
        with tab_reg:
            r_user = st.text_input("Username Baru:", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Sandi Baru:", type="password", key="r_pwd").strip()
            if st.button("✨ DAFTAR"):
                if r_user and r_pass:
                    if db_get_user(r_user): st.error("⚠️ Username terpakai!")
                    else:
                        db_create_user(r_user, hash_password(r_pass))
                        st.success("🎉 Akun Dibuat! Silakan Login.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# DATA PENGGUNA AKTIF
# ==========================================
player = st.session_state.username
user_data = db_get_user(player)
if not user_data: st.session_state.logged_in = False; st.rerun()

avatar_db, title_db, points_db, streak_db = user_data.get("avatar_name", "Geni Us"), user_data.get("title", "🏅 Pemula"), user_data.get("points", 0), user_data.get("streak", 1)
learned_db = db_get_learned_history(player)
user_level = (points_db // 100) + 1
def get_tier(lvl):
    if lvl < 3: return "🥉 Bronze", "#CD7F32"
    elif lvl < 6: return "🥈 Silver", "#C0C0C0"
    else: return "🥇 Gold", "#FFD700"
tier_name, tier_color = get_tier(user_level)

with st.sidebar:
    tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart")
    st.markdown(f"<h2 style='text-align:center; margin-top:10px;' class='gradient-text'>{player}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;'><span style='background:rgba(0,198,255,0.1); color:#00C6FF; padding:4px 15px; border-radius:20px; font-weight:bold; border:1px solid #00C6FF;'>{title_db}</span></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    menu = st.radio("NAVIGASI", ["🏠 Beranda", "📖 Arena Drill", "⚙️ Konsol Admin Pro"])
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT"): st.session_state.logged_in = False; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 1: BERANDA 
# ==========================================
if menu == "🏠 Beranda":
    st.markdown(f"<h1>SELAMAT DATANG, <span class='gradient-text'>{player.upper()}</span>! 🚀</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h2 style='margin:0;'>{streak_db} Hari</h2><p style='color:#94A3B8; margin:0;'>Streak</p></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h2 style='margin:0;'>{len(learned_db)}</h2><p style='color:#94A3B8; margin:0;'>Drill</p></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:40px;'>🏆</div><h2 style='color:{tier_color}; margin:0;'>Lvl {user_level}</h2><p style='color:#94A3B8; margin:0;'>⭐ {points_db} XP</p></div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: ARENA DRILL & LATIHAN BAB 
# ==========================================
elif menu == "📖 Arena Drill":
    st.markdown("<h1>📖 <span class='gradient-text'>ARENA MATERI & EVALUASI</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 20px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("📚 Mata Pelajaran:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("🎓 Tingkat Kelas:", kelas_list if kelas_list else ["-"])
        
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("📑 Sektor Bab:", bab_list if bab_list else ["-"])
        sub_list = DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).get(p_bab, {}).get("sub_bab", ["-"])
        with col4: p_sub = st.selectbox("🔖 Sub-bab:", sub_list)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    tab_mat, tab_doc = st.tabs(["📌 Rangkuman Ekstra", "📂 Berkas Dari Guru (Cloud Drive)"])
    
    with tab_mat:
        try: st.markdown(f"<div class='glass-card' style='text-align:left;'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Catatan tidak ditemukan.")

    with tab_doc:
        st.markdown("### ☁️ Arsip Dokumen Google Drive")
        st.caption("Semua materi di bawah ini ditarik secara otomatis dari Cloud Server.")
        
        # Mengambil daftar link dari Supabase
        materi_cloud = db_get_materi(p_mapel, p_kelas, p_bab, p_sub)
        
        if materi_cloud:
            for item in materi_cloud:
                st.markdown(f"""
                <div style='background:rgba(15,23,42,0.8); border:1px solid #00C6FF; padding:15px; border-radius:10px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;'>
                    <h4 style='margin:0; color:#F8FAFC;'>📄 {item['file_name']}</h4>
                    <a href="{item['drive_link']}" target="_blank" style='background:#00C6FF; color:#0B0F19; padding:8px 15px; border-radius:8px; text-decoration:none; font-weight:bold;'>🔗 BUKA FILE</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 Admin/Guru belum mengunggah file untuk materi ini ke Google Drive.")

# ==========================================
# HALAMAN 3: SUPER ADMIN DASHBOARD
# ==========================================
elif menu == "⚙️ Konsol Admin Pro":
    st.markdown("<h1>⚙️ <span class='gradient-text'>G-DRIVE COMMAND CENTER</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        pwd = st.text_input("Master Password Admin:", type="password")
        if st.button("Buka Akses") and pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
    else:
        st.success("🔓 Otoritas Google Cloud Diberikan.")
        st.markdown("### ☁️ Upload Otomatis ke Google Drive")
        st.caption("Berkas yang diunggah di sini akan dikirim ke robot Google, lalu link-nya akan disimpan permanen ke database Supabase.")
        
        c1, c2 = st.columns(2)
        with c1: up_mapel = st.selectbox("📚 Mata Pelajaran:", list(DATA_MATERI.keys()), key="adm_m")
        k_list = list(DATA_MATERI.get(up_mapel, {}).keys())
        with c2: up_kelas = st.selectbox("🎓 Kelas:", k_list if k_list else ["-"], key="adm_k")
        
        c3, c4 = st.columns(2)
        b_list = list(DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).keys())
        with c3: up_bab = st.selectbox("📑 Bab:", b_list if b_list else ["-"], key="adm_b")
        s_list = DATA_MATERI.get(up_mapel, {}).get(up_kelas, {}).get(up_bab, {}).get("sub_bab", ["-"])
        with c4: up_sub = st.selectbox("🔖 Sub-bab:", s_list, key="adm_s")
        
        st.write("<br>", unsafe_allow_html=True)
        up_file = st.file_uploader("Pilih Berkas (Semua Format Diizinkan):")
        
        if up_file:
            st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
            if st.button("🚀 UPLOAD KE GOOGLE DRIVE & SIMPAN LINK"):
                if not GOOGLE_READY:
                    st.error("Gagal! Kunci Rahasia JSON Google Cloud belum dipasang atau salah format.")
                else:
                    with st.spinner('Menyuntikkan file ke Google Drive...'):
                        try:
                            file_buffer = up_file.getvalue()
                            # 1. Robot upload ke Drive
                            link_publik = upload_to_drive(file_buffer, up_file.name, up_file.type)
                            # 2. Mencatat link tersebut ke Supabase
                            db_save_materi(up_mapel, up_kelas, up_bab, up_sub, up_file.name, link_publik)
                            
                            st.toast("Sukses Tembus Cloud!", icon="☁️")
                            st.success(f"✅ File berhasil di-upload ke Drive! Tautan Publik: {link_publik}")
                            st.info("Siswa sekarang bisa langsung melihat file ini di menu Arena Drill.")
                        except Exception as e:
                            st.error(f"Terjadi kesalahan saat *upload*: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
