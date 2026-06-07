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
            "sub_bab": ["2.1 Concept Gotong Royong", "2.2 Toleransi Antarumat"],
            "rangkuman": "• **Gotong Royong**: Budaya asli Indonesia berupa kerja bersama untuk mencapai hasil yang didambakan. Merupakan manifestasi dari persatuan nasional.\n• **Toleransi**: Kunci utama menjaga keselarasan di tengah keberagaman suku, ras, dan agama di Indonesia."
        }
    },
    "Fisika": {
        "Bab 1: Usaha dan Energi": {
            "sub_bab": ["1.1 Pembangkit Listrik", "1.2 Energi Terbarukan"],
