import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
from materi import DATA_MATERI

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media Pro", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# --- INISIALISASI MEMORI USER (GAMIFICATION ENGINE) ---
if "user_points" not in st.session_state: st.session_state.user_points = 0
if "learned_chapters" not in st.session_state: st.session_state.learned_chapters = set()
if "avatar_name" not in st.session_state: st.session_state.avatar_name = "Geni Us"
if "user_title" not in st.session_state: st.session_state.user_title = "🏅 Pelajar Pemula"
if "unlocked_titles" not in st.session_state: st.session_state.unlocked_titles = ["🏅 Pelajar Pemula"]
if "daily_streak" not in st.session_state: st.session_state.daily_streak = 3

# Konversi Poin ke Level
st.session_state.user_level = (st.session_state.user_points // 100) + 1

# --- DATABASE KUIS INTERAKTIF UTBK ---
DATABASE_KUIS = {
    "Matematika": {
        "soal": "Jika $2^{x+1} = 16$, berapakah nilai dari $x$?",
        "opsi": ["A. 2", "B. 3", "C. 4", "D. 5"],
        "jawaban": "B. 3",
        "pembahasan": "Sederhanakan persamaan eksponen menjadi basis yang sama:\n\n$2^{x+1} = 2^4$\n\nKarena basisnya sudah sama (2), kita bisa menyamakan pangkatnya:\n\n$x + 1 = 4$\n\n$x = 4 - 1 = 3$.\n\nJadi, nilai $x$ adalah **3**."
    },
    "Fisika": {
        "soal": "Sebuah benda bermassa 2 kg jatuh bebas dari ketinggian 10 meter. Berapakah energi potensial awal benda tersebut jika percepatan gravitasi $g = 10 \\text{ m/s}^2$?",
        "opsi": ["A. 50 Joule", "B. 100 Joule", "C. 200 Joule", "D. 400 Joule"],
        "jawaban": "C. 200 Joule",
        "pembahasan": "Energi Potensial ($Ep$) dihitung menggunakan rumus:\n\n$$Ep = m \\cdot g \\cdot h$$\n\nDiketahui: $m = 2 \\text{ kg}$, $g = 10 \\text{ m/s}^2$, $h = 10 \\text{ m}$.\n\n$$Ep = 2 \\cdot 10 \\cdot 10 = 200 \\text{ Joule}$$\n\nJadi, energi potensial awal benda adalah **200 Joule**."
    },
    "Kimia": {
        "soal": "Manakah di bawah ini yang merupakan salah satu dari 12 prinsip utama Kimia Hijau (Green Chemistry)?",
        "opsi": ["A. Memaksimalkan penggunaan energi fosil", "B. Mencegah timbulnya limbah sejak awal proses", "C. Membuang limbah cair langsung ke sungai", "D. Meningkatkan proses pembakaran terbuka"],
        "jawaban": "B. Mencegah timbulnya limbah sejak awal proses",
        "pembahasan": "Salah satu prinsip utama Kimia Hijau adalah **Mencegah Limbah (Prevention)**. Lebih baik mencegah terbentuknya limbah daripada mengolah atau membersihkan limbah setelah diproduksi."
    },
    "Biologi": {
        "soal": "Garis khayal yang memisahkan wilayah persebaran fauna Indonesia bagian Barat (Asiatis) dengan wilayah bagian Tengah (Peralihan) disebut...",
        "opsi": ["A. Garis Weber", "B. Garis Wallace", "C. Garis Khatulistiwa", "D. Garis Meridian"],
        "jawaban": "B. Garis Wallace",
        "pembahasan": "• **Garis Wallace** memisahkan tipe fauna Asiatis (Barat) dengan tipe Peralihan (Tengah).\n• **Garis Weber** memisahkan tipe fauna Peralihan (Tengah) dengan tipe Australis (Timur)."
    },
    "Sejarah": {
        "soal": "Peristiwa penculikan Ir. Soekarno dan Drs. Moh. Hatta oleh golongan muda ke luar kota menjelang Proklamasi Kemerdekaan dikenal dengan nama peristiwa...",
        "opsi": ["A. Peristiwa Ambarawa", "B. Peristiwa Tiga Daerah", "C. Peristiwa Rengasdengklok", "D. Peristiwa Malari"],
        "jawaban": "C. Peristiwa Rengasdengklok",
        "pembahasan": "Peristiwa **Rengasdengklok** terjadi pada 16 Agustus 1945, di mana golongan muda mengamankan Soekarno dan Hatta agar tidak terpengaruh oleh janji-janji Jepang dan segera memproklamasikan kemerdekaan Indonesia."
    },
    "Ekonomi": {
        "soal": "Kondisi di mana kebutuhan manusia tidak terbatas, sedangkan alat pemuas kebutuhan jumlahnya sangat terbatas dinamakan...",
        "opsi": ["A. Inflasi", "B. Deflasi", "C. Kelangkaan (Scarcity)", "D. Distribusi"],
        "jawaban": "C. Kelangkaan (Scarcity)",
        "pembahasan": "Inti masalah ekonomi modern adalah **Kelangkaan (Scarcity)**, yaitu kesenjangan antara sumber daya ekonomi yang terbatas dengan kebutuhan manusia yang tidak terbatas."
    },
    "Sosiologi": {
        "soal": "Pengelompokan masyarakat secara horizontal atau sejajar berdasarkan ras, suku bangsa, profesi, dan agama tanpa tingkatan vertikal dinamakan...",
        "opsi": ["A. Stratifikasi Sosial", "B. Diferensiasi Sosial", "C. Mobilitas Sosial", "D. Konflik Sosial"],
        "jawaban": "B. Diferensiasi Sosial",
        "pembahasan": "• **Diferensiasi Sosial**: Pengelompokan masyarakat secara horizontal/setara (Suku, Agama, Ras).\n• **Stratifikasi Sosial**: Pelapisan masyarakat secara vertikal/bertingkat (Kekayaan, Jabatan)."
    }
}

# --- STORE SHOP JULUKAN ELIT ---
DAFTAR_GELAR = {
    "👑 Raja Eksponen": 80,
    "⚡ Speedrunner Fisika": 120,
    "🧪 Alkemis Ulung": 160,
    "🧬 Master Genetika": 200,
    "📈 Begawan Ekonomi": 240
}

# --- KUSTOMISASI CSS PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    h1 { color: #0F172A; font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { color: #1E293B; font-weight: 600; }
    
    /* Tombol Premium */
    .stButton>button { 
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 600; width: 100%; 
        transition: all 0.3s ease; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3); }
    
    /* Desain UI Komponen Game */
    .dashboard-card { background-color: white; padding: 24px; border-radius: 16px; border: 1px solid #E2E8F0; text-align: center; height: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
    .podium-box { background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%); border: 2px solid #CBD5E1; padding: 15px; border-radius: 16px; text-align: center; }
    .materi-box { background-color: white; padding: 24px; border-radius: 12px; border-left: 5px solid #3B82F6; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .kuis-box { background-color: #FFFFFF; padding: 25px; border-radius: 16px; border: 2px solid #E2E8F0; margin-top: 20px; }
    .pembahasan-box { background-color: #F8FAFC; padding: 20px; border-radius: 12px; border-left: 4px solid #64748B; margin-top: 15px; }
    .title-badge { background-color: #EFF6FF; color: #1E40AF; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: 600; display: inline-block; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI ASISTEN VISUAL ---
def bersihkan_nama(teks):
    return re.sub(r'[\\/*?:"<>|]', "", teks)

def tampilkan_avatar(keyword, fallback_emoji):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gambar_ditemukan = False
    try:
        for f in os.listdir(current_dir):
            if keyword in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = Image.open(os.path.join(current_dir, f))
                st.image(img, use_column_width=True)
                gambar_ditemukan = True
                break
    except: pass
    if not gambar_ditemukan:
        st.markdown(f"<div style='text-align:center; font-size:80px;'>{fallback_emoji}</div>", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI PERMAINAN ---
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#0F172A; margin-bottom: 10px;'>🎮 Ksatria Pelajar</h3>", unsafe_allow_html=True)
    
    col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
    with col_img2:
        if st.session_state.avatar_name == "Geni Us": tampilkan_avatar("genius", "👨‍🎓")
        else: tampilkan_avatar("smart", "👩‍🎓")
            
    st.markdown(f"<h3 style='text-align:center; margin-top: 5px; margin-bottom: 0; color:#1E293B;'>{st.session_state.avatar_name}</h3>", unsafe_allow_html=True)
    
    # Label Gelar Aktif
    st.markdown(f"<div style='text-align:center;'><span class='title-badge'>{st.session_state.user_title}</span></div>", unsafe_allow_html=True)
    
    # Indikator Streak Harian
    st.markdown(f"<div style='text-align:center; margin-top:10px; font-size:15px;'>🔥 <b>{st.session_state.daily_streak} Hari Beruntun</b></div>", unsafe_allow_html=True)
    
    # XP Progress Bar
    progress_val = st.session_state.user_points % 100
    st.markdown(f"""
        <div style='background-color: #E2E8F0; border-radius: 999px; height: 8px; margin: 15px 0;'>
            <div style='background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%); width: {progress_val}%; height: 100%; border-radius: 999px;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 14px; color: #64748B;'>
            <span>Level {st.session_state.user_level}</span>
            <span style='font-weight: 600; color: #2563EB;'>⭐ {st.session_state.user_points} XP</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px dashed #CBD5E1; margin: 20px 0;'>", unsafe_allow_html=True)
    menu = st.radio("Menu Arena", ["🏠 Dashboard Utama", "📖 Arena Belajar & Kuis", "📤 Kontribusi Berkas", "🎭 Sanggar Avatar & Gelar"], label_visibility="collapsed")

# --- HALAMAN BERANDA & PAPAN PERINGKAT LIVE ---
if menu == "🏠 Dashboard Utama":
    st.markdown("<h1>Dashboard Ksatria Belajar 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#64748B;'>Pantau peringkat kompetisimu dan selesaikan misi harian untuk bonus XP besar.</p>", unsafe_allow_html=True)
    
    # --- KOTAK LIVE LEADERBOARD (PODIUM JUARA) ---
    st.markdown("### 🏆 Papan Peringkat Live Pekan Ini")
    
    # Sistem Kalkulasi Ranking Otomatis Mengikuti Skor Player
    data_kompetitor = {"Geni Us": 110, "Smar T": 70, "Eka Cendekia": 180, "Budi Master": 140, "Siti Juara": 50}
    data_kompetitor[st.session_state.avatar_name] = st.session_state.user_points
    ranking_sorted = sorted(data_kompetitor.items(), key=lambda x: x[1], reverse=True)
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown(f"""<div class='podium-box' style='border-color:#CBD5E1;'>
            <h4 style='color:#64748B; margin:0;'>🥈 Peringkat 2</h4>
            <h3 style='margin:10px 0;'>{ranking_sorted[1][0]}</h3>
            <span class='title-badge' style='background-color:#F1F5F9; color:#475569;'>⭐ {ranking_sorted[1][1]} XP</span>
        </div>""", unsafe_allow_html=True)
    with col_p2:
        st.markdown(f"""<div class='podium-box' style='border-color:#F59E0B; background: linear-gradient(180deg, #FFFDF5 0%, #FEF3C7 100%); transform: translateY(-10px);'>
            <h4 style='color:#D97706; margin:0;'>🥇 Peringkat 1</h4>
            <h2 style='margin:10px 0; color:#92400E;'>{ranking_sorted[0][0]}</h2>
            <span class='title-badge' style='background-color:#FEF3C7; color:#92400E;'>⭐ {ranking_sorted[0][1]} XP</span>
        </div>""", unsafe_allow_html=True)
    with col_p3:
        st.markdown(f"""<div class='podium-box' style='border-color:#B45309;'>
            <h4 style='color:#B45309; margin:0;'>🥉 Peringkat 3</h4>
            <h3 style='margin:10px 0;'>{ranking_sorted[2][0]}</h3>
            <span class='title-badge' style='background-color:#FFEDD5; color:#B45309;'>⭐ {ranking_sorted[2][1]} XP</span>
        </div>""", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    
    # --- QUEST HARIAN TRACKER ---
    st.markdown("### 🎯 Misi Harian Kamu")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.checkbox("📖 Selesaikan 1 Tantangan Kuis Arena (Hadiah +40 XP)", value=len(st.session_state.learned_chapters) > 0, disabled=True)
        st.checkbox("🔥 Pertahankan Streak Belajar di atas 2 hari", value=st.session_state.daily_streak >= 2, disabled=True)
    with col_q2:
        st.checkbox("🎭 Klaim Julukan Elit Pertama di Sanggar Gelar", value=len(st.session_state.unlocked_titles) > 1, disabled=True)
        st.caption("Misi harian akan otomatis tercentang jika kamu melakukan aksi belajarmu!")

# --- HALAMAN ARENA BELAJAR & KUIS INTERAKTIF ---
elif menu == "📖 Arena Belajar & Kuis":
    st.markdown("<h1>📖 Arena Belajar & Kuis Eksklusif</h1>", unsafe_allow_html=True)
    
    st.markdown("<div style='background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0; margin-bottom: 24px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: lihat_pelajaran = st.selectbox("📚 Pilih Mata Pelajaran:", list(DATA_MATERI.keys()))
    with col2: lihat_kelas = st.selectbox("🎓 Pilih Tingkatan Kelas:", list(DATA_MATERI[lihat_pelajaran].keys()))
    col3, col4 = st.columns(2)
    with col3: lihat_bab = st.selectbox("📑 Pilih Bab Pembahasan:", list(DATA_MATERI[lihat_pelajaran][lihat_kelas].keys()))
    with col4: lihat_subbab = st.selectbox("🔖 Detail Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]["sub_bab"])
    st.markdown("</div>", unsafe_allow_html=True)
        
    tab1, tab2 = st.tabs(["📌 Rangkuman & Kuis Terintegrasi", "📂 Bank Berkas Sekolah"])
    
    with tab1:
        st.markdown(f"### 📝 Intisari: {lihat_bab}")
        st.markdown(f"<div class='materi-box'>{DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        
        # KUBAH KUIS ENGINE AUTOMATION
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 Uji Pemahaman Kompetensi (Instan Feedback)")
        
        id_kuis = f"quiz_{lihat_pelajaran}_{lihat_kelas}_{lihat_bab}"
        
        if lihat_pelajaran in DATABASE_KUIS:
            data_soal = DATABASE_KUIS[lihat_pelajaran]
            st.markdown("<div class='kuis-box'>", unsafe_allow_html=True)
            st.write(data_soal['soal'])
            
            pilihan_siswa = st.radio("Klik pada bulatan opsi jawaban:", data_soal["opsi"], key=f"r_{id_kuis}")
            
            key_submit = f"sub_{id_kuis}"
            if key_submit not in st.session_state: st.session_state[key_submit] = False
                
            if st.button("🚀 Koreksi Hasil Jawaban", key=f"b_{id_kuis}"):
                st.session_state[key_submit] = True
                    
            if st.session_state[key_submit]:
                if pilihan_siswa == data_soal["jawaban"]:
                    st.success("🎉 **Jawabanmu Benar Sempurna!** Anda berhak mendapatkan bonus XP.")
                    if id_kuis not in st.session_state.learned_chapters:
                        st.session_state.learned_chapters.add(id_kuis)
                        st.session_state.user_points += 40
                        st.rerun()
                else:
                    st.error("❌ **Jawabanmu Masih Keliru.** Pelajari letak kesalahannya pada pembahasan di bawah ini.")
                
                st.markdown("<div class='pembahasan-box'>", unsafe_allow_html=True)
                st.markdown("#### 🧠 Kotak Pembahasan:")
                st.markdown(data_soal["pembahasan"])
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("💡 Klik tombol di bawah untuk mengambil bonus poin membaca dari materi ini.")
            if id_kuis in st.session_state.learned_chapters:
                st.success("✅ Poin dari materi ini sudah diklaim.")
            else:
                if st.button("🏁 Ambil Bonus +40 XP", key=f"f_{id_kuis}"):
                    st.session_state.learned_chapters.add(id_kuis)
                    st.session_state.user_points += 40
                    st.rerun()
                
    with tab2:
        folder_target = os.path.join("uploads", bersihkan_nama(lihat_pelajaran), bersihkan_nama(lihat_kelas), bersihkan_nama(lihat_bab), bersihkan_nama(lihat_subbab))
        if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
            st.info("📭 Belum ada dokumen PDF/PPT tambahan untuk sub-bab spesifik ini.")
        else:
            for file in os.listdir(folder_target):
                file_path = os.path.join(folder_target, file)
                with st.expander(f"📄 Berkas Pendukung: {file}"):
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Unduh Berkas", data=f.read(), file_name=file, key=file_path)
                    except: st.error("Gagal memuat tombol dokumen.")

# --- HALAMAN UPLOAD ---
elif menu == "📤 Kontribusi Berkas":
    st.markdown("<h1>📤 Pusat Unggah Berkas Berbagi</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: pilih_pelajaran = st.selectbox("📚 Pilihan Mapel:", list(DATA_MATERI.keys()))
    with col2: pilih_kelas = st.selectbox("🎓 Kelas Sasaran:", list(DATA_MATERI[pilih_pelajaran].keys()))
    col3, col4 = st.columns(2)
    with col3: pilih_bab = st.selectbox("📑 Pilihan Bab:", list(DATA_MATERI[pilih_pelajaran][pilih_kelas].keys()))
    with col4: pilih_subbab = st.selectbox("🔖 Sub-bab Sasaran:", DATA_MATERI[pilih_pelajaran][pilih_kelas][pilih_bab]["sub_bab"])
        
    st.write("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Seret lembar tugas ke kotak ini", type=['jpg', 'png', 'pdf', 'docx', 'xlsx', 'pptx'])
    
    if uploaded_file is not None:
        st.info(f"Berkas '{uploaded_file.name}' siap diproses.")
        if st.button("🚀 Unggah Ke Perpustakaan Cloud"):
            folder_tujuan = os.path.join("uploads", bersihkan_nama(pilih_pelajaran), bersihkan_nama(pilih_kelas), bersihkan_nama(pilih_bab), bersihkan_nama(pilih_subbab))
            if not os.path.exists(folder_tujuan): os.makedirs(folder_tujuan)
            with open(os.path.join(folder_tujuan, uploaded_file.name), "wb") as f: f.write(uploaded_file.getbuffer())
            st.success("🎉 Sukses! Materi kontribusimu berhasil dipublikasikan untuk semua siswa.")

# --- HALAMAN PERALIHAN KARAKTER & PASAR GELAR ---
elif menu == "🎭 Sanggar Avatar & Gelar":
    st.markdown("<h1>🎭 Sanggar Karakter & Pasar Gelar</h1>", unsafe_allow_html=True)
    
    tab_av, tab_gl = st.tabs(["👤 Alih Karakter Utama", "👑 Pasar Julukan Elit"])
    
    with tab_av:
        col_av1, col_av2 = st.columns(2)
        with col_av1:
            st.markdown("<div class='dashboard-card'><h2>Geni Us</h2>", unsafe_allow_html=True)
            tampilkan_avatar("genius", "👨‍🎓")
            if st.button("GUNAKAN GENI US", key="s_gen"):
                st.session_state.avatar_name = "Geni Us"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with col_av2:
            st.markdown("<div class='dashboard-card'><h2>Smar T</h2>", unsafe_allow_html=True)
            tampilkan_avatar("smart", "👩‍🎓")
            if st.button("GUNAKAN SMAR T", key="s_sma"):
                st.session_state.avatar_name = "Smar T"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_gl:
        st.subheader("Tukarkan Poin Belajarmu dengan Gelar Kehormatan")
        st.write(f"Tabungan Poinmu saat ini: ⭐ **{st.session_state.user_points} XP**")
        st.markdown("---")
        
        for gelar, harga in DAFTAR_GELAR.items():
            c_g1, c_g2, c_g3 = st.columns([3, 1, 1])
            with c_g1: st.markdown(f"### {gelar}")
            with c_g2: st.write(f"💰 {harga} XP")
            with c_g3:
                if gelar in st.session_state.unlocked_titles:
                    if st.session_state.user_title == gelar:
                        st.button("⚙️ Aktif", key=f"ak_{gelar}", disabled=True)
                    else:
                        if st.button("Gunakan", key=f"gk_{gelar}"):
                            st.session_state.user_title = gelar
                            st.rerun()
                else:
                    if st.button("🛒 Beli", key=f"by_{gelar}"):
                        if st.session_state.user_points >= harga:
                            st.session_state.user_points -= harga
                            st.session_state.unlocked_titles.append(gelar)
                            st.session_state.user_title = gelar
                            st.success(f"Sukses membuka julukan {gelar}!")
                            st.rerun()
                        else:
                            st.error("Skor XP belum cukup!")
