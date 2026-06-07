import streamlit as st
import pandas as pd
from PIL import Image
import os
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media", page_icon="📚", layout="wide")

# --- INISIALISASI MEMORI USER (SESSION STATE) ---
if "user_points" not in st.session_state:
    st.session_state.user_points = 0
if "user_level" not in st.session_state:
    st.session_state.user_level = 1
if "learned_chapters" not in st.session_state:
    st.session_state.learned_chapters = set()
if "avatar_base" not in st.session_state:
    st.session_state.avatar_base = "https://img.icons8.com/illustrations/external-pack-flat-symbols-tanah-basah/200/external-student-back-to-school-pack-flat-symbols-tanah-basah.png"  # Default Siswa
if "avatar_hat" not in st.session_state:
    st.session_state.avatar_hat = ""      # Kosong (Tanpa Aksesoris)
if "unlocked_accessories" not in st.session_state:
    st.session_state.unlocked_accessories = ["Tanpa Aksesoris"]

# --- KUSTOMISASI CSS (Arsitektur Grafis Tumpukan Avatar) ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    
    .stButton>button {
        background-color: #2563EB; color: white; border-radius: 8px; border: none;
        padding: 10px 24px; font-weight: bold; transition: all 0.3s ease; width: 100%;
    }
    .stButton>button:hover { background-color: #1D4ED8; transform: scale(1.02); }
    
    /* === DESAIN GRAFIS PROFIL GAME === */
    .profile-card {
        background-color: white; border-radius: 16px; padding: 20px;
        border: 2px solid #E5E7EB; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 20px;
    }
    
    /* Container utama grafik avatar */
    .avatar-container {
        width: 140px; height: 140px; margin: 0 auto 15px auto;
        position: relative; background: radial-gradient(circle, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 50%; border: 4px solid #3B82F6; display: flex; align-items: center; justify-content: center;
    }
    
    /* Gambar Tubuh Karakter */
    .avatar-base-img {
        width: 100px; height: 100px; object-fit: contain; position: absolute; bottom: 10px; z-index: 1;
    }
    
    /* Gambar Aksesoris yang Bertumpuk di Kepala */
    .avatar-hat-img {
        width: 65px; height: 65px; object-fit: contain; position: absolute; top: -12px; z-index: 2;
    }
    
    div[data-testid="stExpander"] {
        background-color: white; border-radius: 10px; border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PEMBERSIH NAMA FOLDER ---
def bersihkan_nama(teks):
    return re.sub(r'[\\/*?:"<>|]', "", teks)

# --- REFRESH LEVEL OTOMATIS ---
st.session_state.user_level = (st.session_state.user_points // 100) + 1

# --- STRUKTUR DATA MATERI ---
DAFTAR_KELAS = ["Kelas 10", "Kelas 11", "Kelas 12"]
DATA_MATERI = {
    "Pendidikan Pancasila (PKn)": {
        "Bab 1: Pancasila sebagai Dasar Negara": {
            "sub_bab": ["1.1 Sejarah Pancasila", "1.2 Penerapan Pancasila"],
            "rangkuman": "• **Sejarah Pancasila**: Dirumuskan dalam Sidang BPUPKI pertama. Istilah Pancasila lahir pada 1 Juni 1945.\n• **Penerapan**: Berfungsi sebagai pandangan hidup bangsa."
        }
    },
    "Fisika": {
        "Bab 1: Usaha dan Energi": {
            "sub_bab": ["1.1 Pembangkit Listrik", "1.2 Energi Terbarukan"],
            "rangkuman": "• **Usaha ($W$)**: Perkalian gaya dengan perpindahan ($W = F \\cdot s$).\n• **Energi Mekanik**: Gabungan Energi Kinetik ($Ek = \\frac{1}{2}mv^2$) dan Energi Potensial ($Ep = mgh$)."
        }
    }
}

# --- DATABASE GRAFIS TOKO AKSESORIS (URL Gambar PNG Transparan) ---
TOKO_AKSESORIS = {
    "👑 Mahkota Emas": {
        "harga": 100, 
        "url": "https://img.icons8.com/isometric/100/crown.png"
    },
    "🎧 Headphone Neon": {
        "harga": 60, 
        "url": "https://img.icons8.com/isometric/100/headphones.png"
    },
    "🎓 Topi Kelulusan": {
        "harga": 40, 
        "url": "https://img.icons8.com/isometric/100/mortarboard.png"
    },
    "🥽 Kacamata Google": {
        "harga": 50, 
        "url": "https://img.icons8.com/isometric/100/safety-goggles.png"
    }
}

# --- SIDEBAR NAVIGASI & STATS USER ---
with st.sidebar:
    # Memasang Grafis Tumpukan Karakter (Base + Hat) lewat HTML & CSS
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
    
    progress_persen = st.session_state.user_points % 100
    st.progress(progress_persen / 100)
    st.caption(f"ℹ️ {100 - progress_persen} PTS lagi menuju Level {st.session_state.user_level + 1}")
    st.markdown("---")
    
    st.title("🧭 Menu Utama")
    menu = st.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Ruang Belajar", "🎭 Kustom Avatar & Toko"])

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Portal Learning Media")
    st.markdown("### Belajar, Kumpulkan Poin, dan Kembangkan Avatarmu!")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Tambah Materi Baru")
    col1, col2 = st.columns(2)
    with col1: pilih_kelas = st.selectbox("🎓 Pilih Kelas Target:", DAFTAR_KELAS)
    with col2: pilih_pelajaran = st.selectbox("📖 Pilih Mata Pelajaran:", list(DATA_MATERI.keys()))
    
    col3, col4 = st.columns(2)
    with col3: pilih_bab = st.selectbox("📑 Pilih Bab:", list(DATA_MATERI[pilih_pelajaran].keys()))
    with col4: pilih_subbab = st.selectbox("🔖 Pilih Sub-bab:", DATA_MATERI[pilih_pelajaran][pilih_bab]["sub_bab"])
        
    st.markdown("---")
    uploaded_file = st.file_uploader("Seret file ke sini", type=['jpg', 'png', 'pdf', 'docx', 'xlsx'])
    
    if uploaded_file is not None:
        st.warning(f"File '{uploaded_file.name}' siap ditambahkan. Klik tombol di bawah untuk konfirmasi.")
        if st.button("🚀 Submit Materi Sekarang"):
            folder_tujuan = os.path.join("uploads", bersihkan_nama(pilih_kelas), bersihkan_nama(pilih_pelajaran), bersihkan_nama(pilih_bab), bersihkan_nama(pilih_subbab))
            if not os.path.exists(folder_tujuan): os.makedirs(folder_tujuan)
            with open(os.path.join(folder_tujuan, uploaded_file.name), "wb") as f: f.write(uploaded_file.getbuffer())
            st.success(f"🎉 Sukses menyimpan materi!")
            st.balloons()

# --- HALAMAN LIHAT MATERI ---
elif menu == "📖 Ruang Belajar":
    st.title("📖 Ruang Belajar Interaktif")
    col1, col2 = st.columns(2)
    with col1: lihat_kelas = st.selectbox("🔍 Filter Kelas:", DAFTAR_KELAS)
    with col2: lihat_pelajaran = st.selectbox("🔍 Filter Pelajaran:", list(DATA_MATERI.keys()))
    col3, col4 = st.columns(2)
    with col3: lihat_bab = st.selectbox("🔍 Filter Bab:", list(DATA_MATERI[lihat_pelajaran].keys()))
    with col4: lihat_subbab = st.selectbox("🔍 Filter Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_bab]["sub_bab"])
        
    st.markdown("---")
    tab_rangkuman, tab_files = st.tabs(["📌 Rangkuman Materi", "📂 File Materi & Download"])
    
    with tab_rangkuman:
        st.write(f"### 📝 Rangkuman {lihat_bab}")
        st.markdown(DATA_MATERI[lihat_pelajaran][lihat_bab]["rangkuman"])
        
        id_materi = f"{lihat_pelajaran}_{lihat_bab}"
        st.markdown("---")
        if id_materi in st.session_state.learned_chapters:
            st.info("✅ Kamu sudah menyelesaikan materi ini dan mengambil hadiah poinnya.")
        else:
            if st.button("🏁 Selesai Membaca & Klaim +40 PTS"):
                st.session_state.learned_chapters.add(id_materi)
                st.session_state.user_points += 40
                st.success("🎉 Selamat! +40 PTS telah ditambahkan ke profilmu.")
                st.balloons()
                st.rerun()
        
    with tab_files:
        folder_target = os.path.join("uploads", bersihkan_nama(lihat_kelas), bersihkan_nama(lihat_pelajaran), bersihkan_nama(lihat_bab), bersihkan_nama(lihat_subbab))
        if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
            st.info(f"📭 Belum ada file unggahan tambahan.")
        else:
            for file in os.listdir(folder_target):
                file_path = os.path.join(folder_target, file)
                with st.expander(f"📄 Buka Materi: {file}"):
                    st.download_button(label=f"⬇️ Unduh File", data=open(file_path, "rb"), file_name=file, key=file_path)

# --- HALAMAN KUSTOM AVATAR & TOKO (GRAFIS BARU) ---
elif menu == "🎭 Kustom Avatar & Toko":
    st.title("🎭 Sanggar Kustomisasi Avatar")
    tab_kustom, tab_toko = st.tabs(["👤 Edit Karakter", "🛒 Toko Aksesoris Klasik"])
    
    with tab_kustom:
        st.subheader("Ubah Karakter Dasarmu")
        pilihan_base = st.selectbox("Pilih Tipe Karakter:", ["Siswa Pintar", "Siswi Kreatif", "Kucing Cerdas", "Robot Masa Depan"])
        
        map_base = {
            "Siswa Pintar": "https://img.icons8.com/illustrations/external-pack-flat-symbols-tanah-basah/200/external-student-back-to-school-pack-flat-symbols-tanah-basah.png",
            "Siswi Kreatif": "https://img.icons8.com/illustrations/flat-round/200/female-student--v1.png",
            "Kucing Cerdas": "https://img.icons8.com/illustrations/flat-round/200/cat.png",
            "Robot Masa Depan": "https://img.icons8.com/illustrations/flat-round/200/robot.png"
        }
        if st.button("💾 Simpan Karakter"):
            st.session_state.avatar_base = map_base[pilihan_base]
            st.success("Karakter dasar berhasil diperbarui!")
            st.rerun()
            
        st.markdown("---")
        st.subheader("Lemari Aksesoris")
        aksesoris_dipilih = st.selectbox("Gunakan Koleksimu:", st.session_state.unlocked_accessories)
        
        if st.button("🎒 Pakai Sekarang"):
            if aksesoris_dipilih == "Tanpa Aksesoris":
                st.session_state.avatar_hat = ""
            else:
                st.session_state.avatar_hat = TOKO_AKSESORIS[aksesoris_dipilih]["url"]
            st.success("Aksesoris berhasil dipasang ke kepala!")
            st.rerun()
            
    with tab_toko:
        st.subheader("Beli Item Premium dengan Poin Belajarmu")
        st.write(f"Dompet Kamu: ⭐ **{st.session_state.user_points} PTS**")
        st.markdown("---")
        
        for item, detail in TOKO_AKSESORIS.items():
            col_grafis, col_nama, col_harga, col_tombol = st.columns([1, 2, 1, 1])
            with col_grafis:
                st.image(detail["url"], width=50) # Tampilkan preview visual item di toko
            with col_nama:
                st.write(f"### {item}")
            with col_harga:
                st.write(f"💰 {detail['harga']} PTS")
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
                        else:
                            st.error("Poin tidak mencukupi!")
