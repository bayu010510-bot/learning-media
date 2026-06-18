# ==========================================
# FILE: database_soal.py
# FUNGSI: Bank Soal Terstruktur (Mata Pelajaran -> Kelas -> Bab -> Sub-bab)
# ==========================================

BANK_SOAL_PRO = {
    "Fisika": {
        "Kelas 10": {
            "Kinematika Partikel": {
                "Gerak Lurus Berubah Beraturan": [
                    {
                        "soal": "Dalam persiapan menyambut acara lari maraton SMANSARUN, seorang pelari mulai memacu kecepatannya saat mendekati garis finis. Ia mempercepat larinya dari kecepatan awal 2 m/s menjadi 6 m/s secara konstan dalam waktu 4 detik. Berapakah jarak total yang ditempuh pelari tersebut selama proses percepatan berlangsung?",
                        "opsi": ["16 meter", "32 meter", "8 meter", "24 meter"],
                        "jawaban": "16 meter",
                        "pem": "Gunakan persamaan GLBB. Pertama, cari percepatan (a):<br>$a = \\frac{v_t - v_0}{t} = \\frac{6 - 2}{4} = 1 \\text{ m/s}^2$<br>Lalu, hitung jarak tempuh (s):<br>$s = v_0 \\cdot t + \\frac{1}{2} \\cdot a \\cdot t^2$<br>$s = 2(4) + \\frac{1}{2}(1)(4^2)$<br>$s = 8 + 8 = 16 \\text{ meter}$."
                    },
                    {
                        "soal": "Sebuah mobil mengerem mendadak dari kecepatan 20 m/s hingga berhenti total dalam waktu 5 detik untuk menghindari tabrakan. Berapakah perlambatan mobil tersebut?",
                        "opsi": ["-4 m/s²", "-5 m/s²", "-2 m/s²", "-10 m/s²"],
                        "jawaban": "-4 m/s²",
                        "pem": "$a = \\frac{v_t - v_0}{t} = \\frac{0 - 20}{5} = -4 \\text{ m/s}^2$."
                    }
                ]
            }
        }
    },
    "Ekonomi": {
        "Kelas 10": {
            "Konsep Manajemen & Bisnis Digital": {
                "Pemasaran Digital & Pertumbuhan Eksponensial": [
                    {
                        "soal": "Sebuah akun TikTok @gitarsurabaya yang menjual instrumen akustik mengalami lonjakan penonton eksponensial setelah memposting video tutorial genjrengan pola DDUUDD untuk lagu dari Raim Laode. Jika penonton awal video tersebut adalah 100 orang dan jumlahnya berlipat ganda setiap 3 hari, berapa total penonton pada hari ke-15?",
                        "opsi": ["3.200 penonton", "1.500 penonton", "6.400 penonton", "800 penonton"],
                        "jawaban": "3.200 penonton",
                        "pem": "Gunakan deret geometri: $U_n = a \\cdot r^n$.<br>Waktu = 15 hari. Karena berlipat setiap 3 hari, maka terjadi $n = \\frac{15}{3} = 5$ kali pelipatan.<br>Jumlah = $100 \\times 2^5 = 100 \\times 32 = 3.200 \\text{ penonton}$."
                    }
                ]
            }
        }
    },
    "Kimia": {
        "Kelas 11": {
            "Kinetika Kimia": {
                "Faktor-Faktor Laju Reaksi": [
                    {
                        "soal": "Dalam penyusunan LK-10 untuk inovasi resep masakan daerah, SOP menyebutkan bahwa pemanasan bumbu pada suhu 60°C membutuhkan waktu 20 menit agar matang sempurna. Diketahui setiap kenaikan suhu sebesar 10°C akan mempercepat laju reaksi pencoklatan (Maillard) menjadi 2 kali lipat lebih cepat. Jika koki menaikkan suhu kompor menjadi 80°C, berapa waktu yang dibutuhkan bumbu untuk matang?",
                        "opsi": ["5 menit", "10 menit", "2.5 menit", "40 menit"],
                        "jawaban": "5 menit",
                        "pem": "Kenaikan suhu $\\Delta T = 80 - 60 = 20^\\circ\\text{C}$.<br>Karena naik setiap 10°C laju menjadi 2x lipat, maka laju total = $2^{\\frac{20}{10}} = 2^2 = 4$ kali lebih cepat.<br>Waktu reaksi berbanding terbalik dengan laju: $t_{baru} = \\frac{t_{awal}}{4} = \\frac{20}{4} = 5 \\text{ menit}$."
                    }
                ]
            }
        }
    },
    "Seni Budaya": {
        "Kelas 12": {
            "Seni Teater": {
                "Rancangan Naskah Drama": [
                    {
                        "soal": "Dalam penulisan naskah drama musikal berbahasa Jawa moderen yang mengambil inspirasi dari dinamika komunikasi Gen Z (seperti gaya penceritaan film 'Sekawan Limo' atau 'Yowis Ben'), elemen penyutradaraan apa yang paling membedakannya secara struktural dibandingkan dengan teater Ketoprak klasik?",
                        "opsi": ["Penggunaan dialog improvisasi kasual yang disisipi musik pop-indie sebagai transisi emosi adegan.", "Penggunaan pakem tembang macapat yang ketat di setiap pergantian babak.", "Penggunaan latar panggung keraton dengan tata bahasa krama inggil secara penuh.", "Penghilangan unsur komedi demi menjaga nilai moral naskah."],
                        "jawaban": "Penggunaan dialog improvisasi kasual yang disisipi musik pop-indie sebagai transisi emosi adegan.",
                        "pem": "Drama musikal remaja Jawa modern mengandalkan unsur pop-kultur, musik indie/akustik, serta *slang* lokal yang *relatable* dengan Gen Z, berbeda dengan Ketoprak klasik yang terikat erat pada pakem macapat, krama inggil, dan struktur cerita keraton."
                    }
                ]
            }
        }
    }
}
