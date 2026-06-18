import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
import base64
import random
import sqlite3

# --- SISTEM DATABASE GLOBAL SINKRON (ONLINE SIMULATION VIA SQLITE) ---
conn = sqlite3.connect("learning_media_pro.db", check_same_thread=False)
cursor = conn.cursor()

# Membuat tabel database untuk menyimpan data semua pengguna secara global
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    avatar_name TEXT,
    title TEXT,
    points INTEGER,
    streak INTEGER,
    matematika INT, fisika INT, kimia INT, biologi INT, sejarah INT, ekonomi INT, sosiologi INT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS kuis_history (
    username TEXT,
    id_kuis TEXT,
    PRIMARY KEY(username, id_kuis)
)
""")
conn.commit()

# Sistem anti-error untuk grafik canggih Plotly
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media Pro | Edisi Cloud", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

# --- KATA SANDI RAHASIA ADMIN ---
PASSWORD_ADMIN = "LEARNWITHLM"

# --- FUNGSI PEMBERSIH NAMA FOLDER & MANAJEMEN FILE ---
def bersihkan_nama(teks):
    return re.sub(r'[\\/*?:"<>|]', "", teks)

# --- SIDEBAR: AUTENTIKASI AKSES ONLINE ---
st.sidebar.markdown("<h2 style='text-align:center; color:#00C6FF; font-weight:800;'>🌐 ONLINE PORTAL</h2>", unsafe_allow_html=True)

# Input Nama Pengguna untuk Sinkronisasi Database Online
user_input = st.sidebar.text_input("Masukan Nama Ksatria Kamu:", value="Geni Us Baru", max_chars=15).strip()
if not user_input:
    user_input = "Ksatria Anonim"

# Load atau Buat Akun Baru di Database Global jika Belum Ada
cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
user_data = cursor.fetchone()

if user_data is None:
    # Daftarkan pengguna baru ke database global
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (user_input, "Geni Us", "🏅 Pemula", 0, 5, 10, 10, 10, 10, 10, 10, 10))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
    user_data = cursor.fetchone()

# Sinkronisasi variabel lokal dengan data dari Database SQL
player_name = user_data[0]
avatar_name_db = user_data[1]
user_title_db = user_data[2]
user_points_db = user_data[3]
daily_streak_db = user_data[4]

# Ambil riwayat kuis dari database
cursor.execute("SELECT id_kuis FROM kuis_history WHERE username = ?", (player_name,))
learned_chapters_db = set([row[0] for row in cursor.fetchall()])

# Hitung Level & Tier berdasarkan poin di Database
user_level = (user_points_db // 100) + 1

def get_tier(level):
    if level < 3: return "🥉 Bronze", "#CD7F32"
    elif level < 6: return "🥈 Silver", "#C0C0C0"
    elif level < 10: return "🥇 Gold", "#FFD700"
    elif level < 15: return "💎 Platinum", "#00EDFF"
    else: return "🌌 Mythic", "#9D00FF"

tier_name, tier_color = get_tier(user_level)

# --- KUSTOMISASI CSS HOLOGRAFIS & FIXED TEXT COLOUR ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .stApp {{ background-color: #0F172A; background-image: radial-gradient(circle at 50% 0%, #1E293B 0%, #0F172A 100%); color: white; }}
    
    h1, h2, h3, h4, h5, p {{ color: #F8FAFC; }}
    
    /* PERBAIKAN WARNA INPUT & DROPDOWN DROPDOWN */
    .stSelectbox label p, .stTextInput label p {{ color: #00C6FF !important; font-weight: 800; letter-spacing: 0.5px; }}
    div[data-baseweb="select"], div[data-baseweb="input"] {{ background-color: #F8FAFC !important; border-radius: 10px; border: 2px solid #334155; }}
    div[data-baseweb="select"] span, div[data-baseweb="input"] input {{ color: #0F172A !important; font-weight: 600; }} 
    ul[role="listbox"] span {{ color: #0F172A !important; font-weight: 600; }} 
    
    @keyframes float {{ 0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} 100% {{ transform: translateY(0px); }} }}
    .floating-avatar {{ animation: float 4s ease-in-out infinite; }}
    
    .glass-card {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px; text-align: center; transition: all 0.3s ease; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}
    .glass-card:hover {{ transform: translateY(-5px); border: 1px solid rgba(59, 130, 246, 0.5); box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }}
    
    .stButton>button {{ 
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; 
        text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ box-shadow: 0 0 20px rgba(0, 198, 255, 0.6); transform: scale(1.02); }}
    
    .btn-red>button {{ background: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%); box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }}
    .btn-red>button:hover {{ background: linear-gradient(135deg, #F87171 0%, #DC2626 100%); box-shadow: 0 0 25px rgba(239, 68, 68, 0.8); }}
    
    .lootbox-btn>button {{ background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; border: 2px solid #FEF3C7; box-shadow: 0 0 15px rgba(245, 158, 11, 0.5); }}
    .lootbox-btn>button:hover {{ background: linear-gradient(135deg, #FCD34D 0%, #F59E0B 100%); box-shadow: 0 0 25px rgba(245, 158, 11, 0.8); transform: scale(1.05); }}
    
    .tier-badge {{ background: {tier_color}40; color: {tier_color}; padding: 6px 15px; border-radius: 20px; font-weight: 800; border: 1px solid {tier_color}; display: inline-block; box-shadow: 0 0 10px {tier_color}40; }}
    .title-badge {{ background: rgba(0, 198, 255, 0.1); color: #00C6FF; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: 800; border: 1px solid #00C6FF; margin-top: 8px; display: inline-block; }}
    
    [data-testid="stSidebar"] {{ background-color: #1E293B !important; border-right: 1px solid #334155; }}
    </style>
    """, unsafe_allow_html=True)

from materi import DATA_MATERI

DATABASE_KUIS = {
    "Matematika": {"soal": "Jika $2^{x+1} = 16$, nilai $x$ adalah?", "opsi": ["2", "3", "4", "5"], "jaw": "3", "pem": "Sederhanakan jadi $2^{x+1} = 2^4$. Maka $x+1=4 \\Rightarrow x=3$."},
    "Fisika": {"soal": "Energi potensial benda 2 kg di ketinggian 10 m (g=10)?", "opsi": ["100 J", "200 J", "300 J", "400 J"], "jaw": "200 J", "pem": "Ep = m.g.h = $2 \\times 10 \\times 10 = 200$ Joule."},
    "Kimia": {"soal": "Kondisi di mana laju reaksi ke kanan dan kiri sama disebut?", "opsi": ["Katalis", "Kesetimbangan Dinamis", "Reaksi Eksoterm", "Redoks"], "jaw": "Kesetimbangan Dinamis", "pem": "Kesetimbangan tercapai saat V1 (kanan) = V2 (kiri)."},
    "Biologi": {"soal": "Pemisah fauna Asiatis dan Peralihan adalah garis?", "opsi": ["Khatulistiwa", "Wallace", "Weber", "Bujur"], "jaw": "Wallace", "pem": "Garis Wallace memisahkan tipe Asiatis dan Peralihan."},
    "Sejarah": {"soal": "Pengamanan Soekarno-Hatta ke luar Jakarta disebut peristiwa?", "opsi": ["Bandung Lautan Api", "Rengasdengklok", "Ambarawa", "Madiun"], "jaw": "Rengasdengklok", "pem": "Golongan muda menculik ke Rengasdengklok pada 16 Agustus 1945."},
    "Ekonomi": {"soal": "Inti masalah ekonomi adalah...", "opsi": ["Inflasi", "Kelangkaan (Scarcity)", "Deflasi", "Monopoli"], "jaw": "Kelangkaan (Scarcity)", "pem": "Kelangkaan: kebutuhan tak terbatas vs alat pemuas terbatas."},
    "Sosiologi": {"soal": "Pengelompokan masyarakat yang sejajar/horizontal disebut...", "opsi": ["Stratifikasi", "Diferensiasi", "Mobilitas", "Konflik"], "jaw": "Diferensiasi", "pem": "Diferensiasi = setara (Suku, Agama). Stratifikasi = bertingkat (Harta)."}
}

def tampilkan_avatar(keyword):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        for f in os.listdir(current_dir):
            if keyword in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_b64 = base64.b64encode(open(os.path.join(current_dir, f), 'rb').read()).decode()
                st.markdown(f"""<div class="floating-avatar" style="display:flex; justify-content:center;"><img src="data:image/png;base64,{img_b64}" style="width:130px; filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.5));"></div>""", unsafe_allow_html=True)
                return True
    except: pass
    st.markdown(f"<div class='floating-avatar' style='text-align:center; font-size:90px;'>{'👨‍🎓' if keyword=='genius' else '👩‍🎓'}</div>", unsafe_allow_html=True)

# --- TAMPILAN SIDEBAR PROFIL STATS ---
with st.sidebar:
    st.write("<br>", unsafe_allow_html=True)
    tampilkan_avatar("genius" if avatar_name_db == "Geni Us" else "smart")
            
    st.markdown(f"<h3 style='text-align:center; margin-top: 10px; margin-bottom: 0;'>{player_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;'><span class='title-badge'>{user_title_db}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-top:10px; margin-bottom: 15px;'><span class='tier-badge'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    progress_val = user_points_db % 100
    st.markdown(f"""
        <div style='background-color: #334155; border-radius: 999px; height: 10px; margin: 15px 0;'>
            <div style='background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%); width: {progress_val}%; height: 100%; border-radius: 999px; box-shadow: 0 0 10px #00C6FF;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 14px; font-weight: bold;'>
            <span style='color:#94A3B8;'>Lvl {user_level}</span>
            <span style='color: #00C6FF;'>⭐ {user_points_db} XP</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px solid #334155;'>", unsafe_allow_html=True)
    menu = st.radio("SISTEM NAVIGASI", ["🏠 Command Center", "⚔️ Arena Pelatihan", "📤 Upload Materi", "📊 Analitik Kemampuan", "🛒 Pasar Gelar & Avatar"])
    
    # RADIO FOKUS (SPOTIFY)
    st.markdown("<hr style='border:1px solid #334155;'>", unsafe_allow_html=True)
    st.components.v1.html('<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/0vvXsWCC9xrXsKd4FyS8kM?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>', height=160)

# --- HALAMAN BERANDA & REAL-TIME LEADERBOARD ---
if menu == "🏠 Command Center":
    st.markdown(f"<h1>COMMAND CENTER | HELLO {player_name.upper()}! 🚀</h1>", unsafe_allow_html=True)
    
    # SISTEM GACHA HARIAN
    if "gacha_claimed" not in st.session_state: st.session_state.gacha_claimed = False
    if not st.session_state.gacha_claimed:
        st.markdown("<div class='glass-card' style='border-color:#F59E0B; background:rgba(245, 158, 11, 0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FCD34D;'>🎁 Peti Harta Karun Harian Aktif!</h2>", unsafe_allow_html=True)
        if st.button("🗝️ BUKA & KLAIM BONUS XP"):
            bonus = random.choice([20, 50, 100, 200])
            new_pts = user_points_db + bonus
            cursor.execute("UPDATE users SET points = ? WHERE username = ?", (new_pts, player_name))
            conn.commit()
            st.session_state.gacha_claimed = True
            st.success(f"🎉 Selamat! Kamu memenangkan +{bonus} XP Langsung!")
            st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h3>{daily_streak_db} Days</h3><p style='color:#94A3B8;'>Login Streak</p></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h3>{len(learned_chapters_db)}</h3><p style='color:#94A3B8;'>Kuis Ditaklukkan</p></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='glass-card' style='border-color:{tier_color};'><div style='font-size:40px;'>🏆</div><h3 style='color:{tier_color};'>{tier_name.split()[1]}</h3><p style='color:#94A3B8;'>Kasta Saat Ini</p></div>", unsafe_allow_html=True)
        
    # --- GLOBAL MULTIPLAYER LEADERBOARD ---
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h3>📊 LIVE GLOBAL LEADERBOARD (SINKRON ANTAR-SISI)</h3>", unsafe_allow_html=True)
    st.caption("Papan peringkat di bawah ini bersifat riil dan sinkron otomatis dengan pengguna lain yang sedang online.")
    
    cursor.execute("SELECT username, points, title, avatar_name FROM users ORDER BY points DESC LIMIT 5")
    global_ranking = cursor.fetchall()
    
    for i, row in enumerate(global_ranking):
        medali = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
        bg_color = "rgba(255, 215, 0, 0.08)" if i==0 else "rgba(255,255,255,0.03)"
        st.markdown(f"""
        <div style='background: {bg_color}; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;'>
            <h4 style='margin:0;'>{medali} <b>{row[0]}</b> <span style='font-size:12px; color:gray;'>({row[2]})</span></h4>
            <h3 style='margin:0; color:#00C6FF;'>⭐ {row[1]} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# --- HALAMAN ARENA (BATTLE MODE) ---
elif menu == "⚔️ Arena Pelatihan":
    st.markdown("<h1>⚔️ BATTLE ARENA & SYLLABUS</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='glass-card' style='text-align:left; padding: 30px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: lihat_pelajaran = st.selectbox("Pilih Mata Pelajaran:", list(DATA_MATERI.keys()))
        with col2: lihat_kelas = st.selectbox("Pilih Tingkat Kelas:", list(DATA_MATERI[lihat_pelajaran].keys()))
        col3, col4 = st.columns(2)
        with col3: lihat_bab = st.selectbox("Pilih Sektor Bab:", list(DATA_MATERI[lihat_pelajaran][lihat_kelas].keys()))
        with col4: lihat_subbab = st.selectbox("Target Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]["sub_bab"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📌 Rangkuman & Kuis", "📂 Berkas Tambahan Pelajar"])
    
    with tab1:
        st.markdown(f"### 📜 Intisari: {lihat_bab}")
        st.markdown(f"<div class='glass-card' style='text-align:left; border-left: 5px solid #00C6FF;'>{DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]['rangkuman']}</div>", unsafe_allow_html=True)
            
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 UJI KOMPETENSI (BOSS BATTLE)")
        id_kuis = f"q_{lihat_pelajaran}_{lihat_kelas}_{lihat_bab}"
        
        if lihat_pelajaran in DATABASE_KUIS:
            ds = DATABASE_KUIS[lihat_pelajaran]
            st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
            st.write(f"**Misi Soal:**\n{ds['soal']}")
            
            jawaban_user = st.radio("Pilih Eksekusi Jawaban:", ds["opsi"], key=f"r_{id_kuis}")
            if st.button("⚡ SERANG JAWABAN", key=f"b_{id_kuis}"):
                if jawaban_user == ds["jaw"]:
                    st.success("💥 CRITICAL HIT! Jawabanmu Benar!")
                    if id_kuis not in learned_chapters_db:
                        cursor.execute("INSERT INTO kuis_history VALUES (?, ?)", (player_name, id_kuis))
                        cursor.execute(f"UPDATE users SET points = points + 50, {lihat_pelajaran.lower()} = {lihat_pelajaran.lower()} + 20 WHERE username = ?", (player_name,))
                        conn.commit()
                        st.rerun()
                else:
                    st.error("🛡️ ATTACK BLOCKED! Jawaban keliru.")
                st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; margin-top:15px;'><b>🧠 Analisis Taktik:</b><br>{ds['pem']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        folder_target = os.path.join("uploads", bersihkan_nama(lihat_pelajaran), bersihkan_nama(lihat_kelas), bersihkan_nama(lihat_bab), bersihkan_nama(lihat_subbab))
        if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
            st.info("📭 Belum ada berkas tambahan di folder cloud sub-bab ini.")
        else:
            for file in os.listdir(folder_target):
                file_path = os.path.join(folder_target, file)
                with st.expander(f"📄 Modul: {file}"):
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Unduh Berkas", data=f.read(), file_name=file, key=file_path)
                    except: pass

# --- HALAMAN UPLOAD & MANAJEMEN ADMIN (CRUD FILE BERKAS) ---
elif menu == "📤 Upload Materi":
    st.markdown("<h1>📤 TERMINAL ADMINISTRATOR & UNGGAHAN</h1>", unsafe_allow_html=True)
    
    if "is_admin" not in st.session_state: st.session_state.is_admin = False
    
    if not st.session_state.is_admin:
        st.markdown("<div class='glass-card' style='border-color:#EF4444;'>", unsafe_allow_html=True)
        st.markdown("<h2>🔒 Hak Akses Terbatas (Admin Only)</h2>")
        pwd = st.text_input("Sandi Otorisasi:", type="password")
        if st.button("Masuk Konsol Admin"):
            if pwd == PASSWORD_ADMIN:
                st.session_state.is_admin = True
                st.rerun()
            else: st.error("Sandi Salah!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        tab_up, tab_man = st.tabs(["📤 Unggah Materi Baru", "📋 Dasbor Kendali Berkas (Hapus/Update)"])
        
        with tab_up:
            st.markdown("### Masukkan Materi Tambahan")
            col1, col2 = st.columns(2)
            with col1: pilih_pelajaran = st.selectbox("Mata Pelajaran:", list(DATA_MATERI.keys()))
            with col2: pilih_kelas = st.selectbox("Tingkat Kelas:", list(DATA_MATERI[pilih_pelajaran].keys()))
            col3, col4 = st.columns(2)
            with col3: pilih_bab = st.selectbox("Pilih Bab:", list(DATA_MATERI[pilih_pelajaran][pilih_kelas].keys()))
            with col4: pilih_subbab = st.selectbox("Pilih Sub-bab:", DATA_MATERI[pilih_pelajaran][pilih_kelas][pilih_bab]["sub_bab"])
            
            uploaded_file = st.file_uploader("Pilih Berkas Pelajaran:", type=['pdf', 'docx', 'xlsx', 'pptx', 'png', 'jpg'])
            if uploaded_file is not None:
                if st.button("🚀 PUBLIKASIKAN MATERI"):
                    folder_tujuan = os.path.join("uploads", bersihkan_nama(pilih_pelajaran), bersihkan_nama(pilih_kelas), bersihkan_nama(pilih_bab), bersihkan_nama(pilih_subbab))
                    if not os.path.exists(folder_tujuan): os.makedirs(folder_tujuan)
                    with open(os.path.join(folder_tujuan, uploaded_file.name), "wb") as f: f.write(uploaded_file.getbuffer())
                    st.success("🎉 Berkas berhasil disinkronkan ke cloud server!")
                    st.balloons()
                    
        with tab_man:
            st.markdown("### 🗑️ Penghapusan & Manajemen Dokumen Aktif")
            st.caption("Di bawah ini adalah daftar semua file yang tersimpan di dalam folder uploads sistem Anda. Anda dapat menghapusnya kapan saja.")
            
            basis_folder = "uploads"
            file_lists = []
            if os.path.exists(basis_folder):
                for root, dirs, files in os.walk(basis_folder):
                    for file in files:
                        rel_path = os.path.relpath(os.path.join(root, file), basis_folder)
                        file_lists.append((file, os.path.join(root, file), rel_path))
            
            if len(file_lists) == 0:
                st.info("📭 Server bersih. Tidak ada file materi eksternal saat ini.")
            else:
                for nama_file, path_penuh, r_path in file_lists:
                    col_f1, col_f2 = st.columns([4, 1])
                    with col_f1:
                        st.markdown(f"📁 <code style='color:#00C6FF;'>{r_path}</code>", unsafe_allow_html=True)
                    with col_f2:
                        # Tombol hapus materi untuk Admin (CRUD)
                        if st.button("🗑️ Hapus", key=f"del_{path_penuh}"):
                            try:
                                os.remove(path_penuh)
                                st.success(f"Berhasil menghapus: {nama_file}")
                                st.rerun()
                            except: st.error("Gagal menghapus file.")
                            
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='btn-red'>", unsafe_allow_html=True)
        if st.button("🔴 KELUAR DARI KONSOL ADMIN"):
            st.session_state.is_admin = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- HALAMAN ANALITIK ---
elif menu == "📊 Analitik Kemampuan":
    st.markdown("<h1>📊 MATRIX PETA KEMAMPUAN</h1>", unsafe_allow_html=True)
    
    # Ambil data mastery terbaru dari SQL database milik pengguna aktif
    cursor.execute("SELECT matematika, fisika, kimia, biologi, sejarah, ekonomi, sosiologi FROM users WHERE username = ?", (player_name,))
    m_data = cursor.fetchone()
    
    mastery_dict = {"Matematika": m_data[0], "Fisika": m_data[1], "Kimia": m_data[2], "Biologi": m_data[3], "Sejarah": m_data[4], "Ekonomi": m_data[5], "Sosiologi": m_data[6]}
    
    if HAS_PLOTLY:
        kategori = list(mastery_dict.keys())
        nilai = list(mastery_dict.values())
        kategori.append(kategori[0]) 
        nilai.append(nilai[0])
        fig = go.Figure(data=go.Scatterpolar(r=nilai, theta=kategori, fill='toself', line_color='#00C6FF', fillcolor='rgba(0, 198, 255, 0.4)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(nilai)+20], color="rgba(255,255,255,0.2)"), angularaxis=dict(color="white")), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(pd.DataFrame.from_dict(mastery_dict, orient='index', columns=['XP']))

# --- HALAMAN SANGGAR & BELI GELAR ---
elif menu == "🛒 Pasar Gelar & Avatar":
    st.markdown("<h1>🛒 PASAR UTAMA COIN & JULUKAN</h1>", unsafe_allow_html=True)
    tab_av, tab_gl = st.tabs(["👤 Pilih Karakter Dasar", "👑 Beli Julukan Elit"])
    
    with tab_av:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius")
            if st.button("SET UTAMA: GENI US"):
                cursor.execute("UPDATE users SET avatar_name = 'Geni Us' WHERE username = ?", (player_name,))
                conn.commit()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart")
            if st.button("SET UTAMA: SMAR T"):
                cursor.execute("UPDATE users SET avatar_name = 'Smar T' WHERE username = ?", (player_name,))
                conn.commit()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.markdown("<div class='glass-card' style='text-align:left;'>", unsafe_allow_html=True)
        st.write(f"Tabungan Kamu saat ini: ⭐ **{user_points_db} XP**")
        st.markdown("<hr style='border:1px solid #334155;'>", unsafe_allow_html=True)
        
        for gelar, harga in DAFTAR_GELAR.items():
            c_g1, c_g2, c_g3 = st.columns([3, 1, 1])
            with c_g1: st.markdown(f"#### {gelar}")
            with c_g2: st.markdown(f"<p style='color:#F59E0B;'>💰 {harga} XP</p>", unsafe_allow_html=True)
            with c_g3:
                # Cek jika user sudah memenuhi poin atau sudah punya julukannya
                if user_title_db == gelar:
                    st.button("⚙️ Aktif", key=f"ak_{gelar}", disabled=True)
                else:
                    if st.button("Gunakan / Beli", key=f"by_{gelar}"):
                        if user_points_db >= harga or user_title_db != "🏅 Pemula":
                            # Potong poin jika beli baru (simulasi sederhana)
                            potong = harga if user_points_db >= harga else 0
                            cursor.execute("UPDATE users SET title = ?, points = points - ? WHERE username = ?", (gelar, potong, player_name))
                            conn.commit()
                            st.success("Sukses memasang julukan baru!")
                            st.rerun()
                        else: st.error("XP kamu tidak cukup!")
        st.markdown("</div>", unsafe_allow_html=True)
