# ==========================================
# FILE: database_rangkuman.py
# FUNGSI: Database Rangkuman Materi Premium & Super Lengkap (Update V2)
# ==========================================

DATA_MATERI = {
    "Matematika": {
        "Kelas 10": {
            "Eksponen dan Logaritma": {
                "sub_bab": ["Konsep Dasar Eksponen", "Sifat-sifat Logaritma", "Aplikasi HOTS"],
                "rangkuman": """
#### 🚀 Rahasia Eksponen & Logaritma
Eksponen adalah bentuk perkalian berulang, sedangkan Logaritma adalah **kebalikan (invers)** dari eksponen. Jika kamu menguasai satu, kamu otomatis menguasai yang lainnya!

#### 🔑 Sifat-Sifat Dewa Eksponen
- **Perkalian:** $a^m \cdot a^n = a^{m+n}$ *(Pangkat ditambah)*
- **Pembagian:** $\\frac{a^m}{a^n} = a^{m-n}$ *(Pangkat dikurang)*
- **Pangkat Dipangkatkan:** $(a^m)^n = a^{m \cdot n}$ *(Pangkat dikali)*
- **Pangkat Negatif:** $a^{-n} = \\frac{1}{a^n}$

#### 🎯 Sifat-Sifat Dewa Logaritma
- **Penjumlahan Log:** $^a\\!\\log x + ^a\\!\\log y = ^a\\!\\log(x \cdot y)$
- **Pengurangan Log:** $^a\\!\\log x - ^a\\!\\log y = ^a\\!\\log\\left(\\frac{x}{y}\\right)$
- **Pangkat ke Depan:** $^a\\!\\log x^n = n \cdot ^a\\!\\log x$

> **🧠 KONSEP HOTS UTBK:**
> Soal UTBK jarang menanyakan hitungan langsung! Biasanya soal dihubungkan dengan **Pertumbuhan Eksponensial** (seperti pelipatgandaan bakteri, virus, atau bunga bank). 
> **Rumus Sakti Pertumbuhan:** $P_n = P_0(1 + r)^n$
                """
            },
            "Persamaan Linear": {
                "sub_bab": ["Sistem Persamaan Linear Satu Variabel", "Sistem Persamaan Linear Dua Variabel"],
                "rangkuman": """
#### 🚀 Menaklukkan Persamaan Linear
Persamaan linear adalah persamaan yang variabelnya memiliki **pangkat tertinggi satu** (grafiknya jika digambar pasti berupa garis lurus tegak atau miring).

#### 🔑 Langkah Cepat Substitusi & Eliminasi
Jika menemui Sistem Persamaan Linear Dua Variabel (SPLDV), lakukan langkah ini:
1. **Eliminasi (Gaya Hancur):** Samakan koefisien (angka di depan huruf) dari salah satu variabel, lalu kurangkan atau tambahkan agar variabel tersebut hancur/hilang!
2. **Substitusi (Gaya Susup):** Masukkan nilai variabel yang sudah ketemu ke dalam salah satu persamaan awal untuk mencari variabel pasangannya.

> **💡 TRIK STUDI KASUS BISNIS:**
> Seringkali persamaan linear digunakan untuk mencari **Titik Impas (Break-Even Point)**. Di mana biaya pengeluaran (Modal) persis menyentuh garis Penghasilan (Laba).
                """
            }
        }
    },
    "Fisika": {
        "Kelas 10": {
            "Kinematika Partikel": {
                "sub_bab": ["Gerak Lurus Beraturan (GLB)", "Gerak Lurus Berubah Beraturan (GLBB)"],
                "rangkuman": """
#### 🚀 Apa itu Kinematika Partikel?
Kinematika adalah ilmu murni yang mempelajari gerak benda tanpa memedulikan **penyebab** benda itu bergerak (gaya). Di bab ini, otak kita hanya fokus pada 3 hal: **Kecepatan, Jarak, dan Waktu!**

#### 🔑 Rumus Sakti GLB & GLBB
**1. Gerak Lurus Beraturan (GLB)**
Terjadi saat **Kecepatan Konstan** (Tidak ada injakan pedal gas atau rem / percepatan nol).
$$s = v \cdot t$$

**2. Gerak Lurus Berubah Beraturan (GLBB)**
Terjadi saat kecepatan berubah karena ada **Percepatan ($a$) yang konstan**. Hafalkan 3 rumus dewa ini:
1. $$v_t = v_0 + a \cdot t$$
2. $$s = v_0 \cdot t + \\frac{1}{2} \cdot a \cdot t^2$$
3. $$v_t^2 = v_0^2 + 2 \cdot a \cdot s$$

> **💡 TRIK ANALISIS HOTS (Gaya Cepat):**
> Jika sebuah benda diceritakan **"direm hingga berhenti total"**, itu adalah kata sandi rahasia bahwa kecepatan akhir ($v_t = 0$) dan nilai $a$ pasti **negatif** (perlambatan)! Selalu baca dengan teliti!
                """
            },
            "Hakikat Fisika dan Besaran": {
                "sub_bab": ["Besaran Pokok", "Analisis Dimensi"],
                "rangkuman": """
#### 🚀 Besaran dan Dimensi
Dimensi membuktikan apakah sebuah rumus fisika itu nyata atau hoaks. Semua besaran turunan terlahir dari 7 Besaran Pokok.

#### 🔑 7 Besaran Pokok SI (Jiwa Kuat)
Ingat jembatan keledai **"JIWA SMP"**:
- **J**umlah zat (Mol) $\\rightarrow [N]$
- **I**ntensitas cahaya (Candela) $\\rightarrow [J]$
- **W**aktu (Sekon) $\\rightarrow [T]$
- **A**rus listrik (Ampere) $\\rightarrow [I]$
- **S**uhu (Kelvin) $\\rightarrow [\\theta]$
- **M**assa (Kilogram) $\\rightarrow [M]$
- **P**anjang (Meter) $\\rightarrow [L]$

> **🧠 TRIK UTBK DIMENSI:**
> Rumus yang memiliki penjumlahan atau pengurangan (seperti $A = B + C$) wajib memiliki **Dimensi yang SAMA** di setiap sukunya! Kita tidak mungkin menambahkan dimensi Panjang dengan dimensi Waktu.
                """
            },
            "Momentum dan Impuls": {
                "sub_bab": ["Konsep Momentum", "Tumbukan & Impuls"],
                "rangkuman": """
#### 🚀 Momentum & Impuls: Rahasia Tabrakan
Kenapa menabrak tembok terasa lebih sakit daripada menabrak kasur busa? Jawabannya ada pada Impuls! Momentum adalah tingkat kesukaran menghentikan benda bergerak, sedangkan Impuls adalah gaya kejut yang bekerja dalam waktu sangat singkat.

#### 🔑 Persamaan Utama
- **Momentum ($p$):** Ukuran "gaya dorong" benda.
  $$p = m \cdot v$$
- **Impuls ($I$):** Gaya dikali selang waktu.
  $$I = F \cdot \Delta t$$
- **Teorema Impuls-Momentum:** Impuls selalu menyebabkan perubahan momentum!
  $$I = \Delta p = m(v_t - v_0)$$

> **🧠 ANALISIS HOTS:**
> Pada desain sabuk pengaman dan *airbag* mobil, tujuannya adalah **memperbesar selang waktu sentuh ($\Delta t$)**. Jika $\Delta t$ membesar saat terjadi perubahan momentum yang sama, maka **Gaya hancur ($F$) akan mengecil**, sehingga pengemudi selamat!
                """
            }
        }
    },
    "Geografi": {
        "Kelas 10": {
            "Dinamika Litosfer": {
                "sub_bab": ["Tenaga Endogen", "Tenaga Eksogen", "Mitigasi Bencana Bencana"],
                "rangkuman": """
#### 🚀 Membedah Wajah Bumi (Litosfer)
Bumi kita tidaklah diam. Kulit bumi (Litosfer) terus menerus dipahat oleh dua "pemahat" raksasa: Tenaga dari dalam bumi (Endogen) dan dari luar bumi (Eksogen). Bab ini adalah menu wajib untuk Penilaian Akhir Semester (PAS)!

#### 🔑 Dua Kekuatan Raksasa
1. **Tenaga Endogen (Membangun):** - **Tektonisme:** Pergerakan lempeng (Patahan & Lipatan).
   - **Vulkanisme:** Aktivitas magma naik ke permukaan bumi.
   - **Seisme:** Getaran/Gempa bumi akibat pelepasan energi tektonik atau vulkanik.
2. **Tenaga Eksogen (Merusak/Mengikis):**
   - **Pelapukan:** Hancurnya batuan karena suhu/cuaca.
   - **Erosi & Sedimentasi:** Pengikisan dan pengendapan oleh air, angin, atau gletser.

> **💡 FOKUS PAS & UJIAN:**
> Selalu ingat bahwa letak Indonesia di jalur **Ring of Fire (Cincin Api Pasifik)** membuat tanah kita sangat subur (abu vulkanik) namun berisiko tinggi terhadap gempa megathrust. Mitigasi bencana pragempa, saat gempa, dan pascagempa adalah soal favorit para pembuat ujian!
                """
            }
        }
    },
    "Ekonomi": {
        "Kelas 10": {
            "Konsep Manajemen & Bisnis Digital": {
                "sub_bab": ["Fungsi Manajemen", "Pemasaran Digital & Pertumbuhan Eksponensial"],
                "rangkuman": """
#### 🚀 Pengantar Bisnis di Era Digital
Di era industri 4.0, bisnis tidak lagi mengandalkan penyebaran brosur di pinggir jalan. Manajemen digital menggunakan strategi *Growth Hacking* untuk mendapatkan pengguna secara masif dan instan.

#### 🔑 Konsep Pertumbuhan Eksponensial dalam Bisnis
- **Viral Coefficient (K-Factor):** Jika 1 pengguna merekomendasikan aplikasi ke 2 pengguna baru, aplikasi tersebut akan meledak secara viral (Inilah algoritma asli TikTok dan Gojek di awal rilis).
- **Customer Acquisition Cost (CAC):** Biaya riil yang dikeluarkan oleh perusahaan untuk mendatangkan 1 pembeli baru. Jika CAC lebih besar dari keuntungan per barang, bisnis akan bangkrut.
- **Retensi (Retention):** Percuma mendapat 1000 pelanggan hari ini jika besok 999 orang kabur. Retensi adalah kunci bisnis bertahan lama.

> **💡 ANALISIS KURVA BISNIS (HOTS):**
> Jika kamu melihat grafik penjualan perusahaan melengkung tajam menembus langit, itu disebut **Kurva Eksponensial**. Pemasaran digital yang brilian mampu mengubah kurva linier (naik lambat) menjadi kurva eksponensial.
                """
            }
        }
    },
    "Kimia": {
        "Kelas 11": {
            "Kinetika Kimia": {
                "sub_bab": ["Faktor-Faktor Laju Reaksi", "Orde Reaksi"],
                "rangkuman": """
#### 🚀 Kinetika Kimia & Laju Reaksi
Ilmu yang membahas seberapa cepat suatu reaktan (bahan baku) habis terbakar, atau seberapa cepat produk (hasil) terbentuk. 

#### 🔑 4 Faktor Utama Penentu Kecepatan Reaksi
1. **Suhu (Temperatur):** Semakin panas, energi kinetik partikel semakin brutal. Partikel makin sering tabrakan!
   *Rumus Cepat Kenaikan Suhu:* $$v_2 = v_1 \cdot n^{\\frac{\Delta T}{x}}$$ 
   *(n = kelipatan laju, $\Delta T$ = selisih suhu, x = rentang kenaikan suhu)*
2. **Konsentrasi:** Semakin kental/pekat sebuah larutan, semakin padat jumlah partikelnya. Jalanan yang padat pasti memicu lebih banyak tabrakan!
3. **Luas Permukaan (Bidang Sentuh):** Gula pasir (serbuk) akan larut **jauh lebih cepat** dibanding gula batu (bongkahan besar). Semakin halus ukurannya, semakin cepat bereaksi.
4. **Katalisator:** Sang mak comblang reaksi! Katalis menurunkan **Energi Aktivasi ($E_a$)** agar reaksi cepat meledak tanpa ikut habis di akhir proses.

> **🧠 KUNCI SOAL LAJU REAKSI:**
> Orde reaksi hanya bisa ditentukan melalui eksperimen, **TIDAK BISA** langsung dilihat dari angka koefisien di persamaan reaksi.
                """
            }
        },
        "Kelas 10": {
            "Struktur Atom": {
                "sub_bab": ["Partikel Subatomik", "Konfigurasi Elektron"],
                "rangkuman": """
#### 🚀 Mengintip Isi Inti Atom
Atom bukanlah bola pejal biasa. Di dalamnya terdapat semesta mikro yang bergerak tiada henti!

#### 🔑 Tiga Serangkai Subatomik
1. **Proton (+):** Berada santai di dalam inti atom (Nukleus). Menentukan *Nomor Atom* suatu unsur.
2. **Neutron (Netral):** Pasangan proton di dalam inti atom. Menjaga agar proton-proton tidak saling tolak-menolak.
3. **Elektron (-):** Bintang lapangan yang terus berputar mengelilingi inti atom dalam kecepatan cahaya pada jalur orbitnya (kulit elektron). Sangat mudah lepas dan berpindah!

> **💡 RUMUS NOTASI UNSUR:**
> **Nomor Massa (A)** = Jumlah Proton + Jumlah Neutron.
> **Isotop** = Unsur kembar yang memiliki Nomor Atom (Proton) SAMA, tapi Nomor Massa beda (karena beda neutron).
                """
            },
            "Persamaan Reaksi Kimia": {
                "sub_bab": ["Hukum Kekekalan Massa", "Penyetaraan Reaksi"],
                "rangkuman": """
#### 🚀 Seni Menyetarakan Reaksi Kimia
Hukum Kekekalan Massa (Lavoisier) menyatakan bahwa massa zat sebelum dan sesudah reaksi adalah **SAMA**. Artinya, jumlah atom di ruas kiri (Reaktan) harus persis sama dengan jumlah atom di ruas kanan (Produk).

#### 🔑 Trik Cepat Menyetarakan Reaksi
1. Jangan pernah mengubah angka indeks (angka kecil di belakang unsur, contoh: $O_2$), karena itu akan mengubah jenis senyawanya!
2. Kamu hanya boleh mengotak-atik **Koefisien** (angka besar di paling depan senyawa).
3. **Gaya Aljabar (Untuk Soal Sulit):** Jika reaksinya panjang (seperti pembakaran hidrokarbon), gunakan variabel huruf $a, b, c, d$ pada setiap molekul, lalu buat persamaan matematikanya!

> **🧠 TIPS UJIAN (Balancing):**
> Setarakan atom berurutan menggunakan metode **K-A-H-O**:
> **K**ation (Logam/Kiri), **A**nion (Non-Logam/Kanan), lalu urus **H**idrogen, dan terakhir selesaikan **O**ksigen. Jika Oksigen sudah setara di akhir, berarti reaksimu 100% benar!
                """
            }
        }
    },
    "Seni Budaya": {
        "Kelas 12": {
            "Seni Teater": {
                "sub_bab": ["Rancangan Naskah Drama", "Penyutradaraan"],
                "rangkuman": """
#### 🚀 Seni Teater: Merancang Mahakarya Naskah Drama
Teater adalah perpaduan tertinggi antara seni sastra (naskah), seni musik (scoring), seni rupa (tata panggung), dan seni peran (akting).

#### 🔑 Teater Klasik Tradisional VS Drama Musikal Modern (Gen Z)
- **Teater Tradisional (Contoh: Ketoprak, Wayang Wong, Ludruk):**
  Sangat terikat pada pakem/aturan baku. Sering menggunakan bahasa krama (halus), iringan wajib gamelan/karawitan, dan cerita mayoritas berpusat pada kerajaan/legenda mitos (Istana Sentris).
- **Drama Musikal Modern (Contoh: Laskar Pelangi Musikal, Teater Remaja Sekolah):**
  Bebas, fleksibel, improvisasi tingkat tinggi. Mengangkat isu mental dan sosial masa kini, menggunakan diksi/slang bahasa yang sangat kasual, serta menggunakan transisi tata cahaya (lighting) dan musik pop/indie untuk merepresentasikan perasaan tokohnya.

> **🧠 INTI PEMBUATAN NASKAH HOTS:**
> Naskah teater remaja yang sukses adalah naskah yang memiliki *Relatability* (sangat relevan dengan keseharian penonton). Penonton modern tidak lagi mencari keindahan bahasa puisi yang sulit dimengerti, tetapi mencari pantulan diri mereka sendiri di atas panggung!
                """
            }
        }
    },
    "Prakarya dan Kewirausahaan": {
        "Kelas 11": {
            "Pengolahan Makanan Khas Daerah": {
                "sub_bab": ["Modifikasi Resep (LK-10)", "Standarisasi SOP Komersial", "Strategi Pemasaran"],
                "rangkuman": """
#### 🚀 Inovasi Kuliner Daerah ke Ranah Profesional
Memasak di rumah berbeda dengan memasak untuk industri komersial. Mengubah makanan tradisional (seperti rendang, rawon, atau soto) menjadi produk modern yang bernilai jual tinggi membutuhkan inovasi dan laporan modular berstandar industri.

#### 🔑 Elemen Laporan Modular (Standar LK-10)
Sebuah rancangan pengolahan makanan tidak sekadar resep, melainkan memuat:
1. **Ide & Justifikasi Modifikasi:** Mengapa makanan ini diubah? (Misal: Modifikasi kemasan *vacuum* agar rawon tahan 3 bulan tanpa pengawet).
2. **Standard Operating Procedure (SOP):** Langkah baku yang harus diikuti agar jika koki diganti, rasanya tetap 100% sama persis. Mulai dari takaran gramasi bumbu, suhu api, hingga durasi menit pemanasan.
3. **HPP (Harga Pokok Penjualan):** Hitungan matematis total biaya bahan baku dibagi jumlah porsi yang dihasilkan.

> **💡 TRIK BISNIS KULINER MODERN:**
> Inovasi makanan daerah masa kini sangat berfokus pada **Modifikasi Kemasan (Packaging)** dan **Bentuk Presentasi**. Rasa otentik dipertahankan, namun visualnya disesuaikan untuk menarik perhatian target pasar anak muda di platform digital.
                """
            }
        }
    }
}
