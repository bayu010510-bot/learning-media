# ==========================================
# FILE: database_rangkuman.py
# FUNGSI: Database Silabus Kurikulum Merdeka (Edisi Bebas Bug LaTeX)
# ==========================================

DATA_MATERI = {
    "Matematika": {
        "Kelas 10": {
            "Bab 1: Eksponen dan Logaritma": {
                "sub_bab": ["Sifat Eksponen", "Fungsi Eksponen", "Bentuk Akar", "Sifat Logaritma", "Penyelesaian Masalah"],
                "rangkuman": r"""
#### 🚀 Rahasia Eksponen & Logaritma
Eksponen adalah perkalian berulang, sedangkan Logaritma adalah **invers (kebalikan)** dari eksponen. Menguasai satu berarti menguasai keduanya!

#### 🔑 Sifat-Sifat Dewa
- **Eksponen:** $a^m \cdot a^n = a^{m+n}$ (Kali = Tambah Pangkat)
- **Logaritma:** $^a\!\log x + ^a\!\log y = ^a\!\log(x \cdot y)$

> **🧠 KONSEP HOTS UTBK:**
> Di soal ujian, logaritma sering digabung dengan Persamaan Kuadrat. Jika melihat pangkat eksponen bertingkat, segera gunakan pemisalan variabel $p = a^x$!
"""
                "link_drive": "https://drive.google.com/drive/folders/1sBINxjHzzlLTWI1wZuwIEcLVURrQUncY?usp=drive_link"
            },
            "Bab 2: Barisan dan Deret": {
                "sub_bab": ["Barisan Aritmatika", "Barisan Geometri", "Deret Tak Hingga", "Aplikasi (Bunga, Anuitas)"],
                "rangkuman": r"""
#### 🚀 Melipatgandakan Angka
Barisan adalah urutan angka dengan pola pasti. Aritmatika ditandai dengan **Beda (+/-)**, sedangkan Geometri ditandai dengan **Rasio (x/÷)**.

#### 🔑 Rumus Utama
- **Suku ke-n Aritmatika:** $U_n = a + (n-1)b$
- **Suku ke-n Geometri:** $U_n = a \cdot r^{n-1}$

> **💡 TRIK STUDI KASUS BISNIS:**
> Deret tak hingga geometri berlimpah di soal tes PTN, terutama kasus bola pantul! Gunakan rumus cepat pantulan: $S_{\infty} = \frac{a(b+c)}{b-c}$ (di mana r = c/b).
"""
                "link_drive": "https://drive.google.com/drive/folders/1oP0aA5GESoYShdo1SBeGQgb3Slo6q-uF?usp=drive_link"
            },
            "Bab 3: Vektor dan Operasinya": {
                "sub_bab": ["Notasi Vektor", "Vektor di R2 and R3", "Operasi Vektor", "Cross & Dot Product"],
                "rangkuman": r"""
#### 🚀 Menavigasi Ruang Dimensi
Vektor bukanlah sekadar angka; ia memiliki **Nilai (Besar)** dan **Arah**. 

#### 🔑 Operasi Vektor
- **Panjang Vektor:** $|v| = \sqrt{x^2 + y^2 + z^2}$
- **Dot Product:** Mengkombinasikan dua vektor menjadi sebuah angka pasti (skalar). $a \cdot b = |a| |b| \cos \theta$

> **🧠 TIPS UJIAN:**
> Jika soal menyebutkan "Dua vektor saling tegak lurus", itu adalah kata sandi bahwa **Dot Product mereka bernilai NOL ($a \cdot b = 0$)**!
"""
"link_drive": "https://drive.google.com/drive/folders/1ww_FFUqoMVBCNFrByARTYLLvpJfqY40S?usp=drive_link"
            },
            "Bab 4: Trigonometri": {
                "sub_bab": ["Penamaan Sisi", "Perbandingan Trigonometri", "Sudut Berelasi", "Konteks Nyata"],
                "rangkuman": r"""
#### 🚀 Misteri Sudut & Segitiga
Trigonometri mengkaji hubungan antara sudut dan panjang sisi segitiga siku-siku.

#### 🔑 Aturan SINDEMI
- **Sinus:** Depan / Miring
- **Cosinus:** Samping / Miring
- **Tangen:** Depan / Samping

> **💡 ANALISIS HOTS:**
> Sudut relasi kuadran sangat vital. Hafalkan "Semua - Sindikat - Tangannya - Kosong" (Kuadran I semua positif, II Sin positif, III Tan positif, IV Cos positif).
"""
                "link_drive": "https://drive.google.com/drive/folders/1-N1gX50UJdxI2i04aqPtdRyk4-3iba7H?usp=drive_link"
            },
            "Bab 5: Sistem Persamaan Linear": {
                "sub_bab": ["SPLDV", "SPLTV", "SPtLDV", "Model Matematika"],
                "rangkuman": r"""
#### 🚀 Bold Perubahan Variabel
SPLDV (2 variabel) membentuk garis yang saling memotong, sedangkan SPLTV (3 variabel) berurusan dengan bidang tiga dimensi.

#### 🔑 Langkah Penyelesaian
Lakukan Kombinasi **Eliminasi** (menghilangkan satu variabel dengan menjumlah/mengurang) jika dirasa sulit dilanjutkan dengan teknik **Substitusi** (memasukkan nilai ke persamaan lain).

> **🧠 KUNCI MODEL MATEMATIKA:**
> Langkah tersulit di UTBK bukan menghitungnya, melainkan menerjemahkan cerita soal menjadi bentuk $x$ dan $y$. Fokus pada kalimat "Total" atau "Maksimal".
"""
                "link_drive": "https://drive.google.com/drive/folders/1KcHYn9-3ouoE6GEQtvHBxy_WfI0JAlHm?usp=drive_link"
            },
            "Bab 6: Fungsi Kuadrat": {
                "sub_bab": ["Grafik Fungsi", "Mengonstruksi Fungsi", "Nilai Maks/Min", "Aplikasi"],
                "rangkuman": r"""
#### 🚀 Melengkung Membentuk Parabola
Fungsi kuadrat memiliki bentuk umum $f(x) = ax^2 + bx + c$. Jika $a > 0$ kurva terbuka ke atas (senyum), jika $a < 0$ terbuka ke bawah (cemberut).

#### 🔑 Titik Puncak (Puncak Parabola)
- **Sumbu Simetri (x):** $x_p = \frac{-b}{2a}$
- **Nilai Maks/Min (y):** $y_p = \frac{D}{-4a}$

> **💡 TRIK KILAT:**
> Jika fungsi kuadrat menyinggung sumbu X, artinya Diskriminan bernilai nol ($D = b^2 - 4ac = 0$).
"""
                "link_drive": "https://drive.google.com/drive/folders/1tGZ0Wf5Cr5IuQdfH2QnZ9Li6-ddoZnQc?usp=drive_link"
            },
            "Bab 7: Statistika": {
                "sub_bab": ["Distribusi Frekuensi", "Histogram/Ogive", "Pemusatan Data", "Letak Data", "Penyebaran Data"],
                "rangkuman": r"""
#### 🚀 Membaca Pola Dibalik Angka
Statistika adalah seni mengubah data acak menjadi informasi berharga.

#### 🔑 3 Ukuran Pemusatan Utama
1. **Mean:** Rata-rata dari total data.
2. **Median:** Nilai tengah setelah data diurutkan.
3. **Modus:** Data yang frekuensinya paling sering muncul.

> **🧠 TIPS UTBK STATISTIKA:**
> Hati-hati dengan konsep Simpangan Baku. Jika semua data dikali 2, maka rata-rata ikut dikali 2, TETAPI varians akan dikali $2^2$ (kuadratnya)!
"""
                "link_drive": "https://drive.google.com/drive/folders/1awA-Lv_X_X7emg1WZ0UIFLEtgMxGRgyo?usp=drive_link"
            },
            "Bab 8: Peluang": {
                "sub_bab": ["Ruang Sampel", "Peluang Kejadian", "Frekuensi Harapan", "Saling Lepas/Bebas"],
                "rangkuman": r"""
#### 🚀 Mengukur Kemungkinan Takdir
Peluang adalah rasio antara kejadian yang diharapkan (Titik Sampel) dengan total semua kemungkinan (Ruang Sampel).

#### 🔑 Kaidah Pencacahan
- **Kombinasi:** Memilih tanpa mempedulikan urutan (A, B sama dengan B, A).
- **Permutasi:** Susunan di mana urutan sangat penting (Jabatan ketua, juara 1-2-3).

> **💡 KUNCI CEPAT:**
> Jika soal memakai kata hubung **"DAN"**, kalikan peluangnya. Jika menggunakan kata hubung **"ATAU"**, jumlahkan peluangnya!
"""
                "link_drive": "https://drive.google.com/drive/folders/1ZMmZwbI6yp1mFykwn7u_zhm-Jf1w_eCU?usp=drive_link"
            }
        },
        "Kelas 11": {
            "Bab 1: Komposisi & Invers Fungsi": {
                "sub_bab": ["Domain/Range", "Aljabar Fungsi", "Fungsi Komposisi", "Fungsi Invers", "Invers Komposisi"],
                "rangkuman": r"""
#### 🚀 Mesin Pemroses Angka
Fungsi ibarat mesin giling. Fungsi komposisi $(f \circ g)(x)$ berarti memasukkan output mesin $g$ ke dalam mesin $f$. Fungsi Invers $f^{-1}(x)$ adalah cara membalikkan proses kerja mesinnya.

#### 🔑 Trik Cepat Invers Pecahan
Jika terdapat fungsi pecahan berupa $f(x) = \frac{ax + b}{cx + d}$, maka untuk mencari fungsi inversnya kita cukup menukar posisi angka koefisien pada posisi $a$ dan $d$, kemudian balikkan tanda positif atau negatifnya menjadi:
$$f^{-1}(x) = \frac{-dx + b}{cx - a}$$
"""
            },
            "Bab 2: Lingkaran": {
                "sub_bab": ["Busur Lingkaran", "Sudut Pusat & Keliling", "Tali Busur & Garis Singgung", "Persamaan Lingkaran"],
                "rangkuman": r"""
#### 🚀 Geometri Sang Bundar
Lingkaran memiliki persamaan analitik $(x-a)^2 + (y-b)^2 = r^2$ untuk titik pusat (a,b) dengan jari-jari r.

#### 🔑 Sudut Krusial
Sudut Pusat selalu **2x lebih besar** daripada Sudut Keliling yang menghadap busur yang sama.
"""
            },
            "Bab 3: Matriks": {
                "sub_bab": ["Ordo & Notasi", "Jenis & Transpose", "Operasi Matriks", "Determinan & Invers", "Penyelesaian SPL"],
                "rangkuman": r"""
#### 🚀 Kotak Data Canggih
Matriks adalah sekumpulan angka yang disusun dalam baris dan kolom. Syarat **Perkalian Matriks**: Kolom matriks pertama HARUS SAMA dengan baris matriks kedua.

> **🧠 SIFAT SAKTI DETERMINAN:**
> $|A \cdot B| = |A| \cdot |B|$. Jika matriks dikali sebuah angka konstan $k$, maka determinannya $|k \cdot A| = k^n \cdot |A|$ (n adalah ordo matriks).
"""
            },
            "Bab 4: Transformasi Geometri": {
                "sub_bab": ["Translasi", "Refleksi", "Rotasi", "Dilatasi", "Komposisi Transformasi"],
                "rangkuman": r"""
#### 🚀 Manipulasi Koordinat
1. **Translasi (Geser):** Titik $x, y$ sekadar ditambah.
2. **Refleksi (Cermin):** Koordinat dibalik tergantung cerminnya.
3. **Rotasi (Putar):** Membutuhkan titik pusat dan sudut putar.
4. **Dilatasi (Perbesar/Perkecil):** Koordinat dikali dengan faktor skala $k$.
"""
            }
        },
        "Kelas 12": {
            "Bab 1: Geometri Ruang (Dimensi Tiga)": {
                "sub_bab": ["Jarak Antar Titik", "Jarak Titik ke Garis", "Jarak Titik ke Bidang", "Sudut Ruang"],
                "rangkuman": r"""
#### 🚀 Memvisualisasikan 3D
Menganalisis jarak dan sudut di ruang seperti kubus. 

#### 🔑 Trik Cepat Kubus (Rusuk = a)
- **Diagonal Sisi:** $a\sqrt{2}$
- **Diagonal Ruang:** $a\sqrt{3}$

> **🧠 STRATEGI UTBK:**
> Tarik garis bantu hingga membentuk Segitiga Siku-siku, lalu hajar dengan Pythagoras!
"""
            },
            "Bab 2: Limit Fungsi Aljabar & Trigonometri": {
                "sub_bab": ["Konsep Limit", "Sifat Limit", "Limit Tak Hingga", "Limit Trigonometri"],
                "rangkuman": r"""
#### 🚀 Menembus Batas Pendekatan
Limit mengkaji apa yang terjadi pada suatu fungsi saat nilainya *mendekati* titik kritis, bukan saat *berada* di titik tersebut.

> **💡 TRIK L'HOPITAL:**
> Jika disubstitusi hasilnya $0/0$ atau $\infty/\infty$, langsung turunkan (diferensialkan) pembilang dan penyebutnya!
"""
            },
            "Bab 3: Turunan Fungsi (Diferensial)": {
                "sub_bab": ["Konsep Turunan", "Rumus Turunan", "Sifat Turunan", "Aplikasi Turunan"],
                "rangkuman": r"""
#### 🚀 Laju Perubahan Instan
Turunan pertama $f'(x)$ mewakili kemiringan (gradien) garis singgung kurva. 

#### 🔑 Aplikasi Ekstrim
Untuk mencari titik Maksimum atau Minimum dari keuntungan pabrik / luas tanah, cukup turunkan persamaannya lalu jadikan nol! ($f'(x) = 0$).
"""
            },
            "Bab 4: Integral (Antiturunan)": {
                "sub_bab": ["Integral Tak Tentu", "Sifat Integral", "Integral Tentu", "Teknik Pengintegralan", "Luas Kurva"],
                "rangkuman": r"""
#### 🚀 Mengembalikan Turunan & Menghitung Luas
Integral Tak Tentu menghasilkan fungsi asal (+ C), sedangkan Integral Tentu menghasilkan nilai angka absolut (Luas area).

> **🧠 TRIK LUAS PARABOLA:**
> Luas area tertutup antara parabola dan garis bisa dicari kilat dengan rumus $L = \frac{D\sqrt{D}}{6a^2}$ tanpa perlu repot mengintegral!
"""
            }
        }
    },
    
    "Fisika": {
        "Kelas 10": {
            "Bab 1: Pengukuran Ilmiah": {
                "sub_bab": ["Alat Ukur", "Besaran & Dimensi", "Angka Penting", "Ketidakpastian"],
                "rangkuman": r"""
#### 🚀 Mengukur Presisi Semesta
Beda alat, beda ketelitian. Jangka sorong punya ketelitian 0,01 cm, sedangkan Mikrometer Sekrup sangat akurat di 0,001 cm!

> **🔑 ATURAN ANGKA PENTING:**
> Saat mengalikan atau membagi, hasil finals HANYA BOLEH mengandung Angka Penting paling sedikit dari komponen yang dihitung!
"""
                "link_drive": "https://drive.google.com/drive/folders/1RdLl6_wdI0mnMWDHaQ6jIIPHj0ya4YFe?usp=drive_link"
            },
            "Bab 2: Energi Terbarukan": {
                "sub_bab": ["Bentuk Energi", "Hukum Kekekalan Energi", "Sumber Fosil vs Terbarukan", "Dampak Lingkungan"],
                "rangkuman": r"""
#### 🚀 Transisi Hijau
Energi mekanik ($E_M$) selalu kekal, di mana $E_M = E_{Potensial} + E_{Kinetik}$. Saat di titik tertinggi, Ek bernilai nol. Saat menyentuh tanah, Ep bernilai nol.
"""
                "link_drive": "https://drive.google.com/drive/folders/1ZVqKQoeaHyfRg92F1kKyOUyubtJhtMGa?usp=drive_link" 
            }
        },
        "Kelas 11": {
            "Bab 1: Kinematika Gerak": {
                "sub_bab": ["GLB & GLBB", "Gerak Vertikal", "Gerak Parabola", "Gerak Melingkar"],
                "rangkuman": r"""
#### 🚀 Menggambarkan Laju Partikel
Gabungan GLB (sumbu x horizontal) dan GLBB (sumbu y vertikal yang ditarik gravitasi) menciptakan lintasan melengkung indah yang kita sebut **Gerak Parabola**.
"""
            },
            "Bab 2: Dinamika Gerak (Hukum Newton)": {
                "sub_bab": ["Hukum Newton", "Gaya Gesek/Normal", "Bidang Miring & Katrol", "Gaya Sentripetal"],
                "rangkuman": r"""
#### 🚀 Misteri Dibalik Gerakan
- **Newton 1:** Kelembaman ($\Sigma F = 0$, benda diam akan tetap diam).
- **Newton 2:** Percepatan ($\Sigma F = m \cdot a$).
- **Newton 3:** Action = -Reaction.

> **🧠 TIPS BIDANG MIRING:**
> Gaya yang menarik balok turun sejajar bidang miring selalu bernilai $W \cdot \sin \theta$, sedangkan Gaya Normalnya adalah $W \cdot \cos \theta$.
"""
            },
            "Bab 3: Statika dan Dinamika Rotasi": {
                "sub_bab": ["Torsi & Inersia", "Kesetimbangan", "Titik Berat", "Kekekalan Momentum Sudut"],
                "rangkuman": r"""
#### 🚀 Momen Gaya (Torsi)
Apa yang membuat pintu berputar saat didorong? Torsi! Torsi ($\tau$) adalah perkalian gaya tarik dengan jaraknya dari engsel. Syarat Benda Tegar Seimbang: $\Sigma F = 0$ dan $\Sigma \tau = 0$.
"""
            },
            "Bab 4: Fluida": {
                "sub_bab": ["Fluida Statis", "Fluida Dinamis"],
                "rangkuman": r"""
#### 🚀 Tekanan Zat Cair & Gas
- **Archimedes:** Gaya apung ke atas seberat air yang dipindahkan.
- **Pascal:** Tekanan air di ruangan tertutup menyebar rata ke segala arah (Dongkrak Hidrolik).
- **Bernoulli (Dinamis):** Semakin cepat aliran air/angin, tekanannya justru SEMAKIN KECIL (Ini prinsip mengapa pesawat bisa terbang).
"""
            },
            "Bab 5: Gelombang, Cahaya, dan Bunyi": {
                "sub_bab": ["Karakteristik Gelombang", "Stasioner & Berjalan", "Gelombang Cahaya", "Gelombang Bunyi"],
                "rangkuman": r"""
#### 🚀 Getaran Energi Alam
Efek Doppler menjelaskan mengapa suara sirine ambulans makin melengking tinggi (Frekuensi naik) saat mendekati kita, dan merendah saat menjauh.
"""
            }
        },
        "Kelas 12": {
            "Bab 1: Termodinamika": {
                "sub_bab": ["Suhu & Kalor", "Teori Kinetik Gas", "Hukum Termodinamika", "Proses & Siklus Carnot"],
                "rangkuman": r"""
#### 🚀 Mesin Penghasil Usaha
Gas yang dipanaskan akan memuai dan menghasilkan Usaha (W). 
> **💡 SIKLUS CARNOT:**
> Tidak ada satupun mesin di dunia yang efisiensinya 100%. Sebagian kalor pasti terbuang ke reservoir suhu rendah!
"""
            },
            "Bab 2: Listrik Statis & Dinamis": {
                "sub_bab": ["Hukum Coulomb & Kapasitor", "Hukum Ohm & Kirchhoff", "Rangkaian Seri-Paralel"],
                "rangkuman": r"""
#### 🚀 Pertarungan Muatan Positif & Negatif
Listrik Statis dipengaruhi Hukum Coulomb (Gaya muatan $F = k\frac{q_1 q_2}{r^2}$). Listrik Dinamis berlaku Hukum Kirchhoff (Arus masuk percabangan sama dengan arus yang keluar).
"""
            },
            "Bab 3: Kemagnetan & Induksi": {
                "sub_bab": ["Medan Magnet", "Gaya Lorentz", "Induksi Faraday", "Transformator & AC"],
                "rangkuman": r"""
#### 🚀 Ilusi Kawat Berarus
Gaya Lorentz adalah gaya dorong ajaib yang dialami kawat berarus saat ditaruh di dekat magnet. Ini adalah fondasi terciptanya Motor Listrik penggerak dunia!
"""
            },
            "Bab 4: Fisika Modern & Kuantum": {
                "sub_bab": ["Relativitas Khusus", "Radiasi Benda Hitam", "Efek Fotolistrik", "Fisika Inti"],
                "rangkuman": r"""
#### 🚀 Einstein & Fisika Inti
Waktu dan panjang ruang tidaklah mutlak! Saat kita bergerak mendekati kecepatan cahaya, Waktu terasa lebih lambat (Dilatasi) dan Ukuran memendek (Kontraksi Panjang).
"""
            }
        }
    },

    "Kimia": {
        "Kelas 10": {
            "Bab 1: Kimia Hijau": {
                "sub_bab": ["12 Prinsip Kimia Hijau", "Isu Lingkungan", "Proses Ramah Lingkungan"],
                "rangkuman": r"""
#### 🚀 Solusi Atas Polusi
Kimia hijau berupaya menciptakan desain proses kimiawi yang mengurangi atau membuang penggunaan bahan beracun demi menekan pemanasan global.
"""
                "link_drive": "https://drive.google.com/drive/folders/1K06zk8SkE3W7XyYZSAgnP8Sw06UMN24Q?usp=drive_link" 
            },
            "Bab 2: Struktur Atom & Hukum Dasar": {
                "sub_bab": ["Model Atom", "Partikel Penyusun", "Isotop/Isobar", "Hukum Dasar Kimia"],
                "rangkuman": r"""
#### 🚀 Partikel Fundamental & Hukum Lavoisier
Massa reaktan sebelum bereaksi SELALU SAMA dengan massa produk sesudah bereaksi di ruang tertutup. Jika sisa abu kayu lebih ringan dari kayunya, itu karena sebagian massanya menguap menjadi gas CO2!
"""
                "link_drive": "https://drive.google.com/drive/folders/1r0E-DCPmEphKuEGIsOasK0IZi-QZeZsk?usp=drive_link" 
            }
        },
        "Kelas 11": {
            "Bab 1: Struktur Atom Modern": {
                "sub_bab": ["Bilangan Kuantum", "Konfigurasi Elektron", "Sifat Periodik"],
                "rangkuman": r"""
#### 🚀 Alamat Absolut Elektron
Elektron tidak berputar di orbit cincin biasa, melainkan menempati awan "Orbital". Alamatnya disebut Bilangan Kuantum (n, l, m, s).
"""
            },
            "Bab 2: Ikatan Kimia": {
                "sub_bab": ["Kestabilan Unsur", "Ikatan Ion, Kovalen, Logam", "Bentuk Molekul VSEPR", "Gaya Antarmolekul"],
                "rangkuman": r"""
#### 🚀 Berpelukan Mengejar Oktet
- **Ion:** Serah terima elektron (Logam kuat ketemu Non-Logam).
- **Kovalen:** Berbagi elektron bareng (Non-Logam sama Non-Logam).

> **🧠 HOTS:** Titik didih H2O (air) sangat tinggi tidak wajar dibanding senyawa sejenisnya karena ia memiliki Gaya super kuat: **Ikatan Hidrogen!**
"""
            },
            "Bab 3: Stoikiometri": {
                "sub_bab": ["Konsep Mol", "Rumus Empiris/Molekul", "Kadar Zat", "Pereaksi Pembatas"],
                "rangkuman": r"""
#### 🚀 Konsep Mol: Jantungnya Hitungan Kimia
Apapun soal kimianya, jadikan satuan MOL terlebih dahulu!
MOL = Massa / Ar (atau Mr).
"""
            },
            "Bab 4: Termokimia": {
                "sub_bab": ["Sistem & Lingkungan", "Eksoterm/Endoterm", "Entalpi", "Penentuan Entalpi"],
                "rangkuman": r"""
#### 🚀 Kalor dan Energi
- **Eksoterm:** Reaksi melepaskan panas ke luar (Cangkir terasa hangat).
- **Endoterm:** Reaksi menyerap panas (Cangkir terasa dingin membeku).
"""
            },
            "Bab 5: Laju Reaksi": {
                "sub_bab": ["Konsep Laju Reaksi", "Teori Tumbukan", "Faktor Pengaruh", "Orde Reaksi"],
                "rangkuman": r"""
#### 🚀 Kinetika & Tabrakan Partikel
Laju reaksi dipercepat oleh: Konsentrasi pekat, Suhu tinggi, Katalis (mak comblang), dan Luas permukaan serbuk yang sangat halus.
"""
            }
        },
        "Kelas 12": {
            "Bab 1: Kesetimbangan Kimia": {
                "sub_bab": ["Reaksi Reversibel", "Tetapan Kesetimbangan", "Pergeseran Le Chatelier", "Aplikasi Industri"],
                "rangkuman": r"""
#### 🚀 Reaksi yang Bisa Bolak-Balik
Asas Le Chatelier: "Jika ada sistem yang diganggu/diubah, sistem akan bergeser untuk MEMINIMALISIR gangguan tersebut agar setimbang kembali."
"""
            },
            "Bab 2: Asam-Basa & Larutan": {
                "sub_bab": ["Teori Asam Basa", "Skala pH", "Larutan Penyangga", "Hidrolisis Garam", "Kelarutan (Ksp)"],
                "rangkuman": r"""
#### 🚀 Asam Kaustik & Basa Licin
Larutan Buffer (Penyangga) ibarat pertahanan tubuh (ada di darah manusia). Walau ditetesi racun asam atau basa sedikit, nilai pH nya TIDAK AKAN BERUBAH tajam!
"""
            },
            "Bab 3: Elektrokimia": {
                "sub_bab": ["Reaksi Redoks", "Sel Volta", "Korosi", "Sel Elektrolisis"],
                "rangkuman": r"""
#### 🚀 Baterai & Karat Logam
Sel Volta mereaksikan bahan kimia untuk *MENGHASILKAN* listrik (Baterai). Sedangkan Sel Elektrolisis *DIBERI* aliran listrik dari luar paksa untuk merusak zat air.
"""
            },
            "Bab 4: Kimia Organik": {
                "sub_bab": ["Kekhasan Karbon", "Alkana/Alkena/Alkuna", "Gugus Fungsi", "Polimer & Makromolekul"],
                "rangkuman": r"""
#### 🚀 Kerangka Senyawa Kehidupan
Karbon (C) memiliki kekhasan sangat unik: Punya 4 "tangan" (elektron valensi) yang bisa berikatan memanjang seperti rantai kereta api! Plastik adalah contoh produk organik polimer.
"""
            }
        }
    },

    "Biologi": {
        "Kelas 10": {
            "Bab 1: Keanekaragaman Hayati": {
                "sub_bab": ["Tingkat Gen/Jenis", "Flora Fauna RI", "Pelestarian", "Klasifikasi"],
                "rangkuman": r"""
#### 🚀 Pesona Kehati Nusantara
Kehati dipengaruhi Genetik, Spesies, dan Ekosistem. Indonesia terbagi oleh **Garis Wallace** (Asiatis vs Peralihan) dan **Garis Weber** (Peralihan vs Australis).
"""
                "link_drive": "https://drive.google.com/drive/folders/1KvwAPEENgvGkLSIjhnal9bZR3aDrUo45?usp=drive_link"
            },
            "Bab 2: Virus": {
                "sub_bab": ["Struktur Virus", "Siklus Litik/Lisogenik", "Peranan Virus", "Pencegahan"],
                "rangkuman": r"""
#### 🚀 Si Partikel Aseluler Mematikan
Virus adalah parasit sejati yang hanya memiliki 1 kode instruksi: RNA atau DNA. Reproduksinya dilakukan dengan membajak pabrik sel tubuh kita lewat siklus Litik (Hancur) atau Lisogenik (Bersembunyi).
"""
                "link_drive": "https://drive.google.com/drive/folders/1gLlUlZXy0K_rstHkMvHlBXCZp-Y79n7N?usp=drive_link"
            },
            "Bab 3: Lingkungan & Ekosistem": {
                "sub_bab": ["Komponen Ekosistem", "Jaring Makanan", "Daur Biogeokimia", "Pencemaran"],
                "rangkuman": r"""
#### 🚀 Jaring Siklus Rantai Alam
Dalam Piramida Ekologi, semakin tinggi level predatornya (Puncak piramida), energi yang ditransfer dari level dasar menjadi semakin sedikit (hanya sekitar 10%).
"""
                 "link_drive": "https://drive.google.com/drive/folders/1Tq34E33zPA3bIloRIMsFpcaFfVZgz4LN?usp=drive_link"
            }
        },
        "Kelas 11": {
            "Bab 1: Sel": {
                "sub_bab": ["Komponen Kimiawi", "Organel Sel", "Sel Hewan vs Tumbuhan", "Transpor Membran"],
                "rangkuman": r"""
#### 🚀 Kota Mandiri Mikroskopis
- **Mitokondria:** Pabrik pembangkit energi (ATP).
- **Lisosom:** Petugas kebersihan/penghancur benda asing.
- **Kloroplas:** Pabrik gula eksklusif (Hanya ada di sel tumbuhan).
"""
            },
            "Bab 2: Struktur & Fungsi Jaringan": {
                "sub_bab": ["Jaringan Tumbuhan", "Jaringan Hewan"],
                "rangkuman": r"""
#### 🚀 Jaringan Pengangkut
Xilem mengangkat air tanah ke daun. Floem mengedarkan gula hasil fotosintesis ke seluruh dahan batang.
"""
            },
            "Bab 3: Sistem Organ (Bagian 1)": {
                "sub_bab": ["Sistem Gerak", "Sistem Sirkulasi", "Sistem Pencernaan"],
                "rangkuman": r"""
#### 🚀 Pompa Darah (Jantung) & Enzim
Pencernaan kimiawi dikendalikan Enzim spesifik. Di lambung, Enzim Pepsin memecah protein keras menjadi serpihan Pepton dengan bantuan Asam Klorida (HCl).
"""
            },
            "Bab 4: Sistem Organ (Bagian 2)": {
                "sub_bab": ["Sistem Pernapasan", "Sistem Ekskresi", "Sistem Koordinasi", "Sistem Reproduksi"],
                "rangkuman": r"""
#### 🚀 Saraf & Ekskresi Limbah Beracun
Ginjal adalah alat ekskresi elit! Proses Nefron ada 3 tahap: Filtrasi (Saringan darah di Glomerulus), Reabsorbsi (Penyerapan vitamin), lalu Augmentasi (Penambahan zat sisa).
"""
            }
        },
        "Kelas 12": {
            "Bab 1: Pertumbuhan & Perkembangan": {
                "sub_bab": ["Konsep Dasar", "Perkecambahan", "Faktor Internal (Hormon)", "Faktor Eksternal"],
                "rangkuman": r"""
#### 🚀 Mekar dan Memanjang (Fitohormon)
- **Auksin:** Mengatur tanaman untuk tumbuh terus melengkung mengejar arah datangnya sinar matahari.
"""
            },
            "Bab 2: Metabolisme Sel": {
                "sub_bab": ["Enzim", "Katabolisme (Respirasi)", "Anabolisme (Fotosintesis)"],
                "rangkuman": r"""
#### 🚀 Glikolisis, Dekarboksilasi & Krebs
Respirasi Oksigenik memecah 1 Molekul Glukosa menjadi energi listrik sel yang sangat besar (36/38 ATP) agar makhluk hidup mampu bergerak aktif.
"""
            },
            "Bab 3: Genetika & Hereditas": {
                "sub_bab": ["DNA & RNA", "Sintesis Protein", "Pembelahan Sel", "Hukum Mendel", "Penyimpangan Mendel", "Hereditas Manusia"],
                "rangkuman": r"""
#### 🚀 Kode Cetak Biru (DNA) Manusia
Gen adalah pita perekat instruksi biologis. Fenomena *Buta Warna* (terikat kromosom X) adalah warisan gen resesif pautan sex.
"""
            },
            "Bab 4: Evolusi & Bioteknologi": {
                "sub_bab": ["Teori Evolusi", "Bioteknologi Konvensional", "Bioteknologi Modern"],
                "rangkuman": r"""
#### 🚀 Kloning & Pemilihan Alam
Bioteknologi modern memanipulasi kode DNA mikroba. Contohnya menyisipkan Gen penghasil Insulin Manusia ke dalam DNA Bakteri.
"""
            }
        }
    },

    "Sejarah": {
        "Kelas 10": {
            "Bab 1: Pengantar Ilmu Sejarah": {
                "sub_bab": ["Syarat & Manfaat", "Ruang & Waktu", "Sinkronik/Diakronik", "Sumber Sejarah", "Tahapan Penelitian"],
                "rangkuman": r"""
#### 🚀 Membedah Mesin Waktu 
- **Diakronik:** Menganalisis sejarah memanjang dalam garis waktu kronologis, tapi ruangnya sempit.
- **Sinkronik:** Menganalisis sejarah melebar membedah struktur kondisinya secara detail, tetapi di satu waktu tertentu saja.
"""
                "link_drive": "https://drive.google.com/drive/folders/1mfk5lUCU0hErOin0Lh3o4DDWJBXdptUC?usp=drive_link"
            },
            "Bab 2: Jalur Rempah & Hindu-Buddha": {
                "sub_bab": ["Teori Masuknya", "Kerajaan Besar", "Sosial-Budaya", "Jalur Rempah"],
                "rangkuman": r"""
#### 🚀 Kedatuan Emas Nusantara
Kerajaan Sriwijaya menguasai Selat Malaka sebagai poros maritim, disusul kebesaran Majapahit yang menyatukan kepulauan Nusantara berkat Sumpah Palapa Gajah Mada.
"""
                "link_drive": "https://drive.google.com/drive/folders/1S20fzBVa-8mls0ZTJL8s3flfyJagr5DO?usp=drive_link"
            },
            "Bab 3: Islamisasi di Nusantara": {
                "sub_bab": ["Teori Masuk", "Saluran Islamisasi", "Kerajaan Islam", "Akulturasi Budaya"],
                "rangkuman": r"""
#### 🚀 Tsunami Akulturasi Halus
Proses masuknya Islam sangat damai via perdagangan (Gujarat), pernikahan, dan pagelaran Wayang adaptasi oleh Walisongo. Masjid Demak menjadi bukti akulturasi budaya.
"""
                "link_drive": "https://drive.google.com/drive/folders/1BcD9bXK5pFMPPmGADyU4mg7AhuS0MIZd?usp=drive_link"
            }
        },
        "Kelas 11": {
            "Bab 1: Kolonialisme & Perlawanan": {
                "sub_bab": ["Latar Belakang 3G", "VOC & Hindia Belanda", "Dampak Kolonialisme", "Perlawanan Daerah"],
                "rangkuman": r"""
#### 🚀 Runtuhnya Monopoli VOC
Motif 3G: Gold (Kekayaan rempah), Glory (Kejayaan menaklukkan tanah), Gospel (Menyebarkan keyakinan). VOC bangkrut karena wabah korupsi sistemik!
"""
            },
            "Bab 2: Pergerakan Nasional": {
                "sub_bab": ["Faktor Lahir", "Organisasi Awal", "Organisasi Radikal", "Sumpah Pemuda 1928", "Peran Pers"],
                "rangkuman": r"""
#### 🚀 Menulis Pena Kemerdekaan
Munculnya Budi Utomo (1908) dan Sarekat Islam mengubah perjuangan dari senjata kedaerahan menjadi strategi diplomatik lewat kaum terpelajar.
"""
            },
            "Bab 3: Pendudukan Jepang & Proklamasi": {
                "sub_bab": ["Propaganda 3A", "Kebijakan Romusha", "Perlawanan", "Rengasdengklok", "Proklamasi 1945"],
                "rangkuman": r"""
#### 🚀 Vakum Kekuasaan Tercepat
Jepang dibom atom. Kaum muda revolusioner mengamankan Soekarno ke Rengasdengklok untuk menghindari provokasi Jepang dan mendesak proklamasi kemerdekaan.
"""
            }
        },
        "Kelas 12": {
            "Bab 1: Mempertahankan Kemerdekaan": {
                "sub_bab": ["Ancaman Sekutu/NICA", "Perjuangan Fisik", "Diplomasi", "Pemberontakan Dalam Negeri"],
                "rangkuman": r"""
#### 🚀 Agresi & Gencatan Senjata
Berhadapan dengan kembalinya Belanda (NICA), Indonesia bertempur fisik luar biasa di Surabaya dan Ambarawa. Di meja diplomasi, Perjanjian Linggajati & KMB memaksa Belanda mengakui kedaulatan RI.
"""
            },
            "Bab 2: Demokrasi Liberal & Terpimpin": {
                "sub_bab": ["Kabinet Demokrasi Liberal", "Dekrit 1959 & Demokrasi Terpimpin"],
                "rangkuman": r"""
#### 🚀 Kekacauan Kabinet Cepat Ganti
Sistem Liberal membuat kabinet Indonesia jatuh bangun tiap beberapa bulan karena mosi tidak percaya. Soekarno akhirnya mengambil alih kendali lewat Dekrit Presiden 5 Juli 1959.
"""
            },
            "Bab 3: Orde Baru hingga Reformasi": {
                "sub_bab": ["Lahirnya Orde Baru", "Krisis Moneter 1998", "Masa Reformasi"],
                "rangkuman": r"""
#### 🚀 Pembangunan vs Krisis Moneter
Orde Baru melakukan pembangunan fisik masif via Repelita, namun kebebasan politik dikekang. Berakhir dengan demonstrasi mahasiswa masif akibat krisis finansial Asia 1998.
"""
            },
            "Bab 4: Indonesia & Dunia": {
                "sub_bab": ["Politik Bebas Aktif", "KAA & GNB", "Misi Garuda", "Pembentukan ASEAN"],
                "rangkuman": r"""
#### 🚀 Non-Blok Macan Asia
Indonesia memelopori Konferensi Asia Afrika (KAA) di Bandung 1955. Kita mengkampanyekan Gerakan Non-Blok, tidak ikut persekongkolan Blok Barat maupun Blok Timur.
"""
            }
        }
    },

    "Ekonomi": {
        "Kelas 10": {
            "Bab 1: Konsep Dasar Ekonomi": {
                "sub_bab": ["Kelangkaan", "Alat Pemuas", "Biaya Peluang", "Prinsip & Motif"],
                "rangkuman": r"""
#### 🚀 Biaya Kesempatan (Opportunity Cost)
Ilmu memilih karena kelangkaan. Jika kamu memilih menghabiskan uang untuk tiket hiburan dibanding makan siang, maka makan siang itulah yang disebut *Biaya Peluang* yang dikorbankan.
"""
                "link_drive": "https://drive.google.com/drive/folders/1_Qb87-AYA5fmwhoZuBOuY4Po7urY0tbT?usp=drive_link"
            },
            "Bab 2: Kegiatan & Pelaku Ekonomi": {
                "sub_bab": ["Produksi & Konsumsi", "Pelaku Ekonomi", "Circular Flow Diagram"],
                "rangkuman": r"""
#### 🚀 Siklus Uang Melingkar
Alur dari Rumah Tangga Produsen memberikan barang ke Rumah Tangga Konsumen, dan Konsumen memberikan faktor produksi (Tenaga Kerja) ke Pabrik untuk digaji.
"""
                "link_drive": "https://drive.google.com/drive/folders/1QF0IzTdYWClHmsmzFu-LSfpp7oYbyX6_?usp=drive_link"
            },
            "Bab 3: Pasar & Harga": {
                "sub_bab": ["Permintaan", "Penawaran", "Harga Keseimbangan", "Elastisitas", "Struktur Pasar"],
                "rangkuman": r"""
#### 🚀 Supply and Demand
Hukum Permintaan: Harga naik, warga malas beli (berbanding terbalik).
Hukum Penawaran: Harga naik, pabrik malah bersemangat memproduksi karena ingin untung besar.
"""
                "link_drive": "https://drive.google.com/drive/folders/1SyQ8HGfK59qrgWX1RR2VVkjPluYqwrVa?usp=drive_link"
            },
            "Bab 4: Lembaga Keuangan": {
                "sub_bab": ["OJK", "Perbankan", "Lembaga Non-Bank"],
                "rangkuman": r"""
#### 🚀 Para Penjaga Kestabilan Finansial
OJK lahir sebagai wasit independen yang mengawasi seluruh kegiatan asuransi, kredit, investasi, dan perbankan di Indonesia agar warga tidak tertipu investasi bodong.
"""
                "link_drive": "https://drive.google.com/drive/folders/1cUvIMzH9qt0tqr7uKb0jWnJa6DtJ92Fr?usp=drive_link"
            }
        },
        "Kelas 11": {
            "Bab 1: Pendapatan Nasional": {
                "sub_bab": ["Konsep GDP/GNP", "Metode Penghitungan", "Pendapatan Per Kapita", "Kesenjangan (Gini)"],
                "rangkuman": r"""
#### 🚀 Mengkalkulasi Kekayaan RI
GDP (Gross Domestic Product) menghitung seluruh produk barang yang dihasilkan di batas negara, tak peduli siapapun yang memproduksinya.
"""
            },
            "Bab 2: Ketenagakerjaan": {
                "sub_bab": ["Konsep Dasar", "Masalah di Indonesia", "Sistem Upah", "Pengangguran"],
                "rangkuman": r"""
#### 🚀 Mengurai Benang Kusut Pengangguran
- **Friksional:** Menganggur sementara karena menunggu transisi kerja baru.
- **Struktural:** Menganggur karena skill yang dipunya sudah digantikan kemajuan teknologi.
"""
            },
            "Bab 3: Inflasi & Kebijakan": {
                "sub_bab": ["Inflasi", "Kebijakan Moneter", "Kebijakan Fiskal"],
                "rangkuman": r"""
#### 🚀 Kebijakan Menginjak Rem Ekonomi
Saat terjadi *Inflasi Ekstrim*, pemerintah menarik uang dari peredaran warga lewat Kebijakan Fiskal (Menaikkan Pajak) atau Moneter (Menaikkan Suku Bunga Bank).
"""
            }
        },
        "Kelas 12": {
            "Bab 1: APBN dan APBD": {
                "sub_bab": ["Tujuan & Fungsi", "Sumber Pendapatan", "Pengeluaran", "Pengaruh APBN"],
                "rangkuman": r"""
#### 🚀 Brankas Pembangunan Nasional
Penerimaan terbesar negara adalah melalui sektor Pajak. Jika penerimaan negara lebih kecil dari rencana pengeluarannya, negara menerapkan sistem anggaran defisit.
"""
            },
            "Bab 2: Akuntansi Perusahaan Jasa": {
                "sub_bab": ["Karakteristik & Persamaan", "Siklus Akuntansi", "Jurnal Penyesuaian", "Laporan Keuangan", "Jurnal Penutup"],
                "rangkuman": r"""
#### 🚀 Persamaan Dasar Akuntansi
Hukum Keseimbangan Akuntansi Universal: 
$$\text{HARTA (Aset)} = \text{HUTANG (Kewajiban)} + \text{MODAL (Ekuitas)}$$
"""
            },
            "Bab 3: Akuntansi Perusahaan Dagang": {
                "sub_bab": ["Karakteristik Dagang", "Jurnal Khusus", "Buku Besar Pembantu", "Neraca Lajur"],
                "rangkuman": r"""
#### 🚀 Kalkulasi HPP Dagang
Beda dengan perusahan Jasa, perusahaan dagang memiliki siklus barang fisik. Menemukan formula *Harga Pokok Penjualan (HPP)* sangat vital untuk menghitung laba kotor.
"""
            }
        }
    },

    "Sosiologi": {
        "Kelas 10": {
            "Bab 1: Pengantar Sosiologi": {
                "sub_bab": ["Sejarah & Tokoh", "Objek Kajian", "Fungsi Sosiologi"],
                "rangkuman": r"""
#### 🚀 Kacamata Pembedah Masyarakat
Auguste Comte adalah bapak sosiologi. Ilmu Sosiologi bersifat *Non-Etis*, artinya tidak memihak baik-buruknya suatu fakta, melainkan menjelaskan fakta tersebut secara analitis.
"""
                "link_drive": "https://drive.google.com/drive/folders/16sO5HaD9xGMfyYK6dlbif3qv4_-74opM?usp=drive_link"
            },
            "Bab 2: Interaksi & Hubungan Sosial": {
                "sub_bab": ["Identitas Diri", "Tindakan Sosial", "Syarat Interaksi", "Bentuk Interaksi"],
                "rangkuman": r"""
#### 🚀 Simulasi Empati Sosial
Interaksi sosial mensyaratkan dua gerbang utama: **Kontak Sosial** (Pertemuan fisik/virtual) dan **Komunikasi** (Pertukaran makna).
"""
                "link_drive": "https://drive.google.com/drive/folders/1VNySHb740deD9LM4YcsBK5DZUKMI8FnW?usp=drive_link"
            },
            "Bab 3: Lembaga, Nilai, & Norma": {
                "sub_bab": ["Nilai & Norma", "Jenis Norma", "Lembaga Sosial"],
                "rangkuman": r"""
#### 🚀 Tembok Kendali Kelakuan Manusia
- **Folkways:** Aturan kebiasaan biasa (Cara makan/menyapa).
- **Mores:** Norma tata kelakuan luhur/moral tinggi.
- **Customs (Adat):** Adat sanksi keras bagi pelanggarnya.
"""
                "link_drive": "https://drive.google.com/drive/folders/1PERDuQW365qDfcRH22dUJI7V8MTms7_L?usp=drive_link"
            }
        },
        "Kelas 11": {
            "Bab 1: Kelompok Sosial": {
                "sub_bab": ["Pembentukan", "Jenis Kelompok", "Dinamika Kelompok"],
                "rangkuman": r"""
#### 🚀 Solidaritas vs Persaingan
Kelompok *Gemeinschaft* (Paguyuban) diikat oleh hubungan darah batin sejati alami. Kelompok *Gesellschaft* (Patembayan) sifatnya ikatan kontrak pamrih sebatas kepentingan karier profesional.
"""
            },
            "Bab 2: Permasalahan Sosial": {
                "sub_bab": ["Eksklusi Sosial", "Ketimpangan & Kemiskinan", "Kriminalitas & Korupsi"],
                "rangkuman": r"""
#### 🚀 Kesetaraan Sumber Daya
Ketimpangan sosial terjadi karena ketidaksamaan akses terhadap sumber daya yang pada puncaknya memicu *Eksklusi Sosial* (kelompok marginal disingkirkan dari masyarakat).
"""
            },
            "Bab 3: Konflik & Kekerasan": {
                "sub_bab": ["Akar Penyebab", "Konflik vs Kekerasan", "Resolusi Konflik"],
                "rangkuman": r"""
#### 🚀 Resolusi Mediasi vs Arbitrase
Di dalam sistem **Mediasi**, keputusan penengah tidak mengikat. Di dalam **Arbitrase**, keputusan pihak ketiga bersifat mutlak dan harus ditaati secara hukum!
"""
            }
        },
        "Kelas 12": {
            "Bab 1: Perubahan Sosial": {
                "sub_bab": ["Teori Perubahan", "Faktor Pendorong", "Dampak Modernisasi"],
                "rangkuman": r"""
#### 🚀 Pergeseran Lempeng Budaya
- **Cultural Lag (Gegar Budaya):** Warga sudah memiliki teknologi canggih, namun mentalitas pemanfaatannya belum siap (gagap budaya).
"""
            },
            "Bab 2: Globalisasi & Digitalisasi": {
                "sub_bab": ["Konsep Globalisasi", "Tantangan Konsumerisme", "Komunitas Lokal"],
                "rangkuman": r"""
#### 🚀 Gelombang Pemudaran Batas Negara
Masyarakat ditantang oleh **Glokalisasi**, yaitu mengemas unsur tradisional lokal ke dalam standar promosi global dunia.
"""
            },
            "Bab 3: Pemberdayaan Komunitas": {
                "sub_bab": ["Kearifan Lokal", "Strategi Pemberdayaan", "Aksi Sosial"],
                "rangkuman": r"""
#### 🚀 Kemandirian Anti-Eksploitasi
Pemberdayaan sosial harus membekali warga dengan *Skill* dan *Akses Mandiri* agar mereka tidak bergantung pada sekadar bantuan dana sementara.
"""
            }
        }
    }
}
