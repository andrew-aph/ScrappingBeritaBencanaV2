# 🔥 SIBERNA — Sistem Informasi Berita Bencana Nasional

Dashboard monitoring **berita kebencanaan nasional** yang melakukan **web scraping otomatis dari berbagai portal berita** dan menyajikannya dalam bentuk **dataset, analisis distribusi, serta tabel kejadian bencana**.
Dashboard ini dibangun menggunakan **Python dan Streamlit** untuk membantu memantau informasi bencana secara cepat dan akurat dari berbagai sumber media online.

---

# 📸 Tampilan Dashboard

## 📰 Dataset Berita

Dashboard menampilkan seluruh berita hasil scraping yang telah dikumpulkan dari berbagai portal berita, lengkap dengan judul, tanggal, sumber, tag bencana, dan preview isi berita.

![Dataset Berita](https://github.com/andrew-aph/ScrappingBeritaBencanaV2/blob/main/Tab%201.png)

---

## 📖 Detail & Analisis

Pengguna dapat melihat **distribusi berita per sumber** (donut chart), **tipe bencana** (bar chart), **top provinsi terdampak**, serta **ringkasan isi berita** lengkap dengan tanggal, tag, dan link menuju sumber berita asli.

![Detail Analisis](https://github.com/andrew-aph/ScrappingBeritaBencanaV2/blob/main/Tab%202.png)

---

## 📊 Tabel Kejadian Bencana

Dashboard juga mengekstrak dan merekap informasi kejadian bencana seperti:

- Provinsi terdampak
- Jenis bencana
- Waktu kejadian
- Jumlah KK & jiwa terdampak
- Jumlah pengungsi
- Korban meninggal & luka
- Rumah rusak
- Kronologis kejadian

![Tabel Bencana](https://github.com/andrew-aph/ScrappingBeritaBencanaV2/blob/main/Tab%203.png)

---

# 🚀 Fitur Utama

## 🔎 Multi Source Scraping

Mengambil berita dari berbagai portal berita nasional seperti:

- Detik
- Kompas
- MetroTV

---

## 🔑 Keyword Filtering

Scraping dilakukan berdasarkan keyword kebencanaan tertentu seperti:

- Bencana
- Banjir
- Puting Beliung
- Gelombang Pasang
- Abrasi
- Tanah Longsor
- Kekeringan
- Gempa Bumi
- Gunung Meletus
- Kebakaran Hutan

---

## 📅 Filter Tanggal

Pengguna dapat menentukan rentang waktu scraping berita secara fleksibel.

---

## 📊 Dashboard Monitoring

Menampilkan statistik ringkas secara realtime seperti:

- Total berita terkumpul
- Jumlah sumber portal aktif
- Jumlah jenis bencana terdeteksi
- Status sistem scraping

---

## 📰 Detail Artikel

Menampilkan informasi lengkap setiap artikel:

- Judul berita
- Isi / ringkasan berita
- Tanggal publikasi
- Tag bencana
- Link sumber asli

---

## 📑 Ekstraksi Informasi Kejadian

Sistem secara otomatis mengekstrak informasi penting dari isi berita seperti:

- Provinsi lokasi kejadian
- Jenis bencana
- Jumlah korban terdampak
- Jumlah pengungsi
- Kerusakan yang ditimbulkan

---

# 🛠️ Tech Stack

Project ini dibangun menggunakan:

- Python
- Streamlit
- BeautifulSoup
- Requests
- Pandas

---

# ⚙️ Cara Kerja Sistem

1. User memilih:
   - Sumber berita (portal)
   - Keyword kebencanaan
   - Rentang tanggal pemantauan
2. Sistem melakukan scraping berita dari setiap website yang dipilih.
3. Data yang diambil meliputi:
   - Judul berita
   - Tanggal publikasi
   - Isi berita
   - Link berita
4. Sistem melakukan **ekstraksi informasi kejadian bencana** secara otomatis dari isi berita.
5. Hasil ditampilkan pada dashboard Streamlit dalam tiga tab: Dataset Berita, Detail & Analisis, dan Tabel Kejadian Bencana.

---

# 📌 Use Case

Dashboard ini dapat digunakan untuk:

- Monitoring berita kebencanaan secara realtime
- Analisis distribusi kejadian bencana berbasis berita
- Early information monitoring untuk respons cepat
- Rekapitulasi data bencana nasional

---

# ⚠️ Disclaimer

Data diperoleh dari hasil scraping portal berita dan hanya digunakan untuk tujuan:

- Analisis data
- Monitoring informasi publik

---

# 👨‍💻 Author

Developed by **Andrew Putra Hartanto**
