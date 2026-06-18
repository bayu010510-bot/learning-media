# ==========================================
# FILE: database_soal.py
# FUNGSI: Brankas Penyimpanan Bank Soal Ujian
# ==========================================

BANK_SOAL_PRO = {
    "Matematika": {
        "Kelas 10": {
            "Eksponen dan Logaritma": [
                {"soal": "Nilai dari $2^3 \\times 2^2$ adalah...", "opsi": ["32", "16", "64", "8"], "jawaban": "32", "pem": "Sifat pangkat: $2^{3+2} = 2^5 = 32$."},
                {"soal": "Bentuk sederhana dari $\\frac{x^5}{x^2}$ adalah...", "opsi": ["$x^3$", "$x^7$", "$x^{2.5}$", "$x^1$"], "jawaban": "$x^3$", "pem": "Sifat pembagian pangkat: $x^{5-2} = x^3$."},
                {"soal": "Jika $3^x = 81$, maka nilai $x$ adalah...", "opsi": ["4", "3", "5", "6"], "jawaban": "4", "pem": "$3^4 = 81$, maka $x = 4$."},
                {"soal": "Nilai dari $\\log_2 8$ adalah...", "opsi": ["3", "4", "2", "8"], "jawaban": "3", "pem": "$2^3 = 8$, jadi $\\log_2 8 = 3$."},
                {"soal": "Sifat logaritma $\\log a + \\log b$ sama dengan...", "opsi": ["$\\log(a \\times b)$", "$\\log(a+b)$", "$\\log(a/b)$", "$a \\log b$"], "jawaban": "$\\log(a \\times b)$", "pem": "Penjumlahan log dengan basis sama menjadi perkalian numerus."}
            ],
            "Persamaan Linear": [
                {"soal": "Jika $2x + 5 = 15$, berapakah nilai $x$?", "opsi": ["5", "10", "4", "6"], "jawaban": "5", "pem": "$2x = 15 - 5 \\Rightarrow 2x = 10 \\Rightarrow x = 5$."},
                {"soal": "Penyelesaian dari $3(x - 2) = 9$ adalah...", "opsi": ["5", "3", "1", "7"], "jawaban": "5", "pem": "$3x - 6 = 9 \\Rightarrow 3x = 15 \\Rightarrow x = 5$."}
            ]
        }
    },
    "Fisika": {
        "Kelas 10": {
            "Hakikat Fisika dan Besaran": [
                {"soal": "Dimensi dari besaran Gaya adalah...", "opsi": ["$MLT^{-2}$", "$ML^2T^{-2}$", "$MLT^{-1}$", "$LT^{-2}$"], "jawaban": "$MLT^{-2}$", "pem": "Gaya ($F$) = massa ($m$) $\\times$ percepatan ($a$). Dimensi: $M \\times LT^{-2}$."},
                {"soal": "Besaran pokok menurut SI berjumlah...", "opsi": ["7", "5", "9", "6"], "jawaban": "7", "pem": "Ada 7 besaran pokok: Panjang, Massa, Waktu, Suhu, Kuat Arus, Intensitas Cahaya, Jumlah Zat."},
                {"soal": "Satuan dari Energi dalam Sistem Internasional (SI) adalah...", "opsi": ["Joule", "Newton", "Watt", "Pascal"], "jawaban": "Joule", "pem": "Satuan Energi/Usaha adalah Joule ($kg\\cdot m^2/s^2$)."}
            ],
            "Gerak Lurus": [
                {"soal": "Sebuah mobil bergerak dengan kecepatan konstan 20 m/s. Jarak yang ditempuh dalam 5 detik adalah...", "opsi": ["100 m", "50 m", "200 m", "25 m"], "jawaban": "100 m", "pem": "Jarak = Kecepatan $\\times$ Waktu = $20 \\times 5 = 100$ meter."}
            ]
        }
    },
    "Kimia": {
        "Kelas 10": {
            "Struktur Atom": [
                {"soal": "Partikel penyusun atom yang bermuatan negatif adalah...", "opsi": ["Elektron", "Proton", "Neutron", "Nukleon"], "jawaban": "Elektron", "pem": "Elektron bermuatan negatif, proton positif, dan neutron netral."},
                {"soal": "Nomor massa suatu unsur menunjukkan jumlah...", "opsi": ["Proton + Neutron", "Proton + Elektron", "Neutron saja", "Elektron saja"], "jawaban": "Proton + Neutron", "pem": "Nomor massa (A) = Jumlah Proton (Z) + Jumlah Neutron (n)."}
            ]
        }
    }
}
