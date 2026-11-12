# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

**Nama:** Luthfia Ramadhani  
**ID Dicoding:** luthfia_ramadhan20gf  

---

## Deskripsi Proyek
Proyek ini merupakan hasil analisis data terhadap transaksi E-Commerce Olist pada periode **September 2016 hingga Agustus 2018** menggunakan Python. Analisis difokuskan untuk menjawab permasalahan bisnis terkait segmentasi perilaku pelanggan menggunakan metode RFM (*Recency, Frequency, Monetary*), pemetaan sebaran jumlah pelanggan dan total nilai transaksi (*revenue*) berdasarkan negara bagian (*state*), serta evaluasi dampak ketepatan waktu pengiriman terhadap tingkat kepuasan pelanggan (*review score*). 

Seluruh tahapan mulai dari *data wrangling*, eksplorasi data (EDA), hingga visualisasi disajikan secara terstruktur di dalam *notebook*, serta dirangkum ke dalam *dashboard* interaktif berbasis Streamlit untuk memudahkan pemantauan wawasan bisnis.

---

## Struktur Direktori
Berikut adalah susunan lengkap folder dan file di dalam proyek ini:

```text
PROYEK-ANALISIS-DATA/
├── dashboard/
│   ├── dashboard.py               # Kode utama aplikasi dashboard interaktif Streamlit
│   └── main_data.csv              # Dataset bersih hasil penggabungan untuk kebutuhan dashboard
├── data/
│   ├── customers_dataset.csv      # Data profil pelanggan dan lokasi geografis (kota & state)
│   ├── order_items_dataset.csv    # Data rincian item, harga produk, dan ongkos kirim per pesanan
│   ├── order_payments_dataset.csv # Data metode dan total nominal pembayaran transaksi
│   ├── order_reviews_dataset.csv  # Data skor ulasan (rating 1-5) dan komentar pelanggan
│   ├── orders_dataset.csv         # Data histori status pesanan dan waktu proses pengiriman
│   └── products_dataset.csv       # Data katalog dan kategori produk
├── Proyek_Analisis_Data.ipynb     # File notebook berisi proses analisis data lengkap & kesimpulan
├── README.md                      # Dokumentasi proyek dan panduan menjalankan dashboard
├── requirements.txt               # Daftar library Python yang dibutuhkan untuk menjalankan proyek
└── url.txt                        # Tautan live dashboard yang sudah di-deploy ke Streamlit Cloud
```

---

## Kebutuhan Dataset
Aplikasi *dashboard* (`dashboard/dashboard.py`) membaca dataset hasil pengolahan (`main_data.csv`) yang tersimpan di dalam folder `dashboard/`, sedangkan proses analisis dari awal pada `Proyek_Analisis_Data.ipynb` menggunakan enam dataset utama di dalam folder `data/`. Sebelum menjalankan aplikasi secara lokal, pastikan seluruh file berikut tersedia di direktorinya masing-masing:
- `dashboard/main_data.csv`
- `data/customers_dataset.csv`
- `data/order_items_dataset.csv`
- `data/order_payments_dataset.csv`
- `data/order_reviews_dataset.csv`
- `data/orders_dataset.csv`
- `data/products_dataset.csv`

---

## Panduan Menjalankan Dashboard Secara Lokal

### 1. Persiapan Virtual Environment
Buka terminal atau Command Prompt, arahkan ke direktori utama proyek (`PROYEK-ANALISIS-DATA`), lalu buat *virtual environment* baru agar instalasi *library* terisolasi dengan baik:

```bash
python -m venv .venv
```

Setelah proses pembuatan selesai, aktifkan *virtual environment* sesuai dengan sistem operasi yang digunakan:
- **Windows (Command Prompt / PowerShell):**
  ```bash
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 2. Instalasi Dependensi
Pastikan terminal sudah berada di direktori utama proyek (tempat file `requirements.txt` berada) dan *virtual environment* `.venv` sudah aktif, lalu jalankan perintah berikut:

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard Streamlit
Setelah seluruh dependensi berhasil terinstal, jalankan aplikasi *dashboard* dari direktori utama proyek dengan perintah:

```bash
streamlit run dashboard/dashboard.py
```

### 4. Pengujian Aplikasi
Setelah perintah di atas dijalankan, aplikasi *dashboard* akan otomatis terbuka di peramban (*browser*) pada alamat `http://localhost:8501`. Lakukan pengecekan pada halaman *dashboard* untuk memastikan:
- Ringkasan metrik utama (*Total Orders*, *Total Revenue*, dan *Average Rating*) tampil dengan akurat.
- Seluruh grafik visualisasi (Segmentasi Pelanggan RFM, Top State berdasarkan Pelanggan & Revenue, serta Perbandingan Skor Ulasan Pengiriman) muncul tanpa pesan *error*.
- Fitur filter interaktif di bagian *sidebar* (seperti filter rentang tanggal dan filter wilayah/kategori) berfungsi mengubah tampilan visualisasi data secara responsif.

---

## Tautan Dashboard Live
Selain dijalankan secara lokal, *dashboard* interaktif ini juga dapat diakses secara daring melalui Streamlit Cloud pada tautan berikut:  
[https://dashboard-olist-luthfia.streamlit.app/]