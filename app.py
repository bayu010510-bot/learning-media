import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
from materi import DATA_MATERI

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media Pro", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# --- INISIALISASI MEMORI USER ---
if "user_points" not in st.session_state: st.session_state.user_points = 0
if "learned_chapters" not in st.session_state: st.session_state.learned_chapters = set()
if "avatar_name" not in st.session_state: st.session_state.avatar_name = "Geni Us"

# Konversi Poin ke Level
st.session_state.user_level = (st.session_state.user_points // 100) + 1

# --- DATABASE KUIS INTERAKTIF (STANDAR UTBK / KURIKULUM MERDEKA) ---
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

# --- KUSTOMISASI CSS PREMIUM (Gaya Aplikasi EdTech) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    h1 { color: #0F172A; font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { color: #1E293B; font-weight: 600; }
    
    /* Desain Tombol */
    .stButton>button { 
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white; border-radius: 10px; border: none; padding: 12px 24px; font-weight: 600; width: 100%; 
        transition: all 0.3s ease; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3); }
    
    /* Kotak Rangkuman & Kuis */
    .materi-box { background-color: white; padding: 24px; border-radius: 12px; border-left: 5px solid #3B82F6; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .kuis-box { background-color: #FFFFFF; padding: 25px; border-radius: 16px; border: 2px solid #E2E8F0; margin-top: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); }
    .pembahasan-box { background-color: #F1F5F9; padding: 20px; border-radius: 12px; border-left: 4px solid #475569; margin-top: 15px; }
    
    .dashboard-card { background-color: white; padding: 24px; border-radius: 16px; border: 1px solid #E2E8F0; text-align: center; height: 100%; }
    .icon-wrapper { font-size: 40px; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PEMBERSIH & PENCARI GAMBAR ---
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

# --- SIDEBAR: NAVIGASI & PROFIL PELAJAR ---
with st.sidebar:
    st.markdown("<h3 style='text-align:center; color:#0F172A; margin-bottom: 20px;'>✨ Ruang Siswa</h3>", unsafe_allow_html=True)
    
    col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
    with col_img2:
        if st.session_state.avatar_name == "Geni Us": tampilkan_avatar("genius", "👨‍🎓")
        else: tampilkan_avatar("smart", "👩‍🎓")
            
    st.markdown(f"<h3 style='text-align:center; margin-top: 10px; margin-bottom: 0; color:#1E293B;'>{st.session_state.avatar_name}</h3>", unsafe_allow_html=True)
    
    # Progress Bar XP Level Up
    progress_val = st.session_state.user_points % 100
    st.markdown(f"""
        <div style='background-color: #E2E8F0; border-radius: 999px; height: 8px; margin: 15px 0;'>
            <div style='background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%); width: {progress_val}%; height: 100%; border-radius: 999px;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 14px; color: #64748B;'>
            <span>Lvl {st.session_state.user_level}</span>
            <span style='font-weight: 600; color: #2563EB;'>⭐ {st.session_state.user_points} PTS</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border:1px dashed #CBD5E1; margin: 24px 0;'>", unsafe_allow_html=True)
    menu = st.radio("Navigasi Menu", ["🏠 Beranda", "📖 Ruang Belajar", "📤 Upload Materi", "🎭 Pilih Avatar"], label_visibility="collapsed")

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.markdown("<h1>Selamat Datang di Portal Belajar! 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #64748B; margin-bottom: 30px;'>Baca materi rangkuman, jawab kuis instan, dan tingkatkan skor Level tokomu!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='dashboard-card'><div class='icon-wrapper'>🔥</div><h3>{st.session_state.user_level}</h3><p style='color:#64748B; margin:0;'>Level Akun</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='dashboard-card'><div class='icon-wrapper'>🏆</div><h3>{st.session_state.user_points}</h3><p style='color:#64748B; margin:0;'>Total Poin XP</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='dashboard-card'><div class='icon-wrapper'>⚡</div><h3>{len(st.session_state.learned_chapters)}</h3><p style='color:#64748B; margin:0;'>Materi Dikuasai</p></div>", unsafe_allow_html=True)
        
    st.write("<br>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)

# --- HALAMAN RUANG BELAJAR (KUBAH ENGINE KUIS TERINTEGRASI) ---
elif menu == "📖 Ruang Belajar":
    st.markdown("<h1>📖 Ruang Belajar Interaktif</h1>", unsafe_allow_html=True)
    
    # Kotak Filter Silabus
    st.markdown("<div style='background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0; margin-bottom: 24px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: lihat_pelajaran = st.selectbox("📚 Pilih Mata Pelajaran:", list(DATA_MATERI.keys()))
    with col2: lihat_kelas = st.selectbox("🎓 Pilih Kelas:", list(DATA_MATERI[lihat_pelajaran].keys()))
    col3, col4 = st.columns(2)
    with col3: lihat_bab = st.selectbox("📑 Pilih Bab Materi:", list(DATA_MATERI[lihat_pelajaran][lihat_kelas].keys()))
    with col4: lihat_subbab = st.selectbox("🔖 Detail Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]["sub_bab"])
    st.markdown("</div>", unsafe_allow_html=True)
        
    tab1, tab2 = st.tabs(["📌 Intisari Materi & Kuis Arena", "📂 Berkas Tambahan (Download)"])
    
    with tab1:
        st.markdown(f"### 📝 Rangkuman: {lihat_bab}")
        st.markdown(f"<div class='materi-box'>{DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]['rangkuman']}</div>", unsafe_allow_html=True)
        
        # --- ENGINE KUIS INTERAKTIF (ALA RUANGGURU) ---
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 Kuis Evaluasi Kilat")
        
        id_kuis = f"quiz_{lihat_pelajaran}_{lihat_kelas}_{lihat_bab}"
        
        # Memeriksa apakah mata pelajaran ini memiliki kuis di database
        if lihat_pelajaran in DATABASE_KUIS:
            data_soal = DATABASE_KUIS[lihat_pelajaran]
            
            st.markdown("<div class='kuis-box'>", unsafe_allow_html=True)
            st.markdown(f"**Pertanyaan:** \n{data_soal['soal']}")
            
            # Form Pilihan Ganda
            pilihan_siswa = st.radio("Pilih jawaban yang menurutmu paling benar:", data_soal["opsi"], key=f"radio_{id_kuis}")
            
            # Membuat ID unik status kirim kuis di session_state
            key_submit = f"submit_{id_kuis}"
            if key_submit not in st.session_state:
                st.session_state[key_submit] = False
                
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.button("🚀 Cek Jawaban", key=f"btn_{id_kuis}"):
                    st.session_state[key_submit] = True
                    
            # Logika Koreksi Instan & Pembahasan
            if st.session_state[key_submit]:
                if pilihan_siswa == data_soal["jawaban"]:
                    st.success("🎉 **Luar Biasa, Jawabanmu Benar!** (+40 PTS Masuk Rekening Skor)")
                    # Tambah poin jika bab belum pernah diselesaikan
                    if id_kuis not in st.session_state.learned_chapters:
                        st.session_state.learned_chapters.add(id_kuis)
                        st.session_state.user_points += 40
                        st.rerun()
                else:
                    st.error("❌ **Aduh, Jawabanmu Masih Kurang Tepat!** Jangan menyerah, pelajari pembahasan di bawah.")
                
                # Kotak Eksposisi Pembahasan Instan
                st.markdown("<div class='pembahasan-box'>", unsafe_allow_html=True)
                st.markdown("#### 🧠 Pembahasan Lengkap:")
                st.markdown(data_soal["pembahasan"])
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Fallback jika kuis mata pelajaran tertentu belum di-input ke database
            st.info("💡 Rangkuman selesai! Klik di bawah untuk mengklaim poin membaca.")
            if id_kuis in st.session_state.learned_chapters:
                st.success("✅ Kamu sudah mengambil poin dari bab ini.")
            else:
                if st.button("🏁 Ambil Bonus +40 PTS Membaca", key=f"fallback_{id_kuis}"):
                    st.session_state.learned_chapters.add(id_kuis)
                    st.session_state.user_points += 40
                    st.rerun()
                
    with tab2:
        folder_target = os.path.join("uploads", bersihkan_nama(lihat_pelajaran), bersihkan_nama(lihat_kelas), bersihkan_nama(lihat_bab), bersihkan_nama(lihat_subbab))
        if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
            st.info("📭 Belum ada file tugas/modul PDF untuk sub-bab ini. Silakan kontribusi di menu Upload!")
        else:
            for file in os.listdir(folder_target):
                file_path = os.path.join(folder_target, file)
                with st.expander(f"📄 Berkas Dokumen: {file}"):
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Unduh Berkas", data=f.read(), file_name=file, key=file_path)
                    except: st.error("Gagal memuat sistem unduhan.")

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.markdown("<h1>📤 Pusat Kontribusi Materi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B;'>Unggah berkas tugas atau bahan ajar untuk berbagi dengan rekan pelajar lainnya.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: pilih_pelajaran = st.selectbox("📚 Pilih Mata Pelajaran:", list(DATA_MATERI.keys()))
    with col2: pilih_kelas = st.selectbox("🎓 Pilih Kelas Target:", list(DATA_MATERI[pilih_pelajaran].keys()))
    col3, col4 = st.columns(2)
    with col3: pilih_bab = st.selectbox("📑 Pilih Target Bab:", list(DATA_MATERI[pilih_pelajaran][pilih_kelas].keys()))
    with col4: pilih_subbab = st.selectbox("🔖 Target Sub-bab:", DATA_MATERI[pilih_pelajaran][pilih_kelas][pilih_bab]["sub_bab"])
        
    st.write("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Seret file tugas ke sini (PDF, Gambar, PPTX)", type=['jpg', 'png', 'pdf', 'docx', 'xlsx', 'pptx'])
    
    if uploaded_file is not None:
        st.info(f"Berkas '{uploaded_file.name}' siap dikirim.")
        if st.button("🚀 Luncurkan ke Folder Server"):
            folder_tujuan = os.path.join("uploads", bersihkan_nama(pilih_pelajaran), bersihkan_nama(pilih_kelas), bersihkan_nama(pilih_bab), bersihkan_nama(pilih_subbab))
            if not os.path.exists(folder_tujuan): os.makedirs(folder_tujuan)
            with open(os.path.join(folder_tujuan, uploaded_file.name), "wb") as f: f.write(uploaded_file.getbuffer())
            st.success("🎉 Sukses! Berkasmu telah disimpan dan kini tersedia di tab download siswa.")

# --- HALAMAN PEMILIHAN AVATAR ---
elif menu == "🎭 Pilih Avatar":
    st.markdown("<h1>🎭 Studio Ganti Avatar Kelulusan</h1>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div style='background-color:white; padding:25px; border-radius:16px; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h2>Geni Us</h2>", unsafe_allow_html=True)
        tampilkan_avatar("genius", "👨‍🎓")
        st.write("Si Pintar Yang Ceria, Berprestasi, Ijazah di Tangan!")
        if st.button("PILIH GENI US", key="select_genius"):
            st.session_state.avatar_name = "Geni Us"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div style='background-color:white; padding:25px; border-radius:16px; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h2>Smar T</h2>", unsafe_allow_html=True)
        tampilkan_avatar("smart", "👩‍🎓")
        st.write("Si Cerdas Juara, Medali Emas Kebanggaan di Leher!")
        if st.button("PILIH SMAR T", key="select_smart"):
            st.session_state.avatar_name = "Smar T"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
