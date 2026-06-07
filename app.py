import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Learning Media", page_icon="📚", layout="wide")

# --- KUSTOMISASI CSS (Hal-hal kecil yang mempercantik UI) ---
st.markdown("""
    <style>
    /* Mengubah warna latar belakang aplikasi menjadi lebih lembut */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Mempercantik tampilan font judul */
    h1, h2, h3 {
        color: #1E3A8A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Mempercantik tombol menjadi membulat dan interaktif */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        transform: scale(1.02);
    }
    
    /* Mempercantik area upload file */
    .stFileUploader>div>div>div>button {
        background-color: #10B981;
        color: white;
    }
    
    /* Membuat kartu (card) pembatas yang rapi */
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA KATEGORI KELAS & PELAJARAN ---
DAFTAR_KELAS = ["Kelas 10", "Kelas 11", "Kelas 12"]
DAFTAR_PELAJARAN = [
    "Pendidikan Pancasila (PKn)", 
    "Fisika", 
    "Kimia", 
    "Biologi (Ekologi)", 
    "Matematika", 
    "Prakarya & Kewirausahaan", 
    "Seni Budaya",
    "Ekonomi",
    "Sosiologi",
    "Geografi"
    "Sejarah",
    "Bahasa Indonesia",
    "Bahasa Inggris"
]

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3364/3364053.png", width=80) # Ikon logo kecil
    st.title("🧭 Menu Utama")
    menu = st.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Ruang Belajar"])
    
    st.markdown("---")
    st.caption("✨ Didesain untuk kenyamanan belajar.")

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Portal Learning Media")
    st.markdown("### Belajar jadi lebih fokus dan tertata.")
    
    # Placeholder Banner (Ganti dengan desain buatanmu sendiri!)
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)
    
    st.info("💡 **Petunjuk Penggunaan:** Gunakan menu di sebelah kiri untuk mengelola atau membaca materi pelajaran berdasarkan kelas.")

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Tambah Materi Baru")
    st.write("Silakan tentukan penempatan materi agar rapi di dalam sistem.")
    
    # Layout Kolom yang lebih rapi untuk dropdown
    col1, col2 = st.columns(2)
    with col1:
        pilih_kelas = st.selectbox("🎓 Pilih Kelas Target:", DAFTAR_KELAS)
    with col2:
        pilih_pelajaran = st.selectbox("📖 Pilih Mata Pelajaran:", DAFTAR_PELAJARAN)
        
    st.markdown("---")
    uploaded_file = st.file_uploader("Seret file ke sini atau klik tombol browse", type=['jpg', 'png', 'pdf', 'docx', 'xlsx'])
    
    if uploaded_file is not None:
        folder_tujuan = os.path.join("uploads", pilih_kelas, pilih_pelajaran)
        if not os.path.exists(folder_tujuan):
            os.makedirs(folder_tujuan)
            
        path_simpan = os.path.join(folder_tujuan, uploaded_file.name)
        with open(path_simpan, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"🎉 Sukses! File '{uploaded_file.name}' berhasil tersimpan di {pilih_kelas} - {pilih_pelajaran}.")

# --- HALAMAN LIHAT MATERI ---
elif menu == "📖 Ruang Belajar":
    st.title("📖 Ruang Belajar Interaktif")
    st.write("Cari dan pelajari materi yang sudah tersedia di bawah ini.")
    
    # Filter pencarian
    col1, col2 = st.columns(2)
    with col1:
        lihat_kelas = st.selectbox("🔍 Tampilkan Kelas:", DAFTAR_KELAS)
    with col2:
        lihat_pelajaran = st.selectbox("🔍 Tampilkan Pelajaran:", DAFTAR_PELAJARAN)
        
    st.markdown("---")
    folder_target = os.path.join("uploads", lihat_kelas, lihat_pelajaran)
    
    if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
        st.info(f"📭 Belum ada materi yang tersedia untuk **{lihat_kelas} - {lihat_pelajaran}**.")
    else:
        files = os.listdir(folder_target)
        
        # Menggunakan Expander (Materi bisa dilipat/dibuka agar tidak makan tempat)
        for file in files:
            file_path = os.path.join(folder_target, file)
            file_ext = file.split('.')[-1].lower()
            
            with st.expander(f"📄 Buka Materi: {file}", expanded=False):
                # Preview Gambar
                if file_ext in ['jpg', 'png', 'jpeg']:
                    try:
                        img = Image.open(file_path)
                        st.image(img, use_column_width=True)
                    except Exception:
                        st.write("(Gambar tidak dapat dimuat)")
                
                # Preview Excel
                elif file_ext in ['xlsx', 'xls']:
                    try:
                        df = pd.read_excel(file_path)
                        st.dataframe(df, use_container_width=True)
                    except:
                        st.error("Gagal membaca file Excel.")
                else:
                    st.write("Pratinjau tidak tersedia untuk format file ini. Silakan unduh untuk melihat isinya.")
                
                # Tombol Download di dalam expander
                with open(file_path, "rb") as f:
                    st.download_button(label=f"⬇️ Unduh File", data=f, file_name=file, key=file_path)
