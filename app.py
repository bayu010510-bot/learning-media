import streamlit as st
import pandas as pd
from PIL import Image
import os

# Konfigurasi Tampilan
st.set_page_config(page_title="Learning Media", page_icon="📚", layout="wide")

# Buat folder materi
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- SIDEBAR ---
st.sidebar.title("🧭 Navigasi Menu")
menu = st.sidebar.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Lihat Materi"])

st.sidebar.markdown("---")
st.sidebar.info("💡 Tips: Belajarlah dengan sungguh sungguh agar kau berhasil.")

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Selamat Datang di Learning Media!")
    st.info("Platform belajar interaktif untuk berbagi materi pelajaran (contoh: PKn, Ekologi, Fisika, dll) dengan mudah.")
    
    # Placeholder Banner
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", use_column_width=True)

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Upload Materi Belajar")
    uploaded_file = st.file_uploader("Format yang didukung: JPG, PNG, PDF, DOCX, XLSX", type=['jpg', 'png', 'pdf', 'docx', 'xlsx'])
    
    if uploaded_file is not None:
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Mantap! File '{uploaded_file.name}' berhasil disimpan.")
        st.balloons()

# --- HALAMAN LIHAT MATERI ---
elif menu == "📖 Lihat Materi":
    st.title("📖 Ruang Belajar")
    files = os.listdir("uploads")
    
    if len(files) == 0:
        st.warning("Belum ada materi yang diunggah.")
    else:
        for file in files:
            file_path = os.path.join("uploads", file)
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
