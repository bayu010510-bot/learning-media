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
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- FUNGSI UTILITAS DATABASE (REST API SUPABASE ENGINE) ---
def db_get_user(username):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?username=ilike.{username}"
    res = requests.get(url, headers=HEADERS).json()
    return res[0] if res else None

def db_create_user(username, hashed_pwd):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud"
    data = {
        "username": username, "password": hashed_pwd, "avatar_name": "Geni Us",
        "title": "🏅 Pemula", "points": 0, "streak": 1,
        "matematika": 10, "fisika": 10, "kimia": 10, "biologi": 10,
        "sejarah": 10, "ekonomi": 10, "sosiologi": 10, "seni_budaya": 10,
        "geografi": 10, "prakarya_dan_kewirausahaan": 10
    }
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
        # Ambil poin saat ini lalu kurangi
        current = db_get_user(username)
        if current:
            payload["points"] = current["points"] - cost
    requests.patch(url, headers=HEADERS, json=payload)

def db_get_learned_history(username):
    url = f"{SUPABASE_URL}/rest/v1/kuis_history_cloud?username=eq.{username}"
    res = requests.get(url, headers=HEADERS).json()
    return set([row["id_kuis"] for row in res])

def db_add_kuis_history(username, id_kuis):
    url = f"{SUPABASE_URL}/rest/v1/kuis_history_cloud"
    requests.post(url, headers=HEADERS, json={"username": username, "id_kuis": id_kuis})

def db_get_leaderboard():
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,points,title&order=points.desc&limit=5"
    return requests.get(url, headers=HEADERS).json()

def db_get_all_users_admin():
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?select=username,title,points,streak&order=points.desc"
    return requests.get(url, headers=HEADERS).json()

def db_get_random_opponent(exclude_username):
    url = f"{SUPABASE_URL}/rest/v1/users_cloud?username=neq.{exclude_username}&limit=10"
    res = requests.get(url, headers=HEADERS).json()
    return random.choice(res) if res else None

def db_update_pvp_win(winner, loser, winner_current_pts, loser_current_pts):
    url_w = f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{winner}"
    requests.patch(url_w, headers=HEADERS, json={"points": winner_current_pts + 100})
    url_l = f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{loser}"
    requests.patch(url_l, headers=HEADERS, json={"points": max(0, loser_current_pts - 20)})

def db_update_pvp_lose(loser, loser_current_pts):
    url_l = f"{SUPABASE_URL}/rest/v1/users_cloud?username=eq.{loser}"
    requests.patch(url_l, headers=HEADERS, json={"points": max(0, loser_current_pts - 30)})

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
from database_rangkuman import DATA_MATERI
from database_soal import BANK_SOAL_PRO

DAFTAR_GELAR = {"⚡ Petarung Cepat": 150, "🧪 Alkemis Gila": 200, "👑 Raja Duel": 400, "🌌 Penguasa Server": 1000}

# --- KUSTOMISASI CSS PRO UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0B0F19; background-image: radial-gradient(circle at 50% 0%, #172136 0%, #0B0F19 100%); color: #F8FAFC; }
    h1, h2, h3, h4, h5, p, span, label { color: #F8FAFC !important; }
    
    .gradient-text { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .vs-text { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 50px; }
    
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(0, 198, 255, 0.4) !important; border-radius: 10px; }
    div[data-baseweb="input"] input, div[data-baseweb="select"] span { color: #00C6FF !important; -webkit-text-fill-color: #00C6FF !important; font-weight: bold; font-size: 16px; }
    
    .glass-card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 30px; text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s; }
    .glass-card:hover { transform: translateY(-5px); border-color: rgba(0, 198, 255, 0.4); box-shadow: 0 0 30px rgba(0, 198, 255, 0.2); }
    .score-card { background: linear-gradient(135deg, rgba(0, 198, 255, 0.1) 0%, rgba(0, 114, 255, 0.1) 100%); border: 1px solid #00C6FF; border-radius: 15px; padding: 20px; text-align: center; }
    
    .stButton>button { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease; width: 100%; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4); }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 0 25px rgba(0, 198, 255, 0.7); }
    .btn-red>button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); }
    .btn-red>button:hover { box-shadow: 0 0 25px rgba(255, 75, 43, 0.8); }
    .btn-green>button { background: linear-gradient(135deg, #10B981 0%, #047857 100%); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }
    .btn-green>button:hover { box-shadow: 0 0 25px rgba(16, 185, 129, 0.8); }
    
    div[data-testid="stMetricValue"] { color: #00C6FF !important; font-size: 35px !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 16px !important; font-weight: bold !important; text-transform: uppercase; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;} [data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

def tampilkan_avatar(keyword, ukuran="130px"):
    c_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        for f in os.listdir(c_dir):
            if keyword in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_b64 = base64.b64encode(open(os.path.join(c_dir, f), 'rb').read()).decode()
                st.markdown(f"<div style='display:flex; justify-content:center;'><img src='data:image/png;base64,{img_b64}' style='width:{ukuran}; filter: drop-shadow(0 0 20px rgba(0, 198, 255, 0.4)); animation: float 3s ease-in-out infinite;'></div>", unsafe_allow_html=True)
                return True
    except: pass
    st.markdown(f"<div style='text-align:center; font-size:80px;'>{'👨‍🎓' if keyword=='genius' else '👩‍🎓'}</div>", unsafe_allow_html=True)

# ==========================================
# PORTAL AUTENTIKASI CLOUD
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; margin-top:50px; font-size:50px;'>Learning Media <span class='gradient-text'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:40px;'>Satu Profil, Ribuan Tantangan. Masuk ke Arena Belajar Cloud.</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
    with col_form:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 MASUK ARENA", "📝 BUAT PROFIL BARU"])
        
        with tab_log:
            l_user = st.text_input("Username Ksatria:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            if st.button("🚀 LOGIN SEKARANG"):
                if l_user and l_pass:
                    user_record = db_get_user(l_user)
                    if user_record and user_record["password"] == hash_password(l_pass):
                        st.session_state.username = user_record["username"] 
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("❌ Username atau Sandi salah!")
                else: st.warning("Isi semua kolom!")
                
        with tab_reg:
            r_user = st.text_input("Buat Username (Maks 15 Huruf):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Buat Kata Sandi:", type="password", key="r_pwd").strip()
            if st.button("✨ DAFTAR BARU"):
                if r_user and r_pass:
                    if db_get_user(r_user): st.error("⚠️ Username sudah dipakai petarung lain!")
                    else:
                        db_create_user(r_user, hash_password(r_pass))
                        st.success("🎉 Profil Berhasil Ditempa Cloud! Silakan beralih ke tab '🔐 MASUK ARENA'.")
                else: st.warning("Isi semua kolom pendaftaran!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# MEMUAT DATA CLOUD PENGGUNA AKTIF
# ==========================================
player = st.session_state.username
user_data = db_get_user(player)
avatar_db, title_db, points_db, streak_db = user_data["avatar_name"], user_data["title"], user_data["points"], user_data["streak"]

learned_db = db_get_learned_history(player)
user_level = (points_db // 100) + 1

def get_tier(lvl):
    if lvl < 3: return "🥉 Bronze", "#CD7F32"
    elif lvl < 6: return "🥈 Silver", "#C0C0C0"
    elif lvl < 10: return "🥇 Gold", "#FFD700"
    elif lvl < 15: return "💎 Platinum", "#00EDFF"
    else: return "🌌 Mythic", "#9D00FF"
tier_name, tier_color = get_tier(user_level)

# --- SIDEBAR KOKPIT ---
with st.sidebar:
    st.write("<br>", unsafe_allow_html=True)
    tampilkan_avatar("genius" if avatar_db == "Geni Us" else "smart", "100px")
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
    menu = st.radio("SISTEM NAVIGASI", ["🏠 Beranda Server", "⚔️ Mode Duel Ranked (PvP)", "📖 Arena Drill & Latihan", "⚙️ Konsol Admin Pro", "🛒 Pasar Gelar & Profil"])
    
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT PROFIL"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 1: BERANDA SERVER CLOUD
# ==========================================
if menu == "🏠 Beranda Server":
    st.markdown(f"<h1>SELAMAT DATANG, <span class='gradient-text'>{player.upper()}</span>! 🚀</h1>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='border-color:#F59E0B; background:rgba(245, 158, 11, 0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FCD34D; margin-top:0;'>🎁 Peti Harta Karun Harian!</h2>", unsafe_allow_html=True)
        if st.button("🗝️ KLAIM BONUS LOGIN XP"):
            bonus = random.choice([20, 50, 100])
            db_update_points(player, points_db + bonus)
            st.session_state.gacha_claimed = True
            st.toast(f"HORE! Dapat +{bonus} XP!", icon="🎉")
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h2 style='margin:0;'>{streak_db} Hari</h2><p style='color:#94A3B8; margin:0;'>Login Streak</p></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h2 style='margin:0;'>{len(learned_db)}</h2><p style='color:#94A3B8; margin:0;'>Drill Dikuasai</p></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:40px;'>🏆</div><h2 style='color:{tier_color}; margin:0;'>{tier_name.split()[1]}</h2><p style='color:#94A3B8; margin:0;'>Kasta Global</p></div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3>📊 LIVE GLOBAL RANKING (CLOUD REAL-TIME)</h3>", unsafe_allow_html=True)
    
    ranking_data = db_get_leaderboard()
    for i, row in enumerate(ranking_data):
        medali = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        bg_color = "rgba(255, 215, 0, 0.1)" if i==0 else "rgba(255,255,255,0.02)"
        bdr_color = "rgba(255, 215, 0, 0.5)" if i==0 else "rgba(255,255,255,0.08)"
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid {bdr_color}; border-radius: 15px; padding: 15px 25px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>
            <h3 style='margin:0;'>{medali} {row["username"]} <span style='font-size:14px; font-weight:normal; color:#94A3B8;'>({row["title"]})</span></h3>
            <h3 style='margin:0; color:#00C6FF;'>⭐ {row["points"]} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: MODE DUEL CLOUD (PvP MENGGUNAKAN BANK SOAL)
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1>⚔️ <span class='gradient-text'>ARENA DUEL MULTIPLAYER CLOUD</span></h1>", unsafe_allow_html=True)
    
    pool_pvp = {}
    for mp, data_kelas in BANK_SOAL_PRO.items():
        pool_pvp[mp] = []
        for kl, data_bab in data_kelas.items():
            for bb, data_sub in data_bab.items():
                for sub, list_soal in data_sub.items():
                    pool_pvp[mp].extend(list_soal)
                
    if not pool_pvp:
        st.warning("Bank soal PvP masih kosong. Silakan gunakan Arena Latihan.")
        st.stop()
        
    col_mapel, col_btn = st.columns([3,1])
    with col_mapel: mapel_duel = st.selectbox("🎯 Pilih Arena Mata Pelajaran:", list(pool_pvp.keys()))
    
    if "lawan_duel" not in st.session_state: st.session_state.lawan_duel = None
    if "kuis_duel" not in st.session_state: st.session_state.kuis_duel = False
    if "soal_pvp_aktif" not in st.session_state: st.session_state.soal_pvp_aktif = None
    
    with col_btn:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🔍 CARI LAWAN ACURATE"):
            lawan = db_get_random_opponent(player)
            if lawan and len(pool_pvp[mapel_duel]) > 0:
                st.session_state.lawan_duel = (lawan["username"], lawan["points"])
                st.session_state.kuis_duel = True
                soal_asli = random.choice(pool_pvp[mapel_duel])
                opsi_acak = soal_asli["opsi"].copy()
                random.shuffle(opsi_acak)
                st.session_state.soal_pvp_aktif = {"soal": soal_asli["soal"], "opsi": opsi_acak, "jawaban": soal_asli["jawaban"]}
            else: st.error("Tidak ada lawan / kuis tersedia di cloud!")
            
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
        
        if st.button("⚡ EKSEKUSI SERANGAN CLOUD"):
            if j_user == ds['jawaban']:
                db_update_pvp_win(player, l_nama, points_db, l_pts)
                st.toast(f"CRITICAL STRIKE! Berhasil mengalahkan {l_nama}", icon="⚔️")
                st.session_state.kuis_duel = False 
                st.success(f"🎉 **KAMU MENANG!** +100 XP ditambahkan ke database cloud.")
            else:
                db_update_pvp_lose(player, points_db)
                st.toast("BLOCKED! Pertahanan hancur.", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"💀 **KAMU KALAH!** Kehilangan 30 XP.")
            if st.button("🔄 Sinkronisasi"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: ARENA DRILL & LATIHAN BAB (CLOUD INTEGRATED)
# ==========================================
elif menu == "📖 Arena Drill & Latihan":
    st.markdown("<h1>📖 <span class='gradient-text'>ARENA DRILL EVALUASI</span></h1>", unsafe_allow_html=True)
    
    mapel_list = list(DATA_MATERI.keys())
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 20px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("📚 Mata Pelajaran:", mapel_list)
        kelas_list = list(DATA_MATERI.get(p_mapel, {}).keys())
        with col2: p_kelas = st.selectbox("🎓 Tingkat Kelas:", kelas_list if kelas_list else ["Tidak tersedia"])
        
        col3, col4 = st.columns(2)
        bab_list = list(DATA_MATERI.get(p_mapel, {}).get(p_kelas, {}).keys())
        with col3: p_bab = st.selectbox("📑 Sektor Bab:", bab_list if bab_list else ["Tidak tersedia"])
        sub_list = []
        try: sub_list = DATA_MATERI[p_mapel][p_kelas][p_bab].get("sub_bab", [])
        except: pass
        with col4: p_sub = st.selectbox("🔖 Sub-bab Spesifik:", sub_list if sub_list else ["Tidak tersedia"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    tab_drill, tab_mat, tab_doc = st.tabs(["⚔️ Latihan Drill (Sistem Acak)", "📌 Rangkuman Ekstra", "📂 Modul Google Drive"])
    
    with tab_drill:
        st.markdown("### 🎯 Simulasi Ujian Sub-bab")
        soal_tersedia = []
        try: soal_tersedia = BANK_SOAL_PRO[p_mapel][p_kelas][p_bab][p_sub]
        except KeyError: pass
        
        if not soal_tersedia:
            st.info("📭 Bank Soal untuk Sub-bab ini belum di-input di database_soal.py.")
        else:
            if not st.session_state.drill_aktif and not st.session_state.hasil_drill:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🚀 MULAI GENERASI SOAL ACAK"):
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
                total_s = len(st.session_state.soal_drill_saat_ini)
                st.progress(100)
                with st.form(key="form_drill"):
                    jawaban_user = []
                    for i, s in enumerate(st.session_state.soal_drill_saat_ini):
                        st.markdown(f"<div class='glass-card' style='text-align:left; padding:20px; margin-bottom:15px; border-left:4px solid #00C6FF;'>", unsafe_allow_html=True)
                        st.markdown(f"**Pertanyaan {i+1}:**<br>{s['soal']}", unsafe_allow_html=True)
                        ans = st.radio(f"Pilih jawaban:", s['opsi_acak'], key=f"d_ans_{i}", label_visibility="collapsed")
                        jawaban_user.append(ans)
                        st.markdown("</div>", unsafe_allow_html=True)
                    submit_drill = st.form_submit_button("📝 KUMPULKAN JAWABAN & KOREKSI")
                    
                if submit_drill:
                    skor_benar = 0
                    eval_data = []
                    for i, s in enumerate(st.session_state.soal_drill_saat_ini):
                        j_user = jawaban_user[i]
                        j_asli = s['jawaban_asli']
                        benar = (j_user == j_asli)
                        if benar: skor_benar += 1
                        eval_data.append({"soal": s['soal'], "jawaban_anda": j_user, "jawaban_benar": j_asli, "pem": s['pembahasan'], "is_correct": benar})
                    st.session_state.hasil_drill = {"skor_benar": skor_benar, "total": total_s, "evaluasi": eval_data}
                    st.session_state.drill_aktif = False
                    st.rerun()
            
            elif st.session_state.hasil_drill:
                hasil = st.session_state.hasil_drill
                skor, tot = hasil["skor_benar"], hasil["total"]
                xp_gained = skor * 30
                akurasi = int((skor / tot) * 100)
                
                st.markdown("### 📊 DASHBOARD EVALUASI")
                c_met1, c_met2, c_met3 = st.columns(3)
                with c_met1: st.markdown(f"<div class='score-card'><h4>🎯 Akurasi</h4><h1 style='color:#00C6FF; margin:0;'>{akurasi}%</h1></div>", unsafe_allow_html=True)
                with c_met2: st.markdown(f"<div class='score-card'><h4>✅ Benar</h4><h1 style='color:#10B981; margin:0;'>{skor}/{tot}</h1></div>", unsafe_allow_html=True)
                with c_met3: st.markdown(f"<div class='score-card'><h4>⚡ XP</h4><h1 style='color:#F59E0B; margin:0;'>+{xp_gained}</h1></div>", unsafe_allow_html=True)
                
                if xp_gained > 0:
                    db_update_points(player, points_db + xp_gained)
                    id_drill = f"drill_{p_mapel}_{p_kelas}_{p_bab}_{p_sub}"
                    if akurasi == 100 and id_drill not in learned_db:
                        db_add_kuis_history(player, id_drill)
                    st.toast(f"Sinkronisasi Cloud Selesai! +{xp_gained} XP Saved.", icon="🏆")
                
                for i, ev in enumerate(hasil["evaluasi"]):
                    ikon, warna = ("✅", "#10B981") if ev["is_correct"] else ("❌", "#EF4444")
                    with st.expander(f"{ikon} Soal {i+1} | Kunci: {ev['jawaban_benar']}"):
                        st.write(ev['soal'])
                        st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; border-left:3px solid {warna};'><b>🧠 Pembahasan:</b><br>{ev['pem']}</div>", unsafe_allow_html=True)
                
                if st.button("🔄 Selesai & Kembali"):
                    st.session_state.hasil_drill = None
                    st.rerun()

    with tab_mat:
        try: st.markdown(f"<div class='glass-card' style='text-align:left;'>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        except: st.info("Rangkuman tidak ditemukan di file `database_rangkuman.py`.")

    with tab_doc:
        st.markdown("### 📂 Modul Pendukung Cloud")
        try: link_drive = DATA_MATERI[p_mapel][p_kelas][p_bab].get("link_drive", "")
        except: link_drive = ""
        if link_drive: st.link_button("🔗 BUKA MODUL DI GOOGLE DRIVE", link_drive, use_container_width=True)
        else: st.info("📭 Modul Google Drive belum disematkan oleh Admin.")

# ==========================================
# HALAMAN 4: SUPER ADMIN DASHBOARD
# ==========================================
elif menu == "⚙️ Konsol Admin Pro":
    st.markdown("<h1>⚙️ <span class='gradient-text'>SUPER ADMIN COMMAND CENTER</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='border-color:#EF4444;'><h2>🔒 SECURE SECURITY GATEWAY</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Master Password Admin:", type="password")
        if st.button("Buka Akses"):
            if pwd == PASSWORD_ADMIN: st.session_state.is_admin = True; st.rerun()
            else: st.error("Akses Ditolak!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("🔓 Akses Server Utama Terbuka.")
        tab_stat, tab_db = st.tabs(["📊 Statistik Jaringan Cloud", "👥 Pantau Database Siswa"])
        
        users_admin = db_get_all_users_admin()
        
        with tab_stat:
            total_akun = len(users_admin)
            total_xp = sum([r["points"] for r in users_admin])
            max_streak = max([r["streak"] for r in users_admin]) if users_admin else 0
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Siswa Terdaftar", f"{total_akun} Akun")
            c2.metric("Total XP di Database", f"{total_xp} XP")
            c3.metric("Rekor Login Streak", f"{max_streak} Hari")
            
        with tab_db:
            if users_admin:
                df = pd.DataFrame(users_admin)
                df.columns = ["Nama Akun", "Julukan", "Total XP", "Login Streak"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else: st.info("Database Kosong.")
            
        if st.button("🔴 KUNCI DASHBOARD ADMIN"): st.session_state.is_admin = False; st.rerun()

# ==========================================
# HALAMAN 5: PASAR SHOP
# ==========================================
elif menu == "🛒 Pasar Gelar & Profil":
    st.markdown("<h1>🛒 <span class='gradient-text'>BLACK MARKET PROFIL</span></h1>", unsafe_allow_html=True)
    tab_av, tab_gl = st.tabs(["👤 Pilih Karakter", "👑 Tukar Julukan"])
    
    with tab_av:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            if st.button("SET AVATAR: GENI US"):
                db_update_avatar(player, "Geni Us")
                st.toast("Avatar Diperbarui!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            if st.button("SET AVATAR: SMAR T"):
                db_update_avatar(player, "Smar T")
                st.toast("Avatar Diperbarui!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left;'><h3>Bursa Julukan Ksatria</h3>", unsafe_allow_html=True)
        st.write(f"Tabungan Kamu: ⭐ **{points_db} XP**")
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        for gelar, harga in DAFTAR_GELAR.items():
            cg1, cg2, cg3 = st.columns([3, 1, 1])
            cg1.markdown(f"#### {gelar}")
            cg2.markdown(f"<p style='color:#F59E0B;'>💰 {harga} XP</p>", unsafe_allow_html=True)
            with cg3:
                if title_db == gelar: st.button("✅ Aktif", key=f"ak_{gelar}", disabled=True)
                else:
                    if st.button("Beli & Pakai", key=f"by_{gelar}"):
                        if points_db >= harga:
                            db_update_title(player, gelar, cost=harga)
                            st.toast(f"Julukan {gelar} Terpasang!", icon="👑"); st.rerun()
                        else: st.error("XP Kurang!")
        st.markdown("</div>", unsafe_allow_html=True)
