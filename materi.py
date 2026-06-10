# --- DATABASE SILABUS KURIKULUM MERDEKA ---
# Struktur: Pelajaran -> Kelas -> Bab -> {sub_bab, rangkuman}

DATA_MATERI = {
    "Matematika": {
        "Kelas 10": {
            "Bab 1: Eksponen dan Logaritma": {
                "sub_bab": ["Sifat Eksponen", "Fungsi Eksponen", "Bentuk Akar", "Sifat Logaritma", "Penyelesaian Masalah"],
                "rangkuman": "• **Eksponen & Logaritma**: Mempelajari sifat pangkat, pertumbuhan/peluruhan, merasionalkan penyebut, dan operasi logaritma dasar."
            },
            "Bab 2: Barisan dan Deret": {
                "sub_bab": ["Barisan Aritmatika", "Barisan Geometri", "Deret Tak Hingga", "Aplikasi (Bunga, Anuitas)"],
                "rangkuman": "• **Barisan & Deret**: Pola bilangan dengan beda tetap (Aritmatika) atau rasio tetap (Geometri), beserta aplikasinya pada keuangan."
            },
            "Bab 3: Vektor dan Operasinya": {
                "sub_bab": ["Notasi Vektor", "Vektor di R2 dan R3", "Operasi Vektor", "Cross & Dot Product"],
                "rangkuman": "• **Vektor**: Besaran yang memiliki nilai dan arah. Beroperasi di dimensi 2 dan dimensi 3."
            },
            "Bab 4: Trigonometri": {
                "sub_bab": ["Penamaan Sisi", "Perbandingan Trigonometri", "Sudut Berelasi", "Konteks Nyata"],
                "rangkuman": "• **Trigonometri**: Hubungan sudut dan sisi segitiga siku-siku (Sin, Cos, Tan, Csc, Sec, Cot)."
            },
            "Bab 5: Sistem Persamaan Linear": {
                "sub_bab": ["SPLDV", "SPLTV", "SPtLDV", "Model Matematika"],
                "rangkuman": "• **SPL**: Menyelesaikan masalah dengan dua variabel (SPLDV) atau tiga variabel (SPLTV) serta pertidaksamaannya."
            },
            "Bab 6: Fungsi Kuadrat": {
                "sub_bab": ["Grafik Fungsi", "Mengonstruksi Fungsi", "Nilai Maks/Min", "Aplikasi"],
                "rangkuman": "• **Fungsi Kuadrat**: Kurva berbentuk parabola dengan persamaan karakteristik yang memiliki titik puncak."
            },
            "Bab 7: Statistika": {
                "sub_bab": ["Distribusi Frekuensi", "Histogram/Ogive", "Pemusatan Data", "Letak Data", "Penyebaran Data"],
                "rangkuman": "• **Statistika**: Mengolah data melalui Mean, Median, Modus, Kuartil, hingga Simpangan Baku."
            },
            "Bab 8: Peluang": {
                "sub_bab": ["Ruang Sampel", "Peluang Kejadian", "Frekuensi Harapan", "Saling Lepas/Bebas"],
                "rangkuman": "• **Peluang**: Kemungkinan terjadinya suatu kejadian dari sebuah ruang sampel."
            }
        },
        "Kelas 11": {
            "Bab 1: Komposisi & Invers Fungsi": {
                "sub_bab": ["Domain/Range", "Aljabar Fungsi", "Fungsi Komposisi", "Fungsi Invers", "Invers Komposisi"],
                "rangkuman": "• **Fungsi**: Menggabungkan dua fungsi (Komposisi) dan membalik arah pemetaan fungsi (Invers)."
            },
            "Bab 2: Lingkaran": {
                "sub_bab": ["Busur Lingkaran", "Sudut Pusat & Keliling", "Tali Busur & Garis Singgung", "Persamaan Lingkaran"],
                "rangkuman": "• **Lingkaran**: Mempelajari unsur lingkaran dan persamaannya dengan pusat (0,0) maupun (a,b)."
            },
            "Bab 3: Matriks": {
                "sub_bab": ["Ordo & Notasi", "Jenis & Transpose", "Operasi Matriks", "Determinan & Invers", "Penyelesaian SPL"],
                "rangkuman": "• **Matriks**: Susunan bilangan dalam baris dan kolom untuk menyelesaikan persamaan linear kompleks."
            },
            "Bab 4: Transformasi Geometri": {
                "sub_bab": ["Translasi", "Refleksi", "Rotasi", "Dilatasi", "Komposisi Transformasi"],
                "rangkuman": "• **Transformasi**: Pergeseran, pencerminan, perputaran, dan perkalian ukuran pada bidang koordinat."
            }
        },
        "Kelas 12": {
            "Bab 1: Geometri Ruang (Dimensi Tiga)": {
                "sub_bab": ["Jarak Antar Titik", "Jarak Titik ke Garis", "Jarak Titik ke Bidang", "Sudut Ruang"],
                "rangkuman": "• **Dimensi Tiga**: Menganalisis jarak dan sudut pada bangun ruang seperti kubus, balok, dan limas."
            },
            "Bab 2: Limit Fungsi Aljabar & Trigonometri": {
                "sub_bab": ["Konsep Limit", "Sifat Limit", "Limit Tak Hingga", "Limit Trigonometri"],
                "rangkuman": "• **Limit**: Nilai hampiran suatu fungsi saat mendekati titik tertentu."
            },
            "Bab 3: Turunan Fungsi (Diferensial)": {
                "sub_bab": ["Konsep Turunan", "Rumus Turunan", "Sifat Turunan", "Aplikasi Turunan"],
                "rangkuman": "• **Turunan**: Laju perubahan suatu fungsi. Diaplikasikan pada garis singgung dan titik maksimum/minimum."
            },
            "Bab 4: Integral (Antiturunan)": {
                "sub_bab": ["Integral Tak Tentu", "Sifat Integral", "Integral Tentu", "Teknik Pengintegralan", "Luas Kurva"],
                "rangkuman": "• **Integral**: Kebalikan dari turunan. Digunakan untuk menghitung luasan di bawah kurva."
            }
        }
    },
    "Fisika": {
        "Kelas 10": {
            "Bab 1: Pengukuran Ilmiah": {
                "sub_bab": ["Alat Ukur", "Besaran & Dimensi", "Angka Penting", "Ketidakpastian"],
                "rangkuman": "• **Pengukuran**: Kaidah menggunakan alat ukur presisi dengan memperhatikan angka penting dan ketidakpastian."
            },
            "Bab 2: Energi Terbarukan": {
                "sub_bab": ["Bentuk Energi", "Hukum Kekekalan Energi", "Sumber Fosil vs Terbarukan", "Dampak Lingkungan"],
                "rangkuman": "• **Energi**: Memahami transisi dari energi fosil menuju energi hijau (angin, surya, air)."
            }
        },
        "Kelas 11": {
            "Bab 1: Kinematika Gerak": {
                "sub_bab": ["GLB & GLBB", "Gerak Vertikal", "Gerak Parabola", "Gerak Melingkar"],
                "rangkuman": "• **Kinematika**: Analisis murni lintasan gerak benda tanpa memperhitungkan penyebabnya."
            },
            "Bab 2: Dinamika Gerak (Hukum Newton)": {
                "sub_bab": ["Hukum Newton", "Gaya Gesek/Normal", "Bidang Miring & Katrol", "Gaya Sentripetal"],
                "rangkuman": "• **Dinamika**: Mempelajari gaya yang menyebabkan benda diam atau bergerak."
            },
            "Bab 3: Statika dan Dinamika Rotasi": {
                "sub_bab": ["Torsi & Inersia", "Kesetimbangan", "Titik Berat", "Kekekalan Momentum Sudut"],
                "rangkuman": "• **Rotasi**: Ilmu tentang benda yang berputar dan syarat kesetimbangannya."
            },
            "Bab 4: Fluida": {
                "sub_bab": ["Fluida Statis", "Fluida Dinamis"],
                "rangkuman": "• **Fluida**: Zat cair/gas dalam keadaan diam (Hukum Archimedes, Pascal) maupun bergerak (Hukum Bernoulli)."
            },
            "Bab 5: Gelombang, Cahaya, dan Bunyi": {
                "sub_bab": ["Karakteristik Gelombang", "Stasioner & Berjalan", "Gelombang Cahaya", "Gelombang Bunyi"],
                "rangkuman": "• **Gelombang**: Rambatan energi melalui medium atau ruang hampa. Termasuk efek Doppler pada bunyi."
            }
        },
        "Kelas 12": {
            "Bab 1: Termodinamika": {
                "sub_bab": ["Suhu & Kalor", "Teori Kinetik Gas", "Hukum Termodinamika", "Proses & Siklus Carnot"],
                "rangkuman": "• **Termodinamika**: Usaha yang dihasilkan dari pertukaran kalor dalam suatu sistem gas."
            },
            "Bab 2: Listrik Statis & Dinamis": {
                "sub_bab": ["Hukum Coulomb & Kapasitor", "Hukum Ohm & Kirchhoff", "Rangkaian Seri-Paralel"],
                "rangkuman": "• **Listrik**: Interaksi muatan diam (Statis) dan muatan mengalir (Dinamis/DC)."
            },
            "Bab 3: Kemagnetan & Induksi": {
                "sub_bab": ["Medan Magnet", "Gaya Lorentz", "Induksi Faraday", "Transformator & AC"],
                "rangkuman": "• **Magnet**: Timbulnya gaya magnet dari arus listrik, dan sebaliknya (Arus Bolak-Balik/AC)."
            },
            "Bab 4: Fisika Modern & Kuantum": {
                "sub_bab": ["Relativitas Khusus", "Radiasi Benda Hitam", "Efek Fotolistrik", "Fisika Inti"],
                "rangkuman": "• **Fisika Modern**: Teori relativitas Einstein dan fenomena di tingkat atom (radioaktivitas)."
            }
        }
    },
    "Kimia": {
        "Kelas 10": {
            "Bab 1: Kimia Hijau": {
                "sub_bab": ["12 Prinsip Kimia Hijau", "Isu Lingkungan", "Proses Ramah Lingkungan"],
                "rangkuman": "• **Kimia Hijau**: Praktik kimia untuk mencegah polusi dan menciptakan produk ramah lingkungan."
            },
            "Bab 2: Struktur Atom & Hukum Dasar": {
                "sub_bab": ["Model Atom", "Partikel Penyusun", "Isotop/Isobar", "Hukum Dasar Kimia"],
                "rangkuman": "• **Atom**: Partikel terkecil dan hukum-hukum kekekalan serta perbandingan tetap (Lavoisier, Proust)."
            }
        },
        "Kelas 11": {
            "Bab 1: Struktur Atom Modern": {
                "sub_bab": ["Bilangan Kuantum", "Konfigurasi Elektron", "Sifat Periodik"],
                "rangkuman": "• **Atom Modern**: Memahami posisi elektron berdasarkan orbital mekanika kuantum."
            },
            "Bab 2: Ikatan Kimia": {
                "sub_bab": ["Kestabilan Unsur", "Ikatan Ion, Kovalen, Logam", "Bentuk Molekul VSEPR", "Gaya Antarmolekul"],
                "rangkuman": "• **Ikatan**: Proses atom-atom bergabung membentuk senyawa agar stabil (Oktet/Duplet)."
            },
            "Bab 3: Stoikiometri": {
                "sub_bab": ["Konsep Mol", "Rumus Empiris/Molekul", "Kadar Zat", "Pereaksi Pembatas"],
                "rangkuman": "• **Stoikiometri**: Perhitungan matematis kimia terkait massa, volume, dan jumlah partikel."
            },
            "Bab 4: Termokimia": {
                "sub_bab": ["Sistem & Lingkungan", "Eksoterm/Endoterm", "Entalpi", "Penentuan Entalpi"],
                "rangkuman": "• **Termokimia**: Analisis perpindahan energi (kalor) yang menyertai reaksi kimia."
            },
            "Bab 5: Laju Reaksi": {
                "sub_bab": ["Konsep Laju Reaksi", "Teori Tumbukan", "Faktor Pengaruh", "Orde Reaksi"],
                "rangkuman": "• **Laju Reaksi**: Seberapa cepat reaktan habis dan produk terbentuk berdasarkan berbagai faktor."
            }
        },
        "Kelas 12": {
            "Bab 1: Kesetimbangan Kimia": {
                "sub_bab": ["Reaksi Reversibel", "Tetapan Kesetimbangan", "Pergeseran Le Chatelier", "Aplikasi Industri"],
                "rangkuman": "• **Kesetimbangan**: Kondisi di mana laju reaksi ke kanan dan kiri sama besar."
            },
            "Bab 2: Asam-Basa & Larutan": {
                "sub_bab": ["Teori Asam Basa", "Skala pH", "Larutan Penyangga", "Hidrolisis Garam", "Kelarutan (Ksp)"],
                "rangkuman": "• **Asam-Basa**: Sifat larutan, sistem pertahanan pH (Buffer), dan kelarutan zat."
            },
            "Bab 3: Elektrokimia": {
                "sub_bab": ["Reaksi Redoks", "Sel Volta", "Korosi", "Sel Elektrolisis"],
                "rangkuman": "• **Elektrokimia**: Konversi energi kimia menjadi listrik (Baterai) atau sebaliknya (Penyepuhan)."
            },
            "Bab 4: Kimia Organik": {
                "sub_bab": ["Kekhasan Karbon", "Alkana/Alkena/Alkuna", "Gugus Fungsi", "Polimer & Makromolekul"],
                "rangkuman": "• **Kimia Organik**: Mempelajari rantai senyawa karbon pembentuk kehidupan dan material polimer."
            }
        }
    },
    "Biologi": {
        "Kelas 10": {
            "Bab 1: Keanekaragaman Hayati": {
                "sub_bab": ["Tingkat Gen/Jenis", "Flora Fauna RI", "Pelestarian", "Klasifikasi"],
                "rangkuman": "• **Kehati**: Mempelajari ragam makhluk hidup, garis batas biogeografi, dan upaya konservasi."
            },
            "Bab 2: Virus": {
                "sub_bab": ["Struktur Virus", "Siklus Litik/Lisogenik", "Peranan Virus", "Pencegahan"],
                "rangkuman": "• **Virus**: Entitas aseluler yang mereplikasi diri dalam sel inang dan peranannya dalam medis."
            },
            "Bab 3: Lingkungan & Ekosistem": {
                "sub_bab": ["Komponen Ekosistem", "Jaring Makanan", "Daur Biogeokimia", "Pencemaran"],
                "rangkuman": "• **Ekosistem**: Hubungan timbal balik biotik dan abiotik, siklus alam, serta dampak pencemaran."
            }
        },
        "Kelas 11": {
            "Bab 1: Sel": {
                "sub_bab": ["Komponen Kimiawi", "Organel Sel", "Sel Hewan vs Tumbuhan", "Transpor Membran"],
                "rangkuman": "• **Sel**: Unit terkecil kehidupan, fungsi organel, dan mekanisme perpindahan zat."
            },
            "Bab 2: Struktur & Fungsi Jaringan": {
                "sub_bab": ["Jaringan Tumbuhan", "Jaringan Hewan"],
                "rangkuman": "• **Jaringan**: Kumpulan sel khusus. Meliputi pelindung, penyokong, dan pengangkut (Xilem/Floem)."
            },
            "Bab 3: Sistem Organ (Bagian 1)": {
                "sub_bab": ["Sistem Gerak", "Sistem Sirkulasi", "Sistem Pencernaan"],
                "rangkuman": "• **Organ I**: Anatomi tulang, jantung & darah, serta lambung hingga usus."
            },
            "Bab 4: Sistem Organ (Bagian 2)": {
                "sub_bab": ["Sistem Pernapasan", "Sistem Ekskresi", "Sistem Koordinasi", "Sistem Reproduksi"],
                "rangkuman": "• **Organ II**: Sistem pengeluaran karbon dioksida, urine, sinyal saraf/hormon, dan reproduksi manusia."
            }
        },
        "Kelas 12": {
            "Bab 1: Pertumbuhan & Perkembangan": {
                "sub_bab": ["Konsep Dasar", "Perkecambahan", "Faktor Internal (Hormon)", "Faktor Eksternal"],
                "rangkuman": "• **Pertumbuhan**: Proses irreversibel tanaman dan faktor yang memicu pemanjangan sel."
            },
            "Bab 2: Metabolisme Sel": {
                "sub_bab": ["Enzim", "Katabolisme (Respirasi)", "Anabolisme (Fotosintesis)"],
                "rangkuman": "• **Metabolisme**: Reaksi kimia sel (Glikolisis, Siklus Krebs) dan pembentukan makanan oleh klorofil."
            },
            "Bab 3: Genetika & Hereditas": {
                "sub_bab": ["DNA & RNA", "Sintesis Protein", "Pembelahan Sel", "Hukum Mendel", "Penyimpangan Mendel", "Hereditas Manusia"],
                "rangkuman": "• **Genetika**: Pewarisan sifat dari induk ke keturunan, struktur DNA, dan kelainan genetik bawaan."
            },
            "Bab 4: Evolusi & Bioteknologi": {
                "sub_bab": ["Teori Evolusi", "Bioteknologi Konvensional", "Bioteknologi Modern"],
                "rangkuman": "• **Evolusi**: Perubahan perlahan sepanjang masa dan rekayasa genetika (kloning, kultur jaringan)."
            }
        }
    },
    "Sejarah": {
        "Kelas 10": {
            "Bab 1: Pengantar Ilmu Sejarah": {
                "sub_bab": ["Syarat & Manfaat", "Ruang & Waktu", "Sinkronik/Diakronik", "Sumber Sejarah", "Tahapan Penelitian"],
                "rangkuman": "• **Ilmu Sejarah**: Metode berpikir historis dan cara melakukan penelitian menggunakan heuristik & historiografi."
            },
            "Bab 2: Jalur Rempah & Hindu-Buddha": {
                "sub_bab": ["Teori Masuknya", "Kerajaan Besar", "Sosial-Budaya", "Jalur Rempah"],
                "rangkuman": "• **Hindu-Buddha**: Masa kejayaan Nusantara dari Kutai hingga Majapahit dalam jaringan perdagangan dunia."
            },
            "Bab 3: Islamisasi di Nusantara": {
                "sub_bab": ["Teori Masuk", "Saluran Islamisasi", "Kerajaan Islam", "Akulturasi Budaya"],
                "rangkuman": "• **Kerajaan Islam**: Penyebaran agama lewat perdagangan dan munculnya kesultanan seperti Demak dan Samudera Pasai."
            }
        },
        "Kelas 11": {
            "Bab 1: Kolonialisme & Perlawanan": {
                "sub_bab": ["Latar Belakang 3G", "VOC & Hindia Belanda", "Dampak Kolonialisme", "Perlawanan Daerah"],
                "rangkuman": "• **Kolonialisme**: Penjajahan Belanda dan perjuangan tokoh lokal (Pangeran Diponegoro, Imam Bonjol)."
            },
            "Bab 2: Pergerakan Nasional": {
                "sub_bab": ["Faktor Lahir", "Organisasi Awal", "Organisasi Radikal", "Sumpah Pemuda 1928", "Peran Pers"],
                "rangkuman": "• **Pergerakan**: Kesadaran kebangsaan melalui pendidikan, Budi Utomo, hingga Sumpah Pemuda."
            },
            "Bab 3: Pendudukan Jepang & Proklamasi": {
                "sub_bab": ["Propaganda 3A", "Kebijakan Romusha", "Perlawanan", "Rengasdengklok", "Proklamasi 1945"],
                "rangkuman": "• **Kemerdekaan**: Kekejaman fasisme Jepang yang berujung pada kekosongan kekuasaan dan Proklamasi 17 Agustus."
            }
        },
        "Kelas 12": {
            "Bab 1: Mempertahankan Kemerdekaan": {
                "sub_bab": ["Ancaman Sekutu/NICA", "Perjuangan Fisik", "Diplomasi", "Pemberontakan Dalam Negeri"],
                "rangkuman": "• **Revolusi Fisik**: Pertempuran sengit (Surabaya, Ambarawa) dan perjanjian di meja perundingan (Linggajati, KMB)."
            },
            "Bab 2: Demokrasi Liberal & Terpimpin": {
                "sub_bab": ["Kabinet Demokrasi Liberal", "Dekrit 1959 & Demokrasi Terpimpin"],
                "rangkuman": "• **Orde Lama**: Dinamika politik pasca kemerdekaan yang penuh pergantian kabinet dan ideologi Nasakom."
            },
            "Bab 3: Orde Baru hingga Reformasi": {
                "sub_bab": ["Lahirnya Orde Baru", "Krisis Moneter 1998", "Masa Reformasi"],
                "rangkuman": "• **Reformasi**: Masa pembangunan Soeharto yang runtuh akibat krisis, memicu era kebebasan berdemokrasi."
            },
            "Bab 4: Indonesia & Dunia": {
                "sub_bab": ["Politik Bebas Aktif", "KAA & GNB", "Misi Garuda", "Pembentukan ASEAN"],
                "rangkuman": "• **Politik Global**: Peran sentral RI dalam menjaga perdamaian dunia sebagai negara non-blok."
            }
        }
    },
    "Ekonomi": {
        "Kelas 10": {
            "Bab 1: Konsep Dasar Ekonomi": {
                "sub_bab": ["Kelangkaan", "Alat Pemuas", "Biaya Peluang", "Prinsip & Motif"],
                "rangkuman": "• **Dasar Ekonomi**: Cara manusia membuat pilihan di tengah kelangkaan sumber daya (Opportunity Cost)."
            },
            "Bab 2: Kegiatan & Pelaku Ekonomi": {
                "sub_bab": ["Produksi & Konsumsi", "Pelaku Ekonomi", "Circular Flow Diagram"],
                "rangkuman": "• **Sistem Ekonomi**: Hubungan rumah tangga, produsen, dan pemerintah dalam perputaran uang."
            },
            "Bab 3: Pasar & Harga": {
                "sub_bab": ["Permintaan", "Penawaran", "Harga Keseimbangan", "Elastisitas", "Struktur Pasar"],
                "rangkuman": "• **Mekanisme Pasar**: Hukum tawar menawar (Supply & Demand) yang membentuk harga kesepakatan pasar."
            },
            "Bab 4: Lembaga Keuangan": {
                "sub_bab": ["OJK", "Perbankan", "Lembaga Non-Bank"],
                "rangkuman": "• **Institusi**: Fungsi bank sentral, bank umum, asuransi, hingga otoritas pengawas (OJK)."
            }
        },
        "Kelas 11": {
            "Bab 1: Pendapatan Nasional": {
                "sub_bab": ["Konsep GDP/GNP", "Metode Penghitungan", "Pendapatan Per Kapita", "Kesenjangan (Gini)"],
                "rangkuman": "• **Makro Ekonomi**: Mengukur kekayaan suatu negara dan menganalisis pemerataan distribusinya."
            },
            "Bab 2: Ketenagakerjaan": {
                "sub_bab": ["Konsep Dasar", "Masalah di Indonesia", "Sistem Upah", "Pengangguran"],
                "rangkuman": "• **Tenaga Kerja**: Isu angkatan kerja, UMR, dan solusi mengurangi berbagai jenis pengangguran."
            },
            "Bab 3: Inflasi & Kebijakan": {
                "sub_bab": ["Inflasi", "Kebijakan Moneter", "Kebijakan Fiskal"],
                "rangkuman": "• **Inflasi**: Kenaikan harga barang secara umum yang diatasi lewat kebijakan pajak dan suku bunga bank."
            }
        },
        "Kelas 12": {
            "Bab 1: APBN dan APBD": {
                "sub_bab": ["Tujuan & Fungsi", "Sumber Pendapatan", "Pengeluaran", "Pengaruh APBN"],
                "rangkuman": "• **Anggaran Negara**: Tata kelola keuangan pemerintah untuk mendanai pembangunan infrastruktur nasional/daerah."
            },
            "Bab 2: Akuntansi Perusahaan Jasa": {
                "sub_bab": ["Karakteristik & Persamaan", "Siklus Akuntansi", "Jurnal Penyesuaian", "Laporan Keuangan", "Jurnal Penutup"],
                "rangkuman": "• **Akuntansi Jasa**: Pembuatan laporan laba/rugi dan neraca dari usaha berbasis layanan (salon, bengkel, dll)."
            },
            "Bab 3: Akuntansi Perusahaan Dagang": {
                "sub_bab": ["Karakteristik Dagang", "Jurnal Khusus", "Buku Besar Pembantu", "Neraca Lajur"],
                "rangkuman": "• **Akuntansi Dagang**: Sistem kompleks yang menghitung Harga Pokok Penjualan (HPP) barang."
            }
        }
    },
    "Sosiologi": {
        "Kelas 10": {
            "Bab 1: Pengantar Sosiologi": {
                "sub_bab": ["Sejarah & Tokoh", "Objek Kajian", "Fungsi Sosiologi"],
                "rangkuman": "• **Sosiologi**: Ilmu yang mengkaji hubungan antarmanusia dan gejala sosial di masyarakat."
            },
            "Bab 2: Interaksi & Hubungan Sosial": {
                "sub_bab": ["Identitas Diri", "Tindakan Sosial", "Syarat Interaksi", "Bentuk Interaksi"],
                "rangkuman": "• **Interaksi**: Proses sosial baik yang menyatukan (Asosiatif) maupun merenggangkan (Disosiatif)."
            },
            "Bab 3: Lembaga, Nilai, & Norma": {
                "sub_bab": ["Nilai & Norma", "Jenis Norma", "Lembaga Sosial"],
                "rangkuman": "• **Norma & Lembaga**: Aturan tak tertulis pengikat masyarakat dan fungsi institusi seperti keluarga & agama."
            }
        },
        "Kelas 11": {
            "Bab 1: Kelompok Sosial": {
                "sub_bab": ["Pembentukan", "Jenis Kelompok", "Dinamika Kelompok"],
                "rangkuman": "• **Kelompok Sosial**: Bagaimana individu berhimpun membentuk in-group, paguyuban, dan patembayan."
            },
            "Bab 2: Permasalahan Sosial": {
                "sub_bab": ["Eksklusi Sosial", "Ketimpangan & Kemiskinan", "Kriminalitas & Korupsi"],
                "rangkuman": "• **Isu Sosial**: Penyakit masyarakat struktural akibat kesenjangan yang tidak teratasi."
            },
            "Bab 3: Konflik & Kekerasan": {
                "sub_bab": ["Akar Penyebab", "Konflik vs Kekerasan", "Resolusi Konflik"],
                "rangkuman": "• **Konflik**: Pertentangan sosial dan cara menyelesaikannya lewat mediasi maupun kompromi."
            }
        },
        "Kelas 12": {
            "Bab 1: Perubahan Sosial": {
                "sub_bab": ["Teori Perubahan", "Faktor Pendorong", "Dampak Modernisasi"],
                "rangkuman": "• **Perubahan Sosial**: Transformasi budaya dari tradisional ke modern serta risiko gegar budaya."
            },
            "Bab 2: Globalisasi & Digitalisasi": {
                "sub_bab": ["Konsep Globalisasi", "Tantangan Konsumerisme", "Komunitas Lokal"],
                "rangkuman": "• **Globalisasi**: Hilangnya batas antarnegara dan upaya melestarikan budaya lokal (Glokalisasi)."
            },
            "Bab 3: Pemberdayaan Komunitas": {
                "sub_bab": ["Kearifan Lokal", "Strategi Pemberdayaan", "Aksi Sosial"],
                "rangkuman": "• **Kearifan Lokal**: Memberdayakan masyarakat berbasis nilai tradisi agar tahan banting di era digital."
            }
        }
    }
}
