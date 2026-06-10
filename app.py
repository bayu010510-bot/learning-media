import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
import base64
from materi import DATA_MATERI

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media Pro", page_icon="📚", layout="wide")

# --- INISIALISASI MEMORI USER ---
if "user_points" not in st.session_state: st.session_state.user_points = 0
if "learned_chapters" not in st.session_state: st.session_state.learned_chapters = set()
if "avatar_hat" not in st.session_state: st.session_state.avatar_hat = ""
if "unlocked_accessories" not in st.session_state: st.session_state.unlocked_accessories = ["Tanpa Aksesoris"]

# --- SISTEM PEMBACA AVATAR LOKAL AMAN (ANTI ERROR) ---
def get_base64_image(image_path, fallback_url):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return fallback_url

# Membaca gambar yang kamu upload (siswa.png dan siswi.png)
AVATAR_LAKI = get_base64_image("siswa.png", "https://img.icons8.com/illustrations/external-pack-flat-symbols-tanah-basah/200/external-student-back-to-school-pack-flat-symbols-tanah-basah.png")
AVATAR_PEREMPUAN = get_base64_image("siswi.png", "https://img.icons8.com/illustrations/flat-round/200/female-student--v1.png")

if "avatar_base" not in st.session_state:
    st.session_state.avatar_base = AVATAR_LAKI # Default

# --- KUSTOMISASI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #2563EB; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #1D4ED8; transform: scale(1.02); }
    
    .profile-card { background-color: white; border-radius: 16px; padding: 20px; border: 2px solid #E5E7EB; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; }
    .avatar-container { width: 140px; height: 140px; margin: 0 auto 15px auto; position: relative; background: radial-gradient(circle, #EFF6FF 0%, #DBEAFE 100%); border-radius: 50%; border: 4px solid #3B82F6; display: flex; align-items: center; justify-content: center; }
    .avatar-base-img { width: 100px; height: 100px; object-fit: contain; position: absolute; bottom: 10px; z-index: 1; }
    .avatar-hat-img { width: 65px; height: 65px; object-fit: contain; position: absolute; top: -12px; z-index: 2; }
    
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; border: 1px solid #E5E7EB; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PEMBERSIH NAMA FOLDER ---
def bersihkan_nama(teks):
    return re.sub(r'[\\/*?:"<>|]', "", teks)

# Konversi Poin ke Level
st.session_state.user_level = (st.session_state.user_points // 100) + 1

# --- DATABASE GRAFIS TOKO ---
TOKO_AKSESORIS = {
    "👑 Mahkota Emas": {"harga": 100, "url": "https://img.icons8.com/isometric/100/crown.png"},
    "🎧 Headphone Neon": {"harga": 60, "url": "https://img.icons8.com/isometric/100/headphones.png"},
    "🎓 Topi Kelulusan": {"harga": 40, "url": "https://img.icons8.com/isometric/100/mortarboard.png"},
    "🥽 Kacamata Google": {"harga": 50, "url": "https://img.icons8.com/isometric/100/safety-goggles.png"}
}

# --- SIDEBAR & NAVIGASI ---
with st.sidebar:
    hat_element = f"<img class='avatar-hat-img' src='{st.session_state.avatar_hat}'>" if st.session_state.avatar_hat else ""
    st.markdown(f"""
    <div class='profile-card'>
        <div class='avatar-container'>
            {hat_element}
            <img class='avatar-base-img' src='{st.session_state.avatar_base}'>
        </div>
        <h4>Level {st.session_state.user_level}</h4>
        <p style='color:#2563EB; font-weight:bold; margin:0;'>⭐ {st.session_state.user_points} PTS</p>
    </div>
    """, unsafe_allow_html=True)
    
    prog = st.session_state.user_points % 100
    st.progress(prog / 100)
    st.caption(f"ℹ️ {100 - prog} PTS lagi menuju Level {st.session_state.user_level + 1}")
    st.markdown("---")
    menu = st.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Ruang Belajar", "🎭 Kustom Avatar & Toko"])

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Portal Learning Media Pro")
    st.markdown("### Platform Edukasi Lengkap Kurikulum Merdeka (Kelas 10-12).")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)
    st.info("💡 **Petunjuk:** Pilih Ruang Belajar untuk mengakses silabus lengkap 7 Mata Pelajaran!")

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Tambah Materi Baru")
    
    col1, col2 = st.columns(2)
    with col1: pilih_pelajaran = st.selectbox("📖 Pilih Pelajaran:", list(DATA_MATERI.keys()))
    with col2: pilih_kelas = st.selectbox("🎓 Pilih Kelas Target:", list(DATA_MATERI[pilih_pelajaran].keys()))
    
    col3, col4 = st.columns(2)
    with col3: pilih_bab = st.selectbox("📑 Pilih Bab:", list(DATA_MATERI[pilih_pelajaran][pilih_kelas].keys()))
    with col4: pilih_subbab = st.selectbox("🔖 Pilih Sub-bab:", DATA_MATERI[pilih_pelajaran][pilih_kelas][pilih_bab]["sub_bab"])
        
    st.markdown("---")
    uploaded_file = st.file_uploader("Seret file (PDF, PPT, Gambar) ke sini", type=['jpg', 'png', 'pdf', 'docx', 'xlsx', 'pptx'])
    
    if uploaded_file is not None:
        st.warning(f"File '{uploaded_file.name}' siap ditambahkan.")
        if st.button("🚀 Submit Materi Sekarang"):
            folder_tujuan = os.path.join("uploads", bersihkan_nama(pilih_pelajaran), bersihkan_nama(pilih_kelas), bersihkan_nama(pilih_bab), bersihkan_nama(pilih_subbab))
            if not os.path.exists(folder_tujuan): os.makedirs(folder_tujuan)
            with open(os.path.join(folder_tujuan, uploaded_file.name), "wb") as f: f.write(uploaded_file.getbuffer())
            st.success("🎉 Sukses menyimpan materi pelajaran!")
            st.balloons()

# --- HALAMAN RUANG BELAJAR ---
elif menu == "📖 Ruang Belajar":
    st.title("📖 Ruang Belajar Interaktif")
    
    col1, col2 = st.columns(2)
    with col1: lihat_pelajaran = st.selectbox("🔍 Filter Pelajaran:", list(DATA_MATERI.keys()))
    with col2: lihat_kelas = st.selectbox("🔍 Filter Kelas:", list(DATA_MATERI[lihat_pelajaran].keys()))
    
    col3, col4 = st.columns(2)
    with col3: lihat_bab = st.selectbox("🔍 Filter Bab:", list(DATA_MATERI[lihat_pelajaran][lihat_kelas].keys()))
    with col4: lihat_subbab = st.selectbox("🔍 Filter Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]["sub_bab"])
        
    st.markdown("---")
    tab_rangkuman, tab_files = st.tabs(["📌 Rangkuman Materi", "📂 File Materi Tambahan"])
    
    with tab_rangkuman:
        st.write(f"### 📝 Rangkuman Singkat: {lihat_bab}")
        st.markdown(DATA_MATERI[lihat_pelajaran][lihat_kelas][lihat_bab]["rangkuman"])
        
        id_materi = f"{lihat_pelajaran}_{lihat_kelas}_{lihat_bab}"
        st.markdown("---")
        if id_materi in st.session_state.learned_chapters:
            st.info("✅ Kamu sudah menyelesaikan materi ini dan mengambil hadiah poinnya.")
        else:
            if st.button("🏁 Selesai Membaca & Klaim +40 PTS"):
                st.session_state.learned_chapters.add(id_materi)
                st.session_state.user_points += 40
                st.success("🎉 Selamat! +40 PTS ditambahkan.")
                st.balloons()
                st.rerun()
        
    with tab_files:
        folder_target = os.path.join("uploads", bersihkan_nama(lihat_pelajaran), bersihkan_nama(lihat_kelas), bersihkan_nama(lihat_bab), bersihkan_nama(lihat_subbab))
        if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
            st.info("📭 Belum ada berkas tambahan dari guru/siswa untuk sub-bab ini.")
        else:
            for file in os.listdir(folder_target):
                file_path = os.path.join(folder_target, file)
                file_ext = file.split('.')[-1].lower()
                with st.expander(f"📄 {file}"):
                    if file_ext in ['jpg', 'png', 'jpeg']:
                        try: st.image(Image.open(file_path), use_column_width=True)
                        except: pass
                    elif file_ext in ['xlsx', 'xls']:
                        try: st.dataframe(pd.read_excel(file_path), use_container_width=True)
                        except: pass
                    else: st.write("Klik tombol di bawah untuk mengunduh dokumen.")
                    
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Unduh File", data=f.read(), file_name=file, key=file_path)
                    except: pass

# --- HALAMAN KUSTOM AVATAR & TOKO ---
elif menu == "🎭 Kustom Avatar & Toko":
    st.title("🎭 Sanggar Kustomisasi Avatar")
    tab_kustom, tab_toko = st.tabs(["👤 Edit Karakter", "🛒 Toko Aksesoris Klasik"])
    
    with tab_kustom:
        st.subheader("Ubah Karakter Dasarmu")
        pilihan_base = st.selectbox("Pilih Tipe Karakter:", ["Siswa Laki-laki", "Siswa Perempuan"])
        
        if st.button("💾 Pakai Karakter"):
            st.session_state.avatar_base = AVATAR_LAKI if pilihan_base == "Siswa Laki-laki" else AVATAR_PEREMPUAN
            st.success("Karakter berhasil diubah!")
            st.rerun()
            
        st.markdown("---")
        st.subheader("Lemari Aksesoris")
        aksesoris_dipilih = st.selectbox("Gunakan Koleksimu:", st.session_state.unlocked_accessories)
        
        if st.button("🎒 Pakai Topi/Mahkota"):
            st.session_state.avatar_hat = "" if aksesoris_dipilih == "Tanpa Aksesoris" else TOKO_AKSESORIS[aksesoris_dipilih]["url"]
            st.success("Aksesoris dipasang!")
            st.rerun()
            
    with tab_toko:
        st.subheader("Beli Item Premium (Toko Game)")
        st.write(f"Dompet Kamu: ⭐ **{st.session_state.user_points} PTS**")
        st.markdown("---")
        for item, detail in TOKO_AKSESORIS.items():
            col_grafis, col_nama, col_harga, col_tombol = st.columns([1, 2, 1, 1])
            with col_grafis: st.image(detail["url"], width=50)
            with col_nama: st.write(f"### {item}")
            with col_harga: st.write(f"💰 {detail['harga']} PTS")
            with col_tombol:
                if item in st.session_state.unlocked_accessories:
                    st.button("✅ Dimiliki", key=item, disabled=True)
                else:
                    if st.button("🛒 Beli", key=item):
                        if st.session_state.user_points >= detail["harga"]:
                            st.session_state.user_points -= detail["harga"]
                            st.session_state.unlocked_accessories.append(item)
                            st.success(f"Sukses membeli {item}!")
                            st.rerun()
                        else: st.error("Poin tidak cukup!")
