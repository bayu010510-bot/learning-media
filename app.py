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
    st.session_state.avatar_base = "https://img.icons8.com/illustrations/external-pack-flat-symbols-tanah-basah/200/external-student-back-to-school-pack-flat-symbols-tanah-basah.png"
if "avatar_hat" not in st.session_state:
    st.session_state.avatar_hat = ""
if "unlocked_accessories" not in st.session_state:
    st.session_state.unlocked_accessories = ["Tanpa Aksesoris"]

# --- KUSTOMISASI CSS (Arsitektur Grafis Tumpukan Avatar & UI/UX) ---
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
    
    .avatar-container {
        width: 140px; height: 140px; margin: 0 auto 15px auto;
        position: relative; background: radial-gradient(circle, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 50%; border: 4px solid #3B82F6; display: flex; align-items: center; justify-content: center;
    }
    
    .avatar-base-img {
        width: 100px; height: 100px; object-fit: contain; position: absolute; bottom: 10px; z-index: 1;
    }
    
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

# --- STRUKTUR DATA MATERI LENGKAP + RANGKUMAN ---
DAFTAR_KELAS = ["Kelas 10", "Kelas 11", "Kelas 12"]

DATA_MATERI = {
    "Pendidikan Pancasila (PKn)": {
        "Bab 1: Pancasila sebagai Dasar Negara": {
            "sub_bab": ["1.1 Sejarah Pancasila", "1.2 Penerapan Pancasila"],
            "rangkuman": "• **Sejarah Pancasila**: Dirumuskan dalam Sidang BPUPKI pertama oleh Ir. Soekarno, Moh. Yamin, dan Soepomo. Istilah Pancasila lahir pada 1 Juni 1945.\n• **Penerapan**: Pancasila berfungsi sebagai pandangan hidup bangsa dan dasar negara yang menjiwai seluruh hukum di Indonesia."
        },
        "Bab 2: Bhinneka Tunggal Ika": {
            "sub_bab": ["2.1 Konsep Gotong Royong", "2.2 Toleransi Antarumat"],
            "rangkuman": "• **Gotong Royong**: Budaya asli Indonesia berupa kerja bersama untuk mencapai hasil yang didambakan. Merupakan manifestasi dari persatuan nasional.\n• **Toleransi**: Kunci utama menjaga keselarasan di tengah keberagaman suku, ras, dan agama di Indonesia."
        }
    },
    "Fisika": {
        "Bab 1: Usaha dan Energi": {
            "sub_bab": ["1.1 Pembangkit Listrik", "1.2 Energi Terbarukan"],
            "rangkuman": "• **Usaha ($W$)**: Perkalian gaya dengan perpindahan ($W = F \\cdot s$).\n• **Energi Mekanik**: Gabungan Energi Kinetik ($Ek = \\frac{1}{2}mv^2$) dan Energi Potensial ($Ep = mgh$).\n• **PLTA**: Memanfaatkan energi potensial air terjun untuk memutar turbin generator menjadi energi listrik."
        },
        "Bab 2: Momentum dan Impuls": {
            "sub_bab": ["2.1 Konsep Impuls", "2.2 Tumbukan Benda"],
            "rangkuman": "• **Momentum ($p$)**: Tingkat kesukaran menghentikan benda bergerak ($p = m \\cdot v$).\n• **Impuls ($I$)**: Perubahan momentum yang disebabkan oleh gaya yang bekerja dalam waktu singkat ($I = F \\cdot \\Delta t = \\Delta p$).\n• **Hukum Kekekalan Momentum**: Jumlah momentum sebelum tumbukan sama dengan jumlah momentum setelah tumbukan."
        }
    },
    "Kimia": {
        "Bab 1: Hukum Dasar Kimia": {
            "sub_bab": ["1.1 Penyetaraan Reaksi Kimia", "1.2 Mol dan Massa Molar"],
            "rangkuman": "• **Penyetaraan Reaksi**: Menyamakan jumlah atom di ruas kiri (reaktan) dan ruas kanan (produk) sesuai Hukum Kekekalan Massa (Lavoisier).\n• **Konsep Mol**: Satuan jumlah zat dalam kimia. $1 \\text{ mol} = 6,02 \\times 10^{23}$ partikel."
        },
        "Bab 2: Struktur Atom": {
            "sub_bab": ["2.1 Model Atom", "2.2 Konfigurasi Elektron"],
            "rangkuman": "• **Model Atom**: Berkembang dari teori Dalton, Thomson, Rutherford, Bohr, hingga Mekanika Kuantum.\n• **Konfigurasi Elektron**: Susunan elektron pada kulit atom berdasarkan asas Aufbau, larangan Pauli, dan kaidah Hund."
        }
    },
    "Biologi": {
        "Bab 1: Keanekaragaman Hayati": {
            "sub_bab": ["1.1 Tingkat Keanekaragaman", "1.2 Flora dan Fauna Indonesia"],
            "rangkuman": "• **Tingkat Keanekaragaman**: Terbagi menjadi 3 tingkat, yaitu tingkat Gen (variasi dalam spesies), tingkat Spesies (antar spesies), dan tingkat Ekosistem.\n• **Garis Wallace & Weber**: Memisahkan tipe fauna Indonesia menjadi Asiatis (Barat), Peralihan (Tengah), dan Australis (Timur)."
        },
        "Bab 2: Ekologi dan Lingkungan": {
            "sub_bab": ["2.1 Komponen Ekosistem", "2.2 Daur Biogeokimia"],
            "rangkuman": "• **Komponen Ekosistem**: Terdiri dari Biotik (makhluk hidup) dan Abiotik (benda tak hidup seperti air, cahaya, tanah).\n• **Interaksi**: Membentuk rantai makanan, jaring-jaring makanan, dan daur materi alami."
        }
    },
    "Ekonomi": {
        "Bab 1: Konsep Dasar Ilmu Ekonomi": {
            "sub_bab": ["1.1 Kebutuhan dan Kelangkaan", "1.2 Sistem Ekonomi"],
            "rangkuman": "• **Kelangkaan (Scarcity)**: Masalah inti ekonomi di mana kebutuhan manusia tidak terbatas, sedangkan alat pemuas kebutuhan jumlahnya terbatas.\n• **Biaya Peluang (Opportunity Cost)**: Biaya yang timbul akibat memilih satu alternatif dan mengorbankan alternatif terbaik lainnya."
        },
        "Bab 2: Ketenagakerjaan": {
            "sub_bab": ["2.1 Angkatan Kerja", "2.2 Pengangguran dan Dampaknya"],
            "rangkuman": "• **Ketenagakerjaan**: Penduduk yang berada dalam usia kerja (15 tahun ke atas).\n• **Pengangguran**: Orang yang tidak bekerja, sedang mencari kerja, atau sedang mempersiapkan suatu usaha baru."
        }
    },
    "Sosiologi": {
        "Bab 1: Struktur Sosial": {
            "sub_bab": ["1.1 Stratifikasi Sosial", "1.2 Diferensiasi Sosial"],
            "rangkuman": "• **Stratifikasi Sosial**: Pelapisan masyarakat secara vertikal/bertingkat (misal: kelas ekonomi, kasta).\n• **Diferensiasi Sosial**: Pengelompokan masyarakat secara horizontal/sejajar tanpa tingkatan (misal: ras, suku, profesi, agama)."
        },
        "Bab 2: Konflik dan Integrasi Sosial": {
            "sub_bab": ["2.1 Akar Konflik di Masyarakat", "2.2 Resolusi Konflik"],
            "rangkuman": "• **Konflik**: Proses sosial antara dua orang atau lebih yang berusaha menyingkirkan pihak lain.\n• **Integrasi**: Proses penyesuaian unsur-unsur yang berbeda dalam masyarakat sehingga menjadi satu kesatuan."
        }
    },
    "Geografi": {
        "Bab 1: Pengetahuan Dasar Geografi": {
            "sub_bab": ["1.1 Objek Studi Geografi", "1.2 Peta dan Penginderaan Jauh"],
            "rangkuman": "• **Objek Geografi**: Terdiri dari objek material (Litosfer, Atmosfer, Hidrosfer, Biosfer, Antroposfer) dan objek formal (pendekatan analisis keruangan, kelingkungan, kompleks wilayah)."
        },
        "Bab 2: Dinamika Bumi": {
            "sub_bab": ["2.1 Litosfer (Lapisan Batuan)", "2.2 Atmosfer dan Cuaca"],
            "rangkuman": "• **Litosfer**: Lapisan batuan pembentuk kulit bumi, memicu tenaga endogen (tektonisme, vulkanisme) dan eksogen.\n• **Atmosfer**: Lapisan udara bumi yang mempengaruhi iklim, cuaca, dan suhu lokal harian."
        }
    },
    "Sejarah": {
        "Bab 1: Konsep Dasar Sejarah": {
            "sub_bab": ["1.1 Berpikir Diakronik & Sinkronik", "1.2 Sumber-sumber Sejarah"],
            "rangkuman": "• **Diakronik**: Berpikir memanjang dalam waktu tetapi menyempit dalam ruang (kronologis berurutan).\n• **Sinkronik**: Berpikir meluas dalam ruang tetapi terbatas dalam waktu (mengkaji struktur peristiwa secara mendalam)."
        },
        "Bab 2: Pergerakan Nasional": {
            "sub_bab": ["2.1 Organisasi Pergerakan", "2.2 Sumpah Pemuda"],
            "rangkuman": "• **Pergerakan**: Fase perjuangan Indonesia menggunakan organisasi modern (Budi Utomo, Sarekat Islam, dll).\n• **Sumpah Pemuda**: 28 Oktober 1928, tonggak utama ikrar satu tanah air, satu bangsa, dan satu bahasa."
        }
    },
    "Bahasa Inggris": {
        "Bab 1: Narrative Text": {
            "sub_bab": ["1.1 Generic Structure", "1.2 Fairy Tales and Legends"],
            "rangkuman": "• **Definition**: A text that tells an imaginative story to entertain the readers.\n• **Generic Structure**: Orientation ➔ Complication ➔ Resolution ➔ Re-orientation/Coda."
        },
        "Bab 2: Analytical Exposition": {
            "sub_bab": ["2.1 Presenting Arguments", "2.2 Language Features"],
            "rangkuman": "• **Definition**: A text that evaluates a topic critically but focuses only on one side of an argument.\n• **Structure**: Thesis ➔ Arguments ➔ Reiteration."
        }
    },
    "Bahasa Indonesia": {
        "Bab 1: Teks Laporan Hasil Observasi": {
