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
    st.session_state.avatar_base = "🧑‍🎓"  # Default Siswa
if "avatar_hat" not in st.session_state:
    st.session_state.avatar_hat = ""      # Belum pakai aksesoris
if "unlocked_accessories" not in st.session_state:
    st.session_state.unlocked_accessories = ["Tanpa Aksesoris"]

# --- KUSTOMISASI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    
    .stButton>button {
        background-color: #2563EB; color: white; border-radius: 8px; border: none;
        padding: 10px 24px; font-weight: bold; transition: all 0.3s ease; width: 100%;
    }
    .stButton>button:hover { background-color: #1D4ED8; transform: scale(1.02); }
    
    /* Desain Kartu Profil Gamifikasi */
    .profile-card {
        background-color: white; border-radius: 12px; padding: 20px;
        border: 1px solid #E5E7EB; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        text-align: center; margin-bottom: 20px;
    }
    .avatar-display { font-size: 70px; margin-bottom: 10px; position: relative; display: inline-block; }
    .hat-overlay { position: absolute; top: -25px; left: 0; right: 0; font-size: 45px; }
    
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
# Setiap kelipatan 100 poin, user naik 1 level
st.session_state.user_level = (st.session_state.user_points // 100) + 1

# --- STRUKTUR DATA MATERI & RANGKUMAN ---
DAFTAR_KELAS = ["Kelas 10", "Kelas 11", "Kelas 12"]
DATA_MATERI = {
    "Pendidikan Pancasila (PKn)": {
        "Bab 1: Pancasila sebagai Dasar Negara": {
            "sub_bab": ["1.1 Sejarah Pancasila", "1.2 Penerapan Pancasila"],
            "rangkuman": "• **Sejarah Pancasila**: Dirumuskan dalam Sidang BPUPKI pertama oleh Ir. Soekarno, Moh. Yamin, dan Soepomo. Istilah Pancasila lahir pada 1 Juni 1945.\n• **Penerapan**: Pancasila berfungsi sebagai pandangan hidup bangsa."
        },
        "Bab 2: Bhinneka Tunggal Ika": {
            "sub_bab": ["2.1 Konsep Gotong Royong", "2.2 Toleransi Antarumat"],
            "rangkuman": "• **Gotong Royong**: Budaya asli Indonesia berupa kerja bersama untuk mencapai hasil yang didambakan."
        }
    },
    "Fisika": {
        "Bab 1: Usaha dan Energi": {
            "sub_bab": ["1.1 Pembangkit Listrik", "1.2 Energi Terbarukan"],
            "rangkuman": "• **Usaha ($W$)**: Perkalian gaya dengan perpindahan ($W = F \\cdot s$).\n• **Energi Mekanik**: Gabungan Energi Kinetik ($Ek = \\frac{1}{2}mv^2$) dan Energi Potensial ($Ep = mgh$)."
        },
        "Bab 2: Momentum dan Impuls": {
            "sub_bab": ["2.1 Konsep Impuls", "2.2 Tumbukan Benda"],
            "rangkuman": "• **Momentum ($p$)**: $High$ tingkat kesukaran menghentikan benda ($p = m \\cdot v$).\n• **Impuls ($I$)**: Perubahan momentum yang disebabkan gaya singkat ($I = F \\cdot \\Delta t = \\Delta p$)."
        }
    },
    "Kimia": {
        "Bab 1: Hukum Dasar Kimia": {
            "sub_bab": ["1.1 Penyetaraan Reaksi Kimia", "1.2 Mol dan Massa Molar"],
            "rangkuman": "• **Penyetaraan Reaksi**: Menyamakan jumlah atom di reaktan dan produk.\n• **Konsep Mol**: Satuan jumlah zat. $1 \\text{ mol} = 6,02 \\times 10^{23}$ partikel."
        }
    }
}

# --- TOKO AKSESORIS AVATAR ---
TOKO_AKSESORIS = {
    "🎓 Topi Wisuda": {"harga": 50, "emoji": "🎓"},
    "👑 Mahkota Raja": {"harga": 150, "emoji": "👑"},
    "🎧 Headphone Gaming": {"harga": 100, "emoji": "🎧"},
    "🥽 Kacamata Lab": {"harga": 70, "emoji": "🥽"},
    "🐱 Telinga Kucing": {"harga": 120, "emoji": "🐱"}
}

# --- SIDEBAR NAVIGASI & STATS USER ---
with st.sidebar:
    # Tampilan Avatar Gabungan (Base + Aksesoris)
    hat_html = f"<div class='hat-overlay'>{st.session_state.avatar_hat}</div>" if st.session_state.avatar_hat else ""
    st.markdown(f"""
    <div class='profile-card'>
        <div class='avatar-display'>
            {hat_html}
            {st.session_state.avatar_base}
        </div>
        <h4>Level {st.session_state.user_level}</h4>
        <p style='color:#7C3AED; font-weight:bold; margin:0;'>⭐ {st.session_state.user_points} PTS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Bar menuju Level Selanjutnya
    progress_persen = st.session_state.user_points % 100
    st.progress(progress_persen / 100)
    st.caption(f"ℹ️ {100 - progress_persen} PTS lagi menuju Level {st.session_state.user_level + 1}")
    st.markdown("---")
    
    st.title("🧭 Menu Utama")
    menu = st.radio("Pilih Halaman:", ["🏠 Beranda", "📤 Upload Materi", "📖 Ruang Belajar", "🎭 Kustom Avatar & Toko"])
    st.markdown("---")
    st.caption("✨ Hub Pengalaman Belajar Interaktif.")

# --- HALAMAN BERANDA ---
if menu == "🏠 Beranda":
    st.title("📚 Portal Learning Media")
    st.markdown("### Belajar, Kumpulkan Poin, dan Kembangkan Avatarmu!")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)
    st.success("💡 **Cara Bermain & Belajar:** Setiap kali kamu menyelesaikan membaca **Rangkuman Materi** baru di Ruang Belajar, kamu akan mendapatkan hadiah **+40 PTS**. Gunakan poinmu untuk membeli aksesoris keren di Toko Avatar!")

# --- HALAMAN UPLOAD ---
elif menu == "📤 Upload Materi":
    st.title("📤 Tambah Materi Baru")
    
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
        daftar_subbab = DATA_MATERI[pilih_pelajaran][pilih_bab]["sub_bab"]
        pilih_subbab = st.selectbox("🔖 Pilih Sub-bab:", daftar_subbab)
        
    st.markdown("---")
    uploaded_file = st.file_uploader("Seret file ke sini", type=['jpg', 'png', 'pdf', 'docx', 'xlsx'])
    
    if uploaded_file is not None:
        st.warning(f"File '{uploaded_file.name}' siap ditambahkan. Klik tombol di bawah untuk konfirmasi.")
        if st.button("🚀 Submit Materi Sekarang"):
            folder_tujuan = os.path.join("uploads", bersihkan_nama(pilih_kelas), bersihkan_nama(pilih_pelajaran), bersihkan_nama(pilih_bab), bersihkan_nama(pilih_subbab))
            if not os.path.exists(folder_tujuan):
                os.makedirs(folder_tujuan)
            with open(os.path.join(folder_tujuan, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"🎉 Sukses menyimpan materi!")
            st.balloons()

# --- HALAMAN LIHAT MATERI (DENGAN REWARD POIN) ---
elif menu == "📖 Ruang Belajar":
    st.title("📖 Ruang Belajar Interaktif")
    
    col1, col2 = st.columns(2)
    with col1:
        lihat_kelas = st.selectbox("🔍 Filter Kelas:", DAFTAR_KELAS)
    with col2:
        lihat_pelajaran = st.selectbox("🔍 Filter Pelajaran:", list(DATA_MATERI.keys()))
    col3, col4 = st.columns(2)
    with col3:
        lihat_bab = st.selectbox("🔍 Filter Bab:", list(DATA_MATERI[lihat_pelajaran].keys()))
    with col4:
        lihat_subbab = st.selectbox("🔍 Filter Sub-bab:", DATA_MATERI[lihat_pelajaran][lihat_bab]["sub_bab"])
        
    st.markdown("---")
    tab_rangkuman, tab_files = st.tabs(["📌 Rangkuman Materi", "📂 File Materi & Download"])
    
    with tab_rangkuman:
        st.write(f"### 📝 Rangkuman {lihat_bab}")
        st.markdown(DATA_MATERI[lihat_pelajaran][lihat_bab]["rangkuman"])
        
        # Logika Poin Belajar
        id_materi = f"{lihat_pelajaran}_{lihat_bab}"
        st.markdown("---")
        if id_materi in st.session_state.learned_chapters:
            st.info("✅ Kamu sudah menyelesaikan materi ini dan mengambil hadiah poinnya.")
        else:
            if st.button("🏁 Selesai Membaca & Klaim +40 PTS"):
                st.session_state.learned_chapters.add(id_materi)
                st.session_state.user_points += 40
                st.success("🎉 Selamat! +40 PTS telah ditambahkan ke profilmu. Levelmu akan otomatis dihitung ulang.")
                st.balloons()
                st.rerun() # Refresh halaman untuk update sidebar instan
        
    with tab_files:
        folder_target = os.path.join("uploads", bersihkan_nama(lihat_kelas), bersihkan_nama(lihat_pelajaran), bersihkan_nama(lihat_bab), bersihkan_nama(lihat_subbab))
        if not os.path.exists(folder_target) or len(os.listdir(folder_target)) == 0:
            st.info(f"📭 Belum ada file unggahan tambahan untuk sub-bab ini.")
        else:
            for file in os.listdir(folder_target):
                file_path = os.path.join(folder_target, file)
                with st.expander(f"📄 Buka Materi: {file}"):
                    st.download_button(label=f"⬇️ Unduh File", data=open(file_path, "rb"), file_name=file, key=file_path)

# --- HALAMAN KUSTOM AVATAR & TOKO ---
elif menu == "🎭 Kustom Avatar & Toko":
    st.title("🎭 Sanggar Kustomisasi Avatar")
    
    tab_kustom, tab_toko = st.tabs(["👤 Edit Karakter", "🛒 Toko Aksesoris Klasik"])
    
    with tab_kustom:
        st.subheader("Ubah Basis Karaktermu")
        pilihan_base = st.selectbox("Pilih Ekspresi/Gender Avatar:", ["🧑‍🎓 Siswa", "👩‍🎓 Siswi", "🥷 Ninja Belajar", "🤖 Robot Pintar", "🦊 Rubah Cerdas"])
        
        # Kamus konversi pilihan ke emoji
        map_base = {"🧑‍🎓 Siswa": "🧑‍🎓", "👩‍🎓 Siswi": "👩‍🎓", "🥷 Ninja Belajar": "🥷", "🤖 Robot Pintar": "🤖", "🦊 Rubah Cerdas": "🦊"}
        if st.button("💾 Simpan Basis Avatar"):
            st.session_state.avatar_base = map_base[pilihan_base]
            st.success("Avatar dasar berhasil diubah!")
            st.rerun()
            
        st.markdown("---")
        st.subheader("Gunakan Aksesoris yang Sudah Kamu Miliki")
        aksesoris_dipilih = st.selectbox("Pilih Aksesoris Kepala:", st.session_state.unlocked_accessories)
        
        if st.button("🎒 Pakai Aksesoris"):
            if aksesoris_dipilih == "Tanpa Aksesoris":
                st.session_state.avatar_hat = ""
            else:
                # Ambil emojinya saja dari nama barang
                nama_barang = [k for k, v in TOKO_AKSESORIS.items() if k == aksesoris_dipilih][0]
                st.session_state.avatar_hat = TOKO_AKSESORIS[nama_barang]["emoji"]
            st.success("Penampilan berhasil diperbarui!")
            st.rerun()
            
    with tab_toko:
        st.subheader("Beli Item Premium dengan Poin Belajarmu")
        st.write(f"Dompet Digital Kamu: ⭐ **{st.session_state.user_points} PTS**")
        st.markdown("---")
        
        # Memisahkan barang ke bentuk kolom agar menarik
        for item, detail in TOKO_AKSESORIS.items():
            col_nama, col_harga, col_tombol = st.columns([2, 1, 1])
            with col_nama:
                st.write(f"### {item}")
            with col_harga:
                st.write(f"💰 {detail['harga']} PTS")
            with col_tombol:
                if item in st.session_state.unlocked_accessories:
                    st.button("✅ Sudah Dimiliki", key=item, disabled=True)
                else:
                    if st.button("🛒 Beli", key=item):
                        if st.session_state.user_points >= detail["harga"]:
                            st.session_state.user_points -= detail["harga"]
                            st.session_state.unlocked_accessories.append(item)
                            st.success(f"Berhasil membeli {item}! Silakan pakai di tab 'Edit Karakter'.")
                            st.rerun()
                        else:
                            st.error("Poin tidak mencukupi! Ayo membaca lebih banyak materi lagi.")
