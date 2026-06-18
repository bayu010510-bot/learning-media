import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
import base64
import random
import sqlite3
import hashlib

# --- SISTEM DATABASE MULTIPLAYER V2 ---
conn = sqlite3.connect("learning_media_pro.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users_v2 (
    username TEXT PRIMARY KEY,
    password TEXT,
    avatar_name TEXT,
    title TEXT,
    points INTEGER,
    streak INTEGER,
    matematika INT, fisika INT, kimia INT, biologi INT, sejarah INT, ekonomi INT, sosiologi INT
)
""")
cursor.execute("CREATE TABLE IF NOT EXISTS kuis_history_v2 (username TEXT, id_kuis TEXT, PRIMARY KEY(username, id_kuis))")
conn.commit()

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media | Edisi Esports", page_icon="⚔️", layout="wide", initial_sidebar_state="expanded")

# --- INISIALISASI MEMORI ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "gacha_claimed" not in st.session_state: st.session_state.gacha_claimed = False
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "drill_aktif" not in st.session_state: st.session_state.drill_aktif = False
if "soal_drill_saat_ini" not in st.session_state: st.session_state.soal_drill_saat_ini = []

PASSWORD_ADMIN = "LEARNWITHLM"

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def bersihkan_nama(teks): return re.sub(r'[\\/*?:"<>|]', "", teks)

# ==========================================
# IMPORT DATA DARI FILE EKSTERNAL
# ==========================================
from materi import DATA_MATERI
from database_soal import BANK_SOAL_PRO

DAFTAR_GELAR = {"⚡ Petarung Cepat": 150, "🧪 Alkemis Gila": 200, "👑 Raja Duel": 400, "🌌 Penguasa Server": 1000}

# --- KUSTOMISASI CSS HOLOGRAFIS & NEON ---
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
    
    .stButton>button { background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease; width: 100%; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4); }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 0 25px rgba(0, 198, 255, 0.7); }
    .btn-red>button { background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); }
    .btn-red>button:hover { box-shadow: 0 0 25px rgba(255, 75, 43, 0.8); }
    .btn-green>button { background: linear-gradient(135deg, #10B981 0%, #047857 100%); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }
    .btn-green>button:hover { box-shadow: 0 0 25px rgba(16, 185, 129, 0.8); }
    
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
# PORTAL AUTENTIKASI
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; margin-top:50px; font-size:50px;'>Learning Media <span class='gradient-text'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8; margin-bottom:40px;'>Satu Profil, Ribuan Tantangan. Masuk ke Arena Belajar.</p>", unsafe_allow_html=True)
    
    col_space1, col_form, col_space3 = st.columns([1, 1.5, 1])
    with col_form:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 MASUK ARENA", "📝 BUAT PROFIL BARU"])
        
        with tab_log:
            l_user = st.text_input("Username Ksatria:", key="l_usr").strip()
            l_pass = st.text_input("Kata Sandi:", type="password", key="l_pwd").strip()
            if st.button("🚀 LOGIN SEKARANG"):
                if l_user and l_pass:
                    cursor.execute("SELECT username, password FROM users_v2 WHERE lower(username)=lower(?)", (l_user,))
                    res = cursor.fetchone()
                    if res and res[1] == hash_password(l_pass):
                        st.session_state.username = res[0] 
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("❌ Username atau Sandi salah!")
                else: st.warning("Isi semua kolom!")
                
        with tab_reg:
            r_user = st.text_input("Buat Username (Maks 15 Huruf):", max_chars=15, key="r_usr").strip()
            r_pass = st.text_input("Buat Kata Sandi:", type="password", key="r_pwd").strip()
            if st.button("✨ DAFTAR BARU"):
                if r_user and r_pass:
                    cursor.execute("SELECT username FROM users_v2 WHERE lower(username)=lower(?)", (r_user,))
                    if cursor.fetchone(): st.error("⚠️ Username sudah dipakai petarung lain!")
                    else:
                        cursor.execute("""
                            INSERT INTO users_v2 (username, password, avatar_name, title, points, streak, matematika, fisika, kimia, biologi, sejarah, ekonomi, sosiologi)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (r_user, hash_password(r_pass), "Geni Us", "🏅 Pemula", 0, 1, 10, 10, 10, 10, 10, 10, 10))
                        conn.commit()
                        st.success("🎉 Profil Ditempa! Silakan klik tab '🔐 MASUK ARENA' untuk Login.")
                else: st.warning("Isi semua kolom pendaftaran!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# MEMUAT DATA PENGGUNA AKTIF
# ==========================================
player = st.session_state.username
cursor.execute("SELECT * FROM users_v2 WHERE username=?", (player,))
user_data = cursor.fetchone()
avatar_db, title_db, points_db, streak_db = user_data[2], user_data[3], user_data[4], user_data[5]

cursor.execute("SELECT id_kuis FROM kuis_history_v2 WHERE username=?", (player,))
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
    menu = st.radio("SISTEM NAVIGASI", ["🏠 Beranda Server", "⚔️ Mode Duel Ranked (PvP)", "📖 Arena Drill & Latihan", "📤 Terminal Berkas (Admin)", "🛒 Pasar Gelar & Profil"])
    
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
            cursor.execute("UPDATE users_v2 SET points = points + ? WHERE username = ?", (bonus, player))
            conn.commit()
            st.session_state.gacha_claimed = True
            st.toast(f"HORE! Dapat +{bonus} XP!", icon="🎉")
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h2 style='margin:0;'>{streak_db} Hari</h2><p style='color:#94A3B8; margin:0;'>Login Streak</p></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h2 style='margin:0;'>{len(learned_db)}</h2><p style='color:#94A3B8; margin:0;'>Drill Dikuasai</p></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:40px;'>🏆</div><h2 style='color:{tier_color}; margin:0;'>{tier_name.split()[1]}</h2><p style='color:#94A3B8; margin:0;'>Kasta Global</p></div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3>📊 LIVE GLOBAL RANKING</h3>", unsafe_allow_html=True)
    
    cursor.execute("SELECT username, points, title FROM users_v2 ORDER BY points DESC LIMIT 5")
    for i, row in enumerate(cursor.fetchall()):
        medali = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        bg_color = "rgba(255, 215, 0, 0.1)" if i==0 else "rgba(255,255,255,0.02)"
        bdr_color = "rgba(255, 215, 0, 0.5)" if i==0 else "rgba(255,255,255,0.08)"
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid {bdr_color}; border-radius: 15px; padding: 15px 25px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>
            <h3 style='margin:0;'>{medali} {row[0]} <span style='font-size:14px; font-weight:normal; color:#94A3B8;'>({row[2]})</span></h3>
            <h3 style='margin:0; color:#00C6FF;'>⭐ {row[1]} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: MODE DUEL (PvP) MENGGUNAKAN BANK SOAL
# ==========================================
elif menu == "⚔️ Mode Duel Ranked (PvP)":
    st.markdown("<h1>⚔️ <span class='gradient-text'>ARENA DUEL MULTIPLAYER</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8;'>Pilih mata pelajaran, cari lawan acak, jawab 1 kuis tercepat, dan curi XP mereka!</p>", unsafe_allow_html=True)
    
    # Ekstraksi Semua Soal dari Bank Soal ke Pool PvP
    pool_pvp = {}
    for mp, data_kelas in BANK_SOAL_PRO.items():
        pool_pvp[mp] = []
        for kl, data_bab in data_kelas.items():
            for bb, list_soal in data_bab.items():
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
        if st.button("🔍 CARI LAWAN"):
            cursor.execute("SELECT username, points FROM users_v2 WHERE username != ? ORDER BY RANDOM() LIMIT 1", (player,))
            lawan = cursor.fetchone()
            if lawan and len(pool_pvp[mapel_duel]) > 0:
                st.session_state.lawan_duel = lawan
                st.session_state.kuis_duel = True
                soal_asli = random.choice(pool_pvp[mapel_duel])
                opsi_acak = soal_asli["opsi"].copy()
                random.shuffle(opsi_acak)
                st.session_state.soal_pvp_aktif = {"soal": soal_asli["soal"], "opsi": opsi_acak, "jawaban": soal_asli["jawaban"]}
            else: st.error("Tidak ada lawan / soal tersedia!")
            
    if st.session_state.lawan_duel and st.session_state.kuis_duel and st.session_state.soal_pvp_aktif:
        l_nama, l_pts = st.session_state.lawan_duel
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        c_p1, c_vs, c_p2 = st.columns([2,1,2])
        with c_p1: st.markdown(f"<div class='glass-card' style='border-color:#00C6FF;'><h2 style='color:#00C6FF; margin:0;'>{player}</h2><p>⭐ {points_db} XP</p></div>", unsafe_allow_html=True)
        with c_vs: st.markdown("<div style='text-align:center; margin-top:20px;'><span class='vs-text'>VS</span></div>", unsafe_allow_html=True)
        with c_p2: st.markdown(f"<div class='glass-card' style='border-color:#FF416C;'><h2 style='color:#FF416C; margin:0;'>{l_nama}</h2><p>⭐ {l_pts} XP</p></div>", unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
        st.markdown(f"### 🎯 SERANGAN KILAT: {mapel_duel.upper()}")
        ds = st.session_state.soal_pvp_aktif
        st.write(ds['soal'])
        j_user = st.radio("Pilih Serangan:", ds['opsi'], key="duel_ans")
        
        if st.button("⚡ EKSEKUSI SERANGAN"):
            if j_user == ds['jawaban']:
                cursor.execute("UPDATE users_v2 SET points = points + 100 WHERE username=?", (player,))
                cursor.execute("UPDATE users_v2 SET points = MAX(0, points - 20) WHERE username=?", (l_nama,))
                conn.commit()
                st.toast(f"CRITICAL STRIKE! +100 XP", icon="⚔️")
                st.session_state.kuis_duel = False 
                st.success(f"🎉 **KAMU MENANG!** +100 XP. {l_nama} kehilangan 20 XP.")
            else:
                cursor.execute("UPDATE users_v2 SET points = MAX(0, points - 30) WHERE username=?", (player,))
                conn.commit()
                st.toast("GAGAL! -30 XP.", icon="🛡️")
                st.session_state.kuis_duel = False
                st.error(f"💀 **KAMU KALAH!** Kamu kehilangan 30 XP.")
            if st.button("🔄 Lanjut"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: ARENA DRILL & LATIHAN BAB (ENGINE BARU)
# ==========================================
elif menu == "📖 Arena Drill & Latihan":
    st.markdown("<h1>📖 <span class='gradient-text'>ARENA LATIHAN & DRILL UJIAN</span></h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 20px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: p_mapel = st.selectbox("Mata Pelajaran:", list(DATA_MATERI.keys()))
        with col2: p_kelas = st.selectbox("Tingkat Kelas:", list(DATA_MATERI[p_mapel].keys()))
        col3, col4 = st.columns(2)
        with col3: p_bab = st.selectbox("Sektor Bab:", list(DATA_MATERI[p_mapel][p_kelas].keys()))
        with col4: p_sub = st.selectbox("Sub-bab Rangkuman:", DATA_MATERI[p_mapel][p_kelas][p_bab]["sub_bab"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    tab_mat, tab_drill, tab_doc = st.tabs(["📌 Rangkuman", "⚔️ Latihan Drill (Acak)", "📂 Modul Tambahan"])
    
    with tab_mat:
        st.markdown(f"<div class='glass-card' style='text-align:left; border-left: 5px solid #00C6FF;'><h3>📜 Intisari {p_bab}</h3>{DATA_MATERI[p_mapel][p_kelas][p_bab]['rangkuman']}</div>", unsafe_allow_html=True)

    # MESIN DRILL & TEST PEMAHAMAN
    with tab_drill:
        st.markdown("### 🎯 Simulasi Drill Ujian")
        st.caption("Sistem menarik maksimal 5 soal secara acak dari Bank Soal dan mengacak susunan opsi jawabannya.")
        
        soal_tersedia = []
        try: soal_tersedia = BANK_SOAL_PRO[p_mapel][p_kelas][p_bab]
        except KeyError: pass
        
        if not soal_tersedia:
            st.info("📭 Bank Soal untuk Bab ini belum ditambahkan oleh Admin.")
        else:
            if not st.session_state.drill_aktif:
                st.markdown("<div class='btn-green'>", unsafe_allow_html=True)
                if st.button("🚀 MULAI GENERASI SOAL ACAK"):
                    jml_soal = min(5, len(soal_tersedia))
                    soal_terpilih = random.sample(soal_tersedia, jml_soal)
                    data_sesi = []
                    for s in soal_terpilih:
                        opsi_acak = s["opsi"].copy()
                        random.shuffle(opsi_acak)
                        data_sesi.append({
                            "soal": s["soal"], "opsi_acak": opsi_acak, "jawaban_asli": s["jawaban"], "pembahasan": s["pem"]
                        })
                    st.session_state.soal_drill_saat_ini = data_sesi
                    st.session_state.drill_aktif = True
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            else:
                st.warning("⏱️ Sesi Drill Sedang Berjalan. Harap kerjakan dengan teliti!")
                with st.form(key="form_drill"):
                    jawaban_user = []
                    for i, s in enumerate(st.session_state.soal_drill_saat_ini):
                        st.markdown(f"<div class='glass-card' style='text-align:left; padding:20px; margin-bottom:15px;'>", unsafe_allow_html=True)
                        st.markdown(f"**Soal No. {i+1}:**<br>{s['soal']}", unsafe_allow_html=True)
                        ans = st.radio(f"Pilihan No {i+1}:", s['opsi_acak'], key=f"d_ans_{i}")
                        jawaban_user.append(ans)
                        st.markdown("</div>", unsafe_allow_html=True)
                    submit_drill = st.form_submit_button("📝 KUMPULKAN JAWABAN & KOREKSI")
                    
                if submit_drill:
                    skor_benar = 0
                    st.markdown("### 📊 HASIL EVALUASI DRILL")
                    for i, s in enumerate(st.session_state.soal_drill_saat_ini):
                        j_user = jawaban_user[i]
                        j_asli = s['jawaban_asli']
                        if j_user == j_asli:
                            skor_benar += 1
                            st.success(f"✅ **Soal {i+1}: BENAR**")
                        else:
                            st.error(f"❌ **Soal {i+1}: SALAH** | Jawaban kamu: {j_user}")
                            st.info(f"**Pembahasan:** {s['pembahasan']}")
                    
                    total_soal = len(st.session_state.soal_drill_saat_ini)
                    xp_didapat = skor_benar * 30 
                    
                    st.markdown("---")
                    st.markdown(f"### 🏆 SKOR AKHIR: {skor_benar} / {total_soal}")
                    if xp_didapat > 0:
                        cursor.execute(f"UPDATE users_v2 SET points = points + ?, {p_mapel.lower()} = {p_mapel.lower()} + ? WHERE username = ?", (xp_didapat, skor_benar*10, player))
                        id_drill = f"drill_{p_mapel}_{p_kelas}_{p_bab}"
                        if skor_benar == total_soal and id_drill not in learned_db:
                            cursor.execute("INSERT INTO kuis_history_v2 VALUES (?, ?)", (player, id_drill))
                        conn.commit()
                        st.success(f"🎉 Kamu mendapatkan **+{xp_didapat} XP** dari sesi latihan ini!")
                        st.balloons()
                    else: st.warning("⚠️ Belum ada yang benar. Pelajari lagi dan coba kembali!")
                    
                    if st.button("🔄 Akhiri Sesi & Mulai Ulang"):
                        st.session_state.drill_aktif = False
                        st.rerun()

    with tab_doc:
        folder_t = os.path.join("uploads", bersihkan_nama(p_mapel), bersihkan_nama(p_kelas), bersihkan_nama(p_bab), bersihkan_nama(p_sub))
        if not os.path.exists(folder_t) or len(os.listdir(folder_t)) == 0: st.info("📭 Tidak ada modul PDF dari guru/admin.")
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
                cursor.execute("UPDATE users_v2 SET avatar_name='Geni Us' WHERE username=?", (player,))
                conn.commit(); st.toast("Karakter Diperbarui!", icon="👗"); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            if st.button("PILIH SMAR T"):
                cursor.execute("UPDATE users_v2 SET avatar_name='Smar T' WHERE username=?", (player,))
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
                            cursor.execute("UPDATE users_v2 SET title=?, points=points-? WHERE username=?", (gelar, harga, player))
                            conn.commit(); st.toast(f"Julukan {gelar} Terpasang!", icon="👑"); st.rerun()
                        else: st.error("XP Kurang!")
        st.markdown("</div>", unsafe_allow_html=True)
