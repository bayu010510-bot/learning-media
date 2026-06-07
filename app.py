import streamlit as st
import pandas as pd
from PIL import Image
import os

# Konfigurasi Tampilan
st.set_page_config(page_title="Learning Media", page_icon="📚", layout="wide")

# --- DATA KATEGORI KELAS & PELAJARAN ---
DAFTAR_KELAS = ["Kelas 10", "Kelas 11", "Kelas 12"]
DAFTAR_PELAJARAN = [
    "Pendidikan Pancasila (PKn)", 
    "Fisika", 
    "Kimia", 
    "Biologi (Ekologi)", 
    "Matematika", 
    "Prakarya & Kewirausahaan", 
    "Seni Budaya"
]

# --- SIDEBAR ---
st.sidebar.title("🧭 Navigasi Menu")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Lihat Materi"])

st.sidebar.markdown("---")
st.sidebar.info("💡 Tips: Pilih kelas dan mata pelajaran yang sesuai agar materi tersusun rapi di dalam sistem.")

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Selamat Datang di Learning Media!")
    st.info("Platform belajar interaktif untuk berbagi materi pelajaran dengan susunan folder yang rapi.")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", use_column_width=True)

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Upload Materi Belajar")
    
    # Membuat 2 kolom untuk pilihan kelas dan pelajaran
    col1, col2 = st.columns(2)
    with col1:
        pilih_kelas = st.selectbox("🎓 Pilih Kelas:", DAFTAR_KELAS)
    with col2:
        pilih_pelajaran = st.selectbox("📖 Pilih Mata Pelajaran:", DAFTAR_PELAJARAN)
        
    st.markdown("---")
    uploaded_file = st.file_uploader("Format yang didukung: JPG, PNG, PDF, DOCX, XLSX", type=['jpg', 'png', 'pdf', 'docx', 'xlsx'])
    
    if uploaded_file is not None:
        # Membuat direktori folder dinamis: uploads/Kelas/Pelajaran
        folder_tujuan = os.path.join("uploads", pilih_kelas, pilih_pelajaran)
        if not os.path.exists(folder_tujuan):
            os.makedirs(folder_tujuan) # Membuat folder jika belum ada
            
        # Menyimpan file ke dalam folder yang sudah dipilih
        path_simpan = os.path.join(folder_tujuan, uploaded_file.name)
        with open(path_simpan, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"Mantap! File '{uploaded_file.name}' berhasil disimpan ke dalam folder {pilih_kelas} - {pilih_pelajaran}.")
        st.balloons()

# --- HALAMAN LIHAT MATERI ---
elif menu == "📖 Lihat Materi":
    st.title("📖 Ruang Belajar")
    
    # Filter pencarian materi
    col1, col2 = st.columns(2)
    with col1:
        lihat_kelas = st.selectbox("🔍 Filter Kelas:", DAFTAR_KELAS)
    with col2:
        lihat_pelajaran = st.selectbox("🔍 Filter Mata Pelajaran:", DAFTAR_PELAJARAN)
        
    st.markdown("---")
    
    # Menentukan target folder yang akan dibaca
    folder_target = os.path.join("uploads", lihat_kelas, lihat_pelajaran)
    
    # Mengecek apakah folder tersebut ada isinya
    if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
        st.warning(f"Belum ada materi yang diunggah untuk {lihat_kelas} - {lihat_pelajaran}.")
    else:
        files = os.listdir(folder_target)
        for file in files:
            file_path = os.path.join(folder_target, file)
            file_ext = file.split('.')[-1].lower()
            
            st.write(f"### 📄 {file}")
            
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
                    st.dataframe(df.head())
                except:
                    st.error("Gagal membaca file Excel.")
            
            # Tombol Download
            with open(file_path, "rb") as f:
                st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)
            st.markdown("---")
