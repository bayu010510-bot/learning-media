import streamlit as st
import pandas as pd
from PIL import Image
import os
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media", page_icon="📚", layout="wide")

# --- KUSTOMISASI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .stButton>button {
        background-color: #2563EB; color: white; border-radius: 8px; border: none;
        padding: 10px 24px; font-weight: bold; transition: all 0.3s ease; width: 100%;
    }
    .stButton>button:hover { background-color: #1D4ED8; transform: scale(1.02); }
    
    div[data-testid="stExpander"] {
        background-color: white; border-radius: 10px; border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI PEMBERSIH NAMA FOLDER ---
def bersihkan_nama(teks):
    return re.sub(r'[\\/*?:"<>|]', "", teks)

# --- STRUKTUR DATA MATERI LENGKAP ---
DAFTAR_KELAS = ["Kelas 10", "Kelas 11", "Kelas 12"]

DATA_MATERI = {
    "Pendidikan Pancasila (PKn)": {
        "Bab 1: Pancasila sebagai Dasar Negara": ["1.1 Sejarah Pancasila", "1.2 Penerapan Pancasila"],
        "Bab 2: Bhinneka Tunggal Ika": ["2.1 Konsep Gotong Royong", "2.2 Toleransi Antarumat"]
    },
    "Fisika": {
        "Bab 1: Usaha dan Energi": ["1.1 Pembangkit Listrik", "1.2 Energi Terbarukan"],
        "Bab 2: Momentum dan Impuls": ["2.1 Konsep Impuls", "2.2 Tumbukan Benda"]
    },
    "Kimia": {
        "Bab 1: Hukum Dasar Kimia": ["1.1 Penyetaraan Reaksi Kimia", "1.2 Mol dan Massa Molar"],
        "Bab 2: Struktur Atom": ["2.1 Model Atom", "2.2 Konfigurasi Elektron"]
    },
    "Biologi": {
        "Bab 1: Keanekaragaman Hayati": ["1.1 Tingkat Keanekaragaman", "1.2 Flora dan Fauna Indonesia"],
        "Bab 2: Ekologi dan Lingkungan": ["2.1 Komponen Ekosistem", "2.2 Daur Biogeokimia"]
    },
    "Ekonomi": {
        "Bab 1: Konsep Dasar Ilmu Ekonomi": ["1.1 Kebutuhan dan Kelangkaan", "1.2 Sistem Ekonomi"],
        "Bab 2: Ketenagakerjaan": ["2.1 Angkatan Kerja", "2.2 Pengangguran dan Dampaknya"]
    },
    "Sosiologi": {
        "Bab 1: Struktur Sosial": ["1.1 Stratifikasi Sosial", "1.2 Diferensiasi Sosial"],
        "Bab 2: Konflik dan Integrasi Sosial": ["2.1 Akar Konflik di Masyarakat", "2.2 Resolusi Konflik"]
    },
    "Geografi": {
        "Bab 1: Pengetahuan Dasar Geografi": ["1.1 Objek Studi Geografi", "1.2 Peta dan Penginderaan Jauh"],
        "Bab 2: Dinamika Bumi": ["2.1 Litosfer (Lapisan Batuan)", "2.2 Atmosfer dan Cuaca"]
    },
    "Sejarah": {
        "Bab 1: Konsep Dasar Sejarah": ["1.1 Berpikir Diakronik & Sinkronik", "1.2 Sumber-sumber Sejarah"],
        "Bab 2: Pergerakan Nasional": ["2.1 Organisasi Pergerakan", "2.2 Sumpah Pemuda"]
    },
    "Bahasa Inggris": {
        "Bab 1: Narrative Text": ["1.1 Generic Structure", "1.2 Fairy Tales and Legends"],
        "Bab 2: Analytical Exposition": ["2.1 Presenting Arguments", "2.2 Language Features"]
    },
    "Bahasa Indonesia": {
        "Bab 1: Teks Laporan Hasil Observasi": ["1.1 Struktur Teks Observasi", "1.2 Kaidah Kebahasaan"],
        "Bab 2: Proposal dan Karya Ilmiah": ["2.1 Merancang Sistematika Proposal", "2.2 Format Karya Ilmiah"]
    }
}

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3364/3364053.png", width=80)
    st.title("🧭 Menu Utama")
    menu = st.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Ruang Belajar"])
    st.markdown("---")
    st.caption("✨ Didesain untuk kenyamanan belajar.")

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Portal Learning Media")
    st.markdown("### Belajar jadi lebih fokus dan terstruktur rapi.")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)
    st.info("💡 **Petunjuk Penggunaan:** Gunakan menu di sebelah kiri untuk mengelola atau membaca materi pelajaran yang sudah disusun per Bab dan Sub-bab.")

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Tambah Materi Baru")
    st.write("Silakan tentukan penempatan hierarki materi, lalu klik **Submit** untuk menyimpan.")
    
    col1, col2 = st.columns(2)
    with col1:
        pilih_kelas = st.selectbox("🎓 Pilih Kelas Target:", DAFTAR_KELAS)
    with col2:
        pilih_pelajaran = st.selectbox("📖 Pilih Mata Pelajaran:", list(DATA_MATERI.keys()))
        
    col3, col4 = st.columns(2)
    with col3:
        daftar_bab = list(DATA_MATERI[pilih_pelajaran].keys())
        pilih_bab = st.selectbox("📑 Pilih Bab:", daftar_bab)
    with col4:
        daftar_subbab = DATA_MATERI[pilih_pelajaran][pilih_bab]
        pilih_subbab = st.selectbox("🔖 Pilih Sub-bab:", daftar_subbab)
        
    st.markdown("---")
    uploaded_file = st.file_uploader("Seret file ke sini atau klik tombol browse", type=['jpg', 'png', 'pdf', 'docx', 'xlsx'])
    
    if uploaded_file is not None:
        st.warning(f"File '{uploaded_file.name}' siap ditambahkan ke [{pilih_bab} - {pilih_subbab}]. Klik tombol di bawah untuk konfirmasi.")
        
        if st.button("🚀 Submit Materi Sekarang"):
            folder_tujuan = os.path.join(
                "uploads", 
                bersihkan_nama(pilih_kelas), 
                bersihkan_nama(pilih_pelajaran), 
                bersihkan_nama(pilih_bab), 
                bersihkan_nama(pilih_subbab)
            )
            
            if not os.path.exists(folder_tujuan):
                os.makedirs(folder_tujuan)
                
            path_simpan = os.path.join(folder_tujuan, uploaded_file.name)
            with open(path_simpan, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            st.success(f"🎉 Sukses! File berhasil tersimpan di hierarki yang dipilih.")
            st.balloons()

# --- HALAMAN LIHAT MATERI ---
elif menu == "📖 Ruang Belajar":
    st.title("📖 Ruang Belajar Interaktif")
    st.write("Telusuri materi pelajaran secara spesifik hingga ke Sub-bab.")
    
    col1, col2 = st.columns(2)
    with col1:
        lihat_kelas = st.selectbox("🔍 Filter Kelas:", DAFTAR_KELAS)
    with col2:
        lihat_pelajaran = st.selectbox("🔍 Filter Pelajaran:", list(DATA_MATERI.keys()))
        
    col3, col4 = st.columns(2)
    with col3:
        lihat_bab = st.selectbox("🔍 Filter Bab:", list(DATA_MATERI[lihat_pelajaran].keys()))
    with col4:
        lihat_subbab = st.selectbox("🔍 Filter Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_bab])
        
    st.markdown("---")
    
    folder_target = os.path.join(
        "uploads", 
        bersihkan_nama(lihat_kelas), 
        bersihkan_nama(lihat_pelajaran), 
        bersihkan_nama(lihat_bab), 
        bersihkan_nama(lihat_subbab)
    )
    
    if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
        st.info(f"📭 Belum ada materi yang tersedia untuk **{lihat_subbab}**.")
    else:
        files = os.listdir(folder_target)
        
        for file in files:
            file_path = os.path.join(folder_target, file)
            file_ext = file.split('.')[-1].lower()
            
            with st.expander(f"📄 Buka Materi: {file}", expanded=False):
                if file_ext in ['jpg', 'png', 'jpeg']:
                    try:
                        img = Image.open(file_path)
                        st.image(img, use_column_width=True)
                    except Exception:
                        st.write("(Gambar tidak dapat dimuat)")
                elif file_ext in ['xlsx', 'xls']:
                    try:
                        df = pd.read_excel(file_path)
                        st.dataframe(df, use_container_width=True)
                    except:
                        st.error("Gagal membaca file Excel.")
                else:
                    st.write("Pratinjau tidak tersedia untuk format file ini. Silakan unduh untuk melihat isinya.")
                
                with open(file_path, "rb") as f:
                    st.download_button(label=f"⬇️ Unduh File", data=f, file_name=file, key=file_path)
