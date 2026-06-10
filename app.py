import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
import base64

# Sistem anti-error untuk grafik canggih
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media Pro | Edisi Mythic", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

# --- INISIALISASI MEMORI (ENGINE RPG & ANALITIK) ---
if "user_points" not in st.session_state: st.session_state.user_points = 0
if "learned_chapters" not in st.session_state: st.session_state.learned_chapters = set()
if "avatar_name" not in st.session_state: st.session_state.avatar_name = "Geni Us"
if "user_title" not in st.session_state: st.session_state.user_title = "Pemula"
if "unlocked_titles" not in st.session_state: st.session_state.unlocked_titles = ["Pemula"]
if "daily_streak" not in st.session_state: st.session_state.daily_streak = 5
if "mastery" not in st.session_state: 
    # Poin kecerdasan dasar tiap mapel untuk grafik Radar
    st.session_state.mastery = {"Matematika": 10, "Fisika": 10, "Kimia": 10, "Biologi": 10, "Sejarah": 10, "Ekonomi": 10, "Sosiologi": 10}

# --- SISTEM KALKULASI RANK (KASTA TIER) ---
st.session_state.user_level = (st.session_state.user_points // 100) + 1

def get_tier(level):
    if level < 3: return "🥉 Bronze", "#CD7F32"
    elif level < 6: return "🥈 Silver", "#C0C0C0"
    elif level < 10: return "🥇 Gold", "#FFD700"
    elif level < 15: return "💎 Platinum", "#00EDFF"
    else: return "🌌 Mythic", "#9D00FF"

tier_name, tier_color = get_tier(st.session_state.user_level)

# --- KUSTOMISASI CSS ANIMASI & PERBAIKAN DROPDOWN ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .stApp {{ background-color: #0F172A; background-image: radial-gradient(circle at 50% 0%, #1E293B 0%, #0F172A 100%); color: white; }}
    
    /* Hanya Header dan Paragraf yang putih, agar komponen lain tidak rusak */
    h1, h2, h3, h4, h5, p {{ color: #F8FAFC; }}
    
    /* PERBAIKAN KOTAK DROPDOWN (SELECTBOX) */
    .stSelectbox label p {{ color: #00C6FF !important; font-weight: 800; letter-spacing: 0.5px; }} /* Judul Dropdown Neon */
    div[data-baseweb="select"] {{ background-color: #F8FAFC !important; border-radius: 10px; border: 2px solid #334155; }}
    div[data-baseweb="select"] span {{ color: #0F172A !important; font-weight: 600; }} /* Teks Opsi Terpilih (Gelap) */
    ul[role="listbox"] span {{ color: #0F172A !important; font-weight: 600; }} /* Teks di dalam list (Gelap) */
    
    /* Animasi Melayang untuk Avatar */
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .floating-avatar {{ animation: float 4s ease-in-out infinite; }}
    
    /* Efek Kaca (Glassmorphism) & Glow */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px; text-align: center; transition: all 0.3s ease;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}
    .glass-card:hover {{ transform: translateY(-5px); border: 1px solid rgba(59, 130, 246, 0.5); box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }}
    
    /* Tombol Super Premium */
    .stButton>button {{ 
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 800; 
        text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ box-shadow: 0 0 20px rgba(0, 198, 255, 0.6); transform: scale(1.02); }}
    
    /* Label Tier */
    .tier-badge {{ background: {tier_color}40; color: {tier_color}; padding: 6px 15px; border-radius: 20px; font-weight: 800; border: 1px solid {tier_color}; display: inline-block; box-shadow: 0 0 10px {tier_color}40; }}
    
    /* Sidebar Styling Override */
    [data-testid="stSidebar"] {{ background-color: #1E293B !important; border-right: 1px solid #334155; }}
    </style>
    """, unsafe_allow_html=True)

from materi import DATA_MATERI

# Database Kuis Ringkas
DATABASE_KUIS = {
    "Matematika": {"soal": "Jika $2^{x+1} = 16$, nilai $x$ adalah?", "opsi": ["2", "3", "4", "5"], "jaw": "3", "pem": "Sederhanakan jadi $2^{x+1} = 2^4$. Maka $x+1=4 \\Rightarrow x=3$."},
    "Fisika": {"soal": "Energi potensial benda 2 kg di ketinggian 10 m (g=10)?", "opsi": ["100 J", "200 J", "300 J", "400 J"], "jaw": "200 J", "pem": "Ep = m.g.h = $2 \\times 10 \\times 10 = 200$ Joule."},
    "Kimia": {"soal": "Kondisi di mana laju reaksi ke kanan dan kiri sama disebut?", "opsi": ["Katalis", "Kesetimbangan Dinamis", "Reaksi Eksoterm", "Redoks"], "jaw": "Kesetimbangan Dinamis", "pem": "Kesetimbangan tercapai saat V1 (kanan) = V2 (kiri)."},
    "Biologi": {"soal": "Pemisah fauna Asiatis dan Peralihan adalah garis?", "opsi": ["Khatulistiwa", "Wallace", "Weber", "Bujur"], "jaw": "Wallace", "pem": "Garis Wallace memisahkan tipe Asiatis dan Peralihan."},
    "Sejarah": {"soal": "Pengamanan Soekarno-Hatta ke luar Jakarta disebut peristiwa?", "opsi": ["Bandung Lautan Api", "Rengasdengklok", "Ambarawa", "Madiun"], "jaw": "Rengasdengklok", "pem": "Golongan muda menculik ke Rengasdengklok pada 16 Agustus 1945."},
    "Ekonomi": {"soal": "Inti masalah ekonomi adalah...", "opsi": ["Inflasi", "Kelangkaan (Scarcity)", "Deflasi", "Monopoli"], "jaw": "Kelangkaan (Scarcity)", "pem": "Kelangkaan: kebutuhan tak terbatas vs alat pemuas terbatas."},
    "Sosiologi": {"soal": "Pengelompokan masyarakat yang sejajar/horizontal disebut...", "opsi": ["Stratifikasi", "Diferensiasi", "Mobilitas", "Konflik"], "jaw": "Diferensiasi", "pem": "Diferensiasi = setara (Suku, Agama). Stratifikasi = bertingkat (Harta)."}
}

# Fungsi Pembaca Avatar Anti-Error
def tampilkan_avatar(keyword):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        for f in os.listdir(current_dir):
            if keyword in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_b64 = base64.b64encode(open(os.path.join(current_dir, f), 'rb').read()).decode()
                st.markdown(f"""<div class="floating-avatar" style="display:flex; justify-content:center;"><img src="data:image/png;base64,{img_b64}" style="width:150px; filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.5));"></div>""", unsafe_allow_html=True)
                return True
    except: pass
    st.markdown(f"<div class='floating-avatar' style='text-align:center; font-size:100px;'>{'👨‍🎓' if keyword=='genius' else '👩‍🎓'}</div>", unsafe_allow_html=True)

# --- SIDEBAR: KOKPIT PEMAIN ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00C6FF; font-weight:800;'>⚡ BATTLE STATS</h2>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    tampilkan_avatar("genius" if st.session_state.avatar_name == "Geni Us" else "smart")
            
    st.markdown(f"<h2 style='text-align:center; margin-top: 15px; margin-bottom: 5px;'>{st.session_state.avatar_name}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom: 20px;'><span class='tier-badge'>{tier_name}</span></div>", unsafe_allow_html=True)
    
    # Progress Bar Neon
    progress_val = st.session_state.user_points % 100
    st.markdown(f"""
        <div style='background-color: #334155; border-radius: 999px; height: 10px; margin: 15px 0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);'>
            <div style='background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%); width: {progress_val}%; height: 100%; border-radius: 999px; box-shadow: 0 0 10px #00C6FF;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 14px; font-weight: bold;'>
            <span style='color:#94A3B8;'>Lvl {st.session_state.user_level}</span>
            <span style='color: #00C6FF; text-shadow: 0 0 5px #00C6FF;'>⭐ {st.session_state.user_points} XP</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px solid #334155;'>", unsafe_allow_html=True)
    menu = st.radio("SISTEM NAVIGASI", ["🏠 Command Center", "⚔️ Arena Pelatihan", "📊 Analitik Kemampuan", "🎭 Ganti Karakter"])

# --- HALAMAN BERANDA ---
if menu == "🏠 Command Center":
    st.markdown("<h1>COMMAND CENTER 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; color:#94A3B8;'>Selesaikan misi belajarmu, taklukkan kuis, dan capai tingkat Mythic!</p>", unsafe_allow_html=True)
    
    # KARTU STATUS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>🔥</div><h3>{st.session_state.daily_streak} Days</h3><p style='color:#94A3B8;'>Login Streak</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='glass-card'><div style='font-size:40px;'>📚</div><h3>{len(st.session_state.learned_chapters)}</h3><p style='color:#94A3B8;'>Materi Diselesaikan</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='glass-card' style='border-color:{tier_color}; box-shadow: 0 0 20px {tier_color}40;'><div style='font-size:40px;'>🏆</div><h3 style='color:{tier_color};'>{tier_name.split()[1]}</h3><p style='color:#94A3B8;'>Kasta Saat Ini</p></div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    
    # LEADERBOARD CYBERPUNK
    st.markdown("<h3>📊 TOP 3 GLOBAL RANKING</h3>", unsafe_allow_html=True)
    data_rank = {"Geni Us": 110, "Smar T": 70, "Eka Bot": 180, "Siti Bot": 50}
    data_rank[st.session_state.avatar_name] = st.session_state.user_points
    ranking = sorted(data_rank.items(), key=lambda x: x[1], reverse=True)[:3]
    
    for i, (nama, skor) in enumerate(ranking):
        medali = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        warna = "rgba(255, 215, 0, 0.1)" if i==0 else "rgba(192, 192, 192, 0.1)" if i==1 else "rgba(205, 127, 50, 0.1)"
        st.markdown(f"""
        <div style='background: {warna}; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;'>
            <h3 style='margin:0;'>{medali} {nama}</h3>
            <h3 style='margin:0; color:#00C6FF; text-shadow: 0 0 10px #00C6FF;'>⭐ {skor} XP</h3>
        </div>
        """, unsafe_allow_html=True)

# --- HALAMAN ARENA (BATTLE MODE) ---
elif menu == "⚔️ Arena Pelatihan":
    st.markdown("<h1>⚔️ BATTLE ARENA & MATERI</h1>", unsafe_allow_html=True)
    
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
        kunci = f"sub_{id_kuis}"
        if kunci not in st.session_state: st.session_state[kunci] = False
            
        if st.button("⚡ SERANG JAWABAN", key=f"b_{id_kuis}"):
            st.session_state[kunci] = True
                
        if st.session_state[kunci]:
            if jawaban_user == ds["jaw"]:
                st.success("💥 CRITICAL HIT! Jawabanmu Benar!")
                if id_kuis not in st.session_state.learned_chapters:
                    st.session_state.learned_chapters.add(id_kuis)
                    st.session_state.user_points += 50
                    st.session_state.mastery[lihat_pelajaran] += 20
                    st.rerun()
            else:
                st.error("🛡️ ATTACK BLOCKED! Jawaban keliru. Cek analisis taktik di bawah.")
            
            st.markdown(f"<div style='background:rgba(255,255,255,0.1); padding:15px; border-radius:10px; margin-top:15px;'><b>🧠 Analisis Taktik:</b><br>{ds['pem']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Sistem belum mendeteksi bos di sektor ini. Klaim poin eksplorasi!")
        if st.button("🏁 Klaim +40 XP Eksplorasi"):
            if id_kuis not in st.session_state.learned_chapters:
                st.session_state.learned_chapters.add(id_kuis)
                st.session_state.user_points += 40
                st.session_state.mastery[lihat_pelajaran] += 10
                st.rerun()

# --- HALAMAN ANALITIK SPIDER-WEB ---
elif menu == "📊 Analitik Kemampuan":
    st.markdown("<h1>📊 PEMETAAN OTAK (SKILL MATRIX)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8;'>Lihat dominasi kecerdasanmu berdasarkan kuis dan materi yang telah diselesaikan.</p>", unsafe_allow_html=True)
    
    if HAS_PLOTLY:
        kategori = list(st.session_state.mastery.keys())
        nilai = list(st.session_state.mastery.values())
        kategori.append(kategori[0]) 
        nilai.append(nilai[0])
        
        fig = go.Figure(data=go.Scatterpolar(
            r=nilai, theta=kategori, fill='toself',
            line_color='#00C6FF', fillcolor='rgba(0, 198, 255, 0.4)',
            marker=dict(color='white', size=8)
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(nilai)+20], color="rgba(255,255,255,0.3)", gridcolor="rgba(255,255,255,0.2)"),
                angularaxis=dict(color="white", gridcolor="rgba(255,255,255,0.2)")
            ),
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Petunjuk:** Jawab kuis dengan benar di *Arena Pelatihan* untuk memperluas jaring kemampuan pada mata pelajaran tertentu!")
    else:
        st.bar_chart(pd.DataFrame.from_dict(st.session_state.mastery, orient='index', columns=['XP Penguasaan']))

# --- HALAMAN AVATAR ---
elif menu == "🎭 Ganti Karakter":
    st.markdown("<h1>🎭 SANGGAR KLONING KARAKTER</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
        tampilkan_avatar("genius")
        if st.button("AKTIFKAN PROTOKOL GENI US"):
            st.session_state.avatar_name = "Geni Us"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'><h2>Smar T</h2>", unsafe_allow_html=True)
        tampilkan_avatar("smart")
        if st.button("AKTIFKAN PROTOKOL SMAR T"):
            st.session_state.avatar_name = "Smar T"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
