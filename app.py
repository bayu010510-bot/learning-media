import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
import base64
import random
import sqlite3
import hashlib

# --- SISTEM DATABASE MULTIPLAYER (SQLITE) ---
conn = sqlite3.connect("learning_media_pro.db", check_same_thread=False)
cursor = conn.cursor()

# Membuat tabel dengan Sistem Password
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    avatar_name TEXT,
    title TEXT,
    points INTEGER,
    streak INTEGER,
    matematika INT, fisika INT, kimia INT, biologi INT, sejarah INT, ekonomi INT, sosiologi INT
)
""")
cursor.execute("CREATE TABLE IF NOT EXISTS kuis_history (username TEXT, id_kuis TEXT, PRIMARY KEY(username, id_kuis))")
# Update tabel lama jika belum punya kolom password (Anti-Error)
try: cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
except: pass
conn.commit()

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media | Edisi Esports", page_icon="⚔️", layout="wide", initial_sidebar_state="expanded")

# --- INISIALISASI MEMORI LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "gacha_claimed" not in st.session_state: st.session_state.gacha_claimed = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False

PASSWORD_ADMIN = "LEARNWITHLM"

# --- FUNGSI PENGAMANAN & BANTUAN ---
def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def bersihkan_nama(teks): return re.sub(r'[\\/*?:"<>|]', "", teks)

# --- DATABASE MATERI & KUIS UTBK ---
from materi import DATA_MATERI

DATABASE_KUIS = {
    "Matematika": {"soal": "Jika $2^{x+1} = 16$, nilai $x$ adalah?", "opsi": ["2", "3", "4", "5"], "jaw": "3", "pem": "$2^{x+1} = 2^4 \\Rightarrow x+1=4 \\Rightarrow x=3$."},
    "Fisika": {"soal": "Energi potensial benda 2 kg di ketinggian 10 m (g=10)?", "opsi": ["100 J", "200 J", "300 J", "400 J"], "jaw": "200 J", "pem": "Ep = m.g.h = $2 \\times 10 \\times 10 = 200$ J."},
    "Kimia": {"soal": "Kondisi laju reaksi ke kanan dan kiri sama disebut?", "opsi": ["Katalis", "Kesetimbangan Dinamis", "Reaksi Eksoterm", "Redoks"], "jaw": "Kesetimbangan Dinamis", "pem": "V(kanan) = V(kiri)."},
    "Biologi": {"soal": "Pemisah fauna Asiatis dan Peralihan?", "opsi": ["Khatulistiwa", "Wallace", "Weber", "Bujur"], "jaw": "Wallace", "pem": "Garis Wallace."},
    "Sejarah": {"soal": "Penculikan Soekarno-Hatta ke luar Jakarta disebut?", "opsi": ["Bandung Lautan Api", "Rengasdengklok", "Ambarawa", "Madiun"], "jaw": "Rengasdengklok", "pem": "16 Agustus 1945."},
    "Ekonomi": {"soal": "Inti masalah ekonomi adalah...", "opsi": ["Inflasi", "Kelangkaan (Scarcity)", "Deflasi", "Monopoli"], "jaw": "Kelangkaan (Scarcity)", "pem": "Kebutuhan tak terbatas vs alat terbatas."},
    "Sosiologi": {"soal": "Pengelompokan masyarakat sejajar disebut...", "opsi": ["Stratifikasi", "Diferensiasi", "Mobilitas", "Konflik"], "jaw": "Diferensiasi", "pem": "Diferensiasi = setara."}
}

DAFTAR_GELAR = {"⚡ Petarung Cepat": 150, "🧪 Alkemis Gila": 200, "👑 Raja Duel": 400, "🌌 Penguasa Server": 1000}

# --- KUSTOMISASI CSS HOLOGRAFIS & NEON (ANTI BUG TEKS HILANG) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0B0F19; background-image: radial-gradient(circle at 50% 0%, #172136 0%, #0B0F19 100%); color: #F8FAFC; }
    h1, h2, h3, h4, h5, p, span, label { color: #F8FAFC !important; }
    
    /* Teks Gradasi Super Keren */
    .gradient-text { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
    .vs-text { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 50px; }
    
    /* PERBAIKAN INPUT & DROPDOWN AGAR TEKS SELALU TERLIHAT */
    div[data-baseweb="input"] { background-color: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(0, 198, 255, 0.4) !important; border-radius: 10px; }
    div[data-baseweb="input"] input { color: #00C6FF !important; -webkit-text-fill-color: #00C6FF !important; font-weight: bold; font-size: 16px; }
    
    div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(0, 198, 255, 0.4) !important; border-radius: 10px; }
    div[data-baseweb="select"] span { color: #00C6FF !important; -webkit-text-fill-color: #00C6FF !important; font-weight: bold; }
    
    /* Kartu Kaca (Glassmorphism 3.0) */
    .glass-card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 30px; text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); transition: transform 0.3s; }
    .glass-card:hover { transform: translateY(-5px); border-color: rgba(0, 198, 255, 0.4); box-shadow: 0 0 30px rgba(0, 198, 255, 0.2); }
    
    /* Tombol Interaktif */
    .stButton>button { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease; width: 100%; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4); }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 0 25px rgba(0, 198, 255, 0.7); }
    .btn-red>button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); }
    .btn-red>button:hover { box-shadow: 0 0 25px rgba(255, 75, 43, 0.8); }
    
    /* Menyembunyikan elemen bawaan Streamlit */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Sembunyikan Sidebar jika belum login
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
# PORTAL AUTENTIKASI (LOGIN / REGISTER)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; margin-top:50px; font-size:50px;'>Learning Media <span class='gradient-text'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:40px;'>Satu Profil, Ribuan Tantangan. Masuk ke Arena Belajar.</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
    with col_form:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 MASUK ARENA", "📝 BUAT PROFIL BARU"])
        
        with tab_log:
            # Fungsi strip() akan membuang spasi otomatis
            l_user = st.text_input("Username Ksatria:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            if st.button("🚀 LOGIN SEKARANG"):
                if l_user and l_pass:
                    cursor.execute("SELECT username, password FROM users WHERE lower(username)=lower(?)", (l_user,))
                    res = cursor.fetchone()
                    if res and res[1] == hash_password(l_pass):
                        st.session_state.username = res[0] # Menggunakan nama asli dari DB
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("❌ Username atau Sandi salah! Pastikan ketikanmu benar.")
                else: st.warning("Isi semua kolom!")
                
        with tab_reg:
            r_user = st.text_input("Buat Username (Maks 15 Huruf):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Buat Kata Sandi:", type="password", key="r_pwd").strip()
            if st.button("✨ DAFTAR BARU"):
                if r_user and r_pass:
                    cursor.execute("SELECT username FROM users WHERE lower(username)=lower(?)", (r_user,))
                    if cursor.fetchone(): st.error("⚠️ Username sudah dipakai petarung lain. Cari nama lain!")
                    else:
                        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                                       (r_user, hash_password(r_pass), "Geni Us", "🏅 Pemula", 0, 1, 10, 10, 10, 10, 10, 10, 10))
                        conn.commit()
                        st.success("🎉 Profil Ditempa! Silakan klik tab '🔐 MASUK ARENA' untuk Login.")
                else: st.warning("Isi semua kolom pendaftaran!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # Hentikan eksekusi kode di bawah ini jika belum login

# ==========================================
# MEMUAT DATA PENGGUNA AKTIF DARI DATABASE
# ==========================================
player = st.session_state.username
cursor.execute("SELECT * FROM users WHERE username=?", (player,))
user_data = cursor.fetchone()
avatar_db, title_db, points_db, streak_db = user_data[2], user_data[3], user_data[4], user_data[5]

cursor.execute("SELECT id_kuis FROM kuis_history WHERE username=?", (player,))
learned_db = set([row[0] for row in cursor.fetchall()])

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
    menu = st.radio("SISTEM NAVIGASI", ["🏠 Beranda Server", "⚔️ Mode Duel Ranked (PvP)", "📖 Arena Belajar Kuis", "📤 Terminal Berkas (Admin)", "🛒 Pasar Gelar & Profil"])
    
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT PROFIL"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 1: BERANDA SERVER & LEADERBOARD
# ==========================================
if menu == "🏠 Beranda Server":
    st.markdown(f"<h1>SELAMAT DATANG, <span class='gradient-text'>{player.upper()}</span>! 🚀</h1>", unsafe_allow_html=True)
    
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='border-color:#F59E0B; background:rgba(245, 158, 11, 0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FCD34D; margin-top:0;'>🎁 Peti Harta Karun Harian!</h2>", unsafe_allow_html=True)
        if st.button("🗝️ KLAIM BONUS LOGIN XP"):
            bonus = random.choice([20, 50, 100])
            cursor.execute("UPDATE users SET points = points + ? WHERE username = ?", (bonus, player))
            conn.commit()
            st.session_state.gacha_claimed = True
            st.toast(f"HORE! Dapat +{bonus} XP!", icon="🎉")
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h2 style='margin:0;'>{streak_db} Hari</h2><p style='color:#94A3B8; margin:0;'>Login Streak</p></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h2 style='margin:0;'>{len(learned_db)}</h2><p style='color:#94A3B8; margin:0;'>Kuis Dikuasai</p></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:40px;'>🏆</div><h2 style='color:{tier_color}; margin:0;'>{tier_name.split()[1]}</h2><p style='color:#94A3B8; margin:0;'>Kasta Global</p></div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3>📊 LIVE GLOBAL RANKING (ANTAR PEMAIN)</h3>", unsafe_allow_html=True)
    
    cursor.execute("SELECT username, points, title FROM users ORDER BY points DESC LIMIT 5")
    for i, row in enumerate(cursor.fetchall()):
        medali = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        bg_color = "rgba(255, 215, 0, 0.1)" if i==0 else "rgba(255,255,255,0.02)"
        bdr_color = "rgba(255, 215, 0, 0.5)" if i==0 else "rgba(255,255,255,0.08)"
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid {bdr_color}; border-radius: 15px; padding: 15px 25px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h3 style='margin:0;'>{medali} {row[0]} <span style='font-size:14px; font-weight:normal; color:#94A3B8;'>({row[2]})</span></h3>
            <h3 style='margin:0; color:#00C6FF; text-shadow: 0 0 10px rgba(0,198,255,0.5);'>⭐ {row[1]} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: MODE DUEL RANKED (PvP MATERI)
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1>⚔️ <span class='gradient-text'>ARENA DUEL MULTIPLAYER</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8;'>Pilih mata pelajaran, cari lawan acak secara real-time, jawab kuisnya, dan curi XP mereka!</p>", unsafe_allow_html=True)
    
    col_mapel, col_btn = st.columns([3,1])
    with col_mapel: mapel_duel = st.selectbox("🎯 Pilih Arena Mata Pelajaran:", list(DATABASE_KUIS.keys()))
    
    if "lawan_duel" not in st.session_state: st.session_state.lawan_duel = None
    if "kuis_duel" not in st.session_state: st.session_state.kuis_duel = False
    
    with col_btn:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🔍 CARI LAWAN (MATCHMAKING)"):
            cursor.execute("SELECT username, points FROM users WHERE username != ? ORDER BY RANDOM() LIMIT 1", (player,))
            lawan = cursor.fetchone()
            if lawan:
                st.session_state.lawan_duel = lawan
                st.session_state.kuis_duel = True
            else: st.error("Belum ada pemain lain yang terdaftar!")
            
    if st.session_state.lawan_duel and st.session_state.kuis_duel:
        l_nama, l_pts = st.session_state.lawan_duel
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Papan VS Ala Game Fighting
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='glass-card' style='border-color:#00C6FF;'><h2 style='color:#00C6FF; margin:0;'>{player}</h2><p>⭐ {points_db} XP</p></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div style='text-align:center; margin-top:20px;'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='glass-card' style='border-color:#FF416C;'><h2 style='color:#FF416C; margin:0;'>{l_nama}</h2><p>⭐ {l_pts} XP</p></div>", unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
        st.markdown(f"### 🎯 SERANGAN KILAT: {mapel_duel.upper()}")
        ds = DATABASE_KUIS[mapel_duel]
        st.write(ds['soal'])
        j_user = st.radio("Pilih Serangan:", ds['opsi'], key="duel_ans")
        
        if st.button("⚡ EKSEKUSI SERANGAN"):
            if j_user == ds['jaw']:
                # Menang! Curi Poin
                cursor.execute("UPDATE users SET points = points + 100 WHERE username=?", (player,))
                cursor.execute("UPDATE users SET points = MAX(0, points - 20) WHERE username=?", (l_nama,))
                conn.commit()
                st.toast(f"CRITICAL STRIKE! Kamu mencuri XP dari {l_nama}!", icon="⚔️")
                st.session_state.kuis_duel = False # Reset duel
                st.success(f"🎉 **KAMU MENANG!** +100 XP didapatkan. {l_nama} kehilangan 20 XP.")
            else:
                cursor.execute("UPDATE users SET points = MAX(0, points - 30) WHERE username=?", (player,))
                conn.commit()
                st.toast("SERANGAN GAGAL! Kamu kehilangan XP.", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"💀 **KAMU KALAH!** Jawaban keliru. Kamu kehilangan 30 XP.")
            if st.button("🔄 Segarkan Papan Skor"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: ARENA BELAJAR (KUIS & MATERI BACAAN)
# ==========================================
elif menu == "📖 Arena Belajar Kuis":
    st.markdown("<h1>📖 <span class='gradient-text'>ARENA BACA & TUGAS</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 20px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("Mata Pelajaran:", list(DATA_MATERI.keys()))
        with col2: p_kelas = st.selectbox("Tingkat Kelas:", list(DATA_MATERI[p_mapel].keys()))
        col3, col4 = st.columns(2)
        with col3: p_bab = st.selectbox("Sektor Bab:", list(DATA_MATERI[p_mapel][p_kelas].keys()))
        with col4: p_sub = st.selectbox("Sub-bab:", DATA_MATERI[p_mapel][p_kelas][p_bab]["sub_bab"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    tab_mat, tab_doc = st.tabs(["📌 Rangkuman & Latihan", "📂 Modul PDF"])
    
    with tab_mat:
        st.markdown(f"<div class='glass-card' style='text-align:left; border-left: 5px solid #00C6FF;'><h3>📜 Intisari {p_bab}</h3>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        
        id_k = f"q_{p_mapel}_{p_kelas}_{p_bab}"
        if p_mapel in DATABASE_KUIS:
            ds = DATABASE_KUIS[p_mapel]
            st.markdown("<div class='glass-card' style='text-align:left;'><h3>🎯 UJI PEMAHAMAN</h3>", unsafe_allow_html=True)
            st.write(ds['soal'])
            ans = st.radio("Pilih Jawaban:", ds['opsi'], key=f"r_{id_k}")
            if st.button("JAWAB & KLAIM XP"):
                if ans == ds['jaw']:
                    if id_k not in learned_db:
                        cursor.execute("INSERT INTO kuis_history VALUES (?, ?)", (player, id_k))
                        cursor.execute(f"UPDATE users SET points = points + 50, {p_mapel.lower()} = {p_mapel.lower()} + 20 WHERE username = ?", (player,))
                        conn.commit()
                        st.toast("Hebat! +50 XP ditambahkan!", icon="🚀")
                        st.success("💥 Jawaban Benar!")
                    else: st.info("Kamu sudah pernah menyelesaikan kuis ini.")
                else: st.error(f"❌ Keliru. Pembahasan: {ds['pem']}")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_doc:
        folder_t = os.path.join("uploads", bersihkan_nama(p_mapel), bersihkan_nama(p_kelas), bersihkan_nama(p_bab), bersihkan_nama(p_sub))
        if not os.path.exists(folder_t) or len(os.listdir(folder_t)) == 0: st.info("📭 Tidak ada modul dari guru/admin.")
        else:
            for f in os.listdir(folder_t):
                with open(os.path.join(folder_t, f), "rb") as file: st.download_button(f"⬇️ Unduh Berkas: {f}", data=file.read(), file_name=f)

# ==========================================
# HALAMAN 4: TERMINAL ADMIN & UPLOAD
# ==========================================
elif menu == "📤 Terminal Berkas (Admin)":
    st.markdown("<h1>📤 <span class='gradient-text'>CONSOLE ADMINISTRATOR</span></h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='border-color:#EF4444;'><h2>🔒 RESTRICTED AREA</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Kode Otorisasi (Password Admin):", type="password")
        if st.button("Buka Konsol"):
            if pwd == PASSWORD_ADMIN:
                st.session_state.is_admin = True
                st.rerun()
            else: st.error("Akses Ditolak!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("🔓 Otorisasi Diterima. Selamat bekerja, Admin.")
        tab_up, tab_del = st.tabs(["📤 Upload Materi", "🗑️ Hapus Server File"])
        
        with tab_up:
            c1, c2 = st.columns(2)
            with c1: p_mapel = st.selectbox("Mapel:", list(DATA_MATERI.keys()))
            with c2: p_kelas = st.selectbox("Kelas:", list(DATA_MATERI[p_mapel].keys()))
            c3, c4 = st.columns(2)
            with c3: p_bab = st.selectbox("Bab:", list(DATA_MATERI[p_mapel][p_kelas].keys()))
            with c4: p_sub = st.selectbox("Sub-bab:", DATA_MATERI[p_mapel][p_kelas][p_bab]["sub_bab"])
            
            up_file = st.file_uploader("Pilih Berkas (PDF/PPT):", type=['pdf', 'docx', 'xlsx', 'pptx'])
            if up_file and st.button("🚀 UNGGAH KE SERVER CLOUD"):
                ft = os.path.join("uploads", bersihkan_nama(p_mapel), bersihkan_nama(p_kelas), bersihkan_nama(p_bab), bersihkan_nama(p_sub))
                if not os.path.exists(ft): os.makedirs(ft)
                with open(os.path.join(ft, up_file.name), "wb") as f: f.write(up_file.getbuffer())
                st.toast("Upload Sukses!", icon="✅")
                
        with tab_del:
            if os.path.exists("uploads"):
                for r, d, f_list in os.walk("uploads"):
                    for file in f_list:
                        path = os.path.join(r, file)
                        c_a, c_b = st.columns([4,1])
                        c_a.code(path)
                        if c_b.button("🗑️ Del", key=path): os.remove(path); st.rerun()
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("🔴 TUTUP KONSOL ADMIN"): st.session_state.is_admin = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 5: PASAR GELAR & KARAKTER
# ==========================================
elif menu == "🛒 Pasar Gelar & Profil":
    st.markdown("<h1>🛒 <span class='gradient-text'>BLACK MARKET PROFIL</span></h1>", unsafe_allow_html=True)
    tab_av, tab_gl = st.tabs(["👤 Kloning Karakter Utama", "👑 Beli Julukan Elit"])
    
    with tab_av:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            if st.button("PILIH GENI US"):
                cursor.execute("UPDATE users SET avatar_name='Geni Us' WHERE username=?", (player,))
                conn.commit(); st.toast("Karakter Diperbarui!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            if st.button("PILIH SMAR T"):
                cursor.execute("UPDATE users SET avatar_name='Smar T' WHERE username=?", (player,))
                conn.commit(); st.toast("Karakter Diperbarui!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left;'><h3>Bursa Julukan Ksatria</h3>", unsafe_allow_html=True)
        st.write(f"Sisa XP kamu: ⭐ **{points_db} XP**")
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
                            cursor.execute("UPDATE users SET title=?, points=points-? WHERE username=?", (gelar, harga, player))
                            conn.commit(); st.toast(f"Julukan {gelar} Terpasang!", icon="👑"); st.rerun()
                        else: st.error("XP Kurang!")
        st.markdown("</div>", unsafe_allow_html=True)
